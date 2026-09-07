const fs = require('node:fs');
const { test, expect } = require('@playwright/test');

async function workspace(page) {
  const root = page.locator('dealix-catalog-workspace');
  await expect(root).toBeVisible();
  await expect(root.locator('.card')).toHaveCount(100);
  return root;
}

test('market-to-delivery catalog is truthful, filterable and browser-local', async ({ page }) => {
  const postRequests = [];
  page.on('request', (request) => {
    if (request.method() === 'POST') postRequests.push(request.url());
  });

  await page.goto('/app/service-catalog');
  const root = await workspace(page);

  await expect(root.locator('.brand')).toContainText('DEALIX');
  await expect(root.locator('.notice')).toContainText('كتالوج بحثي');
  await expect(root.locator('.stat .num')).toHaveText(['8', '20', '100']);

  await root.locator('#sector').selectOption('construction');
  await expect(root.locator('.card')).toHaveCount(5);

  await root.locator('#search').fill('RFI');
  await expect(root.locator('.card')).toHaveCount(1);
  await expect(root.locator('.card h2')).toContainText('RFI');

  await root.locator('.choose').click();
  await expect(root.locator('.intake')).toBeVisible();

  await root.locator('#tenant_id').fill('synthetic-tenant');
  await root.locator('#problem').fill('Synthetic RFI handoff requirement');
  await root.locator('#authorized').check();

  const downloadPromise = page.waitForEvent('download');
  await root.locator('.save').click();
  const download = await downloadPromise;
  const path = await download.path();
  const payload = JSON.parse(fs.readFileSync(path, 'utf8'));

  expect(payload.tenant_id).toBe('synthetic-tenant');
  expect(payload.project_id).toBe('construction-01');
  expect(payload.data_authorized).toBe(true);
  expect(payload.evidence_refs).toEqual([]);
  expect(postRequests).toEqual([]);
  await expect(root.locator('.status')).not.toHaveText('');

  await root.locator('.lang').click();
  await expect(root.locator('h1')).toHaveText('From need to delivery plan');

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  expect(overflow).toBe(false);
});

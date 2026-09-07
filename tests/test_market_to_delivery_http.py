"""Run in a full repository environment; existing auth and catalog imports required."""
import os
import secrets
import unittest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routers.service_catalog import router

class HttpTests(unittest.TestCase):
    def setUp(self):
        self.key=secrets.token_urlsafe(32)
        self.env=patch.dict(os.environ, {'APP_ENV':'production','ADMIN_API_KEYS':self.key,'DEALIX_ADMIN_API_KEY':''})
        self.env.start()
        app=FastAPI();app.include_router(router);self.client=TestClient(app)
        self.path='/api/v1/services/market-to-delivery/prepare'
        self.input={'tenant_id':'test','request_id':'test-1','project_id':'construction-01','problem':'Synthetic requirement','data_authorized':True}
    def tearDown(self): self.env.stop()
    def test_missing_admin_denied(self):
        self.assertEqual(self.client.post(self.path,json=self.input).status_code,401)
    def test_wrong_admin_denied(self):
        self.assertEqual(self.client.post(self.path,json=self.input,headers={'X-Admin-API-Key':secrets.token_urlsafe(32)}).status_code,403)
    def test_unconfigured_auth_denied(self):
        with patch.dict(os.environ,{'ADMIN_API_KEYS':'','DEALIX_ADMIN_API_KEY':'','APP_ENV':'development'}):
            self.assertEqual(self.client.post(self.path,json=self.input).status_code,503)
    def test_authorized_preparation_remains_draft(self):
        r=self.client.post(self.path,json=self.input,headers={'X-Admin-API-Key':self.key})
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()['status'],'NEEDS_INPUT')
        self.assertTrue(all(v is False for v in r.json()['authority'].values()))
    def test_privilege_injection_rejected(self):
        r=self.client.post(self.path,json={**self.input,'auto_approve':True},headers={'X-Admin-API-Key':self.key})
        self.assertEqual(r.status_code,422)
    def test_research_catalog_requires_admin(self):
        self.assertEqual(self.client.get('/api/v1/services/market-to-delivery/catalog').status_code,401)

if __name__=='__main__':unittest.main()

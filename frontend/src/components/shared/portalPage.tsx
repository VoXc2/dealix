import { getTranslations } from "next-intl/server";
import { PortalPlaceholder } from "@/components/shared/PortalPlaceholder";

interface PageParams {
  params: Promise<{ locale: string }>;
}

/**
 * Builds a scaffolded portal route. Each Full Ops portal page is a thin
 * `export default makePortalPage(slug, group)` over this factory.
 */
export function makePortalPage(slug: string, group: string) {
  return async function PortalPage({ params }: PageParams) {
    const { locale } = await params;
    const t = await getTranslations({ locale, namespace: "portals" });
    return (
      <PortalPlaceholder
        portal={t(`groups.${group}`)}
        title={t(`pages.${slug}.title`)}
        subtitle={t(`pages.${slug}.subtitle`)}
        phase={t(`pages.${slug}.phase`)}
        phaseLabel={t("phaseLabel")}
        scopeLabel={t("scopeLabel")}
        scope={t.raw(`pages.${slug}.scope`) as string[]}
        backHref={`/${locale}/dashboard`}
        backLabel={t("backLabel")}
      />
    );
  };
}

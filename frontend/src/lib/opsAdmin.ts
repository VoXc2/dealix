const LS_KEY = "dealix_admin_api_key";

export function getAdminApiKey(): string {
  if (typeof window === "undefined") return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? "";
  return (
    localStorage.getItem(LS_KEY) ||
    process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ||
    ""
  );
}

export function isOpsConfigured(): boolean {
  return getAdminApiKey().trim().length > 0;
}

export function opsMissingKeyMessage(isAr?: boolean): string {
  return isAr
    ? "يرجى إدخال مفتاح API للمشرف للمتابعة."
    : "Please set your admin API key to continue.";
}

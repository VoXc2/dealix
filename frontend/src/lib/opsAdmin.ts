const LS_KEY = "dealix_admin_api_key";

export function getAdminApiKey(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem(LS_KEY) || "";
}

export function isOpsConfigured(): boolean {
  return getAdminApiKey().trim().length > 0;
}

export function opsMissingKeyMessage(isAr?: boolean): string {
  return isAr
    ? "يرجى تسجيل الدخول أو إدخال مفتاح API للمشرف محليًا للمتابعة."
    : "Please sign in or set your admin API key locally to continue.";
}

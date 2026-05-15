/**
 * Single source of truth for JWT + user blobs in localStorage.
 * Used by apiClient interceptors and AuthProvider (Axios-only HTTP).
 */
import type { AuthTokens, User } from "@/types";

export const AUTH_STORAGE_KEYS = {
  access: "dealix_access_token",
  refresh: "dealix_refresh_token",
  expires: "dealix_expires_at",
  user: "dealix_user",
} as const;

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

function parseJson<T>(raw: string | null): T | null {
  if (!raw) return null;
  try {
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

export function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return parseJson<string>(localStorage.getItem(AUTH_STORAGE_KEYS.access));
}

export function getStoredRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return parseJson<string>(localStorage.getItem(AUTH_STORAGE_KEYS.refresh));
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  return parseJson<User>(localStorage.getItem(AUTH_STORAGE_KEYS.user));
}

export function persistAuthResponse(data: LoginResponse): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(
    AUTH_STORAGE_KEYS.access,
    JSON.stringify(data.tokens.accessToken),
  );
  localStorage.setItem(
    AUTH_STORAGE_KEYS.refresh,
    JSON.stringify(data.tokens.refreshToken),
  );
  localStorage.setItem(
    AUTH_STORAGE_KEYS.expires,
    JSON.stringify(data.tokens.expiresAt),
  );
  localStorage.setItem(AUTH_STORAGE_KEYS.user, JSON.stringify(data.user));
  window.dispatchEvent(
    new CustomEvent<LoginResponse>("dealix-auth-updated", { detail: data }),
  );
}

export function clearAuthStorage(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(AUTH_STORAGE_KEYS.access);
  localStorage.removeItem(AUTH_STORAGE_KEYS.refresh);
  localStorage.removeItem(AUTH_STORAGE_KEYS.expires);
  localStorage.removeItem(AUTH_STORAGE_KEYS.user);
  window.dispatchEvent(new Event("dealix-auth-cleared"));
}

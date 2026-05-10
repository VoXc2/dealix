"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import type { User, AuthTokens } from "@/types";
import {
  AUTH_STORAGE_KEYS,
  clearAuthStorage,
  getStoredAccessToken,
  getStoredRefreshToken,
  getStoredUser,
  persistAuthResponse,
  type LoginResponse,
} from "@/lib/auth-storage";
import { apiClient } from "@/lib/api";
import axios from "axios";

function extractApiErrorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as { message?: string; detail?: string } | undefined;
    return data?.message || data?.detail || err.message || fallback;
  }
  if (err instanceof Error) return err.message;
  return fallback;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
}

interface RegisterPayload {
  email: string;
  password: string;
  fullName: string;
  company: string;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

function readExpiresAt(): number | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(AUTH_STORAGE_KEYS.expires);
    return raw ? (JSON.parse(raw) as number) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const clearAuth = useCallback(() => {
    setUser(null);
    setToken(null);
    clearAuthStorage();
  }, []);

  const persistAuth = useCallback((tokens: AuthTokens, userData: User) => {
    persistAuthResponse({ user: userData, tokens });
    setToken(tokens.accessToken);
    setUser(userData);
  }, []);

  const refreshToken = useCallback(async (): Promise<string | null> => {
    const refresh = getStoredRefreshToken();
    if (!refresh) return null;

    try {
      const { data } = await apiClient.post<LoginResponse>(
        "/api/v1/auth/refresh",
        { refresh_token: refresh },
      );
      persistAuthResponse(data);
      setToken(data.tokens.accessToken);
      setUser(data.user);
      return data.tokens.accessToken;
    } catch {
      clearAuth();
      return null;
    }
  }, [clearAuth]);

  useEffect(() => {
    const onUpdated = (e: Event) => {
      const ce = e as CustomEvent<LoginResponse>;
      if (ce.detail?.tokens && ce.detail?.user) {
        setToken(ce.detail.tokens.accessToken);
        setUser(ce.detail.user);
      }
    };
    const onCleared = () => {
      setUser(null);
      setToken(null);
    };
    window.addEventListener("dealix-auth-updated", onUpdated);
    window.addEventListener("dealix-auth-cleared", onCleared);
    return () => {
      window.removeEventListener("dealix-auth-updated", onUpdated);
      window.removeEventListener("dealix-auth-cleared", onCleared);
    };
  }, []);

  useEffect(() => {
    const storedToken = getStoredAccessToken();
    const storedUser = getStoredUser();
    const expiresAt = readExpiresAt();

    if (storedToken && storedUser) {
      if (expiresAt && Date.now() > expiresAt) {
        refreshToken().finally(() => setIsLoading(false));
      } else {
        setToken(storedToken);
        setUser(storedUser);
        setIsLoading(false);
      }
    } else {
      setIsLoading(false);
    }
  }, [refreshToken]);

  useEffect(() => {
    const expiresAt = readExpiresAt();
    if (!expiresAt || !token) return;

    const msUntilExpiry = expiresAt - Date.now();
    const refreshBuffer = 60_000;
    const delay = Math.max(msUntilExpiry - refreshBuffer, 0);

    const timer = setTimeout(() => {
      refreshToken();
    }, delay);

    return () => clearTimeout(timer);
  }, [token, refreshToken]);

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        const { data } = await apiClient.post<LoginResponse>(
          "/api/v1/auth/login",
          { email, password },
        );
        persistAuth(data.tokens, data.user);
      } catch (e: unknown) {
        const msg = extractApiErrorMessage(e, "Login failed");
        throw new Error(msg);
      }
    },
    [persistAuth],
  );

  const register = useCallback(
    async (payload: RegisterPayload) => {
      try {
        const { data } = await apiClient.post<LoginResponse>(
          "/api/v1/auth/register",
          payload,
        );
        persistAuth(data.tokens, data.user);
      } catch (e: unknown) {
        const msg = extractApiErrorMessage(e, "Registration failed");
        throw new Error(msg);
      }
    },
    [persistAuth],
  );

  const logout = useCallback(async () => {
    const refresh = getStoredRefreshToken();
    const access = token ?? getStoredAccessToken();
    try {
      await apiClient.post(
        "/api/v1/auth/logout",
        { refresh_token: refresh },
        {
          headers: access ? { Authorization: `Bearer ${access}` } : {},
        },
      );
    } catch {
      // Best-effort logout call
    }
    clearAuth();
  }, [token, clearAuth]);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}

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

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

const TOKEN_KEY = "dealix_access_token";
const REFRESH_KEY = "dealix_refresh_token";
const EXPIRES_KEY = "dealix_expires_at";
const USER_KEY = "dealix_user";

function getStored<T>(key: string): T | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function setStored(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  localStorage.setItem(key, JSON.stringify(value));
}

function removeStored(...keys: string[]) {
  if (typeof window === "undefined") return;
  keys.forEach((k) => localStorage.removeItem(k));
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const clearAuth = useCallback(() => {
    setUser(null);
    setToken(null);
    removeStored(TOKEN_KEY, REFRESH_KEY, EXPIRES_KEY, USER_KEY);
  }, []);

  const persistAuth = useCallback((tokens: AuthTokens, userData: User) => {
    setStored(TOKEN_KEY, tokens.accessToken);
    setStored(REFRESH_KEY, tokens.refreshToken);
    setStored(EXPIRES_KEY, tokens.expiresAt);
    setStored(USER_KEY, userData);
    setToken(tokens.accessToken);
    setUser(userData);
  }, []);

  const refreshToken = useCallback(async (): Promise<string | null> => {
    const refresh = getStored<string>(REFRESH_KEY);
    if (!refresh) return null;

    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refresh }),
      });
      if (!res.ok) throw new Error("Refresh failed");

      const data: LoginResponse = await res.json();
      persistAuth(data.tokens, data.user);
      return data.tokens.accessToken;
    } catch {
      clearAuth();
      return null;
    }
  }, [persistAuth, clearAuth]);

  useEffect(() => {
    const storedToken = getStored<string>(TOKEN_KEY);
    const storedUser = getStored<User>(USER_KEY);
    const expiresAt = getStored<number>(EXPIRES_KEY);

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
    const expiresAt = getStored<number>(EXPIRES_KEY);
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
      const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.message || "Login failed");
      }
      const data: LoginResponse = await res.json();
      persistAuth(data.tokens, data.user);
    },
    [persistAuth],
  );

  const register = useCallback(
    async (data: RegisterPayload) => {
      const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.message || "Registration failed");
      }
      const result: LoginResponse = await res.json();
      persistAuth(result.tokens, result.user);
    },
    [persistAuth],
  );

  const logout = useCallback(async () => {
    const refresh = getStored<string>(REFRESH_KEY);
    try {
      await fetch(`${API_BASE}/api/v1/auth/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ refresh_token: refresh }),
      });
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

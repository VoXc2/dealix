import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// Token storage helpers (SSR-safe)
export const tokenStorage = {
  getAccessToken: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("dealix_access_token");
  },
  setAccessToken: (token: string): void => {
    if (typeof window !== "undefined") {
      localStorage.setItem("dealix_access_token", token);
    }
  },
  getRefreshToken: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("dealix_refresh_token");
  },
  setRefreshToken: (token: string): void => {
    if (typeof window !== "undefined") {
      localStorage.setItem("dealix_refresh_token", token);
    }
  },
  clear: (): void => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("dealix_access_token");
      localStorage.removeItem("dealix_refresh_token");
    }
  },
};

// Create base axios instance
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Request interceptor – attach JWT
  client.interceptors.request.use(
    (config) => {
      const token = tokenStorage.getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor – handle 401 token refresh
  client.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as AxiosRequestConfig & {
        _retry?: boolean;
      };

      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const refreshToken = tokenStorage.getRefreshToken();

        if (refreshToken) {
          try {
            const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });
            const { access_token } = response.data;
            tokenStorage.setAccessToken(access_token);

            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
            }
            return client(originalRequest);
          } catch {
            tokenStorage.clear();
            if (typeof window !== "undefined") {
              window.location.href = "/ar/login";
            }
          }
        } else {
          tokenStorage.clear();
          if (typeof window !== "undefined") {
            window.location.href = "/ar/login";
          }
        }
      }

      return Promise.reject(error);
    }
  );

  return client;
};

export const apiClient = createApiClient();
export default apiClient;

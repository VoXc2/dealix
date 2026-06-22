import apiClient, { tokenStorage } from "./client";
import type { User, AuthTokens } from "@/types";

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  fullName: string;
  company: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    // FastAPI OAuth2 form-based login
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await apiClient.post<AuthResponse>("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const { access_token, refresh_token } = response.data;
    tokenStorage.setAccessToken(access_token);
    tokenStorage.setRefreshToken(refresh_token);

    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>("/auth/register", data);
    const { access_token, refresh_token } = response.data;
    tokenStorage.setAccessToken(access_token);
    tokenStorage.setRefreshToken(refresh_token);
    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await apiClient.post("/auth/logout");
    } finally {
      tokenStorage.clear();
    }
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>("/auth/me");
    return response.data;
  },

  refreshTokens: async (): Promise<AuthTokens> => {
    const refreshToken = tokenStorage.getRefreshToken();
    const response = await apiClient.post<AuthTokens>("/auth/refresh", {
      refresh_token: refreshToken,
    });
    tokenStorage.setAccessToken(response.data.accessToken);
    return response.data;
  },
};

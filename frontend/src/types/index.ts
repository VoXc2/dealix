export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Deal {
  id: number;
  title: string;
  stage: string;
  original_price: number;
  deal_price: number;
  discount_percentage: number;
  is_active: boolean;
  created_at: string;
}

export interface Lead {
  id: number;
  full_name: string;
  email: string;
  status: string;
  score: string;
  source: string;
  created_at: string;
}

export interface Meeting {
  id: number;
  title: string;
  meeting_type: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

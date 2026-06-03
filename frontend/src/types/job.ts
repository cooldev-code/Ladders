export type SalaryPeriod = "annual" | "hourly";

export type EmploymentType =
  | "full_time"
  | "part_time"
  | "contract"
  | "internship"
  | "other";

export interface Location {
  city: string;
  state: string;
  country: string;
  is_remote: boolean;
}

export interface Salary {
  amount: number;
  currency: string;
  period: SalaryPeriod;
  display: string;
}

export interface Job {
  id: string;
  title: string;
  description: string;
  company: string;
  location: Location;
  salary: Salary;
  employment_type: EmploymentType;
  posting_date: string | null;
  company_type: string;
  language: string;
}

export type SortField = "salary" | "posting_date";
export type SortOrder = "asc" | "desc";

export interface JobSearchParams {
  q?: string;
  country?: string;
  sort_by?: SortField;
  order?: SortOrder;
  page?: number;
  page_size?: number;
}

export interface PaginatedJobs {
  items: Job[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface CatalogStats {
  total: number;
  remote: number;
  countries: number;
}

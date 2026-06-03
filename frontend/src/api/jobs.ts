import type { CatalogStats, JobSearchParams, PaginatedJobs } from "@/types/job";

function buildQuery(params: JobSearchParams): string {
  const search = new URLSearchParams();
  if (params.q) search.set("q", params.q);
  if (params.country) search.set("country", params.country);
  if (params.sort_by) search.set("sort_by", params.sort_by);
  if (params.order) search.set("order", params.order);
  if (params.page) search.set("page", String(params.page));
  if (params.page_size) search.set("page_size", String(params.page_size));
  const query = search.toString();
  return query ? `?${query}` : "";
}

export async function fetchJobs(
  params: JobSearchParams = {},
): Promise<PaginatedJobs> {
  const response = await fetch(`/api/jobs${buildQuery(params)}`);
  if (!response.ok) {
    throw new Error(`Failed to load jobs (${response.status})`);
  }
  return response.json();
}

export async function fetchCatalogStats(): Promise<CatalogStats> {
  const response = await fetch("/api/stats");
  if (!response.ok) {
    throw new Error(`Failed to load stats (${response.status})`);
  }
  return response.json();
}

import { useEffect, useState } from "react";

import { fetchJobs } from "@/api/jobs";
import type { Job, JobSearchParams, PaginatedJobs } from "@/types/job";
import { useDebouncedValue } from "@/hooks/useDebouncedValue";

interface UseJobsResult {
  jobs: Job[];
  meta: Omit<PaginatedJobs, "items"> | null;
  loading: boolean;
  error: string | null;
}

export function useJobs(params: JobSearchParams): UseJobsResult {
  const debouncedQuery = useDebouncedValue(params.q ?? "");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [meta, setMeta] = useState<Omit<PaginatedJobs, "items"> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const effectiveParams: JobSearchParams = {
    ...params,
    q: debouncedQuery || undefined,
  };
  const requestKey = JSON.stringify(effectiveParams);

  useEffect(() => {
    let cancelled = false;

    async function loadJobs() {
      setLoading(true);
      setError(null);
      try {
        const { items, ...rest } = await fetchJobs(effectiveParams);
        if (!cancelled) {
          setJobs(items);
          setMeta(rest);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unknown error");
          setJobs([]);
          setMeta(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadJobs();
    return () => {
      cancelled = true;
    };
    // requestKey captures every field of effectiveParams
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [requestKey]);

  return { jobs, meta, loading, error };
}

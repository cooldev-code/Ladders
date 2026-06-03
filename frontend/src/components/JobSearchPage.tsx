import { useEffect, useState } from "react";

import type { JobSearchParams } from "@/types/job";
import { useJobs } from "@/hooks/useJobs";
import { useCatalogStats } from "@/hooks/useCatalogStats";
import { SiteHeader } from "@/components/SiteHeader";
import { HeroSearch } from "@/components/HeroSearch";
import { JobFilters } from "@/components/JobFilters";
import { JobList, JobListSkeleton } from "@/components/JobList";
import { EmptyState, ErrorState } from "@/components/JobStates";
import { PAGE_SIZE_OPTIONS, Pagination } from "@/components/Pagination";

const defaultParams: JobSearchParams = {
  sort_by: "posting_date",
  order: "desc",
  page: 1,
  page_size: PAGE_SIZE_OPTIONS[0],
};

export function JobSearchPage() {
  const [params, setParams] = useState<JobSearchParams>(defaultParams);
  const { jobs, meta, loading, error } = useJobs(params);
  const stats = useCatalogStats();

  const applyFilters = (patch: Partial<JobSearchParams>) => {
    setParams((prev) => ({ ...prev, ...patch, page: 1 }));
  };

  const goToPage = (page: number) => {
    setParams((prev) => ({ ...prev, page }));
  };

  const changePageSize = (pageSize: number) => {
    setParams((prev) => ({ ...prev, page_size: pageSize, page: 1 }));
  };

  const clearFilters = () => setParams(defaultParams);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [params.page, params.page_size]);

  const showResults = !loading && !error && jobs.length > 0;
  const showEmpty = !loading && !error && jobs.length === 0;

  return (
    <div className="min-h-screen">
      <SiteHeader />

      <main className="mx-auto max-w-6xl px-4 pb-20 pt-5 md:px-6">
        <HeroSearch
          query={params.q ?? ""}
          onQueryChange={(value) => applyFilters({ q: value })}
          totalJobs={stats?.total ?? 0}
          remoteJobs={stats?.remote ?? 0}
          countries={stats?.countries ?? 0}
        />

        <div className="mt-6 space-y-5">
          <JobFilters
            params={params}
            onChange={applyFilters}
            resultCount={meta?.total ?? jobs.length}
            loading={loading}
          />

          {loading && <JobListSkeleton />}
          {!loading && error && <ErrorState message={error} />}
          {showEmpty && <EmptyState onClear={clearFilters} />}

          {showResults && (
            <>
              <JobList jobs={jobs} />
              {meta && (
                <div className="border-t pt-4">
                  <Pagination
                    page={meta.page}
                    pageSize={meta.page_size}
                    totalPages={meta.total_pages}
                    total={meta.total}
                    hasPrev={meta.has_prev}
                    hasNext={meta.has_next}
                    onPageChange={goToPage}
                    onPageSizeChange={changePageSize}
                  />
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

import {
  ArrowDownNarrowWideIcon,
  ArrowUpNarrowWideIcon,
  GlobeIcon,
} from "lucide-react";

import type { JobSearchParams, SortField, SortOrder } from "@/types/job";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface JobFiltersProps {
  params: JobSearchParams;
  onChange: (params: JobSearchParams) => void;
  resultCount: number;
  loading: boolean;
}

export function JobFilters({
  params,
  onChange,
  resultCount,
  loading,
}: JobFiltersProps) {
  const update = (patch: Partial<JobSearchParams>) => {
    onChange({ ...params, ...patch });
  };

  const order: SortOrder = params.order ?? "desc";

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm font-medium text-muted-foreground">
        {loading ? (
          "Searching roles..."
        ) : (
          <>
            <span className="font-bold text-foreground">{resultCount}</span>{" "}
            {resultCount === 1 ? "role" : "roles"} found
          </>
        )}
      </p>

      <div className="flex flex-wrap items-center gap-2">
        <div className="flex items-center gap-2 rounded-lg border bg-card px-2.5 shadow-xs">
          <GlobeIcon className="size-4 text-muted-foreground" />
          <Select
            value={params.country ?? "all"}
            onValueChange={(value) =>
              update({ country: value === "all" ? undefined : value })
            }
          >
            <SelectTrigger className="h-9 w-[130px] border-0 bg-transparent px-0 shadow-none focus-visible:ring-0">
              <SelectValue placeholder="All countries" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All countries</SelectItem>
              <SelectItem value="USA">United States</SelectItem>
              <SelectItem value="Canada">Canada</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Select
          value={params.sort_by ?? "posting_date"}
          onValueChange={(value) => update({ sort_by: value as SortField })}
        >
          <SelectTrigger className="h-9 w-[150px] bg-card shadow-xs">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="posting_date">Newest first</SelectItem>
            <SelectItem value="salary">Salary</SelectItem>
          </SelectContent>
        </Select>

        <button
          type="button"
          onClick={() => update({ order: order === "desc" ? "asc" : "desc" })}
          className="inline-flex h-9 items-center gap-1.5 rounded-lg border bg-card px-3 text-sm font-medium shadow-xs transition-colors hover:bg-accent"
          title={order === "desc" ? "Descending" : "Ascending"}
        >
          {order === "desc" ? (
            <ArrowDownNarrowWideIcon className="size-4" />
          ) : (
            <ArrowUpNarrowWideIcon className="size-4" />
          )}
          <span className="hidden sm:inline">
            {order === "desc" ? "High to low" : "Low to high"}
          </span>
        </button>
      </div>
    </div>
  );
}

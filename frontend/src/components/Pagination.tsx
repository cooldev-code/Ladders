import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const PAGE_SIZE_OPTIONS = [5, 10, 20] as const;

interface PaginationProps {
  page: number;
  pageSize: number;
  totalPages: number;
  total: number;
  hasPrev: boolean;
  hasNext: boolean;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
}

function getPageItems(page: number, totalPages: number): (number | "...")[] {
  if (totalPages <= 7) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  const items: (number | "...")[] = [1];
  const start = Math.max(2, page - 1);
  const end = Math.min(totalPages - 1, page + 1);

  if (start > 2) items.push("...");
  for (let i = start; i <= end; i += 1) items.push(i);
  if (end < totalPages - 1) items.push("...");

  items.push(totalPages);
  return items;
}

export function Pagination({
  page,
  pageSize,
  totalPages,
  total,
  hasPrev,
  hasNext,
  onPageChange,
  onPageSizeChange,
}: PaginationProps) {
  const items = getPageItems(page, totalPages);
  const start = total === 0 ? 0 : (page - 1) * pageSize + 1;
  const end = Math.min(page * pageSize, total);

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
        <span>
          Showing{" "}
          <span className="font-medium text-foreground">
            {start}–{end}
          </span>{" "}
          of{" "}
          <span className="font-medium text-foreground">{total}</span>
        </span>

        <div className="flex items-center gap-2">
          <span className="text-xs">Per page</span>
          <Select
            value={String(pageSize)}
            onValueChange={(value) => onPageSizeChange(Number(value))}
          >
            <SelectTrigger className="h-8 w-[72px] bg-card shadow-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {PAGE_SIZE_OPTIONS.map((size) => (
                <SelectItem key={size} value={String(size)}>
                  {size}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {totalPages > 1 && (
        <nav
          className="flex items-center justify-center gap-1.5 sm:justify-end"
          aria-label="Pagination"
        >
          <button
            type="button"
            onClick={() => onPageChange(page - 1)}
            disabled={!hasPrev}
            className="inline-flex h-8 items-center gap-1 rounded-lg border bg-card px-2.5 text-sm font-medium shadow-xs transition-colors hover:bg-accent disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeftIcon className="size-4" />
            <span className="hidden sm:inline">Previous</span>
          </button>

          <div className="flex items-center gap-1">
            {items.map((item, index) =>
              item === "..." ? (
                <span
                  key={`gap-${index}`}
                  className="px-1.5 text-sm text-muted-foreground"
                >
                  ...
                </span>
              ) : (
                <button
                  key={item}
                  type="button"
                  onClick={() => onPageChange(item)}
                  aria-current={item === page ? "page" : undefined}
                  className={cn(
                    "inline-flex size-8 items-center justify-center rounded-lg text-sm font-medium transition-colors",
                    item === page
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "border bg-card shadow-xs hover:bg-accent",
                  )}
                >
                  {item}
                </button>
              ),
            )}
          </div>

          <button
            type="button"
            onClick={() => onPageChange(page + 1)}
            disabled={!hasNext}
            className="inline-flex h-8 items-center gap-1 rounded-lg border bg-card px-2.5 text-sm font-medium shadow-xs transition-colors hover:bg-accent disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span className="hidden sm:inline">Next</span>
            <ChevronRightIcon className="size-4" />
          </button>
        </nav>
      )}
    </div>
  );
}

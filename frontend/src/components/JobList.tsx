import type { Job } from "@/types/job";
import { JobCard } from "@/components/JobCard";
import { Skeleton } from "@/components/ui/skeleton";

interface JobListProps {
  jobs: Job[];
}

function JobCardSkeleton() {
  return (
    <div className="flex gap-4 rounded-2xl border border-border/70 bg-card p-5 shadow-sm">
      <Skeleton className="size-12 shrink-0 rounded-xl" />
      <div className="flex-1 space-y-3">
        <Skeleton className="h-4 w-1/2" />
        <Skeleton className="h-3 w-1/3" />
        <Skeleton className="h-3 w-2/3" />
        <div className="flex gap-2 pt-1">
          <Skeleton className="h-6 w-24 rounded-lg" />
          <Skeleton className="h-6 w-20 rounded-lg" />
        </div>
      </div>
    </div>
  );
}

export function JobListSkeleton() {
  return (
    <div className="grid gap-4">
      {Array.from({ length: 5 }).map((_, index) => (
        <JobCardSkeleton key={index} />
      ))}
    </div>
  );
}

export function JobList({ jobs }: JobListProps) {
  return (
    <div className="grid gap-4">
      {jobs.map((job, index) => (
        <div
          key={job.id}
          className="animate-fade-in-up"
          style={{ animationDelay: `${Math.min(index, 8) * 40}ms` }}
        >
          <JobCard job={job} />
        </div>
      ))}
    </div>
  );
}

import {
  BanknoteIcon,
  BookmarkIcon,
  CalendarIcon,
  Building2Icon,
  CheckCircle2Icon,
  MapPinIcon,
} from "lucide-react";

import type { Job } from "@/types/job";
import {
  countryLabel,
  employmentTypeLabel,
  formatLocation,
  formatPostingDate,
  formatRelativeDate,
  getAvatarGradient,
  getInitials,
} from "@/utils/format";
import { cn } from "@/lib/utils";

interface JobCardProps {
  job: Job;
}

function MetaChip({
  icon: Icon,
  children,
}: {
  icon: typeof MapPinIcon;
  children: React.ReactNode;
}) {
  return (
    <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
      <Icon className="size-4 shrink-0" />
      {children}
    </span>
  );
}

export function JobCard({ job }: JobCardProps) {
  const relative = formatRelativeDate(job.posting_date);

  return (
    <article className="group relative flex gap-4 rounded-2xl border border-border/70 bg-card p-5 shadow-sm transition-all hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-md">
      <div
        className={cn(
          "flex size-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br text-base font-bold text-white shadow-sm",
          getAvatarGradient(job.company),
        )}
      >
        {getInitials(job.company)}
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h3 className="truncate text-base font-bold tracking-tight transition-colors group-hover:text-primary">
              {job.title}
            </h3>
            <div className="mt-0.5 flex items-center gap-1.5 text-sm font-medium text-muted-foreground">
              <Building2Icon className="size-3.5 shrink-0" />
              <span className="truncate">{job.company}</span>
            </div>
          </div>

          <button
            type="button"
            className="text-muted-foreground/60 transition-colors hover:text-primary"
            title="Save job"
          >
            <BookmarkIcon className="size-5" />
          </button>
        </div>

        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5">
          <MetaChip icon={MapPinIcon}>{formatLocation(job)}</MetaChip>
          <MetaChip icon={CalendarIcon}>
            {relative ?? formatPostingDate(job.posting_date)}
          </MetaChip>
        </div>

        <p className="mt-3 line-clamp-2 text-sm leading-relaxed text-muted-foreground">
          {job.description}
        </p>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-50 px-2.5 py-1 text-sm font-semibold text-emerald-700 ring-1 ring-inset ring-emerald-600/15">
            <BanknoteIcon className="size-4" />
            {job.salary.display}
          </span>
          <span className="inline-flex items-center rounded-lg bg-secondary px-2.5 py-1 text-xs font-semibold text-secondary-foreground">
            {employmentTypeLabel(job.employment_type)}
          </span>
          {job.location.is_remote && (
            <span className="inline-flex items-center rounded-lg bg-sky-50 px-2.5 py-1 text-xs font-semibold text-sky-700 ring-1 ring-inset ring-sky-600/15">
              Remote
            </span>
          )}
          {job.location.country && (
            <span className="inline-flex items-center rounded-lg bg-accent px-2.5 py-1 text-xs font-semibold text-accent-foreground">
              {countryLabel(job.location.country)}
            </span>
          )}
          <span className="ml-auto inline-flex items-center gap-1 text-xs font-medium text-emerald-600">
            <CheckCircle2Icon className="size-3.5" />
            Vetted
          </span>
        </div>
      </div>
    </article>
  );
}

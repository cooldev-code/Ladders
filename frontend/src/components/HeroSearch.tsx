import { SearchIcon, SparklesIcon } from "lucide-react";

interface HeroSearchProps {
  query: string;
  onQueryChange: (value: string) => void;
  totalJobs: number;
  remoteJobs: number;
  countries: number;
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="text-center sm:text-left">
      <div className="text-lg font-extrabold tracking-tight text-white">
        {value}
      </div>
      <div className="text-[11px] font-medium text-white/70">{label}</div>
    </div>
  );
}

export function HeroSearch({
  query,
  onQueryChange,
  totalJobs,
  remoteJobs,
  countries,
}: HeroSearchProps) {
  return (
    <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-700 px-5 py-6 shadow-lg md:px-8 md:py-7">
      <div className="pointer-events-none absolute -right-12 -top-12 size-40 rounded-full bg-white/10 blur-2xl" />
      <div className="pointer-events-none absolute -bottom-16 -left-8 size-48 rounded-full bg-fuchsia-400/20 blur-3xl" />

      <div className="relative mx-auto max-w-2xl text-center">
        <span className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-0.5 text-[11px] font-semibold text-white ring-1 ring-inset ring-white/20 backdrop-blur">
          <SparklesIcon className="size-3" />
          Every role hand-vetted for quality
        </span>

        <h1 className="mt-3 text-2xl font-extrabold tracking-tight text-white md:text-3xl">
          Find a job worth the climb
        </h1>
        <p className="mx-auto mt-2 max-w-lg text-xs text-white/80 md:text-sm">
          Browse approved full-time roles across the United States and Canada,
          carefully screened for compensation and quality.
        </p>

        <div className="mx-auto mt-4 flex max-w-lg items-center gap-2 rounded-xl bg-white p-1 shadow-md">
          <div className="flex flex-1 items-center gap-2 pl-3">
            <SearchIcon className="size-4 shrink-0 text-muted-foreground" />
            <input
              type="search"
              placeholder="Search by job title, e.g. engineer"
              value={query}
              onChange={(event) => onQueryChange(event.target.value)}
              className="h-9 w-full bg-transparent text-sm text-foreground outline-none placeholder:text-muted-foreground"
            />
          </div>
          <button
            type="button"
            className="hidden h-9 items-center rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 sm:inline-flex"
          >
            Search
          </button>
        </div>

        <div className="mt-5 flex items-center justify-center gap-6 sm:gap-8">
          <Stat value={`${totalJobs}`} label="Open roles" />
          <div className="h-6 w-px bg-white/20" />
          <Stat value={`${remoteJobs}`} label="Remote friendly" />
          <div className="h-6 w-px bg-white/20" />
          <Stat value={`${countries}`} label="Countries" />
        </div>
      </div>
    </section>
  );
}

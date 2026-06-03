export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/80 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 md:px-6">
        <a href="#" className="flex items-center gap-2.5">
          <img
            src="/ladders-logo.png"
            alt="Ladders"
            className="size-9 object-contain"
          />
          <div className="leading-tight">
            <span className="block text-base font-extrabold tracking-tight">
              Ladders
            </span>
            <span className="text-muted-foreground block text-[11px] font-medium">
              Curated roles, vetted for you
            </span>
          </div>
        </a>

        <div className="flex items-center gap-3">
          <a
            href="#"
            className="hidden text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:block"
          >
            Sign in
          </a>
          <a
            href="#"
            className="inline-flex h-9 items-center justify-center rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground shadow-sm transition-colors hover:bg-primary/90"
          >
            Post a job
          </a>
        </div>
      </div>
    </header>
  );
}

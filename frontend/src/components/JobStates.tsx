import { AlertCircleIcon, SearchXIcon } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

export function EmptyState({ onClear }: { onClear?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-border bg-card/50 px-6 py-16 text-center">
      <div className="flex size-14 items-center justify-center rounded-full bg-accent text-accent-foreground">
        <SearchXIcon className="size-7" />
      </div>
      <h3 className="mt-4 text-lg font-semibold">No roles match your search</h3>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">
        Try adjusting your search terms or clearing filters to see more
        opportunities.
      </p>
      {onClear && (
        <Button variant="outline" className="mt-5" onClick={onClear}>
          Clear all filters
        </Button>
      )}
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <Alert variant="destructive">
      <AlertCircleIcon />
      <AlertTitle>Unable to load jobs</AlertTitle>
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  );
}

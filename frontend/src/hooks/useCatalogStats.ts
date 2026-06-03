import { useEffect, useState } from "react";

import { fetchCatalogStats } from "@/api/jobs";
import type { CatalogStats } from "@/types/job";

export function useCatalogStats(): CatalogStats | null {
  const [stats, setStats] = useState<CatalogStats | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchCatalogStats()
      .then((result) => {
        if (!cancelled) setStats(result);
      })
      .catch(() => {
        if (!cancelled) setStats(null);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return stats;
}

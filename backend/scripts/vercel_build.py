"""Copy repo feed data into the backend bundle for Vercel serverless."""

from __future__ import annotations

import shutil
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
SRC = REPO_ROOT / "data" / "feeds"
DST = BACKEND_ROOT / "data" / "feeds"


def main() -> None:
    if not SRC.is_dir():
        print(f"vercel_build: no feeds at {SRC}, skipping copy")
        return
    DST.parent.mkdir(parents=True, exist_ok=True)
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    print(f"vercel_build: copied feeds from {SRC} to {DST}")


if __name__ == "__main__":
    main()

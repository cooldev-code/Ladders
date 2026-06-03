from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    """A single page of results plus the metadata needed to navigate them."""

    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size <= 0 or self.total == 0:
            return 1
        return math.ceil(self.total / self.page_size)

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


def paginate(items: list[T], *, page: int, page_size: int) -> Page[T]:
    start = (page - 1) * page_size
    end = start + page_size
    return Page(
        items=items[start:end],
        total=len(items),
        page=page,
        page_size=page_size,
    )

"""Registry of expressible-yet-unknown mathematical truths.

The engines encode known truths for each base.  Base-10 is treated as a
well-understood system whose facts are mostly known.  Base-12 and base-60
start with known truths plus references to this registry; as experiments
reveal new relationships, entries here are amended in place (never renamed
or version-copied).

Each unknown has:
  - id: stable identifier (e.g. "base60.fraction.1_7.period")
  - base: which base the unknown concerns (10, 12, or 60)
  - category: domain (fractions, geometry, frequency, etc.)
  - statement: human-readable description of the unknown relationship
  - status: "open" | "conjecture" | "proven" | "refuted"
  - evidence: list of experiment ids that bear on this unknown
  - version: semantic version "MAJOR.MINOR.PATCH" of the current understanding
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UnknownEntry:
    """A single entry in the unknowns registry."""

    id: str
    base: int
    category: str
    statement: str
    status: str = "open"
    evidence: list[str] = field(default_factory=list)
    version: str = "0.1.0"
    notes: str = ""

    def __post_init__(self) -> None:
        if self.base not in (10, 12, 60):
            raise ValueError(f"unsupported base {self.base}")
        if self.status not in ("open", "conjecture", "proven", "refuted"):
            raise ValueError(f"invalid status {self.status!r}")


class UnknownsRegistry:
    """Mutable registry of unknown mathematical truths.

    Entries are amended in place.  The registry is the mechanism by which
    experiments "update the engines as new truths are revealed."
    """

    def __init__(self) -> None:
        self._entries: dict[str, UnknownEntry] = {}

    def add(self, entry: UnknownEntry) -> None:
        """Register a new unknown (or overwrite an existing id in place)."""
        self._entries[entry.id] = entry

    def get(self, entry_id: str) -> UnknownEntry | None:
        return self._entries.get(entry_id)

    def update_status(self, entry_id: str, status: str, evidence_id: str | None = None, version: str | None = None) -> None:
        """Amend an entry's status in place (the update mechanism experiments use)."""
        entry = self._entries.get(entry_id)
        if entry is None:
            raise KeyError(f"unknown id {entry_id!r} not in registry")
        entry.status = status
        if evidence_id and evidence_id not in entry.evidence:
            entry.evidence.append(evidence_id)
        if version is not None:
            entry.version = version

    def list_by_base(self, base: int) -> list[UnknownEntry]:
        return [e for e in self._entries.values() if e.base == base]

    def list_by_status(self, status: str) -> list[UnknownEntry]:
        return [e for e in self._entries.values() if e.status == status]

    def list_by_category(self, category: str) -> list[UnknownEntry]:
        return [e for e in self._entries.values() if e.category == category]

    def all_entries(self) -> list[UnknownEntry]:
        return list(self._entries.values())

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries.values())


__all__ = ["UnknownEntry", "UnknownsRegistry"]

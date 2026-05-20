from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
    queued = "queued"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class TaskKind(str, Enum):
    design = "design"
    implement = "implement"
    validate = "validate"


@dataclass
class Task:
    id: str
    goal: str
    acceptance_criteria: List[str] = field(default_factory=list)
    context: str = ""
    owner: str = ""
    kind: TaskKind = TaskKind.design
    status: TaskStatus = TaskStatus.queued
    result: Optional[str] = None
    retries: int = 0
    max_retries: int = 2
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["kind"] = self.kind.value
        d["status"] = self.status.value
        return d


@dataclass
class FeedbackItem:
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {"content": self.content, "created_at": self.created_at.isoformat()}


@dataclass
class IntentSpec:
    goal: str
    acceptance_criteria: List[str]
    context: str

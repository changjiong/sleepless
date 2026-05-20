from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class TaskStatus(str, Enum):
    queued = "queued"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


@dataclass
class Task:
    id: str
    goal: str
    acceptance_criteria: List[str] = field(default_factory=list)
    context: str = ""
    owner: str = ""
    status: TaskStatus = TaskStatus.queued
    result: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class FeedbackItem:
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class IntentSpec:
    goal: str
    acceptance_criteria: List[str]
    context: str

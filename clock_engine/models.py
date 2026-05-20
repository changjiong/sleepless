from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    queued = "queued"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class Task(BaseModel):
    id: str
    goal: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    context: str = ""
    owner: str
    status: TaskStatus = TaskStatus.queued
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackItem(BaseModel):
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class IntentSpec(BaseModel):
    goal: str
    acceptance_criteria: List[str]
    context: str

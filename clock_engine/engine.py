from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .agents import ElonCEO
from .logging_config import get_logger
from .scheduler import ClockScheduler
from .storage import JsonStorage

logger = get_logger("engine")


@dataclass
class ClockEngine:
    ceo: ElonCEO = field(default_factory=ElonCEO)
    scheduler: ClockScheduler = field(default_factory=ClockScheduler)
    storage: JsonStorage = field(default_factory=JsonStorage)

    def submit_intent(self, text: str) -> Dict[str, List[str]]:
        spec = self.ceo.parse_intent(text)
        tasks = self.ceo.decompose(spec)
        self.scheduler.push_tasks(tasks)

        executed: List[str] = []
        while self.scheduler.queue:
            report = self.scheduler.tick()
            if report.get("task"):
                executed.append(report["task"])

        self._persist()
        return {"goal": [spec.goal], "executed": executed}

    def add_feedback(self, text: str) -> None:
        self.scheduler.add_feedback(text)
        self._persist()

    def status_snapshot(self) -> List[dict]:
        return [t.to_dict() for t in self.scheduler.done]

    def _persist(self) -> None:
        self.storage.save(
            done=[t.to_dict() for t in self.scheduler.done],
            feedback=[f.to_dict() for f in self.scheduler.feedback_pool],
        )

    def load_state(self) -> Dict[str, object]:
        return self.storage.load()

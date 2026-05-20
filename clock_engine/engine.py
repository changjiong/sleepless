from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .agents import ElonCEO
from .scheduler import ClockScheduler


@dataclass
class ClockEngine:
    ceo: ElonCEO = field(default_factory=ElonCEO)
    scheduler: ClockScheduler = field(default_factory=ClockScheduler)

    def submit_intent(self, text: str) -> Dict[str, List[str]]:
        spec = self.ceo.parse_intent(text)
        tasks = self.ceo.decompose(spec)
        self.scheduler.push_tasks(tasks)

        executed: List[str] = []
        while self.scheduler.queue:
            report = self.scheduler.tick()
            if report.get("task"):
                executed.append(report["task"])

        return {
            "goal": [spec.goal],
            "executed": executed,
        }

    def status_snapshot(self) -> List[dict]:
        return [
            {
                "id": t.id,
                "owner": t.owner,
                "goal": t.goal,
                "status": t.status.value,
                "result": t.result,
            }
            for t in self.scheduler.done
        ]

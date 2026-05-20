from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .agents import ElonCEO
from .logging_config import get_logger
from .scheduler import ClockScheduler

logger = get_logger("engine")


@dataclass
class ClockEngine:
    ceo: ElonCEO = field(default_factory=ElonCEO)
    scheduler: ClockScheduler = field(default_factory=ClockScheduler)

    def submit_intent(self, text: str) -> Dict[str, List[str]]:
        logger.trace("submit_intent.start text={!r}", text)
        spec = self.ceo.parse_intent(text)
        tasks = self.ceo.decompose(spec)
        self.scheduler.push_tasks(tasks)

        executed: List[str] = []
        while self.scheduler.queue:
            report = self.scheduler.tick()
            if report.get("task"):
                executed.append(report["task"])
                logger.debug("submit_intent.task_report task_report={!r}", report["task"])

        result = {
            "goal": [spec.goal],
            "executed": executed,
        }
        logger.info("submit_intent.done goal={!r} executed_count={}", spec.goal, len(executed))
        return result

    def status_snapshot(self) -> List[dict]:
        snapshot = [
            {
                "id": t.id,
                "owner": t.owner,
                "goal": t.goal,
                "status": t.status.value,
                "result": t.result,
            }
            for t in self.scheduler.done
        ]
        logger.trace("status_snapshot count={}", len(snapshot))
        return snapshot

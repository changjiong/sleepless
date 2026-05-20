from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List

from .agents import BossCS, JobsDesigner, LinusEngineer, TuringValidator
from .models import FeedbackItem, Task


@dataclass
class ClockScheduler:
    jobs: JobsDesigner = field(default_factory=JobsDesigner)
    linus: LinusEngineer = field(default_factory=LinusEngineer)
    turing: TuringValidator = field(default_factory=TuringValidator)
    boss: BossCS = field(default_factory=BossCS)

    queue: List[Task] = field(default_factory=list)
    done: List[Task] = field(default_factory=list)
    feedback_pool: List[FeedbackItem] = field(default_factory=list)
    next_feedback_scan_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=4))

    def push_tasks(self, tasks: List[Task]) -> None:
        self.queue.extend(tasks)

    def add_feedback(self, text: str) -> None:
        self.feedback_pool.append(FeedbackItem(content=text))

    def tick(self) -> Dict[str, str]:
        report: Dict[str, str] = {}
        if self.queue:
            task = self.queue.pop(0)
            runner = {
                "jobs": self.jobs.run,
                "linus": self.linus.run,
                "turing": self.turing.run,
            }[task.owner]
            finished = runner(task)
            self.done.append(finished)
            report["task"] = f"{finished.owner} 完成任务 {finished.id}"

        now = datetime.utcnow()
        if now >= self.next_feedback_scan_at:
            report["feedback"] = self.boss.summarize(self.feedback_pool)
            self.feedback_pool.clear()
            self.next_feedback_scan_at = now + timedelta(hours=4)

        return report

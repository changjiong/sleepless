from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from .agents import BossCS, JobsDesigner, LinusEngineer, TuringValidator
from .logging_config import get_logger
from .models import FeedbackItem, Task, TaskKind

logger = get_logger("scheduler")


@dataclass
class ClockScheduler:
    jobs: JobsDesigner = field(default_factory=JobsDesigner)
    linus: LinusEngineer = field(default_factory=LinusEngineer)
    turing: TuringValidator = field(default_factory=TuringValidator)
    boss: BossCS = field(default_factory=BossCS)

    queue: List[Task] = field(default_factory=list)
    done: List[Task] = field(default_factory=list)
    feedback_pool: List[FeedbackItem] = field(default_factory=list)
    next_feedback_scan_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=4))

    def push_tasks(self, tasks: List[Task]) -> None:
        self.queue.extend(tasks)

    def add_feedback(self, text: str) -> None:
        self.feedback_pool.append(FeedbackItem(content=text))

    def tick(self) -> Dict[str, str]:
        report: Dict[str, str] = {}
        if self.queue:
            task = self.queue.pop(0)
            runner = {"jobs": self.jobs.run, "linus": self.linus.run, "turing": self.turing.run}[task.owner]
            finished = runner(task)

            if finished.kind == TaskKind.validate and finished.status.value == "blocked":
                if finished.retries < finished.max_retries:
                    finished.retries += 1
                    rework = Task(
                        id=finished.id,
                        goal=finished.goal.replace("质量验证：", "工程实现：返工修复："),
                        acceptance_criteria=finished.acceptance_criteria,
                        context=finished.context,
                        owner="linus",
                        kind=TaskKind.implement,
                        retries=finished.retries,
                        max_retries=finished.max_retries,
                    )
                    revalidate = Task(
                        id=finished.id,
                        goal=finished.goal,
                        acceptance_criteria=finished.acceptance_criteria,
                        context=finished.context,
                        owner="turing",
                        kind=TaskKind.validate,
                        retries=finished.retries,
                        max_retries=finished.max_retries,
                    )
                    self.queue.insert(0, revalidate)
                    self.queue.insert(0, rework)
                    report["task"] = f"{finished.owner} 验证失败，已回流 linus 返工 (retry={finished.retries})"
                    logger.warning(report["task"])
                else:
                    self.done.append(finished)
                    report["task"] = f"{finished.owner} 验证失败且达到重试上限"
            else:
                self.done.append(finished)
                report["task"] = f"{finished.owner} 完成任务 {finished.id}"

        now = datetime.now(timezone.utc)
        if now >= self.next_feedback_scan_at:
            report["feedback"] = self.boss.summarize(self.feedback_pool)
            self.feedback_pool.clear()
            self.next_feedback_scan_at = now + timedelta(hours=4)

        return report

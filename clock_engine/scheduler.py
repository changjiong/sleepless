from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from .agents import BossCS, JobsDesigner, LinusEngineer, TuringValidator
from .logging_config import get_logger
from .models import FeedbackItem, Task

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
        logger.trace("push_tasks.start incoming={} queue_before={}", len(tasks), len(self.queue))
        self.queue.extend(tasks)
        logger.info("push_tasks.done queue_after={} task_ids={}", len(self.queue), [t.id for t in tasks])

    def add_feedback(self, text: str) -> None:
        logger.trace("add_feedback.start text={!r} pool_before={}", text, len(self.feedback_pool))
        self.feedback_pool.append(FeedbackItem(content=text))
        logger.debug("add_feedback.done pool_after={}", len(self.feedback_pool))

    def tick(self) -> Dict[str, str]:
        logger.trace(
            "tick.start queue={} done={} feedback_pool={} next_feedback_scan_at={}",
            len(self.queue), len(self.done), len(self.feedback_pool), self.next_feedback_scan_at.isoformat(),
        )
        report: Dict[str, str] = {}
        if self.queue:
            task = self.queue.pop(0)
            logger.debug("tick.dispatch task_id={} owner={} goal={!r}", task.id, task.owner, task.goal)
            runner = {
                "jobs": self.jobs.run,
                "linus": self.linus.run,
                "turing": self.turing.run,
            }[task.owner]
            finished = runner(task)
            self.done.append(finished)
            report["task"] = f"{finished.owner} 完成任务 {finished.id}"
            logger.info("tick.task_done task_id={} owner={} status={} done_total={}", finished.id, finished.owner, finished.status.value, len(self.done))

        now = datetime.now(timezone.utc)
        if now >= self.next_feedback_scan_at:
            logger.debug("tick.feedback_scan_triggered now={} next_scan={}", now.isoformat(), self.next_feedback_scan_at.isoformat())
            report["feedback"] = self.boss.summarize(self.feedback_pool)
            self.feedback_pool.clear()
            self.next_feedback_scan_at = now + timedelta(hours=4)
            logger.info("tick.feedback_scan_done next_feedback_scan_at={}", self.next_feedback_scan_at.isoformat())

        logger.trace("tick.end report_keys={}", list(report.keys()))
        return report

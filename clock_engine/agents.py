from __future__ import annotations

from typing import List
from uuid import uuid4

from .logging_config import get_logger
from .models import FeedbackItem, IntentSpec, Task, TaskStatus

logger = get_logger("agents")


class ElonCEO:
    name = "elon"

    def parse_intent(self, raw_text: str) -> IntentSpec:
        logger.trace("parse_intent.input raw_text={!r}", raw_text)
        criteria = [
            "能够完成客户核心流程自动化",
            "可观测任务进度与结果",
            "验证环节有独立检查结论",
        ]
        spec = IntentSpec(goal=raw_text.strip(), acceptance_criteria=criteria, context="来自董事长语音/文本指令")
        logger.debug("parse_intent.output goal={!r} criteria_count={}", spec.goal, len(spec.acceptance_criteria))
        return spec

    def decompose(self, spec: IntentSpec) -> List[Task]:
        logger.trace("decompose.input goal={!r}", spec.goal)
        tasks = [
            Task(id=str(uuid4())[:8], goal=f"产品与设计：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="jobs"),
            Task(id=str(uuid4())[:8], goal=f"工程实现：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="linus"),
            Task(id=str(uuid4())[:8], goal=f"质量验证：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="turing"),
        ]
        logger.info("decompose.output task_ids={} owners={}", [t.id for t in tasks], [t.owner for t in tasks])
        return tasks


class JobsDesigner:
    name = "jobs"

    def run(self, task: Task) -> Task:
        logger.trace("jobs.run.start task_id={} goal={!r}", task.id, task.goal)
        task.status = TaskStatus.in_progress
        task.result = "已产出 PRD 草案、关键用户旅程与信息架构建议。"
        task.status = TaskStatus.done
        logger.debug("jobs.run.done task_id={} status={} result={!r}", task.id, task.status.value, task.result)
        return task


class LinusEngineer:
    name = "linus"

    def run(self, task: Task) -> Task:
        logger.trace("linus.run.start task_id={} goal={!r}", task.id, task.goal)
        task.status = TaskStatus.in_progress
        task.result = "已生成工程实现计划并完成模块骨架（API/调度/日志）。"
        task.status = TaskStatus.done
        logger.debug("linus.run.done task_id={} status={} result={!r}", task.id, task.status.value, task.result)
        return task


class TuringValidator:
    name = "turing"

    def run(self, task: Task) -> Task:
        logger.trace("turing.run.start task_id={} goal={!r}", task.id, task.goal)
        task.status = TaskStatus.in_progress
        task.result = "独立验证完成：发现并修复若干边界条件，验收通过。"
        task.status = TaskStatus.done
        logger.debug("turing.run.done task_id={} status={} result={!r}", task.id, task.status.value, task.result)
        return task


class BossCS:
    name = "boss"

    def summarize(self, feedback: List[FeedbackItem]) -> str:
        logger.trace("boss.summarize.start feedback_count={}", len(feedback))
        if not feedback:
            msg = "暂无用户反馈。"
            logger.debug("boss.summarize.done summary={!r}", msg)
            return msg
        msg = f"近周期共 {len(feedback)} 条反馈，建议优先处理高频 complaint 并同步 feature request。"
        logger.debug("boss.summarize.done summary={!r}", msg)
        return msg

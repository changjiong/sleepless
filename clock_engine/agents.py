from __future__ import annotations

from typing import List
from uuid import uuid4

from .logging_config import get_logger
from .models import FeedbackItem, IntentSpec, Task, TaskKind, TaskStatus
from .tools import CodeTool, DesignTool, ValidationTool

logger = get_logger("agents")


class ElonCEO:
    name = "elon"

    def parse_intent(self, raw_text: str) -> IntentSpec:
        logger.trace("parse_intent.input raw_text={!r}", raw_text)
        criteria = ["核心流程可自动化", "有可观察执行状态", "验证可独立进行"]
        return IntentSpec(goal=raw_text.strip(), acceptance_criteria=criteria, context="chairman chat")

    def decompose(self, spec: IntentSpec) -> List[Task]:
        logger.trace("decompose.input goal={!r}", spec.goal)
        return [
            Task(id=str(uuid4())[:8], goal=f"产品与设计：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="jobs", kind=TaskKind.design),
            Task(id=str(uuid4())[:8], goal=f"工程实现：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="linus", kind=TaskKind.implement),
            Task(id=str(uuid4())[:8], goal=f"质量验证：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="turing", kind=TaskKind.validate),
        ]


class JobsDesigner:
    def __init__(self) -> None:
        self.tool = DesignTool()

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        out = self.tool.run(task.goal)
        task.result = out.output
        task.status = TaskStatus.done if out.ok else TaskStatus.blocked
        return task


class LinusEngineer:
    def __init__(self) -> None:
        self.tool = CodeTool()

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        out = self.tool.run(task.goal, attempt=task.retries)
        task.result = out.output
        task.status = TaskStatus.done if out.ok else TaskStatus.blocked
        return task


class TuringValidator:
    def __init__(self) -> None:
        self.tool = ValidationTool()

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        out = self.tool.run(task.goal, attempt=task.retries)
        task.result = out.output
        task.status = TaskStatus.done if out.ok else TaskStatus.blocked
        return task


class BossCS:
    def summarize(self, feedback: List[FeedbackItem]) -> str:
        if not feedback:
            return "暂无用户反馈。"
        return f"近周期共 {len(feedback)} 条反馈，建议先处理 complaint 再处理 feature request。"

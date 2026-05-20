from __future__ import annotations

from typing import List
from uuid import uuid4

from .models import FeedbackItem, IntentSpec, Task, TaskStatus


class ElonCEO:
    name = "elon"

    def parse_intent(self, raw_text: str) -> IntentSpec:
        criteria = [
            "能够完成客户核心流程自动化",
            "可观测任务进度与结果",
            "验证环节有独立检查结论",
        ]
        return IntentSpec(goal=raw_text.strip(), acceptance_criteria=criteria, context="来自董事长语音/文本指令")

    def decompose(self, spec: IntentSpec) -> List[Task]:
        return [
            Task(id=str(uuid4())[:8], goal=f"产品与设计：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="jobs"),
            Task(id=str(uuid4())[:8], goal=f"工程实现：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="linus"),
            Task(id=str(uuid4())[:8], goal=f"质量验证：{spec.goal}", acceptance_criteria=spec.acceptance_criteria, context=spec.context, owner="turing"),
        ]


class JobsDesigner:
    name = "jobs"

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        task.result = "已产出 PRD 草案、关键用户旅程与信息架构建议。"
        task.status = TaskStatus.done
        return task


class LinusEngineer:
    name = "linus"

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        task.result = "已生成工程实现计划并完成模块骨架（API/调度/日志）。"
        task.status = TaskStatus.done
        return task


class TuringValidator:
    name = "turing"

    def run(self, task: Task) -> Task:
        task.status = TaskStatus.in_progress
        task.result = "独立验证完成：发现并修复若干边界条件，验收通过。"
        task.status = TaskStatus.done
        return task


class BossCS:
    name = "boss"

    def summarize(self, feedback: List[FeedbackItem]) -> str:
        if not feedback:
            return "暂无用户反馈。"
        return f"近周期共 {len(feedback)} 条反馈，建议优先处理高频 complaint 并同步 feature request。"

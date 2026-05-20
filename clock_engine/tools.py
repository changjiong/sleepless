from __future__ import annotations

from dataclasses import dataclass

from .logging_config import get_logger

logger = get_logger("tools")


@dataclass
class ToolResult:
    ok: bool
    output: str


class DesignTool:
    def run(self, goal: str) -> ToolResult:
        logger.trace("design_tool.run goal={!r}", goal)
        return ToolResult(True, f"PRD/IA 已生成: {goal}")


class CodeTool:
    def run(self, goal: str, attempt: int) -> ToolResult:
        logger.trace("code_tool.run goal={!r} attempt={}", goal, attempt)
        return ToolResult(True, f"代码实现完成(第{attempt}轮): {goal}")


class ValidationTool:
    def run(self, goal: str, attempt: int) -> ToolResult:
        logger.trace("validation_tool.run goal={!r} attempt={}", goal, attempt)
        if attempt == 0:
            return ToolResult(False, "验证失败: 缺少边界条件处理，已回流 Linus")
        return ToolResult(True, "验证通过: 边界条件已覆盖")

from __future__ import annotations

from clock_engine import ClockEngine
from clock_engine.logging_config import get_logger

logger = get_logger("app")


def show_status(engine: ClockEngine) -> None:
    logger.trace("show_status.start")
    print("\n=== Clock Engine Status ===")
    print("Task ID | Owner | Goal | Result")
    for task in engine.status_snapshot()[-10:]:
        print(f"{task['id']} | {task['owner']} | {task['goal']} | {task['result'] or ''}")
    print()
    logger.trace("show_status.end")


def main() -> None:
    engine = ClockEngine()
    logger.info("app.start")

    print("Clockpla AI Demo 已启动")
    print("输入意图 / status / feedback <内容> / exit")

    while True:
        user_input = input("> ").strip()
        logger.trace("app.input {!r}", user_input)
        if not user_input:
            continue
        if user_input == "exit":
            logger.info("app.exit")
            break
        if user_input == "status":
            show_status(engine)
            continue
        if user_input.startswith("feedback "):
            feedback_text = user_input.removeprefix("feedback ")
            engine.scheduler.add_feedback(feedback_text)
            logger.debug("app.feedback_recorded {!r}", feedback_text)
            print("反馈已记录")
            continue

        result = engine.submit_intent(user_input)
        logger.debug("app.intent_executed executed_count={}", len(result["executed"]))
        for line in result["executed"]:
            print(line)

    print("已退出。")


if __name__ == "__main__":
    main()

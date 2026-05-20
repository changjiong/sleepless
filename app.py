from __future__ import annotations

from clock_engine import ClockEngine
from clock_engine.logging_config import get_logger

logger = get_logger("app")


def show_status(engine: ClockEngine) -> None:
    print("\n=== Clock Engine Status ===")
    print("Task ID | Owner | Goal | Retries | Result")
    for task in engine.status_snapshot()[-10:]:
        print(f"{task['id']} | {task['owner']} | {task['goal']} | {task['retries']} | {task['result'] or ''}")
    print()


def main() -> None:
    engine = ClockEngine()
    logger.info("app.start")
    print("Clockpla AI Demo 已启动")
    print("输入意图 / status / feedback <内容> / state / exit")

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input == "exit":
            break
        if user_input == "status":
            show_status(engine)
            continue
        if user_input == "state":
            print(engine.load_state())
            continue
        if user_input.startswith("feedback "):
            engine.add_feedback(user_input.removeprefix("feedback "))
            print("反馈已记录")
            continue

        result = engine.submit_intent(user_input)
        for line in result["executed"]:
            print(line)

    print("已退出。")


if __name__ == "__main__":
    main()

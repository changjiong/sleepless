from pathlib import Path

from clock_engine import ClockEngine


def test_submit_intent_executes_with_rework_loop() -> None:
    engine = ClockEngine()
    result = engine.submit_intent("给房产中介做自动跟进")

    assert result["goal"] == ["给房产中介做自动跟进"]
    assert any("验证失败，已回流" in x for x in result["executed"])
    assert result["executed"][-1].startswith("turing 完成任务")


def test_state_persisted() -> None:
    state_file = Path(".clockpla_state.json")
    if state_file.exists():
        state_file.unlink()

    engine = ClockEngine()
    engine.submit_intent("测试持久化")
    assert state_file.exists()

    data = engine.load_state()
    assert "done" in data
    assert len(data["done"]) >= 3

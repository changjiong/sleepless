from pathlib import Path

from clock_engine import ClockEngine


def test_submit_intent_executes_all_workers() -> None:
    engine = ClockEngine()
    result = engine.submit_intent("给房产中介做自动跟进")
    assert result["goal"] == ["给房产中介做自动跟进"]
    assert len(result["executed"]) == 3

    owners = [item["owner"] for item in engine.status_snapshot()]
    assert owners == ["jobs", "linus", "turing"]


def test_trace_log_file_is_created() -> None:
    engine = ClockEngine()
    engine.submit_intent("测试日志是否完整记录")

    trace_log = Path("logs/clockpla.trace.log")
    assert trace_log.exists()
    content = trace_log.read_text(encoding="utf-8")
    assert "submit_intent.start" in content
    assert "tick.dispatch" in content
    assert "turing.run.done" in content

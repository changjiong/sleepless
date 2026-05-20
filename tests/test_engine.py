from clock_engine import ClockEngine


def test_submit_intent_executes_all_workers() -> None:
    engine = ClockEngine()
    result = engine.submit_intent("给房产中介做自动跟进")
    assert result["goal"] == ["给房产中介做自动跟进"]
    assert len(result["executed"]) == 3

    owners = [item["owner"] for item in engine.status_snapshot()]
    assert owners == ["jobs", "linus", "turing"]

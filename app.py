from __future__ import annotations

from rich.console import Console
from rich.table import Table

from clock_engine.agents import ElonCEO
from clock_engine.scheduler import ClockScheduler

console = Console()


def show_status(scheduler: ClockScheduler) -> None:
    table = Table(title="Clock Engine Status")
    table.add_column("Task ID")
    table.add_column("Owner")
    table.add_column("Goal")
    table.add_column("Result")
    for task in scheduler.done[-10:]:
        table.add_row(task.id, task.owner, task.goal, task.result or "")
    console.print(table)


def main() -> None:
    ceo = ElonCEO()
    scheduler = ClockScheduler()

    console.print("[bold green]Clockpla AI Demo 已启动[/bold green]")
    console.print("输入意图 / status / feedback <内容> / exit")

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input == "exit":
            break
        if user_input == "status":
            show_status(scheduler)
            continue
        if user_input.startswith("feedback "):
            scheduler.add_feedback(user_input.removeprefix("feedback "))
            console.print("[cyan]反馈已记录[/cyan]")
            continue

        spec = ceo.parse_intent(user_input)
        tasks = ceo.decompose(spec)
        scheduler.push_tasks(tasks)

        while scheduler.queue:
            report = scheduler.tick()
            if report.get("task"):
                console.print(f"[yellow]{report['task']}[/yellow]")

    console.print("[bold]已退出。[/bold]")


if __name__ == "__main__":
    main()

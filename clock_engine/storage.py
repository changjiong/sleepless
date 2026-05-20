from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class JsonStorage:
    def __init__(self, path: str = ".clockpla_state.json") -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {"tasks": [], "feedback": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, tasks: List[Dict[str, Any]], feedback: List[Dict[str, Any]]) -> None:
        payload = {"tasks": tasks, "feedback": feedback}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

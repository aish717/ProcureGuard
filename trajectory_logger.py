from pathlib import Path
import json
from datetime import datetime

class TrajectoryLogger:
    def __init__(self, base_dir="trajectories", case_id="live"):
        self.case_dir = Path(base_dir) / case_id
        self.case_dir.mkdir(parents=True, exist_ok=True)
        self.events = []

    def log(self, agent, instruction, input_data=None, action=None,
            tool=None, tool_input=None, tool_output=None, output=None,
            retry=False, human_checkpoint=False):
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent,
            "instruction": instruction,
            "input": input_data,
            "action": action,
            "tool": tool,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "output": output,
            "retry": retry,
            "human_checkpoint": human_checkpoint,
        }
        self.events.append(event)
        self._save()

    def _save(self):
        path = self.case_dir / "trajectory.json"
        path.write_text(json.dumps(self.events, indent=2, ensure_ascii=False), encoding="utf-8")

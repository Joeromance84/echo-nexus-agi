# echopack/echo/memory.py
# Stores logs, build history, and project-specific memories.

import json
import os

class EchoMemory:
    """
    A simple log and memory saver for the EchoPack system.
    """
    def __init__(self, log_file="build_log.json"):
        self.log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'output', log_file)
        self.logs = []

    def log_event(self, event: dict):
        """Records a new event in the build log."""
        self.logs.append(event)
        self.save_logs()

    def save_logs(self):
        """Saves the current log to a file."""
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=2)
        print(f"Build log saved to {self.log_file}")
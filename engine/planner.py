# echo-nexus-training-system/engine/planner.py
import json

class Planner:
    """
    Prioritizes training tasks like a student.
    It reads the curriculum and organizes the learning schedule.
    """
    def __init__(self, curriculum_path: str):
        self.curriculum_path = curriculum_path
        self.curriculum = self._load_curriculum()
        self.task_queue = []

    def _load_curriculum(self):
        """Loads all learning modules from the training directory."""
        curriculum = {}
        # Placeholder logic: walks through all training modules
        # for folder in os.listdir(self.curriculum_path):
        # ... and loads their learning_modules.json
        print("Loading curriculum from all modules...")
        return curriculum

    def prioritize_tasks(self):
        """
        Creates a prioritized list of tasks.
        This could use rules or LLM reasoning.
        """
        # Conceptual prioritization logic
        self.task_queue.append("Start with foundational skills: chinese_master_programming.")
        self.task_queue.append("Next, build a tool from the tools/ folder.")
        print("Training tasks have been prioritized.")

    def get_next_task(self):
        """Returns the highest-priority task from the queue."""
        if self.task_queue:
            return self.task_queue.pop(0)
        return None
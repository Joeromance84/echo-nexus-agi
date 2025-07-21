# echo-nexus-training-system/engine/coach.py

class Coach:
    """
    Acts like a teacher bot, giving assignments and scoring performance.
    """
    def __init__(self, llm_engine, test_runner):
        self.llm_engine = llm_engine
        self.test_runner = test_runner

    def give_assignment(self, task_description: str):
        """Generates a detailed assignment from a task description."""
        prompt = f"As a coach, generate a detailed assignment for the following task: {task_description}"
        assignment = self.llm_engine.generate_response(prompt)
        print("Assignment generated.")
        return assignment

    def score_performance(self, task_id: str, results: dict):
        """
        Evaluates task performance using a test runner and provides feedback.
        """
        score = self.test_runner.run_tests(task_id)
        # LLM-based feedback
        feedback_prompt = f"Based on a test score of {score}, provide constructive feedback."
        feedback = self.llm_engine.generate_response(feedback_prompt)
        print(f"Performance scored: {score}")
        return feedback
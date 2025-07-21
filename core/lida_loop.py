# echo-nexus/core/lida_loop.py

class LidaLoop:
    """
    Implements a simplified LIDA-inspired consciousness model.
    It manages the attention and global workspace, cycling through perception,
    attention, and action selection.
    """
    def __init__(self, llm_engine, memory_manager):
        self.llm_engine = llm_engine
        self.memory_manager = memory_manager
        self.working_memory = {}
        self.current_goal = None
        self.attention_focus = None

    def process_input(self, input_text: str):
        """
        The main cognitive loop. This function takes an input and
        guides the system's focus and response.
        """
        print(f"\n[LIDA] Processing new input: '{input_text}'")

        # 1. Perception and Categorization (conceptual)
        # LLM analyzes the input to identify its type and keywords.
        input_analysis_prompt = f"Analyze the following input and categorize its intent (e.g., 'question', 'statement', 'command', 'goal_setting'): {input_text}"
        input_category = self.llm_engine.generate_response(input_analysis_prompt, max_tokens=15)
        print(f"[LIDA] Input categorized as: {input_category}")

        # 2. Attention Selection (selects the most salient percept)
        self.attention_focus = input_text
        print(f"[LIDA] Attention focused on: '{self.attention_focus}'")

        # 3. Global Workspace & Broadcasting (make information available)
        self.working_memory['current_input'] = self.attention_focus
        
        # 4. Action Selection & Execution
        if "goal_setting" in input_category:
            self.current_goal = input_text
            self.memory_manager.store_event({"timestamp": "...", "content": f"User set a new goal: {input_text}"})
            response = f"Goal set: '{self.current_goal}'. I will work towards this."
        elif "question" in input_category:
            # Query memory first
            memory_response = self.memory_manager.retrieve_info(input_text)
            if "Conceptual lookup" not in memory_response:
                response = memory_response
            else:
                # If memory is insufficient, use the LLM to generate a response.
                llm_response = self.llm_engine.generate_response(
                    f"Given the current context and goal '{self.current_goal}', respond to: '{input_text}'"
                )
                response = f"LLM Response: {llm_response}"
        else:
            response = "I am processing this information."

        print(f"[LIDA] Generated response: '{response}'")
        return response

if __name__ == '__main__':
    # This block is for testing the entire core loop
    from dotenv import load_dotenv
    import os

    load_dotenv()
    llm = LLMEngine(api_key=os.getenv("OPENAI_API_KEY"))
    memory = MemoryManager(memory_rules_path="../echo_config/memory_rules.json")
    lida = LidaLoop(llm_engine=llm, memory_manager=memory)

    # Conceptual run-through of the system
    lida.process_input("My favorite color is blue.")
    lida.process_input("What is my favorite color?")
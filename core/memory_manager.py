# echo-nexus/core/memory_manager.py
import json

class MemoryManager:
    """
    A SOAR-like memory system with episodic and semantic memory components.
    This class handles the storage, retrieval, and application of rules.
    """
    def __init__(self, memory_rules_path: str):
        self.episodic_memory = []  # Stores chronological events/interactions
        self.semantic_memory = {}  # Stores facts, concepts, and relationships
        self.rules = self._load_rules(memory_rules_path)

    def _load_rules(self, path: str) -> dict:
        """Loads memory rules from a JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found. Starting with empty rules.")
            return {"retrieval_rules": [], "storage_rules": []}

    def store_event(self, event: dict):
        """
        Stores an episodic event and updates semantic memory based on rules.

        Args:
            event (dict): The event to store, e.g., {"timestamp": ..., "content": ...}
        """
        self.episodic_memory.append(event)
        # Apply storage rules to extract key facts for semantic memory
        for rule in self.rules.get("storage_rules", []):
            if rule["condition"] in event["content"]:
                fact_to_store = event["content"].split(rule["delimiter"])[-1].strip()
                self.semantic_memory[rule["key"]] = fact_to_store
                print(f"Stored new semantic fact: {rule['key']} = {fact_to_store}")

    def retrieve_info(self, query: str) -> str:
        """
        Retrieves information from memory based on a query.
        This function uses retrieval rules to decide where to look first.

        Args:
            query (str): The information to retrieve.

        Returns:
            str: The retrieved information or a default message.
        """
        for rule in self.rules.get("retrieval_rules", []):
            if rule["trigger"] in query:
                # Prioritize semantic memory lookup based on a rule
                if rule["target"] in self.semantic_memory:
                    return f"From semantic memory: {self.semantic_memory[rule['target']]}"
        
        # Fallback to a conceptual LLM-driven search through episodic memory
        return "Conceptual lookup in episodic memory via LLM..."

if __name__ == '__main__':
    # This is for testing the memory manager
    manager = MemoryManager(memory_rules_path="../echo_config/memory_rules.json")
    
    # Simulate loading rules and storing an event
    manager.store_event({"timestamp": "2025-07-21T08:00:00Z", "content": "The user's favorite color is blue."})
    
    # Simulate a retrieval query
    retrieval_result = manager.retrieve_info("What is my favorite color?")
    print(f"Retrieval result: {retrieval_result}")
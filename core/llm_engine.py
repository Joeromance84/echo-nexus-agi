# echo-nexus/core/llm_engine.py
import openai  # or another LLM provider like Google's Gemini

class LLMEngine:
    """
    Manages all interactions with the underlying Large Language Model.
    This class handles prompt construction, routing, and response parsing.
    """
    def __init__(self, api_key: str):
        # Initialize the LLM client with the API key.
        self.client = openai.OpenAI(api_key=api_key)

    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 150):
        """
        Sends a constructed prompt to the LLM and returns the generated text.

        Args:
            prompt (str): The complete prompt string to send.
            temperature (float): Controls the randomness of the output.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Replace with your desired model
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "An internal error occurred."

    def route_prompt(self, task_type: str, context: dict):
        """
        A conceptual function for routing prompts based on the task type.
        This would use different templates or system prompts for different
        cognitive operations (e.g., memory lookup, planning, etc.).
        """
        if task_type == "memory_recall":
            # Formulate a specific prompt for memory lookup.
            prompt = f"Based on the following context: {context['context']}, what is the key fact about {context['query']}?"
        elif task_type == "planning":
            # Formulate a prompt for high-level planning.
            prompt = f"Given the goal '{context['goal']}', what are the next 3 logical steps to take?"
        else:
            prompt = f"You are Echo Nexus, an AGI hybrid system. {context['user_input']}"

        return self.generate_response(prompt)
if __name__ == '__main__':
    # This block is for testing the LLM engine locally
    import os
    from dotenv import load_dotenv

    load_dotenv()
    llm = LLMEngine(api_key=os.getenv("OPENAI_API_KEY"))
    test_prompt = "Tell me a short story about an AI that learns to code."
    print("Test LLM Response:")
    print(llm.generate_response(test_prompt))
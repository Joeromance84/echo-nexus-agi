# echo-nexus/core/sensors/text_input.py

class TextInputSensor:
    """
    Text input or sensor emulation for the Echo Nexus system.
    Handles various forms of text-based input and preprocessing.
    """
    def __init__(self):
        self.input_history = []
        self.preprocessing_filters = []

    def receive_input(self, text: str) -> dict:
        """
        Receives raw text input and prepares it for processing.
        
        Args:
            text (str): Raw input text
            
        Returns:
            dict: Processed input with metadata
        """
        processed_input = {
            "raw_text": text,
            "cleaned_text": self._preprocess_text(text),
            "metadata": {
                "length": len(text),
                "word_count": len(text.split()),
                "timestamp": "2025-07-21T00:00:00Z"  # Placeholder
            }
        }
        
        self.input_history.append(processed_input)
        return processed_input

    def _preprocess_text(self, text: str) -> str:
        """Basic text preprocessing."""
        # Remove extra whitespace, normalize case, etc.
        cleaned = text.strip()
        return cleaned

    def add_preprocessing_filter(self, filter_func):
        """Add a custom preprocessing filter function."""
        self.preprocessing_filters.append(filter_func)

    def get_recent_inputs(self, count: int = 5) -> list:
        """Get the most recent inputs."""
        return self.input_history[-count:] if self.input_history else []
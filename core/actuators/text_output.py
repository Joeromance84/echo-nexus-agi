# echo-nexus/core/actuators/text_output.py

class TextOutputActuator:
    """
    Outputs back to the user or system.
    Handles formatting and delivery of responses.
    """
    def __init__(self):
        self.output_history = []
        self.formatting_rules = {
            "max_length": 1000,
            "line_breaks": True,
            "timestamp": True
        }

    def send_output(self, text: str, output_type: str = "response") -> bool:
        """
        Sends formatted output to the user or system.
        
        Args:
            text (str): The text to output
            output_type (str): Type of output (response, alert, debug, etc.)
            
        Returns:
            bool: True if output was successful
        """
        formatted_output = self._format_output(text, output_type)
        
        output_record = {
            "text": formatted_output,
            "type": output_type,
            "timestamp": "2025-07-21T00:00:00Z",  # Placeholder
            "length": len(formatted_output)
        }
        
        self.output_history.append(output_record)
        
        # In a real system, this would send to the actual output channel
        print(f"[{output_type.upper()}] {formatted_output}")
        
        return True

    def _format_output(self, text: str, output_type: str) -> str:
        """Apply formatting rules to the output text."""
        formatted = text
        
        # Apply max length restriction
        if len(formatted) > self.formatting_rules["max_length"]:
            formatted = formatted[:self.formatting_rules["max_length"]] + "..."
        
        # Add timestamp if enabled
        if self.formatting_rules["timestamp"]:
            timestamp = "2025-07-21T00:00:00Z"  # Placeholder
            formatted = f"[{timestamp}] {formatted}"
        
        return formatted

    def set_formatting_rule(self, rule: str, value):
        """Update a formatting rule."""
        self.formatting_rules[rule] = value

    def get_recent_outputs(self, count: int = 5) -> list:
        """Get the most recent outputs."""
        return self.output_history[-count:] if self.output_history else []
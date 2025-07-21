# echo-nexus/builder/code_writer.py

class CodeWriter:
    """
    AI subagent to write/update modules for the Echo Nexus system.
    Generates new code based on specifications and requirements.
    """
    def __init__(self, llm_engine=None):
        self.llm_engine = llm_engine
        self.code_templates = self._load_templates()
        self.generation_history = []

    def _load_templates(self) -> dict:
        """Load code generation templates."""
        return {
            "python_class": '''class {class_name}:
    """
    {class_description}
    """
    def __init__(self):
        {init_body}
    
    def {primary_method}(self, {method_params}):
        """
        {method_description}
        """
        {method_body}
        return {return_statement}
''',
            "python_function": '''def {function_name}({parameters}):
    """
    {function_description}
    
    Args:
        {args_description}
    
    Returns:
        {return_description}
    """
    {function_body}
    return {return_statement}
''',
            "module_header": '''# {module_path}

"""
{module_description}
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

'''
        }

    def generate_module(self, specification: dict) -> str:
        """
        Generate a complete Python module based on specifications.
        
        Args:
            specification (dict): Module requirements and structure
            
        Returns:
            str: Generated Python code
        """
        module_type = specification.get("type", "class")
        
        if module_type == "class":
            return self._generate_class_module(specification)
        elif module_type == "function_collection":
            return self._generate_function_module(specification)
        elif module_type == "data_processor":
            return self._generate_data_processor(specification)
        else:
            return self._generate_generic_module(specification)

    def _generate_class_module(self, spec: dict) -> str:
        """Generate a class-based module."""
        template = self.code_templates["module_header"] + self.code_templates["python_class"]
        
        # Fill in template placeholders
        code = template.format(
            module_path=spec.get("path", "generated_module.py"),
            module_description=spec.get("description", "Auto-generated module"),
            class_name=spec.get("class_name", "GeneratedClass"),
            class_description=spec.get("class_description", "Auto-generated class"),
            init_body=self._generate_init_body(spec.get("attributes", [])),
            primary_method=spec.get("primary_method", "process"),
            method_params=", ".join(spec.get("method_params", ["data"])),
            method_description=spec.get("method_description", "Process input data"),
            method_body=self._generate_method_body(spec.get("method_logic", [])),
            return_statement=spec.get("return_value", "result")
        )
        
        self._record_generation(spec, code)
        return code

    def _generate_function_module(self, spec: dict) -> str:
        """Generate a module with multiple utility functions."""
        header = self.code_templates["module_header"].format(
            module_path=spec.get("path", "utilities.py"),
            module_description=spec.get("description", "Utility functions")
        )
        
        functions = []
        for func_spec in spec.get("functions", []):
            function_code = self.code_templates["python_function"].format(
                function_name=func_spec.get("name", "utility_function"),
                parameters=", ".join(func_spec.get("params", ["data"])),
                function_description=func_spec.get("description", "Utility function"),
                args_description=func_spec.get("args_desc", "data: Input data"),
                return_description=func_spec.get("return_desc", "Processed result"),
                function_body=self._generate_function_body(func_spec.get("logic", [])),
                return_statement=func_spec.get("return_value", "result")
            )
            functions.append(function_code)
        
        code = header + "\n".join(functions)
        self._record_generation(spec, code)
        return code

    def _generate_data_processor(self, spec: dict) -> str:
        """Generate a specialized data processing module."""
        processor_template = '''# {module_path}

"""
{module_description}
Specialized data processor for {data_type} data.
"""

import json
from typing import Dict, List, Any
from datetime import datetime

class {processor_name}:
    """
    Processes {data_type} data with {processing_method} methodology.
    """
    def __init__(self):
        self.processing_rules = {{}}
        self.processed_count = 0
        
    def process(self, data: {input_type}) -> {output_type}:
        """
        Main processing method for {data_type} data.
        """
        # Validation
        if not self._validate_input(data):
            raise ValueError("Invalid input data")
            
        # Processing
        result = self._apply_processing_rules(data)
        self.processed_count += 1
        
        return result
    
    def _validate_input(self, data: {input_type}) -> bool:
        """Validate input data format and content."""
        return data is not None
    
    def _apply_processing_rules(self, data: {input_type}) -> {output_type}:
        """Apply processing transformation rules."""
        # Implementation depends on specific requirements
        return data  # Placeholder
        
    def get_stats(self) -> dict:
        """Get processing statistics."""
        return {{
            "processed_count": self.processed_count,
            "rules_loaded": len(self.processing_rules)
        }}
'''
        
        code = processor_template.format(
            module_path=spec.get("path", "data_processor.py"),
            module_description=spec.get("description", "Data processor"),
            data_type=spec.get("data_type", "generic"),
            processor_name=spec.get("class_name", "DataProcessor"),
            processing_method=spec.get("method", "rule-based"),
            input_type=spec.get("input_type", "Any"),
            output_type=spec.get("output_type", "Any")
        )
        
        self._record_generation(spec, code)
        return code

    def _generate_generic_module(self, spec: dict) -> str:
        """Generate a generic module structure."""
        return f'''# {spec.get("path", "generic_module.py")}

"""
{spec.get("description", "Generic module")}
"""

# Module implementation would be generated based on specific requirements
# This is a placeholder for custom module generation

class GenericModule:
    def __init__(self):
        self.initialized = True
    
    def process(self, input_data):
        """Generic processing method."""
        return input_data
'''

    def _generate_init_body(self, attributes: list) -> str:
        """Generate __init__ method body from attribute list."""
        if not attributes:
            return "        pass"
        
        lines = []
        for attr in attributes:
            if isinstance(attr, str):
                lines.append(f"        self.{attr} = None")
            elif isinstance(attr, dict):
                attr_name = attr.get("name", "attribute")
                attr_default = attr.get("default", "None")
                lines.append(f"        self.{attr_name} = {attr_default}")
        
        return "\n".join(lines)

    def _generate_method_body(self, logic_steps: list) -> str:
        """Generate method body from logic steps."""
        if not logic_steps:
            return "        # Method implementation here\n        pass"
        
        lines = []
        for step in logic_steps:
            lines.append(f"        # {step}")
            lines.append(f"        pass  # Implement: {step}")
        
        return "\n".join(lines)

    def _generate_function_body(self, logic_steps: list) -> str:
        """Generate function body from logic steps."""
        if not logic_steps:
            return "    # Function implementation here\n    pass"
        
        lines = []
        for step in logic_steps:
            lines.append(f"    # {step}")
            lines.append(f"    pass  # Implement: {step}")
        
        return "\n".join(lines)

    def _record_generation(self, specification: dict, generated_code: str):
        """Record code generation for history and analysis."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "specification": specification,
            "code_length": len(generated_code),
            "module_type": specification.get("type", "unknown")
        }
        self.generation_history.append(record)

    def update_existing_module(self, file_path: str, updates: dict) -> str:
        """
        Update an existing module with new functionality.
        
        Args:
            file_path (str): Path to existing module
            updates (dict): Specification for updates
            
        Returns:
            str: Updated module code
        """
        try:
            with open(file_path, 'r') as f:
                existing_code = f.read()
        except FileNotFoundError:
            # If file doesn't exist, create new module
            return self.generate_module(updates)
        
        # Simple update logic - in practice, this would use AST manipulation
        updated_code = existing_code
        
        # Add new methods if specified
        if "new_methods" in updates:
            for method_spec in updates["new_methods"]:
                method_code = self._generate_method_from_spec(method_spec)
                # Insert before the last line (assuming it's a class)
                lines = updated_code.split('\n')
                lines.insert(-1, method_code)
                updated_code = '\n'.join(lines)
        
        return updated_code

    def _generate_method_from_spec(self, method_spec: dict) -> str:
        """Generate a single method from specification."""
        return f'''
    def {method_spec.get("name", "new_method")}(self, {", ".join(method_spec.get("params", []))}):
        """
        {method_spec.get("description", "New method")}
        """
        {self._generate_method_body(method_spec.get("logic", []))}
        return {method_spec.get("return_value", "None")}
'''

    def get_generation_stats(self) -> dict:
        """Get statistics about code generation activity."""
        if not self.generation_history:
            return {"total_generations": 0}
        
        total_lines = sum(record["code_length"] for record in self.generation_history)
        module_types = [record["module_type"] for record in self.generation_history]
        type_distribution = {t: module_types.count(t) for t in set(module_types)}
        
        return {
            "total_generations": len(self.generation_history),
            "total_code_lines": total_lines,
            "module_type_distribution": type_distribution,
            "average_module_size": total_lines / len(self.generation_history)
        }

if __name__ == '__main__':
    # Test the code writer
    writer = CodeWriter()
    
    # Test class generation
    class_spec = {
        "type": "class",
        "path": "test_module.py",
        "description": "Test module for demonstration",
        "class_name": "TestProcessor",
        "class_description": "Processes test data",
        "attributes": ["data", "results"],
        "primary_method": "process_data",
        "method_params": ["input_data"],
        "method_description": "Process input data and return results",
        "method_logic": ["validate input", "transform data", "generate results"],
        "return_value": "self.results"
    }
    
    generated_code = writer.generate_module(class_spec)
    print("Generated Class Module:")
    print(generated_code[:300] + "..." if len(generated_code) > 300 else generated_code)
    
    # Test function generation
    func_spec = {
        "type": "function_collection",
        "path": "utilities.py", 
        "description": "Utility functions collection",
        "functions": [
            {
                "name": "process_text",
                "params": ["text", "options"],
                "description": "Process text with given options",
                "logic": ["clean text", "apply transformations"],
                "return_value": "processed_text"
            }
        ]
    }
    
    func_code = writer.generate_module(func_spec)
    print("\nGenerated Function Module:")
    print(func_code[:300] + "..." if len(func_code) > 300 else func_code)
#!/usr/bin/env python3
"""
Echo AGI Chat Enhancement Processor
Processes code from chat conversations for safe self-enhancement
"""

import re
import ast
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class ChatEnhancementProcessor:
    """Processes code from chat for Echo self-enhancement"""
    
    def __init__(self):
        self.enhancement_input_file = "self_enhancement_input.txt"
        self.chat_log_file = "echo_chat_enhancements.json"
        self.code_patterns = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'def\s+\w+\([^)]*\):',
            r'class\s+\w+\([^)]*\):',
            r'import\s+\w+',
            r'from\s+\w+\s+import'
        ]
        
    def detect_code_in_message(self, message: str) -> List[Dict[str, str]]:
        """Detect code blocks in chat messages"""
        
        code_blocks = []
        
        # Look for code blocks with triple backticks
        python_pattern = r'```python\n(.*?)\n```'
        generic_pattern = r'```\n(.*?)\n```'
        
        # Find Python code blocks
        python_matches = re.findall(python_pattern, message, re.DOTALL)
        for match in python_matches:
            code_blocks.append({
                'type': 'python',
                'code': match.strip(),
                'confidence': 0.9
            })
        
        # Find generic code blocks
        if not python_matches:
            generic_matches = re.findall(generic_pattern, message, re.DOTALL)
            for match in generic_matches:
                if self.looks_like_python(match):
                    code_blocks.append({
                        'type': 'python',
                        'code': match.strip(),
                        'confidence': 0.7
                    })
        
        # Look for inline code patterns
        if not code_blocks:
            inline_code = self.extract_inline_code(message)
            if inline_code:
                code_blocks.append({
                    'type': 'python',
                    'code': inline_code,
                    'confidence': 0.6
                })
        
        return code_blocks
    
    def looks_like_python(self, text: str) -> bool:
        """Heuristic check if text looks like Python code"""
        
        python_indicators = [
            'def ', 'class ', 'import ', 'from ', 'if __name__',
            'return ', 'print(', '.append(', '.extend(',
            'self.', '__init__', 'try:', 'except:', 'finally:',
            'for ', 'while ', 'with ', 'as ', 'lambda '
        ]
        
        # Check if it contains Python-like syntax
        indicators_found = sum(1 for indicator in python_indicators if indicator in text)
        
        # Also check for proper indentation patterns
        lines = text.split('\n')
        indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))
        
        return indicators_found >= 2 or (indicators_found >= 1 and indented_lines >= 2)
    
    def extract_inline_code(self, message: str) -> Optional[str]:
        """Extract inline code snippets from message"""
        
        # Look for function definitions
        func_pattern = r'(def\s+\w+\([^)]*\):[^def]*?)(?=def|\Z)'
        func_matches = re.findall(func_pattern, message, re.DOTALL)
        
        if func_matches:
            return func_matches[0].strip()
        
        # Look for class definitions
        class_pattern = r'(class\s+\w+\([^)]*\):[^class]*?)(?=class|\Z)'
        class_matches = re.findall(class_pattern, message, re.DOTALL)
        
        if class_matches:
            return class_matches[0].strip()
        
        # Look for import statements and related code
        import_lines = []
        lines = message.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                # Collect this import and following related lines
                import_block = [line.strip()]
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line and (next_line.startswith(' ') or 
                                    any(keyword in next_line for keyword in ['def ', 'class ', '='])):
                        import_block.append(next_line)
                    elif next_line:
                        break
                
                if len(import_block) > 1:
                    import_lines.extend(import_block)
        
        if import_lines:
            return '\n'.join(import_lines)
        
        return None
    
    def validate_chat_code(self, code_block: Dict[str, str]) -> Dict[str, Any]:
        """Validate code from chat before enhancement"""
        
        validation = {
            'valid': False,
            'syntax_valid': False,
            'safety_check': False,
            'enhancement_type': 'unknown',
            'target_module': None,
            'confidence': code_block['confidence'],
            'errors': [],
            'warnings': []
        }
        
        code = code_block['code']
        
        # 1. Syntax validation
        try:
            ast.parse(code)
            validation['syntax_valid'] = True
        except SyntaxError as e:
            validation['errors'].append(f"Syntax error: {e}")
            return validation
        
        # 2. Safety checks
        if self.is_code_safe(code):
            validation['safety_check'] = True
        else:
            validation['errors'].append("Code contains potentially unsafe operations")
            return validation
        
        # 3. Determine enhancement type and target
        enhancement_info = self.analyze_enhancement_intent(code)
        validation.update(enhancement_info)
        
        # 4. Final validation
        if validation['syntax_valid'] and validation['safety_check']:
            validation['valid'] = True
        
        return validation
    
    def is_code_safe(self, code: str) -> bool:
        """Check if code is safe for self-enhancement"""
        
        # Forbidden patterns for safety
        dangerous_patterns = [
            'os.system', 'subprocess.', 'exec(', 'eval(',
            'open(', '__import__', 'getattr', 'setattr',
            'delattr', 'globals(', 'locals(', 'vars(',
            'input(', 'raw_input', 'file(', 'execfile',
            'reload(', 'compile(', 'import os', 'import sys',
            'import subprocess', 'import shutil'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False
        
        # Check for file system operations
        if any(op in code for op in ['open(', 'with open', 'file(']):
            # Allow only specific safe file operations
            safe_files = ['self_enhancement_input.txt', 'echo_enhancement_log.json']
            if not any(safe_file in code for safe_file in safe_files):
                return False
        
        return True
    
    def analyze_enhancement_intent(self, code: str) -> Dict[str, Any]:
        """Analyze what the code is intended to enhance"""
        
        intent = {
            'enhancement_type': 'function_addition',
            'target_module': 'echo_nexus/echo_enhancements.py',
            'description': 'Generic enhancement'
        }
        
        # Analyze code content to determine intent
        if 'class ' in code and 'Echo' in code:
            intent.update({
                'enhancement_type': 'class_enhancement',
                'target_module': 'echo_nexus/echo_mind.py',
                'description': 'Echo core class enhancement'
            })
        
        elif any(keyword in code.lower() for keyword in ['agent', 'reasoning', 'think']):
            intent.update({
                'enhancement_type': 'reasoning_enhancement',
                'target_module': 'core_agents/reasoning.py',
                'description': 'Reasoning capability enhancement'
            })
        
        elif any(keyword in code.lower() for keyword in ['creative', 'generate', 'innovation']):
            intent.update({
                'enhancement_type': 'creativity_enhancement',
                'target_module': 'core_agents/creativity.py',
                'description': 'Creative capability enhancement'
            })
        
        elif any(keyword in code.lower() for keyword in ['memory', 'remember', 'store']):
            intent.update({
                'enhancement_type': 'memory_enhancement',
                'target_module': 'core_agents/memory.py',
                'description': 'Memory system enhancement'
            })
        
        elif any(keyword in code.lower() for keyword in ['action', 'execute', 'perform']):
            intent.update({
                'enhancement_type': 'action_enhancement',
                'target_module': 'core_agents/action.py',
                'description': 'Action capability enhancement'
            })
        
        elif any(keyword in code.lower() for keyword in ['blade', 'refactor', 'optimize']):
            intent.update({
                'enhancement_type': 'blade_enhancement',
                'target_module': 'blades/refactor_blade.py',
                'description': 'Refactor blade enhancement'
            })
        
        return intent
    
    def prepare_enhancement_input(self, code_block: Dict[str, str], validation: Dict[str, Any], user_message: str) -> str:
        """Prepare code for enhancement system"""
        
        enhancement_input = f"""# Echo AGI Chat-Driven Self-Enhancement
# Submitted via chat: {datetime.now().isoformat()}
# Enhancement type: {validation['enhancement_type']}
# Target module: {validation['target_module']}
# Validation confidence: {validation['confidence']}

# Original user message context:
# {user_message[:200]}{'...' if len(user_message) > 200 else ''}

# Validated enhancement code:
{code_block['code']}

# Enhancement metadata
ENHANCEMENT_STATUS=READY_FOR_APPLICATION
LAST_VALIDATION=PASSED
VALIDATION_CONFIDENCE={validation['confidence']}
ENHANCEMENT_TYPE={validation['enhancement_type']}
TARGET_MODULE={validation['target_module']}
"""
        
        return enhancement_input
    
    def process_chat_message(self, message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a chat message for potential self-enhancement code"""
        
        result = {
            'code_detected': False,
            'code_blocks': [],
            'enhancement_prepared': False,
            'validation_results': [],
            'status': 'no_code_detected'
        }
        
        # Detect code in message
        code_blocks = self.detect_code_in_message(message)
        
        if not code_blocks:
            return result
        
        result['code_detected'] = True
        result['code_blocks'] = code_blocks
        result['status'] = 'code_detected'
        
        # Validate each code block
        valid_enhancements = []
        
        for code_block in code_blocks:
            validation = self.validate_chat_code(code_block)
            result['validation_results'].append(validation)
            
            if validation['valid']:
                valid_enhancements.append((code_block, validation))
        
        # If we have valid enhancements, prepare them
        if valid_enhancements:
            # For now, process the first valid enhancement
            code_block, validation = valid_enhancements[0]
            
            enhancement_input = self.prepare_enhancement_input(code_block, validation, message)
            
            # Write to enhancement input file
            with open(self.enhancement_input_file, 'w') as f:
                f.write(enhancement_input)
            
            result['enhancement_prepared'] = True
            result['status'] = 'enhancement_ready'
            
            # Log the chat enhancement
            self.log_chat_enhancement(message, code_block, validation, user_context)
            
            print(f"Echo: Code enhancement prepared from chat")
            print(f"Type: {validation['enhancement_type']}")
            print(f"Target: {validation['target_module']}")
            print(f"Confidence: {validation['confidence']}")
        
        else:
            result['status'] = 'validation_failed'
            print("Echo: Code detected in chat but validation failed")
        
        return result
    
    def log_chat_enhancement(self, message: str, code_block: Dict[str, str], 
                           validation: Dict[str, Any], user_context: Dict[str, Any] = None):
        """Log chat-driven enhancement attempt"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message_excerpt': message[:300],
            'code_type': code_block['type'],
            'code_lines': len(code_block['code'].split('\n')),
            'enhancement_type': validation['enhancement_type'],
            'target_module': validation['target_module'],
            'confidence': validation['confidence'],
            'validation_passed': validation['valid'],
            'user_context': user_context or {}
        }
        
        # Load existing log
        if os.path.exists(self.chat_log_file):
            with open(self.chat_log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {'chat_enhancements': []}
        
        # Add entry
        log_data['chat_enhancements'].append(log_entry)
        
        # Save updated log
        with open(self.chat_log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_enhancement_suggestions(self, message: str) -> List[str]:
        """Suggest enhancement opportunities based on user message"""
        
        suggestions = []
        
        # Keyword-based suggestions
        if any(word in message.lower() for word in ['improve', 'better', 'enhance', 'upgrade']):
            suggestions.append("I can process code enhancements from your messages")
        
        if any(word in message.lower() for word in ['function', 'method', 'def']):
            suggestions.append("Share Python functions and I'll integrate them into my capabilities")
        
        if any(word in message.lower() for word in ['memory', 'remember', 'learn']):
            suggestions.append("I can enhance my memory systems with new capabilities you provide")
        
        if any(word in message.lower() for word in ['creative', 'generate', 'innovation']):
            suggestions.append("I can integrate new creative algorithms into my creativity engine")
        
        return suggestions

def main():
    """Main chat enhancement processor function"""
    
    print("💬 Echo AGI Chat Enhancement Processor")
    print("Processing chat messages for self-enhancement opportunities...")
    
    processor = ChatEnhancementProcessor()
    
    # Example usage
    test_message = """
    Here's a new function for you:
    ```python
    def enhanced_reasoning(self, problem):
        # Advanced reasoning algorithm
        confidence = 0.0
        for step in self.reasoning_steps:
            confidence += step.evaluate(problem)
        return confidence / len(self.reasoning_steps)
    ```
    This should improve your reasoning capabilities.
    """
    
    result = processor.process_chat_message(test_message)
    
    print(f"Code detected: {result['code_detected']}")
    print(f"Enhancement prepared: {result['enhancement_prepared']}")
    print(f"Status: {result['status']}")

if __name__ == '__main__':
    main()
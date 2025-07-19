"""
Mimic Engine - Advanced Code Style and Pattern Mimicry
"""

import ast
import re
import json
from typing import Dict, Any, List, Tuple
from mirror_logger import MirrorLogger

class MimicEngine:
    def __init__(self, mirror_logger: MirrorLogger):
        self.mirror_logger = mirror_logger
        self.style_patterns = {}
        self.learned_structures = {}
    
    def analyze_code_features(self, code: str) -> Dict[str, Any]:
        """Deep analysis of code features for mimicry"""
        features = {
            'structure': {},
            'style': {},
            'patterns': {},
            'complexity': {}
        }
        
        try:
            # Parse AST for structural analysis
            tree = ast.parse(code)
            features['structure'] = self._analyze_ast_structure(tree)
        except:
            # Fallback to regex-based analysis
            features['structure'] = self._analyze_regex_structure(code)
        
        # Style analysis
        features['style'] = self._analyze_code_style(code)
        
        # Pattern analysis
        features['patterns'] = self._analyze_code_patterns(code)
        
        # Complexity analysis
        features['complexity'] = self._analyze_complexity(code)
        
        return features
    
    def _analyze_ast_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code structure using AST"""
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'variables': [],
            'control_flow': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                structure['functions'].append({
                    'name': node.name,
                    'args': len(node.args.args),
                    'decorators': len(node.decorator_list),
                    'docstring': ast.get_docstring(node) is not None
                })
            elif isinstance(node, ast.ClassDef):
                structure['classes'].append({
                    'name': node.name,
                    'bases': len(node.bases),
                    'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    structure['imports'].append({'type': 'import', 'name': alias.name})
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    structure['imports'].append({'type': 'from', 'module': module, 'name': alias.name})
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                structure['control_flow'].append(type(node).__name__)
        
        return structure
    
    def _analyze_regex_structure(self, code: str) -> Dict[str, Any]:
        """Fallback regex-based structure analysis"""
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'control_flow': []
        }
        
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            
            # Function definitions
            func_match = re.match(r'def\s+(\w+)\s*\(([^)]*)\):', stripped)
            if func_match:
                structure['functions'].append({
                    'name': func_match.group(1),
                    'args': len([arg.strip() for arg in func_match.group(2).split(',') if arg.strip()]),
                    'decorators': 0,
                    'docstring': False
                })
            
            # Class definitions
            class_match = re.match(r'class\s+(\w+)(?:\([^)]*\))?:', stripped)
            if class_match:
                structure['classes'].append({
                    'name': class_match.group(1),
                    'bases': 0,
                    'methods': 0
                })
            
            # Imports
            if stripped.startswith('import '):
                structure['imports'].append({'type': 'import', 'name': stripped[7:]})
            elif stripped.startswith('from '):
                structure['imports'].append({'type': 'from', 'name': stripped})
        
        return structure
    
    def _analyze_code_style(self, code: str) -> Dict[str, Any]:
        """Analyze coding style preferences"""
        lines = code.split('\n')
        
        style = {
            'indentation': 'spaces',
            'indent_size': 4,
            'line_length': 0,
            'comment_style': {},
            'naming_convention': {},
            'docstring_style': 'triple_quotes'
        }
        
        # Analyze indentation
        indent_chars = []
        for line in lines:
            if line.startswith((' ', '\t')):
                leading = len(line) - len(line.lstrip())
                if line.startswith('\t'):
                    indent_chars.append('tabs')
                else:
                    indent_chars.append('spaces')
                    if leading > 0:
                        style['indent_size'] = leading
        
        if indent_chars:
            style['indentation'] = max(set(indent_chars), key=indent_chars.count)
        
        # Analyze line length
        style['line_length'] = max(len(line) for line in lines) if lines else 0
        
        # Comment analysis
        comments = [line.strip() for line in lines if line.strip().startswith('#')]
        style['comment_style'] = {
            'frequency': len(comments) / max(len(lines), 1),
            'style': 'hash' if comments else 'none'
        }
        
        return style
    
    def _analyze_code_patterns(self, code: str) -> Dict[str, Any]:
        """Identify common code patterns"""
        patterns = {
            'error_handling': False,
            'logging': False,
            'type_hints': False,
            'list_comprehensions': False,
            'context_managers': False,
            'decorators': False
        }
        
        # Simple pattern detection
        if 'try:' in code and 'except' in code:
            patterns['error_handling'] = True
        
        if any(log_word in code for log_word in ['print(', 'logging.', 'logger.']):
            patterns['logging'] = True
        
        if '->' in code or ': str' in code or ': int' in code:
            patterns['type_hints'] = True
        
        if '[' in code and 'for' in code and 'in' in code and ']' in code:
            patterns['list_comprehensions'] = True
        
        if 'with ' in code and ':' in code:
            patterns['context_managers'] = True
        
        if '@' in code:
            patterns['decorators'] = True
        
        return patterns
    
    def _analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        complexity = {
            'lines_of_code': len(non_empty_lines),
            'cyclomatic_complexity': 1,  # Start with 1
            'nesting_depth': 0,
            'function_count': len(re.findall(r'def\s+\w+', code)),
            'class_count': len(re.findall(r'class\s+\w+', code))
        }
        
        # Simple cyclomatic complexity
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally']
        for keyword in complexity_keywords:
            complexity['cyclomatic_complexity'] += code.count(keyword)
        
        # Nesting depth
        max_depth = 0
        current_depth = 0
        for line in lines:
            stripped = line.strip()
            if any(keyword + ' ' in stripped or keyword + ':' in stripped 
                   for keyword in ['if', 'for', 'while', 'try', 'with', 'def', 'class']):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif stripped in ['else:', 'elif', 'except:', 'finally:']:
                pass  # Don't change depth
            elif stripped == '' or stripped.startswith('#'):
                pass  # Don't change depth
            else:
                # Rough heuristic: if line doesn't start with space, reset depth
                if not line.startswith((' ', '\t')):
                    current_depth = 0
        
        complexity['nesting_depth'] = max_depth
        
        return complexity
    
    def mimic_style(self, example_code: str, new_goal: str, target_features: Dict[str, Any] = None) -> str:
        """Generate code that mimics the style of example code"""
        if not target_features:
            target_features = self.analyze_code_features(example_code)
        
        # Get similar patterns from mirror logger
        similar_observations = self.mirror_logger.get_similar_observations(['code', 'function', new_goal])
        
        # Generate code structure
        mimicked_code = self._generate_code_structure(target_features, new_goal, similar_observations)
        
        # Apply style patterns
        mimicked_code = self._apply_style_patterns(mimicked_code, target_features['style'])
        
        return mimicked_code
    
    def _generate_code_structure(self, features: Dict[str, Any], goal: str, observations: List[Dict]) -> str:
        """Generate basic code structure based on learned features"""
        structure = features.get('structure', {})
        style = features.get('style', {})
        
        # Start with imports if original had them
        code_parts = []
        
        if structure.get('imports'):
            code_parts.append("# Imports based on learned patterns")
            for imp in structure['imports'][:3]:  # Limit imports
                if imp['type'] == 'import':
                    code_parts.append(f"import {imp['name'].split('.')[0]}")
                elif imp['type'] == 'from':
                    code_parts.append(f"from {imp['module']} import {imp['name']}")
            code_parts.append("")
        
        # Generate main function based on goal
        func_name = goal.lower().replace(' ', '_').replace('-', '_')
        code_parts.append(f"def {func_name}():")
        
        # Add docstring if original had them
        if any(func.get('docstring') for func in structure.get('functions', [])):
            code_parts.append(f'    """')
            code_parts.append(f'    {goal} - Generated using learned patterns')
            code_parts.append(f'    """')
        
        # Add basic structure
        if features.get('patterns', {}).get('error_handling'):
            code_parts.extend([
                "    try:",
                f"        # Implement {goal}",
                "        result = {'success': True, 'message': 'Operation completed'}",
                "        return result",
                "    except Exception as e:",
                "        return {'success': False, 'error': str(e)}"
            ])
        else:
            code_parts.extend([
                f"    # Implement {goal}",
                "    result = {'success': True}",
                "    return result"
            ])
        
        return '\n'.join(code_parts)
    
    def _apply_style_patterns(self, code: str, style_features: Dict[str, Any]) -> str:
        """Apply style patterns to generated code"""
        lines = code.split('\n')
        
        # Apply indentation style
        if style_features.get('indentation') == 'tabs':
            lines = [line.replace('    ', '\t') for line in lines]
        elif style_features.get('indent_size', 4) != 4:
            indent_size = style_features['indent_size']
            lines = [line.replace('    ', ' ' * indent_size) for line in lines]
        
        # Add comments if original was heavily commented
        comment_freq = style_features.get('comment_style', {}).get('frequency', 0)
        if comment_freq > 0.3:  # If more than 30% of lines were comments
            # Add some explanatory comments
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') or line.strip().startswith('try:'):
                    lines.insert(i, f"{' ' * (len(line) - len(line.lstrip()))}# {line.strip()}")
                    break
        
        return '\n'.join(lines)
    
    def self_evaluate(self, original: str, mimic: str) -> Dict[str, Any]:
        """Evaluate the quality of mimicry"""
        original_features = self.analyze_code_features(original)
        mimic_features = self.analyze_code_features(mimic)
        
        evaluation = {
            'overall_similarity': 0.0,
            'structure_similarity': 0.0,
            'style_similarity': 0.0,
            'pattern_similarity': 0.0,
            'recommendations': []
        }
        
        # Structure similarity
        struct_scores = []
        orig_struct = original_features['structure']
        mimic_struct = mimic_features['structure']
        
        # Compare function counts
        orig_func_count = len(orig_struct.get('functions', []))
        mimic_func_count = len(mimic_struct.get('functions', []))
        if orig_func_count > 0:
            struct_scores.append(min(mimic_func_count / orig_func_count, 1.0))
        
        # Compare import counts
        orig_import_count = len(orig_struct.get('imports', []))
        mimic_import_count = len(mimic_struct.get('imports', []))
        if orig_import_count > 0:
            struct_scores.append(min(mimic_import_count / orig_import_count, 1.0))
        
        evaluation['structure_similarity'] = sum(struct_scores) / len(struct_scores) if struct_scores else 0.0
        
        # Style similarity
        style_scores = []
        orig_style = original_features['style']
        mimic_style = mimic_features['style']
        
        # Compare indentation
        if orig_style.get('indentation') == mimic_style.get('indentation'):
            style_scores.append(1.0)
        else:
            style_scores.append(0.0)
        
        # Compare line length patterns
        orig_length = orig_style.get('line_length', 0)
        mimic_length = mimic_style.get('line_length', 0)
        if orig_length > 0:
            style_scores.append(1.0 - abs(orig_length - mimic_length) / orig_length)
        
        evaluation['style_similarity'] = sum(style_scores) / len(style_scores) if style_scores else 0.0
        
        # Pattern similarity
        orig_patterns = original_features.get('patterns', {})
        mimic_patterns = mimic_features.get('patterns', {})
        
        pattern_matches = sum(1 for key in orig_patterns if orig_patterns[key] == mimic_patterns.get(key, False))
        total_patterns = len(orig_patterns)
        evaluation['pattern_similarity'] = pattern_matches / total_patterns if total_patterns > 0 else 0.0
        
        # Overall similarity
        evaluation['overall_similarity'] = (
            evaluation['structure_similarity'] * 0.4 +
            evaluation['style_similarity'] * 0.3 +
            evaluation['pattern_similarity'] * 0.3
        )
        
        # Generate recommendations
        if evaluation['structure_similarity'] < 0.7:
            evaluation['recommendations'].append("Add more functions or classes to match original structure")
        
        if evaluation['style_similarity'] < 0.7:
            evaluation['recommendations'].append("Adjust indentation and line length to match original style")
        
        if evaluation['pattern_similarity'] < 0.7:
            evaluation['recommendations'].append("Include more patterns like error handling, logging, or type hints")
        
        # Log evaluation for learning
        self.mirror_logger.observe(
            input_text=f"MIMICRY_EVALUATION: {evaluation['overall_similarity']:.2f}",
            response_text=f"SIMILARITY_BREAKDOWN: Structure {evaluation['structure_similarity']:.2f}, Style {evaluation['style_similarity']:.2f}, Patterns {evaluation['pattern_similarity']:.2f}",
            context_snapshot={
                'evaluation_scores': evaluation,
                'original_features': original_features,
                'mimic_features': mimic_features,
                'action_type': 'mimicry_evaluation'
            },
            outcome='evaluated'
        )
        
        return evaluation
    
    def learn_from_correction(self, original_mimic: str, corrected_code: str, feedback: str):
        """Learn from human corrections to improve mimicry"""
        correction_analysis = {
            'original_mimic': original_mimic,
            'corrected_code': corrected_code,
            'feedback': feedback,
            'learned_improvements': []
        }
        
        # Analyze what changed
        orig_features = self.analyze_code_features(original_mimic)
        corrected_features = self.analyze_code_features(corrected_code)
        
        # Identify improvements
        if corrected_features['complexity']['lines_of_code'] > orig_features['complexity']['lines_of_code']:
            correction_analysis['learned_improvements'].append("Add more detailed implementation")
        
        if len(corrected_features['structure']['functions']) > len(orig_features['structure']['functions']):
            correction_analysis['learned_improvements'].append("Break code into more functions")
        
        # Log the correction for future learning
        self.mirror_logger.observe_code_pattern(
            original_code=original_mimic,
            fixed_code=corrected_code,
            problem_description=f"human_correction: {feedback}"
        )
        
        return correction_analysis
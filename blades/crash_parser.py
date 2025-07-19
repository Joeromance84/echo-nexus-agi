#!/usr/bin/env python3
"""
CrashParser - Phase 1 Core Blade
Focused on parsing specific, common error types (starting with Python SyntaxError and IndentationError)
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CrashParser:
    """
    Phase 1 Core: Targeted error parser for specific error types
    Initially handles Python IndentationError and SyntaxError
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger('CrashParser')
        
        # Phase 1: Focus on specific, common error patterns
        self.error_patterns = {
            'IndentationError': {
                'pattern': r'IndentationError:\s*(.*?)\s*\(.*?line\s*(\d+)\)',
                'file_pattern': r'File\s*"([^"]+)"',
                'severity': 'high',
                'auto_fixable': True
            },
            'SyntaxError': {
                'pattern': r'SyntaxError:\s*(.*?)\s*\(.*?line\s*(\d+)\)',
                'file_pattern': r'File\s*"([^"]+)"',
                'severity': 'high', 
                'auto_fixable': True
            },
            'NameError': {
                'pattern': r'NameError:\s*name\s*[\'"]([^\'"]+)[\'"]\s*is\s*not\s*defined',
                'file_pattern': r'File\s*"([^"]+)".*?line\s*(\d+)',
                'severity': 'medium',
                'auto_fixable': False
            },
            'ImportError': {
                'pattern': r'ImportError:\s*No\s*module\s*named\s*[\'"]([^\'"]+)[\'"]',
                'file_pattern': r'File\s*"([^"]+)".*?line\s*(\d+)',
                'severity': 'medium',
                'auto_fixable': True
            }
        }
    
    def parse_error_log(self, error_text: str) -> Dict:
        """
        Main parsing function - extracts structured information from error text
        Phase 1: Simple, reliable parsing for common Python errors
        """
        if not error_text or not error_text.strip():
            return {'success': False, 'reason': 'empty_error_text'}
        
        # Try to identify error type and extract information
        for error_type, config in self.error_patterns.items():
            match_result = self._match_error_pattern(error_text, error_type, config)
            if match_result['matched']:
                self.logger.info(f"Successfully parsed {error_type}: {match_result['file_path']}:{match_result['line_number']}")
                return {
                    'success': True,
                    'error_type': error_type,
                    'file_path': match_result['file_path'],
                    'line_number': match_result['line_number'],
                    'error_message': match_result['error_message'],
                    'severity': config['severity'],
                    'auto_fixable': config['auto_fixable'],
                    'raw_error': error_text,
                    'extracted_info': match_result.get('extracted_info', {})
                }
        
        # If no specific pattern matched, try generic parsing
        generic_result = self._generic_parse(error_text)
        if generic_result['success']:
            return generic_result
        
        return {
            'success': False,
            'reason': 'unrecognized_error_pattern',
            'raw_error': error_text
        }
    
    def _match_error_pattern(self, error_text: str, error_type: str, config: Dict) -> Dict:
        """Match error text against specific pattern"""
        result = {
            'matched': False,
            'file_path': None,
            'line_number': None,
            'error_message': None,
            'extracted_info': {}
        }
        
        try:
            # Extract main error information
            main_match = re.search(config['pattern'], error_text, re.MULTILINE | re.IGNORECASE)
            if not main_match:
                return result
            
            # Extract file path
            file_match = re.search(config['file_pattern'], error_text, re.MULTILINE | re.IGNORECASE)
            if not file_match:
                return result
            
            result['matched'] = True
            result['file_path'] = file_match.group(1)
            result['error_message'] = main_match.group(1) if main_match.groups() else error_type
            
            # Extract line number (different patterns have line number in different groups)
            if len(main_match.groups()) >= 2 and main_match.group(2).isdigit():
                result['line_number'] = int(main_match.group(2))
            else:
                # Try to find line number in file pattern match
                line_match = re.search(r'line\s*(\d+)', error_text, re.IGNORECASE)
                if line_match:
                    result['line_number'] = int(line_match.group(1))
            
            # Error-specific extraction
            if error_type == 'IndentationError':
                result['extracted_info'] = self._extract_indentation_info(error_text, main_match)
            elif error_type == 'SyntaxError':
                result['extracted_info'] = self._extract_syntax_info(error_text, main_match)
            elif error_type == 'NameError':
                result['extracted_info'] = {'undefined_name': main_match.group(1)}
            elif error_type == 'ImportError':
                result['extracted_info'] = {'missing_module': main_match.group(1)}
                
        except Exception as e:
            self.logger.error(f"Error matching pattern for {error_type}: {e}")
            result['matched'] = False
        
        return result
    
    def _extract_indentation_info(self, error_text: str, match) -> Dict:
        """Extract specific information for IndentationError"""
        info = {}
        
        # Common indentation error patterns
        if 'expected an indented block' in error_text.lower():
            info['error_subtype'] = 'missing_indentation'
            info['fix_hint'] = 'add_indentation'
        elif 'unexpected indent' in error_text.lower():
            info['error_subtype'] = 'extra_indentation'
            info['fix_hint'] = 'remove_indentation'
        elif 'unindent does not match' in error_text.lower():
            info['error_subtype'] = 'misaligned_indentation'
            info['fix_hint'] = 'align_indentation'
        else:
            info['error_subtype'] = 'general_indentation'
            info['fix_hint'] = 'fix_indentation'
        
        return info
    
    def _extract_syntax_info(self, error_text: str, match) -> Dict:
        """Extract specific information for SyntaxError"""
        info = {}
        
        # Common syntax error patterns
        if 'invalid syntax' in error_text.lower():
            info['error_subtype'] = 'invalid_syntax'
            
            # Check for common syntax issues
            if ':' in error_text and 'expected' in error_text.lower():
                info['fix_hint'] = 'missing_colon'
            elif 'parenthes' in error_text.lower():
                info['fix_hint'] = 'unmatched_parentheses'
            elif 'bracket' in error_text.lower():
                info['fix_hint'] = 'unmatched_brackets'
            elif 'quote' in error_text.lower():
                info['fix_hint'] = 'unmatched_quotes'
            else:
                info['fix_hint'] = 'general_syntax'
        
        elif 'unexpected eof' in error_text.lower():
            info['error_subtype'] = 'unexpected_eof'
            info['fix_hint'] = 'incomplete_statement'
        
        return info
    
    def _generic_parse(self, error_text: str) -> Dict:
        """Generic parsing for unrecognized error patterns"""
        # Try to extract any file path and line number
        file_match = re.search(r'File\s*"([^"]+)"', error_text, re.IGNORECASE)
        line_match = re.search(r'line\s*(\d+)', error_text, re.IGNORECASE)
        
        if file_match or line_match:
            return {
                'success': True,
                'error_type': 'generic',
                'file_path': file_match.group(1) if file_match else 'unknown',
                'line_number': int(line_match.group(1)) if line_match else None,
                'error_message': error_text.split('\n')[0][:100],  # First line, truncated
                'severity': 'unknown',
                'auto_fixable': False,
                'raw_error': error_text
            }
        
        return {'success': False, 'reason': 'no_parseable_information'}
    
    def analyze_file_for_errors(self, file_path: str) -> List[Dict]:
        """
        Analyze a specific file for potential syntax errors
        Phase 1: Simple compilation check
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return [{'error': f'File not found: {file_path}'}]
            
            # Try to compile the Python file
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            try:
                compile(source_code, str(file_path), 'exec')
                return []  # No syntax errors
                
            except SyntaxError as e:
                # Convert SyntaxError to our standard format
                error_info = {
                    'error_type': 'SyntaxError',
                    'file_path': str(file_path),
                    'line_number': e.lineno,
                    'error_message': str(e.msg),
                    'severity': 'high',
                    'auto_fixable': True,
                    'column': e.offset,
                    'text': e.text.strip() if e.text else None
                }
                return [error_info]
                
            except IndentationError as e:
                # Convert IndentationError to our standard format
                error_info = {
                    'error_type': 'IndentationError',
                    'file_path': str(file_path),
                    'line_number': e.lineno,
                    'error_message': str(e.msg),
                    'severity': 'high',
                    'auto_fixable': True,
                    'column': e.offset,
                    'text': e.text.strip() if e.text else None
                }
                return [error_info]
                
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return [{'error': f'Analysis failed: {e}'}]
    
    def get_error_context(self, file_path: str, line_number: int, context_lines: int = 3) -> Dict:
        """
        Get surrounding lines for error context
        Phase 1: Simple line extraction
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'error': f'File not found: {file_path}'}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if line_number <= 0 or line_number > len(lines):
                return {'error': f'Invalid line number: {line_number}'}
            
            # Extract context (convert to 0-based indexing)
            start_line = max(0, line_number - context_lines - 1)
            end_line = min(len(lines), line_number + context_lines)
            
            context = {
                'file_path': str(file_path),
                'error_line': line_number,
                'error_text': lines[line_number - 1].rstrip() if line_number <= len(lines) else '',
                'context_lines': [],
                'total_lines': len(lines)
            }
            
            for i in range(start_line, end_line):
                context['context_lines'].append({
                    'line_number': i + 1,
                    'text': lines[i].rstrip(),
                    'is_error_line': (i + 1) == line_number
                })
            
            return context
            
        except Exception as e:
            self.logger.error(f"Error getting context for {file_path}:{line_number}: {e}")
            return {'error': str(e)}
    
    def run(self, command: str, data: Dict = None) -> Dict:
        """
        Main entry point for EchoMind integration
        Phase 1: Simple command processing
        """
        if data is None:
            data = {}
        
        try:
            if command == 'parse_error':
                error_text = data.get('error_text', '')
                return self.parse_error_log(error_text)
                
            elif command == 'analyze_file':
                file_path = data.get('file_path', '')
                errors = self.analyze_file_for_errors(file_path)
                return {'success': True, 'errors': errors}
                
            elif command == 'get_context':
                file_path = data.get('file_path', '')
                line_number = data.get('line_number', 0)
                context = self.get_error_context(file_path, line_number)
                return {'success': True, 'context': context}
                
            else:
                return {'success': False, 'error': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"CrashParser run failed: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """CLI interface for testing CrashParser"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CrashParser - Phase 1 Error Analysis")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--error-text', help='Error text to parse')
    parser.add_argument('--analyze-file', help='File to analyze for errors')
    parser.add_argument('--test', action='store_true', help='Run test cases')
    
    args = parser.parse_args()
    
    crash_parser = CrashParser(args.project)
    
    if args.test:
        # Test cases for Phase 1
        test_errors = [
            'File "test.py", line 5\n    return x\nIndentationError: expected an indented block',
            'File "app.py", line 12\n    if x == 1\nSyntaxError: invalid syntax',
            'File "main.py", line 8, in <module>\nNameError: name \'undefined_var\' is not defined'
        ]
        
        for i, error in enumerate(test_errors, 1):
            print(f"\nTest Case {i}:")
            result = crash_parser.parse_error_log(error)
            print(f"Result: {result}")
        
        return 0
    
    if args.error_text:
        result = crash_parser.parse_error_log(args.error_text)
        print(f"Parse Result: {json.dumps(result, indent=2)}")
        return 0
    
    if args.analyze_file:
        errors = crash_parser.analyze_file_for_errors(args.analyze_file)
        print(f"File Analysis: {json.dumps(errors, indent=2)}")
        return 0
    
    print("CrashParser Phase 1 ready. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
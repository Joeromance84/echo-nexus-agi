#!/usr/bin/env python3
"""
RepairEngine - Phase 1 Core Blade
Applies symbolic fixes based on RepairGenome.json patterns
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class RepairEngine:
    """
    Phase 1 Core: Symbolic repair system based on pattern matching
    Uses RepairGenome.json for hard-coded fix strategies
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.genome_path = self.project_root / "data" / "RepairGenome.json"
        self.logger = logging.getLogger('RepairEngine')
        
        # Load repair genome
        self.repair_genome = self.load_repair_genome()
        
        # Phase 1: Simple repair statistics
        self.repair_stats = {
            'total_attempts': 0,
            'successful_repairs': 0,
            'failed_repairs': 0,
            'rules_used': {}
        }
    
    def load_repair_genome(self) -> Dict:
        """Load the RepairGenome.json knowledge base"""
        try:
            if self.genome_path.exists():
                with open(self.genome_path, 'r') as f:
                    genome = json.load(f)
                self.logger.info(f"Loaded repair genome with {len(genome.get('rules', []))} rules")
                return genome
            else:
                # Create default Phase 1 genome
                default_genome = self.create_default_genome()
                self.genome_path.parent.mkdir(exist_ok=True)
                with open(self.genome_path, 'w') as f:
                    json.dump(default_genome, f, indent=2)
                self.logger.info("Created default RepairGenome.json")
                return default_genome
                
        except Exception as e:
            self.logger.error(f"Failed to load repair genome: {e}")
            return self.create_default_genome()
    
    def create_default_genome(self) -> Dict:
        """Create default Phase 1 repair patterns"""
        return {
            "version": "1.0.0",
            "description": "Phase 1 RepairGenome - Basic symbolic repair patterns",
            "last_updated": datetime.now().isoformat() + 'Z',
            "rules": [
                {
                    "rule_id": "rule_01",
                    "name": "Fix Missing Indentation",
                    "error_type": "IndentationError",
                    "error_subtype": "missing_indentation",
                    "pattern": r"^\s*(return|pass|break|continue|raise)\s*$",
                    "fix_strategy": "add_indentation",
                    "replacement": r"    \1",
                    "confidence": 0.9,
                    "auto_apply": True,
                    "description": "Add 4-space indentation to statements that need it"
                },
                {
                    "rule_id": "rule_02", 
                    "name": "Fix Extra Indentation",
                    "error_type": "IndentationError",
                    "error_subtype": "extra_indentation",
                    "pattern": r"^(\s{8,})(.*?)$",
                    "fix_strategy": "reduce_indentation",
                    "replacement": r"    \2",
                    "confidence": 0.8,
                    "auto_apply": True,
                    "description": "Reduce excessive indentation to 4 spaces"
                },
                {
                    "rule_id": "rule_03",
                    "name": "Add Missing Colon",
                    "error_type": "SyntaxError",
                    "error_subtype": "invalid_syntax",
                    "pattern": r"^(\s*)(if|elif|else|for|while|def|class|try|except|finally|with)\s+([^:]+?)$",
                    "fix_strategy": "add_colon",
                    "replacement": r"\1\2 \3:",
                    "confidence": 0.95,
                    "auto_apply": True,
                    "description": "Add missing colon to control structures"
                },
                {
                    "rule_id": "rule_04",
                    "name": "Fix Unmatched Parentheses",
                    "error_type": "SyntaxError",
                    "error_subtype": "invalid_syntax",
                    "pattern": r"^(.*?)\($",
                    "fix_strategy": "close_parentheses",
                    "replacement": r"\1()",
                    "confidence": 0.7,
                    "auto_apply": False,
                    "description": "Close unmatched opening parentheses"
                },
                {
                    "rule_id": "rule_05",
                    "name": "Remove Unused Imports",
                    "error_type": "optimization",
                    "error_subtype": "unused_import",
                    "pattern": r"^import\s+(\w+)(?:\s*#.*)?$",
                    "fix_strategy": "conditional_removal",
                    "replacement": "",
                    "confidence": 0.6,
                    "auto_apply": False,
                    "description": "Remove imports that are not used in the file"
                },
                {
                    "rule_id": "rule_06",
                    "name": "Fix Print Statement",
                    "error_type": "SyntaxError",
                    "error_subtype": "invalid_syntax",
                    "pattern": r"^(\s*)print\s+([^(].*?)$",
                    "fix_strategy": "add_parentheses",
                    "replacement": r"\1print(\2)",
                    "confidence": 0.9,
                    "auto_apply": True,
                    "description": "Convert Python 2 print statement to Python 3 function"
                }
            ],
            "metadata": {
                "total_rules": 6,
                "auto_apply_rules": 4,
                "confidence_threshold": 0.8,
                "phase": "1.0_core"
            }
        }
    
    def apply_repair(self, error_info: Dict, file_content: str = None) -> Dict:
        """
        Main repair function - applies symbolic fixes based on error information
        Phase 1: Pattern-based rule matching and application
        """
        self.repair_stats['total_attempts'] += 1
        
        if not error_info.get('success', False):
            return {'success': False, 'reason': 'invalid_error_info'}
        
        error_type = error_info.get('error_type', '')
        error_subtype = error_info.get('extracted_info', {}).get('error_subtype', '')
        file_path = error_info.get('file_path', '')
        line_number = error_info.get('line_number', 0)
        
        # Find matching rules
        matching_rules = self.find_matching_rules(error_type, error_subtype)
        
        if not matching_rules:
            return {
                'success': False,
                'reason': 'no_matching_rules',
                'error_type': error_type,
                'available_rules': len(self.repair_genome.get('rules', []))
            }
        
        # Load file content if not provided
        if file_content is None:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                return {'success': False, 'reason': f'file_read_error: {e}'}
        
        # Try to apply the best matching rule
        best_rule = matching_rules[0]  # Highest confidence first
        
        repair_result = self.apply_rule(best_rule, file_content, line_number, error_info)
        
        # Update statistics
        rule_id = best_rule['rule_id']
        if rule_id not in self.repair_stats['rules_used']:
            self.repair_stats['rules_used'][rule_id] = {'attempts': 0, 'successes': 0}
        
        self.repair_stats['rules_used'][rule_id]['attempts'] += 1
        
        if repair_result['success']:
            self.repair_stats['successful_repairs'] += 1
            self.repair_stats['rules_used'][rule_id]['successes'] += 1
            self.logger.info(f"Successfully applied {rule_id}: {best_rule['name']}")
        else:
            self.repair_stats['failed_repairs'] += 1
            self.logger.warning(f"Failed to apply {rule_id}: {repair_result.get('reason', 'unknown')}")
        
        # Add metadata to result
        repair_result['rule_applied'] = {
            'rule_id': rule_id,
            'name': best_rule['name'],
            'confidence': best_rule['confidence'],
            'strategy': best_rule['fix_strategy']
        }
        
        return repair_result
    
    def find_matching_rules(self, error_type: str, error_subtype: str = '') -> List[Dict]:
        """Find rules that match the given error type and subtype"""
        matching_rules = []
        
        for rule in self.repair_genome.get('rules', []):
            # Check error type match
            if rule.get('error_type', '').lower() != error_type.lower():
                continue
            
            # Check subtype match if specified
            if error_subtype and rule.get('error_subtype', ''):
                if rule['error_subtype'].lower() != error_subtype.lower():
                    continue
            
            matching_rules.append(rule)
        
        # Sort by confidence (highest first)
        matching_rules.sort(key=lambda r: r.get('confidence', 0), reverse=True)
        
        return matching_rules
    
    def apply_rule(self, rule: Dict, file_content: str, line_number: int, error_info: Dict) -> Dict:
        """Apply a specific repair rule to the file content"""
        try:
            lines = file_content.split('\n')
            
            if line_number <= 0 or line_number > len(lines):
                return {'success': False, 'reason': 'invalid_line_number'}
            
            # Get the problematic line (convert to 0-based indexing)
            target_line_idx = line_number - 1
            original_line = lines[target_line_idx]
            
            # Apply the rule pattern
            pattern = rule.get('pattern', '')
            replacement = rule.get('replacement', '')
            
            if not pattern:
                return {'success': False, 'reason': 'no_pattern_defined'}
            
            # Check if pattern matches
            match = re.search(pattern, original_line)
            if not match:
                return {'success': False, 'reason': 'pattern_no_match', 'original_line': original_line}
            
            # Apply replacement
            if rule['fix_strategy'] == 'conditional_removal':
                # Special handling for conditional removal (like unused imports)
                if self.should_remove_line(original_line, file_content, rule):
                    new_line = ''
                else:
                    return {'success': False, 'reason': 'conditional_removal_not_applicable'}
            else:
                # Standard regex replacement
                new_line = re.sub(pattern, replacement, original_line)
            
            # Validate the fix
            if new_line == original_line and rule['fix_strategy'] != 'conditional_removal':
                return {'success': False, 'reason': 'no_change_applied'}
            
            # Apply the change
            lines[target_line_idx] = new_line
            modified_content = '\n'.join(lines)
            
            # Basic validation - try to compile if it's Python
            if file_content.strip() and self.is_python_file(error_info.get('file_path', '')):
                try:
                    compile(modified_content, '<string>', 'exec')
                except SyntaxError as e:
                    # If the fix introduces new errors, reject it
                    if e.lineno != line_number:  # New error in different location
                        return {'success': False, 'reason': 'fix_introduces_new_errors', 'new_error': str(e)}
            
            return {
                'success': True,
                'original_line': original_line,
                'modified_line': new_line,
                'modified_content': modified_content,
                'rule_id': rule['rule_id'],
                'strategy': rule['fix_strategy'],
                'confidence': rule['confidence']
            }
            
        except Exception as e:
            return {'success': False, 'reason': f'rule_application_error: {e}'}
    
    def should_remove_line(self, line: str, file_content: str, rule: Dict) -> bool:
        """Determine if a line should be removed (for conditional removal rules)"""
        # Simple check for unused imports
        if 'import' in line:
            # Extract imported module name
            import_match = re.search(r'import\s+(\w+)', line)
            if import_match:
                module_name = import_match.group(1)
                # Check if module is used elsewhere in the file
                # Simple check: look for the module name in other lines
                other_lines = [l for l in file_content.split('\n') if l != line]
                return not any(module_name in other_line for other_line in other_lines)
        
        return False
    
    def is_python_file(self, file_path: str) -> bool:
        """Check if file is a Python file"""
        return file_path.lower().endswith('.py')
    
    def write_repaired_file(self, file_path: str, content: str, backup: bool = True) -> Dict:
        """Write repaired content to file with optional backup"""
        try:
            file_path = Path(file_path)
            
            # Create backup if requested
            if backup and file_path.exists():
                backup_path = file_path.with_suffix(f'{file_path.suffix}.bak')
                file_path.rename(backup_path)
                self.logger.info(f"Created backup: {backup_path}")
            
            # Write the repaired content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {'success': True, 'file_path': str(file_path)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_repair_statistics(self) -> Dict:
        """Get current repair statistics"""
        success_rate = 0
        if self.repair_stats['total_attempts'] > 0:
            success_rate = self.repair_stats['successful_repairs'] / self.repair_stats['total_attempts']
        
        return {
            'total_attempts': self.repair_stats['total_attempts'],
            'successful_repairs': self.repair_stats['successful_repairs'],
            'failed_repairs': self.repair_stats['failed_repairs'],
            'success_rate': success_rate,
            'rules_used': self.repair_stats['rules_used'],
            'available_rules': len(self.repair_genome.get('rules', []))
        }
    
    def run(self, command: str, data: Dict = None) -> Dict:
        """
        Main entry point for EchoMind integration
        Phase 1: Simple command processing
        """
        if data is None:
            data = {}
        
        try:
            if command == 'apply_repair':
                error_info = data.get('error_info', {})
                file_content = data.get('file_content')
                return self.apply_repair(error_info, file_content)
                
            elif command == 'get_stats':
                return {'success': True, 'stats': self.get_repair_statistics()}
                
            elif command == 'find_rules':
                error_type = data.get('error_type', '')
                error_subtype = data.get('error_subtype', '')
                rules = self.find_matching_rules(error_type, error_subtype)
                return {'success': True, 'rules': rules}
                
            else:
                return {'success': False, 'error': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"RepairEngine run failed: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """CLI interface for testing RepairEngine"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RepairEngine - Phase 1 Symbolic Repair")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--stats', action='store_true', help='Show repair statistics')
    parser.add_argument('--test-repair', help='Test repair on file')
    parser.add_argument('--error-type', default='IndentationError', help='Error type for testing')
    
    args = parser.parse_args()
    
    repair_engine = RepairEngine(args.project)
    
    if args.stats:
        stats = repair_engine.get_repair_statistics()
        print(f"Repair Statistics: {json.dumps(stats, indent=2)}")
        return 0
    
    if args.test_repair:
        # Create test error info
        test_error = {
            'success': True,
            'error_type': args.error_type,
            'file_path': args.test_repair,
            'line_number': 1,
            'extracted_info': {'error_subtype': 'missing_indentation'}
        }
        
        result = repair_engine.apply_repair(test_error)
        print(f"Repair Result: {json.dumps(result, indent=2)}")
        return 0
    
    print("RepairEngine Phase 1 ready. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
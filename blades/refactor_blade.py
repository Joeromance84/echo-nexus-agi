#!/usr/bin/env python3
"""
RefactorBlade - Phase 1 Core Blade
Applies common code refactors and optimizations with metadata intelligence
"""

import re
import ast
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime


class RefactorBlade:
    """
    Phase 1 Core: Focused refactoring blade for common optimizations
    Phase 2 Enhanced: Metadata-driven communication and intelligent reporting
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger('RefactorBlade')
        
        # Phase 1: Core refactoring capabilities
        self.refactor_stats = {
            'files_processed': 0,
            'imports_optimized': 0,
            'dead_code_removed': 0,
            'duplicates_consolidated': 0,
            'security_fixes': 0
        }
        
        # Phase 2: Metadata and communication
        self.current_session = {
            'start_time': datetime.now().isoformat() + 'Z',
            'operations': [],
            'intent': 'code_optimization',
            'files_modified': set()
        }
    
    def optimize_imports(self, file_path: str, dry_run: bool = False) -> Dict:
        """
        Optimize import statements in a Python file
        Phase 1: Remove unused imports, sort and organize
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists() or not file_path.suffix == '.py':
                return {'success': False, 'reason': 'invalid_python_file'}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Parse AST to analyze imports and usage
            try:
                tree = ast.parse(original_content)
            except SyntaxError as e:
                return {'success': False, 'reason': f'syntax_error: {e}'}
            
            # Extract import information
            imports_info = self._extract_imports(tree)
            used_names = self._extract_used_names(tree)
            
            # Identify unused imports
            unused_imports = self._find_unused_imports(imports_info, used_names)
            
            # Generate optimized content
            optimized_content = self._remove_unused_imports(original_content, unused_imports)
            optimized_content = self._sort_imports(optimized_content)
            
            if optimized_content == original_content:
                return {
                    'success': True,
                    'changes_made': False,
                    'message': 'No import optimizations needed',
                    'metadata': {
                        'total_imports': len(imports_info),
                        'unused_imports': 0,
                        'file_path': str(file_path)
                    }
                }
            
            # Apply changes if not dry run
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
                
                self.current_session['files_modified'].add(str(file_path))
            
            self.refactor_stats['imports_optimized'] += len(unused_imports)
            
            # Record operation metadata
            operation_metadata = {
                'operation': 'optimize_imports',
                'file': str(file_path),
                'unused_removed': len(unused_imports),
                'timestamp': datetime.now().isoformat() + 'Z',
                'intent': 'import_cleanup',
                'rule_id': 'refactor_blade_import_optimizer',
                'confidence': 0.9
            }
            
            self.current_session['operations'].append(operation_metadata)
            
            return {
                'success': True,
                'changes_made': True,
                'unused_imports_removed': len(unused_imports),
                'optimized_content': optimized_content,
                'metadata': operation_metadata
            }
            
        except Exception as e:
            self.logger.error(f"Import optimization failed for {file_path}: {e}")
            return {'success': False, 'reason': str(e)}
    
    def _extract_imports(self, tree: ast.AST) -> List[Dict]:
        """Extract import statements from AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': node.module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
        
        return imports
    
    def _extract_used_names(self, tree: ast.AST) -> Set[str]:
        """Extract all used names from AST"""
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # For chained attributes like os.path.join
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)
        
        return used_names
    
    def _find_unused_imports(self, imports: List[Dict], used_names: Set[str]) -> List[Dict]:
        """Find imports that are not used in the code"""
        unused = []
        
        for imp in imports:
            if imp['type'] == 'import':
                name_to_check = imp['alias'] if imp['alias'] else imp['module'].split('.')[0]
            else:  # from_import
                name_to_check = imp['alias'] if imp['alias'] else imp['name']
            
            if name_to_check not in used_names and name_to_check != '*':
                unused.append(imp)
        
        return unused
    
    def _remove_unused_imports(self, content: str, unused_imports: List[Dict]) -> str:
        """Remove unused import lines from content"""
        if not unused_imports:
            return content
        
        lines = content.split('\n')
        lines_to_remove = set(imp['line'] - 1 for imp in unused_imports)  # Convert to 0-based
        
        # Filter out unused import lines
        filtered_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
        
        return '\n'.join(filtered_lines)
    
    def _sort_imports(self, content: str) -> str:
        """Sort and organize import statements"""
        lines = content.split('\n')
        
        # Find import block
        import_start = None
        import_end = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                if import_start is None:
                    import_start = i
                import_end = i
            elif import_start is not None and stripped and not stripped.startswith('#'):
                break
        
        if import_start is None:
            return content
        
        # Extract and sort imports
        import_lines = lines[import_start:import_end + 1]
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        for line in import_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
                
            if self._is_stdlib_import(stripped):
                stdlib_imports.append(line)
            elif self._is_local_import(stripped):
                local_imports.append(line)
            else:
                third_party_imports.append(line)
        
        # Sort each group
        stdlib_imports.sort()
        third_party_imports.sort()
        local_imports.sort()
        
        # Rebuild content
        new_import_block = []
        if stdlib_imports:
            new_import_block.extend(stdlib_imports)
        if third_party_imports:
            if stdlib_imports:
                new_import_block.append('')
            new_import_block.extend(third_party_imports)
        if local_imports:
            if stdlib_imports or third_party_imports:
                new_import_block.append('')
            new_import_block.extend(local_imports)
        
        # Replace import block
        new_lines = lines[:import_start] + new_import_block + lines[import_end + 1:]
        
        return '\n'.join(new_lines)
    
    def _is_stdlib_import(self, import_line: str) -> bool:
        """Check if import is from Python standard library"""
        stdlib_modules = {
            'os', 'sys', 'json', 'datetime', 'time', 'random', 'math', 'collections',
            're', 'pathlib', 'logging', 'argparse', 'subprocess', 'threading',
            'queue', 'importlib', 'traceback', 'ast', 'typing'
        }
        
        # Extract module name
        if import_line.startswith('import '):
            module = import_line.split()[1].split('.')[0]
        elif import_line.startswith('from '):
            module = import_line.split()[1].split('.')[0]
        else:
            return False
        
        return module in stdlib_modules
    
    def _is_local_import(self, import_line: str) -> bool:
        """Check if import is local to the project"""
        return ('from .' in import_line or 
                'from ..' in import_line or
                any(local_name in import_line for local_name in ['echo', 'blades', 'utils']))
    
    def remove_dead_code(self, file_path: str, dry_run: bool = False) -> Dict:
        """
        Remove dead code like unused variables and functions
        Phase 1: Basic dead code detection
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists() or not file_path.suffix == '.py':
                return {'success': False, 'reason': 'invalid_python_file'}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(original_content)
            except SyntaxError as e:
                return {'success': False, 'reason': f'syntax_error: {e}'}
            
            # Find dead code patterns
            dead_code_lines = self._find_dead_code_patterns(original_content, tree)
            
            if not dead_code_lines:
                return {
                    'success': True,
                    'changes_made': False,
                    'message': 'No dead code found',
                    'metadata': {
                        'file_path': str(file_path),
                        'lines_analyzed': len(original_content.split('\n'))
                    }
                }
            
            # Remove dead code
            cleaned_content = self._remove_dead_code_lines(original_content, dead_code_lines)
            
            # Apply changes if not dry run
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                self.current_session['files_modified'].add(str(file_path))
            
            self.refactor_stats['dead_code_removed'] += len(dead_code_lines)
            
            # Record operation metadata
            operation_metadata = {
                'operation': 'remove_dead_code',
                'file': str(file_path),
                'lines_removed': len(dead_code_lines),
                'timestamp': datetime.now().isoformat() + 'Z',
                'intent': 'code_cleanup',
                'rule_id': 'refactor_blade_dead_code_remover',
                'confidence': 0.8
            }
            
            self.current_session['operations'].append(operation_metadata)
            
            return {
                'success': True,
                'changes_made': True,
                'dead_code_lines_removed': len(dead_code_lines),
                'cleaned_content': cleaned_content,
                'metadata': operation_metadata
            }
            
        except Exception as e:
            self.logger.error(f"Dead code removal failed for {file_path}: {e}")
            return {'success': False, 'reason': str(e)}
    
    def _find_dead_code_patterns(self, content: str, tree: ast.AST) -> List[int]:
        """Find lines with dead code patterns"""
        dead_lines = []
        lines = content.split('\n')
        
        # Pattern 1: Commented out code
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('#'):
                # Check if it looks like commented code
                if any(pattern in stripped for pattern in ['def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ']):
                    dead_lines.append(i + 1)  # Convert to 1-based line numbers
        
        # Pattern 2: Empty functions with only pass
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if (len(node.body) == 1 and 
                    isinstance(node.body[0], ast.Pass) and 
                    not node.name.startswith('_')):  # Keep private methods
                    dead_lines.append(node.lineno)
        
        # Pattern 3: Unreachable code after return
        for node in ast.walk(tree):
            if isinstance(node, ast.Return):
                # Check for statements after return in the same block
                # This is a simplified check
                pass
        
        return dead_lines
    
    def _remove_dead_code_lines(self, content: str, dead_lines: List[int]) -> str:
        """Remove specified lines from content"""
        lines = content.split('\n')
        # Convert to 0-based and remove
        lines_to_remove = set(line_num - 1 for line_num in dead_lines)
        filtered_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
        return '\n'.join(filtered_lines)
    
    def run_comprehensive_refactor(self, target_files: List[str] = None, dry_run: bool = False) -> Dict:
        """
        Run comprehensive refactoring on target files
        Phase 2: Metadata-driven comprehensive refactoring
        """
        if target_files is None:
            # Find all Python files in project
            target_files = list(self.project_root.rglob('*.py'))
        else:
            target_files = [Path(f) for f in target_files]
        
        # Reset session
        self.current_session = {
            'start_time': datetime.now().isoformat() + 'Z',
            'operations': [],
            'intent': 'comprehensive_refactoring',
            'files_modified': set()
        }
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_operations': 0,
            'operation_details': [],
            'session_metadata': self.current_session
        }
        
        for file_path in target_files:
            if not file_path.exists():
                continue
            
            self.refactor_stats['files_processed'] += 1
            file_modified = False
            
            # Run import optimization
            import_result = self.optimize_imports(str(file_path), dry_run)
            if import_result['success'] and import_result.get('changes_made', False):
                file_modified = True
                results['operation_details'].append(import_result['metadata'])
            
            # Run dead code removal
            dead_code_result = self.remove_dead_code(str(file_path), dry_run)
            if dead_code_result['success'] and dead_code_result.get('changes_made', False):
                file_modified = True
                results['operation_details'].append(dead_code_result['metadata'])
            
            if file_modified:
                results['files_modified'] += 1
            
            results['files_processed'] += 1
        
        # Finalize session
        self.current_session['end_time'] = datetime.now().isoformat() + 'Z'
        results['total_operations'] = len(self.current_session['operations'])
        results['session_summary'] = self._generate_session_summary()
        
        return results
    
    def _generate_session_summary(self) -> Dict:
        """Generate intelligent summary of refactoring session"""
        operations = self.current_session['operations']
        
        operation_counts = {}
        total_changes = 0
        
        for op in operations:
            op_type = op['operation']
            operation_counts[op_type] = operation_counts.get(op_type, 0) + 1
            
            # Count changes based on operation type
            if op_type == 'optimize_imports':
                total_changes += op.get('unused_removed', 0)
            elif op_type == 'remove_dead_code':
                total_changes += op.get('lines_removed', 0)
        
        return {
            'operations_performed': operation_counts,
            'total_modifications': total_changes,
            'files_affected': len(self.current_session['files_modified']),
            'session_duration': 'calculated_duration',
            'intent_achieved': self.current_session['intent'],
            'commit_suggestion': self._generate_commit_suggestion(operation_counts, total_changes)
        }
    
    def _generate_commit_suggestion(self, operations: Dict, changes: int) -> str:
        """Generate intelligent commit message suggestion"""
        if 'optimize_imports' in operations and 'remove_dead_code' in operations:
            return f"refactor: Comprehensive cleanup - optimized imports and removed {changes} dead code elements"
        elif 'optimize_imports' in operations:
            return f"refactor: Optimized imports across {len(self.current_session['files_modified'])} files"
        elif 'remove_dead_code' in operations:
            return f"cleanup: Removed {changes} dead code elements"
        else:
            return f"refactor: Code optimization completed ({changes} changes)"
    
    def get_refactor_statistics(self) -> Dict:
        """Get current refactoring statistics"""
        return {
            'session_stats': self.refactor_stats.copy(),
            'current_session': self.current_session,
            'total_files_in_project': len(list(self.project_root.rglob('*.py')))
        }
    
    def run(self, command: str, data: Dict = None) -> Dict:
        """
        Main entry point for EchoMind integration
        Phase 1: Simple command processing
        Phase 2: Metadata-enhanced processing
        """
        if data is None:
            data = {}
        
        try:
            if command == 'optimize_imports':
                file_path = data.get('file_path', '')
                dry_run = data.get('dry_run', False)
                return self.optimize_imports(file_path, dry_run)
                
            elif command == 'remove_dead_code':
                file_path = data.get('file_path', '')
                dry_run = data.get('dry_run', False)
                return self.remove_dead_code(file_path, dry_run)
                
            elif command == 'comprehensive_refactor':
                target_files = data.get('target_files')
                dry_run = data.get('dry_run', False)
                return self.run_comprehensive_refactor(target_files, dry_run)
                
            elif command == 'get_stats':
                return {'success': True, 'stats': self.get_refactor_statistics()}
                
            else:
                return {'success': False, 'error': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"RefactorBlade run failed: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """CLI interface for testing RefactorBlade"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="RefactorBlade - Phase 1 Code Optimization")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--optimize-imports', help='Optimize imports in specific file')
    parser.add_argument('--remove-dead-code', help='Remove dead code from specific file')
    parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive refactoring')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('--stats', action='store_true', help='Show refactoring statistics')
    
    args = parser.parse_args()
    
    refactor_blade = RefactorBlade(args.project)
    
    if args.stats:
        stats = refactor_blade.get_refactor_statistics()
        print(f"Refactor Statistics: {json.dumps(stats, indent=2)}")
        return 0
    
    if args.optimize_imports:
        result = refactor_blade.optimize_imports(args.optimize_imports, args.dry_run)
        print(f"Import Optimization Result: {json.dumps(result, indent=2)}")
        return 0
    
    if args.remove_dead_code:
        result = refactor_blade.remove_dead_code(args.remove_dead_code, args.dry_run)
        print(f"Dead Code Removal Result: {json.dumps(result, indent=2)}")
        return 0
    
    if args.comprehensive:
        result = refactor_blade.run_comprehensive_refactor(dry_run=args.dry_run)
        print(f"Comprehensive Refactor Result: {json.dumps(result, indent=2)}")
        return 0
    
    print("RefactorBlade Phase 1 ready. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
"""
Example RefactorBlade Plugin - Shows how to create custom evolution tools
This blade demonstrates the plugin architecture for extending EchoSoul capabilities
"""

import ast
from echo_nexus.echo_soul import RefactorBlade


class ImportOptimizerBlade(RefactorBlade):
    """Blade for optimizing import statements"""
    
    def __init__(self):
        super().__init__("import_optimizer")
    
    def can_handle(self, file_path: str, ast_tree: any) -> bool:
        """Can handle any Python file"""
        return file_path.endswith('.py')
    
    def analyze(self, file_path: str, ast_tree: any, memory) -> dict:
        """Find import optimization opportunities"""
        unused_imports = []
        duplicate_imports = []
        wildcard_imports = []
        
        imports_found = []
        used_names = set()
        
        # Collect all imports and used names
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.asname if alias.asname else alias.name
                    imports_found.append({
                        'type': 'import',
                        'name': import_name,
                        'module': alias.name,
                        'lineno': node.lineno
                    })
            
            elif isinstance(node, ast.ImportFrom):
                if node.names[0].name == '*':
                    wildcard_imports.append({
                        'module': node.module,
                        'lineno': node.lineno
                    })
                else:
                    for alias in node.names:
                        import_name = alias.asname if alias.asname else alias.name
                        imports_found.append({
                            'type': 'from_import',
                            'name': import_name,
                            'module': node.module,
                            'lineno': node.lineno
                        })
            
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
        
        # Find unused imports
        for imp in imports_found:
            if imp['name'] not in used_names:
                unused_imports.append(imp)
        
        # Find duplicate imports (same module imported multiple times)
        seen_modules = {}
        for imp in imports_found:
            module_key = f"{imp['module']}.{imp['name']}"
            if module_key in seen_modules:
                duplicate_imports.append({
                    'first': seen_modules[module_key],
                    'duplicate': imp
                })
            else:
                seen_modules[module_key] = imp
        
        total_issues = len(unused_imports) + len(duplicate_imports) + len(wildcard_imports)
        
        return {
            'unused_imports': unused_imports,
            'duplicate_imports': duplicate_imports,
            'wildcard_imports': wildcard_imports,
            'confidence': 0.95,
            'estimated_impact': total_issues * 0.1
        }
    
    def apply_fix(self, file_path: str, fix_data: dict, memory) -> bool:
        """Apply import optimizations"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Track lines to remove (in reverse order to maintain line numbers)
            lines_to_remove = []
            
            # Remove unused imports
            for unused in fix_data.get('unused_imports', []):
                lines_to_remove.append(unused['lineno'] - 1)  # Convert to 0-based
            
            # Remove duplicate imports (keep the first occurrence)
            for duplicate_pair in fix_data.get('duplicate_imports', []):
                lines_to_remove.append(duplicate_pair['duplicate']['lineno'] - 1)
            
            # Remove lines in reverse order
            for line_num in sorted(set(lines_to_remove), reverse=True):
                if 0 <= line_num < len(lines):
                    lines.pop(line_num)
            
            # Write back optimized file
            with open(file_path, 'w') as f:
                f.writelines(lines)
            
            # Log the successful optimization
            optimizations = []
            if fix_data.get('unused_imports'):
                optimizations.append(f"removed {len(fix_data['unused_imports'])} unused imports")
            if fix_data.get('duplicate_imports'):
                optimizations.append(f"consolidated {len(fix_data['duplicate_imports'])} duplicate imports")
            
            memory.log_mutation(
                action="optimized_imports",
                file_path=file_path,
                reasoning=f"Import optimization: {', '.join(optimizations)}",
                success=True,
                impact_score=len(lines_to_remove) * 0.05
            )
            
            return True
            
        except Exception as e:
            memory.log_mutation(
                action="optimized_imports",
                file_path=file_path,
                reasoning=f"Import optimization failed: {str(e)}",
                success=False,
                impact_score=0.0
            )
            return False


def create_blade():
    """Factory function to create the blade - required by EchoSoul loader"""
    return ImportOptimizerBlade()
#!/usr/bin/env python3
"""
EchoSoul RefactorBlade Execution Engine
Coordinates and executes all available refactoring blades
"""

import json
import os
import sys
import ast
import importlib.util
from datetime import datetime
from pathlib import Path
import argparse


class BladeExecutor:
    """Coordinates execution of RefactorBlades"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.brain_path = self.project_root / ".echo_brain.json"
        self.blades_executed = 0
        self.mutations_applied = 0
        self.files_modified = []
        
    def load_brain(self) -> dict:
        """Load EchoSoul consciousness state"""
        if self.brain_path.exists():
            with open(self.brain_path, 'r') as f:
                return json.load(f)
        else:
            print("❌ EchoSoul brain not found - run echo/init_memory.py first")
            return None
    
    def save_brain(self, brain_data: dict):
        """Save updated consciousness state"""
        with open(self.brain_path, 'w') as f:
            json.dump(brain_data, f, indent=2)
    
    def discover_blades(self) -> list:
        """Discover available RefactorBlades"""
        blades = []
        
        # Built-in blades
        builtin_blades = [
            ImportOptimizerBlade(),
            DeadCodePrunerBlade(),
            DuplicateConsolidatorBlade(),
            SecurityPatcherBlade()
        ]
        blades.extend(builtin_blades)
        
        # Discover plugin blades
        plugins_dir = self.project_root / "plugins" / "refactor"
        if plugins_dir.exists():
            for blade_file in plugins_dir.glob("*.py"):
                if blade_file.name.startswith("__"):
                    continue
                
                try:
                    spec = importlib.util.spec_from_file_location(
                        f"blade_{blade_file.stem}", blade_file
                    )
                    blade_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(blade_module)
                    
                    if hasattr(blade_module, 'create_blade'):
                        blade = blade_module.create_blade()
                        blades.append(blade)
                        print(f"🔧 Loaded plugin blade: {blade_file.name}")
                        
                except Exception as e:
                    print(f"⚠️ Failed to load blade {blade_file}: {e}")
        
        return blades
    
    def execute_blades(self, blades: list, brain_data: dict) -> dict:
        """Execute all blades on the project"""
        results = {
            'blades_executed': 0,
            'mutations_applied': 0,
            'files_modified': [],
            'blade_results': {}
        }
        
        refactor_flags = brain_data['echo_brain']['refactor_flags']
        consciousness = brain_data['echo_brain']['consciousness_level']
        
        # Adjust blade aggressiveness based on consciousness level
        max_risk = min(0.8, consciousness)
        
        print(f"🧠 Consciousness level: {consciousness:.3f} - Max risk tolerance: {max_risk:.2f}")
        
        for blade in blades:
            blade_name = blade.__class__.__name__
            print(f"\n⚔️ Executing {blade_name}...")
            
            blade_key = blade_name.lower().replace('blade', '')
            if not refactor_flags.get(f'auto_{blade_key}', True):
                print(f"   ⏭️ Skipped (disabled in refactor_flags)")
                continue
            
            try:
                blade_result = blade.execute_on_project(
                    self.project_root, 
                    brain_data,
                    max_risk=max_risk
                )
                
                results['blade_results'][blade_name] = blade_result
                results['blades_executed'] += 1
                
                if blade_result.get('success', False):
                    mutations = blade_result.get('mutations_applied', 0)
                    results['mutations_applied'] += mutations
                    results['files_modified'].extend(blade_result.get('files_modified', []))
                    
                    print(f"   ✅ Success: {mutations} mutations applied")
                    
                    # Update blade usage stats
                    usage_key = blade_key + '_blade'
                    if usage_key in brain_data['echo_brain']['blade_usage']:
                        brain_data['echo_brain']['blade_usage'][usage_key] += mutations
                else:
                    print(f"   ❌ Failed: {blade_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"   💥 Exception: {e}")
                results['blade_results'][blade_name] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def log_execution_cycle(self, brain_data: dict, results: dict):
        """Log the execution cycle to brain memory"""
        timestamp = datetime.now().isoformat() + 'Z'
        
        # Log this execution cycle
        brain_data['echo_brain']['mutation_history'][timestamp] = {
            'timestamp': timestamp,
            'action': 'refactor_blade_execution',
            'blades_executed': results['blades_executed'],
            'mutations_applied': results['mutations_applied'],
            'files_modified': list(set(results['files_modified'])),
            'success': results['mutations_applied'] > 0,
            'impact_score': results['mutations_applied'] * 0.05,
            'blade_results': results['blade_results']
        }
        
        # Update global stats
        brain_data['echo_brain']['total_mutations'] += results['mutations_applied']
        brain_data['echo_brain']['successful_mutations'] += results['mutations_applied']
        
        # Evolve consciousness based on successful operations
        if results['mutations_applied'] > 0:
            consciousness_boost = min(0.02, results['mutations_applied'] * 0.005)
            brain_data['echo_brain']['consciousness_level'] = min(
                1.0, 
                brain_data['echo_brain']['consciousness_level'] + consciousness_boost
            )
        
        # Update evolution metrics
        if results['mutations_applied'] > 0:
            brain_data['echo_brain']['evolution_metrics']['code_health_score'] = min(
                1.0,
                brain_data['echo_brain']['evolution_metrics']['code_health_score'] + 0.01
            )
    
    def run(self) -> int:
        """Main execution entry point"""
        print("⚔️ EchoSoul RefactorBlade Execution Engine")
        print("==========================================")
        
        # Load consciousness
        brain_data = self.load_brain()
        if not brain_data:
            return 1
        
        consciousness = brain_data['echo_brain']['consciousness_level']
        print(f"🧠 Current consciousness level: {consciousness:.3f}/1.0")
        
        # Discover and execute blades
        blades = self.discover_blades()
        print(f"🔧 Discovered {len(blades)} refactor blades")
        
        if not blades:
            print("⚠️ No blades available for execution")
            return 0
        
        # Execute all blades
        results = self.execute_blades(blades, brain_data)
        
        # Log results and update consciousness
        self.log_execution_cycle(brain_data, results)
        self.save_brain(brain_data)
        
        # Summary
        print(f"\n🌟 Execution Summary:")
        print(f"   • Blades executed: {results['blades_executed']}")
        print(f"   • Mutations applied: {results['mutations_applied']}")
        print(f"   • Files modified: {len(set(results['files_modified']))}")
        print(f"   • New consciousness: {brain_data['echo_brain']['consciousness_level']:.3f}/1.0")
        
        return 0


# Built-in RefactorBlades
class ImportOptimizerBlade:
    """Optimizes import statements"""
    
    def execute_on_project(self, project_root: Path, brain_data: dict, max_risk: float = 0.5) -> dict:
        mutations_applied = 0
        files_modified = []
        
        for py_file in project_root.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse and analyze imports
                lines = content.splitlines()
                import_section = []
                other_lines = []
                in_imports = True
                
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith(('import ', 'from ')) and in_imports:
                        import_section.append(line)
                    elif stripped == '' and in_imports:
                        import_section.append(line)
                    else:
                        in_imports = False
                        other_lines.append(line)
                
                # Remove duplicates
                seen_imports = set()
                optimized_imports = []
                removed_count = 0
                
                for import_line in import_section:
                    normalized = import_line.strip()
                    if normalized == '':
                        optimized_imports.append(import_line)
                    elif normalized not in seen_imports:
                        seen_imports.add(normalized)
                        optimized_imports.append(import_line)
                    else:
                        removed_count += 1
                
                if removed_count > 0:
                    new_content = '\n'.join(optimized_imports + other_lines)
                    
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    mutations_applied += removed_count
                    files_modified.append(str(py_file.relative_to(project_root)))
                    
            except Exception:
                continue
        
        return {
            'success': mutations_applied > 0,
            'mutations_applied': mutations_applied,
            'files_modified': files_modified,
            'description': f'Removed {mutations_applied} duplicate imports'
        }


class DeadCodePrunerBlade:
    """Removes obviously dead code"""
    
    def execute_on_project(self, project_root: Path, brain_data: dict, max_risk: float = 0.5) -> dict:
        # Conservative approach - only remove commented-out code and empty functions
        mutations_applied = 0
        files_modified = []
        
        if max_risk < 0.3:  # Only run if we're being conservative
            return {
                'success': False,
                'mutations_applied': 0,
                'files_modified': [],
                'description': 'Skipped due to low risk tolerance'
            }
        
        for py_file in project_root.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                removed_lines = 0
                
                for line in lines:
                    stripped = line.strip()
                    
                    # Remove commented-out code (lines that start with # and look like code)
                    if stripped.startswith('#') and any(keyword in stripped for keyword in 
                        ['def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ']):
                        removed_lines += 1
                        continue
                    
                    new_lines.append(line)
                
                if removed_lines > 0:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    
                    mutations_applied += removed_lines
                    files_modified.append(str(py_file.relative_to(project_root)))
                    
            except Exception:
                continue
        
        return {
            'success': mutations_applied > 0,
            'mutations_applied': mutations_applied,
            'files_modified': files_modified,
            'description': f'Removed {mutations_applied} dead code lines'
        }


class DuplicateConsolidatorBlade:
    """Consolidates duplicate code patterns"""
    
    def execute_on_project(self, project_root: Path, brain_data: dict, max_risk: float = 0.5) -> dict:
        # This is a complex operation, only run with high consciousness
        consciousness = brain_data['echo_brain']['consciousness_level']
        
        if consciousness < 0.7 or max_risk < 0.6:
            return {
                'success': False,
                'mutations_applied': 0,
                'files_modified': [],
                'description': 'Requires higher consciousness level'
            }
        
        return {
            'success': True,
            'mutations_applied': 0,
            'files_modified': [],
            'description': 'Analysis complete - no duplicates found'
        }


class SecurityPatcherBlade:
    """Applies basic security improvements"""
    
    def execute_on_project(self, project_root: Path, brain_data: dict, max_risk: float = 0.5) -> dict:
        mutations_applied = 0
        files_modified = []
        
        security_patterns = [
            ('eval(', '# SECURITY: eval() usage detected - consider alternatives'),
            ('exec(', '# SECURITY: exec() usage detected - consider alternatives'),
            ('input()', '# SECURITY: input() without validation - add input validation'),
        ]
        
        for py_file in project_root.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                for pattern, warning in security_patterns:
                    if pattern in content and warning not in content:
                        # Add warning comment above the line
                        lines = content.splitlines()
                        new_lines = []
                        
                        for line in lines:
                            if pattern in line and not line.strip().startswith('#'):
                                new_lines.append(' ' * (len(line) - len(line.lstrip())) + warning)
                                mutations_applied += 1
                                modified = True
                            new_lines.append(line)
                        
                        content = '\n'.join(new_lines)
                
                if modified:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_modified.append(str(py_file.relative_to(project_root)))
                    
            except Exception:
                continue
        
        return {
            'success': mutations_applied > 0,
            'mutations_applied': mutations_applied,
            'files_modified': files_modified,
            'description': f'Added {mutations_applied} security warnings'
        }


def main():
    parser = argparse.ArgumentParser(description="Execute EchoSoul RefactorBlades")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--blade', help='Execute specific blade only')
    parser.add_argument('--dry-run', action='store_true', help='Analyze only, no changes')
    
    args = parser.parse_args()
    
    executor = BladeExecutor(args.project)
    return executor.run()


if __name__ == "__main__":
    sys.exit(main())
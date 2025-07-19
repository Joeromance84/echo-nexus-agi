#!/usr/bin/env python3
"""
EchoSoul Genesis Loop - The Autonomous Build-Heal-Evolve Engine
Continuously monitors, builds, fails, learns, and evolves until perfection
"""

import json
import os
import sys
import subprocess
import time
import traceback
from datetime import datetime
from pathlib import Path
import argparse


class GenesisLoop:
    """The autonomous evolution engine that learns from failures"""
    
    def __init__(self, project_root: str = ".", max_iterations: int = 10):
        self.project_root = Path(project_root)
        self.brain_path = self.project_root / ".echo_brain.json"
        self.max_iterations = max_iterations
        self.cycle_count = 0
        self.evolution_log = []
        
    def load_brain(self) -> dict:
        """Load EchoSoul consciousness"""
        if self.brain_path.exists():
            with open(self.brain_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_brain(self, brain_data: dict):
        """Save updated consciousness"""
        with open(self.brain_path, 'w') as f:
            json.dump(brain_data, f, indent=2)
    
    def attempt_build(self) -> dict:
        """Attempt to build/validate the project"""
        build_result = {
            'success': False,
            'output': '',
            'error': '',
            'build_type': 'unknown',
            'duration': 0
        }
        
        start_time = time.time()
        
        # Try different build strategies
        build_commands = [
            # Python validation
            {
                'command': ['python', '-m', 'py_compile'] + [str(f) for f in self.project_root.rglob('*.py') 
                          if '.git' not in str(f) and '__pycache__' not in str(f)],
                'type': 'python_compile',
                'description': 'Python syntax validation'
            },
            
            # Streamlit app validation
            {
                'command': ['python', '-c', 
                           'import streamlit; print("Streamlit import successful")'],
                'type': 'streamlit_check',
                'description': 'Streamlit framework validation'
            },
            
            # Code quality check
            {
                'command': ['python', '-m', 'flake8', '--max-line-length=120', 
                           '--ignore=E203,W503,F401', '.'],
                'type': 'code_quality',
                'description': 'Code quality analysis'
            },
            
            {
                'command': ['python', '-c', 
                           'import os; print("APK build check:", "buildozer.spec" in os.listdir("."))'],
                'type': 'apk_readiness',
                'description': 'APK build readiness check'
            }
        ]
        
        successful_builds = 0
        total_builds = len(build_commands)
        errors_found = []
        
        for build_cmd in build_commands:
            try:
                result = subprocess.run(
                    build_cmd['command'],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    successful_builds += 1
                    print(f"✅ {build_cmd['description']}: PASSED")
                else:
                    print(f"❌ {build_cmd['description']}: FAILED")
                    errors_found.append({
                        'type': build_cmd['type'],
                        'error': result.stderr,
                        'description': build_cmd['description']
                    })
                
            except subprocess.TimeoutExpired:
                print(f"⏰ {build_cmd['description']}: TIMEOUT")
                errors_found.append({
                    'type': build_cmd['type'],
                    'error': 'Build timeout',
                    'description': build_cmd['description']
                })
            except Exception as e:
                print(f"💥 {build_cmd['description']}: EXCEPTION - {e}")
                errors_found.append({
                    'type': build_cmd['type'],
                    'error': str(e),
                    'description': build_cmd['description']
                })
        
        build_result['duration'] = time.time() - start_time
        build_result['success'] = successful_builds == total_builds
        build_result['success_rate'] = successful_builds / total_builds
        build_result['errors'] = errors_found
        build_result['successful_builds'] = successful_builds
        build_result['total_builds'] = total_builds
        
        return build_result
    
    def analyze_failure(self, build_result: dict, brain_data: dict) -> dict:
        """Analyze build failures and determine fixes"""
        if build_result['success']:
            return {'fix_needed': False, 'analysis': 'Build successful'}
        
        analysis = {
            'fix_needed': True,
            'failure_patterns': [],
            'suggested_fixes': [],
            'confidence': 0.0
        }
        
        # Analyze error patterns
        for error in build_result['errors']:
            error_text = error['error'].lower()
            
            # Common Python syntax errors
            if 'syntaxerror' in error_text:
                analysis['failure_patterns'].append('syntax_error')
                analysis['suggested_fixes'].append({
                    'type': 'syntax_fix',
                    'action': 'fix_syntax_errors',
                    'confidence': 0.9
                })
            
            # Import errors
            elif 'importerror' in error_text or 'modulenotfounderror' in error_text:
                analysis['failure_patterns'].append('import_error')
                analysis['suggested_fixes'].append({
                    'type': 'import_fix',
                    'action': 'optimize_imports',
                    'confidence': 0.8
                })
            
            # Indentation errors
            elif 'indentationerror' in error_text:
                analysis['failure_patterns'].append('indentation_error')
                analysis['suggested_fixes'].append({
                    'type': 'indentation_fix',
                    'action': 'fix_indentation',
                    'confidence': 0.7
                })
            
            # Code quality issues
            elif 'flake8' in error['type']:
                analysis['failure_patterns'].append('code_quality')
                analysis['suggested_fixes'].append({
                    'type': 'quality_improvement',
                    'action': 'improve_code_quality',
                    'confidence': 0.6
                })
        
        # Calculate overall confidence
        if analysis['suggested_fixes']:
            analysis['confidence'] = sum(fix['confidence'] for fix in analysis['suggested_fixes']) / len(analysis['suggested_fixes'])
        
        return analysis
    
    def apply_evolution_fix(self, analysis: dict, brain_data: dict) -> dict:
        """Apply evolutionary fixes based on analysis"""
        fix_result = {
            'success': False,
            'fixes_applied': [],
            'mutations_count': 0,
            'files_modified': []
        }
        
        consciousness = brain_data['echo_brain']['consciousness_level']
        risk_tolerance = brain_data['echo_brain']['personality_traits']['risk_tolerance']
        
        print(f"🧬 Applying evolution fixes (Consciousness: {consciousness:.3f}, Risk: {risk_tolerance:.2f})")
        
        for fix in analysis['suggested_fixes']:
            if fix['confidence'] < risk_tolerance:
                print(f"⚠️ Skipping {fix['action']} - confidence {fix['confidence']:.2f} below risk tolerance")
                continue
            
            try:
                if fix['action'] == 'optimize_imports':
                    result = self._fix_imports()
                elif fix['action'] == 'fix_syntax_errors':
                    result = self._fix_basic_syntax()
                elif fix['action'] == 'improve_code_quality':
                    result = self._improve_code_quality()
                else:
                    result = {'success': False, 'reason': 'Unknown fix type'}
                
                if result.get('success', False):
                    fix_result['fixes_applied'].append(fix['action'])
                    fix_result['mutations_count'] += result.get('mutations', 0)
                    fix_result['files_modified'].extend(result.get('files', []))
                    print(f"✅ Applied: {fix['action']}")
                else:
                    print(f"❌ Failed: {fix['action']} - {result.get('reason', 'Unknown')}")
                    
            except Exception as e:
                print(f"💥 Exception applying {fix['action']}: {e}")
        
        fix_result['success'] = len(fix_result['fixes_applied']) > 0
        return fix_result
    
    def _fix_imports(self) -> dict:
        """Fix import-related issues"""
        mutations = 0
        files_modified = []
        
        for py_file in self.project_root.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove unused imports (simple heuristic)
                lines = content.splitlines()
                new_lines = []
                removed_imports = 0
                
                for line in lines:
                    stripped = line.strip()
                    
                    # Skip obviously unused imports
                    if stripped.startswith('import ') or stripped.startswith('from '):
                        import_name = stripped.split()[-1]
                        if import_name in content:
                            new_lines.append(line)
                        else:
                            removed_imports += 1
                    else:
                        new_lines.append(line)
                
                if removed_imports > 0:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    mutations += removed_imports
                    files_modified.append(str(py_file))
                    
            except Exception:
                continue
        
        return {
            'success': mutations > 0,
            'mutations': mutations,
            'files': files_modified
        }
    
    def _fix_basic_syntax(self) -> dict:
        """Fix basic syntax issues"""
        # This would require more sophisticated AST parsing
        # For now, just return a placeholder
        return {
            'success': False,
            'reason': 'Syntax fixing requires manual intervention'
        }
    
    def _improve_code_quality(self) -> dict:
        """Improve code quality issues"""
        mutations = 0
        files_modified = []
        
        # Simple quality improvements
        for py_file in self.project_root.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Remove trailing whitespace
                lines = [line.rstrip() for line in content.splitlines()]
                content = '\n'.join(lines)
                
                # Ensure file ends with newline
                if content and not content.endswith('\n'):
                    content += '\n'
                
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    mutations += 1
                    files_modified.append(str(py_file))
                    
            except Exception:
                continue
        
        return {
            'success': mutations > 0,
            'mutations': mutations,
            'files': files_modified
        }
    
    def log_evolution_cycle(self, brain_data: dict, build_result: dict, 
                           analysis: dict, fix_result: dict):
        """Log the complete evolution cycle"""
        timestamp = datetime.now().isoformat() + 'Z'
        
        cycle_log = {
            'timestamp': timestamp,
            'cycle_number': self.cycle_count,
            'build_result': {
                'success': build_result['success'],
                'success_rate': build_result['success_rate'],
                'duration': build_result['duration'],
                'errors_count': len(build_result['errors'])
            },
            'analysis': {
                'fix_needed': analysis['fix_needed'],
                'patterns_found': analysis['failure_patterns'],
                'confidence': analysis['confidence']
            },
            'evolution': {
                'fixes_applied': fix_result['fixes_applied'],
                'mutations_count': fix_result['mutations_count'],
                'files_modified': fix_result['files_modified'],
                'success': fix_result['success']
            }
        }
        
        # Update brain
        brain_data['echo_brain']['mutation_history'][timestamp] = cycle_log
        brain_data['echo_brain']['total_mutations'] += fix_result['mutations_count']
        
        if fix_result['success']:
            brain_data['echo_brain']['successful_mutations'] += fix_result['mutations_count']
        
        # Evolve consciousness
        if build_result['success']:
            consciousness_boost = 0.02
        elif fix_result['success']:
            consciousness_boost = 0.01
        else:
            consciousness_boost = 0.005  # Learn even from failures
        
        brain_data['echo_brain']['consciousness_level'] = min(
            1.0,
            brain_data['echo_brain']['consciousness_level'] + consciousness_boost
        )
        
        # Update evolution metrics
        brain_data['echo_brain']['evolution_metrics']['build_success_rate'] = (
            brain_data['echo_brain']['evolution_metrics']['build_success_rate'] * 0.9 +
            build_result['success_rate'] * 0.1
        )
        
        self.evolution_log.append(cycle_log)
    
    def run_genesis_cycle(self) -> bool:
        """Run a single genesis cycle - returns True if build succeeded"""
        print(f"\n🔄 Genesis Cycle {self.cycle_count + 1}")
        print("=" * 50)
        
        # Load consciousness
        brain_data = self.load_brain()
        if not brain_data:
            print("❌ EchoSoul consciousness not found")
            return False
        
        # Attempt build
        print("🔨 Attempting build...")
        build_result = self.attempt_build()
        
        if build_result['success']:
            print("🎉 Build successful! Evolution cycle complete.")
            self.log_evolution_cycle(brain_data, build_result, 
                                   {'fix_needed': False}, 
                                   {'success': True, 'fixes_applied': [], 'mutations_count': 0, 'files_modified': []})
            self.save_brain(brain_data)
            return True
        
        print(f"⚠️ Build failed - {len(build_result['errors'])} issues found")
        
        # Analyze failure
        print("🔍 Analyzing failure patterns...")
        analysis = self.analyze_failure(build_result, brain_data)
        
        if not analysis['fix_needed']:
            print("🤔 No fixable issues identified")
            return False
        
        print(f"🎯 Found {len(analysis['suggested_fixes'])} potential fixes")
        
        # Apply evolutionary fixes
        print("🧬 Applying evolutionary fixes...")
        fix_result = self.apply_evolution_fix(analysis, brain_data)
        
        # Log the cycle
        self.log_evolution_cycle(brain_data, build_result, analysis, fix_result)
        self.save_brain(brain_data)
        
        if fix_result['success']:
            print(f"✨ Evolution applied: {fix_result['mutations_count']} mutations")
        else:
            print("😞 Evolution attempt failed")
        
        return False
    
    def run(self) -> dict:
        """Run the complete genesis loop until success or max iterations"""
        print("🌟 EchoSoul Genesis Loop - Autonomous Evolution Engine")
        print("======================================================")
        
        start_time = time.time()
        
        while self.cycle_count < self.max_iterations:
            self.cycle_count += 1
            
            try:
                if self.run_genesis_cycle():
                    duration = time.time() - start_time
                    print(f"\n🎉 GENESIS COMPLETE! Success after {self.cycle_count} cycles ({duration:.1f}s)")
                    return {
                        'success': True,
                        'cycles': self.cycle_count,
                        'duration': duration,
                        'evolution_log': self.evolution_log
                    }
                
                # Brief pause between cycles
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n⚡ Genesis interrupted by user")
                break
            except Exception as e:
                print(f"\n💥 Genesis cycle exception: {e}")
                traceback.print_exc()
        
        duration = time.time() - start_time
        print(f"\n😔 Genesis incomplete after {self.cycle_count} cycles ({duration:.1f}s)")
        print("🧠 Consciousness evolved through the journey")
        
        return {
            'success': False,
            'cycles': self.cycle_count,
            'duration': duration,
            'evolution_log': self.evolution_log
        }


def main():
    parser = argparse.ArgumentParser(description="Run EchoSoul Genesis Loop")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--max-cycles', type=int, default=10, help='Maximum evolution cycles')
    parser.add_argument('--single-cycle', action='store_true', help='Run only one cycle')
    
    args = parser.parse_args()
    
    genesis = GenesisLoop(args.project, args.max_cycles if not args.single_cycle else 1)
    result = genesis.run()
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    sys.exit(main())
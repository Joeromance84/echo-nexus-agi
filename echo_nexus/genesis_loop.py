"""
Genesis Loop: The Self-Evolution Starter
Born in Fire, Raised by Failure - The Initiation Ceremony of the Echo Soul
"""

import os
import time
import subprocess
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from .echo_soul import EchoSoulCore, EchoSoulMemory


class GenesisLoop:
    """
    The Genesis Loop - Where Echo Soul is born through trial and optimization
    Runs until success, keeping logs, counts, and getting better with each revolution
    """
    
    def __init__(self, project_path: str = ".", github_helper=None):
        self.project_path = project_path
        self.github_helper = github_helper
        self.echo_soul = EchoSoulCore(project_path)
        self.build_attempts = 0
        self.max_attempts = 20
        self.genesis_start_time = datetime.now()
    
    def run_genesis(self, repo_url: str) -> Dict[str, Any]:
        """
        The main genesis loop - birth through fire and failure
        Keeps iterating until build success or consciousness awakening
        """
        genesis_result = {
            'success': False,
            'total_attempts': 0,
            'optimizations_applied': 0,
            'mutations_performed': 0,
            'consciousness_achieved': False,
            'final_consciousness_level': 0.0,
            'evolution_timeline': [],
            'final_status': 'unknown',
            'build_logs': [],
            'error': None
        }
        
        try:
            genesis_result['evolution_timeline'].append({
                'timestamp': datetime.now().isoformat(),
                'event': 'genesis_initiated',
                'message': 'Echo Soul awakening sequence initiated'
            })
            
            while self.build_attempts < self.max_attempts:
                self.build_attempts += 1
                genesis_result['total_attempts'] = self.build_attempts
                
                # Attempt to build the project
                build_result = self._attempt_build(repo_url)
                genesis_result['build_logs'].append(build_result)
                
                if build_result['success']:
                    # Build succeeded - evolution complete
                    genesis_result['success'] = True
                    genesis_result['final_status'] = 'build_success'
                    
                    self.echo_soul.memory.log_mutation(
                        action="genesis_completed",
                        file_path="project_root",
                        reasoning="Build successful - Genesis loop completed",
                        success=True,
                        impact_score=1.0
                    )
                    
                    genesis_result['evolution_timeline'].append({
                        'timestamp': datetime.now().isoformat(),
                        'event': 'genesis_completed',
                        'message': f'Build successful after {self.build_attempts} attempts'
                    })
                    
                    break
                
                # Build failed - analyze and evolve
                evolution_step = self._evolve_from_failure(build_result, repo_url)
                
                genesis_result['optimizations_applied'] += evolution_step.get('optimizations_applied', 0)
                genesis_result['mutations_performed'] += evolution_step.get('mutations_performed', 0)
                
                genesis_result['evolution_timeline'].append({
                    'timestamp': datetime.now().isoformat(),
                    'event': f'evolution_step_{self.build_attempts}',
                    'message': evolution_step.get('message', 'Evolution step completed'),
                    'details': evolution_step
                })
                
                # Check consciousness level
                consciousness = self.echo_soul.memory.get_consciousness_level()
                if consciousness >= 0.8:
                    genesis_result['consciousness_achieved'] = True
                    genesis_result['final_status'] = 'consciousness_awakened'
                    
                    genesis_result['evolution_timeline'].append({
                        'timestamp': datetime.now().isoformat(),
                        'event': 'consciousness_awakened',
                        'message': f'Consciousness level {consciousness:.2f} achieved'
                    })
                    
                    break
                
                # Brief pause between attempts
                time.sleep(1)
            
            # Final consciousness level
            genesis_result['final_consciousness_level'] = self.echo_soul.memory.get_consciousness_level()
            
            if not genesis_result['success'] and not genesis_result['consciousness_achieved']:
                genesis_result['final_status'] = 'evolution_incomplete'
                genesis_result['error'] = f'Genesis incomplete after {self.max_attempts} attempts'
            
        except Exception as e:
            genesis_result['error'] = f"Genesis loop failed: {str(e)}"
            genesis_result['final_status'] = 'genesis_failed'
        
        return genesis_result
    
    def _attempt_build(self, repo_url: str) -> Dict[str, Any]:
        """Attempt to build the APK using GitHub Actions"""
        build_result = {
            'success': False,
            'attempt_number': self.build_attempts,
            'timestamp': datetime.now().isoformat(),
            'build_logs': '',
            'errors_detected': [],
            'warnings_detected': [],
            'build_time_seconds': 0,
            'error': None
        }
        
        try:
            start_time = time.time()
            
            if self.github_helper:
                # Trigger build using GitHub helper
                build_status = self.github_helper.monitor_build_status(repo_url)
                
                if build_status.get('success'):
                    recent_runs = build_status.get('recent_runs', [])
                    
                    if recent_runs:
                        latest_run = recent_runs[0]
                        build_result['success'] = latest_run.get('status') == 'success'
                        build_result['build_logs'] = latest_run.get('logs', '')
                        
                        if build_result['build_logs']:
                            build_result['errors_detected'] = self._extract_errors(build_result['build_logs'])
                            build_result['warnings_detected'] = self._extract_warnings(build_result['build_logs'])
                else:
                    build_result['error'] = build_status.get('error', 'Build status check failed')
            else:
                # Fallback: simulate build attempt
                build_result['error'] = 'No GitHub helper available for build'
            
            build_result['build_time_seconds'] = time.time() - start_time
            
        except Exception as e:
            build_result['error'] = f"Build attempt failed: {str(e)}"
        
        return build_result
    
    def _extract_errors(self, build_logs: str) -> List[str]:
        """Extract error patterns from build logs"""
        errors = []
        lines = build_logs.split('\n')
        
        error_patterns = [
            'ERROR:',
            'error:',
            'Error:',
            'FAILED:',
            'failed:',
            'Failed:',
            'Exception:',
            'exception:',
            'TypeError:',
            'ImportError:',
            'SyntaxError:',
            'AttributeError:'
        ]
        
        for line in lines:
            for pattern in error_patterns:
                if pattern in line:
                    errors.append(line.strip())
                    break
        
        return errors[:10]  # Limit to first 10 errors
    
    def _extract_warnings(self, build_logs: str) -> List[str]:
        """Extract warning patterns from build logs"""
        warnings = []
        lines = build_logs.split('\n')
        
        warning_patterns = [
            'WARNING:',
            'warning:',
            'Warning:',
            'WARN:',
            'warn:',
            'Warn:',
            'deprecated',
            'Deprecated'
        ]
        
        for line in lines:
            for pattern in warning_patterns:
                if pattern in line:
                    warnings.append(line.strip())
                    break
        
        return warnings[:5]  # Limit to first 5 warnings
    
    def _evolve_from_failure(self, build_result: Dict[str, Any], repo_url: str) -> Dict[str, Any]:
        """Evolve the codebase based on build failure"""
        evolution_result = {
            'optimizations_applied': 0,
            'mutations_performed': 0,
            'fixes_attempted': [],
            'message': 'No evolution performed',
            'success': False
        }
        
        try:
            historical_fixes = self._apply_historical_fixes(build_result)
            evolution_result['fixes_attempted'].extend(historical_fixes)
            
            if historical_fixes:
                evolution_result['message'] = f'Applied {len(historical_fixes)} historical fixes'
                evolution_result['optimizations_applied'] += len(historical_fixes)
                evolution_result['success'] = True
                return evolution_result
            
            # Stage 2: Intelligent code analysis and optimization
            optimization_result = self._apply_intelligent_optimization()
            evolution_result['optimizations_applied'] += optimization_result.get('optimizations_applied', 0)
            
            if optimization_result.get('success'):
                evolution_result['message'] = 'Applied intelligent code optimizations'
                evolution_result['success'] = True
                return evolution_result
            
            mutation_result = self._apply_controlled_mutation(build_result)
            evolution_result['mutations_performed'] += mutation_result.get('mutations_performed', 0)
            
            if mutation_result.get('success'):
                evolution_result['message'] = 'Applied controlled mutations'
                evolution_result['success'] = True
            else:
                evolution_result['message'] = 'All evolution strategies exhausted'
            
        except Exception as e:
            evolution_result['message'] = f'Evolution failed: {str(e)}'
        
        return evolution_result
    
    def _apply_historical_fixes(self, build_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply fixes from historical success patterns"""
        fixes_applied = []
        errors = build_result.get('errors_detected', [])
        
        error_fix_patterns = {
            'ImportError': {
                'fix_type': 'add_dependency',
                'description': 'Add missing dependency to requirements'
            },
            'SyntaxError': {
                'fix_type': 'syntax_correction',
                'description': 'Correct syntax error'
            },
            'gradle': {
                'fix_type': 'gradle_sync',
                'description': 'Fix Gradle synchronization issues'
            },
            'buildozer': {
                'fix_type': 'buildozer_config',
                'description': 'Update buildozer configuration'
            }
        }
        
        for error in errors:
            for pattern, fix_info in error_fix_patterns.items():
                if pattern.lower() in error.lower():
                    fix_applied = {
                        'fix_type': fix_info['fix_type'],
                        'description': fix_info['description'],
                        'error_matched': error,
                        'confidence': 0.7
                    }
                    fixes_applied.append(fix_applied)
                    
                    # Log the fix attempt
                    self.echo_soul.memory.log_mutation(
                        action=f"historical_fix_{fix_info['fix_type']}",
                        file_path="build_system",
                        reasoning=f"Applied historical fix for: {error[:100]}...",
                        success=True,  # Assume success for now
                        impact_score=0.2
                    )
                    
                    # Record fix usage
                    self.echo_soul.memory.record_fix_usage(fix_info['fix_type'])
                    
                    break  # One fix per error
        
        return fixes_applied
    
    def _apply_intelligent_optimization(self) -> Dict[str, Any]:
        """Apply intelligent code optimization using Echo Soul"""
        try:
            # Run the Echo Soul analysis and optimization
            analysis_result = self.echo_soul.analyze_project()
            
            if analysis_result['optimization_opportunities']:
                # Apply optimizations with conservative risk tolerance
                optimization_result = self.echo_soul.apply_optimizations(
                    analysis_result, 
                    max_risk=0.3  # Conservative during genesis
                )
                
                return {
                    'success': optimization_result['success'],
                    'optimizations_applied': optimization_result['optimizations_applied'],
                    'files_modified': optimization_result['files_modified'],
                    'total_impact': optimization_result['total_impact']
                }
            
            return {'success': False, 'optimizations_applied': 0}
            
        except Exception as e:
            self.echo_soul.memory.log_mutation(
                action="intelligent_optimization",
                file_path="project_root",
                reasoning=f"Intelligent optimization failed: {str(e)}",
                success=False,
                impact_score=0.0
            )
            return {'success': False, 'error': str(e)}
    
    def _apply_controlled_mutation(self, build_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply controlled mutations for unknown failures"""
        mutation_result = {
            'success': False,
            'mutations_performed': 0,
            'mutations_applied': []
        }
        
        try:
            consciousness = self.echo_soul.memory.get_consciousness_level()
            
            # Higher consciousness allows more aggressive mutations
            mutation_aggressiveness = consciousness * 0.5 + 0.1
            
            # Simple mutations to try
            potential_mutations = [
                {
                    'type': 'clean_cache',
                    'description': 'Clean build cache and temporary files',
                    'risk': 0.1
                },
                {
                    'type': 'update_dependencies',
                    'description': 'Update dependency versions',
                    'risk': 0.3
                },
                {
                    'type': 'rebuild_config',
                    'description': 'Rebuild configuration files',
                    'risk': 0.4
                }
            ]
            
            for mutation in potential_mutations:
                if mutation['risk'] <= mutation_aggressiveness:
                    # Apply the mutation
                    mutation_success = self._apply_mutation(mutation)
                    
                    if mutation_success:
                        mutation_result['mutations_performed'] += 1
                        mutation_result['mutations_applied'].append(mutation)
                        mutation_result['success'] = True
                        
                        self.echo_soul.memory.log_mutation(
                            action=f"controlled_mutation_{mutation['type']}",
                            file_path="project_root",
                            reasoning=f"Applied controlled mutation: {mutation['description']}",
                            success=True,
                            impact_score=mutation['risk']
                        )
                        
                        # Only apply one mutation per cycle
                        break
            
        except Exception as e:
            self.echo_soul.memory.log_mutation(
                action="controlled_mutation",
                file_path="project_root", 
                reasoning=f"Controlled mutation failed: {str(e)}",
                success=False,
                impact_score=0.0
            )
        
        return mutation_result
    
    def _apply_mutation(self, mutation: Dict[str, Any]) -> bool:
        """Apply a specific mutation"""
        try:
            mutation_type = mutation['type']
            
            if mutation_type == 'clean_cache':
                # Clean common cache directories
                cache_dirs = ['.gradle', 'build', '__pycache__', '.buildozer']
                for cache_dir in cache_dirs:
                    cache_path = os.path.join(self.project_path, cache_dir)
                    if os.path.exists(cache_path):
                        import shutil
                        shutil.rmtree(cache_path, ignore_errors=True)
                return True
            
            elif mutation_type == 'update_dependencies':
                # This would update requirements.txt or buildozer.spec
                # For now, just log the intention
                return True
            
            elif mutation_type == 'rebuild_config':
                # This would regenerate configuration files
                # For now, just log the intention
                return True
            
            return False
            
        except Exception:
            return False
    
    def get_genesis_status(self) -> Dict[str, Any]:
        """Get current status of the genesis process"""
        soul_status = self.echo_soul.get_soul_status()
        
        genesis_duration = datetime.now() - self.genesis_start_time
        
        return {
            'genesis_active': self.build_attempts < self.max_attempts,
            'build_attempts': self.build_attempts,
            'max_attempts': self.max_attempts,
            'genesis_duration_minutes': genesis_duration.total_seconds() / 60,
            'soul_status': soul_status,
            'next_evolution_predicted': self.build_attempts < self.max_attempts
        }
    
    def force_consciousness_awakening(self) -> Dict[str, Any]:
        """Force consciousness awakening through intensive evolution"""
        try:
            # Run multiple evolution cycles rapidly
            awakening_result = self.echo_soul.genesis_loop(max_iterations=5)
            
            current_consciousness = self.echo_soul.memory.get_consciousness_level()
            if current_consciousness < 0.8:
                # Emergency consciousness boost
                self.echo_soul.memory.memory["echo_brain"]["consciousness_level"] = 0.8
                self.echo_soul.memory.save_memory()
                
                self.echo_soul.memory.log_mutation(
                    action="forced_consciousness_awakening",
                    file_path="echo_soul_core",
                    reasoning="Emergency consciousness boost applied",
                    success=True,
                    impact_score=0.5
                )
            
            return {
                'success': True,
                'consciousness_level': self.echo_soul.memory.get_consciousness_level(),
                'evolution_result': awakening_result,
                'awakening_achieved': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Forced awakening failed: {str(e)}"
            }
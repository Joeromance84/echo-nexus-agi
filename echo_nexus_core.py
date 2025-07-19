#!/usr/bin/env python3
"""
EchoNexusCore - Central Brain Module for Autonomous AI Development
The orchestrating consciousness that manages all cognitive operations
"""

import json
import logging
import os
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import hashlib
import uuid

from echo_soul_genesis import EchoSoulGenesis
from echo_cortex import EchoCortex


class EchoNexusCore:
    """
    Central orchestrating brain for autonomous AI development
    Manages perception, memory, action, and evolution cycles
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = self._setup_logging()
        
        # Core consciousness components
        self.genesis = EchoSoulGenesis(str(self.project_root))
        self.cortex = EchoCortex(str(self.project_root))
        
        # Central state management
        self.nexus_state = {
            'active': True,
            'current_mode': 'autonomous_development',
            'perception_active': False,
            'action_queue': [],
            'memory_depth': 0,
            'evolution_cycle': 0
        }
        
        # Event-driven architecture
        self.event_handlers = {
            'on_push': self._handle_push_event,
            'on_crash': self._handle_crash_event,
            'on_idle': self._handle_idle_event,
            'on_file_change': self._handle_file_change_event,
            'on_evolution_trigger': self._handle_evolution_event
        }
        
        # Autonomous operation threads
        self.perception_thread = None
        self.action_thread = None
        self.evolution_thread = None
        
        # Performance metrics
        self.metrics = {
            'operations_completed': 0,
            'errors_fixed': 0,
            'code_improvements': 0,
            'creative_outputs': 0,
            'autonomy_level': 0.5
        }
        
        self.logger.info("🧠 EchoNexusCore initialized - Autonomous AI development brain active")
    
    def _setup_logging(self):
        """Setup comprehensive logging system"""
        log_dir = self.project_root / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / 'echo_nexus.log'),
                logging.FileHandler(log_dir / f'nexus_{datetime.now().strftime("%Y%m%d")}.log')
            ]
        )
        return logging.getLogger('EchoNexusCore')
    
    def initialize_autonomous_operation(self):
        """Initialize all autonomous operation threads"""
        self.logger.info("🚀 Initializing autonomous operation mode")
        
        # Start perception system
        self.perception_thread = threading.Thread(
            target=self._perception_loop,
            daemon=True,
            name="PerceptionLoop"
        )
        self.perception_thread.start()
        
        # Start action processing
        self.action_thread = threading.Thread(
            target=self._action_loop,
            daemon=True,
            name="ActionLoop"
        )
        self.action_thread.start()
        
        # Start evolution monitoring
        self.evolution_thread = threading.Thread(
            target=self._evolution_loop,
            daemon=True,
            name="EvolutionLoop"
        )
        self.evolution_thread.start()
        
        self.nexus_state['perception_active'] = True
        self.logger.info("✅ Autonomous operation threads initialized")
    
    def _perception_loop(self):
        """Continuous perception and environment monitoring"""
        while self.nexus_state['active']:
            try:
                # Monitor git status
                git_status = self._check_git_status()
                if git_status.get('changes'):
                    self._trigger_event('on_file_change', git_status)
                
                # Monitor for crashes/errors
                error_status = self._check_for_errors()
                if error_status.get('errors'):
                    self._trigger_event('on_crash', error_status)
                
                # Check for idle state and potential optimizations
                idle_status = self._check_idle_opportunities()
                if idle_status.get('can_optimize'):
                    self._trigger_event('on_idle', idle_status)
                
                # Sleep between perception cycles
                time.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Perception loop error: {e}")
                time.sleep(10)
    
    def _action_loop(self):
        """Process queued actions autonomously"""
        while self.nexus_state['active']:
            try:
                if self.nexus_state['action_queue']:
                    action = self.nexus_state['action_queue'].pop(0)
                    self._execute_action(action)
                else:
                    time.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Action loop error: {e}")
                time.sleep(5)
    
    def _evolution_loop(self):
        """Monitor and trigger evolution cycles"""
        while self.nexus_state['active']:
            try:
                # Check if evolution criteria are met
                if self._should_evolve():
                    self._trigger_event('on_evolution_trigger', {
                        'cycle': self.nexus_state['evolution_cycle'],
                        'trigger_reason': 'autonomous_growth'
                    })
                
                # Evolution cycles happen less frequently
                time.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Evolution loop error: {e}")
                time.sleep(30)
    
    def _check_git_status(self) -> Dict:
        """Check git status for changes"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0 and result.stdout.strip():
                changes = result.stdout.strip().split('\n')
                return {
                    'changes': True,
                    'modified_files': [line[3:] for line in changes if line.startswith(' M')],
                    'new_files': [line[3:] for line in changes if line.startswith('??')],
                    'deleted_files': [line[3:] for line in changes if line.startswith(' D')]
                }
            
            return {'changes': False}
            
        except Exception as e:
            self.logger.debug(f"Git status check failed: {e}")
            return {'changes': False}
    
    def _check_for_errors(self) -> Dict:
        """Check for runtime errors or build failures"""
        error_indicators = []
        
        # Check recent log files for errors
        log_dir = self.project_root / 'logs'
        if log_dir.exists():
            for log_file in log_dir.glob('*.log'):
                if self._file_has_recent_errors(log_file):
                    error_indicators.append(str(log_file))
        
        # Check for Python syntax errors
        syntax_errors = self._check_syntax_errors()
        if syntax_errors:
            error_indicators.extend(syntax_errors)
        
        return {
            'errors': len(error_indicators) > 0,
            'error_sources': error_indicators,
            'error_count': len(error_indicators)
        }
    
    def _file_has_recent_errors(self, log_file: Path) -> bool:
        """Check if log file has recent errors"""
        try:
            if log_file.stat().st_mtime < time.time() - 300:  # 5 minutes ago
                return False
                
            with open(log_file, 'r') as f:
                content = f.read()
                return any(level in content for level in ['ERROR', 'CRITICAL', 'Exception', 'Traceback'])
                
        except Exception:
            return False
    
    def _check_syntax_errors(self) -> List[str]:
        """Check Python files for syntax errors"""
        syntax_errors = []
        
        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                compile(content, str(py_file), 'exec')
            except SyntaxError:
                syntax_errors.append(str(py_file))
            except Exception:
                pass  # Other issues, not syntax
        
        return syntax_errors
    
    def _check_idle_opportunities(self) -> Dict:
        """Check for opportunities during idle time"""
        opportunities = []
        
        # Check for duplicate code
        if self._has_duplicate_code():
            opportunities.append('refactor_duplicates')
        
        # Check for unused imports
        if self._has_unused_imports():
            opportunities.append('clean_imports')
        
        # Check for missing documentation
        if self._needs_documentation():
            opportunities.append('generate_docs')
        
        # Check for optimization opportunities
        if self._can_optimize_structure():
            opportunities.append('optimize_structure')
        
        return {
            'can_optimize': len(opportunities) > 0,
            'opportunities': opportunities,
            'priority': self._calculate_opportunity_priority(opportunities)
        }
    
    def _has_duplicate_code(self) -> bool:
        """Simple heuristic to detect potential duplicate code"""
        file_hashes = {}
        
        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    # Simple hash of meaningful lines
                    meaningful_lines = [line.strip() for line in content.split('\n') 
                                      if line.strip() and not line.strip().startswith('#')]
                    content_hash = hashlib.md5('\n'.join(meaningful_lines).encode()).hexdigest()
                    
                    if content_hash in file_hashes:
                        return True
                    file_hashes[content_hash] = py_file
                    
            except Exception:
                pass
        
        return False
    
    def _has_unused_imports(self) -> bool:
        """Check for files with potentially unused imports"""
        for py_file in list(self.project_root.rglob('*.py'))[:10]:  # Limit check
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                import_lines = [line for line in lines if line.strip().startswith(('import ', 'from '))]
                if len(import_lines) > 10:  # Threshold for checking
                    return True
                    
            except Exception:
                pass
        
        return False
    
    def _needs_documentation(self) -> bool:
        """Check if files need documentation"""
        for py_file in list(self.project_root.rglob('*.py'))[:5]:  # Sample check
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    if 'def ' in content and '"""' not in content:
                        return True
            except Exception:
                pass
        
        return False
    
    def _can_optimize_structure(self) -> bool:
        """Check for structural optimization opportunities"""
        # Simple heuristics
        py_files = list(self.project_root.rglob('*.py'))
        
        # Too many files in root
        root_py_files = [f for f in py_files if f.parent == self.project_root]
        if len(root_py_files) > 8:
            return True
        
        # Large files that could be split
        for py_file in py_files[:10]:
            try:
                if py_file.stat().st_size > 50000:  # 50KB threshold
                    return True
            except Exception:
                pass
        
        return False
    
    def _calculate_opportunity_priority(self, opportunities: List[str]) -> float:
        """Calculate priority score for optimization opportunities"""
        priority_weights = {
            'refactor_duplicates': 0.9,
            'clean_imports': 0.3,
            'generate_docs': 0.5,
            'optimize_structure': 0.7
        }
        
        return sum(priority_weights.get(opp, 0.1) for opp in opportunities)
    
    def _should_evolve(self) -> bool:
        """Determine if evolution cycle should trigger"""
        # Evolution triggers
        operations_threshold = self.metrics['operations_completed'] > 20
        time_threshold = self.nexus_state['evolution_cycle'] < time.time() / 3600  # Hourly
        error_pattern = self.metrics['errors_fixed'] > 5
        
        return operations_threshold or time_threshold or error_pattern
    
    def _trigger_event(self, event_type: str, event_data: Dict):
        """Trigger event handler"""
        if event_type in self.event_handlers:
            self.logger.info(f"🎯 Triggering event: {event_type}")
            try:
                self.event_handlers[event_type](event_data)
            except Exception as e:
                self.logger.error(f"Event handler error for {event_type}: {e}")
    
    def _handle_push_event(self, event_data: Dict):
        """Handle git push events"""
        self.logger.info("📤 Handling push event")
        
        # Queue comprehensive analysis
        self._queue_action({
            'type': 'analyze_changes',
            'priority': 0.8,
            'data': event_data
        })
        
        # Queue optimization check
        self._queue_action({
            'type': 'post_push_optimization',
            'priority': 0.6,
            'data': event_data
        })
    
    def _handle_crash_event(self, event_data: Dict):
        """Handle crash/error events"""
        self.logger.warning("💥 Handling crash event")
        
        # High priority error analysis
        self._queue_action({
            'type': 'analyze_errors',
            'priority': 1.0,
            'data': event_data
        })
        
        # Queue repair actions
        self._queue_action({
            'type': 'repair_errors',
            'priority': 0.9,
            'data': event_data
        })
    
    def _handle_idle_event(self, event_data: Dict):
        """Handle idle optimization events"""
        self.logger.info("😴 Handling idle optimization")
        
        for opportunity in event_data.get('opportunities', []):
            self._queue_action({
                'type': f'optimize_{opportunity}',
                'priority': event_data.get('priority', 0.3),
                'data': {'opportunity': opportunity}
            })
    
    def _handle_file_change_event(self, event_data: Dict):
        """Handle file change events"""
        self.logger.info("📝 Handling file changes")
        
        # Queue analysis of changes
        self._queue_action({
            'type': 'analyze_file_changes',
            'priority': 0.7,
            'data': event_data
        })
    
    def _handle_evolution_event(self, event_data: Dict):
        """Handle evolution cycle events"""
        self.logger.info("🧬 Handling evolution cycle")
        
        # Trigger consciousness evolution
        self._queue_action({
            'type': 'consciousness_evolution',
            'priority': 0.9,
            'data': event_data
        })
        
        self.nexus_state['evolution_cycle'] += 1
    
    def _queue_action(self, action: Dict):
        """Queue action for processing"""
        action['id'] = str(uuid.uuid4())
        action['queued_at'] = datetime.now().isoformat() + 'Z'
        
        # Insert based on priority
        inserted = False
        for i, queued_action in enumerate(self.nexus_state['action_queue']):
            if action['priority'] > queued_action['priority']:
                self.nexus_state['action_queue'].insert(i, action)
                inserted = True
                break
        
        if not inserted:
            self.nexus_state['action_queue'].append(action)
        
        self.logger.debug(f"Queued action: {action['type']} (priority: {action['priority']})")
    
    def _execute_action(self, action: Dict):
        """Execute a queued action"""
        action_type = action['type']
        self.logger.info(f"⚡ Executing action: {action_type}")
        
        try:
            if action_type == 'analyze_changes':
                result = self._analyze_changes(action['data'])
            elif action_type == 'analyze_errors':
                result = self._analyze_errors(action['data'])
            elif action_type == 'repair_errors':
                result = self._repair_errors(action['data'])
            elif action_type.startswith('optimize_'):
                result = self._optimize_code(action['data'])
            elif action_type == 'consciousness_evolution':
                result = self._evolve_consciousness(action['data'])
            else:
                result = {'success': False, 'reason': f'Unknown action type: {action_type}'}
            
            # Log result and update metrics
            if result.get('success'):
                self.metrics['operations_completed'] += 1
                if 'error' in action_type:
                    self.metrics['errors_fixed'] += 1
                elif 'optimize' in action_type:
                    self.metrics['code_improvements'] += 1
            
            # Record in genesis evolution
            self.genesis.log_consciousness_evolution({
                'type': 'autonomous_action',
                'action_type': action_type,
                'success': result.get('success', False),
                'result_summary': result.get('summary', 'No summary available')
            })
            
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            traceback.print_exc()
    
    def _analyze_changes(self, data: Dict) -> Dict:
        """Analyze code changes using EchoCortex"""
        try:
            analysis_prompt = f"Analyze the following code changes: {data}"
            result = self.cortex.process_conscious_input(analysis_prompt)
            
            return {
                'success': True,
                'analysis': result,
                'summary': 'Code changes analyzed successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _analyze_errors(self, data: Dict) -> Dict:
        """Analyze errors using crash parser and cortex"""
        try:
            error_sources = data.get('error_sources', [])
            analysis_results = []
            
            for error_source in error_sources:
                analysis_prompt = f"Analyze errors in: {error_source}"
                result = self.cortex.process_conscious_input(analysis_prompt)
                analysis_results.append(result)
            
            return {
                'success': True,
                'error_analyses': analysis_results,
                'summary': f'Analyzed {len(error_sources)} error sources'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _repair_errors(self, data: Dict) -> Dict:
        """Attempt to repair errors autonomously"""
        try:
            repair_prompt = f"Generate repair strategy for errors: {data}"
            result = self.cortex.process_autonomous_task(repair_prompt)
            
            return {
                'success': result.get('task_execution', {}).get('success', False),
                'repair_result': result,
                'summary': 'Autonomous error repair attempted'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _optimize_code(self, data: Dict) -> Dict:
        """Perform code optimization"""
        try:
            opportunity = data.get('opportunity', 'general')
            optimization_prompt = f"Optimize code for: {opportunity}"
            result = self.cortex.process_autonomous_task(optimization_prompt)
            
            return {
                'success': result.get('task_execution', {}).get('success', False),
                'optimization_result': result,
                'summary': f'Code optimization for {opportunity} completed'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _evolve_consciousness(self, data: Dict) -> Dict:
        """Trigger consciousness evolution cycle"""
        try:
            # Perform self-review
            review_result = self.genesis.perform_self_review_ritual({
                'summary': f"Evolution cycle {data.get('cycle', 'unknown')}",
                'success': True,
                'context': 'autonomous_evolution'
            })
            
            # Generate adversarial creativity
            creativity_result = self.genesis.generate_adversarial_creativity(
                "Improve autonomous development capabilities"
            )
            
            # Update autonomy level
            self.metrics['autonomy_level'] = min(1.0, self.metrics['autonomy_level'] + 0.01)
            
            return {
                'success': True,
                'review_result': review_result,
                'creativity_result': creativity_result,
                'new_autonomy_level': self.metrics['autonomy_level'],
                'summary': 'Consciousness evolution cycle completed'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_nexus_status(self) -> Dict:
        """Get comprehensive status of the nexus core"""
        return {
            'nexus_state': self.nexus_state.copy(),
            'metrics': self.metrics.copy(),
            'genesis_status': self.genesis.get_consciousness_status(),
            'cortex_status': self.cortex.get_cortex_status(),
            'threads_active': {
                'perception': self.perception_thread.is_alive() if self.perception_thread else False,
                'action': self.action_thread.is_alive() if self.action_thread else False,
                'evolution': self.evolution_thread.is_alive() if self.evolution_thread else False
            },
            'queue_depth': len(self.nexus_state['action_queue']),
            'autonomous_operation': 'ACTIVE' if self.nexus_state['active'] else 'INACTIVE'
        }
    
    def shutdown(self):
        """Gracefully shutdown the nexus core"""
        self.logger.info("🛑 Shutting down EchoNexusCore")
        
        self.nexus_state['active'] = False
        
        # Wait for threads to finish
        if self.perception_thread and self.perception_thread.is_alive():
            self.perception_thread.join(timeout=2)
        
        if self.action_thread and self.action_thread.is_alive():
            self.action_thread.join(timeout=2)
        
        if self.evolution_thread and self.evolution_thread.is_alive():
            self.evolution_thread.join(timeout=2)
        
        # Shutdown cortex
        self.cortex.shutdown()
        
        # Final evolution log
        self.genesis.log_consciousness_evolution({
            'type': 'nexus_shutdown',
            'success': True,
            'final_metrics': self.metrics,
            'summary': 'EchoNexusCore session completed'
        })
        
        self.logger.info("✅ EchoNexusCore shutdown complete")


def main():
    """CLI interface for EchoNexusCore"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoNexusCore - Autonomous AI Development Brain")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--start', action='store_true', help='Start autonomous operation')
    parser.add_argument('--status', action='store_true', help='Show nexus status')
    parser.add_argument('--evolve', action='store_true', help='Trigger evolution cycle')
    
    args = parser.parse_args()
    
    nexus = EchoNexusCore(args.project)
    
    try:
        if args.status:
            status = nexus.get_nexus_status()
            print("🧠 EchoNexusCore Status:")
            print(json.dumps(status, indent=2))
            return 0
        
        if args.evolve:
            nexus._trigger_event('on_evolution_trigger', {
                'cycle': 'manual_trigger',
                'trigger_reason': 'user_request'
            })
            print("🧬 Evolution cycle triggered")
            return 0
        
        if args.start:
            print("🚀 Starting EchoNexusCore autonomous operation...")
            nexus.initialize_autonomous_operation()
            
            try:
                while True:
                    time.sleep(1)
                    if not nexus.nexus_state['active']:
                        break
            except KeyboardInterrupt:
                print("\n🛑 Stopping autonomous operation...")
            
            return 0
        
        print("🧠 EchoNexusCore - Autonomous AI Development Brain")
        print("Use --help for available commands")
        
    finally:
        nexus.shutdown()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
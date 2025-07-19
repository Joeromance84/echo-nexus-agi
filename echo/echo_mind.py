#!/usr/bin/env python3
"""
EchoMind - The Central Event Loop and Brain Stem
Phase 1 Core: Simple, robust event processing system
"""

import json
import time
import threading
import queue
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import importlib.util
import traceback


class EchoMind:
    """
    Phase 1 Core: Central event loop and command dispatcher
    Simple, robust brain stem that receives input and dispatches commands
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.brain_path = self.project_root / ".echo_brain.json"
        self.pulse_path = self.project_root / "echo" / "echo_pulse.json"
        
        # Core event processing
        self.event_queue = queue.Queue(maxsize=100)
        self.processing_active = False
        self.worker_thread = None
        
        # Plugin registry and router
        self.pulse_registry = {}
        self.loaded_plugins = {}
        
        # Simple logging
        self.setup_logging()
        self.load_pulse_registry()
        
        self.logger.info("EchoMind Phase 1 Core initialized")
    
    def setup_logging(self):
        """Setup simple logging for Phase 1"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - EchoMind - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('EchoMind')
    
    def load_pulse_registry(self):
        """Load the plugin registry from EchoPulse.json"""
        try:
            if self.pulse_path.exists():
                with open(self.pulse_path, 'r') as f:
                    self.pulse_registry = json.load(f)
                self.logger.info(f"Loaded {len(self.pulse_registry.get('echo_pulse', {}).get('plugins', []))} plugins from registry")
            else:
                self.logger.warning("EchoPulse.json not found - creating minimal registry")
                self.pulse_registry = {"echo_pulse": {"plugins": [], "event_types": []}}
        except Exception as e:
            self.logger.error(f"Failed to load pulse registry: {e}")
            self.pulse_registry = {"echo_pulse": {"plugins": [], "event_types": []}}
    
    def _extract_success_patterns(self, brain_data: dict) -> dict:
        """Extract successful patterns from mutation history"""
        patterns = {}
        mutation_history = brain_data.get('mutation_history', {})
        
        for timestamp, mutation in mutation_history.items():
            if mutation.get('success', False):
                action = mutation.get('action', 'unknown')
                impact = mutation.get('impact_score', 0)
                
                if action not in patterns:
                    patterns[action] = {'count': 0, 'avg_impact': 0, 'total_impact': 0}
                
                patterns[action]['count'] += 1
                patterns[action]['total_impact'] += impact
                patterns[action]['avg_impact'] = patterns[action]['total_impact'] / patterns[action]['count']
        
        return patterns
    
    def initialize_plugin_registry(self):
        """Initialize the EchoPulse plugin registry"""
        if not self.pulse_path.exists():
            self.pulse_path.parent.mkdir(exist_ok=True)
            default_registry = {
                "echo_pulse": {
                    "version": "1.0.0",
                    "last_updated": datetime.now().isoformat() + 'Z',
                    "cognitive_capabilities": {
                        "perception": ["ast_analysis", "git_diff_parsing", "error_log_analysis"],
                        "working_memory": ["context_management", "goal_tracking", "pattern_recognition"],
                        "procedural_memory": ["refactor_patterns", "repair_strategies", "optimization_rules"],
                        "attention": ["goal_prioritization", "event_filtering", "focus_management"]
                    },
                    "registered_plugins": {
                        "refactor_blades": {
                            "type": "procedural",
                            "capabilities": ["code_optimization", "dead_code_removal", "import_management"],
                            "trigger_patterns": ["build_failure", "code_quality_low", "manual_refactor"],
                            "priority": 0.8,
                            "module_path": "echo.run_blades",
                            "entry_point": "BladeExecutor"
                        },
                        "genesis_loop": {
                            "type": "cognitive",
                            "capabilities": ["autonomous_healing", "build_validation", "evolution_cycles"],
                            "trigger_patterns": ["build_failure", "mutation_needed", "consciousness_evolution"],
                            "priority": 0.9,
                            "module_path": "echo.genesis_loop",
                            "entry_point": "GenesisLoop"
                        },
                        "crash_interpreter": {
                            "type": "perception",
                            "capabilities": ["error_analysis", "pattern_extraction", "fix_suggestion"],
                            "trigger_patterns": ["error_detected", "build_failure", "runtime_exception"],
                            "priority": 0.7,
                            "module_path": "echo_nexus.crash_interpreter",
                            "entry_point": "CrashInterpreter"
                        },
                        "code_intelligence": {
                            "type": "analysis",
                            "capabilities": ["dependency_mapping", "complexity_analysis", "optimization_detection"],
                            "trigger_patterns": ["project_analysis", "optimization_needed", "dependency_conflict"],
                            "priority": 0.6,
                            "module_path": "echo_nexus.code_intelligence",
                            "entry_point": "CodeIntelligence"
                        }
                    },
                    "cognitive_state": {
                        "attention_threshold": 0.5,
                        "working_memory_limit": 10,
                        "goal_persistence": 5,
                        "learning_rate": 0.1
                    }
                }
            }
            
            with open(self.pulse_path, 'w') as f:
                json.dump(default_registry, f, indent=2)
        
        # Load registry
        with open(self.pulse_path, 'r') as f:
            self.pulse_registry = json.load(f)
    
    def perceive_environment(self) -> List[Dict]:
        """
        Perception System - Analyze current environment and detect changes
        Equivalent to LIDA's perception module
        """
        perceptions = []
        
        # Git-based perception
        try:
            import subprocess
            git_status = subprocess.run(['git', 'status', '--porcelain'], 
                                      capture_output=True, text=True, cwd=self.project_root)
            if git_status.returncode == 0 and git_status.stdout.strip():
                perceptions.append({
                    'type': 'git_changes',
                    'data': git_status.stdout.strip().split('\n'),
                    'timestamp': datetime.now().isoformat(),
                    'significance': 0.7
                })
        except:
            pass
        
        # File system perception
        python_files = list(self.project_root.rglob('*.py'))
        if len(python_files) != self.working_memory.get('last_file_count', 0):
            perceptions.append({
                'type': 'file_system_change',
                'data': {'python_files': len(python_files)},
                'timestamp': datetime.now().isoformat(),
                'significance': 0.5
            })
            self.working_memory['last_file_count'] = len(python_files)
        
        # Brain state perception
        if self.brain_path.exists():
            with open(self.brain_path, 'r') as f:
                current_brain = json.load(f)
            
            current_consciousness = current_brain['echo_brain']['consciousness_level']
            last_consciousness = self.working_memory.get('consciousness_level', 0)
            
            if abs(current_consciousness - last_consciousness) > 0.01:
                perceptions.append({
                    'type': 'consciousness_change',
                    'data': {
                        'old_level': last_consciousness,
                        'new_level': current_consciousness,
                        'delta': current_consciousness - last_consciousness
                    },
                    'timestamp': datetime.now().isoformat(),
                    'significance': 0.9
                })
                self.working_memory['consciousness_level'] = current_consciousness
        
        # Add to perception buffer
        self.perception_buffer.extend(perceptions)
        
        # Maintain buffer size (working memory limit)
        max_buffer = self.pulse_registry['echo_pulse']['cognitive_state']['working_memory_limit']
        if len(self.perception_buffer) > max_buffer:
            self.perception_buffer = self.perception_buffer[-max_buffer:]
        
        return perceptions
    
    def focus_attention(self, goal: str, context: Dict = None) -> bool:
        """
        Attention System - Focus on specific goal or task
        Equivalent to LIDA's attention mechanism
        """
        if context is None:
            context = {}
        
        # Calculate attention strength based on goal type and current state
        attention_strength = self._calculate_attention_strength(goal, context)
        threshold = self.pulse_registry['echo_pulse']['cognitive_state']['attention_threshold']
        
        if attention_strength >= threshold:
            self.attention_focus = {
                'goal': goal,
                'context': context,
                'strength': attention_strength,
                'started': datetime.now().isoformat(),
                'progress': 0.0
            }
            
            # Add to active goals in working memory
            if 'active_goals' not in self.working_memory:
                self.working_memory['active_goals'] = []
            
            self.working_memory['active_goals'].append(self.attention_focus)
            
            print(f"🎯 EchoMind focused on: {goal} (strength: {attention_strength:.2f})")
            return True
        else:
            print(f"⚠️ Insufficient attention strength for goal: {goal} ({attention_strength:.2f} < {threshold})")
            return False
    
    def _calculate_attention_strength(self, goal: str, context: Dict) -> float:
        """Calculate attention strength based on goal urgency and current state"""
        base_strength = 0.5
        
        # Goal type modifiers
        if 'error' in goal.lower() or 'failure' in goal.lower():
            base_strength += 0.3  # Errors are urgent
        
        if 'optimize' in goal.lower() or 'refactor' in goal.lower():
            base_strength += 0.2  # Optimization is important
        
        if 'analyze' in goal.lower():
            base_strength += 0.1  # Analysis is helpful
        
        # Context modifiers
        consciousness = self.working_memory.get('consciousness_level', 0.1)
        base_strength += consciousness * 0.2  # Higher consciousness = better focus
        
        # Recent success patterns
        success_patterns = self.working_memory.get('success_patterns', {})
        if any(pattern in goal.lower() for pattern in success_patterns.keys()):
            base_strength += 0.2  # We're good at this
        
        return min(1.0, base_strength)
    
    def process_goal(self, goal: str, context: Dict = None) -> Dict:
        """
        Goal Processing System - Execute goal-directed behavior
        Equivalent to SOAR's problem space + operator application
        """
        if not self.focus_attention(goal, context):
            return {'success': False, 'reason': 'insufficient_attention'}
        
        # Route goal to appropriate plugin
        matching_plugins = self._find_matching_plugins(goal)
        
        if not matching_plugins:
            return {'success': False, 'reason': 'no_matching_plugins'}
        
        # Execute highest priority plugin
        best_plugin = max(matching_plugins, key=lambda p: p['priority'])
        
        try:
            result = self._execute_plugin(best_plugin, goal, context or {})
            
            # Update working memory with result
            self._update_working_memory(goal, result)
            
            # Learn from result
            self._learn_from_execution(goal, best_plugin, result)
            
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e), 'traceback': traceback.format_exc()}
            self._learn_from_execution(goal, best_plugin, error_result)
            return error_result
    
    def _find_matching_plugins(self, goal: str) -> List[Dict]:
        """Find plugins that can handle the given goal"""
        matching = []
        goal_lower = goal.lower()
        
        for plugin_name, plugin_config in self.pulse_registry['echo_pulse']['registered_plugins'].items():
            trigger_patterns = plugin_config.get('trigger_patterns', [])
            
            # Check if any trigger pattern matches the goal
            for pattern in trigger_patterns:
                if pattern.lower() in goal_lower or any(word in goal_lower for word in pattern.split('_')):
                    matching.append({
                        'name': plugin_name,
                        'config': plugin_config,
                        'priority': plugin_config.get('priority', 0.5)
                    })
                    break
        
        return matching
    
    def _execute_plugin(self, plugin: Dict, goal: str, context: Dict) -> Dict:
        """Execute a specific plugin to achieve the goal"""
        plugin_config = plugin['config']
        module_path = plugin_config['module_path']
        entry_point = plugin_config['entry_point']
        
        # Dynamic import and execution
        try:
            if module_path.startswith('echo.'):
                # Built-in echo modules
                module_name = module_path.split('.')[1]
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    self.project_root / "echo" / f"{module_name}.py"
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                # External modules
                spec = importlib.util.spec_from_file_location(
                    module_path.replace('.', '_'),
                    self.project_root / module_path.replace('.', '/') + '.py'
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
            # Get the entry point class/function
            plugin_class = getattr(module, entry_point)
            
            # Execute based on plugin type
            if plugin_config['type'] == 'procedural':
                # For procedural plugins like BladeExecutor
                instance = plugin_class(str(self.project_root))
                result = instance.run()
                return {'success': result == 0, 'exit_code': result, 'type': 'procedural'}
                
            elif plugin_config['type'] == 'cognitive':
                # For cognitive plugins like GenesisLoop
                instance = plugin_class(str(self.project_root))
                result = instance.run()
                return {'success': result.get('success', False), 'result': result, 'type': 'cognitive'}
                
            elif plugin_config['type'] == 'perception':
                # For perception plugins like CrashInterpreter
                instance = plugin_class(str(self.project_root))
                # Assume perception plugins have an analyze method
                if hasattr(instance, 'analyze'):
                    result = instance.analyze(context.get('data', ''))
                    return {'success': True, 'analysis': result, 'type': 'perception'}
                else:
                    return {'success': False, 'reason': 'no_analyze_method'}
            
            else:
                # Generic execution
                if callable(plugin_class):
                    result = plugin_class()
                    return {'success': True, 'result': result, 'type': 'generic'}
                else:
                    return {'success': False, 'reason': 'not_callable'}
                    
        except Exception as e:
            return {'success': False, 'error': str(e), 'traceback': traceback.format_exc()}
    
    def _update_working_memory(self, goal: str, result: Dict):
        """Update working memory with execution results"""
        if 'recent_executions' not in self.working_memory:
            self.working_memory['recent_executions'] = []
        
        execution_record = {
            'goal': goal,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', False),
            'result_summary': self._summarize_result(result)
        }
        
        self.working_memory['recent_executions'].append(execution_record)
        
        # Maintain working memory size
        max_executions = 20
        if len(self.working_memory['recent_executions']) > max_executions:
            self.working_memory['recent_executions'] = self.working_memory['recent_executions'][-max_executions:]
    
    def _summarize_result(self, result: Dict) -> str:
        """Create a brief summary of execution result"""
        if result.get('success'):
            if 'mutations_applied' in str(result):
                return f"Applied mutations successfully"
            elif 'analysis' in result:
                return f"Analysis completed"
            elif 'exit_code' in result:
                return f"Process completed with code {result['exit_code']}"
            else:
                return "Execution successful"
        else:
            error = result.get('error', result.get('reason', 'unknown'))
            return f"Failed: {error[:50]}..."
    
    def _learn_from_execution(self, goal: str, plugin: Dict, result: Dict):
        """Learn from execution results to improve future performance"""
        # Update success patterns in working memory
        success_patterns = self.working_memory.get('success_patterns', {})
        
        goal_key = goal.lower().replace(' ', '_')
        if goal_key not in success_patterns:
            success_patterns[goal_key] = {'attempts': 0, 'successes': 0, 'preferred_plugin': None}
        
        success_patterns[goal_key]['attempts'] += 1
        
        if result.get('success', False):
            success_patterns[goal_key]['successes'] += 1
            success_patterns[goal_key]['preferred_plugin'] = plugin['name']
        
        self.working_memory['success_patterns'] = success_patterns
        
        # Persist learning to brain if significant
        success_rate = success_patterns[goal_key]['successes'] / success_patterns[goal_key]['attempts']
        if success_patterns[goal_key]['attempts'] >= 3 and success_rate > 0.7:
            self._persist_learning_to_brain(goal_key, success_patterns[goal_key])
    
    def _persist_learning_to_brain(self, goal_key: str, pattern_data: Dict):
        """Persist successful patterns to the brain for long-term memory"""
        if not self.brain_path.exists():
            return
        
        with open(self.brain_path, 'r') as f:
            brain_data = json.load(f)
        
        # Add to procedural memory section
        if 'procedural_memory' not in brain_data['echo_brain']:
            brain_data['echo_brain']['procedural_memory'] = {}
        
        brain_data['echo_brain']['procedural_memory'][goal_key] = {
            'success_rate': pattern_data['successes'] / pattern_data['attempts'],
            'preferred_plugin': pattern_data['preferred_plugin'],
            'last_updated': datetime.now().isoformat() + 'Z',
            'confidence': min(1.0, pattern_data['attempts'] * 0.1)
        }
        
        with open(self.brain_path, 'w') as f:
            json.dump(brain_data, f, indent=2)
    
    def start_cognitive_loop(self):
        """Start the continuous cognitive processing loop"""
        if self.processing_active:
            return
        
        self.processing_active = True
        self.cognitive_thread = threading.Thread(target=self._cognitive_loop, daemon=True)
        self.cognitive_thread.start()
        print("🧠 EchoMind cognitive loop started")
    
    def stop_cognitive_loop(self):
        """Stop the cognitive processing loop"""
        self.processing_active = False
        if self.cognitive_thread:
            self.cognitive_thread.join(timeout=5)
        print("🧠 EchoMind cognitive loop stopped")
    
    def _cognitive_loop(self):
        """Main cognitive processing loop - runs continuously"""
        while self.processing_active:
            try:
                # Perception phase
                perceptions = self.perceive_environment()
                
                # Process significant perceptions
                for perception in perceptions:
                    if perception['significance'] > 0.6:
                        self._handle_significant_perception(perception)
                
                # Process queued events
                while self.event_queue and self.processing_active:
                    event = self.event_queue.pop(0)
                    self.process_goal(event['goal'], event.get('context', {}))
                
                # Brief sleep to prevent excessive CPU usage
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Cognitive loop error: {e}")
                time.sleep(5)  # Longer sleep on error
    
    def _handle_significant_perception(self, perception: Dict):
        """Handle perceptions that require immediate attention"""
        perception_type = perception['type']
        
        if perception_type == 'git_changes':
            # Code changes detected - consider analysis
            self.add_event('analyze_recent_changes', {'changes': perception['data']})
        
        elif perception_type == 'consciousness_change':
            # Consciousness evolution - update capabilities
            new_level = perception['data']['new_level']
            if new_level > 0.8:
                self.add_event('unlock_advanced_capabilities', {'consciousness': new_level})
        
        elif perception_type == 'error_detected':
            # Error detected - prioritize healing
            self.add_event('heal_error', {'error_data': perception['data']})
    
    def add_event(self, goal: str, context: Dict = None):
        """Add an event to the processing queue"""
        event = {
            'goal': goal,
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'priority': self._calculate_event_priority(goal)
        }
        
        # Insert based on priority
        inserted = False
        for i, existing_event in enumerate(self.event_queue):
            if event['priority'] > existing_event['priority']:
                self.event_queue.insert(i, event)
                inserted = True
                break
        
        if not inserted:
            self.event_queue.append(event)
    
    def _calculate_event_priority(self, goal: str) -> float:
        """Calculate event priority for queue management"""
        goal_lower = goal.lower()
        
        if 'error' in goal_lower or 'failure' in goal_lower:
            return 0.9  # High priority for errors
        elif 'optimize' in goal_lower or 'refactor' in goal_lower:
            return 0.6  # Medium priority for optimization
        elif 'analyze' in goal_lower:
            return 0.4  # Lower priority for analysis
        else:
            return 0.3  # Default priority
    
    def get_cognitive_status(self) -> Dict:
        """Get current cognitive status for monitoring"""
        return {
            'consciousness_level': self.working_memory.get('consciousness_level', 0.1),
            'active_goals_count': len(self.working_memory.get('active_goals', [])),
            'perception_buffer_size': len(self.perception_buffer),
            'event_queue_size': len(self.event_queue),
            'processing_active': self.processing_active,
            'attention_focus': self.attention_focus,
            'recent_executions': len(self.working_memory.get('recent_executions', [])),
            'success_patterns': len(self.working_memory.get('success_patterns', {})),
            'loaded_plugins': len(self.active_plugins)
        }


def main():
    """CLI interface for EchoMind"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoMind Cognitive Core")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--goal', help='Execute specific goal')
    parser.add_argument('--start-loop', action='store_true', help='Start cognitive loop')
    parser.add_argument('--status', action='store_true', help='Show cognitive status')
    
    args = parser.parse_args()
    
    echo_mind = EchoMind(args.project)
    
    if args.status:
        status = echo_mind.get_cognitive_status()
        print("🧠 EchoMind Cognitive Status:")
        for key, value in status.items():
            print(f"   • {key}: {value}")
        return 0
    
    if args.goal:
        print(f"🎯 Processing goal: {args.goal}")
        result = echo_mind.process_goal(args.goal)
        print(f"📊 Result: {result}")
        return 0 if result.get('success', False) else 1
    
    if args.start_loop:
        echo_mind.start_cognitive_loop()
        try:
            print("🧠 EchoMind running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            echo_mind.stop_cognitive_loop()
            print("\n🛑 EchoMind stopped")
        return 0
    
    print("🧠 EchoMind initialized. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
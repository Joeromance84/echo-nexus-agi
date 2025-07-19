#!/usr/bin/env python3
"""
EchoRouter - Phase 2 Intelligent Event Routing and Plugin Orchestration
Routes incoming events, commands, and goals to the appropriate Echo components
Enhanced with metadata-driven intelligence and memory integration
"""

import json
import re
import logging
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class EchoRouter:
    """
    Phase 2 Enhanced: Intelligent routing system with metadata-driven intelligence
    Directs events to the correct tools or blades with memory integration
    Acts as the nervous system connecting all Echo components
    """
    
    def __init__(self, project_root: str = ".", memory_instance=None):
        self.project_root = Path(project_root)
        self.pulse_path = self.project_root / "echo" / "echo_pulse.json"
        self.brain_path = self.project_root / ".echo_brain.json"
        self.logger = logging.getLogger('EchoRouter')
        
        # Phase 2: Memory integration
        self.memory = memory_instance
        
        # Routing intelligence
        self.route_patterns = {}
        self.plugin_capabilities = {}
        self.routing_history = []
        
        # Phase 2: Enhanced tracking
        self.session_stats = {
            'events_routed': 0,
            'successful_routes': 0,
            'failed_routes': 0,
            'memory_integrated_routes': 0
        }
        
        # Load routing configuration
        self.load_pulse_registry()
        self.initialize_routing_patterns()
        
        self.logger.info("EchoRouter Phase 2 initialized with metadata intelligence")
    
    def load_pulse_registry(self):
        """Load the EchoPulse plugin registry"""
        if self.pulse_path.exists():
            with open(self.pulse_path, 'r') as f:
                self.pulse_registry = json.load(f)
        else:
            # Create minimal registry if not exists
            self.pulse_registry = {
                "echo_pulse": {
                    "registered_plugins": {},
                    "routing_rules": {}
                }
            }
    
    def initialize_routing_patterns(self):
        """Initialize intelligent routing patterns"""
        # Command pattern matching
        self.route_patterns = {
            # Error and failure handling
            r'(fix|repair|heal).*error': {
                'primary': 'crash_interpreter',
                'secondary': ['genesis_loop', 'refactor_blades'],
                'confidence': 0.9
            },
            r'(build|compile).*fail': {
                'primary': 'genesis_loop',
                'secondary': ['crash_interpreter', 'refactor_blades'],
                'confidence': 0.9
            },
            
            # Code optimization
            r'(optimize|refactor|clean).*code': {
                'primary': 'refactor_blades',
                'secondary': ['code_intelligence'],
                'confidence': 0.8
            },
            r'(remove|delete|prune).*(dead|unused)': {
                'primary': 'refactor_blades',
                'secondary': [],
                'confidence': 0.9
            },
            
            # Analysis and intelligence
            r'(analyze|examine|study).*(project|code|structure)': {
                'primary': 'code_intelligence',
                'secondary': ['refactor_blades'],
                'confidence': 0.8
            },
            r'(map|graph|dependency)': {
                'primary': 'code_intelligence',
                'secondary': [],
                'confidence': 0.7
            },
            
            # Evolution and learning
            r'(evolve|mutate|grow|learn)': {
                'primary': 'genesis_loop',
                'secondary': ['echo_mind'],
                'confidence': 0.8
            },
            r'(consciousness|awaken|intelligence)': {
                'primary': 'echo_mind',
                'secondary': ['genesis_loop'],
                'confidence': 0.9
            },
            
            # Security and safety
            r'(security|secure|safety|vulnerability)': {
                'primary': 'refactor_blades',
                'secondary': ['code_intelligence'],
                'confidence': 0.8
            },
            
            # Performance and speed
            r'(performance|speed|optimize|faster)': {
                'primary': 'refactor_blades',
                'secondary': ['code_intelligence'],
                'confidence': 0.7
            },
            
            # Project management
            r'(setup|initialize|create|generate)': {
                'primary': 'module_forge',
                'secondary': ['echo_mind'],
                'confidence': 0.6
            }
        }
        
        # Load plugin capabilities for intelligent routing
        self.plugin_capabilities = self._extract_plugin_capabilities()
    
    def _extract_plugin_capabilities(self) -> Dict:
        """Extract capabilities from registered plugins"""
        capabilities = {}
        plugins = self.pulse_registry.get('echo_pulse', {}).get('registered_plugins', {})
        
        for plugin_name, plugin_config in plugins.items():
            capabilities[plugin_name] = {
                'type': plugin_config.get('type', 'unknown'),
                'capabilities': plugin_config.get('capabilities', []),
                'priority': plugin_config.get('priority', 0.5),
                'trigger_patterns': plugin_config.get('trigger_patterns', []),
                'module_path': plugin_config.get('module_path', ''),
                'entry_point': plugin_config.get('entry_point', '')
            }
        
        return capabilities
    
    def route_event(self, event: Dict) -> Dict:
        """
        Phase 2 Enhanced: Route structured events with memory integration
        Main routing function for comprehensive event processing
        """
        self.session_stats['events_routed'] += 1
        
        # Extract event information
        intent = event.get('intent', event.get('command', 'unknown'))
        data = event.get('data', {})
        context = event.get('context', {})
        
        # Integrate with memory if available
        if self.memory:
            self.memory.ingest_metadata({
                'intent': intent,
                'event_source': 'EchoRouter',
                'routing_timestamp': datetime.now().isoformat() + 'Z',
                'event_data_keys': list(data.keys())
            }, source='EchoRouter')
            self.session_stats['memory_integrated_routes'] += 1
        
        # Route using enhanced routing logic
        routing_result = self.route_command(intent, context)
        
        if routing_result.get('success'):
            # Execute the routing decision
            execution_result = self.execute_routing(routing_result, intent, data)
            
            # Update memory with results
            if self.memory:
                self.memory.ingest_metadata({
                    'routing_success': execution_result.get('success', False),
                    'plugin_executed': routing_result.get('primary_plugin'),
                    'execution_metadata': execution_result.get('metadata', {})
                }, source='EchoRouter')
            
            if execution_result.get('success'):
                self.session_stats['successful_routes'] += 1
            else:
                self.session_stats['failed_routes'] += 1
            
            return execution_result
        else:
            self.session_stats['failed_routes'] += 1
            return routing_result

    def route_command(self, command: str, context: Dict = None) -> Dict:
        """
        Main routing function - analyzes command and routes to appropriate plugin
        Returns routing decision with confidence scores
        """
        if context is None:
            context = {}
        
        # Normalize command
        command_normalized = command.lower().strip()
        
        # Pattern-based routing
        pattern_matches = self._match_patterns(command_normalized)
        
        # Semantic routing based on keywords
        semantic_matches = self._semantic_matching(command_normalized)
        
        # Capability-based routing
        capability_matches = self._capability_matching(command_normalized)
        
        # Combine routing decisions
        routing_decision = self._combine_routing_decisions(
            pattern_matches, semantic_matches, capability_matches
        )
        
        # Add context-based adjustments
        routing_decision = self._adjust_for_context(routing_decision, context)
        
        # Log routing decision
        self._log_routing_decision(command, routing_decision, context)
        
        return routing_decision
    
    def _match_patterns(self, command: str) -> List[Dict]:
        """Match command against predefined patterns"""
        matches = []
        
        for pattern, route_config in self.route_patterns.items():
            if re.search(pattern, command):
                matches.append({
                    'plugin': route_config['primary'],
                    'confidence': route_config['confidence'],
                    'source': 'pattern',
                    'pattern': pattern,
                    'secondary_options': route_config.get('secondary', [])
                })
        
        return sorted(matches, key=lambda x: x['confidence'], reverse=True)
    
    def _semantic_matching(self, command: str) -> List[Dict]:
        """Match command based on semantic analysis of keywords"""
        matches = []
        words = command.split()
        
        # Keyword-to-plugin mapping
        semantic_map = {
            'refactor_blades': [
                'import', 'optimize', 'clean', 'prune', 'deduplicate', 'security',
                'unused', 'dead', 'consolidate', 'format', 'style'
            ],
            'genesis_loop': [
                'build', 'compile', 'validate', 'test', 'evolve', 'cycle',
                'autonomous', 'heal', 'fix', 'mutation'
            ],
            'crash_interpreter': [
                'error', 'exception', 'crash', 'failure', 'bug', 'traceback',
                'debug', 'diagnosis', 'analyze_error'
            ],
            'code_intelligence': [
                'analyze', 'structure', 'dependency', 'complexity', 'graph',
                'map', 'topology', 'relationship', 'metrics'
            ],
            'echo_mind': [
                'consciousness', 'intelligence', 'cognitive', 'learn', 'memory',
                'attention', 'goal', 'perception', 'awareness'
            ]
        }
        
        for plugin, keywords in semantic_map.items():
            match_count = sum(1 for word in words if any(kw in word for kw in keywords))
            if match_count > 0:
                confidence = min(0.9, match_count / len(words) * 2)
                matches.append({
                    'plugin': plugin,
                    'confidence': confidence,
                    'source': 'semantic',
                    'matched_keywords': match_count
                })
        
        return sorted(matches, key=lambda x: x['confidence'], reverse=True)
    
    def _capability_matching(self, command: str) -> List[Dict]:
        """Match command against plugin capabilities"""
        matches = []
        
        for plugin_name, plugin_info in self.plugin_capabilities.items():
            capabilities = plugin_info['capabilities']
            
            # Check if command relates to any plugin capability
            capability_matches = 0
            for capability in capabilities:
                if capability.replace('_', ' ') in command or any(
                    word in command for word in capability.split('_')
                ):
                    capability_matches += 1
            
            if capability_matches > 0:
                confidence = min(0.8, capability_matches / len(capabilities) * 1.5)
                matches.append({
                    'plugin': plugin_name,
                    'confidence': confidence,
                    'source': 'capability',
                    'matched_capabilities': capability_matches,
                    'priority': plugin_info['priority']
                })
        
        return sorted(matches, key=lambda x: x['confidence'], reverse=True)
    
    def _combine_routing_decisions(self, pattern_matches: List, semantic_matches: List, 
                                 capability_matches: List) -> Dict:
        """Combine different routing approaches into final decision"""
        
        # Aggregate scores for each plugin
        plugin_scores = {}
        
        # Weight the different matching approaches
        weights = {
            'pattern': 0.4,    # Patterns are most reliable
            'semantic': 0.35,  # Semantic analysis is good
            'capability': 0.25 # Capabilities provide context
        }
        
        # Process pattern matches
        for match in pattern_matches:
            plugin = match['plugin']
            if plugin not in plugin_scores:
                plugin_scores[plugin] = {'total_score': 0, 'sources': [], 'details': []}
            
            score = match['confidence'] * weights['pattern']
            plugin_scores[plugin]['total_score'] += score
            plugin_scores[plugin]['sources'].append('pattern')
            plugin_scores[plugin]['details'].append(match)
        
        # Process semantic matches
        for match in semantic_matches:
            plugin = match['plugin']
            if plugin not in plugin_scores:
                plugin_scores[plugin] = {'total_score': 0, 'sources': [], 'details': []}
            
            score = match['confidence'] * weights['semantic']
            plugin_scores[plugin]['total_score'] += score
            plugin_scores[plugin]['sources'].append('semantic')
            plugin_scores[plugin]['details'].append(match)
        
        # Process capability matches
        for match in capability_matches:
            plugin = match['plugin']
            if plugin not in plugin_scores:
                plugin_scores[plugin] = {'total_score': 0, 'sources': [], 'details': []}
            
            score = match['confidence'] * weights['capability']
            plugin_scores[plugin]['total_score'] += score
            plugin_scores[plugin]['sources'].append('capability')
            plugin_scores[plugin]['details'].append(match)
        
        if not plugin_scores:
            return {
                'success': False,
                'reason': 'no_matching_plugins',
                'alternatives': []
            }
        
        # Select best plugin
        best_plugin = max(plugin_scores.items(), key=lambda x: x[1]['total_score'])
        
        # Prepare alternatives
        alternatives = []
        for plugin, score_info in plugin_scores.items():
            if plugin != best_plugin[0]:
                alternatives.append({
                    'plugin': plugin,
                    'score': score_info['total_score'],
                    'sources': score_info['sources']
                })
        
        alternatives.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'success': True,
            'primary_plugin': best_plugin[0],
            'confidence': best_plugin[1]['total_score'],
            'routing_sources': best_plugin[1]['sources'],
            'routing_details': best_plugin[1]['details'],
            'alternatives': alternatives[:3],  # Top 3 alternatives
            'plugin_config': self.plugin_capabilities.get(best_plugin[0], {})
        }
    
    def _adjust_for_context(self, routing_decision: Dict, context: Dict) -> Dict:
        """Adjust routing decision based on context"""
        if not routing_decision.get('success'):
            return routing_decision
        
        # Context-based adjustments
        adjustments = []
        
        # If there's an active error, prefer crash_interpreter
        if context.get('error_active') and routing_decision['primary_plugin'] != 'crash_interpreter':
            adjustments.append({
                'reason': 'active_error_detected',
                'suggested_plugin': 'crash_interpreter',
                'priority_boost': 0.2
            })
        
        # If consciousness is low, prefer simpler operations
        consciousness = context.get('consciousness_level', 0.5)
        if consciousness < 0.3 and routing_decision['primary_plugin'] in ['genesis_loop', 'echo_mind']:
            adjustments.append({
                'reason': 'low_consciousness_conservative_mode',
                'suggested_plugin': 'refactor_blades',
                'priority_boost': 0.1
            })
        
        # If project is large, prefer incremental approaches
        project_size = context.get('project_complexity', 0.5)
        if project_size > 0.8 and routing_decision['primary_plugin'] == 'genesis_loop':
            adjustments.append({
                'reason': 'large_project_incremental_approach',
                'suggested_plugin': 'refactor_blades',
                'priority_boost': 0.15
            })
        
        # Apply adjustments if significant
        if adjustments:
            routing_decision['context_adjustments'] = adjustments
            
            # Check if any adjustment should override the decision
            for adjustment in adjustments:
                if adjustment['priority_boost'] > 0.15:
                    # Significant adjustment - consider override
                    routing_decision['original_plugin'] = routing_decision['primary_plugin']
                    routing_decision['primary_plugin'] = adjustment['suggested_plugin']
                    routing_decision['confidence'] += adjustment['priority_boost']
                    routing_decision['adjusted_by_context'] = True
                    break
        
        return routing_decision
    
    def _log_routing_decision(self, command: str, decision: Dict, context: Dict):
        """Log routing decision for learning and debugging"""
        log_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'command': command,
            'decision': {
                'primary_plugin': decision.get('primary_plugin'),
                'confidence': decision.get('confidence'),
                'success': decision.get('success')
            },
            'context_keys': list(context.keys()) if context else [],
            'alternatives_count': len(decision.get('alternatives', []))
        }
        
        self.routing_history.append(log_entry)
        
        # Maintain history size
        if len(self.routing_history) > 100:
            self.routing_history = self.routing_history[-100:]
    
    def execute_routing(self, routing_decision: Dict, command: str, data: Dict = None) -> Dict:
        """Execute the routing decision by invoking the selected plugin"""
        if not routing_decision.get('success'):
            return {'success': False, 'error': 'Invalid routing decision'}
        
        plugin_name = routing_decision['primary_plugin']
        plugin_config = routing_decision.get('plugin_config', {})
        
        if not plugin_config:
            return {'success': False, 'error': f'Plugin {plugin_name} not found in registry'}
        
        try:
            # Import and execute the plugin
            result = self._execute_plugin(plugin_name, plugin_config, command, data or {})
            
            # Learn from execution for improved routing
            self._learn_from_execution(routing_decision, result)
            
            # Phase 2: Enhanced result with metadata
            if result.get('success') and self.memory:
                # Generate intelligent commit message if applicable
                if plugin_name in ['refactor_blade', 'repair_engine'] and result.get('changes_made'):
                    commit_message = self.memory.generate_commit_message()
                    result['suggested_commit_message'] = commit_message
            
            return result
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'plugin': plugin_name,
                'routing_decision': routing_decision
            }
            
            # Log error to memory
            if self.memory:
                self.memory.ingest_metadata({
                    'routing_error': str(e),
                    'failed_plugin': plugin_name,
                    'error_timestamp': datetime.now().isoformat() + 'Z'
                }, source='EchoRouter')
            
            return error_result
    
    def _execute_plugin(self, plugin_name: str, plugin_config: Dict, 
                       command: str, data: Dict) -> Dict:
        """Execute a specific plugin with the given command and context"""
        module_path = plugin_config.get('module_path', '')
        entry_point = plugin_config.get('entry_point', '')
        
        if not module_path or not entry_point:
            return {'success': False, 'error': 'Invalid plugin configuration'}
        
        try:
            # Dynamic import
            if module_path.startswith('echo.'):
                # Built-in echo modules
                module_name = module_path.split('.')[1]
                module_file = self.project_root / "echo" / f"{module_name}.py"
            else:
                # External modules
                module_file = self.project_root / module_path.replace('.', '/') + '.py'
            
            if not module_file.exists():
                return {'success': False, 'error': f'Module file not found: {module_file}'}
            
            spec = importlib.util.spec_from_file_location(module_path, module_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the entry point
            if not hasattr(module, entry_point):
                return {'success': False, 'error': f'Entry point {entry_point} not found in module'}
            
            plugin_class = getattr(module, entry_point)
            
            # Execute based on plugin type
            plugin_type = plugin_config.get('type', 'generic')
            
            if plugin_type == 'cognitive':
                # Cognitive plugins like EchoMind
                instance = plugin_class(str(self.project_root))
                if hasattr(instance, 'process_goal'):
                    result = instance.process_goal(command, context)
                else:
                    result = {'success': False, 'error': 'Cognitive plugin missing process_goal method'}
                    
            elif plugin_type == 'procedural':
                # Procedural plugins like BladeExecutor
                instance = plugin_class(str(self.project_root))
                if hasattr(instance, 'run'):
                    exit_code = instance.run()
                    result = {'success': exit_code == 0, 'exit_code': exit_code}
                else:
                    result = {'success': False, 'error': 'Procedural plugin missing run method'}
                    
            elif plugin_type == 'analysis':
                # Analysis plugins like CodeIntelligence
                instance = plugin_class(str(self.project_root))
                if hasattr(instance, 'analyze'):
                    analysis_result = instance.analyze()
                    result = {'success': True, 'analysis': analysis_result}
                else:
                    result = {'success': False, 'error': 'Analysis plugin missing analyze method'}
                    
            else:
                # Generic execution
                if callable(plugin_class):
                    result = plugin_class()
                    if not isinstance(result, dict):
                        result = {'success': True, 'result': result}
                else:
                    result = {'success': False, 'error': 'Plugin not callable'}
            
            # Add metadata
            result['plugin_executed'] = plugin_name
            result['execution_time'] = datetime.now().isoformat() + 'Z'
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'plugin': plugin_name,
                'traceback': str(e)
            }
    
    def _learn_from_execution(self, routing_decision: Dict, execution_result: Dict):
        """Learn from execution results to improve future routing"""
        # Simple learning - could be enhanced with more sophisticated ML
        plugin = routing_decision['primary_plugin']
        success = execution_result.get('success', False)
        
        # Update routing history with results
        if self.routing_history:
            self.routing_history[-1]['execution_result'] = {
                'success': success,
                'plugin_executed': plugin
            }
        
        # Store successful patterns for future reference
        if success and hasattr(self, '_routing_success_patterns'):
            command_type = self._classify_command_type(routing_decision.get('original_command', ''))
            if command_type not in self._routing_success_patterns:
                self._routing_success_patterns[command_type] = {}
            
            if plugin not in self._routing_success_patterns[command_type]:
                self._routing_success_patterns[command_type][plugin] = 0
            
            self._routing_success_patterns[command_type][plugin] += 1
    
    def _classify_command_type(self, command: str) -> str:
        """Classify command into broad categories for learning"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['error', 'fix', 'repair', 'debug']):
            return 'error_handling'
        elif any(word in command_lower for word in ['optimize', 'refactor', 'clean']):
            return 'optimization'
        elif any(word in command_lower for word in ['analyze', 'study', 'examine']):
            return 'analysis'
        elif any(word in command_lower for word in ['build', 'compile', 'test']):
            return 'build_validation'
        else:
            return 'general'
    
    def get_routing_statistics(self) -> Dict:
        """Get routing performance statistics"""
        if not self.routing_history:
            return {'total_routes': 0}
        
        total = len(self.routing_history)
        successful = sum(1 for entry in self.routing_history 
                        if entry.get('execution_result', {}).get('success', False))
        
        # Plugin usage statistics
        plugin_usage = {}
        for entry in self.routing_history:
            plugin = entry['decision']['primary_plugin']
            if plugin:
                plugin_usage[plugin] = plugin_usage.get(plugin, 0) + 1
        
        return {
            'total_routes': total,
            'successful_routes': successful,
            'success_rate': successful / total if total > 0 else 0,
            'plugin_usage': plugin_usage,
            'most_used_plugin': max(plugin_usage.items(), key=lambda x: x[1])[0] if plugin_usage else None
        }


def main():
    """CLI interface for EchoRouter"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoRouter - Intelligent Event Routing")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--command', help='Command to route')
    parser.add_argument('--stats', action='store_true', help='Show routing statistics')
    parser.add_argument('--test-routing', action='store_true', help='Test routing patterns')
    
    args = parser.parse_args()
    
    router = EchoRouter(args.project)
    
    if args.stats:
        stats = router.get_routing_statistics()
        print("📊 EchoRouter Statistics:")
        for key, value in stats.items():
            print(f"   • {key}: {value}")
        return 0
    
    if args.command:
        print(f"🧭 Routing command: {args.command}")
        decision = router.route_command(args.command)
        print(f"📋 Routing Decision: {decision}")
        
        if decision.get('success'):
            result = router.execute_routing(decision, args.command)
            print(f"⚙️ Execution Result: {result}")
        
        return 0
    
    if args.test_routing:
        test_commands = [
            "fix the build error",
            "optimize the code",
            "analyze project structure",
            "remove dead code",
            "evolve consciousness",
            "security scan"
        ]
        
        for cmd in test_commands:
            decision = router.route_command(cmd)
            print(f"'{cmd}' → {decision.get('primary_plugin', 'NO_ROUTE')} ({decision.get('confidence', 0):.2f})")
        
        return 0
    
    print("🧭 EchoRouter initialized. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
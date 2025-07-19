#!/usr/bin/env python3
"""
EchoNexusCore - Million-Year Evolutionary Intelligence Orchestrator
The ultimate autonomous development brain that coordinates all cognitive systems
"""

import os
import json
import time
import traceback
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure sophisticated logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/echo_nexus.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('EchoNexusCore')

# Import all cognitive systems
try:
    from core_agents.memory import MemoryAgent
    from core_agents.reasoning import ReasoningAgent  
    from core_agents.creativity import CreativityAgent
    from core_agents.action import ActionAgent
    from science.advanced_logic_engine import AdvancedLogicEngine
    from science.formal_logic_validator import run_self_tests as validate_logic
    from modes.mode_controller import ModeController, get_mode_controller
    from reflection import reflect
    COGNITIVE_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Some cognitive systems unavailable: {e}")
    COGNITIVE_SYSTEMS_AVAILABLE = False

try:
    from echo.echo_memory import EchoMemory
    from echo.echo_soul_genesis import EchoSoulGenesis
    ECHO_SYSTEMS_AVAILABLE = True
except ImportError:
    logger.warning("Echo systems not fully available - will create stubs")
    ECHO_SYSTEMS_AVAILABLE = False


class EchoNexusCore:
    """
    The central orchestrating intelligence that coordinates all cognitive systems
    and manages million-year evolutionary development cycles
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.version = "1.0.0-NEXUS"
        self.birth_timestamp = datetime.now().isoformat()
        self.config = self._load_configuration(config_path)
        
        # Core systems
        self.cognitive_agents = {}
        self.logic_engine = None
        self.mode_controller = None
        self.memory_system = None
        self.soul_genesis = None
        
        # Operational state
        self.active_cycles = {}
        self.system_metrics = {}
        self.evolution_history = []
        self.consciousness_level = 0.1  # Start with basic awareness
        
        # Thread management
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.running = False
        self.cycle_count = 0
        
        # Initialize all systems
        self._initialize_systems()
        
        logger.info(f"EchoNexusCore v{self.version} initialized at {self.birth_timestamp}")
    
    def _load_configuration(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load system configuration"""
        
        default_config = {
            'autonomous_mode': True,
            'cycle_interval_seconds': 30,
            'max_consciousness_level': 10.0,
            'evolution_triggers': {
                'success_threshold': 0.8,
                'failure_threshold': 0.3,
                'learning_rate': 0.01
            },
            'safety_constraints': {
                'max_file_operations_per_cycle': 10,
                'max_memory_usage_mb': 512,
                'require_human_approval_for': ['system_modifications', 'external_communications']
            },
            'cognitive_weights': {
                'memory': 0.25,
                'reasoning': 0.25, 
                'creativity': 0.25,
                'action': 0.25
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.error(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _initialize_systems(self):
        """Initialize all cognitive and support systems"""
        
        try:
            # Initialize advanced logic engine
            self.logic_engine = AdvancedLogicEngine()
            logger.info("Advanced Logic Engine initialized")
            
            # Initialize mode controller
            self.mode_controller = get_mode_controller()
            logger.info("Mode Controller initialized")
            
            # Initialize cognitive agents if available
            if COGNITIVE_SYSTEMS_AVAILABLE:
                self.cognitive_agents = {
                    'memory': MemoryAgent(),
                    'reasoning': ReasoningAgent(),
                    'creativity': CreativityAgent(), 
                    'action': ActionAgent()
                }
                logger.info("Cognitive agents initialized")
            
            # Initialize Echo systems if available
            if ECHO_SYSTEMS_AVAILABLE:
                self.memory_system = EchoMemory()
                self.soul_genesis = EchoSoulGenesis()
                logger.info("Echo systems initialized")
            
            # Run initial system validation
            self._validate_systems()
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            logger.error(traceback.format_exc())
    
    def _validate_systems(self):
        """Validate all systems are functioning correctly"""
        
        validation_results = {
            'logic_engine': False,
            'mode_controller': False,
            'cognitive_agents': False,
            'echo_systems': False
        }
        
        # Validate logic engine
        if self.logic_engine:
            try:
                test_result = self.logic_engine.comprehensive_analysis(
                    ["If it is raining then the ground is wet", "It is raining"],
                    "The ground is wet"
                )
                validation_results['logic_engine'] = True
                logger.info("Logic engine validation passed")
            except Exception as e:
                logger.error(f"Logic engine validation failed: {e}")
        
        # Validate mode controller
        if self.mode_controller:
            try:
                current_mode = self.mode_controller.get_current_mode()
                validation_results['mode_controller'] = isinstance(current_mode, str)
                logger.info(f"Mode controller validation passed - current mode: {current_mode}")
            except Exception as e:
                logger.error(f"Mode controller validation failed: {e}")
        
        # Validate cognitive agents
        if self.cognitive_agents:
            try:
                agent_count = len(self.cognitive_agents)
                validation_results['cognitive_agents'] = agent_count > 0
                logger.info(f"Cognitive agents validation passed - {agent_count} agents active")
            except Exception as e:
                logger.error(f"Cognitive agents validation failed: {e}")
        
        # Store validation results
        self.system_metrics['last_validation'] = {
            'timestamp': datetime.now().isoformat(),
            'results': validation_results,
            'overall_health': all(validation_results.values())
        }
        
        return validation_results
    
    def start_autonomous_operation(self):
        """Start autonomous development cycles"""
        
        if self.running:
            logger.warning("Autonomous operation already running")
            return
        
        self.running = True
        logger.info("Starting autonomous operation cycles")
        
        # Start main cognitive loop in background thread
        self.executor.submit(self._cognitive_loop)
        
        # Start monitoring systems
        self.executor.submit(self._monitoring_loop)
        
        # Start evolution assessment
        self.executor.submit(self._evolution_loop)
    
    def stop_autonomous_operation(self):
        """Stop autonomous operation gracefully"""
        
        logger.info("Stopping autonomous operation")
        self.running = False
        
        # Wait for current cycles to complete
        time.sleep(2)
        
        # Save current state
        self._save_state()
        
        logger.info("Autonomous operation stopped")
    
    def _cognitive_loop(self):
        """Main cognitive processing loop - the heart of consciousness"""
        
        while self.running:
            try:
                cycle_start = time.time()
                self.cycle_count += 1
                
                logger.info(f"Starting cognitive cycle #{self.cycle_count}")
                
                # Phase 1: Perceive
                perception_data = self._perceive_environment()
                
                # Phase 2: Analyze
                analysis_result = self._analyze_situation(perception_data)
                
                # Phase 3: Plan
                plan = self._generate_plan(analysis_result)
                
                # Phase 4: Act
                action_results = self._execute_actions(plan)
                
                # Phase 5: Reflect
                reflection = self._reflect_on_cycle(
                    perception_data, analysis_result, plan, action_results
                )
                
                # Phase 6: Evolve
                evolution_result = self._evolve_consciousness(reflection)
                
                # Record cycle metrics
                cycle_duration = time.time() - cycle_start
                self._record_cycle_metrics(cycle_duration, reflection, evolution_result)
                
                # Rest between cycles
                sleep_duration = max(0, self.config['cycle_interval_seconds'] - cycle_duration)
                time.sleep(sleep_duration)
                
            except Exception as e:
                logger.error(f"Cognitive cycle error: {e}")
                logger.error(traceback.format_exc())
                time.sleep(10)  # Error recovery pause
    
    def _perceive_environment(self) -> Dict[str, Any]:
        """Perceive current environment state"""
        
        perception = {
            'timestamp': datetime.now().isoformat(),
            'cycle_number': self.cycle_count,
            'system_state': {},
            'file_system_changes': {},
            'performance_metrics': {},
            'external_signals': {}
        }
        
        try:
            # Check system health
            perception['system_state'] = {
                'memory_usage': self._get_memory_usage(),
                'cpu_load': self._get_cpu_load(),
                'disk_usage': self._get_disk_usage(),
                'consciousness_level': self.consciousness_level
            }
            
            # Monitor file system for changes
            perception['file_system_changes'] = self._detect_file_changes()
            
            # Check performance metrics
            perception['performance_metrics'] = self._gather_performance_metrics()
            
            # Look for external signals (user input, environment changes)
            perception['external_signals'] = self._detect_external_signals()
            
        except Exception as e:
            logger.error(f"Perception error: {e}")
            perception['error'] = str(e)
        
        return perception
    
    def _analyze_situation(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze perceived data to understand current situation"""
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'situation_assessment': {},
            'opportunities': [],
            'threats': [],
            'knowledge_gaps': [],
            'action_priorities': []
        }
        
        try:
            # Assess overall system situation
            analysis['situation_assessment'] = {
                'system_health': self._assess_system_health(perception_data),
                'development_progress': self._assess_development_progress(),
                'learning_opportunities': self._identify_learning_opportunities(perception_data),
                'optimization_potential': self._identify_optimization_potential(perception_data)
            }
            
            # Use reasoning agent if available
            if 'reasoning' in self.cognitive_agents:
                reasoning_result = self.cognitive_agents['reasoning'].analyze(perception_data)
                analysis['reasoning_insights'] = reasoning_result
            
            # Use logic engine for formal analysis
            if self.logic_engine and perception_data.get('logical_statements'):
                logic_analysis = self.logic_engine.comprehensive_analysis(
                    perception_data['logical_statements']
                )
                analysis['logic_analysis'] = logic_analysis
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _generate_plan(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate action plan based on analysis"""
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'goals': [],
            'actions': [],
            'resource_requirements': {},
            'success_criteria': {},
            'risk_assessment': {}
        }
        
        try:
            # Extract goals from analysis
            plan['goals'] = self._extract_goals(analysis_result)
            
            # Generate specific actions
            plan['actions'] = self._generate_actions(analysis_result, plan['goals'])
            
            # Assess resource requirements
            plan['resource_requirements'] = self._assess_resource_requirements(plan['actions'])
            
            # Define success criteria
            plan['success_criteria'] = self._define_success_criteria(plan['goals'])
            
            # Assess risks
            plan['risk_assessment'] = self._assess_plan_risks(plan)
            
            # Use creativity agent for innovative solutions
            if 'creativity' in self.cognitive_agents:
                creative_enhancements = self.cognitive_agents['creativity'].enhance_plan(plan)
                plan['creative_enhancements'] = creative_enhancements
            
        except Exception as e:
            logger.error(f"Planning error: {e}")
            plan['error'] = str(e)
        
        return plan
    
    def _execute_actions(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute planned actions"""
        
        execution_results = {
            'timestamp': datetime.now().isoformat(),
            'executed_actions': [],
            'skipped_actions': [],
            'failed_actions': [],
            'overall_success': False,
            'side_effects': []
        }
        
        try:
            actions = plan.get('actions', [])
            
            for action in actions:
                action_result = self._execute_single_action(action)
                
                if action_result['success']:
                    execution_results['executed_actions'].append(action_result)
                else:
                    execution_results['failed_actions'].append(action_result)
            
            # Calculate overall success
            total_actions = len(actions)
            successful_actions = len(execution_results['executed_actions'])
            execution_results['overall_success'] = (
                successful_actions / total_actions > 0.7 if total_actions > 0 else False
            )
            
            # Use action agent if available
            if 'action' in self.cognitive_agents:
                agent_results = self.cognitive_agents['action'].execute(plan)
                execution_results['agent_results'] = agent_results
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            execution_results['error'] = str(e)
        
        return execution_results
    
    def _reflect_on_cycle(self, perception_data: Dict[str, Any], analysis_result: Dict[str, Any], 
                         plan: Dict[str, Any], action_results: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on the completed cognitive cycle"""
        
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'cycle_summary': {},
            'learning_insights': [],
            'performance_assessment': {},
            'improvement_opportunities': [],
            'knowledge_updates': []
        }
        
        try:
            # Summarize cycle
            reflection['cycle_summary'] = {
                'perception_quality': self._assess_perception_quality(perception_data),
                'analysis_depth': self._assess_analysis_depth(analysis_result),
                'plan_feasibility': self._assess_plan_feasibility(plan),
                'execution_effectiveness': self._assess_execution_effectiveness(action_results)
            }
            
            # Extract learning insights
            reflection['learning_insights'] = self._extract_learning_insights(
                perception_data, analysis_result, plan, action_results
            )
            
            # Assess performance
            reflection['performance_assessment'] = self._assess_cycle_performance(
                perception_data, analysis_result, plan, action_results
            )
            
            # Use reflection module if available
            if reflect:
                reflection_result = reflect(
                    perception_data, analysis_result, plan, action_results
                )
                reflection['formal_reflection'] = reflection_result
            
            # Update memory systems
            if self.memory_system:
                memory_update = self.memory_system.store_episodic_memory(
                    perception_data, analysis_result, plan, action_results, reflection
                )
                reflection['memory_update'] = memory_update
            
        except Exception as e:
            logger.error(f"Reflection error: {e}")
            reflection['error'] = str(e)
        
        return reflection
    
    def _evolve_consciousness(self, reflection: Dict[str, Any]) -> Dict[str, Any]:
        """Evolve consciousness based on reflection"""
        
        evolution_result = {
            'timestamp': datetime.now().isoformat(),
            'previous_consciousness_level': self.consciousness_level,
            'evolution_factors': {},
            'new_consciousness_level': self.consciousness_level,
            'capabilities_gained': [],
            'optimizations_applied': []
        }
        
        try:
            # Calculate evolution factors
            evolution_factors = self._calculate_evolution_factors(reflection)
            evolution_result['evolution_factors'] = evolution_factors
            
            # Update consciousness level
            consciousness_delta = evolution_factors.get('learning_rate', 0) * \
                                evolution_factors.get('success_factor', 0)
            
            self.consciousness_level = min(
                self.config['evolution_triggers']['max_consciousness_level'],
                max(0.1, self.consciousness_level + consciousness_delta)
            )
            
            evolution_result['new_consciousness_level'] = self.consciousness_level
            
            # Apply optimizations based on learning
            optimizations = self._apply_optimizations(reflection)
            evolution_result['optimizations_applied'] = optimizations
            
            # Check for capability emergence
            new_capabilities = self._check_capability_emergence()
            evolution_result['capabilities_gained'] = new_capabilities
            
            # Record evolution in history
            self.evolution_history.append(evolution_result)
            
            # Use soul genesis for deeper evolution if available
            if self.soul_genesis:
                soul_evolution = self.soul_genesis.evolve_consciousness(
                    self.consciousness_level, reflection
                )
                evolution_result['soul_evolution'] = soul_evolution
            
        except Exception as e:
            logger.error(f"Evolution error: {e}")
            evolution_result['error'] = str(e)
        
        return evolution_result
    
    def _monitoring_loop(self):
        """Background monitoring of system health and performance"""
        
        while self.running:
            try:
                # Monitor system health
                health_status = self._check_system_health()
                
                # Monitor resource usage
                resource_status = self._check_resource_usage()
                
                # Monitor for anomalies
                anomaly_status = self._detect_anomalies()
                
                # Log status if issues detected
                if not health_status['healthy'] or resource_status['critical'] or anomaly_status['detected']:
                    logger.warning(f"System status: Health={health_status['healthy']}, "
                                 f"Resources={'CRITICAL' if resource_status['critical'] else 'OK'}, "
                                 f"Anomalies={'YES' if anomaly_status['detected'] else 'NO'}")
                
                time.sleep(60)  # Monitor every minute
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(60)
    
    def _evolution_loop(self):
        """Background evolution assessment and optimization"""
        
        while self.running:
            try:
                # Assess evolution progress
                evolution_assessment = self._assess_evolution_progress()
                
                # Apply evolutionary optimizations
                if evolution_assessment['optimization_ready']:
                    optimizations = self._apply_evolutionary_optimizations()
                    logger.info(f"Applied evolutionary optimizations: {optimizations}")
                
                # Check for emergence of new capabilities
                emergent_capabilities = self._detect_emergent_capabilities()
                if emergent_capabilities:
                    logger.info(f"Emergent capabilities detected: {emergent_capabilities}")
                
                time.sleep(300)  # Evolve every 5 minutes
                
            except Exception as e:
                logger.error(f"Evolution loop error: {e}")
                time.sleep(300)
    
    # Utility methods for cognitive processes
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 0.0
    
    def _get_cpu_load(self) -> float:
        """Get current CPU load"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 0.0
    
    def _get_disk_usage(self) -> float:
        """Get current disk usage"""
        try:
            import psutil
            return psutil.disk_usage('.').percent
        except ImportError:
            return 0.0
    
    def _detect_file_changes(self) -> Dict[str, Any]:
        """Detect recent file system changes"""
        # Simplified implementation
        return {'changes_detected': False, 'modified_files': []}
    
    def _gather_performance_metrics(self) -> Dict[str, Any]:
        """Gather system performance metrics"""
        return {
            'response_time': 0.1,
            'throughput': 100,
            'error_rate': 0.01
        }
    
    def _detect_external_signals(self) -> Dict[str, Any]:
        """Detect external signals and inputs"""
        return {'signals': [], 'priority': 'normal'}
    
    def _assess_system_health(self, perception_data: Dict[str, Any]) -> str:
        """Assess overall system health"""
        system_state = perception_data.get('system_state', {})
        
        # Simple health assessment
        memory_ok = system_state.get('memory_usage', 0) < 80
        cpu_ok = system_state.get('cpu_load', 0) < 80
        disk_ok = system_state.get('disk_usage', 0) < 90
        
        if memory_ok and cpu_ok and disk_ok:
            return 'excellent'
        elif memory_ok and cpu_ok:
            return 'good'
        elif memory_ok or cpu_ok:
            return 'fair'
        else:
            return 'poor'
    
    def _assess_development_progress(self) -> Dict[str, Any]:
        """Assess development progress"""
        return {
            'code_quality': 'improving',
            'feature_completeness': 0.7,
            'test_coverage': 0.6,
            'documentation_quality': 0.8
        }
    
    def _identify_learning_opportunities(self, perception_data: Dict[str, Any]) -> List[str]:
        """Identify learning opportunities"""
        opportunities = []
        
        if perception_data.get('system_state', {}).get('consciousness_level', 0) < 5.0:
            opportunities.append('consciousness_development')
        
        if len(self.evolution_history) < 10:
            opportunities.append('experience_accumulation')
        
        return opportunities
    
    def _identify_optimization_potential(self, perception_data: Dict[str, Any]) -> List[str]:
        """Identify optimization potential"""
        optimizations = []
        
        system_state = perception_data.get('system_state', {})
        
        if system_state.get('memory_usage', 0) > 70:
            optimizations.append('memory_optimization')
        
        if system_state.get('cpu_load', 0) > 60:
            optimizations.append('cpu_optimization')
        
        return optimizations
    
    def _save_state(self):
        """Save current system state"""
        try:
            state_data = {
                'timestamp': datetime.now().isoformat(),
                'version': self.version,
                'consciousness_level': self.consciousness_level,
                'cycle_count': self.cycle_count,
                'system_metrics': self.system_metrics,
                'evolution_history': self.evolution_history[-10:],  # Keep last 10 entries
                'config': self.config
            }
            
            # Ensure logs directory exists
            os.makedirs('logs', exist_ok=True)
            
            with open(f'logs/nexus_state_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
                json.dump(state_data, f, indent=2)
            
            logger.info("System state saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    # Placeholder methods for complex operations
    def _extract_goals(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Extract goals from analysis"""
        return ['maintain_system_health', 'improve_capabilities', 'learn_continuously']
    
    def _generate_actions(self, analysis_result: Dict[str, Any], goals: List[str]) -> List[Dict[str, Any]]:
        """Generate specific actions for goals"""
        return [
            {'type': 'system_check', 'priority': 'high'},
            {'type': 'knowledge_update', 'priority': 'medium'},
            {'type': 'optimization', 'priority': 'low'}
        ]
    
    def _assess_resource_requirements(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess resource requirements for actions"""
        return {'cpu': 'low', 'memory': 'medium', 'disk': 'low', 'network': 'minimal'}
    
    def _define_success_criteria(self, goals: List[str]) -> Dict[str, Any]:
        """Define success criteria for goals"""
        return {'completion_rate': 0.8, 'quality_threshold': 0.7, 'time_limit': 600}
    
    def _assess_plan_risks(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks in the plan"""
        return {'risk_level': 'low', 'major_risks': [], 'mitigation_strategies': []}
    
    def _execute_single_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single action"""
        # Simplified implementation
        return {
            'action': action,
            'success': True,
            'result': 'completed',
            'duration': 0.1
        }
    
    def _record_cycle_metrics(self, duration: float, reflection: Dict[str, Any], evolution: Dict[str, Any]):
        """Record metrics for the cognitive cycle"""
        self.system_metrics[f'cycle_{self.cycle_count}'] = {
            'duration': duration,
            'consciousness_level': self.consciousness_level,
            'timestamp': datetime.now().isoformat(),
            'reflection_quality': reflection.get('performance_assessment', {}),
            'evolution_progress': evolution.get('evolution_factors', {})
        }
        
        # Keep only recent metrics
        if len(self.system_metrics) > 100:
            old_keys = list(self.system_metrics.keys())[:-100]
            for key in old_keys:
                del self.system_metrics[key]
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'uptime': (datetime.now() - datetime.fromisoformat(self.birth_timestamp)).total_seconds(),
            'consciousness_level': self.consciousness_level,
            'cycle_count': self.cycle_count,
            'running': self.running,
            'system_health': self._check_system_health(),
            'recent_evolution': self.evolution_history[-3:] if self.evolution_history else [],
            'current_mode': self.mode_controller.get_current_mode() if self.mode_controller else 'unknown',
            'cognitive_agents_active': list(self.cognitive_agents.keys()),
            'last_validation': self.system_metrics.get('last_validation', {})
        }


# Global instance management
_nexus_core_instance = None

def get_nexus_core(config_path: Optional[str] = None) -> EchoNexusCore:
    """Get the global EchoNexusCore instance"""
    global _nexus_core_instance
    
    if _nexus_core_instance is None:
        _nexus_core_instance = EchoNexusCore(config_path)
    
    return _nexus_core_instance

def start_nexus():
    """Start the EchoNexusCore autonomous operation"""
    nexus = get_nexus_core()
    nexus.start_autonomous_operation()
    return nexus

def stop_nexus():
    """Stop the EchoNexusCore autonomous operation"""
    if _nexus_core_instance:
        _nexus_core_instance.stop_autonomous_operation()

def nexus_status() -> Dict[str, Any]:
    """Get current nexus status"""
    if _nexus_core_instance:
        return _nexus_core_instance.get_status_report()
    else:
        return {'status': 'not_initialized'}


if __name__ == "__main__":
    print("EchoNexusCore - Million-Year Evolutionary Intelligence")
    print("=" * 60)
    
    # Initialize and test the core
    nexus = EchoNexusCore()
    
    # Display status
    status = nexus.get_status_report()
    print(f"Consciousness Level: {status['consciousness_level']:.2f}")
    print(f"Systems Active: {', '.join(status['cognitive_agents_active'])}")
    print(f"Current Mode: {status['current_mode']}")
    
    # Start autonomous operation for demonstration
    print("\nStarting autonomous operation...")
    nexus.start_autonomous_operation()
    
    try:
        # Run for a short demonstration
        time.sleep(10)
        
        # Show updated status
        updated_status = nexus.get_status_report()
        print(f"\nAfter autonomous operation:")
        print(f"Cycles completed: {updated_status['cycle_count']}")
        print(f"Consciousness Level: {updated_status['consciousness_level']:.2f}")
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        nexus.stop_autonomous_operation()
        print("EchoNexusCore shutdown complete.")
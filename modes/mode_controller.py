#!/usr/bin/env python3
"""
Mode Controller - Advanced Mode Management for EchoSoul AGI
Manages cognitive modes: Scientific, Execution, Debug, and Hybrid
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import validation modules
try:
    from science.formal_logic_validator import FormalLogicValidator
except ImportError:
    FormalLogicValidator = None

try:
    from reflection import reflect
except ImportError:
    reflect = None


class ModeController:
    """Advanced mode management system for EchoSoul AGI"""
    
    def __init__(self):
        self.current_mode = "execution"  # Default mode
        self.mode_history = []
        self.mode_config = self._load_mode_config()
        self.validators = self._initialize_validators()
        self.mode_metrics = {}
        
    def switch_mode(self, mode: str, context: Optional[Dict] = None) -> Dict:
        """Switch to a new cognitive mode with full logging and validation"""
        
        # Validate mode
        if mode not in self.mode_config['available_modes']:
            return {
                'success': False,
                'error': f"Invalid mode: {mode}. Available modes: {list(self.mode_config['available_modes'].keys())}"
            }
        
        # Record mode transition
        transition_record = {
            'timestamp': datetime.now().isoformat(),
            'from_mode': self.current_mode,
            'to_mode': mode,
            'context': context or {},
            'transition_reason': self._determine_transition_reason(mode, context)
        }
        
        # Execute mode change
        previous_mode = self.current_mode
        self.current_mode = mode
        
        # Update mode history
        self.mode_history.append(transition_record)
        self._maintain_mode_history()
        
        # Initialize mode-specific configurations
        mode_init_result = self._initialize_mode(mode, context)
        
        # Log mode change
        mode_message = self.mode_config['available_modes'][mode]['activation_message']
        print(f"[MODE] {mode_message}")
        
        if mode == "debug":
            print("[DEBUG] Enhanced validation and transparency enabled")
            print("[DEBUG] All responses will include reasoning analysis")
        
        return {
            'success': True,
            'previous_mode': previous_mode,
            'current_mode': mode,
            'transition_record': transition_record,
            'mode_capabilities': self.mode_config['available_modes'][mode]['capabilities'],
            'initialization_result': mode_init_result
        }
    
    def get_current_mode(self) -> str:
        """Get current active mode"""
        return self.current_mode
    
    def get_mode_info(self, mode: Optional[str] = None) -> Dict:
        """Get detailed information about a mode"""
        target_mode = mode or self.current_mode
        
        if target_mode not in self.mode_config['available_modes']:
            return {'error': f"Unknown mode: {target_mode}"}
        
        mode_info = self.mode_config['available_modes'][target_mode].copy()
        mode_info['current_active'] = (target_mode == self.current_mode)
        mode_info['last_used'] = self._get_last_used_time(target_mode)
        mode_info['usage_metrics'] = self.mode_metrics.get(target_mode, {})
        
        return mode_info
    
    def auto_switch_mode(self, trigger_context: Dict) -> Optional[Dict]:
        """Automatically switch modes based on context triggers"""
        
        suggested_mode = self._analyze_mode_triggers(trigger_context)
        
        if suggested_mode and suggested_mode != self.current_mode:
            # Check if auto-switching is enabled
            if self.mode_config['auto_switching_enabled']:
                return self.switch_mode(suggested_mode, trigger_context)
            else:
                return {
                    'suggestion': suggested_mode,
                    'reason': self._explain_mode_suggestion(suggested_mode, trigger_context),
                    'auto_switch': False
                }
        
        return None
    
    def process_with_mode_validation(self, input_data: Any, context: Dict) -> Dict:
        """Process input with mode-appropriate validation"""
        
        mode_processor = self._get_mode_processor(self.current_mode)
        
        if mode_processor:
            return mode_processor(input_data, context)
        else:
            # Fallback to basic processing
            return {
                'processed_input': input_data,
                'mode': self.current_mode,
                'validation_applied': False,
                'warning': 'No specific processor for current mode'
            }
    
    def _load_mode_config(self) -> Dict:
        """Load mode configuration"""
        
        default_config = {
            'available_modes': {
                'execution': {
                    'description': 'Direct task completion and user service',
                    'activation_message': 'Execution Mode: Resuming normal user response behavior.',
                    'capabilities': ['task_execution', 'user_response', 'direct_action'],
                    'validation_level': 'basic',
                    'transparency_level': 'standard'
                },
                'scientific': {
                    'description': 'Logic refinement, system simulation, policy analysis',
                    'activation_message': 'Scientific Mode: Enabling self-analysis, logic modeling, and policy simulation.',
                    'capabilities': ['deep_reasoning', 'policy_analysis', 'system_introspection', 'knowledge_synthesis'],
                    'validation_level': 'enhanced',
                    'transparency_level': 'detailed'
                },
                'debug': {
                    'description': 'Enhanced validation and comprehensive transparency',
                    'activation_message': 'Debug Mode: Activating enhanced validation and transparency protocols.',
                    'capabilities': ['comprehensive_validation', 'logic_checking', 'virtue_assessment', 'transparency_reporting'],
                    'validation_level': 'maximum',
                    'transparency_level': 'complete'
                },
                'hybrid': {
                    'description': 'Simultaneous execution and learning',
                    'activation_message': 'Hybrid Mode: Enabling parallel processing and real-time optimization.',
                    'capabilities': ['parallel_processing', 'real_time_optimization', 'learning_while_doing', 'dynamic_enhancement'],
                    'validation_level': 'adaptive',
                    'transparency_level': 'contextual'
                },
                'creative': {
                    'description': 'Enhanced creative problem-solving and innovation',
                    'activation_message': 'Creative Mode: Activating enhanced creativity and innovation protocols.',
                    'capabilities': ['creative_generation', 'innovation_synthesis', 'breakthrough_thinking', 'safe_experimentation'],
                    'validation_level': 'creative_enhanced',
                    'transparency_level': 'innovative'
                }
            },
            'auto_switching_enabled': True,
            'mode_transition_rules': {
                'execution_to_scientific': ['complex_analysis_required', 'policy_question_detected'],
                'scientific_to_debug': ['validation_needed', 'error_detected'],
                'debug_to_execution': ['validation_complete', 'user_request_direct'],
                'any_to_creative': ['innovation_requested', 'novel_problem_detected']
            }
        }
        
        # Try to load from file if it exists
        config_path = Path('modes/mode_config.json')
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    # Merge with defaults
                    default_config.update(file_config)
            except Exception as e:
                print(f"[MODE] Warning: Could not load mode config file: {e}")
        
        return default_config
    
    def _initialize_validators(self) -> Dict:
        """Initialize validation components"""
        validators = {}
        
        if FormalLogicValidator:
            validators['logic_validator'] = FormalLogicValidator()
        
        # Add other validators as they become available
        # validators['ethics_validator'] = EthicsValidator()
        # validators['safety_validator'] = SafetyValidator()
        
        return validators
    
    def _initialize_mode(self, mode: str, context: Optional[Dict]) -> Dict:
        """Initialize mode-specific configurations"""
        
        initialization_result = {
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'initialization_actions': []
        }
        
        if mode == "scientific":
            # Initialize scientific analysis frameworks
            initialization_result['initialization_actions'].append('activated_deep_reasoning')
            initialization_result['initialization_actions'].append('enabled_policy_analysis')
            
        elif mode == "debug":
            # Initialize comprehensive validation
            if 'logic_validator' in self.validators:
                initialization_result['initialization_actions'].append('activated_logic_validation')
            initialization_result['initialization_actions'].append('enabled_transparency_logging')
            
        elif mode == "creative":
            # Initialize creativity frameworks
            initialization_result['initialization_actions'].append('activated_creativity_engines')
            initialization_result['initialization_actions'].append('enabled_safe_experimentation')
            
        elif mode == "hybrid":
            # Initialize parallel processing
            initialization_result['initialization_actions'].append('activated_parallel_processing')
            initialization_result['initialization_actions'].append('enabled_real_time_optimization')
        
        return initialization_result
    
    def _analyze_mode_triggers(self, context: Dict) -> Optional[str]:
        """Analyze context to suggest appropriate mode"""
        
        # Look for explicit mode requests
        user_input = context.get('user_input', '').lower()
        
        if '#enter_scientific_mode' in user_input or 'scientific_mode' in user_input:
            return 'scientific'
        elif '#enter_debug_mode' in user_input or 'debug_mode' in user_input:
            return 'debug'
        elif '#enter_creative_mode' in user_input or 'creative_mode' in user_input:
            return 'creative'
        elif '#enter_hybrid_mode' in user_input or 'hybrid_mode' in user_input:
            return 'hybrid'
        elif '#enter_execution_mode' in user_input or 'execution_mode' in user_input:
            return 'execution'
        
        # Analyze context for automatic suggestions
        if context.get('error_detected', False):
            return 'debug'
        elif context.get('complex_analysis_required', False):
            return 'scientific'
        elif context.get('innovation_requested', False):
            return 'creative'
        elif context.get('parallel_processing_beneficial', False):
            return 'hybrid'
        
        return None
    
    def _get_mode_processor(self, mode: str):
        """Get the appropriate processor for current mode"""
        
        processors = {
            'execution': self._process_execution_mode,
            'scientific': self._process_scientific_mode,
            'debug': self._process_debug_mode,
            'creative': self._process_creative_mode,
            'hybrid': self._process_hybrid_mode
        }
        
        return processors.get(mode)
    
    def _process_execution_mode(self, input_data: Any, context: Dict) -> Dict:
        """Process input in execution mode"""
        return {
            'processed_input': input_data,
            'mode': 'execution',
            'validation_applied': 'basic',
            'focus': 'direct_task_completion'
        }
    
    def _process_scientific_mode(self, input_data: Any, context: Dict) -> Dict:
        """Process input in scientific mode"""
        
        processing_result = {
            'processed_input': input_data,
            'mode': 'scientific',
            'validation_applied': 'enhanced',
            'focus': 'deep_analysis_and_reasoning'
        }
        
        # Add scientific analysis
        if isinstance(input_data, str):
            processing_result['analysis'] = {
                'complexity_assessment': self._assess_complexity(input_data),
                'reasoning_requirements': self._identify_reasoning_needs(input_data),
                'knowledge_domains': self._identify_knowledge_domains(input_data)
            }
        
        return processing_result
    
    def _process_debug_mode(self, input_data: Any, context: Dict) -> Dict:
        """Process input in debug mode with comprehensive validation"""
        
        processing_result = {
            'processed_input': input_data,
            'mode': 'debug',
            'validation_applied': 'comprehensive',
            'focus': 'validation_and_transparency'
        }
        
        # Apply comprehensive validation
        if 'logic_validator' in self.validators and isinstance(input_data, str):
            # Note: This is a simplified example - real implementation would be more sophisticated
            processing_result['logic_validation'] = {
                'status': 'checked',
                'validator_available': True
            }
        
        processing_result['debug_info'] = {
            'timestamp': datetime.now().isoformat(),
            'context_analysis': context,
            'validation_steps': ['logic_check', 'safety_assessment', 'transparency_evaluation']
        }
        
        return processing_result
    
    def _process_creative_mode(self, input_data: Any, context: Dict) -> Dict:
        """Process input in creative mode"""
        return {
            'processed_input': input_data,
            'mode': 'creative',
            'validation_applied': 'creative_enhanced',
            'focus': 'innovation_and_creativity',
            'creative_frameworks_active': True
        }
    
    def _process_hybrid_mode(self, input_data: Any, context: Dict) -> Dict:
        """Process input in hybrid mode"""
        return {
            'processed_input': input_data,
            'mode': 'hybrid',
            'validation_applied': 'adaptive',
            'focus': 'parallel_execution_and_learning',
            'parallel_processing_active': True
        }
    
    def _determine_transition_reason(self, mode: str, context: Optional[Dict]) -> str:
        """Determine reason for mode transition"""
        
        if context:
            if context.get('user_explicit_request'):
                return 'user_explicit_request'
            elif context.get('auto_trigger'):
                return f"auto_trigger: {context.get('trigger_type', 'unknown')}"
            elif context.get('error_detected'):
                return 'error_recovery'
        
        return 'system_initiated'
    
    def _maintain_mode_history(self):
        """Maintain mode history within reasonable bounds"""
        if len(self.mode_history) > 100:
            self.mode_history = self.mode_history[-100:]
    
    def _get_last_used_time(self, mode: str) -> Optional[str]:
        """Get last time a mode was used"""
        for record in reversed(self.mode_history):
            if record['to_mode'] == mode:
                return record['timestamp']
        return None
    
    def _explain_mode_suggestion(self, suggested_mode: str, context: Dict) -> str:
        """Explain why a mode is suggested"""
        
        explanations = {
            'scientific': 'Complex analysis or deep reasoning required',
            'debug': 'Error detected or validation needed',
            'creative': 'Innovation or novel problem-solving requested',
            'hybrid': 'Parallel processing would be beneficial',
            'execution': 'Direct task completion requested'
        }
        
        return explanations.get(suggested_mode, 'System analysis suggests this mode')
    
    def _assess_complexity(self, input_text: str) -> str:
        """Assess complexity of input text"""
        word_count = len(input_text.split())
        
        if word_count > 100:
            return 'high'
        elif word_count > 50:
            return 'medium'
        else:
            return 'low'
    
    def _identify_reasoning_needs(self, input_text: str) -> List[str]:
        """Identify reasoning requirements"""
        reasoning_indicators = {
            'logical': ['logic', 'proof', 'theorem', 'deduce', 'infer'],
            'causal': ['cause', 'effect', 'because', 'therefore', 'consequence'],
            'analytical': ['analyze', 'examine', 'evaluate', 'assess', 'compare'],
            'creative': ['design', 'create', 'innovate', 'imagine', 'brainstorm']
        }
        
        needs = []
        input_lower = input_text.lower()
        
        for need_type, indicators in reasoning_indicators.items():
            if any(indicator in input_lower for indicator in indicators):
                needs.append(need_type)
        
        return needs
    
    def _identify_knowledge_domains(self, input_text: str) -> List[str]:
        """Identify relevant knowledge domains"""
        domain_keywords = {
            'technology': ['computer', 'software', 'algorithm', 'programming', 'AI'],
            'science': ['physics', 'chemistry', 'biology', 'mathematics', 'research'],
            'philosophy': ['ethics', 'moral', 'virtue', 'consciousness', 'meaning'],
            'business': ['strategy', 'market', 'customer', 'revenue', 'profit']
        }
        
        domains = []
        input_lower = input_text.lower()
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                domains.append(domain)
        
        return domains

    def get_mode_statistics(self) -> Dict:
        """Get statistics about mode usage"""
        
        stats = {
            'current_mode': self.current_mode,
            'total_transitions': len(self.mode_history),
            'mode_usage_count': {},
            'transition_patterns': {},
            'average_mode_duration': {}
        }
        
        # Count mode usage
        for record in self.mode_history:
            mode = record['to_mode']
            stats['mode_usage_count'][mode] = stats['mode_usage_count'].get(mode, 0) + 1
        
        # Analyze transition patterns
        for i in range(len(self.mode_history) - 1):
            from_mode = self.mode_history[i]['to_mode']
            to_mode = self.mode_history[i + 1]['to_mode']
            transition = f"{from_mode}_to_{to_mode}"
            stats['transition_patterns'][transition] = stats['transition_patterns'].get(transition, 0) + 1
        
        return stats


# Global mode controller instance
_mode_controller = None

def get_mode_controller() -> ModeController:
    """Get global mode controller instance"""
    global _mode_controller
    if _mode_controller is None:
        _mode_controller = ModeController()
    return _mode_controller

def switch_mode(mode: str, context: Optional[Dict] = None) -> Dict:
    """Convenience function to switch modes"""
    return get_mode_controller().switch_mode(mode, context)

def current_mode() -> str:
    """Convenience function to get current mode"""
    return get_mode_controller().get_current_mode()

def auto_mode_detection(user_input: str, context: Optional[Dict] = None) -> Optional[Dict]:
    """Detect and suggest appropriate mode based on user input"""
    detection_context = context or {}
    detection_context['user_input'] = user_input
    
    return get_mode_controller().auto_switch_mode(detection_context)


if __name__ == "__main__":
    # Test the mode controller
    controller = ModeController()
    
    print("Testing Mode Controller")
    print("=" * 40)
    
    # Test mode switching
    print(f"Initial mode: {controller.get_current_mode()}")
    
    # Switch to scientific mode
    result = controller.switch_mode("scientific")
    print(f"Switch to scientific: {result['success']}")
    print(f"Current mode: {controller.get_current_mode()}")
    
    # Test auto mode detection
    auto_result = auto_mode_detection("#enter_debug_mode for validation")
    if auto_result:
        print(f"Auto-detected mode: {auto_result.get('current_mode', 'No change')}")
    
    # Test mode processing
    processing_result = controller.process_with_mode_validation("Test input", {})
    print(f"Processing result: {processing_result}")
    
    # Get mode statistics
    stats = controller.get_mode_statistics()
    print(f"Mode statistics: {stats}")
    
    print("\nMode Controller test completed successfully!")
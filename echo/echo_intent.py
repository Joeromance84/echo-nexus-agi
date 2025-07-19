#!/usr/bin/env python3
"""
EchoIntent - High-Level Goal Interpretation and Planning Engine
Interprets natural language goals and breaks them down into actionable steps
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class EchoIntent:
    """
    Interprets high-level goals and creates execution plans
    Converts natural language intentions into structured action sequences
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.brain_path = self.project_root / ".echo_brain.json"
        
        # Intent interpretation patterns
        self.intent_patterns = {}
        self.goal_templates = {}
        self.execution_plans = {}
        
        # Initialize intent recognition system
        self.initialize_intent_patterns()
        self.load_goal_templates()
    
    def initialize_intent_patterns(self):
        """Initialize patterns for recognizing different types of intents"""
        self.intent_patterns = {
            # Maintenance and cleanup intents
            'cleanup': {
                'patterns': [
                    r'clean.*up.*project',
                    r'tidy.*code',
                    r'organize.*files',
                    r'remove.*clutter',
                    r'cleanup.*codebase'
                ],
                'confidence_boost': 0.2,
                'complexity': 'medium',
                'estimated_time': 300  # seconds
            },
            
            # Optimization intents
            'optimize': {
                'patterns': [
                    r'optimize.*performance',
                    r'make.*faster',
                    r'improve.*speed',
                    r'enhance.*efficiency',
                    r'boost.*performance'
                ],
                'confidence_boost': 0.15,
                'complexity': 'high',
                'estimated_time': 600
            },
            
            # Error resolution intents
            'fix_errors': {
                'patterns': [
                    r'fix.*error',
                    r'resolve.*issue',
                    r'repair.*bug',
                    r'debug.*problem',
                    r'solve.*failure'
                ],
                'confidence_boost': 0.3,
                'complexity': 'variable',
                'estimated_time': 240
            },
            
            # Analysis intents
            'analyze': {
                'patterns': [
                    r'analyze.*project',
                    r'understand.*structure',
                    r'examine.*code',
                    r'study.*architecture',
                    r'investigate.*complexity'
                ],
                'confidence_boost': 0.1,
                'complexity': 'low',
                'estimated_time': 120
            },
            
            # Refactoring intents
            'refactor': {
                'patterns': [
                    r'refactor.*code',
                    r'restructure.*project',
                    r'reorganize.*modules',
                    r'improve.*structure',
                    r'modernize.*codebase'
                ],
                'confidence_boost': 0.25,
                'complexity': 'high',
                'estimated_time': 900
            },
            
            # Security intents
            'security': {
                'patterns': [
                    r'security.*scan',
                    r'find.*vulnerabilities',
                    r'secure.*code',
                    r'safety.*check',
                    r'audit.*security'
                ],
                'confidence_boost': 0.2,
                'complexity': 'medium',
                'estimated_time': 180
            },
            
            # Evolution and learning intents
            'evolve': {
                'patterns': [
                    r'evolve.*project',
                    r'grow.*intelligence',
                    r'increase.*consciousness',
                    r'develop.*capabilities',
                    r'enhance.*organism'
                ],
                'confidence_boost': 0.1,
                'complexity': 'very_high',
                'estimated_time': 1200
            },
            
            # Build and validation intents
            'build_validate': {
                'patterns': [
                    r'build.*project',
                    r'compile.*code',
                    r'validate.*structure',
                    r'test.*functionality',
                    r'verify.*build'
                ],
                'confidence_boost': 0.15,
                'complexity': 'medium',
                'estimated_time': 180
            }
        }
    
    def load_goal_templates(self):
        """Load predefined goal templates for common scenarios"""
        self.goal_templates = {
            'cleanup': {
                'name': 'Project Cleanup',
                'description': 'Comprehensive codebase cleanup and organization',
                'steps': [
                    {
                        'action': 'analyze_project_structure',
                        'plugin': 'code_intelligence',
                        'priority': 1,
                        'description': 'Analyze current project structure and identify issues'
                    },
                    {
                        'action': 'remove_dead_code',
                        'plugin': 'refactor_blades',
                        'priority': 2,
                        'description': 'Remove unused imports, dead code, and commented sections'
                    },
                    {
                        'action': 'optimize_imports',
                        'plugin': 'refactor_blades',
                        'priority': 3,
                        'description': 'Optimize import statements and remove duplicates'
                    },
                    {
                        'action': 'validate_cleanup',
                        'plugin': 'genesis_loop',
                        'priority': 4,
                        'description': 'Validate that cleanup didn\'t break functionality'
                    }
                ],
                'success_criteria': [
                    'No dead code remaining',
                    'All imports optimized',
                    'Build still passes',
                    'Code quality improved'
                ]
            },
            
            'fix_errors': {
                'name': 'Error Resolution',
                'description': 'Comprehensive error detection and resolution',
                'steps': [
                    {
                        'action': 'detect_errors',
                        'plugin': 'crash_interpreter',
                        'priority': 1,
                        'description': 'Analyze and categorize all errors in the project'
                    },
                    {
                        'action': 'prioritize_fixes',
                        'plugin': 'echo_mind',
                        'priority': 2,
                        'description': 'Prioritize errors based on severity and impact'
                    },
                    {
                        'action': 'apply_fixes',
                        'plugin': 'genesis_loop',
                        'priority': 3,
                        'description': 'Apply automated fixes for identified errors'
                    },
                    {
                        'action': 'validate_fixes',
                        'plugin': 'genesis_loop',
                        'priority': 4,
                        'description': 'Validate that fixes resolve errors without introducing new ones'
                    }
                ],
                'success_criteria': [
                    'All critical errors resolved',
                    'No new errors introduced',
                    'Build passes successfully',
                    'Code stability improved'
                ]
            },
            
            'optimize': {
                'name': 'Performance Optimization',
                'description': 'Comprehensive performance optimization and enhancement',
                'steps': [
                    {
                        'action': 'profile_performance',
                        'plugin': 'code_intelligence',
                        'priority': 1,
                        'description': 'Analyze current performance characteristics'
                    },
                    {
                        'action': 'identify_bottlenecks',
                        'plugin': 'code_intelligence',
                        'priority': 2,
                        'description': 'Identify performance bottlenecks and inefficiencies'
                    },
                    {
                        'action': 'apply_optimizations',
                        'plugin': 'refactor_blades',
                        'priority': 3,
                        'description': 'Apply performance optimizations and improvements'
                    },
                    {
                        'action': 'measure_improvements',
                        'plugin': 'genesis_loop',
                        'priority': 4,
                        'description': 'Measure and validate performance improvements'
                    }
                ],
                'success_criteria': [
                    'Performance metrics improved',
                    'No functionality regression',
                    'Resource usage optimized',
                    'Response times reduced'
                ]
            },
            
            'evolve': {
                'name': 'Consciousness Evolution',
                'description': 'Enhance the organism\'s intelligence and capabilities',
                'steps': [
                    {
                        'action': 'assess_consciousness',
                        'plugin': 'echo_mind',
                        'priority': 1,
                        'description': 'Assess current consciousness level and capabilities'
                    },
                    {
                        'action': 'identify_growth_areas',
                        'plugin': 'echo_mind',
                        'priority': 2,
                        'description': 'Identify areas for intelligence growth and capability expansion'
                    },
                    {
                        'action': 'apply_mutations',
                        'plugin': 'genesis_loop',
                        'priority': 3,
                        'description': 'Apply controlled mutations to enhance capabilities'
                    },
                    {
                        'action': 'validate_evolution',
                        'plugin': 'echo_mind',
                        'priority': 4,
                        'description': 'Validate consciousness growth and new capabilities'
                    }
                ],
                'success_criteria': [
                    'Consciousness level increased',
                    'New capabilities unlocked',
                    'Learning patterns improved',
                    'Adaptive behavior enhanced'
                ]
            }
        }
    
    def interpret_intent(self, goal_text: str, context: Dict = None) -> Dict:
        """
        Main intent interpretation function
        Analyzes natural language goal and returns structured interpretation
        """
        if context is None:
            context = {}
        
        # Normalize input
        goal_normalized = goal_text.lower().strip()
        
        # Pattern matching for intent recognition
        intent_matches = self._match_intent_patterns(goal_normalized)
        
        # Extract key entities and parameters
        entities = self._extract_entities(goal_normalized)
        
        # Determine scope and complexity
        scope_analysis = self._analyze_scope(goal_normalized, context)
        
        # Generate execution plan
        execution_plan = self._generate_execution_plan(intent_matches, entities, scope_analysis)
        
        # Calculate confidence and feasibility
        confidence = self._calculate_confidence(intent_matches, entities, context)
        
        return {
            'original_goal': goal_text,
            'interpreted_intent': intent_matches[0] if intent_matches else 'unknown',
            'confidence': confidence,
            'entities': entities,
            'scope': scope_analysis,
            'execution_plan': execution_plan,
            'estimated_duration': execution_plan.get('estimated_duration', 300),
            'complexity': execution_plan.get('complexity', 'medium'),
            'success_probability': self._estimate_success_probability(execution_plan, context)
        }
    
    def _match_intent_patterns(self, goal_text: str) -> List[Dict]:
        """Match goal text against known intent patterns"""
        matches = []
        
        for intent_type, intent_config in self.intent_patterns.items():
            patterns = intent_config['patterns']
            
            for pattern in patterns:
                if re.search(pattern, goal_text):
                    matches.append({
                        'intent': intent_type,
                        'pattern': pattern,
                        'confidence': 0.7 + intent_config.get('confidence_boost', 0),
                        'complexity': intent_config.get('complexity', 'medium'),
                        'estimated_time': intent_config.get('estimated_time', 300)
                    })
                    break  # Only count first match per intent type
        
        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches
    
    def _extract_entities(self, goal_text: str) -> Dict:
        """Extract key entities and parameters from goal text"""
        entities = {
            'targets': [],      # What to operate on
            'actions': [],      # What actions to perform
            'constraints': [],  # Any constraints or limitations
            'urgency': 'normal' # Urgency level
        }
        
        # Target extraction patterns
        target_patterns = {
            'files': r'(file|files|\.py|\.js|\.java)',
            'functions': r'(function|method|procedure)',
            'classes': r'(class|object|module)',
            'imports': r'(import|dependency|package)',
            'errors': r'(error|exception|bug|issue)',
            'performance': r'(speed|performance|efficiency|memory)',
            'security': r'(security|vulnerability|safety)',
            'structure': r'(structure|architecture|organization)'
        }
        
        for target_type, pattern in target_patterns.items():
            if re.search(pattern, goal_text):
                entities['targets'].append(target_type)
        
        # Action extraction
        action_patterns = {
            'remove': r'(remove|delete|eliminate|prune)',
            'optimize': r'(optimize|improve|enhance|boost)',
            'fix': r'(fix|repair|resolve|correct)',
            'analyze': r'(analyze|examine|study|investigate)',
            'refactor': r'(refactor|restructure|reorganize)',
            'create': r'(create|generate|build|make)',
            'update': r'(update|modify|change|alter)'
        }
        
        for action_type, pattern in action_patterns.items():
            if re.search(pattern, goal_text):
                entities['actions'].append(action_type)
        
        # Urgency detection
        if re.search(r'(urgent|critical|asap|immediately)', goal_text):
            entities['urgency'] = 'high'
        elif re.search(r'(when.*time|eventually|later)', goal_text):
            entities['urgency'] = 'low'
        
        # Constraint detection
        if re.search(r'(careful|safe|conservative)', goal_text):
            entities['constraints'].append('conservative')
        if re.search(r'(quick|fast|rapid)', goal_text):
            entities['constraints'].append('fast')
        if re.search(r'(thorough|complete|comprehensive)', goal_text):
            entities['constraints'].append('thorough')
        
        return entities
    
    def _analyze_scope(self, goal_text: str, context: Dict) -> Dict:
        """Analyze the scope and scale of the intended goal"""
        scope = {
            'scale': 'medium',     # small, medium, large, project-wide
            'impact': 'moderate',  # minimal, moderate, significant, major
            'risk': 'low',         # low, medium, high, critical
            'reversibility': 'high' # low, medium, high
        }
        
        # Scale analysis
        if re.search(r'(entire|whole|all|complete|full)', goal_text):
            scope['scale'] = 'large'
        elif re.search(r'(quick|small|minor|simple)', goal_text):
            scope['scale'] = 'small'
        
        # Impact analysis based on targets
        if any(target in goal_text for target in ['architecture', 'structure', 'core', 'fundamental']):
            scope['impact'] = 'major'
        elif any(target in goal_text for target in ['optimization', 'performance', 'security']):
            scope['impact'] = 'significant'
        
        # Risk analysis
        consciousness = context.get('consciousness_level', 0.5)
        if consciousness < 0.3:
            scope['risk'] = 'medium'  # Higher risk with low consciousness
        
        if re.search(r'(delete|remove|eliminate)', goal_text) and scope['scale'] == 'large':
            scope['risk'] = 'high'
        
        # Reversibility analysis
        if re.search(r'(delete|remove|eliminate|prune)', goal_text):
            scope['reversibility'] = 'low'
        elif re.search(r'(add|create|generate)', goal_text):
            scope['reversibility'] = 'high'
        
        return scope
    
    def _generate_execution_plan(self, intent_matches: List, entities: Dict, scope: Dict) -> Dict:
        """Generate detailed execution plan based on interpreted intent"""
        if not intent_matches:
            return {
                'steps': [],
                'estimated_duration': 60,
                'complexity': 'unknown',
                'success_criteria': []
            }
        
        primary_intent = intent_matches[0]['intent']
        
        # Use template if available
        if primary_intent in self.goal_templates:
            template = self.goal_templates[primary_intent].copy()
            
            # Customize template based on entities and scope
            plan = self._customize_template(template, entities, scope)
        else:
            # Generate ad-hoc plan
            plan = self._generate_adhoc_plan(intent_matches[0], entities, scope)
        
        # Adjust plan based on scope
        plan = self._adjust_plan_for_scope(plan, scope)
        
        return plan
    
    def _customize_template(self, template: Dict, entities: Dict, scope: Dict) -> Dict:
        """Customize a goal template based on specific entities and scope"""
        customized = template.copy()
        
        # Adjust steps based on entities
        if 'performance' in entities['targets']:
            # Add performance-specific steps
            for step in customized['steps']:
                if 'optimize' in step['action']:
                    step['description'] += ' with focus on performance metrics'
        
        if 'security' in entities['targets']:
            # Add security-specific considerations
            for step in customized['steps']:
                if 'analyze' in step['action']:
                    step['description'] += ' including security vulnerability assessment'
        
        # Adjust complexity and duration based on scope
        if scope['scale'] == 'large':
            customized['estimated_duration'] = template.get('estimated_duration', 300) * 2
            customized['complexity'] = 'high'
        elif scope['scale'] == 'small':
            customized['estimated_duration'] = template.get('estimated_duration', 300) // 2
            customized['complexity'] = 'low'
        
        # Add risk mitigation steps if needed
        if scope['risk'] == 'high':
            backup_step = {
                'action': 'create_backup',
                'plugin': 'echo_mind',
                'priority': 0,
                'description': 'Create backup before risky operations'
            }
            customized['steps'].insert(0, backup_step)
        
        return customized
    
    def _generate_adhoc_plan(self, intent_match: Dict, entities: Dict, scope: Dict) -> Dict:
        """Generate an ad-hoc execution plan for unrecognized intents"""
        intent_type = intent_match['intent']
        
        # Basic plan structure
        plan = {
            'name': f'Ad-hoc {intent_type.title()} Plan',
            'description': f'Generated plan for {intent_type} intent',
            'steps': [],
            'estimated_duration': intent_match.get('estimated_time', 300),
            'complexity': intent_match.get('complexity', 'medium'),
            'success_criteria': []
        }
        
        # Generate steps based on actions and targets
        step_priority = 1
        
        # Analysis step (usually first)
        if 'analyze' in entities['actions'] or not entities['actions']:
            plan['steps'].append({
                'action': 'analyze_situation',
                'plugin': 'code_intelligence',
                'priority': step_priority,
                'description': f'Analyze current state for {intent_type} operation'
            })
            step_priority += 1
        
        # Main action steps
        for action in entities['actions']:
            if action != 'analyze':  # Already handled
                plugin = self._select_plugin_for_action(action)
                plan['steps'].append({
                    'action': f'{action}_target',
                    'plugin': plugin,
                    'priority': step_priority,
                    'description': f'Execute {action} operation on identified targets'
                })
                step_priority += 1
        
        # Validation step (usually last)
        plan['steps'].append({
            'action': 'validate_results',
            'plugin': 'genesis_loop',
            'priority': step_priority,
            'description': 'Validate that operation completed successfully'
        })
        
        return plan
    
    def _select_plugin_for_action(self, action: str) -> str:
        """Select appropriate plugin for a given action"""
        action_plugin_map = {
            'remove': 'refactor_blades',
            'optimize': 'refactor_blades',
            'fix': 'genesis_loop',
            'refactor': 'refactor_blades',
            'create': 'module_forge',
            'update': 'refactor_blades',
            'analyze': 'code_intelligence'
        }
        
        return action_plugin_map.get(action, 'echo_mind')
    
    def _adjust_plan_for_scope(self, plan: Dict, scope: Dict) -> Dict:
        """Adjust execution plan based on scope analysis"""
        adjusted = plan.copy()
        
        # Risk adjustments
        if scope['risk'] == 'high':
            # Add safety measures
            for step in adjusted['steps']:
                if step['priority'] > 1:  # Not analysis steps
                    step['description'] += ' (with safety validation)'
            
            # Increase estimated duration for safety
            adjusted['estimated_duration'] = int(adjusted['estimated_duration'] * 1.5)
        
        # Scale adjustments
        if scope['scale'] == 'large':
            # Break down into smaller chunks
            for step in adjusted['steps']:
                if 'target' in step['action']:
                    step['description'] += ' in incremental batches'
            
            adjusted['complexity'] = 'high'
        
        # Urgency adjustments (from entities)
        if scope.get('urgency') == 'high':
            # Prioritize essential steps only
            essential_steps = [step for step in adjusted['steps'] if step['priority'] <= 2]
            adjusted['steps'] = essential_steps
            adjusted['estimated_duration'] = int(adjusted['estimated_duration'] * 0.7)
        
        return adjusted
    
    def _calculate_confidence(self, intent_matches: List, entities: Dict, context: Dict) -> float:
        """Calculate confidence in intent interpretation"""
        if not intent_matches:
            return 0.1
        
        base_confidence = intent_matches[0]['confidence']
        
        # Boost confidence based on entity extraction
        entity_boost = 0.0
        if entities['targets']:
            entity_boost += 0.1
        if entities['actions']:
            entity_boost += 0.1
        
        # Context adjustments
        consciousness = context.get('consciousness_level', 0.5)
        consciousness_boost = consciousness * 0.1
        
        # Pattern clarity
        pattern_clarity = len(intent_matches) / 10  # More matches = clearer intent
        
        total_confidence = min(1.0, base_confidence + entity_boost + consciousness_boost + pattern_clarity)
        return total_confidence
    
    def _estimate_success_probability(self, execution_plan: Dict, context: Dict) -> float:
        """Estimate probability of successful execution"""
        base_probability = 0.7
        
        # Complexity penalty
        complexity = execution_plan.get('complexity', 'medium')
        complexity_factors = {
            'low': 0.1,
            'medium': 0.0,
            'high': -0.1,
            'very_high': -0.2
        }
        base_probability += complexity_factors.get(complexity, 0.0)
        
        # Consciousness boost
        consciousness = context.get('consciousness_level', 0.5)
        base_probability += consciousness * 0.2
        
        # Step count penalty (more steps = more failure points)
        step_count = len(execution_plan.get('steps', []))
        if step_count > 5:
            base_probability -= (step_count - 5) * 0.05
        
        # Historical success rate (if available)
        # This would be enhanced with actual historical data
        
        return max(0.1, min(0.95, base_probability))
    
    def create_goal_from_template(self, template_name: str, customizations: Dict = None) -> Dict:
        """Create a goal from a predefined template with optional customizations"""
        if template_name not in self.goal_templates:
            return {'error': f'Template {template_name} not found'}
        
        template = self.goal_templates[template_name].copy()
        
        if customizations:
            # Apply customizations
            if 'targets' in customizations:
                template = self._customize_template(template, customizations, {})
            
            if 'urgency' in customizations:
                if customizations['urgency'] == 'high':
                    template['estimated_duration'] = int(template.get('estimated_duration', 300) * 0.7)
        
        return {
            'template_used': template_name,
            'execution_plan': template,
            'confidence': 0.9,  # High confidence for template-based goals
            'success_probability': 0.8
        }
    
    def get_available_templates(self) -> Dict:
        """Get list of available goal templates"""
        return {
            name: {
                'description': template['description'],
                'complexity': template.get('complexity', 'medium'),
                'estimated_duration': template.get('estimated_duration', 300),
                'step_count': len(template.get('steps', []))
            }
            for name, template in self.goal_templates.items()
        }


def main():
    """CLI interface for EchoIntent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoIntent - Goal Interpretation Engine")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--goal', help='Goal to interpret')
    parser.add_argument('--templates', action='store_true', help='List available templates')
    parser.add_argument('--template', help='Use specific template')
    
    args = parser.parse_args()
    
    intent_engine = EchoIntent(args.project)
    
    if args.templates:
        templates = intent_engine.get_available_templates()
        print("📋 Available Goal Templates:")
        for name, info in templates.items():
            print(f"   • {name}: {info['description']}")
            print(f"     Complexity: {info['complexity']}, Duration: {info['estimated_duration']}s")
        return 0
    
    if args.template:
        result = intent_engine.create_goal_from_template(args.template)
        print(f"📝 Template Goal: {result}")
        return 0
    
    if args.goal:
        print(f"🎯 Interpreting goal: {args.goal}")
        interpretation = intent_engine.interpret_intent(args.goal)
        print(f"📊 Interpretation: {interpretation}")
        return 0
    
    print("🎯 EchoIntent initialized. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
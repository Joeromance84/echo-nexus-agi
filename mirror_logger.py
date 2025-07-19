"""
Mirror Logger - Observational Learning System for AGI
Logs everything to learn from developer behavior patterns
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
import hashlib

class MirrorLogger:
    def __init__(self):
        self.history_file = "mirror_learning_history.json"
        self.history = self.load_history()
        self.session_observations = []
    
    def load_history(self) -> List[Dict]:
        """Load learning history from persistent storage"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self):
        """Save learning history to persistent storage"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def observe(self, input_text: str, response_text: str, context_snapshot: Dict[str, Any], outcome: str = None):
        """Core observation function - logs everything the AGI should learn from"""
        observation = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'response': response_text,
            'context': context_snapshot,
            'outcome': outcome,
            'session_id': self._get_session_id(),
            'observation_id': self._generate_observation_id(input_text, response_text)
        }
        
        self.history.append(observation)
        self.session_observations.append(observation)
        self.save_history()
        
        return observation['observation_id']
    
    def observe_developer_action(self, action: str, thought_process: str, context: str, timing: float, success: bool):
        """Observe developer actions to learn from"""
        return self.observe(
            input_text=f"DEVELOPER_ACTION: {action}",
            response_text=f"THOUGHT: {thought_process}",
            context_snapshot={
                'action_context': context,
                'timing_seconds': timing,
                'success': success,
                'action_type': 'developer_behavior'
            },
            outcome='success' if success else 'failure'
        )
    
    def observe_code_pattern(self, original_code: str, fixed_code: str, problem_description: str):
        """Learn from code correction patterns"""
        return self.observe(
            input_text=f"CODE_PROBLEM: {problem_description}",
            response_text=f"CODE_FIX: Applied correction",
            context_snapshot={
                'original_code': original_code,
                'fixed_code': fixed_code,
                'problem_type': problem_description,
                'action_type': 'code_correction'
            },
            outcome='code_learned'
        )
    
    def observe_workflow_sequence(self, sequence_steps: List[str], context: str, success: bool):
        """Learn workflow sequences from developer"""
        return self.observe(
            input_text=f"WORKFLOW_SEQUENCE: {' -> '.join(sequence_steps)}",
            response_text=f"LEARNED_SEQUENCE: {len(sequence_steps)} steps",
            context_snapshot={
                'workflow_steps': sequence_steps,
                'workflow_context': context,
                'sequence_length': len(sequence_steps),
                'action_type': 'workflow_learning'
            },
            outcome='success' if success else 'failure'
        )
    
    def get_similar_observations(self, context_keywords: List[str], limit: int = 5) -> List[Dict]:
        """Find similar past observations for pattern matching"""
        similar = []
        
        for obs in self.history:
            # Check if any keywords match in input, context, or response
            text_to_search = f"{obs['input']} {obs['response']} {str(obs.get('context', {}))}"
            
            matches = sum(1 for keyword in context_keywords if keyword.lower() in text_to_search.lower())
            
            if matches > 0:
                obs_copy = obs.copy()
                obs_copy['relevance_score'] = matches / len(context_keywords)
                similar.append(obs_copy)
        
        # Sort by relevance and return top results
        similar.sort(key=lambda x: x['relevance_score'], reverse=True)
        return similar[:limit]
    
    def get_learning_patterns(self) -> Dict[str, Any]:
        """Extract learning patterns from observations"""
        patterns = {
            'successful_sequences': [],
            'failed_patterns': [],
            'code_corrections': [],
            'developer_behaviors': [],
            'timing_patterns': {}
        }
        
        for obs in self.history:
            context = obs.get('context', {})
            action_type = context.get('action_type', 'unknown')
            
            if action_type == 'developer_behavior' and obs.get('outcome') == 'success':
                patterns['developer_behaviors'].append({
                    'action': obs['input'],
                    'thought': obs['response'],
                    'timing': context.get('timing_seconds', 0),
                    'context': context.get('action_context', '')
                })
            
            elif action_type == 'code_correction':
                patterns['code_corrections'].append({
                    'problem': obs['input'],
                    'solution': context.get('fixed_code', ''),
                    'original': context.get('original_code', '')
                })
            
            elif action_type == 'workflow_learning' and obs.get('outcome') == 'success':
                patterns['successful_sequences'].append({
                    'steps': context.get('workflow_steps', []),
                    'context': context.get('workflow_context', '')
                })
        
        return patterns
    
    def _get_session_id(self) -> str:
        """Generate session ID based on timestamp"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _generate_observation_id(self, input_text: str, response_text: str) -> str:
        """Generate unique observation ID"""
        content = f"{input_text}_{response_text}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:8]

class MimicryModule:
    def __init__(self, mirror_logger: MirrorLogger):
        self.mirror_logger = mirror_logger
        self.learned_patterns = {}
    
    def analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """Analyze code structure for mimicry"""
        structure = {
            'imports': [],
            'functions': [],
            'classes': [],
            'comments': [],
            'patterns': []
        }
        
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('import ') or stripped.startswith('from '):
                structure['imports'].append(stripped)
            elif stripped.startswith('def '):
                structure['functions'].append(stripped)
            elif stripped.startswith('class '):
                structure['classes'].append(stripped)
            elif stripped.startswith('#'):
                structure['comments'].append(stripped)
        
        return structure
    
    def mimic_style(self, example_code: str, new_goal: str) -> str:
        """Generate code that mimics the style of example code"""
        structure = self.analyze_code_structure(example_code)
        
        # Learn from similar patterns in mirror logger
        similar_obs = self.mirror_logger.get_similar_observations(['code', 'function', 'class'])
        
        # Generate code in similar style
        mimicked_code = f"""# Generated code mimicking learned patterns
# Goal: {new_goal}

"""
        
        # Add similar import patterns
        if structure['imports']:
            for imp in structure['imports'][:3]:  # Limit to avoid clutter
                mimicked_code += f"{imp}\n"
            mimicked_code += "\n"
        
        # Add function structure based on learned patterns
        mimicked_code += f"""def execute_{new_goal.lower().replace(' ', '_')}():
    \"\"\"
    Mimicking learned developer patterns for: {new_goal}
    \"\"\"
    # Pattern learned from developer observations
    result = {{'success': False, 'actions': [], 'learning_applied': True}}
    
    try:
        # Execute goal using learned patterns
        pass
        result['success'] = True
    except Exception as e:
        result['error'] = str(e)
    
    return result
"""
        
        return mimicked_code
    
    def self_evaluate(self, original: str, mimic: str) -> Dict[str, Any]:
        """Evaluate mimicry quality"""
        orig_structure = self.analyze_code_structure(original)
        mimic_structure = self.analyze_code_structure(mimic)
        
        # Calculate similarity scores
        import_similarity = len(set(orig_structure['imports']) & set(mimic_structure['imports'])) / max(len(orig_structure['imports']), 1)
        function_similarity = len(orig_structure['functions']) == len(mimic_structure['functions'])
        
        overall_score = (import_similarity + (1.0 if function_similarity else 0.0)) / 2.0
        
        return {
            'similarity_score': overall_score,
            'import_match': import_similarity,
            'structure_match': function_similarity,
            'recommendations': self._get_improvement_recommendations(orig_structure, mimic_structure)
        }
    
    def _get_improvement_recommendations(self, original: Dict, mimic: Dict) -> List[str]:
        """Get recommendations for improving mimicry"""
        recommendations = []
        
        if len(mimic['imports']) < len(original['imports']):
            recommendations.append("Add more imports to match original structure")
        
        if len(mimic['functions']) != len(original['functions']):
            recommendations.append("Adjust number of functions to match original")
        
        if len(mimic['comments']) < len(original['comments']):
            recommendations.append("Add more comments to match documentation style")
        
        return recommendations

class HumanInteractionTracker:
    def __init__(self, mirror_logger: MirrorLogger):
        self.mirror_logger = mirror_logger
        self.learned_patterns = []
        self.user_profiles = {}
    
    def log_feedback(self, original_code: str, human_fix: str, feedback_type: str = "correction"):
        """Log human feedback for learning"""
        self.learned_patterns.append({
            'timestamp': datetime.now().isoformat(),
            'original_code': original_code,
            'human_fix': human_fix,
            'feedback_type': feedback_type
        })
        
        # Also log in mirror logger
        self.mirror_logger.observe_code_pattern(original_code, human_fix, f"human_{feedback_type}")
    
    def log_preference(self, user_id: str, preference_type: str, preference_value: str):
        """Log user preferences for personalized mimicry"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        self.user_profiles[user_id][preference_type] = preference_value
        
        # Log in mirror logger
        self.mirror_logger.observe(
            input_text=f"USER_PREFERENCE: {preference_type}",
            response_text=f"PREFERENCE_VALUE: {preference_value}",
            context_snapshot={
                'user_id': user_id,
                'preference_type': preference_type,
                'preference_value': preference_value,
                'action_type': 'user_preference'
            },
            outcome='learned'
        )
    
    def get_user_style_profile(self, user_id: str) -> Dict[str, Any]:
        """Get learned style profile for a user"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        return {
            'coding_style': 'adaptive',
            'comment_preference': 'moderate',
            'verbosity': 'balanced'
        }

class GhostHandsMode:
    def __init__(self, mirror_logger: MirrorLogger, confidence_threshold: float = 0.7):
        self.mirror_logger = mirror_logger
        self.confidence_threshold = confidence_threshold
        self.shadow_observations = []
        self.suggestion_ready = False
    
    def shadow_activity(self, action: str, context: str):
        """Shadow developer activity without acting"""
        observation = {
            'timestamp': datetime.now().isoformat(),
            'shadowed_action': action,
            'context': context,
            'confidence': self._calculate_confidence(action, context)
        }
        
        self.shadow_observations.append(observation)
        
        # Check if ready to suggest
        if observation['confidence'] >= self.confidence_threshold:
            self.suggestion_ready = True
        
        return observation
    
    def get_suggestions(self) -> List[Dict[str, Any]]:
        """Get suggestions when confidence threshold is met"""
        if not self.suggestion_ready:
            return []
        
        high_confidence_observations = [
            obs for obs in self.shadow_observations
            if obs['confidence'] >= self.confidence_threshold
        ]
        
        suggestions = []
        for obs in high_confidence_observations[-3:]:  # Last 3 high-confidence observations
            similar_patterns = self.mirror_logger.get_similar_observations([obs['shadowed_action']])
            
            if similar_patterns:
                suggestions.append({
                    'action': obs['shadowed_action'],
                    'confidence': obs['confidence'],
                    'learned_from': f"{len(similar_patterns)} similar patterns",
                    'context': obs['context']
                })
        
        return suggestions
    
    def _calculate_confidence(self, action: str, context: str) -> float:
        """Calculate confidence based on learned patterns"""
        similar_obs = self.mirror_logger.get_similar_observations([action, context])
        
        if not similar_obs:
            return 0.0
        
        successful_similar = [obs for obs in similar_obs if obs.get('outcome') == 'success']
        return len(successful_similar) / len(similar_obs)
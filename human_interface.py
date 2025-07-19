"""
Human Interface - Learning from Human Feedback and Corrections
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from mirror_logger import MirrorLogger

class StyleProfile:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.preferences = {
            'coding_style': 'adaptive',
            'indentation': 'spaces',
            'indent_size': 4,
            'line_length': 80,
            'comment_density': 'moderate',
            'naming_convention': 'snake_case',
            'error_handling': 'explicit',
            'docstring_style': 'google',
            'type_hints': True,
            'complexity_preference': 'simple'
        }
        self.learned_patterns = []
        self.correction_history = []
    
    def update_preference(self, preference_type: str, value: Any):
        """Update a specific preference"""
        self.preferences[preference_type] = value
        self.learned_patterns.append({
            'timestamp': datetime.now().isoformat(),
            'preference_type': preference_type,
            'new_value': value,
            'source': 'explicit_feedback'
        })
    
    def learn_from_correction(self, original: str, corrected: str, context: str):
        """Learn preferences from code corrections"""
        correction = {
            'timestamp': datetime.now().isoformat(),
            'original_code': original,
            'corrected_code': corrected,
            'context': context,
            'inferred_preferences': self._infer_preferences(original, corrected)
        }
        
        self.correction_history.append(correction)
        
        # Update preferences based on corrections
        for pref_type, pref_value in correction['inferred_preferences'].items():
            if pref_type in self.preferences:
                self.preferences[pref_type] = pref_value
    
    def _infer_preferences(self, original: str, corrected: str) -> Dict[str, Any]:
        """Infer preferences from code corrections"""
        inferences = {}
        
        # Analyze indentation changes
        orig_lines = original.split('\n')
        corr_lines = corrected.split('\n')
        
        for orig_line, corr_line in zip(orig_lines, corr_lines):
            if orig_line.strip() == corr_line.strip() and orig_line != corr_line:
                # Only whitespace changed
                if '\t' in corr_line and ' ' * 4 in orig_line:
                    inferences['indentation'] = 'tabs'
                elif ' ' * 2 in corr_line and ' ' * 4 in orig_line:
                    inferences['indent_size'] = 2
        
        # Analyze comment additions
        orig_comment_count = original.count('#')
        corr_comment_count = corrected.count('#')
        
        if corr_comment_count > orig_comment_count:
            inferences['comment_density'] = 'high'
        elif corr_comment_count < orig_comment_count:
            inferences['comment_density'] = 'low'
        
        # Analyze error handling additions
        if 'try:' in corrected and 'try:' not in original:
            inferences['error_handling'] = 'explicit'
        
        # Analyze type hint additions
        if '->' in corrected and '->' not in original:
            inferences['type_hints'] = True
        
        return inferences
    
    def get_style_recommendations(self) -> Dict[str, Any]:
        """Get code generation recommendations based on learned style"""
        return {
            'indentation': self.preferences['indentation'],
            'indent_size': self.preferences['indent_size'],
            'max_line_length': self.preferences['line_length'],
            'add_comments': self.preferences['comment_density'] in ['moderate', 'high'],
            'use_type_hints': self.preferences['type_hints'],
            'include_error_handling': self.preferences['error_handling'] == 'explicit',
            'docstring_format': self.preferences['docstring_style']
        }

class HumanInteractionTracker:
    def __init__(self, mirror_logger: MirrorLogger):
        self.mirror_logger = mirror_logger
        self.learned_patterns = []
        self.user_profiles = {}
        self.feedback_history = []
        self.correction_patterns = {}
        self.interaction_file = "human_interactions.json"
        self.load_interaction_history()
    
    def load_interaction_history(self):
        """Load previous interaction history"""
        if os.path.exists(self.interaction_file):
            try:
                with open(self.interaction_file, 'r') as f:
                    data = json.load(f)
                    self.learned_patterns = data.get('learned_patterns', [])
                    self.feedback_history = data.get('feedback_history', [])
                    self.correction_patterns = data.get('correction_patterns', {})
                    
                    # Reconstruct user profiles
                    for user_id, profile_data in data.get('user_profiles', {}).items():
                        profile = StyleProfile(user_id)
                        profile.preferences = profile_data.get('preferences', profile.preferences)
                        profile.learned_patterns = profile_data.get('learned_patterns', [])
                        profile.correction_history = profile_data.get('correction_history', [])
                        self.user_profiles[user_id] = profile
            except:
                pass
    
    def save_interaction_history(self):
        """Save interaction history to file"""
        data = {
            'learned_patterns': self.learned_patterns,
            'feedback_history': self.feedback_history,
            'correction_patterns': self.correction_patterns,
            'user_profiles': {
                user_id: {
                    'preferences': profile.preferences,
                    'learned_patterns': profile.learned_patterns,
                    'correction_history': profile.correction_history
                }
                for user_id, profile in self.user_profiles.items()
            }
        }
        
        with open(self.interaction_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_user_profile(self, user_id: str) -> StyleProfile:
        """Get or create user style profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = StyleProfile(user_id)
        return self.user_profiles[user_id]
    
    def log_feedback(self, original_code: str, human_fix: str, feedback_type: str = "correction", user_id: str = "default"):
        """Log human feedback for learning"""
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'original_code': original_code,
            'human_fix': human_fix,
            'feedback_type': feedback_type,
            'user_id': user_id,
            'feedback_id': self._generate_feedback_id()
        }
        
        self.feedback_history.append(feedback_entry)
        self.learned_patterns.append({
            'error': original_code,
            'fix': human_fix,
            'type': feedback_type,
            'user': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update user profile
        user_profile = self.get_user_profile(user_id)
        user_profile.learn_from_correction(original_code, human_fix, feedback_type)
        
        # Analyze correction patterns
        self._analyze_correction_pattern(original_code, human_fix, feedback_type)
        
        # Log in mirror logger
        self.mirror_logger.observe_code_pattern(original_code, human_fix, f"human_{feedback_type}")
        
        self.save_interaction_history()
        return feedback_entry['feedback_id']
    
    def log_rejection(self, suggested_code: str, reason: str, user_id: str = "default"):
        """Log when human rejects AI suggestion"""
        rejection_entry = {
            'timestamp': datetime.now().isoformat(),
            'suggested_code': suggested_code,
            'rejection_reason': reason,
            'user_id': user_id,
            'type': 'rejection'
        }
        
        self.feedback_history.append(rejection_entry)
        
        # Learn from rejection
        user_profile = self.get_user_profile(user_id)
        self._learn_from_rejection(suggested_code, reason, user_profile)
        
        # Log in mirror logger
        self.mirror_logger.observe(
            input_text=f"AI_SUGGESTION_REJECTED: {reason}",
            response_text=f"REJECTED_CODE: {len(suggested_code)} characters",
            context_snapshot={
                'suggested_code': suggested_code,
                'rejection_reason': reason,
                'user_id': user_id,
                'action_type': 'suggestion_rejection'
            },
            outcome='rejected'
        )
        
        self.save_interaction_history()
    
    def log_approval(self, suggested_code: str, user_id: str = "default"):
        """Log when human approves AI suggestion"""
        approval_entry = {
            'timestamp': datetime.now().isoformat(),
            'suggested_code': suggested_code,
            'user_id': user_id,
            'type': 'approval'
        }
        
        self.feedback_history.append(approval_entry)
        
        # Positive reinforcement
        self.mirror_logger.observe(
            input_text="AI_SUGGESTION_APPROVED",
            response_text=f"APPROVED_CODE: {len(suggested_code)} characters",
            context_snapshot={
                'suggested_code': suggested_code,
                'user_id': user_id,
                'action_type': 'suggestion_approval'
            },
            outcome='approved'
        )
        
        self.save_interaction_history()
    
    def log_preference(self, user_id: str, preference_type: str, preference_value: str):
        """Log explicit user preference"""
        user_profile = self.get_user_profile(user_id)
        user_profile.update_preference(preference_type, preference_value)
        
        # Log in mirror logger
        self.mirror_logger.observe(
            input_text=f"USER_PREFERENCE: {preference_type}",
            response_text=f"PREFERENCE_VALUE: {preference_value}",
            context_snapshot={
                'user_id': user_id,
                'preference_type': preference_type,
                'preference_value': preference_value,
                'action_type': 'explicit_preference'
            },
            outcome='learned'
        )
        
        self.save_interaction_history()
    
    def get_personalized_recommendations(self, user_id: str, context: str) -> Dict[str, Any]:
        """Get personalized recommendations for a user"""
        user_profile = self.get_user_profile(user_id)
        
        recommendations = {
            'style_preferences': user_profile.get_style_recommendations(),
            'learned_patterns': self._get_user_patterns(user_id),
            'context_specific': self._get_context_recommendations(user_id, context),
            'confidence': self._calculate_recommendation_confidence(user_id)
        }
        
        return recommendations
    
    def get_correction_insights(self) -> Dict[str, Any]:
        """Get insights from correction patterns"""
        insights = {
            'common_mistakes': [],
            'frequent_corrections': [],
            'user_trends': {},
            'improvement_areas': []
        }
        
        # Analyze common correction patterns
        correction_types = {}
        for pattern in self.learned_patterns:
            correction_type = self._categorize_correction(pattern['error'], pattern['fix'])
            correction_types[correction_type] = correction_types.get(correction_type, 0) + 1
        
        # Sort by frequency
        sorted_corrections = sorted(correction_types.items(), key=lambda x: x[1], reverse=True)
        insights['frequent_corrections'] = sorted_corrections[:5]
        
        # User-specific trends
        for user_id, profile in self.user_profiles.items():
            user_corrections = len(profile.correction_history)
            if user_corrections > 0:
                insights['user_trends'][user_id] = {
                    'total_corrections': user_corrections,
                    'recent_corrections': len([c for c in profile.correction_history 
                                             if self._is_recent(c['timestamp'])]),
                    'preferences': profile.preferences
                }
        
        return insights
    
    def _analyze_correction_pattern(self, original: str, corrected: str, feedback_type: str):
        """Analyze and store correction patterns"""
        pattern_key = self._generate_pattern_key(original, corrected)
        
        if pattern_key not in self.correction_patterns:
            self.correction_patterns[pattern_key] = {
                'count': 0,
                'examples': [],
                'categories': []
            }
        
        self.correction_patterns[pattern_key]['count'] += 1
        self.correction_patterns[pattern_key]['examples'].append({
            'original': original[:100],  # Truncate for storage
            'corrected': corrected[:100],
            'feedback_type': feedback_type,
            'timestamp': datetime.now().isoformat()
        })
        
        category = self._categorize_correction(original, corrected)
        if category not in self.correction_patterns[pattern_key]['categories']:
            self.correction_patterns[pattern_key]['categories'].append(category)
    
    def _learn_from_rejection(self, suggested_code: str, reason: str, user_profile: StyleProfile):
        """Learn from suggestion rejections"""
        # Analyze why the suggestion was rejected
        if 'too complex' in reason.lower():
            user_profile.update_preference('complexity_preference', 'simple')
        elif 'too simple' in reason.lower():
            user_profile.update_preference('complexity_preference', 'detailed')
        elif 'wrong style' in reason.lower():
            # Could trigger a style analysis request
            pass
        elif 'missing comments' in reason.lower():
            user_profile.update_preference('comment_density', 'high')
        elif 'too many comments' in reason.lower():
            user_profile.update_preference('comment_density', 'low')
    
    def _get_user_patterns(self, user_id: str) -> List[Dict]:
        """Get learned patterns for a specific user"""
        return [pattern for pattern in self.learned_patterns if pattern.get('user') == user_id]
    
    def _get_context_recommendations(self, user_id: str, context: str) -> Dict[str, Any]:
        """Get context-specific recommendations"""
        user_patterns = self._get_user_patterns(user_id)
        
        context_patterns = [
            pattern for pattern in user_patterns
            if context.lower() in pattern.get('fix', '').lower() or
               context.lower() in pattern.get('error', '').lower()
        ]
        
        recommendations = {}
        if context_patterns:
            # Find most common patterns in this context
            recent_patterns = sorted(context_patterns, key=lambda x: x['timestamp'], reverse=True)[:3]
            recommendations['recent_context_patterns'] = recent_patterns
        
        return recommendations
    
    def _calculate_recommendation_confidence(self, user_id: str) -> float:
        """Calculate confidence in recommendations for a user"""
        user_profile = self.get_user_profile(user_id)
        
        # Base confidence on number of interactions
        interaction_count = len(user_profile.correction_history) + len(user_profile.learned_patterns)
        
        # Confidence grows with interactions but plateaus
        confidence = min(interaction_count / 10.0, 0.9)
        
        return confidence
    
    def _categorize_correction(self, original: str, corrected: str) -> str:
        """Categorize the type of correction"""
        if len(corrected) > len(original) * 1.5:
            return 'code_expansion'
        elif len(corrected) < len(original) * 0.7:
            return 'code_simplification'
        elif original.count('#') < corrected.count('#'):
            return 'comment_addition'
        elif 'try:' in corrected and 'try:' not in original:
            return 'error_handling_addition'
        elif '->' in corrected and '->' not in original:
            return 'type_hint_addition'
        elif original.replace(' ', '') == corrected.replace(' ', ''):
            return 'formatting_change'
        else:
            return 'logic_modification'
    
    def _generate_pattern_key(self, original: str, corrected: str) -> str:
        """Generate a key for pattern matching"""
        import hashlib
        content = f"{original[:50]}_{corrected[:50]}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _generate_feedback_id(self) -> str:
        """Generate unique feedback ID"""
        import hashlib
        content = f"feedback_{datetime.now().isoformat()}_{len(self.feedback_history)}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """Check if timestamp is within recent days"""
        try:
            from datetime import datetime, timedelta
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return datetime.now() - ts < timedelta(days=days)
        except:
            return False
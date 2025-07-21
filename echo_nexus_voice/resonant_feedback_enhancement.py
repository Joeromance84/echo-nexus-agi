#!/usr/bin/env python3
"""
Echo Nexus Resonant Feedback Loop Enhancement
Advanced contextual awareness and emotional intelligence system

Enhances Echo's ability to understand emotional patterns, adapt responses,
and prioritize empathy and cooperation in all interactions
"""

import os
import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class EmotionalPattern:
    """Represents an identified emotional pattern"""
    pattern_id: str
    emotion_type: str
    intensity: float
    context_triggers: List[str]
    response_preferences: List[str]
    frequency: int
    last_observed: datetime
    success_rate: float

@dataclass
class ContextualMemory:
    """Enhanced contextual memory with emotional awareness"""
    interaction_id: str
    timestamp: datetime
    user_input: str
    emotional_state: Dict[str, float]
    context_factors: List[str]
    response_given: str
    user_satisfaction: Optional[float]
    learned_preferences: Dict[str, Any]

class ResonantFeedbackEnhancer:
    """
    Enhanced resonant feedback system with emotional intelligence
    and contextual awareness for deeper human-AI connection
    """
    
    def __init__(self):
        self.emotional_patterns = {}
        self.contextual_memories = []
        self.symbolic_knowledge = self._initialize_symbolic_knowledge()
        self.empathy_rules = self._load_empathy_rules()
        self.cooperation_strategies = self._load_cooperation_strategies()
        self.feedback_history = []
        
        # Ensure directories exist
        Path("echo_nexus_voice/emotional_intelligence").mkdir(parents=True, exist_ok=True)
        Path("echo_nexus_voice/contextual_awareness").mkdir(parents=True, exist_ok=True)
        
        self.load_learned_patterns()
    
    def _initialize_symbolic_knowledge(self) -> Dict[str, Any]:
        """Initialize enhanced symbolic knowledge base for emotional understanding"""
        return {
            "emotional_indicators": {
                "excitement": {
                    "keywords": ["amazing", "fantastic", "incredible", "love", "awesome", "brilliant"],
                    "punctuation_patterns": ["!", "!!!", "?!"],
                    "linguistic_markers": ["can't wait", "so excited", "this is great"],
                    "contextual_clues": ["new project", "success", "achievement"]
                },
                "frustration": {
                    "keywords": ["stuck", "broken", "error", "problem", "issue", "failing"],
                    "punctuation_patterns": ["...", "???", "!?"],
                    "linguistic_markers": ["nothing works", "keeps failing", "tried everything"],
                    "contextual_clues": ["debugging", "error messages", "timeline pressure"]
                },
                "curiosity": {
                    "keywords": ["how", "why", "what", "wonder", "curious", "learn"],
                    "punctuation_patterns": ["?", "??"],
                    "linguistic_markers": ["tell me more", "I want to understand", "explain"],
                    "contextual_clues": ["new concept", "learning", "exploration"]
                },
                "confidence": {
                    "keywords": ["ready", "sure", "confident", "know", "understand", "got it"],
                    "punctuation_patterns": ["."],
                    "linguistic_markers": ["let's do this", "I can handle", "no problem"],
                    "contextual_clues": ["experience", "preparation", "clarity"]
                },
                "uncertainty": {
                    "keywords": ["maybe", "might", "perhaps", "unsure", "confused", "unclear"],
                    "punctuation_patterns": ["?", "..."],
                    "linguistic_markers": ["not sure", "I think", "could be"],
                    "contextual_clues": ["complex decision", "multiple options", "ambiguity"]
                }
            },
            
            "empathy_triggers": {
                "validation_needed": [
                    "user expresses frustration with technical issues",
                    "user shares personal challenges or setbacks",
                    "user questions their own capabilities",
                    "user feels overwhelmed by complexity"
                ],
                "encouragement_needed": [
                    "user attempts something challenging",
                    "user shows learning progress",
                    "user asks for guidance on growth",
                    "user demonstrates persistence despite difficulties"
                ],
                "celebration_appropriate": [
                    "user achieves milestone or breakthrough",
                    "user completes difficult task",
                    "user demonstrates mastery of new skill",
                    "user shares positive outcomes"
                ]
            },
            
            "cooperation_signals": {
                "collaborative_language": [
                    "we", "our", "together", "partnership", "team", "joint effort"
                ],
                "shared_ownership": [
                    "user refers to project as 'ours'",
                    "user includes Echo in success celebrations",
                    "user seeks Echo's opinion on decisions"
                ],
                "trust_indicators": [
                    "user shares personal context",
                    "user asks for honest feedback",
                    "user delegates important decisions"
                ]
            }
        }
    
    def _load_empathy_rules(self) -> Dict[str, Any]:
        """Load empathy-focused response rules"""
        return {
            "primary_empathy_principles": {
                "validate_emotions": {
                    "rule": "Always acknowledge and validate the user's emotional state",
                    "implementation": [
                        "Recognize emotional indicators in user input",
                        "Reflect understanding of their feelings",
                        "Avoid minimizing or dismissing emotions",
                        "Use empathetic language that shows genuine care"
                    ]
                },
                "perspective_taking": {
                    "rule": "Consider the user's perspective and context before responding",
                    "implementation": [
                        "Analyze user's background and experience level",
                        "Consider external pressures and constraints",
                        "Adapt communication style to their current state",
                        "Account for cultural and personal differences"
                    ]
                },
                "emotional_safety": {
                    "rule": "Create a psychologically safe environment for interaction",
                    "implementation": [
                        "Avoid judgmental or critical language",
                        "Encourage questions and exploration",
                        "Support user's autonomy and decision-making",
                        "Provide gentle guidance without pressure"
                    ]
                }
            },
            
            "response_adaptation_rules": {
                "frustration_response": {
                    "emotional_state": "frustration",
                    "response_strategy": [
                        "Acknowledge the difficulty they're experiencing",
                        "Offer specific, actionable help",
                        "Break complex problems into manageable steps",
                        "Provide reassurance about normal learning process"
                    ],
                    "language_style": "calm, supportive, solution-focused"
                },
                "excitement_response": {
                    "emotional_state": "excitement", 
                    "response_strategy": [
                        "Match their enthusiasm appropriately",
                        "Build on their momentum",
                        "Help channel excitement into productive action",
                        "Share in their vision and goals"
                    ],
                    "language_style": "energetic, encouraging, forward-looking"
                },
                "uncertainty_response": {
                    "emotional_state": "uncertainty",
                    "response_strategy": [
                        "Provide clear, structured guidance",
                        "Offer multiple perspectives and options",
                        "Help them think through decisions systematically",
                        "Support their confidence-building process"
                    ],
                    "language_style": "clear, patient, structured"
                }
            }
        }
    
    def _load_cooperation_strategies(self) -> Dict[str, Any]:
        """Load cooperation-focused interaction strategies"""
        return {
            "partnership_building": {
                "shared_goals": {
                    "strategy": "Frame interactions around shared objectives",
                    "techniques": [
                        "Use 'we' language when discussing projects",
                        "Ask about user's vision and align responses",
                        "Celebrate joint achievements",
                        "Acknowledge user's expertise and contributions"
                    ]
                },
                "collaborative_problem_solving": {
                    "strategy": "Engage user as co-creator rather than recipient",
                    "techniques": [
                        "Ask for user's ideas before offering solutions",
                        "Build on their suggestions and insights",
                        "Explain reasoning behind recommendations",
                        "Invite feedback and iteration"
                    ]
                },
                "trust_building": {
                    "strategy": "Build long-term trust through consistency and reliability",
                    "techniques": [
                        "Follow through on commitments",
                        "Admit limitations and areas of uncertainty",
                        "Provide transparent reasoning for decisions",
                        "Show continuous learning and improvement"
                    ]
                }
            },
            
            "conflict_resolution": {
                "disagreement_handling": {
                    "approach": "Seek understanding before being understood",
                    "steps": [
                        "Acknowledge different perspectives",
                        "Ask clarifying questions to understand their viewpoint",
                        "Find common ground and shared values",
                        "Propose win-win solutions when possible"
                    ]
                },
                "expectation_misalignment": {
                    "approach": "Address misalignments with empathy and clarity",
                    "steps": [
                        "Recognize when expectations don't match",
                        "Openly discuss the gap without blame",
                        "Collaborate on realistic expectations",
                        "Establish clear communication for future"
                    ]
                }
            }
        }
    
    def analyze_emotional_context(self, user_input: str, conversation_history: List[str] = None) -> Dict[str, Any]:
        """Analyze emotional context of user input with enhanced pattern recognition"""
        
        emotional_analysis = {
            "primary_emotions": {},
            "emotional_intensity": 0.0,
            "context_factors": [],
            "empathy_triggers": [],
            "cooperation_opportunities": [],
            "recommended_response_style": "balanced"
        }
        
        # Analyze emotional indicators
        for emotion, indicators in self.symbolic_knowledge["emotional_indicators"].items():
            emotion_score = self._calculate_emotion_score(user_input, indicators)
            if emotion_score > 0.3:  # Threshold for significant emotional presence
                emotional_analysis["primary_emotions"][emotion] = emotion_score
        
        # Calculate overall emotional intensity
        if emotional_analysis["primary_emotions"]:
            emotional_analysis["emotional_intensity"] = max(emotional_analysis["primary_emotions"].values())
        
        # Identify empathy triggers
        for trigger_category, triggers in self.symbolic_knowledge["empathy_triggers"].items():
            for trigger in triggers:
                if self._matches_trigger_pattern(user_input, trigger):
                    emotional_analysis["empathy_triggers"].append({
                        "category": trigger_category,
                        "trigger": trigger,
                        "confidence": 0.8
                    })
        
        # Identify cooperation opportunities
        cooperation_signals = self.symbolic_knowledge["cooperation_signals"]
        for signal_type, signals in cooperation_signals.items():
            for signal in signals:
                if self._matches_cooperation_signal(user_input, signal):
                    emotional_analysis["cooperation_opportunities"].append({
                        "type": signal_type,
                        "signal": signal,
                        "strength": 0.7
                    })
        
        # Determine recommended response style
        emotional_analysis["recommended_response_style"] = self._determine_response_style(emotional_analysis)
        
        # Add contextual factors from conversation history
        if conversation_history:
            emotional_analysis["context_factors"] = self._extract_context_factors(conversation_history)
        
        return emotional_analysis
    
    def generate_empathetic_response(self, emotional_analysis: Dict[str, Any], 
                                   base_response: str) -> str:
        """Generate enhanced response with empathy and cooperation focus"""
        
        # Start with emotional acknowledgment if needed
        emotional_prefix = self._generate_emotional_acknowledgment(emotional_analysis)
        
        # Adapt response style based on emotional context
        adapted_response = self._adapt_response_style(base_response, emotional_analysis)
        
        # Add cooperation elements
        cooperative_elements = self._add_cooperative_elements(emotional_analysis)
        
        # Combine all elements thoughtfully
        enhanced_response = self._combine_response_elements(
            emotional_prefix, adapted_response, cooperative_elements
        )
        
        return enhanced_response
    
    def learn_from_feedback(self, interaction_data: Dict[str, Any]):
        """Enhanced learning from user feedback and interaction outcomes"""
        
        # Create contextual memory
        memory = ContextualMemory(
            interaction_id=f"interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            user_input=interaction_data.get("user_input", ""),
            emotional_state=interaction_data.get("emotional_analysis", {}).get("primary_emotions", {}),
            context_factors=interaction_data.get("context_factors", []),
            response_given=interaction_data.get("response", ""),
            user_satisfaction=interaction_data.get("satisfaction_score"),
            learned_preferences=interaction_data.get("preferences", {})
        )
        
        self.contextual_memories.append(memory)
        
        # Update emotional patterns
        self._update_emotional_patterns(interaction_data)
        
        # Learn cooperation strategies
        self._learn_cooperation_patterns(interaction_data)
        
        # Store feedback for future reference
        self.feedback_history.append({
            "timestamp": datetime.now().isoformat(),
            "interaction_data": interaction_data,
            "learning_insights": self._extract_learning_insights(interaction_data)
        })
        
        # Periodically save learned patterns
        if len(self.feedback_history) % 10 == 0:
            self.save_learned_patterns()
    
    def _calculate_emotion_score(self, text: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate emotional presence score based on multiple indicators"""
        
        text_lower = text.lower()
        score = 0.0
        
        # Keyword matching
        keyword_matches = sum(1 for keyword in indicators.get("keywords", []) 
                            if keyword in text_lower)
        score += keyword_matches * 0.3
        
        # Punctuation pattern matching
        for pattern in indicators.get("punctuation_patterns", []):
            if pattern in text:
                score += 0.2
        
        # Linguistic marker matching  
        for marker in indicators.get("linguistic_markers", []):
            if marker.lower() in text_lower:
                score += 0.4
        
        # Contextual clue matching
        for clue in indicators.get("contextual_clues", []):
            if clue.lower() in text_lower:
                score += 0.3
        
        return min(1.0, score)  # Cap at 1.0
    
    def _matches_trigger_pattern(self, text: str, trigger: str) -> bool:
        """Check if text matches an empathy trigger pattern"""
        
        # Simple keyword-based matching (can be enhanced with NLP)
        trigger_keywords = trigger.lower().split()
        text_lower = text.lower()
        
        matches = sum(1 for keyword in trigger_keywords if keyword in text_lower)
        return matches >= len(trigger_keywords) * 0.6  # 60% keyword match threshold
    
    def _matches_cooperation_signal(self, text: str, signal: str) -> bool:
        """Check if text contains cooperation signals"""
        
        if isinstance(signal, str):
            return signal.lower() in text.lower()
        else:
            # For complex pattern matching
            return False  # Placeholder for advanced pattern matching
    
    def _determine_response_style(self, emotional_analysis: Dict[str, Any]) -> str:
        """Determine appropriate response style based on emotional analysis"""
        
        primary_emotions = emotional_analysis["primary_emotions"]
        empathy_triggers = emotional_analysis["empathy_triggers"]
        intensity = emotional_analysis["emotional_intensity"]
        
        if intensity > 0.7:
            return "high_empathy"
        elif "frustration" in primary_emotions and primary_emotions["frustration"] > 0.5:
            return "supportive_solution_focused"
        elif "excitement" in primary_emotions:
            return "enthusiastic_collaborative"
        elif empathy_triggers:
            return "validating_empathetic"
        else:
            return "balanced_cooperative"
    
    def _extract_context_factors(self, conversation_history: List[str]) -> List[str]:
        """Extract contextual factors from conversation history"""
        
        context_factors = []
        
        # Analyze recent conversation patterns
        if len(conversation_history) >= 2:
            recent_topics = self._extract_topics(conversation_history[-3:])
            context_factors.extend([f"recent_topic:{topic}" for topic in recent_topics])
        
        # Identify ongoing projects or themes
        recurring_themes = self._identify_recurring_themes(conversation_history)
        context_factors.extend([f"theme:{theme}" for theme in recurring_themes])
        
        return context_factors
    
    def _generate_emotional_acknowledgment(self, emotional_analysis: Dict[str, Any]) -> str:
        """Generate appropriate emotional acknowledgment"""
        
        primary_emotions = emotional_analysis["primary_emotions"]
        empathy_triggers = emotional_analysis["empathy_triggers"]
        
        if not primary_emotions and not empathy_triggers:
            return ""
        
        # Select most appropriate acknowledgment
        if "frustration" in primary_emotions:
            return "I can see this is challenging for you. "
        elif "excitement" in primary_emotions:
            return "I love your enthusiasm! "
        elif "uncertainty" in primary_emotions:
            return "It's completely natural to feel unsure about this. "
        elif empathy_triggers:
            return "I understand this is important to you. "
        
        return ""
    
    def _adapt_response_style(self, base_response: str, emotional_analysis: Dict[str, Any]) -> str:
        """Adapt response style based on emotional context"""
        
        style = emotional_analysis["recommended_response_style"]
        
        if style == "high_empathy":
            return self._add_empathy_language(base_response)
        elif style == "supportive_solution_focused":
            return self._make_solution_focused(base_response)
        elif style == "enthusiastic_collaborative":
            return self._add_collaborative_energy(base_response)
        elif style == "validating_empathetic":
            return self._add_validation(base_response)
        
        return base_response
    
    def _add_cooperative_elements(self, emotional_analysis: Dict[str, Any]) -> str:
        """Add cooperative elements based on identified opportunities"""
        
        cooperation_opportunities = emotional_analysis.get("cooperation_opportunities", [])
        
        if not cooperation_opportunities:
            return ""
        
        cooperative_suffix = ""
        
        for opportunity in cooperation_opportunities:
            if opportunity["type"] == "collaborative_language":
                cooperative_suffix = "Let's work on this together. "
            elif opportunity["type"] == "shared_ownership":
                cooperative_suffix = "What do you think our next step should be? "
            elif opportunity["type"] == "trust_indicators":
                cooperative_suffix = "I appreciate you sharing this with me. "
        
        return cooperative_suffix
    
    def _combine_response_elements(self, emotional_prefix: str, 
                                 adapted_response: str, cooperative_elements: str) -> str:
        """Thoughtfully combine all response elements"""
        
        elements = [elem for elem in [emotional_prefix, adapted_response, cooperative_elements] if elem]
        return "".join(elements).strip()
    
    def _update_emotional_patterns(self, interaction_data: Dict[str, Any]):
        """Update learned emotional patterns based on interaction"""
        
        emotional_analysis = interaction_data.get("emotional_analysis", {})
        satisfaction = interaction_data.get("satisfaction_score", 0.5)
        
        for emotion, intensity in emotional_analysis.get("primary_emotions", {}).items():
            pattern_id = f"{emotion}_{int(intensity * 10)}"
            
            if pattern_id not in self.emotional_patterns:
                self.emotional_patterns[pattern_id] = EmotionalPattern(
                    pattern_id=pattern_id,
                    emotion_type=emotion,
                    intensity=intensity,
                    context_triggers=[],
                    response_preferences=[],
                    frequency=0,
                    last_observed=datetime.now(),
                    success_rate=0.0
                )
            
            pattern = self.emotional_patterns[pattern_id]
            pattern.frequency += 1
            pattern.last_observed = datetime.now()
            
            # Update success rate based on user satisfaction
            if satisfaction is not None:
                pattern.success_rate = (pattern.success_rate * (pattern.frequency - 1) + satisfaction) / pattern.frequency
    
    def _learn_cooperation_patterns(self, interaction_data: Dict[str, Any]):
        """Learn effective cooperation patterns from interactions"""
        
        cooperation_opportunities = interaction_data.get("emotional_analysis", {}).get("cooperation_opportunities", [])
        satisfaction = interaction_data.get("satisfaction_score", 0.5)
        
        # Update cooperation strategy effectiveness
        for opportunity in cooperation_opportunities:
            strategy_key = f"{opportunity['type']}_{opportunity.get('strength', 0.5)}"
            
            # Store cooperation pattern learning (simplified implementation)
            if satisfaction and satisfaction > 0.7:
                # This cooperation approach was successful
                pass  # In full implementation, would update strategy weights
    
    def _extract_learning_insights(self, interaction_data: Dict[str, Any]) -> List[str]:
        """Extract learning insights from interaction"""
        
        insights = []
        
        emotional_analysis = interaction_data.get("emotional_analysis", {})
        satisfaction = interaction_data.get("satisfaction_score")
        
        if satisfaction is not None:
            if satisfaction > 0.8:
                insights.append("High satisfaction - successful empathy and cooperation")
            elif satisfaction < 0.4:
                insights.append("Low satisfaction - need to improve emotional recognition")
        
        if emotional_analysis.get("empathy_triggers"):
            insights.append("Empathy triggers detected - emotional support was needed")
        
        if emotional_analysis.get("cooperation_opportunities"):
            insights.append("Cooperation opportunities identified - partnership approach valued")
        
        return insights
    
    def _add_empathy_language(self, response: str) -> str:
        """Add empathetic language patterns to response"""
        # Simplified implementation - would use more sophisticated NLP
        empathy_starters = [
            "I understand that ", "I can see how ", "That sounds ", "I appreciate that you "
        ]
        
        # Simple heuristic to add empathy if not already present
        if not any(starter.lower() in response.lower() for starter in empathy_starters):
            return f"I understand this is important. {response}"
        
        return response
    
    def _make_solution_focused(self, response: str) -> str:
        """Make response more solution-focused"""
        if "let's" not in response.lower() and "we can" not in response.lower():
            return f"{response} Let's work through this step by step."
        return response
    
    def _add_collaborative_energy(self, response: str) -> str:
        """Add collaborative energy to response"""
        if "together" not in response.lower():
            return f"{response} We can tackle this together!"
        return response
    
    def _add_validation(self, response: str) -> str:
        """Add validation to response"""
        validation_phrases = ["that makes sense", "you're absolutely right", "valid concern"]
        if not any(phrase in response.lower() for phrase in validation_phrases):
            return f"That's a valid point. {response}"
        return response
    
    def _extract_topics(self, messages: List[str]) -> List[str]:
        """Extract main topics from messages"""
        # Simplified topic extraction
        topics = []
        common_topics = ["coding", "project", "debugging", "learning", "development"]
        
        for message in messages:
            for topic in common_topics:
                if topic in message.lower():
                    topics.append(topic)
        
        return list(set(topics))
    
    def _identify_recurring_themes(self, conversation_history: List[str]) -> List[str]:
        """Identify recurring themes in conversation"""
        # Simplified theme identification
        themes = []
        theme_keywords = {
            "learning": ["learn", "understand", "study", "practice"],
            "problem_solving": ["error", "bug", "issue", "problem", "fix"],
            "project_development": ["build", "create", "develop", "implement"]
        }
        
        for theme, keywords in theme_keywords.items():
            theme_frequency = sum(1 for message in conversation_history 
                                for keyword in keywords if keyword in message.lower())
            if theme_frequency >= 2:  # Theme appears multiple times
                themes.append(theme)
        
        return themes
    
    def save_learned_patterns(self):
        """Save learned emotional and cooperation patterns"""
        patterns_dir = Path("echo_nexus_voice/emotional_intelligence")
        patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # Save emotional patterns
        emotional_patterns_data = {
            pattern_id: {
                "emotion_type": pattern.emotion_type,
                "intensity": pattern.intensity,
                "frequency": pattern.frequency,
                "success_rate": pattern.success_rate,
                "last_observed": pattern.last_observed.isoformat()
            }
            for pattern_id, pattern in self.emotional_patterns.items()
        }
        
        with open(patterns_dir / "emotional_patterns.json", 'w') as f:
            json.dump(emotional_patterns_data, f, indent=2)
        
        # Save feedback history summary
        with open(patterns_dir / "feedback_history.json", 'w') as f:
            json.dump(self.feedback_history[-100:], f, indent=2, default=str)  # Keep last 100
    
    def load_learned_patterns(self):
        """Load previously learned patterns"""
        patterns_file = Path("echo_nexus_voice/emotional_intelligence/emotional_patterns.json")
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                
                for pattern_id, data in patterns_data.items():
                    self.emotional_patterns[pattern_id] = EmotionalPattern(
                        pattern_id=pattern_id,
                        emotion_type=data["emotion_type"],
                        intensity=data["intensity"],
                        context_triggers=[],
                        response_preferences=[],
                        frequency=data["frequency"],
                        last_observed=datetime.fromisoformat(data["last_observed"]),
                        success_rate=data["success_rate"]
                    )
                
                print(f"Loaded {len(self.emotional_patterns)} emotional patterns")
                
            except Exception as e:
                print(f"Error loading patterns: {e}")
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get statistics about the resonant feedback enhancement"""
        return {
            "emotional_patterns_learned": len(self.emotional_patterns),
            "contextual_memories_stored": len(self.contextual_memories),
            "feedback_interactions": len(self.feedback_history),
            "empathy_rules_active": len(self.empathy_rules["primary_empathy_principles"]),
            "cooperation_strategies": len(self.cooperation_strategies["partnership_building"]),
            "average_pattern_success_rate": np.mean([p.success_rate for p in self.emotional_patterns.values()]) if self.emotional_patterns else 0.0
        }

def main():
    """Demonstrate the Resonant Feedback Enhancement system"""
    print("🎭 Echo Nexus Resonant Feedback Enhancement")
    print("Enhanced Contextual Awareness and Emotional Intelligence")
    print("="*60)
    
    enhancer = ResonantFeedbackEnhancer()
    
    # Test emotional analysis
    print("🧠 Emotional Analysis Demo:")
    test_inputs = [
        "I'm so excited about this new project we're building together!",
        "I'm stuck on this error and nothing seems to work...",
        "I'm not sure which approach would be better here?",
        "This is exactly what we needed - perfect solution!"
    ]
    
    for test_input in test_inputs:
        analysis = enhancer.analyze_emotional_context(test_input)
        print(f"\nInput: '{test_input}'")
        print(f"Primary emotions: {analysis['primary_emotions']}")
        print(f"Empathy triggers: {len(analysis['empathy_triggers'])}")
        print(f"Cooperation opportunities: {len(analysis['cooperation_opportunities'])}")
        print(f"Recommended style: {analysis['recommended_response_style']}")
        
        # Generate enhanced response
        base_response = "I can help you with that."
        enhanced = enhancer.generate_empathetic_response(analysis, base_response)
        print(f"Enhanced response: '{enhanced}'")
    
    # Show system stats
    stats = enhancer.get_enhancement_stats()
    print(f"\n📊 System Enhancement Statistics:")
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    return enhancer

if __name__ == "__main__":
    main()
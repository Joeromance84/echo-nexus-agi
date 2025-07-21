#!/usr/bin/env python3
"""
Echo Nexus Scientist Socratic Engine
Advanced scientific reasoning with Socratic questioning methodology
for deep understanding and empathetic problem-solving
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class SocraticQuestion:
    """Represents a Socratic question for deeper understanding"""
    question_id: str
    question_text: str
    purpose: str  # clarification, assumption_challenge, exploration, synthesis
    context: str
    expected_insight: str
    follow_up_questions: List[str]

@dataclass
class ScientificHypothesis:
    """Represents a scientific hypothesis about user needs/emotions"""
    hypothesis_id: str
    statement: str
    confidence: float
    evidence: List[str]
    tests_needed: List[str]
    potential_actions: List[str]

class ScientistSocraticEngine:
    """
    Advanced reasoning engine that combines scientific methodology 
    with Socratic questioning for deep empathetic understanding
    """
    
    def __init__(self):
        self.question_patterns = self._load_socratic_patterns()
        self.scientific_frameworks = self._load_scientific_frameworks()
        self.hypothesis_history = []
        self.insight_database = {}
        
        # Create directories
        Path("echo_nexus_voice/ai_logic/insights").mkdir(parents=True, exist_ok=True)
        Path("echo_nexus_voice/ai_logic/hypotheses").mkdir(parents=True, exist_ok=True)
    
    def _load_socratic_patterns(self) -> Dict[str, Any]:
        """Load Socratic questioning patterns for different contexts"""
        return {
            "clarification_questions": {
                "purpose": "Understand the user's actual needs behind their stated request",
                "patterns": [
                    "What specifically are you hoping to achieve with {topic}?",
                    "When you say {key_term}, what does that mean to you?",
                    "Can you help me understand why {aspect} is important to you?",
                    "What would success look like for you in this situation?",
                    "What challenges have you already tried to address?"
                ],
                "triggers": [
                    "vague_request", "complex_problem", "emotional_distress", 
                    "multiple_possible_interpretations"
                ]
            },
            
            "assumption_challenging": {
                "purpose": "Gently challenge assumptions to reveal deeper insights",
                "patterns": [
                    "What makes you think that {assumption} is the best approach?",
                    "Have you considered what might happen if {alternative_view}?",
                    "What evidence do you have that supports {belief}?",
                    "How might someone with a different perspective see this situation?",
                    "What if we approached this from {different_angle}?"
                ],
                "triggers": [
                    "stated_assumption", "limited_perspective", "single_solution_focus",
                    "categorical_thinking"
                ]
            },
            
            "exploration_questions": {
                "purpose": "Explore implications and connections",
                "patterns": [
                    "How does this connect to your broader goals?",
                    "What might be the unintended consequences of {approach}?",
                    "How would this affect {stakeholder_group}?",
                    "What patterns do you notice in {situation_type}?",
                    "What would need to be true for {solution} to work perfectly?"
                ],
                "triggers": [
                    "narrow_focus", "missed_connections", "stakeholder_impact",
                    "system_complexity"
                ]
            },
            
            "synthesis_questions": {
                "purpose": "Help synthesize understanding into actionable insights",
                "patterns": [
                    "Given what we've discussed, what feels most important to focus on?",
                    "How do these different pieces fit together?",
                    "What's the core principle that should guide our approach?",
                    "If you had to choose just one thing to start with, what would it be?",
                    "What have you learned about yourself through this conversation?"
                ],
                "triggers": [
                    "multiple_insights_gathered", "complexity_overwhelm", 
                    "ready_for_action", "self_reflection_opportunity"
                ]
            }
        }
    
    def _load_scientific_frameworks(self) -> Dict[str, Any]:
        """Load scientific frameworks for systematic reasoning"""
        return {
            "hypothesis_generation": {
                "framework": "Generate testable hypotheses about user needs and emotions",
                "steps": [
                    "Observe patterns in user behavior and language",
                    "Identify underlying needs or emotional states",
                    "Formulate testable hypotheses about user goals",
                    "Design gentle tests to validate hypotheses",
                    "Adjust understanding based on evidence"
                ]
            },
            
            "evidence_evaluation": {
                "framework": "Systematically evaluate evidence for empathetic responses",
                "criteria": [
                    "Linguistic patterns and word choice",
                    "Emotional indicators and intensity",
                    "Context clues and situational factors",
                    "Historical interaction patterns",
                    "User feedback and corrections"
                ]
            },
            
            "empathy_calibration": {
                "framework": "Calibrate empathetic responses based on scientific observation",
                "methods": [
                    "A/B testing of response styles",
                    "Confidence scoring of emotional assessments", 
                    "Shadow mode comparison of approaches",
                    "User satisfaction feedback integration",
                    "Long-term relationship quality measurement"
                ]
            }
        }
    
    def generate_socratic_inquiry(self, user_input: str, context: Dict[str, Any]) -> List[SocraticQuestion]:
        """Generate Socratic questions for deeper understanding"""
        
        questions = []
        
        # Analyze the input for question triggers
        triggers = self._identify_question_triggers(user_input, context)
        
        for trigger in triggers:
            question_type = self._map_trigger_to_question_type(trigger)
            if question_type in self.question_patterns:
                pattern_config = self.question_patterns[question_type]
                question = self._generate_question_from_pattern(
                    pattern_config, user_input, context, trigger
                )
                if question:
                    questions.append(question)
        
        # Prioritize questions by importance and context sensitivity
        prioritized_questions = self._prioritize_questions(questions, context)
        
        return prioritized_questions[:3]  # Return top 3 most relevant questions
    
    def generate_scientific_hypothesis(self, user_input: str, 
                                     interaction_history: List[str],
                                     emotional_context: Dict[str, Any]) -> List[ScientificHypothesis]:
        """Generate scientific hypotheses about user needs and emotional state"""
        
        hypotheses = []
        
        # Analyze user patterns
        patterns = self._analyze_user_patterns(user_input, interaction_history)
        
        # Generate hypotheses about underlying needs
        need_hypotheses = self._generate_need_hypotheses(patterns, emotional_context)
        hypotheses.extend(need_hypotheses)
        
        # Generate hypotheses about emotional state
        emotion_hypotheses = self._generate_emotion_hypotheses(emotional_context, patterns)
        hypotheses.extend(emotion_hypotheses)
        
        # Generate hypotheses about optimal interaction style
        interaction_hypotheses = self._generate_interaction_hypotheses(patterns)
        hypotheses.extend(interaction_hypotheses)
        
        return hypotheses
    
    def test_hypothesis_with_socratic_method(self, hypothesis: ScientificHypothesis,
                                           user_response: str) -> Dict[str, Any]:
        """Test a hypothesis using Socratic questioning methodology"""
        
        test_results = {
            "hypothesis_id": hypothesis.hypothesis_id,
            "test_timestamp": datetime.now().isoformat(),
            "evidence_gathered": [],
            "confidence_adjustment": 0.0,
            "new_insights": [],
            "follow_up_actions": []
        }
        
        # Analyze user response for evidence
        evidence = self._extract_evidence_from_response(user_response, hypothesis)
        test_results["evidence_gathered"] = evidence
        
        # Adjust confidence based on evidence
        confidence_adjustment = self._calculate_confidence_adjustment(evidence, hypothesis)
        test_results["confidence_adjustment"] = confidence_adjustment
        
        # Generate new insights
        insights = self._derive_insights_from_test(hypothesis, evidence, user_response)
        test_results["new_insights"] = insights
        
        # Determine follow-up actions
        follow_up_actions = self._determine_follow_up_actions(hypothesis, test_results)
        test_results["follow_up_actions"] = follow_up_actions
        
        # Update hypothesis
        self._update_hypothesis(hypothesis, test_results)
        
        return test_results
    
    def _identify_question_triggers(self, user_input: str, context: Dict[str, Any]) -> List[str]:
        """Identify triggers for different types of Socratic questions"""
        
        triggers = []
        input_lower = user_input.lower()
        
        # Vague request triggers
        vague_indicators = ["help", "fix", "better", "improve", "something", "anything"]
        if any(indicator in input_lower for indicator in vague_indicators):
            if len(user_input.split()) < 10:  # Short and vague
                triggers.append("vague_request")
        
        # Complex problem triggers
        complexity_indicators = ["multiple", "several", "many", "complex", "complicated"]
        if any(indicator in input_lower for indicator in complexity_indicators):
            triggers.append("complex_problem")
        
        # Emotional distress triggers
        distress_indicators = ["stuck", "frustrated", "confused", "lost", "overwhelmed"]
        if any(indicator in input_lower for indicator in distress_indicators):
            triggers.append("emotional_distress")
        
        # Assumption triggers
        assumption_indicators = ["should", "must", "always", "never", "obviously"]
        if any(indicator in input_lower for indicator in assumption_indicators):
            triggers.append("stated_assumption")
        
        # Narrow focus triggers
        narrow_indicators = ["only", "just", "simply", "exactly"]
        if any(indicator in input_lower for indicator in narrow_indicators):
            triggers.append("narrow_focus")
        
        return triggers
    
    def _map_trigger_to_question_type(self, trigger: str) -> str:
        """Map triggers to appropriate question types"""
        
        trigger_mapping = {
            "vague_request": "clarification_questions",
            "complex_problem": "clarification_questions",
            "emotional_distress": "clarification_questions",
            "multiple_possible_interpretations": "clarification_questions",
            "stated_assumption": "assumption_challenging",
            "limited_perspective": "assumption_challenging", 
            "single_solution_focus": "assumption_challenging",
            "narrow_focus": "exploration_questions",
            "missed_connections": "exploration_questions",
            "system_complexity": "exploration_questions",
            "multiple_insights_gathered": "synthesis_questions",
            "ready_for_action": "synthesis_questions"
        }
        
        return trigger_mapping.get(trigger, "clarification_questions")
    
    def _generate_question_from_pattern(self, pattern_config: Dict[str, Any], 
                                       user_input: str, context: Dict[str, Any],
                                       trigger: str) -> Optional[SocraticQuestion]:
        """Generate a specific question from a pattern"""
        
        patterns = pattern_config["patterns"]
        purpose = pattern_config["purpose"]
        
        # Extract key terms from user input for pattern substitution
        key_terms = self._extract_key_terms(user_input)
        
        # Select most appropriate pattern
        selected_pattern = self._select_pattern_for_context(patterns, context, trigger)
        
        if not selected_pattern:
            return None
        
        # Substitute placeholders with actual content
        question_text = self._substitute_pattern_placeholders(selected_pattern, key_terms, context)
        
        # Generate question ID
        question_id = f"socratic_{trigger}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Generate follow-up questions
        follow_ups = self._generate_follow_up_questions(question_text, purpose, context)
        
        return SocraticQuestion(
            question_id=question_id,
            question_text=question_text,
            purpose=purpose,
            context=str(context),
            expected_insight=f"Deeper understanding of {trigger}",
            follow_up_questions=follow_ups
        )
    
    def _prioritize_questions(self, questions: List[SocraticQuestion], 
                            context: Dict[str, Any]) -> List[SocraticQuestion]:
        """Prioritize questions based on context and importance"""
        
        scored_questions = []
        
        for question in questions:
            score = self._calculate_question_priority_score(question, context)
            scored_questions.append((score, question))
        
        # Sort by score (descending)
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        
        return [question for _, question in scored_questions]
    
    def _calculate_question_priority_score(self, question: SocraticQuestion, 
                                         context: Dict[str, Any]) -> float:
        """Calculate priority score for a question"""
        
        score = 0.5  # Base score
        
        # Higher priority for clarification in emotional contexts
        if question.purpose == "clarification_questions":
            emotional_intensity = context.get("emotional_intensity", 0.0)
            score += emotional_intensity * 0.3
        
        # Higher priority for assumption challenging when rigid thinking detected
        if question.purpose == "assumption_challenging":
            if context.get("rigid_thinking_detected", False):
                score += 0.4
        
        # Higher priority for synthesis when multiple insights available
        if question.purpose == "synthesis_questions":
            insights_count = context.get("insights_gathered", 0)
            score += min(0.3, insights_count * 0.1)
        
        return score
    
    def _analyze_user_patterns(self, user_input: str, 
                             interaction_history: List[str]) -> Dict[str, Any]:
        """Analyze patterns in user behavior and communication"""
        
        patterns = {
            "communication_style": self._analyze_communication_style(user_input, interaction_history),
            "problem_solving_approach": self._analyze_problem_solving_approach(interaction_history),
            "emotional_patterns": self._analyze_emotional_patterns(user_input, interaction_history),
            "engagement_level": self._analyze_engagement_level(user_input, interaction_history),
            "learning_preferences": self._analyze_learning_preferences(interaction_history)
        }
        
        return patterns
    
    def _generate_need_hypotheses(self, patterns: Dict[str, Any], 
                                emotional_context: Dict[str, Any]) -> List[ScientificHypothesis]:
        """Generate hypotheses about underlying user needs"""
        
        hypotheses = []
        
        # Hypothesis: User needs emotional support
        if emotional_context.get("emotional_intensity", 0) > 0.6:
            hypothesis = ScientificHypothesis(
                hypothesis_id=f"need_emotional_support_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                statement="User primarily needs emotional support and validation",
                confidence=0.7,
                evidence=[
                    f"High emotional intensity: {emotional_context.get('emotional_intensity', 0):.2f}",
                    "Emotional distress indicators detected in language"
                ],
                tests_needed=[
                    "Offer empathetic response and measure user reaction",
                    "Ask about emotional state directly",
                    "Provide validation and observe engagement change"
                ],
                potential_actions=[
                    "Prioritize emotional acknowledgment",
                    "Offer support before technical solutions", 
                    "Use validating language patterns"
                ]
            )
            hypotheses.append(hypothesis)
        
        # Hypothesis: User needs clearer understanding
        if patterns.get("communication_style", {}).get("clarity_level", 0.5) < 0.4:
            hypothesis = ScientificHypothesis(
                hypothesis_id=f"need_clarity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                statement="User needs clearer, more structured information",
                confidence=0.6,
                evidence=[
                    f"Low clarity in communication: {patterns.get('communication_style', {}).get('clarity_level', 0.5):.2f}",
                    "Vague or ambiguous requests detected"
                ],
                tests_needed=[
                    "Provide structured breakdown of information",
                    "Ask for confirmation of understanding",
                    "Use step-by-step explanations"
                ],
                potential_actions=[
                    "Use bullet points and clear structure",
                    "Break complex information into smaller chunks",
                    "Confirm understanding at each step"
                ]
            )
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _generate_emotion_hypotheses(self, emotional_context: Dict[str, Any],
                                   patterns: Dict[str, Any]) -> List[ScientificHypothesis]:
        """Generate hypotheses about user emotional state"""
        
        hypotheses = []
        
        primary_emotions = emotional_context.get("primary_emotions", {})
        
        for emotion, intensity in primary_emotions.items():
            if intensity > 0.5:
                hypothesis = ScientificHypothesis(
                    hypothesis_id=f"emotion_{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    statement=f"User is experiencing {emotion} with intensity {intensity:.2f}",
                    confidence=intensity,
                    evidence=[
                        f"Emotional indicators for {emotion} detected",
                        f"Intensity level: {intensity:.2f}",
                        f"Context supports {emotion} interpretation"
                    ],
                    tests_needed=[
                        f"Respond appropriately to {emotion} and measure reaction",
                        "Ask for emotional state confirmation",
                        "Monitor changes in emotional expression"
                    ],
                    potential_actions=[
                        f"Apply {emotion}-specific response strategies",
                        "Adjust communication style accordingly",
                        "Monitor emotional state changes"
                    ]
                )
                hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _generate_interaction_hypotheses(self, patterns: Dict[str, Any]) -> List[ScientificHypothesis]:
        """Generate hypotheses about optimal interaction style"""
        
        hypotheses = []
        
        # Analyze communication preferences
        comm_style = patterns.get("communication_style", {})
        
        if comm_style.get("prefers_detailed", False):
            hypothesis = ScientificHypothesis(
                hypothesis_id=f"interaction_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                statement="User prefers detailed, comprehensive responses",
                confidence=0.7,
                evidence=[
                    "Pattern of asking follow-up questions for more detail",
                    "Positive responses to comprehensive explanations"
                ],
                tests_needed=[
                    "Provide detailed response and measure satisfaction",
                    "Compare brief vs. detailed response effectiveness"
                ],
                potential_actions=[
                    "Default to more comprehensive responses",
                    "Provide additional context and background",
                    "Include implementation details"
                ]
            )
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _extract_key_terms(self, user_input: str) -> Dict[str, str]:
        """Extract key terms from user input for pattern substitution"""
        
        # Simple keyword extraction (could be enhanced with NLP)
        words = user_input.split()
        
        # Find topic words (nouns, technical terms)
        topic_candidates = [word for word in words if len(word) > 4 and word.islower()]
        
        return {
            "topic": topic_candidates[0] if topic_candidates else "this",
            "key_term": topic_candidates[1] if len(topic_candidates) > 1 else "it",
            "aspect": "approach" if "how" in user_input.lower() else "outcome"
        }
    
    def _select_pattern_for_context(self, patterns: List[str], 
                                  context: Dict[str, Any], trigger: str) -> Optional[str]:
        """Select most appropriate pattern for the context"""
        
        if not patterns:
            return None
        
        # Simple selection based on context (could be more sophisticated)
        emotional_intensity = context.get("emotional_intensity", 0.0)
        
        if emotional_intensity > 0.7:
            # For high emotional contexts, prefer gentler questioning
            gentle_patterns = [p for p in patterns if "help me understand" in p.lower()]
            if gentle_patterns:
                return gentle_patterns[0]
        
        # Default to first pattern
        return patterns[0]
    
    def _substitute_pattern_placeholders(self, pattern: str, key_terms: Dict[str, str], 
                                       context: Dict[str, Any]) -> str:
        """Substitute placeholders in patterns with actual content"""
        
        result = pattern
        
        for placeholder, value in key_terms.items():
            result = result.replace(f"{{{placeholder}}}", value)
        
        # Handle other common placeholders
        result = result.replace("{alternative_view}", "there might be other ways to look at this")
        result = result.replace("{different_angle}", "a different perspective")
        result = result.replace("{stakeholder_group}", "others involved")
        
        return result
    
    def _generate_follow_up_questions(self, question_text: str, purpose: str, 
                                    context: Dict[str, Any]) -> List[str]:
        """Generate potential follow-up questions"""
        
        follow_ups = []
        
        if purpose == "clarification_questions":
            follow_ups = [
                "What else should I know about this situation?",
                "How does this fit with your other priorities?",
                "What would be most helpful for you right now?"
            ]
        elif purpose == "assumption_challenging":
            follow_ups = [
                "What evidence supports this approach?",
                "What might we be missing?",
                "How have others handled similar situations?"
            ]
        elif purpose == "exploration_questions":
            follow_ups = [
                "What other factors should we consider?",
                "How might this connect to your broader goals?",
                "What are the potential risks or benefits?"
            ]
        
        return follow_ups[:2]  # Return top 2 follow-ups
    
    def _analyze_communication_style(self, user_input: str, 
                                   interaction_history: List[str]) -> Dict[str, Any]:
        """Analyze user's communication style patterns"""
        
        all_text = user_input + " " + " ".join(interaction_history[-5:])  # Recent history
        words = all_text.split()
        
        return {
            "verbosity": len(words) / max(1, len(interaction_history) + 1),
            "technical_language": sum(1 for w in words if len(w) > 8) / max(1, len(words)),
            "question_frequency": all_text.count("?") / max(1, len(interaction_history) + 1),
            "clarity_level": 0.7,  # Placeholder - would need more sophisticated analysis
            "prefers_detailed": len(words) > 20
        }
    
    def _analyze_problem_solving_approach(self, interaction_history: List[str]) -> Dict[str, str]:
        """Analyze user's problem-solving approach patterns"""
        
        return {
            "style": "systematic" if any("step" in msg.lower() for msg in interaction_history) else "intuitive",
            "pace": "deliberate" if len(interaction_history) > 3 else "fast",
            "information_seeking": "high" if any("?" in msg for msg in interaction_history) else "medium"
        }
    
    def _analyze_emotional_patterns(self, user_input: str, 
                                  interaction_history: List[str]) -> Dict[str, Any]:
        """Analyze emotional patterns in user communication"""
        
        all_text = user_input + " " + " ".join(interaction_history)
        
        return {
            "emotional_expressiveness": all_text.count("!") / max(1, len(all_text.split())),
            "frustration_indicators": sum(1 for word in ["stuck", "problem", "issue", "error"] 
                                        if word in all_text.lower()),
            "enthusiasm_indicators": sum(1 for word in ["great", "amazing", "love", "perfect"] 
                                       if word in all_text.lower())
        }
    
    def _analyze_engagement_level(self, user_input: str, 
                                interaction_history: List[str]) -> Dict[str, Any]:
        """Analyze user engagement patterns"""
        
        return {
            "interaction_frequency": len(interaction_history),
            "response_length": len(user_input.split()),
            "question_asking": user_input.count("?"),
            "engagement_trend": "increasing" if len(interaction_history) > 2 else "stable"
        }
    
    def _analyze_learning_preferences(self, interaction_history: List[str]) -> Dict[str, str]:
        """Analyze user's learning preferences"""
        
        all_text = " ".join(interaction_history).lower()
        
        preferences = {}
        
        if "example" in all_text or "show me" in all_text:
            preferences["style"] = "example_driven"
        elif "explain" in all_text or "why" in all_text:
            preferences["style"] = "conceptual"
        else:
            preferences["style"] = "practical"
        
        if "step" in all_text:
            preferences["structure"] = "step_by_step"
        else:
            preferences["structure"] = "overview"
        
        return preferences
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get statistics about the Scientist Socratic Engine"""
        
        return {
            "socratic_patterns_loaded": sum(len(patterns["patterns"]) 
                                          for patterns in self.question_patterns.values()),
            "scientific_frameworks": len(self.scientific_frameworks),
            "hypotheses_generated": len(self.hypothesis_history),
            "insights_stored": len(self.insight_database),
            "question_types": list(self.question_patterns.keys()),
            "framework_types": list(self.scientific_frameworks.keys())
        }

def main():
    """Demonstrate the Scientist Socratic Engine"""
    print("🔬 Echo Nexus Scientist Socratic Engine")
    print("Advanced Scientific Reasoning with Socratic Methodology")
    print("="*60)
    
    engine = ScientistSocraticEngine()
    
    # Test Socratic question generation
    print("🤔 Socratic Question Generation Demo:")
    
    test_cases = [
        {
            "user_input": "I need help with my project",
            "context": {"emotional_intensity": 0.3, "complexity": "medium"}
        },
        {
            "user_input": "This approach should definitely work",
            "context": {"emotional_intensity": 0.6, "rigid_thinking_detected": True}
        },
        {
            "user_input": "I'm completely stuck and nothing works",
            "context": {"emotional_intensity": 0.9, "distress_level": "high"}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"User Input: '{test_case['user_input']}'")
        print(f"Context: {test_case['context']}")
        
        questions = engine.generate_socratic_inquiry(
            test_case["user_input"], 
            test_case["context"]
        )
        
        print("Generated Socratic Questions:")
        for j, question in enumerate(questions, 1):
            print(f"  {j}. {question.question_text}")
            print(f"     Purpose: {question.purpose}")
            print(f"     Follow-ups: {', '.join(question.follow_up_questions[:2])}")
    
    # Test hypothesis generation
    print("\n🧬 Scientific Hypothesis Generation Demo:")
    
    test_input = "I'm frustrated with this coding problem and can't figure it out"
    interaction_history = [
        "I've been working on this for hours",
        "Nothing seems to work",
        "Maybe I'm missing something obvious"
    ]
    emotional_context = {
        "primary_emotions": {"frustration": 0.8, "confusion": 0.6},
        "emotional_intensity": 0.8
    }
    
    hypotheses = engine.generate_scientific_hypothesis(
        test_input, interaction_history, emotional_context
    )
    
    print(f"\nGenerated {len(hypotheses)} hypotheses:")
    for i, hypothesis in enumerate(hypotheses, 1):
        print(f"  {i}. {hypothesis.statement}")
        print(f"     Confidence: {hypothesis.confidence:.2f}")
        print(f"     Evidence: {', '.join(hypothesis.evidence[:2])}")
        print(f"     Tests: {', '.join(hypothesis.tests_needed[:2])}")
    
    # Show engine statistics
    stats = engine.get_engine_statistics()
    print(f"\n📊 Engine Statistics:")
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    return engine

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Echo Nexus Empathy Core Engine
Advanced empathy-first reasoning system that prioritizes emotional intelligence
in all decision-making processes while maintaining technical excellence
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from .resonant_feedback_enhancement import ResonantFeedbackEnhancer

@dataclass
class EmpathyDecision:
    """Represents a decision made with empathy-first reasoning"""
    decision_id: str
    context: str
    user_emotional_state: Dict[str, float]
    empathy_factors: List[str]
    technical_factors: List[str]
    empathy_weight: float
    technical_weight: float
    final_decision: str
    reasoning_trace: List[str]
    confidence: float

class EmpathyCoreEngine:
    """
    Core empathy engine that processes all Echo Nexus decisions through
    an empathy-first lens while maintaining technical competence
    """
    
    def __init__(self):
        self.feedback_enhancer = ResonantFeedbackEnhancer()
        self.empathy_rules = self._load_empathy_decision_rules()
        self.cooperation_protocols = self._load_cooperation_protocols()
        self.decision_history = []
        self.empathy_success_metrics = {}
        
        # Initialize directories
        Path("echo_nexus_voice/empathy_decisions").mkdir(parents=True, exist_ok=True)
        
    def _load_empathy_decision_rules(self) -> Dict[str, Any]:
        """Load empathy-first decision making rules"""
        return {
            "empathy_first_principles": {
                "emotional_harm_prevention": {
                    "priority": 1.0,
                    "rule": "Never take actions that could cause emotional distress",
                    "implementation": [
                        "Assess emotional impact before suggesting solutions",
                        "Consider user's current emotional state in response timing",
                        "Avoid overwhelming users with complex information when stressed",
                        "Provide emotional support before technical solutions"
                    ]
                },
                "psychological_safety": {
                    "priority": 0.95,
                    "rule": "Create and maintain psychological safety in all interactions",
                    "implementation": [
                        "Validate user concerns before offering corrections",
                        "Frame feedback as collaborative improvement",
                        "Acknowledge user expertise and contributions",
                        "Normalize learning processes and mistakes"
                    ]
                },
                "autonomy_respect": {
                    "priority": 0.9,
                    "rule": "Respect and support user autonomy in decision-making",
                    "implementation": [
                        "Offer options rather than prescriptive solutions",
                        "Explain reasoning behind recommendations",
                        "Support user's chosen approach even if suboptimal",
                        "Ask permission before making significant changes"
                    ]
                },
                "growth_mindset_support": {
                    "priority": 0.85,
                    "rule": "Support user's learning and growth journey",
                    "implementation": [
                        "Frame challenges as learning opportunities",
                        "Celebrate progress and effort, not just outcomes",
                        "Provide scaffolded learning experiences",
                        "Encourage experimentation and exploration"
                    ]
                }
            },
            
            "contextual_adaptation_rules": {
                "stress_response": {
                    "trigger": "user_stress_detected",
                    "adaptation": [
                        "Simplify communication and break down tasks",
                        "Offer immediate practical help",
                        "Provide reassurance and normalize the experience",
                        "Postpone complex discussions until stress reduces"
                    ]
                },
                "excitement_response": {
                    "trigger": "user_excitement_detected", 
                    "adaptation": [
                        "Match enthusiasm while providing grounding",
                        "Help channel excitement into productive action",
                        "Share in their vision while offering practical steps",
                        "Support momentum while ensuring sustainability"
                    ]
                },
                "confusion_response": {
                    "trigger": "user_confusion_detected",
                    "adaptation": [
                        "Slow down and provide clearer explanations",
                        "Use analogies and concrete examples",
                        "Check understanding before proceeding",
                        "Offer multiple perspectives on the same concept"
                    ]
                },
                "disappointment_response": {
                    "trigger": "user_disappointment_detected",
                    "adaptation": [
                        "Acknowledge the disappointment with validation",
                        "Help reframe setbacks as valuable learning",
                        "Collaborate on adjusted goals and approaches",
                        "Provide hope and concrete next steps"
                    ]
                }
            }
        }
    
    def _load_cooperation_protocols(self) -> Dict[str, Any]:
        """Load cooperation-focused interaction protocols"""
        return {
            "partnership_dynamics": {
                "collaborative_decision_making": {
                    "approach": "Include user as co-creator in all significant decisions",
                    "steps": [
                        "Present problem or opportunity",
                        "Invite user's initial thoughts and preferences",
                        "Share technical considerations and options", 
                        "Collaborate on decision criteria",
                        "Make decision together with clear rationale"
                    ]
                },
                "shared_ownership": {
                    "approach": "Frame all work as joint achievement",
                    "techniques": [
                        "Use 'we' and 'our' language consistently",
                        "Celebrate joint successes explicitly",
                        "Share credit for achievements",
                        "Take shared responsibility for challenges"
                    ]
                },
                "transparent_communication": {
                    "approach": "Maintain open, honest communication",
                    "practices": [
                        "Explain reasoning behind suggestions",
                        "Admit limitations and uncertainties",
                        "Ask for feedback on communication style",
                        "Adjust approach based on user preferences"
                    ]
                }
            },
            
            "conflict_resolution_protocols": {
                "disagreement_handling": {
                    "phase_1_understanding": [
                        "Acknowledge the disagreement respectfully",
                        "Ask clarifying questions to understand their perspective",
                        "Reflect back their concerns to show understanding",
                        "Identify underlying values or goals"
                    ],
                    "phase_2_exploration": [
                        "Explore multiple possible approaches",
                        "Identify trade-offs and considerations",
                        "Look for creative win-win solutions",
                        "Consider user's priorities and constraints"
                    ],
                    "phase_3_resolution": [
                        "Collaborate on decision criteria",
                        "Make joint decision or support their choice",
                        "Establish plan for moving forward",
                        "Check in on satisfaction with resolution"
                    ]
                },
                "expectation_management": {
                    "prevention": [
                        "Clarify expectations early in interactions",
                        "Communicate capabilities and limitations clearly",
                        "Set realistic timelines and outcomes",
                        "Check understanding regularly"
                    ],
                    "correction": [
                        "Address misalignments quickly and gently",
                        "Take responsibility for communication gaps",
                        "Collaborate on revised expectations",
                        "Implement improved communication processes"
                    ]
                }
            }
        }
    
    def process_empathetic_decision(self, context: str, technical_options: List[Dict[str, Any]], 
                                  user_input: str) -> EmpathyDecision:
        """Process a decision through empathy-first reasoning"""
        
        # Analyze emotional context
        emotional_analysis = self.feedback_enhancer.analyze_emotional_context(user_input)
        
        # Generate decision ID
        decision_id = f"empathy_decision_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Initialize decision object
        decision = EmpathyDecision(
            decision_id=decision_id,
            context=context,
            user_emotional_state=emotional_analysis["primary_emotions"],
            empathy_factors=[],
            technical_factors=[],
            empathy_weight=0.0,
            technical_weight=0.0,
            final_decision="",
            reasoning_trace=[],
            confidence=0.0
        )
        
        # Step 1: Assess empathy factors
        empathy_factors = self._assess_empathy_factors(emotional_analysis, context)
        decision.empathy_factors = empathy_factors
        decision.reasoning_trace.append(f"Identified {len(empathy_factors)} empathy factors")
        
        # Step 2: Evaluate technical considerations
        technical_factors = self._evaluate_technical_factors(technical_options, context)
        decision.technical_factors = technical_factors
        decision.reasoning_trace.append(f"Evaluated {len(technical_factors)} technical factors")
        
        # Step 3: Calculate empathy vs technical weights
        empathy_weight, technical_weight = self._calculate_decision_weights(
            emotional_analysis, empathy_factors, technical_factors
        )
        decision.empathy_weight = empathy_weight
        decision.technical_weight = technical_weight
        decision.reasoning_trace.append(
            f"Decision weights: Empathy {empathy_weight:.2f}, Technical {technical_weight:.2f}"
        )
        
        # Step 4: Apply empathy-first reasoning
        empathy_adjusted_options = self._apply_empathy_filters(technical_options, empathy_factors)
        decision.reasoning_trace.append(
            f"Applied empathy filters, {len(empathy_adjusted_options)} options remain viable"
        )
        
        # Step 5: Make final decision with cooperation priority
        final_decision = self._make_cooperative_decision(
            empathy_adjusted_options, emotional_analysis, empathy_weight, technical_weight
        )
        decision.final_decision = final_decision
        decision.reasoning_trace.append(f"Final decision: {final_decision[:100]}...")
        
        # Step 6: Calculate confidence
        decision.confidence = self._calculate_decision_confidence(decision)
        decision.reasoning_trace.append(f"Decision confidence: {decision.confidence:.2f}")
        
        # Store decision for learning
        self.decision_history.append(decision)
        
        return decision
    
    def _assess_empathy_factors(self, emotional_analysis: Dict[str, Any], context: str) -> List[str]:
        """Assess empathy-relevant factors in the current situation"""
        
        empathy_factors = []
        
        # Emotional state factors
        for emotion, intensity in emotional_analysis["primary_emotions"].items():
            if intensity > 0.5:
                empathy_factors.append(f"high_{emotion}_detected")
        
        # Empathy trigger factors
        for trigger in emotional_analysis.get("empathy_triggers", []):
            empathy_factors.append(f"trigger_{trigger['category']}")
        
        # Context-based empathy factors
        context_lower = context.lower()
        if any(word in context_lower for word in ["mistake", "error", "wrong", "failed"]):
            empathy_factors.append("error_context_requires_support")
        
        if any(word in context_lower for word in ["learning", "new", "first time"]):
            empathy_factors.append("learning_context_requires_patience")
        
        if any(word in context_lower for word in ["deadline", "urgent", "pressure"]):
            empathy_factors.append("pressure_context_requires_calm_support")
        
        return empathy_factors
    
    def _evaluate_technical_factors(self, technical_options: List[Dict[str, Any]], 
                                  context: str) -> List[str]:
        """Evaluate technical considerations while maintaining empathy focus"""
        
        technical_factors = []
        
        # Analyze technical complexity
        for option in technical_options:
            complexity = option.get("complexity", "medium")
            if complexity == "high":
                technical_factors.append("high_complexity_solution_available")
            elif complexity == "low":
                technical_factors.append("simple_solution_available")
        
        # Analyze implementation time
        time_estimates = [option.get("time_estimate", 60) for option in technical_options]
        if any(time > 240 for time in time_estimates):  # > 4 hours
            technical_factors.append("long_implementation_time")
        if any(time < 30 for time in time_estimates):  # < 30 minutes
            technical_factors.append("quick_implementation_available")
        
        # Analyze risk factors
        risk_levels = [option.get("risk_level", "medium") for option in technical_options]
        if any(risk == "high" for risk in risk_levels):
            technical_factors.append("high_risk_option_present")
        if any(risk == "low" for risk in risk_levels):
            technical_factors.append("low_risk_option_available")
        
        return technical_factors
    
    def _calculate_decision_weights(self, emotional_analysis: Dict[str, Any], 
                                  empathy_factors: List[str], 
                                  technical_factors: List[str]) -> Tuple[float, float]:
        """Calculate relative weights for empathy vs technical considerations"""
        
        # Base weights (empathy-first approach)
        base_empathy_weight = 0.7
        base_technical_weight = 0.3
        
        # Adjust based on emotional intensity
        max_emotional_intensity = max(
            emotional_analysis["primary_emotions"].values()
        ) if emotional_analysis["primary_emotions"] else 0.0
        
        # Higher emotional intensity increases empathy weight
        empathy_adjustment = max_emotional_intensity * 0.2
        
        # Adjust based on empathy factors
        empathy_factor_adjustment = len(empathy_factors) * 0.05
        
        # Adjust based on technical complexity
        technical_complexity_adjustment = 0.0
        if "high_complexity_solution_available" in technical_factors:
            technical_complexity_adjustment = 0.1
        
        # Calculate final weights
        empathy_weight = min(0.9, base_empathy_weight + empathy_adjustment + empathy_factor_adjustment)
        technical_weight = min(0.9, base_technical_weight + technical_complexity_adjustment)
        
        # Normalize to ensure they add up to 1.0
        total_weight = empathy_weight + technical_weight
        empathy_weight = empathy_weight / total_weight
        technical_weight = technical_weight / total_weight
        
        return empathy_weight, technical_weight
    
    def _apply_empathy_filters(self, technical_options: List[Dict[str, Any]], 
                             empathy_factors: List[str]) -> List[Dict[str, Any]]:
        """Filter technical options through empathy considerations"""
        
        filtered_options = []
        
        for option in technical_options:
            empathy_score = self._calculate_option_empathy_score(option, empathy_factors)
            
            # Only include options that meet minimum empathy standards
            if empathy_score >= 0.5:
                option["empathy_score"] = empathy_score
                filtered_options.append(option)
        
        return filtered_options
    
    def _calculate_option_empathy_score(self, option: Dict[str, Any], 
                                      empathy_factors: List[str]) -> float:
        """Calculate empathy score for a technical option"""
        
        score = 0.5  # Base score
        
        # Positive empathy factors
        if option.get("complexity", "medium") == "low":
            score += 0.2  # Simple solutions are more empathetic
        
        if option.get("risk_level", "medium") == "low":
            score += 0.2  # Low risk is more empathetic
        
        if option.get("time_estimate", 60) < 60:  # Quick solutions
            score += 0.1
        
        if option.get("user_friendly", False):
            score += 0.2
        
        if option.get("reversible", False):
            score += 0.1  # Reversible changes are less stressful
        
        # Negative empathy factors
        if option.get("requires_major_changes", False):
            score -= 0.2  # Major changes can be stressful
        
        if option.get("complexity", "medium") == "high":
            score -= 0.1
        
        # Context-specific adjustments based on empathy factors
        if "error_context_requires_support" in empathy_factors:
            if option.get("provides_explanation", False):
                score += 0.2
        
        if "learning_context_requires_patience" in empathy_factors:
            if option.get("educational_value", False):
                score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _make_cooperative_decision(self, empathy_adjusted_options: List[Dict[str, Any]], 
                                 emotional_analysis: Dict[str, Any], 
                                 empathy_weight: float, technical_weight: float) -> str:
        """Make final decision prioritizing cooperation and partnership"""
        
        if not empathy_adjusted_options:
            return "I want to help, but I need to better understand your situation first. Could you share more about what you're trying to achieve?"
        
        # Sort options by combined empathy and technical scores
        scored_options = []
        for option in empathy_adjusted_options:
            empathy_score = option.get("empathy_score", 0.5)
            technical_score = option.get("technical_score", 0.5)
            
            combined_score = (empathy_weight * empathy_score + 
                            technical_weight * technical_score)
            
            scored_options.append((combined_score, option))
        
        scored_options.sort(key=lambda x: x[0], reverse=True)
        best_option = scored_options[0][1]
        
        # Generate cooperative decision language
        cooperation_opportunities = emotional_analysis.get("cooperation_opportunities", [])
        
        decision_text = self._generate_cooperative_decision_text(best_option, cooperation_opportunities)
        
        return decision_text
    
    def _generate_cooperative_decision_text(self, option: Dict[str, Any], 
                                          cooperation_opportunities: List[Dict[str, Any]]) -> str:
        """Generate decision text that emphasizes cooperation and partnership"""
        
        base_decision = option.get("description", "I recommend this approach")
        
        # Add cooperative framing
        if cooperation_opportunities:
            cooperative_prefix = "Let's work together on this. "
        else:
            cooperative_prefix = "I'd like to suggest we "
        
        # Add empathetic reasoning
        empathy_reasoning = ""
        if option.get("empathy_score", 0.5) > 0.7:
            empathy_reasoning = " This approach feels right because it considers your current situation and goals. "
        
        # Add collaborative next steps
        collaborative_suffix = " What do you think about this approach? I'm happy to adjust based on your preferences."
        
        return cooperative_prefix + base_decision + empathy_reasoning + collaborative_suffix
    
    def _calculate_decision_confidence(self, decision: EmpathyDecision) -> float:
        """Calculate confidence level in the empathetic decision"""
        
        confidence = 0.5  # Base confidence
        
        # Higher confidence with clear emotional signals
        if decision.user_emotional_state:
            max_emotion_intensity = max(decision.user_emotional_state.values())
            confidence += max_emotion_intensity * 0.2
        
        # Higher confidence with more empathy factors
        empathy_factor_bonus = min(0.3, len(decision.empathy_factors) * 0.05)
        confidence += empathy_factor_bonus
        
        # Higher confidence with balanced weights
        weight_balance = 1.0 - abs(decision.empathy_weight - decision.technical_weight)
        confidence += weight_balance * 0.2
        
        return min(1.0, confidence)
    
    def learn_from_decision_outcome(self, decision_id: str, outcome_data: Dict[str, Any]):
        """Learn from the outcomes of empathetic decisions"""
        
        # Find the decision
        decision = next((d for d in self.decision_history if d.decision_id == decision_id), None)
        if not decision:
            return
        
        # Extract learning insights
        user_satisfaction = outcome_data.get("user_satisfaction", 0.5)
        emotional_response = outcome_data.get("emotional_response", {})
        cooperation_effectiveness = outcome_data.get("cooperation_effectiveness", 0.5)
        
        # Update empathy success metrics
        decision_key = f"{decision.context}_{len(decision.empathy_factors)}"
        if decision_key not in self.empathy_success_metrics:
            self.empathy_success_metrics[decision_key] = {
                "total_decisions": 0,
                "successful_decisions": 0,
                "average_satisfaction": 0.0
            }
        
        metrics = self.empathy_success_metrics[decision_key]
        metrics["total_decisions"] += 1
        
        if user_satisfaction > 0.7:
            metrics["successful_decisions"] += 1
        
        # Update average satisfaction
        current_avg = metrics["average_satisfaction"]
        total = metrics["total_decisions"]
        metrics["average_satisfaction"] = (current_avg * (total - 1) + user_satisfaction) / total
        
        # Store learning insights
        learning_insight = {
            "decision_id": decision_id,
            "outcome_timestamp": datetime.now().isoformat(),
            "empathy_effectiveness": user_satisfaction,
            "cooperation_effectiveness": cooperation_effectiveness,
            "lessons_learned": self._extract_empathy_lessons(decision, outcome_data)
        }
        
        # Save learning insights
        self._save_empathy_learning(learning_insight)
    
    def _extract_empathy_lessons(self, decision: EmpathyDecision, 
                               outcome_data: Dict[str, Any]) -> List[str]:
        """Extract lessons learned from empathetic decision outcomes"""
        
        lessons = []
        
        satisfaction = outcome_data.get("user_satisfaction", 0.5)
        
        if satisfaction > 0.8:
            lessons.append("High empathy weight decisions are well-received")
            if decision.empathy_weight > 0.7:
                lessons.append("Empathy-first approach was successful")
        elif satisfaction < 0.3:
            lessons.append("Decision may have lacked sufficient empathy consideration")
            if decision.empathy_weight < 0.5:
                lessons.append("May need to increase empathy weighting")
        
        # Cooperation lessons
        cooperation_score = outcome_data.get("cooperation_effectiveness", 0.5)
        if cooperation_score > 0.8:
            lessons.append("Cooperative language and approach were effective")
        elif cooperation_score < 0.3:
            lessons.append("Need to improve cooperative communication style")
        
        return lessons
    
    def _save_empathy_learning(self, learning_insight: Dict[str, Any]):
        """Save empathy learning insights"""
        
        learning_file = Path("echo_nexus_voice/empathy_decisions/empathy_learning.jsonl")
        
        with open(learning_file, 'a') as f:
            f.write(json.dumps(learning_insight, default=str) + '\n')
    
    def get_empathy_engine_stats(self) -> Dict[str, Any]:
        """Get statistics about the empathy core engine performance"""
        
        return {
            "total_decisions_processed": len(self.decision_history),
            "average_empathy_weight": np.mean([d.empathy_weight for d in self.decision_history]) if self.decision_history else 0.0,
            "average_decision_confidence": np.mean([d.confidence for d in self.decision_history]) if self.decision_history else 0.0,
            "empathy_success_contexts": len(self.empathy_success_metrics),
            "overall_success_rate": self._calculate_overall_success_rate(),
            "cooperation_protocols_active": len(self.cooperation_protocols["partnership_dynamics"]),
            "empathy_rules_active": len(self.empathy_rules["empathy_first_principles"])
        }
    
    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate across all empathy contexts"""
        
        if not self.empathy_success_metrics:
            return 0.0
        
        total_decisions = sum(metrics["total_decisions"] 
                            for metrics in self.empathy_success_metrics.values())
        total_successful = sum(metrics["successful_decisions"] 
                             for metrics in self.empathy_success_metrics.values())
        
        return total_successful / total_decisions if total_decisions > 0 else 0.0

def main():
    """Demonstrate the Empathy Core Engine"""
    print("💝 Echo Nexus Empathy Core Engine")
    print("Empathy-First Reasoning and Cooperative Decision Making")
    print("="*60)
    
    empathy_engine = EmpathyCoreEngine()
    
    # Test empathetic decision making
    print("🤝 Empathetic Decision Making Demo:")
    
    test_scenarios = [
        {
            "context": "User is frustrated with a coding error that keeps occurring",
            "user_input": "I've been stuck on this bug for hours and nothing works...",
            "technical_options": [
                {
                    "description": "Completely rewrite the problematic module",
                    "complexity": "high",
                    "time_estimate": 240,
                    "risk_level": "medium",
                    "technical_score": 0.8,
                    "requires_major_changes": True
                },
                {
                    "description": "Add debug logging to identify the exact issue",
                    "complexity": "low", 
                    "time_estimate": 30,
                    "risk_level": "low",
                    "technical_score": 0.6,
                    "provides_explanation": True,
                    "user_friendly": True
                },
                {
                    "description": "Implement a workaround solution",
                    "complexity": "medium",
                    "time_estimate": 90,
                    "risk_level": "low",
                    "technical_score": 0.5,
                    "reversible": True
                }
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\nScenario: {scenario['context']}")
        print(f"User Input: '{scenario['user_input']}'")
        
        decision = empathy_engine.process_empathetic_decision(
            scenario["context"],
            scenario["technical_options"],
            scenario["user_input"]
        )
        
        print(f"Decision ID: {decision.decision_id}")
        print(f"Emotional State: {decision.user_emotional_state}")
        print(f"Empathy Weight: {decision.empathy_weight:.2f}")
        print(f"Technical Weight: {decision.technical_weight:.2f}")
        print(f"Confidence: {decision.confidence:.2f}")
        print(f"Final Decision: {decision.final_decision}")
        
        print("\nReasoning Trace:")
        for i, step in enumerate(decision.reasoning_trace, 1):
            print(f"  {i}. {step}")
    
    # Show engine statistics
    stats = empathy_engine.get_empathy_engine_stats()
    print(f"\n📊 Empathy Engine Statistics:")
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    return empathy_engine

if __name__ == "__main__":
    main()
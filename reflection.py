#!/usr/bin/env python3
"""
Reflection Engine - Advanced Self-Improvement for EchoSoul AGI
Enables the agent to review actions, learn from outcomes, and improve its own logic
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


class ReflectionEngine:
    """Advanced reflection and self-improvement system"""
    
    def __init__(self):
        self.reflection_history = []
        self.improvement_patterns = []
        self.learning_rules = self._load_learning_rules()
        self.meta_learning_threshold = 5  # Trigger meta-learning after 5 reflections
        
    def reflect(self, context: Dict, action_outcome: Dict) -> Dict:
        """Main reflection function that analyzes outcomes and updates system logic"""
        
        reflection_start = datetime.now()
        reflection_id = self._generate_reflection_id(context, action_outcome)
        
        print(f"Reflection: Starting analysis of action outcome")
        
        # Analyze the action outcome
        outcome_analysis = self._analyze_outcome(action_outcome, context)
        
        # Extract lessons learned
        lessons = self._extract_lessons(action_outcome, outcome_analysis, context)
        
        # Identify improvement opportunities
        improvements = self._identify_improvements(outcome_analysis, lessons)
        
        # Update learning patterns
        context = self._update_learning_patterns(context, lessons, improvements)
        
        # Apply immediate system improvements
        context = self._apply_immediate_improvements(context, improvements)
        
        # Trigger meta-learning if threshold reached
        if len(self.reflection_history) >= self.meta_learning_threshold:
            context = self._trigger_meta_learning(context)
        
        # Create reflection record
        reflection_record = {
            "id": reflection_id,
            "timestamp": reflection_start.isoformat(),
            "outcome_analysis": outcome_analysis,
            "lessons": lessons,
            "improvements": improvements,
            "context_updates": self._extract_context_changes(context),
            "reflection_quality": self._assess_reflection_quality(lessons, improvements)
        }
        
        # Store reflection
        self.reflection_history.append(reflection_record)
        self._maintain_reflection_history()
        
        # Update context with reflection results
        context["last_reflection"] = reflection_record
        context["reflection_count"] = len(self.reflection_history)
        
        print(f"Reflection: Identified {len(lessons)} lessons and {len(improvements)} improvements")
        
        return context
    
    def _analyze_outcome(self, action_outcome: Dict, context: Dict) -> Dict:
        """Analyzes action outcome for learning opportunities"""
        
        status = action_outcome.get("status", "unknown")
        execution_time = action_outcome.get("execution_time", 0)
        results = action_outcome.get("results", [])
        
        analysis = {
            "success_level": self._calculate_success_level(action_outcome),
            "efficiency_score": self._calculate_efficiency_score(action_outcome, context),
            "completeness": self._assess_completeness(action_outcome, context),
            "error_patterns": self._identify_error_patterns(action_outcome),
            "success_factors": self._identify_success_factors(action_outcome),
            "performance_metrics": {
                "execution_time": execution_time,
                "steps_completed": len(results) if results else 0,
                "error_rate": self._calculate_error_rate(results)
            }
        }
        
        return analysis
    
    def _extract_lessons(self, action_outcome: Dict, analysis: Dict, context: Dict) -> List[Dict]:
        """Extracts specific lessons from the outcome analysis"""
        
        lessons = []
        
        # Success-based lessons
        if analysis["success_level"] > 0.7:
            lessons.append({
                "type": "success_pattern",
                "lesson": "Current approach is effective for this type of task",
                "evidence": f"Success level: {analysis['success_level']:.2f}",
                "applicability": "similar_tasks",
                "confidence": 0.8
            })
            
            if analysis["efficiency_score"] > 0.8:
                lessons.append({
                    "type": "efficiency_pattern",
                    "lesson": "This execution method is highly efficient",
                    "evidence": f"Efficiency score: {analysis['efficiency_score']:.2f}",
                    "applicability": "optimization_tasks",
                    "confidence": 0.9
                })
        
        # Failure-based lessons
        elif analysis["success_level"] < 0.3:
            lessons.append({
                "type": "failure_pattern",
                "lesson": "Current approach needs significant improvement",
                "evidence": f"Success level: {analysis['success_level']:.2f}",
                "applicability": "similar_tasks",
                "confidence": 0.9
            })
            
            # Extract specific failure lessons
            for error_pattern in analysis.get("error_patterns", []):
                lessons.append({
                    "type": "error_prevention",
                    "lesson": f"Avoid {error_pattern['type']} in future executions",
                    "evidence": error_pattern.get("description", ""),
                    "applicability": "all_tasks",
                    "confidence": 0.7
                })
        
        # Performance lessons
        performance = analysis.get("performance_metrics", {})
        if performance.get("execution_time", 0) > 60:  # Over 1 minute
            lessons.append({
                "type": "performance_optimization",
                "lesson": "Consider breaking long tasks into smaller steps",
                "evidence": f"Execution time: {performance['execution_time']:.1f}s",
                "applicability": "complex_tasks",
                "confidence": 0.6
            })
        
        # Context-based lessons
        goal = context.get("goal", "").lower()
        if "bootstrap" in goal and analysis["completeness"] > 0.8:
            lessons.append({
                "type": "bootstrap_strategy",
                "lesson": "Current bootstrap approach is working well",
                "evidence": f"Completeness: {analysis['completeness']:.2f}",
                "applicability": "initialization_tasks",
                "confidence": 0.8
            })
        
        return lessons
    
    def _identify_improvements(self, analysis: Dict, lessons: List[Dict]) -> List[Dict]:
        """Identifies specific improvements based on analysis and lessons"""
        
        improvements = []
        
        # Performance improvements
        if analysis.get("efficiency_score", 0) < 0.5:
            improvements.append({
                "type": "performance",
                "description": "Optimize execution pipeline for better performance",
                "priority": "high",
                "implementation": "analyze_bottlenecks_and_parallelize",
                "expected_impact": 0.7
            })
        
        # Error handling improvements
        error_patterns = analysis.get("error_patterns", [])
        if len(error_patterns) > 2:
            improvements.append({
                "type": "error_handling",
                "description": "Enhance error detection and recovery mechanisms",
                "priority": "high",
                "implementation": "add_comprehensive_error_checking",
                "expected_impact": 0.8
            })
        
        # Completeness improvements
        if analysis.get("completeness", 0) < 0.7:
            improvements.append({
                "type": "completeness",
                "description": "Improve task completion rates through better planning",
                "priority": "medium",
                "implementation": "enhance_plan_validation_and_step_verification",
                "expected_impact": 0.6
            })
        
        # Learning-based improvements
        for lesson in lessons:
            if lesson["type"] == "failure_pattern" and lesson["confidence"] > 0.8:
                improvements.append({
                    "type": "learning",
                    "description": f"Implement prevention for: {lesson['lesson']}",
                    "priority": "medium",
                    "implementation": f"add_validation_rule_for_{lesson['type']}",
                    "expected_impact": 0.5
                })
        
        # Meta-improvements based on reflection history
        if len(self.reflection_history) > 3:
            meta_improvements = self._identify_meta_improvements()
            improvements.extend(meta_improvements)
        
        return improvements
    
    def _update_learning_patterns(self, context: Dict, lessons: List[Dict], improvements: List[Dict]) -> Dict:
        """Updates learning patterns based on lessons and improvements"""
        
        # Update success patterns
        success_lessons = [l for l in lessons if l["type"] == "success_pattern"]
        for lesson in success_lessons:
            if "success_patterns" not in context:
                context["success_patterns"] = []
            
            pattern_exists = any(
                p.get("pattern") == lesson["lesson"] 
                for p in context["success_patterns"]
            )
            
            if not pattern_exists:
                context["success_patterns"].append({
                    "pattern": lesson["lesson"],
                    "evidence": lesson["evidence"],
                    "confidence": lesson["confidence"],
                    "learned_at": datetime.now().isoformat(),
                    "application_count": 0
                })
        
        # Update failure patterns for avoidance
        failure_lessons = [l for l in lessons if l["type"] == "failure_pattern"]
        for lesson in failure_lessons:
            if "failure_patterns" not in context:
                context["failure_patterns"] = []
            
            context["failure_patterns"].append({
                "pattern": lesson["lesson"],
                "evidence": lesson["evidence"],
                "confidence": lesson["confidence"],
                "learned_at": datetime.now().isoformat()
            })
        
        # Update optimization knowledge
        optimization_lessons = [l for l in lessons if "optimization" in l["type"]]
        for lesson in optimization_lessons:
            if "optimization_knowledge" not in context:
                context["optimization_knowledge"] = []
            
            context["optimization_knowledge"].append({
                "technique": lesson["lesson"],
                "evidence": lesson["evidence"],
                "confidence": lesson["confidence"],
                "learned_at": datetime.now().isoformat()
            })
        
        return context
    
    def _apply_immediate_improvements(self, context: Dict, improvements: List[Dict]) -> Dict:
        """Applies improvements that can be implemented immediately"""
        
        applied_improvements = []
        
        for improvement in improvements:
            if improvement.get("priority") == "high" and improvement.get("expected_impact", 0) > 0.6:
                # Apply high-impact improvements immediately
                applied = self._apply_single_improvement(improvement, context)
                if applied:
                    applied_improvements.append(improvement)
        
        # Update context with applied improvements
        if applied_improvements:
            if "applied_improvements" not in context:
                context["applied_improvements"] = []
            
            context["applied_improvements"].extend(applied_improvements)
            
            print(f"Reflection: Applied {len(applied_improvements)} immediate improvements")
        
        return context
    
    def _trigger_meta_learning(self, context: Dict) -> Dict:
        """Triggers meta-learning analysis across multiple reflections"""
        
        print("Reflection: Triggering meta-learning analysis")
        
        # Analyze patterns across reflection history
        meta_patterns = self._analyze_reflection_patterns()
        
        # Generate meta-insights
        meta_insights = self._generate_meta_insights(meta_patterns)
        
        # Update system-level learning
        context = self._update_system_learning(context, meta_insights)
        
        # Reset counter for next meta-learning cycle
        self.reflection_history = self.reflection_history[-self.meta_learning_threshold:]
        
        return context
    
    def _calculate_success_level(self, action_outcome: Dict) -> float:
        """Calculates overall success level of an action"""
        
        status = action_outcome.get("status", "unknown")
        results = action_outcome.get("results", [])
        
        if status == "success":
            return 1.0
        elif status == "partial_failure":
            # Calculate based on successful steps
            if results:
                successful_steps = sum(1 for r in results if r.get("status") == "success")
                return successful_steps / len(results)
            else:
                return 0.5
        elif status == "error" or status == "blocked":
            return 0.0
        else:
            return 0.3  # Unknown status gets low score
    
    def _calculate_efficiency_score(self, action_outcome: Dict, context: Dict) -> float:
        """Calculates efficiency score based on time and resources used"""
        
        execution_time = action_outcome.get("execution_time", 0)
        results = action_outcome.get("results", [])
        
        if not results:
            return 0.1
        
        # Calculate steps per second as efficiency metric
        steps_per_second = len(results) / max(execution_time, 1)
        
        # Normalize to 0-1 scale (assuming 1 step per second is perfect)
        efficiency = min(1.0, steps_per_second)
        
        return efficiency
    
    def _assess_completeness(self, action_outcome: Dict, context: Dict) -> float:
        """Assesses how completely the action fulfilled its intended purpose"""
        
        total_steps = action_outcome.get("total_steps", 0)
        steps_executed = action_outcome.get("steps_executed", 0)
        
        if total_steps == 0:
            return 0.5  # Unknown total
        
        return steps_executed / total_steps
    
    def _identify_error_patterns(self, action_outcome: Dict) -> List[Dict]:
        """Identifies error patterns from the action outcome"""
        
        patterns = []
        results = action_outcome.get("results", [])
        
        # Count error types
        error_types = {}
        for result in results:
            if result.get("status") == "error":
                error_msg = result.get("error", "unknown_error")
                error_type = self._classify_error_type(error_msg)
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Create patterns for frequent errors
        for error_type, count in error_types.items():
            if count > 1:  # Pattern if occurs more than once
                patterns.append({
                    "type": error_type,
                    "frequency": count,
                    "description": f"Recurring {error_type} errors",
                    "pattern_strength": min(1.0, count / len(results))
                })
        
        return patterns
    
    def _classify_error_type(self, error_message: str) -> str:
        """Classifies error type from error message"""
        
        error_msg_lower = error_message.lower()
        
        if "file" in error_msg_lower and ("not found" in error_msg_lower or "no such" in error_msg_lower):
            return "file_not_found"
        elif "permission" in error_msg_lower or "access" in error_msg_lower:
            return "permission_error"
        elif "timeout" in error_msg_lower:
            return "timeout_error"
        elif "connection" in error_msg_lower or "network" in error_msg_lower:
            return "network_error"
        elif "syntax" in error_msg_lower or "invalid" in error_msg_lower:
            return "syntax_error"
        elif "memory" in error_msg_lower or "out of" in error_msg_lower:
            return "resource_error"
        else:
            return "unknown_error"
    
    def _generate_reflection_id(self, context: Dict, action_outcome: Dict) -> str:
        """Generates unique ID for reflection session"""
        
        content = f"{context.get('goal', '')}{action_outcome.get('status', '')}{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:10]
    
    def _maintain_reflection_history(self) -> None:
        """Maintains reflection history within reasonable bounds"""
        
        # Keep only last 20 reflections in memory
        if len(self.reflection_history) > 20:
            self.reflection_history = self.reflection_history[-20:]
    
    def _load_learning_rules(self) -> Dict:
        """Loads learning rules and patterns"""
        
        return {
            "success_reinforcement": {
                "threshold": 0.8,
                "action": "increase_pattern_confidence"
            },
            "failure_learning": {
                "threshold": 0.3,
                "action": "create_avoidance_pattern"
            },
            "efficiency_optimization": {
                "threshold": 0.5,
                "action": "analyze_bottlenecks"
            },
            "meta_learning_trigger": {
                "reflection_count": 5,
                "action": "analyze_reflection_patterns"
            }
        }


def reflect(context: Dict, action_outcome: Dict) -> Dict:
    """Main reflection function - wrapper for ReflectionEngine"""
    
    # Create or get existing reflection engine
    if not hasattr(reflect, '_engine'):
        reflect._engine = ReflectionEngine()
    
    return reflect._engine.reflect(context, action_outcome)


if __name__ == "__main__":
    # Test the reflection system
    test_context = {
        "goal": "Test reflection capabilities",
        "evolution_count": 5
    }
    
    test_outcome = {
        "status": "success",
        "execution_time": 15.0,
        "steps_executed": 3,
        "total_steps": 3,
        "results": [
            {"status": "success", "message": "Step 1 completed"},
            {"status": "success", "message": "Step 2 completed"},
            {"status": "success", "message": "Step 3 completed"}
        ]
    }
    
    result_context = reflect(test_context, test_outcome)
    
    print(f"Reflection completed. Context updated with:")
    print(f"- Reflection count: {result_context.get('reflection_count', 0)}")
    print(f"- Last reflection quality: {result_context.get('last_reflection', {}).get('reflection_quality', 'N/A')}")
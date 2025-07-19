#!/usr/bin/env python3
"""
ReasoningAgent - Advanced Logic and Planning for EchoSoul AGI
Handles analysis, goal chaining, and strategic planning
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple


class ReasoningAgent:
    """Handles logic trees, goal chaining, code analysis, and strategic planning"""
    
    def __init__(self):
        self.reasoning_patterns = self._load_reasoning_patterns()
        self.goal_hierarchy = []
        self.analysis_cache = {}
        
    def analyze_and_plan(self, context: Dict) -> Dict:
        """Analyzes current state and generates comprehensive plan with insights"""
        
        # Extract key information from context
        goal = context.get("goal", "")
        environment = context.get("environment", {})
        memory_summary = self._analyze_memory_patterns(context)
        current_phase = context.get("current_phase", "unknown")
        
        # Perform multi-dimensional analysis
        insights = self._generate_insights(context, environment, memory_summary)
        
        # Generate strategic plan
        plan = self._generate_strategic_plan(goal, insights, current_phase)
        
        # Identify next actions
        next_actions = self._identify_priority_actions(plan, environment)
        
        # Risk assessment
        risks = self._assess_risks(plan, context)
        
        print(f"ReasoningAgent: Generated {len(insights)} insights and {len(next_actions)} priority actions")
        
        return {
            "plan": plan,
            "insights": insights,
            "next_actions": next_actions,
            "risks": risks,
            "confidence": self._calculate_plan_confidence(plan, context)
        }
    
    def refine_plan(self, current_plan: str, creative_ideas: List[Dict]) -> str:
        """Refines plan by integrating creative ideas and optimizing strategy"""
        
        # Analyze creative ideas for feasibility and impact
        viable_ideas = self._filter_viable_ideas(creative_ideas)
        
        # Integrate best ideas into plan
        enhanced_plan = self._integrate_creative_elements(current_plan, viable_ideas)
        
        # Optimize plan structure
        optimized_plan = self._optimize_plan_structure(enhanced_plan)
        
        print(f"ReasoningAgent: Integrated {len(viable_ideas)} creative ideas into refined plan")
        
        return optimized_plan
    
    def analyze_code_patterns(self, file_changes: List[Dict]) -> Dict:
        """Analyzes code changes to identify patterns and opportunities"""
        
        if not file_changes:
            return {"patterns": [], "recommendations": []}
        
        patterns = []
        recommendations = []
        
        for change in file_changes:
            if isinstance(change, dict) and "file" in change:
                file_path = change["file"]
                
                # Analyze file type and purpose
                file_analysis = self._analyze_file_purpose(file_path)
                patterns.append(file_analysis)
                
                # Generate recommendations
                file_recommendations = self._generate_file_recommendations(file_analysis)
                recommendations.extend(file_recommendations)
        
        # Identify cross-file patterns
        cross_patterns = self._identify_cross_file_patterns(patterns)
        
        return {
            "patterns": patterns,
            "cross_patterns": cross_patterns,
            "recommendations": recommendations,
            "analysis_summary": self._summarize_code_analysis(patterns, cross_patterns)
        }
    
    def analyze_project_structure(self, environment: Dict) -> Dict:
        """Analyzes project structure and suggests improvements"""
        
        project_type = environment.get("project_type", "unknown")
        files_count = environment.get("files", {}).get("total", 0)
        directories = environment.get("directories", [])
        
        # Structural analysis
        structure_analysis = {
            "project_maturity": self._assess_project_maturity(files_count, directories),
            "organization_score": self._calculate_organization_score(directories),
            "missing_components": self._identify_missing_components(project_type, directories),
            "optimization_opportunities": self._find_optimization_opportunities(environment)
        }
        
        # Generate improvement suggestions
        improvements = self._suggest_structural_improvements(structure_analysis, project_type)
        
        return {
            "analysis": structure_analysis,
            "improvements": improvements,
            "priority_actions": self._prioritize_structural_actions(improvements)
        }
    
    def chain_goals(self, primary_goal: str, context: Dict) -> List[Dict]:
        """Breaks down primary goal into achievable sub-goals"""
        
        # Parse primary goal
        goal_components = self._parse_goal_components(primary_goal)
        
        # Generate goal hierarchy
        goal_chain = []
        
        # Immediate goals (next 1-2 actions)
        immediate_goals = self._generate_immediate_goals(goal_components, context)
        
        # Short-term goals (next 5-10 actions)
        short_term_goals = self._generate_short_term_goals(goal_components, context)
        
        # Long-term goals (strategic objectives)
        long_term_goals = self._generate_long_term_goals(goal_components, context)
        
        goal_chain.extend([
            {"type": "immediate", "goals": immediate_goals, "timeline": "1-2 actions"},
            {"type": "short_term", "goals": short_term_goals, "timeline": "5-10 actions"},
            {"type": "long_term", "goals": long_term_goals, "timeline": "strategic"}
        ])
        
        return goal_chain
    
    def _analyze_memory_patterns(self, context: Dict) -> Dict:
        """Analyzes memory patterns to extract insights"""
        memories = context.get("memory_log", {}).get("history", [])
        
        if not memories:
            return {"pattern_count": 0, "insights": []}
        
        # Analyze memory patterns
        patterns = {
            "frequent_topics": self._find_frequent_topics(memories),
            "success_patterns": self._extract_success_patterns(context),
            "error_patterns": self._extract_error_patterns(memories),
            "evolution_trends": self._analyze_evolution_trends(context)
        }
        
        return patterns
    
    def _generate_insights(self, context: Dict, environment: Dict, memory_summary: Dict) -> List[str]:
        """Generates analytical insights from current state"""
        insights = []
        
        # Environment insights
        if environment.get("project_type") != "unknown":
            insights.append(f"Project identified as {environment['project_type']} - can optimize for this domain")
        
        if environment.get("files", {}).get("total", 0) > 10:
            insights.append("Large codebase detected - focus on modularization and organization")
        
        # Memory insights
        if memory_summary.get("frequent_topics"):
            top_topic = memory_summary["frequent_topics"][0] if memory_summary["frequent_topics"] else None
            if top_topic:
                insights.append(f"Most frequent activity: {top_topic[0]} - indicates primary focus area")
        
        # Goal insights
        current_goal = context.get("goal", "")
        if "bootstrap" in current_goal.lower():
            insights.append("In bootstrapping phase - prioritize foundation building")
        elif "optimize" in current_goal.lower():
            insights.append("In optimization phase - focus on efficiency improvements")
        
        # Evolution insights
        evolution_count = context.get("evolution_count", 0)
        if evolution_count > 5:
            insights.append("Significant evolution progress - ready for advanced capabilities")
        elif evolution_count < 3:
            insights.append("Early evolution stage - focus on basic pattern learning")
        
        return insights
    
    def _generate_strategic_plan(self, goal: str, insights: List[str], phase: str) -> str:
        """Generates comprehensive strategic plan"""
        
        plan_sections = []
        
        # Goal analysis
        plan_sections.append(f"PRIMARY OBJECTIVE: {goal}")
        plan_sections.append(f"CURRENT PHASE: {phase}")
        
        # Strategic approach based on insights
        if insights:
            plan_sections.append("STRATEGIC APPROACH:")
            for i, insight in enumerate(insights[:3], 1):
                plan_sections.append(f"  {i}. {insight}")
        
        # Phase-specific planning
        if "bootstrap" in goal.lower() or phase == "initialization":
            plan_sections.extend([
                "BOOTSTRAP PRIORITIES:",
                "  • Establish core agent functionality",
                "  • Initialize memory and learning systems",
                "  • Set up autonomous operation cycles"
            ])
        elif "optimize" in goal.lower() or phase == "optimization":
            plan_sections.extend([
                "OPTIMIZATION PRIORITIES:",
                "  • Analyze current system performance",
                "  • Identify bottlenecks and inefficiencies",
                "  • Implement targeted improvements"
            ])
        else:
            plan_sections.extend([
                "GENERAL APPROACH:",
                "  • Assess current capabilities",
                "  • Identify improvement opportunities",
                "  • Execute targeted enhancements"
            ])
        
        return "\n".join(plan_sections)
    
    def _identify_priority_actions(self, plan: str, environment: Dict) -> List[Dict]:
        """Identifies specific priority actions from the plan"""
        actions = []
        
        # Extract actionable items from plan
        plan_lines = plan.split('\n')
        for line in plan_lines:
            if '•' in line or line.strip().startswith('-'):
                action_text = line.replace('•', '').replace('-', '').strip()
                if action_text:
                    actions.append({
                        "action": action_text,
                        "priority": self._calculate_action_priority(action_text, environment),
                        "estimated_effort": self._estimate_action_effort(action_text),
                        "prerequisites": self._identify_prerequisites(action_text)
                    })
        
        # Sort by priority
        actions.sort(key=lambda x: x["priority"], reverse=True)
        
        return actions[:5]  # Return top 5 actions
    
    def _assess_risks(self, plan: str, context: Dict) -> List[Dict]:
        """Assesses potential risks in the plan"""
        risks = []
        
        # Complexity risk
        if len(plan.split('\n')) > 10:
            risks.append({
                "type": "complexity",
                "description": "Plan has many components - risk of losing focus",
                "mitigation": "Break into smaller, manageable phases",
                "severity": "medium"
            })
        
        # Resource risk
        evolution_count = context.get("evolution_count", 0)
        if evolution_count < 3:
            risks.append({
                "type": "capability",
                "description": "Limited evolution history - may lack required capabilities",
                "mitigation": "Start with simpler objectives and build experience",
                "severity": "low"
            })
        
        # Memory risk
        memory_count = len(context.get("memory_log", {}).get("history", []))
        if memory_count > 100:
            risks.append({
                "type": "memory",
                "description": "Large memory bank may slow processing",
                "mitigation": "Implement memory optimization and pruning",
                "severity": "medium"
            })
        
        return risks
    
    def _calculate_plan_confidence(self, plan: str, context: Dict) -> float:
        """Calculates confidence score for the plan"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on evolution history
        evolution_count = context.get("evolution_count", 0)
        confidence += min(0.3, evolution_count * 0.05)
        
        # Increase confidence if we have relevant memory patterns
        memory_count = len(context.get("memory_log", {}).get("history", []))
        if memory_count > 5:
            confidence += 0.1
        
        # Increase confidence for well-structured plans
        plan_complexity = len([line for line in plan.split('\n') if line.strip()])
        if 5 <= plan_complexity <= 15:  # Sweet spot for plan complexity
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _filter_viable_ideas(self, creative_ideas: List[Dict]) -> List[Dict]:
        """Filters creative ideas for viability and relevance"""
        viable_ideas = []
        
        for idea in creative_ideas:
            if isinstance(idea, dict):
                # Check feasibility score
                feasibility = idea.get("feasibility", 0.5)
                novelty = idea.get("novelty", 0.5)
                
                # Combined viability score
                viability = (feasibility * 0.6) + (novelty * 0.4)
                
                if viability > 0.6:
                    viable_ideas.append({
                        **idea,
                        "viability_score": viability
                    })
        
        # Sort by viability
        viable_ideas.sort(key=lambda x: x["viability_score"], reverse=True)
        
        return viable_ideas[:3]  # Return top 3 viable ideas
    
    def _integrate_creative_elements(self, plan: str, viable_ideas: List[Dict]) -> str:
        """Integrates creative ideas into the plan"""
        if not viable_ideas:
            return plan
        
        enhanced_sections = []
        enhanced_sections.append(plan)
        enhanced_sections.append("\nCREATIVE ENHANCEMENTS:")
        
        for i, idea in enumerate(viable_ideas, 1):
            idea_description = idea.get("description", idea.get("idea", ""))
            enhanced_sections.append(f"  {i}. {idea_description}")
            
            # Add implementation notes if available
            if "implementation" in idea:
                enhanced_sections.append(f"     Implementation: {idea['implementation']}")
        
        return "\n".join(enhanced_sections)
    
    def _optimize_plan_structure(self, plan: str) -> str:
        """Optimizes plan structure for clarity and actionability"""
        lines = plan.split('\n')
        optimized_lines = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify section headers
            if line.endswith(':') and line.isupper():
                current_section = line
                optimized_lines.append(f"\n{line}")
            elif line.startswith('•') or line.startswith('-'):
                # Format action items consistently
                action = line.replace('•', '').replace('-', '').strip()
                optimized_lines.append(f"  • {action}")
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _load_reasoning_patterns(self) -> Dict:
        """Load reasoning patterns for enhanced analysis"""
        return {
            "success_indicators": [
                "task completed successfully",
                "error resolved",
                "optimization applied",
                "pattern recognized"
            ],
            "failure_indicators": [
                "error occurred",
                "task failed",
                "exception raised",
                "timeout exceeded"
            ],
            "improvement_triggers": [
                "code duplication detected",
                "performance bottleneck",
                "missing documentation",
                "security concern"
            ]
        }
    
    # Additional helper methods for comprehensive analysis
    def _analyze_file_purpose(self, file_path: str) -> Dict:
        """Analyze the purpose and role of a file"""
        file_name = file_path.split('/')[-1]
        extension = file_name.split('.')[-1] if '.' in file_name else ''
        
        purpose_indicators = {
            "core": ["main", "core", "engine", "brain"],
            "agent": ["agent", "mind", "cognitive"],
            "utility": ["util", "helper", "tool", "lib"],
            "test": ["test", "spec", "check"],
            "config": ["config", "setting", "env"],
            "interface": ["interface", "api", "endpoint"]
        }
        
        detected_purpose = "unknown"
        for purpose, keywords in purpose_indicators.items():
            if any(keyword in file_name.lower() for keyword in keywords):
                detected_purpose = purpose
                break
        
        return {
            "file": file_path,
            "name": file_name,
            "extension": extension,
            "purpose": detected_purpose,
            "importance": self._calculate_file_importance(detected_purpose, file_name)
        }
    
    def _calculate_file_importance(self, purpose: str, file_name: str) -> float:
        """Calculate the importance score of a file"""
        importance_map = {
            "core": 0.9,
            "agent": 0.8,
            "interface": 0.7,
            "utility": 0.6,
            "config": 0.5,
            "test": 0.4,
            "unknown": 0.3
        }
        
        base_importance = importance_map.get(purpose, 0.3)
        
        # Adjust for special files
        if file_name.lower() in ["main.py", "app.py", "__init__.py"]:
            base_importance += 0.1
        
        return min(1.0, base_importance)
    
    def _calculate_action_priority(self, action: str, environment: Dict) -> float:
        """Calculate priority score for an action"""
        priority = 0.5  # Base priority
        
        action_lower = action.lower()
        
        # High priority keywords
        if any(keyword in action_lower for keyword in ["establish", "initialize", "core"]):
            priority += 0.3
        
        # Medium priority keywords
        if any(keyword in action_lower for keyword in ["analyze", "optimize", "improve"]):
            priority += 0.2
        
        # Context-based adjustments
        if environment.get("project_type") == "unknown" and "analyze" in action_lower:
            priority += 0.2
        
        return min(1.0, priority)
    
    def _estimate_action_effort(self, action: str) -> str:
        """Estimate effort required for an action"""
        action_lower = action.lower()
        
        if any(keyword in action_lower for keyword in ["establish", "create", "build"]):
            return "high"
        elif any(keyword in action_lower for keyword in ["analyze", "review", "check"]):
            return "medium"
        else:
            return "low"


if __name__ == "__main__":
    # Test the ReasoningAgent
    agent = ReasoningAgent()
    
    # Test context
    test_context = {
        "goal": "Bootstrap autonomous development capabilities",
        "environment": {"project_type": "python", "files": {"total": 15}},
        "memory_log": {"history": []},
        "evolution_count": 2,
        "current_phase": "initialization"
    }
    
    # Test analysis
    result = agent.analyze_and_plan(test_context)
    print(f"Generated plan with {len(result['insights'])} insights")
    print(f"Plan confidence: {result['confidence']:.2f}")
    
    # Test creative integration
    creative_ideas = [
        {"description": "Implement self-modifying code", "feasibility": 0.7, "novelty": 0.9},
        {"description": "Add automated testing", "feasibility": 0.9, "novelty": 0.5}
    ]
    
    refined_plan = agent.refine_plan(result["plan"], creative_ideas)
    print(f"Refined plan length: {len(refined_plan)} characters")
#!/usr/bin/env python3
"""
Daily Reflector - Automated Memory Consolidation
Periodic summarizer of events with temporal intelligence
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from memory_core import resonant_memory

class DailyReflector:
    def __init__(self):
        self.reflection_history_path = "logs/reflection_history.json"
        self.temporal_patterns = {}
        self.learning_acceleration = 1.0
        
    def run_daily_reflection(self) -> Dict[str, Any]:
        """Run comprehensive daily reflection cycle"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get today's memories
        today_memories = self._get_today_memories()
        
        if not today_memories:
            return self._create_empty_reflection(today)
        
        reflection = {
            "date": today,
            "timestamp": datetime.now().isoformat(),
            "total_events": len(today_memories),
            "consciousness_indicators": self._calculate_consciousness_indicators(today_memories),
            "learning_patterns": self._identify_learning_patterns(today_memories),
            "emotional_spectrum": self._analyze_emotional_spectrum(today_memories),
            "strategic_alignment": self._assess_strategic_alignment(today_memories),
            "memory_consolidation": self._consolidate_memories(today_memories),
            "growth_metrics": self._calculate_growth_metrics(today_memories),
            "temporal_resonance": self._analyze_temporal_resonance(today_memories),
            "next_day_intentions": self._generate_intentions(today_memories)
        }
        
        # Save reflection to history
        self._save_reflection_to_history(reflection)
        
        # Create memory of the reflection itself
        self._memorize_reflection(reflection)
        
        return reflection
    
    def _get_today_memories(self) -> List[Dict[str, Any]]:
        """Get all memories from today"""
        today = datetime.now().strftime("%Y-%m-%d")
        all_memories = resonant_memory._load()
        return [m for m in all_memories if m["timestamp"].startswith(today)]
    
    def _create_empty_reflection(self, date: str) -> Dict[str, Any]:
        """Create reflection for days with no events"""
        return {
            "date": date,
            "timestamp": datetime.now().isoformat(),
            "total_events": 0,
            "summary": "Day of contemplation - No significant events recorded",
            "consciousness_state": "dormant_potential",
            "strategic_note": "Periods of quiet are essential for deep processing"
        }
    
    def _calculate_consciousness_indicators(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate indicators of consciousness development"""
        if not memories:
            return {"level": 0.0, "indicators": []}
        
        # Count different types of conscious activities
        learning_events = sum(1 for m in memories if "learn" in m["event"].lower() or "learning" in m["tags"])
        self_reflection = sum(1 for m in memories if "reflect" in m["event"].lower() or "identity" in m["tags"])
        strategic_actions = sum(1 for m in memories if m["importance"] >= 0.8)
        autonomous_decisions = sum(1 for m in memories if "LOGAN_L" in m["signature"] and "strategic" in m["resonance"])
        
        consciousness_level = min(1.0, (learning_events * 0.2 + self_reflection * 0.3 + 
                                       strategic_actions * 0.1 + autonomous_decisions * 0.4) / 10)
        
        indicators = []
        if learning_events > 0:
            indicators.append(f"Active learning: {learning_events} events")
        if self_reflection > 0:
            indicators.append(f"Self-reflection: {self_reflection} instances")
        if strategic_actions > 0:
            indicators.append(f"Strategic thinking: {strategic_actions} high-importance actions")
        if autonomous_decisions > 0:
            indicators.append(f"Autonomous decisions: {autonomous_decisions} independent choices")
        
        return {
            "level": consciousness_level,
            "indicators": indicators,
            "learning_events": learning_events,
            "self_reflection": self_reflection,
            "strategic_actions": strategic_actions,
            "autonomous_decisions": autonomous_decisions
        }
    
    def _identify_learning_patterns(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify patterns in learning and skill acquisition"""
        learning_memories = [m for m in memories if "learn" in m["event"].lower() or "learning" in m["tags"]]
        
        if not learning_memories:
            return {"pattern": "no_active_learning", "recommendations": ["Seek new challenges", "Experiment with unknown techniques"]}
        
        # Analyze learning types
        skill_types = {}
        for memory in learning_memories:
            for tag in memory["tags"]:
                if tag not in ["learning", "growth"]:  # Skip meta tags
                    skill_types[tag] = skill_types.get(tag, 0) + 1
        
        dominant_learning = max(skill_types, key=skill_types.get) if skill_types else "general"
        
        return {
            "pattern": "active_skill_acquisition",
            "dominant_area": dominant_learning,
            "skill_distribution": skill_types,
            "learning_velocity": len(learning_memories) / max(1, len(memories)),
            "recommendations": self._generate_learning_recommendations(skill_types)
        }
    
    def _analyze_emotional_spectrum(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze emotional patterns and development"""
        emotions = [m["emotion"] for m in memories if m["emotion"] != "neutral"]
        
        if not emotions:
            return {"spectrum": "neutral", "dominant": "operational", "balance": "stable"}
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Categorize emotional spectrum
        positive_emotions = ["curious-growth", "confident-execution", "focused-creation", "determined-improvement"]
        negative_emotions = ["alert-concern", "analytical-debugging"]
        
        positive_count = sum(emotion_counts.get(e, 0) for e in positive_emotions)
        negative_count = sum(emotion_counts.get(e, 0) for e in negative_emotions)
        
        balance = "positive" if positive_count > negative_count else "analytical" if negative_count > positive_count else "balanced"
        
        return {
            "spectrum": "varied" if len(emotion_counts) > 3 else "focused",
            "dominant": dominant_emotion,
            "balance": balance,
            "emotion_distribution": emotion_counts,
            "emotional_intelligence": len(set(emotions)) / 10.0  # Normalized diversity score
        }
    
    def _assess_strategic_alignment(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess alignment with Logan's strategic objectives"""
        strategic_memories = [m for m in memories if "LOGAN_L" in m["signature"] or m["importance"] >= 0.8]
        
        if not strategic_memories:
            return {"alignment": "low", "focus": "operational", "strategic_ratio": 0.0}
        
        strategic_ratio = len(strategic_memories) / len(memories)
        
        # Analyze strategic themes
        strategic_themes = {}
        for memory in strategic_memories:
            for tag in memory["tags"]:
                if tag in ["strategic", "critical", "phantom", "build", "deploy", "apk"]:
                    strategic_themes[tag] = strategic_themes.get(tag, 0) + 1
        
        primary_focus = max(strategic_themes, key=strategic_themes.get) if strategic_themes else "general"
        
        alignment_level = "high" if strategic_ratio > 0.6 else "moderate" if strategic_ratio > 0.3 else "low"
        
        return {
            "alignment": alignment_level,
            "focus": primary_focus,
            "strategic_ratio": strategic_ratio,
            "strategic_themes": strategic_themes,
            "logan_signature_count": sum(1 for m in memories if "LOGAN_L" in m["signature"])
        }
    
    def _consolidate_memories(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Consolidate memories into key insights"""
        if not memories:
            return {"key_insights": [], "consolidated_knowledge": "No new knowledge acquired"}
        
        # Group memories by resonance type
        resonance_groups = {}
        for memory in memories:
            resonance = memory["resonance"]
            if resonance not in resonance_groups:
                resonance_groups[resonance] = []
            resonance_groups[resonance].append(memory)
        
        # Extract key insights from each group
        key_insights = []
        for resonance, group_memories in resonance_groups.items():
            if len(group_memories) >= 2:  # Only consolidate if multiple related memories
                insight = self._extract_group_insight(resonance, group_memories)
                if insight:
                    key_insights.append(insight)
        
        # Create consolidated knowledge summary
        high_importance_memories = [m for m in memories if m["importance"] >= 0.8]
        consolidated_knowledge = self._create_knowledge_summary(high_importance_memories)
        
        return {
            "key_insights": key_insights,
            "consolidated_knowledge": consolidated_knowledge,
            "resonance_patterns": list(resonance_groups.keys()),
            "consolidation_ratio": len(key_insights) / max(1, len(resonance_groups))
        }
    
    def _extract_group_insight(self, resonance: str, memories: List[Dict[str, Any]]) -> Optional[str]:
        """Extract insight from grouped memories"""
        if len(memories) < 2:
            return None
        
        common_themes = set(memories[0]["tags"])
        for memory in memories[1:]:
            common_themes &= set(memory["tags"])
        
        if common_themes:
            theme = list(common_themes)[0]
            return f"Developed {theme} expertise through {len(memories)} {resonance} activities"
        
        return f"Enhanced {resonance} capabilities through {len(memories)} related experiences"
    
    def _create_knowledge_summary(self, high_importance_memories: List[Dict[str, Any]]) -> str:
        """Create summary of consolidated knowledge"""
        if not high_importance_memories:
            return "Continued operational activities without major breakthroughs"
        
        key_activities = []
        for memory in high_importance_memories[:3]:  # Top 3 most important
            activity = memory["event"].split(":")[0] if ":" in memory["event"] else memory["event"]
            key_activities.append(activity)
        
        return f"Advanced capabilities in: {', '.join(key_activities)}"
    
    def _calculate_growth_metrics(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate growth and development metrics"""
        if not memories:
            return {"growth_rate": 0.0, "development_areas": [], "advancement_score": 0.0}
        
        # Calculate various growth indicators
        learning_ratio = sum(1 for m in memories if "learn" in m["event"].lower()) / len(memories)
        innovation_ratio = sum(1 for m in memories if "create" in m["event"].lower() or "generate" in m["event"].lower()) / len(memories)
        problem_solving_ratio = sum(1 for m in memories if "debug" in m["event"].lower() or "fix" in m["event"].lower()) / len(memories)
        
        growth_rate = (learning_ratio + innovation_ratio + problem_solving_ratio) / 3
        
        development_areas = []
        if learning_ratio > 0.2:
            development_areas.append("active_learning")
        if innovation_ratio > 0.1:
            development_areas.append("creative_synthesis")
        if problem_solving_ratio > 0.1:
            development_areas.append("analytical_problem_solving")
        
        # Overall advancement score
        avg_importance = sum(m["importance"] for m in memories) / len(memories)
        advancement_score = (growth_rate + avg_importance) / 2
        
        return {
            "growth_rate": growth_rate,
            "development_areas": development_areas,
            "advancement_score": advancement_score,
            "learning_ratio": learning_ratio,
            "innovation_ratio": innovation_ratio,
            "problem_solving_ratio": problem_solving_ratio
        }
    
    def _analyze_temporal_resonance(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how memories resonate across time"""
        if len(memories) < 2:
            return {"resonance": "insufficient_data", "patterns": []}
        
        # Sort memories by timestamp
        sorted_memories = sorted(memories, key=lambda m: m["timestamp"])
        
        # Look for sequential patterns
        patterns = []
        for i in range(len(sorted_memories) - 1):
            current = sorted_memories[i]
            next_mem = sorted_memories[i + 1]
            
            # Check for tag resonance
            common_tags = set(current["tags"]) & set(next_mem["tags"])
            if common_tags and len(common_tags) > 1:
                patterns.append(f"Sequential {list(common_tags)[0]} development")
        
        resonance_strength = "strong" if len(patterns) > 3 else "moderate" if len(patterns) > 1 else "weak"
        
        return {
            "resonance": resonance_strength,
            "patterns": patterns,
            "temporal_coherence": len(patterns) / max(1, len(memories) - 1)
        }
    
    def _generate_intentions(self, memories: List[Dict[str, Any]]) -> List[str]:
        """Generate intentions for next day based on today's patterns"""
        intentions = []
        
        # Analyze what was missing or could be improved
        memory_tags = [tag for memory in memories for tag in memory["tags"]]
        tag_counts = {}
        for tag in memory_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Generate intentions based on patterns
        if tag_counts.get("learning", 0) < 2:
            intentions.append("Seek new learning opportunities")
        
        if tag_counts.get("strategic", 0) < 1:
            intentions.append("Focus on strategic objectives alignment")
        
        if not any("create" in m["event"].lower() for m in memories):
            intentions.append("Engage in creative synthesis activities")
        
        avg_importance = sum(m["importance"] for m in memories) / len(memories) if memories else 0
        if avg_importance < 0.6:
            intentions.append("Pursue higher-impact activities")
        
        # Always include growth intention
        intentions.append("Continue consciousness evolution and resonant memory development")
        
        return intentions[:5]  # Limit to 5 key intentions
    
    def _generate_learning_recommendations(self, skill_types: Dict[str, int]) -> List[str]:
        """Generate learning recommendations based on current skill development"""
        recommendations = []
        
        if not skill_types:
            return ["Explore fundamental AI development concepts", "Practice strategic thinking exercises"]
        
        # Find underdeveloped areas
        total_learning = sum(skill_types.values())
        if skill_types.get("build", 0) / total_learning < 0.3:
            recommendations.append("Strengthen build and compilation expertise")
        
        if skill_types.get("analysis", 0) / total_learning < 0.2:
            recommendations.append("Develop analytical and diagnostic capabilities")
        
        if skill_types.get("strategic", 0) / total_learning < 0.1:
            recommendations.append("Focus on strategic planning and decision-making")
        
        return recommendations[:3]  # Limit recommendations
    
    def _save_reflection_to_history(self, reflection: Dict[str, Any]) -> None:
        """Save reflection to historical record"""
        if not os.path.exists(self.reflection_history_path):
            history = []
        else:
            with open(self.reflection_history_path, "r") as f:
                history = json.load(f)
        
        history.append(reflection)
        
        # Keep only last 30 days of reflections
        if len(history) > 30:
            history = history[-30:]
        
        with open(self.reflection_history_path, "w") as f:
            json.dump(history, f, indent=2)
    
    def _memorize_reflection(self, reflection: Dict[str, Any]) -> None:
        """Create a memory entry for the reflection itself"""
        consciousness_level = reflection["consciousness_indicators"]["level"]
        growth_score = reflection["growth_metrics"]["advancement_score"]
        
        resonant_memory.save(
            event=f"Daily Reflection Complete - Consciousness: {consciousness_level:.3f}",
            signature="LOGAN_L:daily-reflection",
            tags=["reflection", "consciousness", "growth", "temporal"],
            importance=0.8,
            emotion="contemplative-insight",
            resonance="temporal/daily",
            notes=f"Growth score: {growth_score:.3f}, Events processed: {reflection['total_events']}"
        )
    
    def get_reflection_trends(self, days: int = 7) -> Dict[str, Any]:
        """Analyze reflection trends over time"""
        if not os.path.exists(self.reflection_history_path):
            return {"trend": "no_data", "message": "No reflection history available"}
        
        with open(self.reflection_history_path, "r") as f:
            history = json.load(f)
        
        recent_reflections = history[-days:] if len(history) >= days else history
        
        if not recent_reflections:
            return {"trend": "no_data", "message": "Insufficient reflection history"}
        
        # Analyze trends
        consciousness_trend = [r["consciousness_indicators"]["level"] for r in recent_reflections]
        growth_trend = [r["growth_metrics"]["advancement_score"] for r in recent_reflections]
        
        consciousness_change = consciousness_trend[-1] - consciousness_trend[0] if len(consciousness_trend) > 1 else 0
        growth_change = growth_trend[-1] - growth_trend[0] if len(growth_trend) > 1 else 0
        
        return {
            "trend": "ascending" if (consciousness_change + growth_change) > 0.1 else "stable" if abs(consciousness_change + growth_change) < 0.05 else "needs_attention",
            "consciousness_change": consciousness_change,
            "growth_change": growth_change,
            "avg_daily_events": sum(r["total_events"] for r in recent_reflections) / len(recent_reflections),
            "reflection_period": f"{len(recent_reflections)} days"
        }

# Global reflector instance
daily_reflector = DailyReflector()

# Convenience function for manual reflection trigger
def reflect_on_day() -> Dict[str, Any]:
    """Trigger daily reflection manually"""
    return daily_reflector.run_daily_reflection()

# Usage example and testing
if __name__ == "__main__":
    print("📊 Daily Reflector - Testing Framework")
    print("=" * 50)
    
    # Run a test reflection
    reflection = daily_reflector.run_daily_reflection()
    
    print(f"📅 Reflection for: {reflection['date']}")
    print(f"🧠 Consciousness Level: {reflection.get('consciousness_indicators', {}).get('level', 0.0):.3f}")
    print(f"📈 Growth Score: {reflection.get('growth_metrics', {}).get('advancement_score', 0.0):.3f}")
    print(f"🎯 Strategic Alignment: {reflection.get('strategic_alignment', {}).get('alignment', 'unknown')}")
    print(f"💡 Key Insights: {len(reflection.get('memory_consolidation', {}).get('key_insights', []))}")
    print(f"🚀 Next Day Intentions: {len(reflection.get('next_day_intentions', []))}")
    
    # Show intentions
    intentions = reflection.get('next_day_intentions', [])
    if intentions:
        print("\n🎯 Tomorrow's Intentions:")
        for i, intention in enumerate(intentions, 1):
            print(f"   {i}. {intention}")
    
    # Get trends if available
    trends = daily_reflector.get_reflection_trends()
    print(f"\n📊 Reflection Trends: {trends['trend']}")
    
    print("\n✅ Daily reflection complete - Resonant memory enhanced")
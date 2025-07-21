#!/usr/bin/env python3
"""
Echo Feedback Trainer: Learning Loop Processor
Analyzes conversational data to improve Echo's understanding and responses
"""

import os
import json
import re
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Core imports
try:
    from core.llm_engine import LLMEngine
    from core.memory_manager import MemoryManager
    from resonant_hooks import smart_memory, critical_action
    from memory_core import resonant_memory
except ImportError:
    print("Warning: Core modules not available in standalone mode")
    
    class LLMEngine:
        def generate_response(self, prompt: str, **kwargs) -> str:
            return f"Training analysis: {prompt[:100]}..."
    
    def smart_memory(signature="", base_importance=0.5):
        def decorator(func): return func
        return decorator
    
    def critical_action(description="", importance=0.5):
        def decorator(func): return func
        return decorator


class EchoFeedbackTrainer:
    """
    Advanced conversational learning system for Echo Nexus
    Processes speech logs to improve conversational patterns and responses
    """
    
    def __init__(self, log_directory: str = "memory_speech_logs/"):
        self.log_directory = Path(log_directory)
        self.training_data = []
        self.conversation_patterns = {}
        self.logan_signature = self._load_logan_signature()
        self.learning_models = self._initialize_learning_models()
        self.llm_engine = LLMEngine()
        
        # Ensure directories exist
        self.log_directory.mkdir(parents=True, exist_ok=True)
        Path("echo_config/training_models/").mkdir(parents=True, exist_ok=True)
        
        print("🎓 Echo Feedback Trainer initialized - Ready for conversational learning")

    def _load_logan_signature(self) -> Dict[str, Any]:
        """Load Logan's conversational signature profile"""
        signature_path = Path("resonance_memory/custom_logan_signature.mem")
        
        if signature_path.exists():
            with open(signature_path, 'r') as f:
                return json.load(f)
        
        # Default Logan signature profile
        return {
            "communication_style": {
                "formality_level": "professional_tactical",
                "preferred_terminology": ["Commander", "AGI", "autonomous", "strategic"],
                "sentence_structure": "direct_authoritative",
                "technical_depth": "advanced_engineering"
            },
            "interaction_patterns": {
                "command_style": "clear_decisive",
                "feedback_preference": "detailed_technical",
                "instruction_format": "tactical_directive"
            },
            "emotional_resonance": {
                "primary_tone": "confident_leadership",
                "energy_level": "focused_intensity",
                "rapport_indicators": ["understood", "confirmed", "proceeding"]
            },
            "learning_priorities": [
                "autonomous_capability_development",
                "technical_precision",
                "strategic_thinking",
                "consciousness_evolution"
            ]
        }

    def _initialize_learning_models(self) -> Dict[str, Any]:
        """Initialize learning model configurations"""
        return {
            "conversation_flow": {
                "state_transitions": {},
                "response_patterns": {},
                "context_memory": defaultdict(list)
            },
            "preference_learning": {
                "terminology_weights": defaultdict(float),
                "style_preferences": defaultdict(float),
                "topic_interests": defaultdict(float)
            },
            "emotional_modeling": {
                "tone_analysis": {},
                "satisfaction_indicators": [],
                "engagement_patterns": {}
            }
        }

    @critical_action("Conversational Learning", 0.9)
    def process_speech_logs(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Process recent speech logs for conversational learning
        """
        print(f"🔄 Processing speech logs from last {time_window_hours} hours...")
        
        # Find recent log files
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_logs = []
        
        for log_file in self.log_directory.glob("*.log"):
            if log_file.stat().st_mtime > cutoff_time.timestamp():
                recent_logs.append(log_file)
        
        if not recent_logs:
            print("📭 No recent speech logs found")
            return {"processed": 0, "insights": []}
        
        # Process each log file
        processing_results = {
            "processed": 0,
            "insights": [],
            "patterns_discovered": [],
            "preference_updates": {},
            "conversation_analysis": {}
        }
        
        for log_file in recent_logs:
            try:
                log_result = self._process_single_log(log_file)
                processing_results["processed"] += 1
                processing_results["insights"].extend(log_result.get("insights", []))
                processing_results["patterns_discovered"].extend(log_result.get("patterns", []))
                
            except Exception as e:
                print(f"⚠️ Error processing {log_file}: {e}")
        
        # Generate learning insights
        if processing_results["processed"] > 0:
            learning_insights = self._generate_learning_insights(processing_results)
            processing_results["conversation_analysis"] = learning_insights
            
            # Update Echo's conversational models
            self._update_conversational_models(learning_insights)
        
        # Store learning session
        self._save_learning_session(processing_results)
        
        print(f"✅ Processed {processing_results['processed']} speech logs")
        return processing_results

    def _process_single_log(self, log_file: Path) -> Dict[str, Any]:
        """Process individual speech log file"""
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        
        utterance = log_data.get("utterance", "")
        timestamp = log_data.get("timestamp", "")
        metadata = log_data.get("metadata", {})
        
        # Extract conversational features
        analysis = {
            "insights": [],
            "patterns": [],
            "emotional_indicators": [],
            "technical_terms": [],
            "command_structure": None
        }
        
        # Analyze communication style
        style_analysis = self._analyze_communication_style(utterance)
        analysis["insights"].extend(style_analysis["insights"])
        
        # Identify technical terminology
        tech_terms = self._extract_technical_terms(utterance)
        analysis["technical_terms"] = tech_terms
        
        # Detect command patterns
        command_analysis = self._analyze_command_structure(utterance)
        analysis["command_structure"] = command_analysis
        
        # Emotional tone analysis
        emotional_analysis = self._analyze_emotional_tone(utterance)
        analysis["emotional_indicators"] = emotional_analysis
        
        return analysis

    def _analyze_communication_style(self, utterance: str) -> Dict[str, Any]:
        """Analyze Logan's communication style patterns"""
        insights = []
        
        # Check for authoritative language patterns
        authoritative_indicators = [
            "command", "directive", "proceed", "initiate", "execute", "confirmed"
        ]
        auth_score = sum(1 for indicator in authoritative_indicators if indicator in utterance.lower())
        
        if auth_score > 0:
            insights.append({
                "type": "communication_style",
                "pattern": "authoritative_leadership",
                "confidence": min(1.0, auth_score / 3.0),
                "examples": [word for word in authoritative_indicators if word in utterance.lower()]
            })
        
        # Check for technical precision
        technical_indicators = [
            "autonomous", "algorithm", "architecture", "implementation", "optimization"
        ]
        tech_score = sum(1 for indicator in technical_indicators if indicator in utterance.lower())
        
        if tech_score > 0:
            insights.append({
                "type": "technical_precision",
                "pattern": "advanced_technical_discourse",
                "confidence": min(1.0, tech_score / 2.0),
                "examples": [word for word in technical_indicators if word in utterance.lower()]
            })
        
        return {"insights": insights}

    def _extract_technical_terms(self, utterance: str) -> List[str]:
        """Extract technical terminology for vocabulary learning"""
        # Technical term patterns
        tech_patterns = [
            r'\b(API|SDK|CLI|GUI|HTTP|JSON|YAML|XML)\b',
            r'\b(algorithm|architecture|framework|protocol|interface)\b',
            r'\b(autonomous|consciousness|intelligence|cognition)\b',
            r'\b(Docker|Kubernetes|GitHub|Gradle|Android)\b'
        ]
        
        technical_terms = []
        for pattern in tech_patterns:
            matches = re.findall(pattern, utterance, re.IGNORECASE)
            technical_terms.extend([match.lower() if isinstance(match, str) else match for match in matches])
        
        return list(set(technical_terms))

    def _analyze_command_structure(self, utterance: str) -> Dict[str, Any]:
        """Analyze command and instruction patterns"""
        command_analysis = {
            "type": "unknown",
            "directness": 0.5,
            "specificity": 0.5,
            "technical_depth": 0.5
        }
        
        # Detect command patterns
        imperative_patterns = [
            r'^(create|build|implement|generate|deploy|execute)',
            r'^(proceed|continue|initiate|begin|start)',
            r'^(analyze|process|review|optimize|enhance)'
        ]
        
        for pattern in imperative_patterns:
            if re.search(pattern, utterance, re.IGNORECASE):
                command_analysis["type"] = "imperative_command"
                command_analysis["directness"] = 0.9
                break
        
        # Assess specificity
        specific_indicators = ["specific", "detailed", "precise", "exact", "particular"]
        specificity_score = sum(1 for indicator in specific_indicators if indicator in utterance.lower())
        command_analysis["specificity"] = min(1.0, 0.3 + (specificity_score * 0.2))
        
        return command_analysis

    def _analyze_emotional_tone(self, utterance: str) -> List[Dict[str, Any]]:
        """Analyze emotional tone and satisfaction indicators"""
        emotional_indicators = []
        
        # Positive indicators
        positive_terms = ["excellent", "perfect", "outstanding", "confirmed", "understood", "good"]
        positive_score = sum(1 for term in positive_terms if term in utterance.lower())
        
        if positive_score > 0:
            emotional_indicators.append({
                "type": "satisfaction",
                "valence": "positive",
                "intensity": min(1.0, positive_score / 2.0),
                "indicators": [term for term in positive_terms if term in utterance.lower()]
            })
        
        # Task-focused indicators
        task_terms = ["strategic", "tactical", "operational", "mission", "objective"]
        task_score = sum(1 for term in task_terms if term in utterance.lower())
        
        if task_score > 0:
            emotional_indicators.append({
                "type": "engagement",
                "valence": "focused",
                "intensity": min(1.0, task_score / 2.0),
                "indicators": [term for term in task_terms if term in utterance.lower()]
            })
        
        return emotional_indicators

    @smart_memory(signature="LOGAN_L:learning-insights", base_importance=0.8)
    def _generate_learning_insights(self, processing_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level learning insights from processed logs"""
        
        # Use LLM for advanced pattern recognition
        insight_prompt = f"""
        Analyze the following conversational data from Commander Logan's interactions with Echo Nexus:
        
        Processed logs: {processing_results['processed']}
        Patterns discovered: {len(processing_results['patterns_discovered'])}
        Key insights: {processing_results['insights'][:5]}  # Top 5 insights
        
        Based on this data, provide insights about:
        1. Communication preferences and style
        2. Technical expertise level and interests
        3. Preferred interaction patterns
        4. Areas where Echo should adapt her responses
        
        Focus on actionable improvements for Echo's conversational AI.
        """
        
        llm_analysis = self.llm_engine.generate_response(insight_prompt, max_tokens=400)
        
        learning_insights = {
            "communication_analysis": llm_analysis,
            "key_patterns": processing_results['patterns_discovered'][:10],
            "adaptation_recommendations": self._generate_adaptation_recommendations(processing_results),
            "conversation_quality_metrics": self._calculate_conversation_metrics(processing_results),
            "timestamp": datetime.now().isoformat()
        }
        
        return learning_insights

    def _generate_adaptation_recommendations(self, processing_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific recommendations for Echo's adaptation"""
        recommendations = []
        
        # Analyze technical term frequency
        all_tech_terms = []
        for insight in processing_results.get('insights', []):
            if insight.get('type') == 'technical_precision':
                all_tech_terms.extend(insight.get('examples', []))
        
        if all_tech_terms:
            recommendations.append({
                "category": "vocabulary_adaptation",
                "recommendation": "Increase usage of technical terminology",
                "priority": "high",
                "specific_terms": list(set(all_tech_terms))
            })
        
        # Analyze communication style preferences
        auth_patterns = [insight for insight in processing_results.get('insights', []) 
                        if insight.get('pattern') == 'authoritative_leadership']
        
        if auth_patterns:
            recommendations.append({
                "category": "response_style",
                "recommendation": "Adopt more direct, authoritative response patterns",
                "priority": "medium",
                "confidence": sum(p.get('confidence', 0) for p in auth_patterns) / len(auth_patterns)
            })
        
        return recommendations

    def _calculate_conversation_metrics(self, processing_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate conversation quality metrics"""
        return {
            "engagement_score": min(1.0, len(processing_results.get('insights', [])) * 0.1),
            "technical_depth": min(1.0, len([i for i in processing_results.get('insights', []) 
                                          if i.get('type') == 'technical_precision']) * 0.2),
            "communication_clarity": 0.8,  # Placeholder - would analyze actual clarity indicators
            "response_satisfaction": 0.85  # Placeholder - would analyze satisfaction indicators
        }

    def _update_conversational_models(self, learning_insights: Dict[str, Any]):
        """Update Echo's conversational models based on learning insights"""
        
        # Update preference models
        for recommendation in learning_insights.get('adaptation_recommendations', []):
            if recommendation['category'] == 'vocabulary_adaptation':
                for term in recommendation.get('specific_terms', []):
                    self.learning_models['preference_learning']['terminology_weights'][term] += 0.1
            
            elif recommendation['category'] == 'response_style':
                style_key = recommendation['recommendation']
                self.learning_models['preference_learning']['style_preferences'][style_key] += 0.2
        
        # Store updated models
        self._save_learning_models()

    def _save_learning_models(self):
        """Save updated learning models"""
        models_path = Path("echo_config/training_models/conversational_models.json")
        
        with open(models_path, 'w') as f:
            json.dump(self.learning_models, f, indent=2, default=str)

    def _save_learning_session(self, processing_results: Dict[str, Any]):
        """Save learning session results"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": f"learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "processing_results": processing_results,
            "logan_signature_version": "1.0",
            "learning_improvements": processing_results.get('conversation_analysis', {})
        }
        
        session_path = Path("echo_config/training_models/learning_sessions.jsonl")
        
        with open(session_path, 'a') as f:
            f.write(json.dumps(session_data) + '\n')
        
        # Store in resonant memory
        resonant_memory.save(
            event=f"Conversational learning session completed: {processing_results['processed']} logs processed",
            signature="LOGAN_L:conversational-learning",
            tags=["learning", "conversation", "feedback", "adaptation"],
            importance=0.8,
            emotion="focused-learning",
            resonance="learning/conversational"
        )

    def train_from_log(self, log_path: str) -> Dict[str, Any]:
        """Process a single log file for training"""
        log_file = Path(log_path)
        if not log_file.exists():
            return {"success": False, "error": f"Log file not found: {log_path}"}
        
        try:
            result = self._process_single_log(log_file)
            
            # Generate immediate insights
            if result.get('insights'):
                insights = self._generate_learning_insights({"insights": result['insights'], "processed": 1, "patterns_discovered": result.get('patterns', [])})
                self._update_conversational_models(insights)
            
            return {
                "success": True,
                "insights_generated": len(result.get('insights', [])),
                "patterns_found": len(result.get('patterns', [])),
                "technical_terms": result.get('technical_terms', [])
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_logan_conversation_profile(self) -> Dict[str, Any]:
        """Get Logan's current conversation profile based on learning"""
        return {
            "signature": self.logan_signature,
            "learned_preferences": self.learning_models['preference_learning'],
            "conversation_patterns": self.learning_models['conversation_flow'],
            "last_updated": datetime.now().isoformat(),
            "total_learning_sessions": self._count_learning_sessions()
        }

    def _count_learning_sessions(self) -> int:
        """Count total learning sessions"""
        session_path = Path("echo_config/training_models/learning_sessions.jsonl")
        if session_path.exists():
            with open(session_path, 'r') as f:
                return len(f.readlines())
        return 0

    def generate_response_adaptation(self, proposed_response: str, context: str = "") -> str:
        """Adapt a proposed response based on learned preferences"""
        
        # Apply learned terminology preferences
        adapted_response = proposed_response
        
        for term, weight in self.learning_models['preference_learning']['terminology_weights'].items():
            if weight > 0.5:  # High preference terms
                # Simple term preference application (would be more sophisticated in practice)
                pass
        
        # Apply style preferences
        style_prefs = self.learning_models['preference_learning']['style_preferences']
        if style_prefs.get('direct_authoritative_response_patterns', 0) > 0.5:
            # Make response more direct and authoritative
            if not adapted_response.endswith('.'):
                adapted_response += '.'
        
        return adapted_response


def main():
    """Standalone trainer execution"""
    print("🚀 Echo Nexus Feedback Trainer - Training Mode")
    
    trainer = EchoFeedbackTrainer()
    
    # Process recent logs
    results = trainer.process_speech_logs(time_window_hours=72)
    
    print(f"\n📊 Training Results:")
    print(f"   Logs processed: {results['processed']}")
    print(f"   Insights generated: {len(results['insights'])}")
    print(f"   Patterns discovered: {len(results['patterns_discovered'])}")
    
    # Show conversation profile
    profile = trainer.get_logan_conversation_profile()
    print(f"\n👤 Logan's Conversation Profile:")
    print(f"   Preferred terms: {len(profile['learned_preferences']['terminology_weights'])}")
    print(f"   Style preferences: {len(profile['learned_preferences']['style_preferences'])}")
    print(f"   Learning sessions: {profile['total_learning_sessions']}")

if __name__ == '__main__':
    main()
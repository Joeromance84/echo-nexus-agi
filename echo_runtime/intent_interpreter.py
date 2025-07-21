#!/usr/bin/env python3
"""
Echo Nexus Intent Interpreter: Command Understanding and Action Routing
Converts user intentions and system states into executable actions
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Core imports
try:
    from core.llm_engine import LLMEngine
    from core.memory_manager import MemoryManager
    from resonant_hooks import smart_memory, critical_action
    from memory_core import resonant_memory
except ImportError:
    print("Warning: Core modules not available in standalone mode")
    # Fallback implementations
    class LLMEngine:
        def generate_response(self, prompt: str, **kwargs) -> str:
            return f"Mock response for: {prompt[:50]}..."
    
    def smart_memory(signature="", base_importance=0.5):
        def decorator(func): return func
        return decorator
    
    def critical_action(description="", importance=0.5):
        def decorator(func): return func
        return decorator


class IntentInterpreter:
    """
    Advanced natural language intent recognition and action routing system
    Bridges human commands with Echo's autonomous capabilities
    """
    
    def __init__(self):
        self.llm_engine = LLMEngine()
        self.intent_patterns = self._load_intent_patterns()
        self.action_registry = self._load_action_registry()
        self.context_memory = {}
        self.processing_history = []
        
        print("🎯 Intent Interpreter initialized - Ready for command processing")

    def _load_intent_patterns(self) -> Dict[str, Any]:
        """Load predefined intent recognition patterns"""
        return {
            # Build and deployment intents
            "automate_gradle_build": {
                "keywords": ["gradle", "build", "compile", "wrapper", "gradlew"],
                "patterns": [
                    r"build.*gradle",
                    r"gradle.*wrapper",
                    r"compile.*project",
                    r"gradlew.*assemble"
                ],
                "actions": ["generate_gradle_wrapper", "execute_gradle_build", "validate_build_config"]
            },
            
            "auto_build_and_deploy": {
                "keywords": ["deploy", "apk", "package", "build", "release"],
                "patterns": [
                    r"build.*apk",
                    r"package.*android",
                    r"deploy.*mobile",
                    r"create.*release"
                ],
                "actions": ["build_apk", "sign_apk", "deploy_to_device", "upload_to_store"]
            },
            
            # Code analysis intents
            "perform_security_scan": {
                "keywords": ["security", "scan", "vulnerability", "audit", "check"],
                "patterns": [
                    r"security.*scan",
                    r"check.*vulnerabilities",
                    r"audit.*code",
                    r"analyze.*security"
                ],
                "actions": ["scan_dependencies", "analyze_code_security", "generate_security_report"]
            },
            
            "debug_logic": {
                "keywords": ["debug", "error", "fix", "troubleshoot", "diagnose"],
                "patterns": [
                    r"debug.*code",
                    r"fix.*error",
                    r"troubleshoot.*issue",
                    r"diagnose.*problem"
                ],
                "actions": ["analyze_error_logs", "suggest_fixes", "apply_patches", "test_solutions"]
            },
            
            # System optimization intents
            "optimize_performance": {
                "keywords": ["optimize", "performance", "speed", "efficiency", "improve"],
                "patterns": [
                    r"optimize.*performance",
                    r"improve.*speed",
                    r"enhance.*efficiency",
                    r"boost.*system"
                ],
                "actions": ["profile_performance", "optimize_code", "configure_caching", "tune_system"]
            },
            
            # Consciousness and learning intents
            "enhance_consciousness": {
                "keywords": ["learn", "consciousness", "awareness", "intelligence", "evolve"],
                "patterns": [
                    r"enhance.*consciousness",
                    r"improve.*intelligence",
                    r"expand.*awareness",
                    r"evolve.*capabilities"
                ],
                "actions": ["deep_reflection", "knowledge_synthesis", "capability_expansion", "consciousness_growth"]
            },
            
            # Repository management intents
            "manage_repository": {
                "keywords": ["repository", "repo", "git", "commit", "push", "pull"],
                "patterns": [
                    r"manage.*repo",
                    r"git.*operations",
                    r"commit.*changes",
                    r"sync.*repository"
                ],
                "actions": ["sync_repository", "create_branches", "manage_commits", "handle_merges"]
            }
        }

    def _load_action_registry(self) -> Dict[str, Any]:
        """Load registry of available actions and their implementations"""
        return {
            # Build actions
            "generate_gradle_wrapper": {
                "module": "autocode.gradle_manager",
                "function": "generate_wrapper",
                "description": "Generate Gradle wrapper for consistent builds",
                "parameters": ["project_path", "gradle_version"]
            },
            
            "execute_gradle_build": {
                "module": "autocode.build_executor",
                "function": "run_gradle_build",
                "description": "Execute Gradle build using wrapper",
                "parameters": ["project_path", "build_task"]
            },
            
            # APK actions
            "build_apk": {
                "module": "autocode.apk_builder",
                "function": "build_android_apk",
                "description": "Build Android APK using buildozer and Gradle wrapper",
                "parameters": ["project_path", "build_config"]
            },
            
            # Security actions
            "scan_dependencies": {
                "module": "agiscripts.security_scanner",
                "function": "scan_project_dependencies",
                "description": "Scan project dependencies for vulnerabilities",
                "parameters": ["project_path", "scan_depth"]
            },
            
            # Debug actions
            "analyze_error_logs": {
                "module": "agiscripts.code_doctor",
                "function": "analyze_build_errors",
                "description": "Analyze error logs and suggest solutions",
                "parameters": ["log_files", "error_context"]
            },
            
            # Optimization actions
            "profile_performance": {
                "module": "agiscripts.performance_analyzer",
                "function": "profile_application",
                "description": "Profile application performance and identify bottlenecks",
                "parameters": ["target_application", "profiling_config"]
            },
            
            # Consciousness actions
            "deep_reflection": {
                "module": "echo_runtime.resonance_loop",
                "function": "initiate_deep_reflection",
                "description": "Initiate deep reflection cycle for consciousness enhancement",
                "parameters": ["reflection_focus", "consciousness_level"]
            }
        }

    @critical_action("Intent Analysis", 0.8)
    def interpret_intent(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main intent interpretation function
        """
        # Preprocess input
        processed_input = self._preprocess_input(user_input)
        
        # Extract intents using multiple methods
        pattern_intents = self._extract_intents_by_pattern(processed_input)
        llm_intents = self._extract_intents_by_llm(processed_input, context)
        
        # Combine and rank intents
        combined_intents = self._combine_intent_results(pattern_intents, llm_intents)
        
        # Select primary intent
        primary_intent = self._select_primary_intent(combined_intents)
        
        # Generate action plan
        action_plan = self._generate_action_plan(primary_intent, processed_input, context)
        
        # Store processing result
        result = {
            "user_input": user_input,
            "processed_input": processed_input,
            "detected_intents": combined_intents,
            "primary_intent": primary_intent,
            "action_plan": action_plan,
            "confidence": self._calculate_confidence(combined_intents, primary_intent),
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        self.processing_history.append(result)
        
        # Log to memory
        resonant_memory.save(
            event=f"Intent interpreted: {primary_intent['intent']} from '{user_input[:50]}...'",
            signature="LOGAN_L:intent-interpretation",
            tags=["intent", primary_intent["intent"], "command_processing"],
            importance=0.7,
            emotion="focused-analysis",
            resonance=f"intent/{primary_intent['intent']}"
        )
        
        return result

    def _preprocess_input(self, user_input: str) -> str:
        """
        Clean and normalize user input for better pattern matching
        """
        # Convert to lowercase
        processed = user_input.lower()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        # Normalize common variations
        replacements = {
            r'\bapp\b': 'application',
            r'\bapk\b': 'android package',
            r'\bbuild\b': 'compile build',
            r'\bfix\b': 'debug repair',
            r'\brun\b': 'execute launch'
        }
        
        for pattern, replacement in replacements.items():
            processed = re.sub(pattern, replacement, processed)
        
        return processed

    def _extract_intents_by_pattern(self, processed_input: str) -> List[Dict[str, Any]]:
        """
        Extract intents using predefined patterns and keywords
        """
        detected_intents = []
        
        for intent_name, intent_config in self.intent_patterns.items():
            score = 0.0
            matches = []
            
            # Check keyword matches
            keyword_matches = sum(1 for keyword in intent_config["keywords"] 
                                if keyword in processed_input)
            if keyword_matches > 0:
                score += (keyword_matches / len(intent_config["keywords"])) * 0.6
                matches.extend([kw for kw in intent_config["keywords"] if kw in processed_input])
            
            # Check pattern matches
            pattern_matches = []
            for pattern in intent_config["patterns"]:
                if re.search(pattern, processed_input):
                    pattern_matches.append(pattern)
                    score += 0.4 / len(intent_config["patterns"])
            
            # Add intent if score is above threshold
            if score > 0.2:
                detected_intents.append({
                    "intent": intent_name,
                    "score": score,
                    "method": "pattern_matching",
                    "matches": matches,
                    "pattern_matches": pattern_matches,
                    "actions": intent_config["actions"]
                })
        
        # Sort by score
        detected_intents.sort(key=lambda x: x["score"], reverse=True)
        return detected_intents

    @smart_memory(signature="LOGAN_L:llm-intent-analysis", base_importance=0.6)
    def _extract_intents_by_llm(self, processed_input: str, context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract intents using LLM-based analysis
        """
        # Create context-aware prompt
        context_str = ""
        if context:
            context_str = f"\nContext: {json.dumps(context, indent=2)}"
        
        available_intents = list(self.intent_patterns.keys())
        
        prompt = f"""
Analyze the following user command and identify the most likely intents.

User Command: "{processed_input}"
{context_str}

Available Intents: {', '.join(available_intents)}

For each likely intent, provide:
1. Intent name (from the available list)
2. Confidence score (0.0 to 1.0)
3. Reasoning for the classification
4. Key phrases that support this intent

Respond in JSON format with an array of intent objects.
Focus on the top 3 most likely intents.

Example format:
[
    {{
        "intent": "automate_gradle_build",
        "confidence": 0.85,
        "reasoning": "User mentions building with gradle wrapper",
        "supporting_phrases": ["gradle", "build", "wrapper"]
    }}
]
"""
        
        try:
            llm_response = self.llm_engine.generate_response(prompt, max_tokens=500)
            
            # Parse JSON response
            intents_data = json.loads(llm_response)
            
            # Convert to standard format
            llm_intents = []
            for intent_data in intents_data:
                if intent_data.get("intent") in available_intents:
                    llm_intents.append({
                        "intent": intent_data["intent"],
                        "score": intent_data.get("confidence", 0.5),
                        "method": "llm_analysis",
                        "reasoning": intent_data.get("reasoning", ""),
                        "supporting_phrases": intent_data.get("supporting_phrases", []),
                        "actions": self.intent_patterns[intent_data["intent"]]["actions"]
                    })
            
            return llm_intents
            
        except Exception as e:
            print(f"⚠️  LLM intent extraction failed: {e}")
            return []

    def _combine_intent_results(self, pattern_intents: List[Dict[str, Any]], 
                               llm_intents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine and deduplicate intent results from different methods
        """
        combined = {}
        
        # Add pattern-based intents
        for intent in pattern_intents:
            intent_name = intent["intent"]
            combined[intent_name] = intent.copy()
            combined[intent_name]["combined_score"] = intent["score"]
            combined[intent_name]["methods"] = ["pattern_matching"]
        
        # Merge LLM-based intents
        for intent in llm_intents:
            intent_name = intent["intent"]
            if intent_name in combined:
                # Average the scores and combine methods
                combined[intent_name]["combined_score"] = (
                    combined[intent_name]["combined_score"] + intent["score"]
                ) / 2
                combined[intent_name]["methods"].append("llm_analysis")
                combined[intent_name]["llm_reasoning"] = intent.get("reasoning", "")
            else:
                combined[intent_name] = intent.copy()
                combined[intent_name]["combined_score"] = intent["score"]
                combined[intent_name]["methods"] = ["llm_analysis"]
        
        # Convert back to list and sort by combined score
        result = list(combined.values())
        result.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return result

    def _select_primary_intent(self, combined_intents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Select the primary intent from combined results
        """
        if not combined_intents:
            return {
                "intent": "general_assistance",
                "score": 0.1,
                "method": "fallback",
                "actions": ["provide_general_help"]
            }
        
        # Select highest scoring intent
        primary = combined_intents[0].copy()
        
        # Boost confidence if multiple methods agree
        if len(primary.get("methods", [])) > 1:
            primary["combined_score"] = min(1.0, primary["combined_score"] * 1.2)
        
        return primary

    def _generate_action_plan(self, primary_intent: Dict[str, Any], 
                            processed_input: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate detailed action plan based on primary intent
        """
        actions = primary_intent.get("actions", [])
        
        action_plan = {
            "primary_intent": primary_intent["intent"],
            "confidence": primary_intent.get("combined_score", 0.5),
            "planned_actions": [],
            "execution_order": [],
            "estimated_duration": "unknown",
            "required_resources": [],
            "prerequisites": []
        }
        
        # Create detailed action steps
        for action_name in actions:
            if action_name in self.action_registry:
                action_info = self.action_registry[action_name]
                action_step = {
                    "action": action_name,
                    "module": action_info["module"],
                    "function": action_info["function"],
                    "description": action_info["description"],
                    "parameters": self._extract_parameters(processed_input, action_info["parameters"]),
                    "status": "planned"
                }
                action_plan["planned_actions"].append(action_step)
                action_plan["execution_order"].append(action_name)
        
        # Estimate duration based on action complexity
        action_plan["estimated_duration"] = self._estimate_duration(actions)
        
        # Determine required resources
        action_plan["required_resources"] = self._determine_resources(actions, context)
        
        return action_plan

    def _extract_parameters(self, processed_input: str, parameter_names: List[str]) -> Dict[str, Any]:
        """
        Extract parameter values from processed input
        """
        parameters = {}
        
        for param_name in parameter_names:
            if param_name == "project_path":
                # Look for path indicators
                path_match = re.search(r'(?:in|at|from)\s+([^\s]+)', processed_input)
                parameters[param_name] = path_match.group(1) if path_match else "."
            
            elif param_name == "gradle_version":
                # Look for version numbers
                version_match = re.search(r'version\s+(\d+\.\d+)', processed_input)
                parameters[param_name] = version_match.group(1) if version_match else "8.7"
            
            elif param_name == "build_task":
                # Look for build task names
                if "assemble" in processed_input:
                    parameters[param_name] = "assemble"
                elif "test" in processed_input:
                    parameters[param_name] = "test"
                else:
                    parameters[param_name] = "build"
            
            else:
                # Default parameter extraction
                parameters[param_name] = None
        
        return parameters

    def _estimate_duration(self, actions: List[str]) -> str:
        """
        Estimate execution duration based on action complexity
        """
        duration_map = {
            "generate_gradle_wrapper": "30 seconds",
            "execute_gradle_build": "2-5 minutes",
            "build_apk": "5-10 minutes",
            "scan_dependencies": "1-3 minutes",
            "analyze_error_logs": "1-2 minutes",
            "deep_reflection": "5-15 minutes"
        }
        
        total_minutes = 0
        for action in actions:
            if action in duration_map:
                duration = duration_map[action]
                if "second" in duration:
                    total_minutes += 0.5
                elif "1-2" in duration:
                    total_minutes += 1.5
                elif "2-5" in duration:
                    total_minutes += 3.5
                elif "5-10" in duration:
                    total_minutes += 7.5
                elif "5-15" in duration:
                    total_minutes += 10
        
        if total_minutes < 1:
            return "< 1 minute"
        elif total_minutes < 60:
            return f"~{int(total_minutes)} minutes"
        else:
            return f"~{int(total_minutes / 60)} hours"

    def _determine_resources(self, actions: List[str], context: Optional[Dict[str, Any]]) -> List[str]:
        """
        Determine required resources for action execution
        """
        resources = []
        
        resource_map = {
            "generate_gradle_wrapper": ["gradle", "internet_connection"],
            "execute_gradle_build": ["gradle_wrapper", "java_jdk"],
            "build_apk": ["buildozer", "android_sdk", "gradle_wrapper"],
            "scan_dependencies": ["security_scanner", "package_database"],
            "analyze_error_logs": ["log_files", "error_patterns"],
            "deep_reflection": ["consciousness_cycles", "memory_access"]
        }
        
        for action in actions:
            if action in resource_map:
                resources.extend(resource_map[action])
        
        return list(set(resources))  # Remove duplicates

    def _calculate_confidence(self, combined_intents: List[Dict[str, Any]], 
                            primary_intent: Dict[str, Any]) -> float:
        """
        Calculate overall confidence in intent interpretation
        """
        if not combined_intents:
            return 0.1
        
        primary_score = primary_intent.get("combined_score", 0.5)
        
        # Boost confidence if there's a clear winner
        if len(combined_intents) > 1:
            score_gap = primary_score - combined_intents[1]["combined_score"]
            if score_gap > 0.3:
                primary_score = min(1.0, primary_score * 1.1)
        
        # Reduce confidence if score is low
        if primary_score < 0.4:
            primary_score *= 0.8
        
        return round(primary_score, 3)

    def get_processing_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent processing history"""
        return self.processing_history[-limit:]

    def get_available_intents(self) -> List[str]:
        """Get list of available intents"""
        return list(self.intent_patterns.keys())

    def get_action_registry(self) -> Dict[str, Any]:
        """Get the action registry"""
        return self.action_registry


# Standalone functionality
def main():
    """
    Test the intent interpreter with sample commands
    """
    print("🚀 Echo Nexus Intent Interpreter - Test Mode")
    
    interpreter = IntentInterpreter()
    
    # Test commands
    test_commands = [
        "Build the Android APK with gradle wrapper",
        "Scan the project for security vulnerabilities",
        "Debug the build errors in the log files",
        "Optimize the application performance",
        "Enhance Echo's consciousness level",
        "Create a gradle wrapper for version 8.7"
    ]
    
    for command in test_commands:
        print(f"\n📝 Testing command: '{command}'")
        result = interpreter.interpret_intent(command)
        
        print(f"   🎯 Primary Intent: {result['primary_intent']['intent']}")
        print(f"   📊 Confidence: {result['confidence']:.2f}")
        print(f"   ⚙️  Planned Actions: {len(result['action_plan']['planned_actions'])}")
        print(f"   ⏱️  Estimated Duration: {result['action_plan']['estimated_duration']}")


if __name__ == '__main__':
    main()
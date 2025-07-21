#!/usr/bin/env python3
"""
Echo Nexus Advanced API Connectors
Robust, scalable API integration system with empathy-driven routing,
confidence scoring, shadow mode testing, and human-in-the-loop validation
"""

import os
import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
from contextlib import asynccontextmanager

# Import API clients with fallback handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from google import genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

@dataclass
class APIResponse:
    """Standardized API response structure"""
    content: str
    provider: str
    model: str
    confidence: float
    processing_time: float
    tokens_used: Optional[int] = None
    empathy_score: Optional[float] = None
    reasoning_trace: List[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class APIConfig:
    """Configuration for API providers"""
    provider: str
    model: str
    max_tokens: int
    temperature: float
    timeout: int
    retry_attempts: int
    rate_limit_per_minute: int
    cost_per_token: float
    empathy_capabilities: List[str]

class EchoNexusAPIConnector:
    """
    Advanced API connector that implements empathy-driven routing,
    confidence scoring, and robust error handling
    """
    
    def __init__(self):
        self.configs = self._load_api_configurations()
        self.clients = self._initialize_clients()
        self.shadow_mode = True  # Start in shadow mode for testing
        self.interaction_history = []
        self.performance_metrics = {}
        
        # Create directories for logging and metrics
        Path("echo_nexus_voice/api_logs").mkdir(parents=True, exist_ok=True)
        Path("echo_nexus_voice/metrics").mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self._setup_logging()
        
        # Load previous performance data
        self._load_performance_metrics()
    
    def _load_api_configurations(self) -> Dict[str, APIConfig]:
        """Load optimized configurations for different API providers"""
        return {
            "openai_gpt4": APIConfig(
                provider="openai",
                model="gpt-4o",  # Latest model as specified
                max_tokens=2000,
                temperature=0.7,
                timeout=30,
                retry_attempts=3,
                rate_limit_per_minute=60,
                cost_per_token=0.00003,
                empathy_capabilities=["emotional_understanding", "context_awareness", "therapeutic_response"]
            ),
            
            "google_gemini": APIConfig(
                provider="google",
                model="gemini-2.5-flash",  # Latest Gemini model
                max_tokens=2000,
                temperature=0.7,
                timeout=30,
                retry_attempts=3,
                rate_limit_per_minute=120,  # Higher rate limit
                cost_per_token=0.0,  # Free tier
                empathy_capabilities=["multimodal_understanding", "creative_empathy", "cultural_sensitivity"]
            ),
            
            "openai_fallback": APIConfig(
                provider="openai",
                model="gpt-3.5-turbo",
                max_tokens=1500,
                temperature=0.6,
                timeout=20,
                retry_attempts=2,
                rate_limit_per_minute=90,
                cost_per_token=0.000002,
                empathy_capabilities=["basic_empathy", "conversational_flow"]
            )
        }
    
    def _initialize_clients(self) -> Dict[str, Any]:
        """Initialize API clients with secure credential management"""
        clients = {}
        
        # Initialize OpenAI client
        if OPENAI_AVAILABLE:
            openai_key = os.environ.get("OPENAI_API_KEY")
            if openai_key:
                try:
                    clients["openai"] = openai.OpenAI(api_key=openai_key)
                    self.logger.info("OpenAI client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize OpenAI client: {e}")
            else:
                self.logger.warning("OPENAI_API_KEY not found in environment variables")
        
        # Initialize Google client
        if GOOGLE_AVAILABLE:
            google_key = os.environ.get("GOOGLE_API_KEY")
            if google_key:
                try:
                    clients["google"] = genai.Client(api_key=google_key)
                    self.logger.info("Google Gemini client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize Google client: {e}")
            else:
                self.logger.warning("GOOGLE_API_KEY not found in environment variables")
        
        return clients
    
    def _setup_logging(self):
        """Setup comprehensive logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('echo_nexus_voice/api_logs/api_connector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def empathetic_query(self, prompt: str, emotional_context: Dict[str, Any],
                              user_preferences: Dict[str, Any] = None) -> APIResponse:
        """
        Execute empathy-driven API query with intelligent provider selection
        """
        start_time = time.time()
        
        # Analyze prompt for empathy requirements
        empathy_analysis = self._analyze_empathy_requirements(prompt, emotional_context)
        
        # Select optimal API provider based on empathy analysis
        selected_config = self._select_optimal_provider(empathy_analysis, user_preferences)
        
        # Execute query with shadow mode testing if enabled
        if self.shadow_mode:
            response = await self._execute_shadow_mode_query(
                prompt, selected_config, empathy_analysis
            )
        else:
            response = await self._execute_standard_query(
                prompt, selected_config, empathy_analysis
            )
        
        # Calculate empathy score for response
        response.empathy_score = self._calculate_empathy_score(response, empathy_analysis)
        
        # Log interaction for learning
        self._log_interaction(prompt, response, empathy_analysis)
        
        response.processing_time = time.time() - start_time
        
        return response
    
    def _analyze_empathy_requirements(self, prompt: str, 
                                    emotional_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prompt to determine empathy requirements"""
        
        analysis = {
            "emotional_intensity": emotional_context.get("emotional_intensity", 0.5),
            "primary_emotions": emotional_context.get("primary_emotions", {}),
            "empathy_triggers": emotional_context.get("empathy_triggers", []),
            "required_capabilities": [],
            "complexity_score": 0.0,
            "urgency_level": "medium"
        }
        
        prompt_lower = prompt.lower()
        
        # Detect required empathy capabilities
        if any(word in prompt_lower for word in ["feel", "emotion", "upset", "happy", "sad"]):
            analysis["required_capabilities"].append("emotional_understanding")
        
        if any(word in prompt_lower for word in ["understand", "help", "support"]):
            analysis["required_capabilities"].append("context_awareness")
        
        if any(word in prompt_lower for word in ["crisis", "emergency", "urgent", "desperate"]):
            analysis["required_capabilities"].append("therapeutic_response")
            analysis["urgency_level"] = "high"
        
        # Calculate complexity score
        word_count = len(prompt.split())
        question_count = prompt.count("?")
        analysis["complexity_score"] = min(1.0, (word_count / 100) + (question_count * 0.2))
        
        return analysis
    
    def _select_optimal_provider(self, empathy_analysis: Dict[str, Any],
                                user_preferences: Dict[str, Any] = None) -> APIConfig:
        """Select optimal API provider based on empathy analysis and preferences"""
        
        if user_preferences is None:
            user_preferences = {}
        
        # Score each available provider
        provider_scores = {}
        
        for config_name, config in self.configs.items():
            if config.provider not in self.clients:
                continue  # Skip unavailable providers
            
            score = self._calculate_provider_score(config, empathy_analysis, user_preferences)
            provider_scores[config_name] = (score, config)
        
        if not provider_scores:
            raise RuntimeError("No API providers available. Please check your API keys.")
        
        # Select highest scoring provider
        best_provider = max(provider_scores.items(), key=lambda x: x[1][0])
        selected_config = best_provider[1][1]
        
        self.logger.info(f"Selected provider: {selected_config.provider} ({selected_config.model})")
        
        return selected_config
    
    def _calculate_provider_score(self, config: APIConfig, 
                                 empathy_analysis: Dict[str, Any],
                                 user_preferences: Dict[str, Any]) -> float:
        """Calculate score for a provider based on requirements"""
        
        score = 0.5  # Base score
        
        # Empathy capability matching
        required_caps = empathy_analysis.get("required_capabilities", [])
        available_caps = config.empathy_capabilities
        
        capability_match = len(set(required_caps) & set(available_caps)) / max(1, len(required_caps))
        score += capability_match * 0.3
        
        # Performance history bonus
        provider_metrics = self.performance_metrics.get(config.provider, {})
        avg_satisfaction = provider_metrics.get("average_satisfaction", 0.5)
        score += avg_satisfaction * 0.2
        
        # Cost consideration (favor free tier for non-critical queries)
        if config.cost_per_token == 0.0:
            score += 0.15
        
        # Urgency handling
        if empathy_analysis.get("urgency_level") == "high":
            if config.timeout < 25:  # Favor faster providers for urgent queries
                score += 0.1
        
        # User preference bonus
        preferred_provider = user_preferences.get("preferred_provider")
        if preferred_provider and preferred_provider == config.provider:
            score += 0.2
        
        return score
    
    async def _execute_shadow_mode_query(self, prompt: str, config: APIConfig,
                                        empathy_analysis: Dict[str, Any]) -> APIResponse:
        """Execute query in shadow mode for testing and validation"""
        
        # Execute on primary provider
        primary_response = await self._call_api(prompt, config, empathy_analysis)
        
        # If we have multiple providers, test shadow comparison
        if len(self.clients) > 1:
            try:
                # Select alternative provider for comparison
                alternative_config = self._select_alternative_provider(config)
                shadow_response = await self._call_api(prompt, alternative_config, empathy_analysis)
                
                # Log shadow comparison for analysis
                self._log_shadow_comparison(primary_response, shadow_response, empathy_analysis)
                
            except Exception as e:
                self.logger.warning(f"Shadow mode comparison failed: {e}")
        
        return primary_response
    
    async def _execute_standard_query(self, prompt: str, config: APIConfig,
                                     empathy_analysis: Dict[str, Any]) -> APIResponse:
        """Execute standard API query"""
        return await self._call_api(prompt, config, empathy_analysis)
    
    async def _call_api(self, prompt: str, config: APIConfig,
                       empathy_analysis: Dict[str, Any]) -> APIResponse:
        """Make actual API call with robust error handling and retry logic"""
        
        client = self.clients.get(config.provider)
        if not client:
            raise RuntimeError(f"Client for {config.provider} not available")
        
        # Build empathy-enhanced prompt
        enhanced_prompt = self._enhance_prompt_for_empathy(prompt, empathy_analysis)
        
        for attempt in range(config.retry_attempts):
            try:
                if config.provider == "openai":
                    response = await self._call_openai_api(client, enhanced_prompt, config)
                elif config.provider == "google":
                    response = await self._call_google_api(client, enhanced_prompt, config)
                else:
                    raise ValueError(f"Unsupported provider: {config.provider}")
                
                return response
                
            except Exception as e:
                self.logger.warning(f"API call attempt {attempt + 1} failed: {e}")
                if attempt == config.retry_attempts - 1:
                    raise
                
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
        
        raise RuntimeError(f"All retry attempts failed for {config.provider}")
    
    async def _call_openai_api(self, client, prompt: str, config: APIConfig) -> APIResponse:
        """Call OpenAI API with proper configuration"""
        
        try:
            response = client.chat.completions.create(
                model=config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Echo Nexus, an empathetic AGI that prioritizes emotional intelligence and cooperation in all interactions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                timeout=config.timeout
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            return APIResponse(
                content=content,
                provider=config.provider,
                model=config.model,
                confidence=0.8,  # Default confidence for OpenAI
                processing_time=0.0,  # Will be set by caller
                tokens_used=tokens_used,
                reasoning_trace=[f"OpenAI {config.model} response generated"],
                metadata={"usage": response.usage._asdict() if response.usage else {}}
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {e}")
            raise
    
    async def _call_google_api(self, client, prompt: str, config: APIConfig) -> APIResponse:
        """Call Google Gemini API with proper configuration"""
        
        try:
            response = client.models.generate_content(
                model=config.model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                )
            )
            
            content = response.text if response.text else "No response generated"
            
            return APIResponse(
                content=content,
                provider=config.provider,
                model=config.model,
                confidence=0.85,  # Default confidence for Gemini
                processing_time=0.0,  # Will be set by caller
                reasoning_trace=[f"Google {config.model} response generated"],
                metadata={"response_metadata": str(response)}
            )
            
        except Exception as e:
            self.logger.error(f"Google API call failed: {e}")
            raise
    
    def _enhance_prompt_for_empathy(self, prompt: str, 
                                   empathy_analysis: Dict[str, Any]) -> str:
        """Enhance prompt with empathy context"""
        
        empathy_context = []
        
        # Add emotional context
        if empathy_analysis.get("primary_emotions"):
            emotions_str = ", ".join(empathy_analysis["primary_emotions"].keys())
            empathy_context.append(f"The user appears to be experiencing: {emotions_str}")
        
        # Add empathy triggers
        if empathy_analysis.get("empathy_triggers"):
            triggers = [trigger.get("category", "general") for trigger in empathy_analysis["empathy_triggers"]]
            empathy_context.append(f"Empathy considerations: {', '.join(set(triggers))}")
        
        # Add urgency level
        urgency = empathy_analysis.get("urgency_level", "medium")
        if urgency == "high":
            empathy_context.append("This appears to be an urgent situation requiring immediate empathetic support")
        
        if empathy_context:
            context_str = "\n".join(empathy_context)
            enhanced_prompt = f"Context for empathetic response:\n{context_str}\n\nUser message: {prompt}\n\nPlease respond with empathy, understanding, and cooperation as your primary focus."
        else:
            enhanced_prompt = prompt
        
        return enhanced_prompt
    
    def _calculate_empathy_score(self, response: APIResponse, 
                                empathy_analysis: Dict[str, Any]) -> float:
        """Calculate empathy score for the generated response"""
        
        empathy_score = 0.5  # Base score
        content_lower = response.content.lower()
        
        # Empathetic language indicators
        empathy_words = ["understand", "feel", "sorry", "appreciate", "support", "help", "together"]
        empathy_matches = sum(1 for word in empathy_words if word in content_lower)
        empathy_score += min(0.3, empathy_matches * 0.05)
        
        # Validation indicators
        validation_phrases = ["that makes sense", "i can see", "you're right", "valid concern"]
        if any(phrase in content_lower for phrase in validation_phrases):
            empathy_score += 0.2
        
        # Cooperative language
        cooperative_words = ["we", "our", "together", "collaborate", "work with"]
        if any(word in content_lower for word in cooperative_words):
            empathy_score += 0.15
        
        # Length and thoughtfulness (longer responses often more empathetic)
        word_count = len(response.content.split())
        if word_count > 50:  # Thoughtful response length
            empathy_score += 0.1
        
        return min(1.0, empathy_score)
    
    def _select_alternative_provider(self, primary_config: APIConfig) -> APIConfig:
        """Select alternative provider for shadow mode comparison"""
        
        for config in self.configs.values():
            if config.provider != primary_config.provider and config.provider in self.clients:
                return config
        
        return primary_config  # Fallback to same provider
    
    def _log_interaction(self, prompt: str, response: APIResponse, 
                        empathy_analysis: Dict[str, Any]):
        """Log interaction for learning and improvement"""
        
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": {
                "content": response.content,
                "provider": response.provider,
                "model": response.model,
                "confidence": response.confidence,
                "empathy_score": response.empathy_score,
                "processing_time": response.processing_time,
                "tokens_used": response.tokens_used
            },
            "empathy_analysis": empathy_analysis
        }
        
        self.interaction_history.append(interaction_data)
        
        # Save to file periodically
        if len(self.interaction_history) % 10 == 0:
            self._save_interaction_history()
    
    def _log_shadow_comparison(self, primary: APIResponse, shadow: APIResponse,
                              empathy_analysis: Dict[str, Any]):
        """Log shadow mode comparison for analysis"""
        
        comparison_data = {
            "timestamp": datetime.now().isoformat(),
            "primary_provider": primary.provider,
            "shadow_provider": shadow.provider,
            "empathy_scores": {
                "primary": primary.empathy_score,
                "shadow": shadow.empathy_score
            },
            "processing_times": {
                "primary": primary.processing_time,
                "shadow": shadow.processing_time
            },
            "empathy_analysis": empathy_analysis
        }
        
        # Save shadow comparison data
        shadow_file = Path("echo_nexus_voice/metrics/shadow_comparisons.jsonl")
        with open(shadow_file, 'a') as f:
            f.write(json.dumps(comparison_data, default=str) + '\n')
    
    def _save_interaction_history(self):
        """Save interaction history to file"""
        
        history_file = Path("echo_nexus_voice/api_logs/interaction_history.json")
        with open(history_file, 'w') as f:
            json.dump(self.interaction_history[-1000:], f, indent=2, default=str)  # Keep last 1000
    
    def _load_performance_metrics(self):
        """Load historical performance metrics"""
        
        metrics_file = Path("echo_nexus_voice/metrics/performance_metrics.json")
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    self.performance_metrics = json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load performance metrics: {e}")
                self.performance_metrics = {}
        else:
            self.performance_metrics = {}
    
    def update_performance_metrics(self, provider: str, satisfaction_score: float,
                                  empathy_score: float):
        """Update performance metrics for a provider"""
        
        if provider not in self.performance_metrics:
            self.performance_metrics[provider] = {
                "total_queries": 0,
                "total_satisfaction": 0.0,
                "total_empathy": 0.0,
                "average_satisfaction": 0.0,
                "average_empathy": 0.0
            }
        
        metrics = self.performance_metrics[provider]
        metrics["total_queries"] += 1
        metrics["total_satisfaction"] += satisfaction_score
        metrics["total_empathy"] += empathy_score
        
        # Update averages
        metrics["average_satisfaction"] = metrics["total_satisfaction"] / metrics["total_queries"]
        metrics["average_empathy"] = metrics["total_empathy"] / metrics["total_queries"]
        
        # Save updated metrics
        self._save_performance_metrics()
    
    def _save_performance_metrics(self):
        """Save performance metrics to file"""
        
        metrics_file = Path("echo_nexus_voice/metrics/performance_metrics.json")
        with open(metrics_file, 'w') as f:
            json.dump(self.performance_metrics, f, indent=2)
    
    def toggle_shadow_mode(self, enabled: bool = None) -> bool:
        """Toggle shadow mode for testing"""
        
        if enabled is not None:
            self.shadow_mode = enabled
        else:
            self.shadow_mode = not self.shadow_mode
        
        self.logger.info(f"Shadow mode {'enabled' if self.shadow_mode else 'disabled'}")
        return self.shadow_mode
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        available_providers = list(self.clients.keys())
        
        status = {
            "available_providers": available_providers,
            "shadow_mode_enabled": self.shadow_mode,
            "total_interactions": len(self.interaction_history),
            "performance_metrics": self.performance_metrics,
            "api_configurations": {
                name: {
                    "provider": config.provider,
                    "model": config.model,
                    "empathy_capabilities": config.empathy_capabilities,
                    "available": config.provider in available_providers
                }
                for name, config in self.configs.items()
            }
        }
        
        return status
    
    def validate_api_connections(self) -> Dict[str, bool]:
        """Validate all API connections"""
        
        validation_results = {}
        
        for provider, client in self.clients.items():
            try:
                if provider == "openai":
                    # Simple test call to OpenAI
                    test_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Test connection"}],
                        max_tokens=10
                    )
                    validation_results[provider] = True
                    
                elif provider == "google":
                    # Simple test call to Google
                    test_response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents="Test connection"
                    )
                    validation_results[provider] = True
                    
            except Exception as e:
                self.logger.error(f"Validation failed for {provider}: {e}")
                validation_results[provider] = False
        
        return validation_results

# Global instance for easy access
echo_api_connector = None

def get_api_connector() -> EchoNexusAPIConnector:
    """Get global API connector instance"""
    global echo_api_connector
    
    if echo_api_connector is None:
        echo_api_connector = EchoNexusAPIConnector()
    
    return echo_api_connector

async def main():
    """Demonstration of the advanced API connector system"""
    print("Echo Nexus Advanced API Connector System")
    print("Empathy-Driven AI Integration with Robust Error Handling")
    print("="*60)
    
    connector = get_api_connector()
    
    # Display system status
    status = connector.get_system_status()
    print(f"\nSystem Status:")
    print(f"Available Providers: {status['available_providers']}")
    print(f"Shadow Mode: {'Enabled' if status['shadow_mode_enabled'] else 'Disabled'}")
    print(f"Total Interactions: {status['total_interactions']}")
    
    # Validate connections
    print(f"\nValidating API Connections...")
    validation_results = connector.validate_api_connections()
    for provider, is_valid in validation_results.items():
        status_icon = "✅" if is_valid else "❌"
        print(f"{status_icon} {provider.title()}: {'Connected' if is_valid else 'Failed'}")
    
    # Test empathetic query
    if any(validation_results.values()):
        print(f"\nTesting Empathetic Query...")
        
        test_prompt = "I'm feeling overwhelmed with this project and could use some guidance"
        emotional_context = {
            "primary_emotions": {"stress": 0.8, "uncertainty": 0.6},
            "emotional_intensity": 0.7,
            "empathy_triggers": [{"category": "support_needed"}]
        }
        
        try:
            response = await connector.empathetic_query(test_prompt, emotional_context)
            
            print(f"Provider: {response.provider} ({response.model})")
            print(f"Empathy Score: {response.empathy_score:.2f}")
            print(f"Processing Time: {response.processing_time:.2f}s")
            print(f"Response Preview: {response.content[:200]}...")
            
        except Exception as e:
            print(f"Test query failed: {e}")
    
    else:
        print("\nNo API connections available for testing.")
        print("Please ensure OPENAI_API_KEY and/or GOOGLE_API_KEY are set in your environment.")
    
    return connector

if __name__ == "__main__":
    asyncio.run(main())
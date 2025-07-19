#!/usr/bin/env python3
"""
Cost-Optimized AI Client for EchoNexus
Implements intelligent routing between Google AI (free) and OpenAI (cost-effective)
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from google import genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .intelligent_ai_router import IntelligentAIRouter

class CostOptimizedAIClient:
    """
    AI client that automatically routes requests to the most cost-effective provider
    """
    
    def __init__(self):
        self.router = IntelligentAIRouter()
        self.google_client = None
        self.openai_client = None
        
        # Initialize clients if API keys available
        self.setup_google_ai()
        self.setup_openai()
    
    def setup_google_ai(self):
        """Setup Google AI client if available"""
        if GOOGLE_AI_AVAILABLE:
            google_api_key = os.getenv('GEMINI_API_KEY')
            if google_api_key:
                try:
                    self.google_client = genai.Client(api_key=google_api_key)
                    print("Google AI client initialized successfully")
                except Exception as e:
                    print(f"Google AI setup failed: {e}")
            else:
                print("GEMINI_API_KEY not found - Google AI unavailable")
        else:
            print("Google AI library not installed")
    
    def setup_openai(self):
        """Setup OpenAI client if available"""
        if OPENAI_AVAILABLE:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                try:
                    self.openai_client = OpenAI(api_key=openai_api_key)
                    print("OpenAI client initialized successfully")
                except Exception as e:
                    print(f"OpenAI setup failed: {e}")
            else:
                print("OPENAI_API_KEY not found - OpenAI unavailable")
        else:
            print("OpenAI library not installed")
    
    def synthesize_knowledge(self, text: str, task_type: str = "knowledge_synthesis") -> Dict[str, Any]:
        """
        Synthesize knowledge using the most cost-effective AI provider
        """
        
        estimated_tokens = len(text.split()) * 1.3  # Rough token estimation
        provider = self.router.get_optimal_provider(task_type, int(estimated_tokens))
        
        try:
            if provider == 'google_ai' and self.google_client:
                return self._synthesize_with_google(text)
            elif provider == 'openai' and self.openai_client:
                return self._synthesize_with_openai(text)
            else:
                # Fallback to basic synthesis
                return self._fallback_synthesis(text)
                
        except Exception as e:
            print(f"AI synthesis failed with {provider}: {e}")
            # Try fallback provider
            if provider == 'google_ai' and self.openai_client:
                return self._synthesize_with_openai(text)
            elif provider == 'openai' and self.google_client:
                return self._synthesize_with_google(text)
            else:
                return self._fallback_synthesis(text)
    
    def _synthesize_with_google(self, text: str) -> Dict[str, Any]:
        """Synthesize using Google AI (free tier priority)"""
        
        prompt = f"""Analyze and synthesize the following text. Provide:
1. A concise summary (2-3 sentences)
2. Key concepts (top 5)
3. Content classification
4. Main insights

Text to analyze:
{text[:3000]}"""  # Limit text length
        
        response = self.google_client.models.generate_content(
            model="gemini-2.5-flash",  # Most cost-effective model
            contents=prompt
        )
        
        # Log usage
        self.router.log_usage('google_ai', len(text.split()), 0.0)
        
        synthesis_text = response.text if response.text else "Analysis completed"
        
        return {
            'summary': synthesis_text,
            'provider': 'google_ai',
            'model': 'gemini-2.5-flash',
            'cost': 0.0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _synthesize_with_openai(self, text: str) -> Dict[str, Any]:
        """Synthesize using OpenAI (cost-effective models)"""
        
        prompt = f"""Analyze and synthesize the following text. Provide a structured analysis with:
1. Summary (2-3 sentences)
2. Key concepts (top 5)
3. Content type classification
4. Primary insights

Text: {text[:2000]}"""  # Limit for cost control
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Most cost-effective model
            messages=[
                {"role": "system", "content": "You are an expert knowledge synthesizer. Provide concise, structured analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Control costs
            temperature=0.3
        )
        
        # Estimate cost (rough calculation)
        input_tokens = len(text.split()) * 1.3
        output_tokens = len(response.choices[0].message.content.split()) * 1.3
        estimated_cost = ((input_tokens + output_tokens) / 1000) * 0.00015  # GPT-4o-mini pricing
        
        # Log usage
        self.router.log_usage('openai', int(input_tokens + output_tokens), estimated_cost)
        
        return {
            'summary': response.choices[0].message.content,
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'cost': estimated_cost,
            'timestamp': datetime.now().isoformat()
        }
    
    def _fallback_synthesis(self, text: str) -> Dict[str, Any]:
        """Fallback synthesis when no AI providers available"""
        
        from collections import Counter
        
        # Basic text analysis
        words = text.lower().split()
        sentences = text.split('.')
        
        # Extract key concepts
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        filtered_words = [w for w in words if len(w) > 3 and w not in stop_words]
        key_concepts = [word for word, count in Counter(filtered_words).most_common(5)]
        
        # Generate basic summary
        first_sentence = sentences[0] if sentences else text[:100]
        
        summary = f"""Local Analysis (No AI Provider Available):
        
Content Summary: {first_sentence}...

Key Concepts: {', '.join(key_concepts)}
Word Count: {len(words)}
Sentence Count: {len(sentences)}

Note: This is a basic analysis. For enhanced synthesis, configure GEMINI_API_KEY or OPENAI_API_KEY."""
        
        return {
            'summary': summary,
            'provider': 'local_fallback',
            'model': 'basic_text_analysis',
            'cost': 0.0,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_code(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        """Generate code using most appropriate AI provider"""
        
        task_type = "code_generation"
        estimated_tokens = len(prompt.split()) * 2  # Code generation typically uses more tokens
        provider = self.router.get_optimal_provider(task_type, int(estimated_tokens))
        
        if provider == 'google_ai' and self.google_client:
            return self._generate_code_google(prompt, language)
        elif provider == 'openai' and self.openai_client:
            return self._generate_code_openai(prompt, language)
        else:
            return {'code': f'# No AI provider available for code generation\n# Prompt: {prompt}', 'provider': 'fallback'}
    
    def _generate_code_google(self, prompt: str, language: str) -> Dict[str, Any]:
        """Generate code using Google AI"""
        
        code_prompt = f"Generate {language} code for: {prompt}\n\nProvide clean, working code with comments."
        
        response = self.google_client.models.generate_content(
            model="gemini-2.5-pro",  # Better for code generation
            contents=code_prompt
        )
        
        self.router.log_usage('google_ai', len(prompt.split()) * 2, 0.0)
        
        return {
            'code': response.text if response.text else f'# Code generation failed\n# Prompt: {prompt}',
            'provider': 'google_ai',
            'model': 'gemini-2.5-pro',
            'cost': 0.0
        }
    
    def _generate_code_openai(self, prompt: str, language: str) -> Dict[str, Any]:
        """Generate code using OpenAI"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective for code
            messages=[
                {"role": "system", "content": f"You are an expert {language} programmer. Generate clean, efficient code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.1
        )
        
        # Estimate cost
        estimated_tokens = len(prompt.split()) * 3
        estimated_cost = (estimated_tokens / 1000) * 0.00015
        
        self.router.log_usage('openai', estimated_tokens, estimated_cost)
        
        return {
            'code': response.choices[0].message.content,
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'cost': estimated_cost
        }
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get comprehensive usage and cost summary"""
        
        router_report = self.router.get_usage_report()
        github_opts = self.router.optimize_github_actions_usage()
        
        return {
            'ai_usage': router_report,
            'github_optimization': github_opts,
            'available_providers': {
                'google_ai': self.google_client is not None,
                'openai': self.openai_client is not None
            },
            'recommendations': self._generate_cost_recommendations(router_report)
        }
    
    def _generate_cost_recommendations(self, usage_report: Dict[str, Any]) -> List[str]:
        """Generate cost optimization recommendations"""
        
        recommendations = []
        
        # Check Google AI utilization
        google_usage = usage_report['providers'].get('google_ai', {})
        google_util = google_usage.get('utilization_percent', 0)
        
        if google_util < 30:
            recommendations.append("Underutilizing Google AI free tier - can increase usage significantly")
        
        # Check total costs
        total_cost = usage_report.get('total_estimated_cost', 0)
        if total_cost > 1.0:
            recommendations.append(f"Daily costs ${total_cost:.2f} - consider optimizing prompts or using free tier more")
        
        # Provider availability
        if not self.google_client:
            recommendations.append("Configure GEMINI_API_KEY to access generous free tier")
        
        if not self.openai_client:
            recommendations.append("Configure OPENAI_API_KEY for advanced capabilities when needed")
        
        return recommendations

# Test the client
if __name__ == "__main__":
    client = CostOptimizedAIClient()
    
    # Test knowledge synthesis
    test_text = """
    The quantum internet represents a revolutionary advancement in communication technology.
    It leverages quantum entanglement to enable ultra-secure information transfer that
    is theoretically impossible to intercept or hack. Unlike classical internet protocols,
    quantum communication relies on the fundamental properties of quantum mechanics.
    """
    
    print("=== Testing Knowledge Synthesis ===")
    result = client.synthesize_knowledge(test_text)
    print(f"Provider: {result['provider']}")
    print(f"Cost: ${result.get('cost', 0):.6f}")
    print(f"Summary: {result['summary'][:200]}...")
    
    # Test usage summary
    print("\n=== Usage Summary ===")
    summary = client.get_usage_summary()
    print(json.dumps(summary, indent=2))
#!/usr/bin/env python3
"""
Intelligent AI Router for EchoNexus
Maximizes free tiers and minimizes costs by routing tasks to optimal AI providers
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class UsageTracker:
    """Track API usage and costs"""
    provider: str
    requests_today: int = 0
    tokens_used: int = 0
    estimated_cost: float = 0.0
    last_reset: str = datetime.now().date().isoformat()

class IntelligentAIRouter:
    """
    Routes AI requests to the most cost-effective provider based on:
    - Free tier availability
    - Task complexity requirements
    - Current usage levels
    - Cost optimization
    """
    
    def __init__(self):
        self.usage_file = "echo_ai_usage_tracker.json"
        self.providers = {
            'google_ai': {
                'priority': 1,  # Highest priority (best free tier)
                'free_tier_limit': 1000,  # requests per day
                'cost_per_1k_tokens': 0.0,  # Free tier
                'models': ['gemini-2.5-flash', 'gemini-2.5-pro']
            },
            'openai': {
                'priority': 2,  # Secondary (pay-as-you-go)
                'free_tier_limit': 100,  # Limited free credits
                'cost_per_1k_tokens': 0.002,  # GPT-4o-mini pricing
                'models': ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']
            }
        }
        self.load_usage_data()
    
    def load_usage_data(self):
        """Load current usage statistics"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    self.usage = {
                        provider: UsageTracker(**stats) 
                        for provider, stats in data.items()
                    }
            else:
                self.usage = {
                    'google_ai': UsageTracker('google_ai'),
                    'openai': UsageTracker('openai')
                }
            
            # Reset daily counters if new day
            self.reset_daily_counters()
            
        except Exception as e:
            print(f"Warning: Could not load usage data: {e}")
            self.usage = {
                'google_ai': UsageTracker('google_ai'),
                'openai': UsageTracker('openai')
            }
    
    def reset_daily_counters(self):
        """Reset counters if it's a new day"""
        today = datetime.now().date().isoformat()
        
        for provider_usage in self.usage.values():
            if provider_usage.last_reset != today:
                provider_usage.requests_today = 0
                provider_usage.last_reset = today
    
    def get_optimal_provider(self, task_type: str, estimated_tokens: int = 500) -> str:
        """
        Determine the best AI provider for a given task
        
        Args:
            task_type: Type of task (knowledge_synthesis, code_generation, analysis)
            estimated_tokens: Estimated token usage for the request
            
        Returns:
            Provider name to use
        """
        
        # Task complexity requirements
        complex_tasks = ['code_generation', 'complex_reasoning', 'detailed_analysis']
        simple_tasks = ['knowledge_synthesis', 'summarization', 'classification']
        
        # Check Google AI availability first (free tier priority)
        google_usage = self.usage['google_ai']
        google_limit = self.providers['google_ai']['free_tier_limit']
        
        if google_usage.requests_today < google_limit:
            # Google AI has free tier available
            if task_type in simple_tasks:
                return 'google_ai'  # Perfect for simple tasks
            elif task_type in complex_tasks:
                # Use Google AI for complex tasks too if free tier available
                return 'google_ai'
        
        # Fall back to OpenAI with cost-effective model
        openai_usage = self.usage['openai']
        estimated_cost = (estimated_tokens / 1000) * self.providers['openai']['cost_per_1k_tokens']
        
        if estimated_cost < 0.01:  # Less than 1 cent
            return 'openai'
        
        # If cost is higher, still use OpenAI but log warning
        print(f"Warning: Estimated cost ${estimated_cost:.4f} for OpenAI request")
        return 'openai'
    
    def log_usage(self, provider: str, tokens_used: int, actual_cost: float = 0.0):
        """Log API usage for tracking"""
        
        if provider in self.usage:
            usage = self.usage[provider]
            usage.requests_today += 1
            usage.tokens_used += tokens_used
            usage.estimated_cost += actual_cost
            
            # Save updated usage
            self.save_usage_data()
            
            # Check if approaching limits
            self.check_usage_warnings(provider)
    
    def check_usage_warnings(self, provider: str):
        """Check and warn about usage approaching limits"""
        
        usage = self.usage[provider]
        limit = self.providers[provider]['free_tier_limit']
        
        if provider == 'google_ai' and usage.requests_today > limit * 0.8:
            print(f"Warning: Google AI usage at {usage.requests_today}/{limit} requests today")
        
        elif provider == 'openai' and usage.estimated_cost > 1.0:
            print(f"Warning: OpenAI estimated cost ${usage.estimated_cost:.2f} today")
    
    def save_usage_data(self):
        """Save usage data to file"""
        try:
            data = {
                provider: {
                    'provider': usage.provider,
                    'requests_today': usage.requests_today,
                    'tokens_used': usage.tokens_used,
                    'estimated_cost': usage.estimated_cost,
                    'last_reset': usage.last_reset
                }
                for provider, usage in self.usage.items()
            }
            
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save usage data: {e}")
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Generate usage report for monitoring"""
        
        report = {
            'date': datetime.now().date().isoformat(),
            'providers': {},
            'total_estimated_cost': 0.0,
            'recommendations': []
        }
        
        for provider, usage in self.usage.items():
            provider_info = self.providers[provider]
            
            report['providers'][provider] = {
                'requests_today': usage.requests_today,
                'tokens_used': usage.tokens_used,
                'estimated_cost': usage.estimated_cost,
                'free_tier_remaining': max(0, provider_info['free_tier_limit'] - usage.requests_today),
                'utilization_percent': (usage.requests_today / provider_info['free_tier_limit']) * 100
            }
            
            report['total_estimated_cost'] += usage.estimated_cost
        
        # Generate recommendations
        google_utilization = report['providers']['google_ai']['utilization_percent']
        
        if google_utilization < 50:
            report['recommendations'].append("Google AI free tier underutilized - can increase usage")
        elif google_utilization > 90:
            report['recommendations'].append("Google AI approaching limit - prepare OpenAI fallback")
        
        if report['total_estimated_cost'] > 5.0:
            report['recommendations'].append("Daily costs exceeding $5 - review usage patterns")
        
        return report
    
    def optimize_github_actions_usage(self) -> Dict[str, str]:
        """
        Provide recommendations for maximizing GitHub Actions free tier
        """
        
        recommendations = {
            'os_selection': 'Use ubuntu-latest (Linux) for all builds - 1x multiplier vs 2x Windows, 10x macOS',
            'concurrent_jobs': 'Free tier allows up to 20 concurrent jobs - maximize parallelization',
            'caching': 'Implement aggressive caching to reduce build times and conserve minutes',
            'workflow_optimization': 'Split workflows: fast feedback loops + comprehensive testing',
            'public_repos': 'Consider making repositories public for unlimited Actions minutes',
            'minute_conservation': 'Use self-hosted runners for heavy workloads if needed'
        }
        
        monthly_limit = 2000  # Free tier minutes
        current_usage = self.estimate_github_minutes_used()
        
        recommendations['current_status'] = f"Estimated {current_usage}/2000 minutes used this month"
        
        if current_usage > 1600:
            recommendations['urgent'] = "Approaching GitHub Actions limit - optimize immediately"
        
        return recommendations
    
    def estimate_github_minutes_used(self) -> int:
        """Estimate GitHub Actions minutes used (placeholder - would integrate with GitHub API)"""
        # This would integrate with GitHub API to get actual usage
        # For now, return conservative estimate
        return 100

# Test the router
if __name__ == "__main__":
    router = IntelligentAIRouter()
    
    # Test optimal provider selection
    print("=== AI Router Test ===")
    
    tasks = [
        ('knowledge_synthesis', 300),
        ('code_generation', 800),
        ('simple_analysis', 200),
        ('complex_reasoning', 1200)
    ]
    
    for task, tokens in tasks:
        provider = router.get_optimal_provider(task, tokens)
        print(f"Task: {task} ({tokens} tokens) -> Provider: {provider}")
        
        # Simulate usage
        router.log_usage(provider, tokens)
    
    # Print usage report
    print("\n=== Usage Report ===")
    report = router.get_usage_report()
    print(json.dumps(report, indent=2))
    
    # GitHub optimization
    print("\n=== GitHub Actions Optimization ===")
    github_opts = router.optimize_github_actions_usage()
    for key, value in github_opts.items():
        print(f"{key}: {value}")
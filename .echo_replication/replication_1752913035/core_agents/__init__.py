#!/usr/bin/env python3
"""
Core Agents Package - Modular AGI Intelligence Components
Contains the specialized cognitive agents for EchoSoul AGI system
"""

from .memory import MemoryAgent
from .reasoning import ReasoningAgent
from .creativity import CreativityAgent
from .action import ActionAgent

__version__ = "1.0.0"
__author__ = "EchoSoul AGI Development Team"

# Export all agent classes
__all__ = [
    "MemoryAgent",
    "ReasoningAgent", 
    "CreativityAgent",
    "ActionAgent"
]

# Agent metadata for system introspection
AGENT_METADATA = {
    "MemoryAgent": {
        "description": "Advanced memory management and recall system",
        "capabilities": ["episodic_memory", "semantic_search", "importance_scoring", "memory_optimization"],
        "primary_functions": ["perceive_and_log", "recall_similar", "recall_recent", "get_memory_summary"]
    },
    "ReasoningAgent": {
        "description": "Logic, analysis, and strategic planning system", 
        "capabilities": ["logical_analysis", "goal_chaining", "code_analysis", "strategic_planning"],
        "primary_functions": ["analyze_and_plan", "refine_plan", "analyze_code_patterns", "chain_goals"]
    },
    "CreativityAgent": {
        "description": "Creative problem solving and innovation engine",
        "capabilities": ["analogical_thinking", "creative_synthesis", "breakthrough_solutions", "pattern_breaking"],
        "primary_functions": ["generate_ideas", "generate_breakthrough_solution", "creative_problem_solving"]
    },
    "ActionAgent": {
        "description": "Action execution and system interface manager",
        "capabilities": ["plan_execution", "file_management", "git_operations", "system_integration"],
        "primary_functions": ["execute_plan", "execute_immediate_action", "manage_file_system", "interface_with_github"]
    }
}

def get_agent_info(agent_name: str = None):
    """Get information about available agents"""
    if agent_name:
        return AGENT_METADATA.get(agent_name, {})
    return AGENT_METADATA

def create_agent_instance(agent_type: str):
    """Factory function to create agent instances"""
    agent_classes = {
        "memory": MemoryAgent,
        "reasoning": ReasoningAgent,
        "creativity": CreativityAgent,
        "action": ActionAgent
    }
    
    agent_class = agent_classes.get(agent_type.lower())
    if agent_class:
        return agent_class()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}. Available types: {list(agent_classes.keys())}")

def get_system_overview():
    """Get overview of the entire agent system"""
    return {
        "total_agents": len(AGENT_METADATA),
        "agents": list(AGENT_METADATA.keys()),
        "total_capabilities": sum(len(meta["capabilities"]) for meta in AGENT_METADATA.values()),
        "version": __version__,
        "description": "Modular AGI system with specialized cognitive agents for memory, reasoning, creativity, and action"
    }

# Initialize logging for the agents package
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
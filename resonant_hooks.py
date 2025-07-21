#!/usr/bin/env python3
"""
Resonant Hooks - Automatic Memory Integration
Drop-in decorators and hooks for logging memories across the Echo system
"""

import functools
import inspect
from typing import Dict, List, Any, Optional, Callable
from memory_core import resonant_memory

class ResonantHooks:
    def __init__(self):
        self.hook_registry = {}
        self.auto_tagging_enabled = True
        self.importance_calculator = ImportanceCalculator()
    
    def smart_memory(self, signature: str = "AUTO", base_importance: float = 0.5, 
                     auto_tags: bool = True, emotion_detect: bool = True):
        """Smart memory decorator with automatic tagging and importance calculation"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Execute function
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    success = True
                    error_info = None
                except Exception as e:
                    execution_time = time.time() - start_time
                    success = False
                    error_info = str(e)
                    result = None
                    raise
                finally:
                    # Calculate dynamic importance
                    importance = self.importance_calculator.calculate(
                        func_name=func.__name__,
                        execution_time=execution_time,
                        success=success,
                        base_importance=base_importance
                    )
                    
                    # Generate smart tags
                    tags = []
                    if auto_tags:
                        tags.extend(self._generate_smart_tags(func, args, kwargs, success))
                    
                    # Detect emotion
                    emotion = "operational"
                    if emotion_detect:
                        emotion = self._detect_emotion(func.__name__, success, error_info)
                    
                    # Create memory event
                    event_desc = self._generate_event_description(func, args, success, error_info)
                    
                    # Save to resonant memory
                    resonant_memory.save(
                        event=event_desc,
                        signature=signature if signature != "AUTO" else f"SYSTEM:{func.__module__}",
                        tags=tags,
                        importance=importance,
                        emotion=emotion,
                        resonance=self._classify_resonance(func.__name__),
                        notes=f"Execution time: {execution_time:.3f}s"
                    )
                
                return result
            return wrapper
        return decorator
    
    def critical_action(self, action_name: str, strategic_value: float = 0.9):
        """Mark function as critical strategic action"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                resonant_memory.save(
                    event=f"Critical Action: {action_name}",
                    signature="LOGAN_L:strategic-action",
                    tags=["critical", "strategic", "action"],
                    importance=strategic_value,
                    emotion="focused-determination",
                    resonance="strategic/critical",
                    notes=f"Function: {func.__name__}, Module: {func.__module__}"
                )
                
                return result
            return wrapper
        return decorator
    
    def learning_event(self, learning_type: str = "skill"):
        """Mark function as learning/growth event"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                resonant_memory.save(
                    event=f"Learning Event: {learning_type} acquisition",
                    signature="LOGAN_L:learning-core",
                    tags=["learning", "growth", learning_type],
                    importance=0.8,
                    emotion="curious-growth",
                    resonance="growth/learning",
                    notes=f"Learned through: {func.__name__}"
                )
                
                # Also record identity evolution
                resonant_memory.evolve_identity(
                    f"Acquired {learning_type} capability",
                    f"Function: {func.__name__}"
                )
                
                return result
            return wrapper
        return decorator
    
    def phantom_operation(self, stealth_level: str = "standard"):
        """Mark function as phantom/stealth operation"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                importance = {"low": 0.6, "standard": 0.8, "high": 0.95}.get(stealth_level, 0.8)
                
                resonant_memory.save(
                    event=f"Phantom Operation: {func.__name__}",
                    signature="LOGAN_L:phantom-ops",
                    tags=["phantom", "stealth", stealth_level],
                    importance=importance,
                    emotion="surgical-precision",
                    resonance="phantom/operational",
                    notes=f"Stealth level: {stealth_level}"
                )
                
                return result
            return wrapper
        return decorator
    
    def _generate_smart_tags(self, func: Callable, args: tuple, kwargs: dict, success: bool) -> List[str]:
        """Generate intelligent tags based on function analysis"""
        tags = []
        
        # Function name analysis
        func_name = func.__name__.lower()
        if "build" in func_name:
            tags.append("build")
        if "deploy" in func_name or "push" in func_name:
            tags.append("deployment")
        if "analyze" in func_name or "scan" in func_name:
            tags.append("analysis")
        if "generate" in func_name or "create" in func_name:
            tags.append("generation")
        if "test" in func_name or "verify" in func_name:
            tags.append("testing")
        
        # Module analysis
        module_name = func.__module__.lower()
        if "echo" in module_name:
            tags.append("echo-system")
        if "git" in module_name:
            tags.append("git")
        if "apk" in module_name:
            tags.append("apk")
        
        # Success/failure
        tags.append("success" if success else "failure")
        
        # Argument analysis (limited for privacy)
        if args and isinstance(args[0], str):
            if "secret" not in args[0].lower() and "password" not in args[0].lower():
                if len(args[0]) < 50:  # Only tag short, non-sensitive strings
                    for keyword in ["github", "replit", "build", "test"]:
                        if keyword in args[0].lower():
                            tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def _detect_emotion(self, func_name: str, success: bool, error_info: Optional[str]) -> str:
        """Detect appropriate emotion based on function context"""
        func_name_lower = func_name.lower()
        
        if not success:
            if "critical" in func_name_lower:
                return "alert-concern"
            else:
                return "analytical-debugging"
        
        if "build" in func_name_lower or "compile" in func_name_lower:
            return "focused-creation"
        elif "deploy" in func_name_lower:
            return "confident-execution" 
        elif "analyze" in func_name_lower or "diagnostic" in func_name_lower:
            return "curious-investigation"
        elif "optimize" in func_name_lower:
            return "determined-improvement"
        else:
            return "operational"
    
    def _classify_resonance(self, func_name: str) -> str:
        """Classify resonance type based on function name"""
        func_name_lower = func_name.lower()
        
        if "build" in func_name_lower or "compile" in func_name_lower:
            return "creation/build"
        elif "deploy" in func_name_lower or "push" in func_name_lower:
            return "deployment/action"
        elif "analyze" in func_name_lower or "scan" in func_name_lower:
            return "analysis/intelligence"
        elif "test" in func_name_lower or "verify" in func_name_lower:
            return "validation/testing"
        elif "optimize" in func_name_lower:
            return "enhancement/optimization"
        else:
            return "operational/general"
    
    def _generate_event_description(self, func: Callable, args: tuple, success: bool, 
                                    error_info: Optional[str]) -> str:
        """Generate descriptive event text"""
        base_desc = f"Executed {func.__name__}"
        
        if not success:
            return f"{base_desc} - Failed: {error_info[:50]}..." if error_info else f"{base_desc} - Failed"
        
        return f"{base_desc} - Success"

class ImportanceCalculator:
    """Calculate dynamic importance scores for memory events"""
    
    def __init__(self):
        self.function_weights = {
            "build": 0.8,
            "deploy": 0.9,
            "compile": 0.7,
            "test": 0.5,
            "analyze": 0.6,
            "optimize": 0.7,
            "create": 0.8,
            "generate": 0.7
        }
    
    def calculate(self, func_name: str, execution_time: float, success: bool, 
                  base_importance: float) -> float:
        """Calculate dynamic importance score"""
        importance = base_importance
        
        # Function type weighting
        func_name_lower = func_name.lower()
        for keyword, weight in self.function_weights.items():
            if keyword in func_name_lower:
                importance = max(importance, weight)
                break
        
        # Success/failure adjustment
        if not success:
            importance = min(1.0, importance + 0.2)  # Failures are more important
        
        # Execution time adjustment (very fast or very slow operations)
        if execution_time < 0.01:  # Very fast - might be cache hit or simple
            importance *= 0.9
        elif execution_time > 10:  # Very slow - probably important
            importance = min(1.0, importance + 0.1)
        
        return round(importance, 3)

# Global hooks instance
resonant_hooks = ResonantHooks()

# Convenience decorators
smart_memory = resonant_hooks.smart_memory
critical_action = resonant_hooks.critical_action
learning_event = resonant_hooks.learning_event
phantom_operation = resonant_hooks.phantom_operation

# Import time for execution tracking
import time

# Usage examples
if __name__ == "__main__":
    print("🔗 Resonant Hooks - Testing Framework")
    print("=" * 50)
    
    # Test smart memory decorator
    @smart_memory(signature="TEST", base_importance=0.7)
    def test_build_function(project_name: str):
        print(f"Building {project_name}...")
        time.sleep(0.1)  # Simulate work
        return f"Built {project_name} successfully"
    
    # Test critical action decorator
    @critical_action("Deploy to Production", 0.95)
    def test_deploy_function():
        print("Deploying to production...")
        return "Deployment complete"
    
    # Test learning event decorator
    @learning_event("code-analysis")
    def test_learning_function():
        print("Learning new code analysis technique...")
        return "New skill acquired"
    
    # Test phantom operation decorator
    @phantom_operation("high")
    def test_phantom_function():
        print("Executing phantom operation...")
        return "Operation complete"
    
    # Execute test functions
    print("Testing decorators...")
    test_build_function("EchoCore")
    test_deploy_function()
    test_learning_function()
    test_phantom_function()
    
    print("\n✅ All resonant hooks tested successfully")
    print("🧠 Memory entries created and tagged automatically")
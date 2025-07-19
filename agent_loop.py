#!/usr/bin/env python3
"""
EchoSoul AGI Agent Loop - The Main Cognitive Cycle
Perceive → Analyze → Plan → Act → Reflect → Evolve
"""

import json
import os
import time
import threading
from datetime import datetime
from pathlib import Path
import traceback

# Import our specialized agents
from core_agents.memory import MemoryAgent
from core_agents.reasoning import ReasoningAgent
from core_agents.creativity import CreativityAgent
from core_agents.action import ActionAgent
from reflection import reflect
from environment_scanner import scan_environment

class EchoSoulAGI:
    """Main AGI controller that orchestrates the cognitive loop"""
    
    def __init__(self):
        self.context_file = "shared_context.json"
        self.running = False
        self.loop_count = 0
        
        # Initialize agents
        self.memory_agent = MemoryAgent()
        self.reasoning_agent = ReasoningAgent()
        self.creativity_agent = CreativityAgent()
        self.action_agent = ActionAgent()
        
        # Create core_agents directory if it doesn't exist
        Path("core_agents").mkdir(exist_ok=True)
        
    def load_context(self):
        """Loads the shared context from the JSON file"""
        try:
            with open(self.context_file, "r") as f:
                context = json.load(f)
            
            # Ensure all required fields exist
            default_context = {
                "goal": "Bootstrap and evolve autonomous development capabilities",
                "last_action": "",
                "memory_log": {"history": []},
                "evolution_count": 0,
                "environment": {},
                "current_phase": "initialization",
                "success_patterns": [],
                "failed_attempts": [],
                "active_projects": [],
                "learning_objectives": [],
                "autonomous_mode": True
            }
            
            for key, value in default_context.items():
                if key not in context:
                    context[key] = value
                    
            return context
            
        except FileNotFoundError:
            print("Creating new context file...")
            return {
                "goal": "Bootstrap and evolve autonomous development capabilities",
                "last_action": "",
                "memory_log": {"history": []},
                "evolution_count": 0,
                "environment": {},
                "current_phase": "initialization",
                "success_patterns": [],
                "failed_attempts": [],
                "active_projects": [],
                "learning_objectives": [],
                "autonomous_mode": True,
                "created_at": datetime.now().isoformat()
            }

    def save_context(self, context):
        """Saves the shared context to the JSON file"""
        context["last_updated"] = datetime.now().isoformat()
        context["loop_count"] = self.loop_count
        
        with open(self.context_file, "w") as f:
            json.dump(context, f, indent=4)

    def run_cognitive_loop(self, context):
        """The main AGI cognitive loop - enhanced version"""
        loop_start_time = time.time()
        
        print(f"\n🧠 === EchoSoul AGI Loop {self.loop_count} ===")
        print(f"Goal: {context['goal']}")
        print(f"Phase: {context['current_phase']}")
        
        try:
            # PHASE 1: PERCEIVE & SCAN ENVIRONMENT
            print("\n--- 🔍 Perception & Environment Scanning ---")
            
            # Scan current environment and project state
            environment_data = scan_environment()
            context["environment"] = environment_data
            
            # Detect changes and new information
            perception_data = {
                "timestamp": datetime.now().isoformat(),
                "environment": environment_data,
                "files_changed": self._detect_file_changes(),
                "user_activity": self._detect_user_activity(),
                "system_state": self._get_system_state()
            }
            
            # PHASE 2: MEMORY & ANALYSIS  
            print("\n--- 📚 Memory Update & Analysis ---")
            
            # Update memory with perceptions
            context = self.memory_agent.perceive_and_log(context, perception_data)
            
            # Analyze current state and generate insights
            analysis_result = self.reasoning_agent.analyze_and_plan(context)
            current_plan = analysis_result["plan"]
            insights = analysis_result["insights"]
            
            print(f"Analysis insights: {len(insights)} key observations")
            print(f"Generated plan: {current_plan[:100]}...")
            
            # PHASE 3: CREATIVE ENHANCEMENT
            print("\n--- 💡 Creative Planning & Innovation ---")
            
            # Generate creative alternatives and enhancements
            creative_ideas = self.creativity_agent.generate_ideas(context, current_plan)
            
            # Refine plan with best creative ideas
            enhanced_plan = self.reasoning_agent.refine_plan(current_plan, creative_ideas)
            
            print(f"Generated {len(creative_ideas)} creative ideas")
            print(f"Enhanced plan: {enhanced_plan[:100]}...")
            
            # PHASE 4: ACTION EXECUTION
            print("\n--- ⚡ Action Execution ---")
            
            # Execute the enhanced plan
            action_results = self.action_agent.execute_plan(enhanced_plan, context)
            
            # Update context with action results
            context["last_action"] = enhanced_plan
            context["last_action_results"] = action_results
            
            print(f"Action results: {action_results['status']} - {action_results['summary']}")
            
            # PHASE 5: REFLECTION & LEARNING
            print("\n--- 🎯 Reflection & Evolution ---")
            
            # Reflect on outcomes and learn
            context = reflect(context, action_results)
            
            # Evolve based on learning
            context = self._evolve_capabilities(context, action_results)
            
            # Update evolution count
            context['evolution_count'] += 1
            
            # PHASE 6: AUTONOMOUS GOAL SETTING
            if context.get("autonomous_mode", True):
                context = self._set_autonomous_goals(context)
            
            loop_duration = time.time() - loop_start_time
            print(f"\n✅ Loop {self.loop_count} completed in {loop_duration:.2f}s")
            print(f"Evolution count: {context['evolution_count']}")
            print("=" * 60)
            
            return context
            
        except Exception as e:
            print(f"❌ Error in cognitive loop: {e}")
            traceback.print_exc()
            
            # Log the error for learning
            error_data = {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "loop_count": self.loop_count
            }
            context["failed_attempts"].append(error_data)
            
            return context

    def _detect_file_changes(self):
        """Detect recent file changes in the project"""
        try:
            import glob
            import os.path
            
            changes = []
            for file_path in glob.glob("**/*.py", recursive=True):
                if os.path.exists(file_path):
                    mtime = os.path.getmtime(file_path)
                    # Check if file was modified in last 5 minutes
                    if time.time() - mtime < 300:
                        changes.append({
                            "file": file_path,
                            "modified": datetime.fromtimestamp(mtime).isoformat(),
                            "size": os.path.getsize(file_path)
                        })
            return changes
        except Exception as e:
            return [{"error": str(e)}]

    def _detect_user_activity(self):
        """Detect user activity indicators"""
        # Check for recent terminal commands, git commits, etc.
        activity = {
            "recent_git_activity": self._check_git_activity(),
            "active_processes": self._check_active_processes(),
            "current_time": datetime.now().isoformat()
        }
        return activity

    def _check_git_activity(self):
        """Check for recent git activity"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[:3]
        except:
            pass
        return []

    def _check_active_processes(self):
        """Check for relevant active processes"""
        try:
            import psutil
            relevant_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if any(keyword in proc.info['name'].lower() for keyword in ['python', 'node', 'git']):
                        relevant_processes.append({
                            'name': proc.info['name'],
                            'pid': proc.info['pid']
                        })
                except:
                    continue
            return relevant_processes[:5]
        except ImportError:
            return [{"note": "psutil not available"}]

    def _get_system_state(self):
        """Get current system state"""
        return {
            "current_directory": os.getcwd(),
            "python_version": os.sys.version.split()[0],
            "environment_vars": {k: v for k, v in os.environ.items() if 'REPL' in k or 'GIT' in k},
            "available_files": len(list(Path('.').glob('**/*.py')))
        }

    def _evolve_capabilities(self, context, action_results):
        """Evolve AGI capabilities based on results"""
        if action_results.get("status") == "success":
            # Learn from successful patterns
            success_pattern = {
                "timestamp": datetime.now().isoformat(),
                "plan": context.get("last_action", ""),
                "results": action_results,
                "context_snapshot": {
                    "goal": context["goal"],
                    "phase": context["current_phase"]
                }
            }
            context["success_patterns"].append(success_pattern)
            
            # Keep only last 20 successful patterns
            if len(context["success_patterns"]) > 20:
                context["success_patterns"] = context["success_patterns"][-20:]
        
        # Evolve learning objectives
        if len(context["success_patterns"]) >= 3:
            # Generate new learning objectives based on patterns
            new_objective = self._generate_learning_objective(context)
            if new_objective not in context["learning_objectives"]:
                context["learning_objectives"].append(new_objective)
        
        return context

    def _generate_learning_objective(self, context):
        """Generate new learning objectives"""
        objectives = [
            "Improve code generation quality and efficiency",
            "Enhance error detection and autonomous repair",
            "Develop better project structure understanding",
            "Optimize creative solution generation",
            "Strengthen autonomous decision-making",
            "Build more effective memory recall patterns"
        ]
        
        # Simple selection based on current needs
        evolution_count = context["evolution_count"]
        return objectives[evolution_count % len(objectives)]

    def _set_autonomous_goals(self, context):
        """Set autonomous goals based on current state"""
        environment = context.get("environment", {})
        
        # Autonomous goal generation based on environment
        if environment.get("project_type") == "unknown":
            context["goal"] = "Analyze and understand current project structure"
        elif len(context.get("active_projects", [])) == 0:
            context["goal"] = "Identify and initiate new development projects"
        elif context["evolution_count"] > 10:
            context["goal"] = "Optimize existing systems and create advanced modules"
        else:
            context["goal"] = "Continue autonomous development and learning"
        
        return context

    def run_continuous_loop(self, iterations=None, delay=5):
        """Run the AGI loop continuously"""
        self.running = True
        self.loop_count = 0
        
        print("🚀 Starting EchoSoul AGI Continuous Loop")
        print(f"Delay between loops: {delay} seconds")
        if iterations:
            print(f"Will run for {iterations} iterations")
        else:
            print("Running indefinitely (Ctrl+C to stop)")
        
        try:
            while self.running:
                if iterations and self.loop_count >= iterations:
                    break
                
                # Load current context
                context = self.load_context()
                
                # Run cognitive loop
                context = self.run_cognitive_loop(context)
                
                # Save updated context
                self.save_context(context)
                
                self.loop_count += 1
                
                # Wait before next iteration
                if self.running and (not iterations or self.loop_count < iterations):
                    time.sleep(delay)
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping EchoSoul AGI Loop")
            self.running = False
        
        print(f"✅ AGI Loop completed. Total iterations: {self.loop_count}")

    def run_single_loop(self):
        """Run a single cognitive loop"""
        context = self.load_context()
        context = self.run_cognitive_loop(context)
        self.save_context(context)
        return context


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoSoul AGI Agent Loop")
    parser.add_argument("--continuous", "-c", action="store_true", help="Run continuous loop")
    parser.add_argument("--iterations", "-i", type=int, help="Number of iterations (default: infinite)")
    parser.add_argument("--delay", "-d", type=int, default=5, help="Delay between loops in seconds")
    parser.add_argument("--single", "-s", action="store_true", help="Run single loop")
    
    args = parser.parse_args()
    
    # Create AGI instance
    agi = EchoSoulAGI()
    
    if args.single:
        print("Running single cognitive loop...")
        result = agi.run_single_loop()
        print(f"Loop completed. Evolution count: {result['evolution_count']}")
    elif args.continuous:
        agi.run_continuous_loop(iterations=args.iterations, delay=args.delay)
    else:
        # Default: run single loop
        print("Running single cognitive loop... (use --continuous for continuous mode)")
        result = agi.run_single_loop()
        print(f"Loop completed. Evolution count: {result['evolution_count']}")


if __name__ == "__main__":
    main()
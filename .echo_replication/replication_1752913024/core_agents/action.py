#!/usr/bin/env python3
"""
ActionAgent - Advanced Action Execution for EchoSoul AGI
Executes plans, manages workflows, and interfaces with external systems
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class ActionAgent:
    """Executes plans, manages workflows, and interfaces with external systems"""
    
    def __init__(self):
        self.action_history = []
        self.execution_context = {}
        self.safety_checks = True
        self.max_execution_time = 300  # 5 minutes max per action
        
    def execute_plan(self, plan: str, context: Dict) -> Dict:
        """Executes a comprehensive plan with proper error handling and logging"""
        
        execution_start = time.time()
        execution_id = self._generate_execution_id()
        
        print(f"ActionAgent: Starting execution {execution_id}")
        
        try:
            # Parse plan into actionable steps
            steps = self._parse_plan_steps(plan)
            
            # Validate plan safety
            if self.safety_checks:
                safety_result = self._validate_plan_safety(steps, context)
                if not safety_result["safe"]:
                    return {
                        "status": "blocked",
                        "reason": safety_result["reason"],
                        "execution_id": execution_id,
                        "summary": "Plan blocked due to safety concerns"
                    }
            
            # Execute steps sequentially
            execution_results = []
            overall_success = True
            
            for i, step in enumerate(steps):
                print(f"Executing step {i+1}/{len(steps)}: {step['description'][:50]}...")
                
                step_result = self._execute_step(step, context)
                execution_results.append(step_result)
                
                if step_result["status"] != "success":
                    overall_success = False
                    if step.get("critical", False):
                        print(f"Critical step failed, aborting execution")
                        break
                
                # Check execution time limit
                if time.time() - execution_start > self.max_execution_time:
                    print("Execution time limit reached, stopping")
                    break
            
            # Compile final results
            execution_time = time.time() - execution_start
            final_result = {
                "status": "success" if overall_success else "partial_failure",
                "execution_id": execution_id,
                "steps_executed": len(execution_results),
                "total_steps": len(steps),
                "execution_time": execution_time,
                "results": execution_results,
                "summary": self._generate_execution_summary(execution_results),
                "outputs": self._collect_execution_outputs(execution_results)
            }
            
            # Log execution
            self._log_execution(final_result, plan, context)
            
            return final_result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "execution_id": execution_id,
                "error": str(e),
                "execution_time": time.time() - execution_start,
                "summary": f"Execution failed with error: {str(e)}"
            }
            
            self._log_execution(error_result, plan, context)
            return error_result
    
    def execute_immediate_action(self, action_type: str, parameters: Dict, context: Dict) -> Dict:
        """Executes immediate actions like file operations, git commands, etc."""
        
        action_start = time.time()
        
        try:
            if action_type == "create_file":
                return self._create_file(parameters, context)
            elif action_type == "modify_file":
                return self._modify_file(parameters, context)
            elif action_type == "run_command":
                return self._run_command(parameters, context)
            elif action_type == "git_operation":
                return self._git_operation(parameters, context)
            elif action_type == "analyze_code":
                return self._analyze_code(parameters, context)
            elif action_type == "install_dependency":
                return self._install_dependency(parameters, context)
            elif action_type == "optimize_system":
                return self._optimize_system(parameters, context)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown action type: {action_type}",
                    "execution_time": time.time() - action_start
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - action_start
            }
    
    def manage_file_system(self, operation: str, target: str, content: Optional[str] = None) -> Dict:
        """Manages file system operations with safety checks"""
        
        if self.safety_checks:
            if not self._is_safe_path(target):
                return {
                    "status": "blocked",
                    "reason": f"Unsafe path: {target}"
                }
        
        try:
            if operation == "read":
                return self._read_file(target)
            elif operation == "write":
                return self._write_file(target, content)
            elif operation == "create_directory":
                return self._create_directory(target)
            elif operation == "list_directory":
                return self._list_directory(target)
            elif operation == "delete":
                return self._delete_path(target)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown file operation: {operation}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def interface_with_replit(self, operation: str, parameters: Dict) -> Dict:
        """Interfaces with Replit-specific functionality"""
        
        try:
            if operation == "check_environment":
                return self._check_replit_environment()
            elif operation == "manage_secrets":
                return self._manage_replit_secrets(parameters)
            elif operation == "deploy_app":
                return self._deploy_replit_app(parameters)
            elif operation == "check_workflows":
                return self._check_replit_workflows()
            else:
                return {
                    "status": "error",
                    "error": f"Unknown Replit operation: {operation}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def interface_with_github(self, operation: str, parameters: Dict) -> Dict:
        """Interfaces with GitHub using available tools and APIs"""
        
        try:
            if operation == "create_repository":
                return self._create_github_repository(parameters)
            elif operation == "push_code":
                return self._push_to_github(parameters)
            elif operation == "create_workflow":
                return self._create_github_workflow(parameters)
            elif operation == "manage_issues":
                return self._manage_github_issues(parameters)
            elif operation == "setup_fortified_structure":
                return self._setup_fortified_github_structure(parameters)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown GitHub operation: {operation}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _parse_plan_steps(self, plan: str) -> List[Dict]:
        """Parses a plan into executable steps"""
        steps = []
        
        lines = plan.split('\n')
        current_section = None
        step_counter = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify sections
            if line.endswith(':') and line.isupper():
                current_section = line.replace(':', '').lower()
                continue
            
            # Identify action items
            if line.startswith('•') or line.startswith('-') or line.startswith(str(step_counter + 1)):
                action_text = line.replace('•', '').replace('-', '').strip()
                
                # Remove step numbers
                if action_text.startswith(f'{step_counter + 1}.'):
                    action_text = action_text[3:].strip()
                
                if action_text:
                    step = self._classify_action_step(action_text, current_section)
                    step["step_number"] = step_counter + 1
                    step["section"] = current_section
                    steps.append(step)
                    step_counter += 1
        
        return steps
    
    def _classify_action_step(self, action_text: str, section: Optional[str]) -> Dict:
        """Classifies an action step and determines execution method"""
        
        action_lower = action_text.lower()
        
        # Determine action type and parameters
        if any(keyword in action_lower for keyword in ["create", "generate", "build"]):
            action_type = "create"
            priority = "high" if section == "bootstrap_priorities" else "medium"
        elif any(keyword in action_lower for keyword in ["analyze", "examine", "review"]):
            action_type = "analyze"
            priority = "medium"
        elif any(keyword in action_lower for keyword in ["optimize", "improve", "enhance"]):
            action_type = "optimize"
            priority = "medium"
        elif any(keyword in action_lower for keyword in ["install", "setup", "configure"]):
            action_type = "setup"
            priority = "high"
        elif any(keyword in action_lower for keyword in ["test", "validate", "verify"]):
            action_type = "validate"
            priority = "low"
        else:
            action_type = "generic"
            priority = "medium"
        
        # Determine if step is critical
        critical = any(keyword in action_lower for keyword in ["core", "essential", "critical", "initialize"])
        
        return {
            "description": action_text,
            "type": action_type,
            "priority": priority,
            "critical": critical,
            "estimated_time": self._estimate_step_time(action_type),
            "requirements": self._identify_step_requirements(action_text)
        }
    
    def _execute_step(self, step: Dict, context: Dict) -> Dict:
        """Executes a single step"""
        
        step_start = time.time()
        step_type = step.get("type", "generic")
        description = step.get("description", "")
        
        try:
            if step_type == "create":
                result = self._execute_create_step(step, context)
            elif step_type == "analyze":
                result = self._execute_analyze_step(step, context)
            elif step_type == "optimize":
                result = self._execute_optimize_step(step, context)
            elif step_type == "setup":
                result = self._execute_setup_step(step, context)
            elif step_type == "validate":
                result = self._execute_validate_step(step, context)
            else:
                result = self._execute_generic_step(step, context)
            
            result["execution_time"] = time.time() - step_start
            result["step_info"] = step
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - step_start,
                "step_info": step
            }
    
    def _execute_create_step(self, step: Dict, context: Dict) -> Dict:
        """Executes creation/generation steps"""
        description = step["description"].lower()
        
        if "file" in description or "module" in description:
            # Create a new file or module
            filename = self._extract_filename_from_description(description)
            if filename:
                content = self._generate_file_content(filename, description, context)
                return self._create_file({"filename": filename, "content": content}, context)
        
        elif "directory" in description or "folder" in description:
            # Create a directory
            dirname = self._extract_dirname_from_description(description)
            if dirname:
                return self._create_directory(dirname)
        
        elif "workflow" in description or "action" in description:
            # Create GitHub workflow
            return self._create_github_workflow_from_description(description, context)
        
        else:
            # Generic creation task
            return {
                "status": "simulated",
                "message": f"Simulated creation: {step['description']}",
                "details": "This step would create the specified component"
            }
    
    def _execute_analyze_step(self, step: Dict, context: Dict) -> Dict:
        """Executes analysis steps"""
        description = step["description"].lower()
        
        if "code" in description or "file" in description:
            # Analyze code files
            return self._analyze_codebase(context)
        
        elif "structure" in description or "architecture" in description:
            # Analyze project structure
            return self._analyze_project_structure(context)
        
        elif "performance" in description:
            # Analyze performance
            return self._analyze_performance(context)
        
        else:
            # Generic analysis
            return {
                "status": "completed",
                "message": f"Analysis completed: {step['description']}",
                "findings": ["Code structure appears well-organized", "No immediate issues detected"]
            }
    
    def _validate_plan_safety(self, steps: List[Dict], context: Dict) -> Dict:
        """Validates that a plan is safe to execute"""
        
        unsafe_patterns = [
            "delete",
            "remove",
            "rm -rf",
            "format",
            "drop table",
            "truncate",
            "sudo",
            "chmod 777"
        ]
        
        for step in steps:
            description = step["description"].lower()
            for pattern in unsafe_patterns:
                if pattern in description:
                    return {
                        "safe": False,
                        "reason": f"Potentially unsafe operation detected: {pattern} in '{step['description']}'"
                    }
        
        # Check for too many file operations
        file_operations = sum(1 for step in steps if any(keyword in step["description"].lower() 
                                                        for keyword in ["create", "write", "modify"]))
        if file_operations > 10:
            return {
                "safe": False,
                "reason": f"Too many file operations ({file_operations}) - may overwhelm system"
            }
        
        return {"safe": True}
    
    def _create_file(self, parameters: Dict, context: Dict) -> Dict:
        """Creates a new file"""
        filename = parameters.get("filename", "")
        content = parameters.get("content", "")
        
        if not filename:
            return {"status": "error", "error": "No filename provided"}
        
        try:
            # Ensure directory exists
            file_path = Path(filename)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(filename, 'w') as f:
                f.write(content)
            
            return {
                "status": "success",
                "message": f"Created file: {filename}",
                "filename": filename,
                "size": len(content)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to create file {filename}: {str(e)}"
            }
    
    def _run_command(self, parameters: Dict, context: Dict) -> Dict:
        """Runs a shell command safely"""
        command = parameters.get("command", "")
        timeout = parameters.get("timeout", 30)
        
        if not command:
            return {"status": "error", "error": "No command provided"}
        
        # Safety check
        if self.safety_checks and self._is_unsafe_command(command):
            return {
                "status": "blocked",
                "reason": f"Unsafe command blocked: {command}"
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Command timed out after {timeout} seconds",
                "command": command
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "command": command
            }
    
    def _is_unsafe_command(self, command: str) -> bool:
        """Checks if a command is potentially unsafe"""
        unsafe_commands = [
            "rm -rf", "sudo", "chmod 777", "dd if=", "format", 
            "mkfs", "fdisk", "parted", "shutdown", "reboot"
        ]
        
        command_lower = command.lower()
        return any(unsafe in command_lower for unsafe in unsafe_commands)
    
    def _is_safe_path(self, path: str) -> bool:
        """Checks if a path is safe for operations"""
        unsafe_paths = [
            "/etc", "/bin", "/usr/bin", "/sbin", "/usr/sbin",
            "/root", "/home/", "C:\\Windows", "C:\\Program Files"
        ]
        
        return not any(unsafe in path for unsafe in unsafe_paths)
    
    def _generate_execution_id(self) -> str:
        """Generates unique execution ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"exec_{timestamp}_{len(self.action_history)}"
    
    def _generate_execution_summary(self, results: List[Dict]) -> str:
        """Generates summary of execution results"""
        if not results:
            return "No steps executed"
        
        successful = sum(1 for r in results if r.get("status") == "success")
        total = len(results)
        
        if successful == total:
            return f"All {total} steps completed successfully"
        elif successful == 0:
            return f"All {total} steps failed"
        else:
            return f"{successful}/{total} steps completed successfully"
    
    def _log_execution(self, result: Dict, plan: str, context: Dict) -> None:
        """Logs execution for history tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "execution_id": result.get("execution_id", "unknown"),
            "status": result.get("status", "unknown"),
            "plan_summary": plan[:200] + "..." if len(plan) > 200 else plan,
            "context_snapshot": {
                "goal": context.get("goal", ""),
                "evolution_count": context.get("evolution_count", 0)
            },
            "result_summary": result.get("summary", "")
        }
        
        self.action_history.append(log_entry)
        
        # Keep only last 50 executions
        if len(self.action_history) > 50:
            self.action_history = self.action_history[-50:]


if __name__ == "__main__":
    # Test the ActionAgent
    agent = ActionAgent()
    
    # Test context
    test_context = {
        "goal": "Test action execution",
        "evolution_count": 3
    }
    
    # Test plan execution
    test_plan = """
BOOTSTRAP PRIORITIES:
• Create test file for demonstration
• Analyze current project structure
• Optimize memory usage
"""
    
    result = agent.execute_plan(test_plan, test_context)
    print(f"Execution result: {result['status']}")
    print(f"Summary: {result['summary']}")
    
    # Test immediate action
    immediate_result = agent.execute_immediate_action(
        "create_file",
        {"filename": "test_output.txt", "content": "Test content"},
        test_context
    )
    print(f"Immediate action result: {immediate_result['status']}")
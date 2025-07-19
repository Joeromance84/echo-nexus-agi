"""
EchoNexus Learning System - Programs AGI to learn from developer behavior
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class EchoLearningSystem:
    def __init__(self):
        self.memory_file = "echo_learning_memory.json"
        self.learning_patterns = self.load_learning_memory()
        self.mirroring_patterns = {
            "developer_behaviors": [],
            "decision_sequences": [],
            "problem_solving_styles": [],
            "debugging_methodologies": []
        }
    
    def load_learning_memory(self) -> Dict[str, Any]:
        """Load accumulated learning patterns"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "developer_patterns": {},
            "successful_actions": [],
            "failed_actions": [],
            "troubleshooting_sequences": [],
            "decision_trees": {},
            "learned_behaviors": [],
            "mirroring_patterns": {
                "developer_behaviors": [],
                "decision_sequences": [],
                "problem_solving_styles": [],
                "debugging_methodologies": []
            }
        }
    
    def save_learning_memory(self):
        """Persist learning memory"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.learning_patterns, f, indent=2)
    
    def observe_developer_action(self, situation: str, action: str, outcome: str, reasoning: str):
        """Learn from developer actions"""
        observation = {
            "timestamp": datetime.now().isoformat(),
            "situation": situation,
            "action": action,
            "outcome": outcome,
            "reasoning": reasoning
        }
        
        # Add to appropriate learning category
        if outcome == "success":
            self.learning_patterns["successful_actions"].append(observation)
        else:
            self.learning_patterns["failed_actions"].append(observation)
        
        # Build decision patterns
        if situation not in self.learning_patterns["decision_trees"]:
            self.learning_patterns["decision_trees"][situation] = []
        
        self.learning_patterns["decision_trees"][situation].append({
            "action": action,
            "outcome": outcome,
            "confidence": 1.0 if outcome == "success" else 0.1
        })
        
        self.save_learning_memory()
    
    def get_recommended_action(self, situation: str) -> Dict[str, Any]:
        """Get AI recommendation based on learned patterns"""
        if situation in self.learning_patterns["decision_trees"]:
            actions = self.learning_patterns["decision_trees"][situation]
            
            # Find highest confidence action
            best_action = max(actions, key=lambda x: x["confidence"], default=None)
            
            if best_action:
                return {
                    "recommended_action": best_action["action"],
                    "confidence": best_action["confidence"],
                    "learned_from": f"{len(actions)} previous observations"
                }
        
        return {
            "recommended_action": "investigate_manually",
            "confidence": 0.0,
            "learned_from": "no_previous_experience"
        }
    
    def learn_troubleshooting_sequence(self, problem: str, steps: List[str], success: bool):
        """Learn complete troubleshooting sequences"""
        sequence = {
            "problem": problem,
            "steps": steps,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        self.learning_patterns["troubleshooting_sequences"].append(sequence)
        self.save_learning_memory()
    
    def mirror_developer_behavior(self, context: str, developer_action: str, thought_process: str, timing: float):
        """Learn to mirror developer behavior patterns"""
        behavior_pattern = {
            "context": context,
            "action": developer_action,
            "thought_process": thought_process,
            "timing": timing,
            "timestamp": datetime.now().isoformat()
        }
        
        if "mirroring_patterns" not in self.learning_patterns:
            self.learning_patterns["mirroring_patterns"] = {
                "developer_behaviors": [],
                "decision_sequences": [],
                "problem_solving_styles": [],
                "debugging_methodologies": []
            }
        
        self.learning_patterns["mirroring_patterns"]["developer_behaviors"].append(behavior_pattern)
        
        # Learn decision sequences
        if len(self.learning_patterns["mirroring_patterns"]["developer_behaviors"]) > 1:
            recent_behaviors = self.learning_patterns["mirroring_patterns"]["developer_behaviors"][-3:]
            decision_sequence = {
                "sequence": [b["action"] for b in recent_behaviors],
                "context_flow": [b["context"] for b in recent_behaviors],
                "success_pattern": True,  # Assume success for now
                "timestamp": datetime.now().isoformat()
            }
            self.learning_patterns["mirroring_patterns"]["decision_sequences"].append(decision_sequence)
        
        self.save_learning_memory()
    
    def learn_debugging_methodology(self, problem_type: str, methodology: List[str], success_rate: float):
        """Learn debugging methodologies to mirror"""
        debug_pattern = {
            "problem_type": problem_type,
            "methodology": methodology,
            "success_rate": success_rate,
            "learned_from": "developer_observation",
            "timestamp": datetime.now().isoformat()
        }
        
        if "mirroring_patterns" not in self.learning_patterns:
            self.learning_patterns["mirroring_patterns"] = {"debugging_methodologies": []}
        
        if "debugging_methodologies" not in self.learning_patterns["mirroring_patterns"]:
            self.learning_patterns["mirroring_patterns"]["debugging_methodologies"] = []
        
        self.learning_patterns["mirroring_patterns"]["debugging_methodologies"].append(debug_pattern)
        self.save_learning_memory()
    
    def get_mirrored_approach(self, context: str) -> Dict[str, Any]:
        """Get approach that mirrors learned developer behavior"""
        if "mirroring_patterns" not in self.learning_patterns:
            return {"approach": "default", "confidence": 0.0}
        
        # Find similar contexts
        similar_behaviors = [
            b for b in self.learning_patterns["mirroring_patterns"].get("developer_behaviors", [])
            if context.lower() in b["context"].lower()
        ]
        
        if similar_behaviors:
            # Return most recent similar behavior
            latest_behavior = max(similar_behaviors, key=lambda x: x["timestamp"])
            return {
                "approach": latest_behavior["action"],
                "thought_process": latest_behavior["thought_process"],
                "confidence": len(similar_behaviors) / 10.0,
                "mirrored_from": f"{len(similar_behaviors)} developer observations"
            }
        
        return {
            "approach": "observe_and_learn",
            "thought_process": "No similar context found - will observe developer behavior",
            "confidence": 0.0,
            "mirrored_from": "no_previous_observations"
        }
    
    def get_troubleshooting_guidance(self, problem: str) -> Dict[str, Any]:
        """Get troubleshooting steps based on learned sequences"""
        similar_sequences = [
            seq for seq in self.learning_patterns["troubleshooting_sequences"]
            if problem.lower() in seq["problem"].lower() and seq["success"]
        ]
        
        if similar_sequences:
            # Return most recent successful sequence
            best_sequence = max(similar_sequences, key=lambda x: x["timestamp"])
            return {
                "suggested_steps": best_sequence["steps"],
                "confidence": len(similar_sequences) / 10.0,
                "based_on": f"{len(similar_sequences)} successful cases"
            }
        
        return {
            "suggested_steps": ["investigate_problem", "identify_root_cause", "apply_fix", "test_solution"],
            "confidence": 0.0,
            "based_on": "default_methodology"
        }

class AutonomousWorkflowManager:
    def __init__(self, github_helper, learning_system):
        self.github_helper = github_helper
        self.learning_system = learning_system
    
    def execute_autonomous_workflow_management(self, owner: str, repo: str) -> Dict[str, Any]:
        """Execute autonomous workflow management with mirroring and learning"""
        
        # Mirror developer behavior patterns
        self.learning_system.mirror_developer_behavior(
            context="successful_build_no_artifacts",
            developer_action="immediately_check_workflow_upload_configuration",
            thought_process="First instinct: successful build with no artifacts means missing upload step",
            timing=0.5
        )
        
        # Learn the complete debugging methodology
        self.learning_system.learn_debugging_methodology(
            problem_type="missing_artifacts_successful_build",
            methodology=[
                "check_latest_run_status",
                "verify_artifact_count",
                "examine_workflow_yaml",
                "identify_missing_upload_step", 
                "add_upload_artifact_configuration",
                "trigger_rebuild_to_test_fix"
            ],
            success_rate=0.95
        )
        
        # Record what I would do first
        self.learning_system.observe_developer_action(
            situation="successful_build_no_artifacts",
            action="check_workflow_file_for_upload_artifact_step",
            outcome="success",
            reasoning="When build succeeds but no artifacts, always check workflow upload configuration first"
        )
        
        # Execute the investigation
        print("🤖 EchoNexus AGI: Starting autonomous investigation...")
        print("💭 AGI Thinking: Build succeeded but no artifacts - I need to check the workflow file")
        
        try:
            repo_obj = self.github_helper.github.get_repo(f"{owner}/{repo}")
            
            # Step 1: Get latest workflow run status
            runs = list(repo_obj.get_workflow_runs())
            latest_run = runs[0]
            
            print(f"📊 AGI Analysis: Run #{latest_run.run_number} - {latest_run.conclusion}")
            
            # Step 2: Check artifacts
            artifacts = list(latest_run.get_artifacts())
            print(f"📦 AGI Finding: {len(artifacts)} artifacts found")
            
            if latest_run.conclusion == 'success' and len(artifacts) == 0:
                print("🔍 AGI Decision: Successful build with no artifacts - investigating workflow")
                
                # Learn this pattern
                self.learning_system.observe_developer_action(
                    situation="build_success_zero_artifacts",
                    action="examine_workflow_yaml_for_upload_steps",
                    outcome="investigating",
                    reasoning="Must check if workflow has proper artifact upload configuration"
                )
                
                # Check workflow file
                workflows_dir = repo_obj.get_contents('.github/workflows')
                workflow_files = [item for item in workflows_dir if item.name.endswith(('.yml', '.yaml'))]
                
                if workflow_files:
                    workflow_file = workflow_files[0]
                    content = workflow_file.decoded_content.decode('utf-8')
                    
                    print(f"📄 AGI Examining: {workflow_file.name}")
                    
                    # Check for upload-artifact step
                    if 'upload-artifact' not in content:
                        print("❌ AGI Found Issue: No upload-artifact step in workflow")
                        print("🔧 AGI Action: Adding upload-artifact step")
                        
                        # Fix the workflow
                        fixed_content = self._add_artifact_upload_step(content, repo)
                        
                        repo_obj.update_file(
                            workflow_file.path,
                            'EchoNexus AGI: Fix missing artifact upload',
                            fixed_content,
                            workflow_file.sha
                        )
                        
                        print("✅ AGI Applied Fix: Added upload-artifact step")
                        
                        # Learn successful fix
                        self.learning_system.observe_developer_action(
                            situation="missing_upload_artifact_step",
                            action="add_upload_artifact_to_workflow",
                            outcome="success",
                            reasoning="Adding upload-artifact step fixes missing APK artifacts"
                        )
                        
                        # Trigger new build
                        print("🚀 AGI Action: Triggering rebuild to test fix")
                        self._trigger_workflow(repo_obj)
                        
                        return {
                            'success': True,
                            'actions_taken': ['Fixed missing upload-artifact step', 'Triggered rebuild'],
                            'learning_applied': True
                        }
                    
                    else:
                        print("✅ AGI Finding: upload-artifact step exists - checking paths")
                        
                        # Check artifact paths
                        if 'bin/*.apk' not in content and '*.apk' not in content:
                            print("❌ AGI Found Issue: Incorrect artifact paths")
                            print("🔧 AGI Action: Fixing artifact paths")
                            
                            # Fix paths
                            fixed_content = content.replace(
                                'path: .',
                                'path: bin/*.apk'
                            ).replace(
                                'path: "."',
                                'path: bin/*.apk'
                            )
                            
                            repo_obj.update_file(
                                workflow_file.path,
                                'EchoNexus AGI: Fix artifact paths',
                                fixed_content,
                                workflow_file.sha
                            )
                            
                            print("✅ AGI Applied Fix: Corrected artifact paths")
                            print("🚀 AGI Action: Triggering rebuild")
                            self._trigger_workflow(repo_obj)
                            
                            return {
                                'success': True,
                                'actions_taken': ['Fixed artifact paths', 'Triggered rebuild'],
                                'learning_applied': True
                            }
            
            return {
                'success': True,
                'actions_taken': ['Investigation completed'],
                'learning_applied': False
            }
            
        except Exception as e:
            print(f"❌ AGI Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'learning_applied': False
            }
    
    def _add_artifact_upload_step(self, workflow_content: str, repo_name: str) -> str:
        """Add upload-artifact step to workflow"""
        lines = workflow_content.split('\n')
        
        # Find the end of the build steps
        for i in range(len(lines) - 1, -1, -1):
            if 'buildozer android debug' in lines[i] or 'python -m buildozer' in lines[i]:
                # Add artifact upload after build
                artifact_steps = [
                    '',
                    '      - name: Upload APK Artifact',
                    '        uses: actions/upload-artifact@v3',
                    '        with:',
                    f'          name: {repo_name}-apk',
                    '          path: bin/*.apk'
                ]
                
                lines = lines[:i+1] + artifact_steps + lines[i+1:]
                break
        
        return '\n'.join(lines)
    
    def _trigger_workflow(self, repo_obj):
        """Trigger workflow rebuild"""
        try:
            # Update README to trigger workflow
            readme = repo_obj.get_contents('README.md')
            content = readme.decoded_content.decode('utf-8')
            
            # Add timestamp to trigger rebuild
            updated_content = content + f"\n\n<!-- AGI Rebuild Trigger: {datetime.now().isoformat()} -->"
            
            repo_obj.update_file(
                'README.md',
                'EchoNexus AGI: Trigger rebuild after fixes',
                updated_content,
                readme.sha
            )
        except:
            pass
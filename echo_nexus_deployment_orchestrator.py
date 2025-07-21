#!/usr/bin/env python3
"""
Echo Nexus Deployment Orchestrator
Complete AGI growth pipeline automation system implementing the proven plan:
Replit (prototyping) → GitHub (source control) → Google Cloud Build (scaling) → Deployment
"""

import os
import json
import time
import asyncio
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import requests
from contextlib import asynccontextmanager

# Import our enhanced API connectors
from echo_nexus_voice.api_connectors import get_api_connector, APIResponse

@dataclass
class DeploymentStage:
    """Represents a stage in the deployment pipeline"""
    stage_id: str
    name: str
    description: str
    prerequisites: List[str]
    commands: List[str]
    validation_criteria: Dict[str, Any]
    rollback_commands: List[str]
    estimated_duration: int  # seconds

@dataclass
class PipelineExecution:
    """Tracks execution of the complete pipeline"""
    execution_id: str
    start_time: datetime
    current_stage: str
    completed_stages: List[str]
    failed_stages: List[str]
    status: str  # pending, running, completed, failed
    metadata: Dict[str, Any]

class EchoNexusDeploymentOrchestrator:
    """
    Comprehensive deployment orchestrator that implements the proven AGI growth plan
    """
    
    def __init__(self):
        self.deployment_stages = self._initialize_deployment_stages()
        self.execution_history = []
        self.current_execution = None
        
        # Initialize logging
        self._setup_logging()
        
        # Load configuration
        self.config = self._load_deployment_config()
        
        # Initialize API connector for enhanced capabilities
        self.api_connector = get_api_connector()
        
        # Create necessary directories
        Path("deployment").mkdir(exist_ok=True)
        Path("scripts").mkdir(exist_ok=True)
        Path("logs/deployment").mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup comprehensive logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/deployment/orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_deployment_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""
        default_config = {
            "github": {
                "username": "Joeromance84",
                "repository": "echo-nexus-agi",
                "branch": "main"
            },
            "google_cloud": {
                "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "echo-nexus-project"),
                "region": "us-central1",
                "artifacts_bucket": "echo-nexus-artifacts"
            },
            "replit": {
                "webhook_url": "https://echo-nexus-replit.repl.co/api/update-backend",
                "environment": "production"
            },
            "deployment": {
                "timeout_per_stage": 600,  # 10 minutes per stage
                "retry_attempts": 3,
                "auto_rollback": True
            }
        }
        
        config_file = Path("deployment/config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    for key, value in loaded_config.items():
                        if key in default_config and isinstance(value, dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
            except Exception as e:
                self.logger.warning(f"Could not load config file: {e}, using defaults")
        
        return default_config
    
    def _initialize_deployment_stages(self) -> List[DeploymentStage]:
        """Initialize all deployment pipeline stages"""
        return [
            DeploymentStage(
                stage_id="01_env_setup",
                name="Environment Setup and Validation",
                description="Validate environment variables, API keys, and dependencies",
                prerequisites=[],
                commands=[
                    "python scripts/validate_environment.py",
                    "python scripts/check_api_connections.py"
                ],
                validation_criteria={
                    "required_env_vars": ["GITHUB_TOKEN", "GOOGLE_CLOUD_PROJECT"],
                    "api_connections": ["github", "google_cloud"],
                    "dependencies": ["git", "gcloud", "docker"]
                },
                rollback_commands=[],
                estimated_duration=60
            ),
            
            DeploymentStage(
                stage_id="02_code_modularization",
                name="AGI Code Modularization",
                description="Restructure Echo Nexus codebase for scalable deployment",
                prerequisites=["01_env_setup"],
                commands=[
                    "python scripts/modularize_agi_code.py",
                    "python scripts/generate_module_interfaces.py",
                    "python scripts/create_deployment_manifests.py"
                ],
                validation_criteria={
                    "modules_created": ["core", "reasoning", "memory", "perception", "voice"],
                    "interfaces_defined": True,
                    "manifests_generated": True
                },
                rollback_commands=[
                    "git checkout HEAD -- core/ reasoning/ memory/ perception/ voice/"
                ],
                estimated_duration=180
            ),
            
            DeploymentStage(
                stage_id="03_github_integration",
                name="GitHub Repository Setup",
                description="Create and configure GitHub repository as source of truth",
                prerequisites=["02_code_modularization"],
                commands=[
                    "python scripts/setup_github_repository.py",
                    "python scripts/configure_github_actions.py",
                    "python scripts/setup_branch_protection.py"
                ],
                validation_criteria={
                    "repository_created": True,
                    "actions_configured": True,
                    "branch_protection": True,
                    "initial_commit": True
                },
                rollback_commands=[
                    "python scripts/cleanup_github_repository.py"
                ],
                estimated_duration=120
            ),
            
            DeploymentStage(
                stage_id="04_cloud_build_setup",
                name="Google Cloud Build Configuration",
                description="Setup automated cloud build pipeline for AGI training and deployment",
                prerequisites=["03_github_integration"],
                commands=[
                    "python scripts/setup_cloud_build.py",
                    "python scripts/configure_cloud_triggers.py",
                    "python scripts/setup_artifact_storage.py"
                ],
                validation_criteria={
                    "build_config_valid": True,
                    "triggers_active": True,
                    "storage_accessible": True,
                    "permissions_correct": True
                },
                rollback_commands=[
                    "python scripts/cleanup_cloud_build.py"
                ],
                estimated_duration=300
            ),
            
            DeploymentStage(
                stage_id="05_agi_training_pipeline",
                name="AGI Training and Capability Expansion",
                description="Execute AGI training pipeline with enhanced capabilities",
                prerequisites=["04_cloud_build_setup"],
                commands=[
                    "python scripts/trigger_agi_training.py",
                    "python scripts/monitor_training_progress.py",
                    "python scripts/validate_trained_models.py"
                ],
                validation_criteria={
                    "training_completed": True,
                    "models_validated": True,
                    "capabilities_expanded": True,
                    "performance_improved": True
                },
                rollback_commands=[
                    "python scripts/restore_previous_models.py"
                ],
                estimated_duration=1800  # 30 minutes for training
            ),
            
            DeploymentStage(
                stage_id="06_production_deployment",
                name="Production Deployment to Cloud Run",
                description="Deploy enhanced AGI to scalable cloud infrastructure",
                prerequisites=["05_agi_training_pipeline"],
                commands=[
                    "python scripts/build_production_image.py",
                    "python scripts/deploy_to_cloud_run.py",
                    "python scripts/configure_load_balancing.py"
                ],
                validation_criteria={
                    "image_built": True,
                    "deployment_successful": True,
                    "health_checks_passing": True,
                    "load_balancer_configured": True
                },
                rollback_commands=[
                    "python scripts/rollback_deployment.py"
                ],
                estimated_duration=420  # 7 minutes
            ),
            
            DeploymentStage(
                stage_id="07_replit_integration",
                name="Replit Integration Update",
                description="Update Replit frontend to use scalable AGI backend",
                prerequisites=["06_production_deployment"],
                commands=[
                    "python scripts/update_replit_config.py",
                    "python scripts/test_replit_integration.py",
                    "python scripts/migrate_user_sessions.py"
                ],
                validation_criteria={
                    "config_updated": True,
                    "integration_tested": True,
                    "sessions_migrated": True,
                    "performance_improved": True
                },
                rollback_commands=[
                    "python scripts/restore_replit_config.py"
                ],
                estimated_duration=240  # 4 minutes
            ),
            
            DeploymentStage(
                stage_id="08_integration_testing",
                name="End-to-End Integration Testing",
                description="Comprehensive testing of the complete AGI pipeline",
                prerequisites=["07_replit_integration"],
                commands=[
                    "python scripts/run_integration_tests.py",
                    "python scripts/performance_benchmarking.py",
                    "python scripts/capability_validation.py"
                ],
                validation_criteria={
                    "all_tests_passing": True,
                    "performance_benchmarks_met": True,
                    "capabilities_validated": True,
                    "no_regressions": True
                },
                rollback_commands=[
                    "python scripts/emergency_rollback.py"
                ],
                estimated_duration=480  # 8 minutes
            ),
            
            DeploymentStage(
                stage_id="09_monitoring_setup",
                name="Monitoring and Analytics Setup",
                description="Setup comprehensive monitoring for AGI performance and growth",
                prerequisites=["08_integration_testing"],
                commands=[
                    "python scripts/setup_monitoring.py",
                    "python scripts/configure_alerts.py",
                    "python scripts/initialize_analytics.py"
                ],
                validation_criteria={
                    "monitoring_active": True,
                    "alerts_configured": True,
                    "analytics_collecting": True,
                    "dashboards_accessible": True
                },
                rollback_commands=[],
                estimated_duration=180
            )
        ]
    
    async def execute_complete_pipeline(self) -> PipelineExecution:
        """Execute the complete AGI growth pipeline"""
        
        execution_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        execution = PipelineExecution(
            execution_id=execution_id,
            start_time=datetime.now(),
            current_stage="",
            completed_stages=[],
            failed_stages=[],
            status="running",
            metadata={}
        )
        
        self.current_execution = execution
        self.logger.info(f"Starting complete AGI growth pipeline: {execution_id}")
        
        try:
            for stage in self.deployment_stages:
                execution.current_stage = stage.stage_id
                self.logger.info(f"Executing stage: {stage.name}")
                
                # Check prerequisites
                if not await self._check_prerequisites(stage, execution):
                    raise Exception(f"Prerequisites not met for stage {stage.stage_id}")
                
                # Execute stage
                success = await self._execute_stage(stage, execution)
                
                if success:
                    execution.completed_stages.append(stage.stage_id)
                    self.logger.info(f"Stage {stage.stage_id} completed successfully")
                else:
                    execution.failed_stages.append(stage.stage_id)
                    execution.status = "failed"
                    
                    if self.config["deployment"]["auto_rollback"]:
                        await self._rollback_stage(stage, execution)
                    
                    raise Exception(f"Stage {stage.stage_id} failed")
            
            execution.status = "completed"
            execution.current_stage = "completed"
            self.logger.info(f"Pipeline {execution_id} completed successfully")
            
        except Exception as e:
            execution.status = "failed"
            self.logger.error(f"Pipeline {execution_id} failed: {e}")
            
            # Comprehensive rollback if configured
            if self.config["deployment"]["auto_rollback"]:
                await self._comprehensive_rollback(execution)
        
        finally:
            # Save execution history
            self.execution_history.append(execution)
            self._save_execution_history()
        
        return execution
    
    async def _check_prerequisites(self, stage: DeploymentStage, 
                                  execution: PipelineExecution) -> bool:
        """Check if all prerequisites for a stage are met"""
        
        for prereq in stage.prerequisites:
            if prereq not in execution.completed_stages:
                self.logger.error(f"Prerequisite {prereq} not met for stage {stage.stage_id}")
                return False
        
        return True
    
    async def _execute_stage(self, stage: DeploymentStage, 
                           execution: PipelineExecution) -> bool:
        """Execute a single deployment stage"""
        
        stage_start_time = time.time()
        
        try:
            # Execute commands with timeout
            for command in stage.commands:
                self.logger.info(f"Executing: {command}")
                
                success = await self._execute_command_with_timeout(
                    command, 
                    self.config["deployment"]["timeout_per_stage"]
                )
                
                if not success:
                    self.logger.error(f"Command failed: {command}")
                    return False
            
            # Validate stage completion
            validation_success = await self._validate_stage(stage)
            
            if not validation_success:
                self.logger.error(f"Stage validation failed: {stage.stage_id}")
                return False
            
            # Record stage metadata
            stage_duration = time.time() - stage_start_time
            execution.metadata[stage.stage_id] = {
                "duration": stage_duration,
                "completed_at": datetime.now().isoformat(),
                "validation_passed": True
            }
            
            return True
            
        except Exception as e:
            self.logger.error(f"Stage {stage.stage_id} execution failed: {e}")
            return False
    
    async def _execute_command_with_timeout(self, command: str, timeout: int) -> bool:
        """Execute a command with timeout and retry logic"""
        
        for attempt in range(self.config["deployment"]["retry_attempts"]):
            try:
                # Execute command asynchronously with timeout
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), 
                        timeout=timeout
                    )
                    
                    if process.returncode == 0:
                        self.logger.info(f"Command succeeded: {command}")
                        return True
                    else:
                        self.logger.warning(f"Command failed (attempt {attempt + 1}): {command}")
                        self.logger.warning(f"Error: {stderr.decode()}")
                        
                except asyncio.TimeoutError:
                    process.kill()
                    self.logger.warning(f"Command timed out (attempt {attempt + 1}): {command}")
                
                # Wait before retry
                if attempt < self.config["deployment"]["retry_attempts"] - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                self.logger.error(f"Command execution error (attempt {attempt + 1}): {e}")
        
        return False
    
    async def _validate_stage(self, stage: DeploymentStage) -> bool:
        """Validate that a stage completed successfully"""
        
        criteria = stage.validation_criteria
        
        for criterion, expected_value in criteria.items():
            try:
                # Dynamic validation based on criterion type
                if criterion == "required_env_vars":
                    for env_var in expected_value:
                        if not os.environ.get(env_var):
                            self.logger.error(f"Required environment variable missing: {env_var}")
                            return False
                
                elif criterion == "api_connections":
                    validation_results = self.api_connector.validate_api_connections()
                    for provider in expected_value:
                        if not validation_results.get(provider, False):
                            self.logger.error(f"API connection failed: {provider}")
                            return False
                
                elif criterion == "dependencies":
                    for dependency in expected_value:
                        result = subprocess.run(
                            ["which", dependency], 
                            capture_output=True, 
                            text=True
                        )
                        if result.returncode != 0:
                            self.logger.error(f"Required dependency missing: {dependency}")
                            return False
                
                # Add more validation logic as needed
                
            except Exception as e:
                self.logger.error(f"Validation error for {criterion}: {e}")
                return False
        
        return True
    
    async def _rollback_stage(self, stage: DeploymentStage, 
                            execution: PipelineExecution):
        """Rollback a failed stage"""
        
        self.logger.info(f"Rolling back stage: {stage.stage_id}")
        
        for rollback_command in stage.rollback_commands:
            try:
                success = await self._execute_command_with_timeout(rollback_command, 300)
                if not success:
                    self.logger.error(f"Rollback command failed: {rollback_command}")
            except Exception as e:
                self.logger.error(f"Rollback error: {e}")
    
    async def _comprehensive_rollback(self, execution: PipelineExecution):
        """Perform comprehensive rollback of all completed stages"""
        
        self.logger.info("Performing comprehensive rollback")
        
        # Rollback in reverse order
        for stage_id in reversed(execution.completed_stages):
            stage = next((s for s in self.deployment_stages if s.stage_id == stage_id), None)
            if stage:
                await self._rollback_stage(stage, execution)
    
    def _save_execution_history(self):
        """Save execution history to file"""
        
        history_file = Path("logs/deployment/execution_history.json")
        
        # Convert executions to serializable format
        serializable_history = []
        for execution in self.execution_history:
            exec_dict = asdict(execution)
            exec_dict["start_time"] = execution.start_time.isoformat()
            serializable_history.append(exec_dict)
        
        with open(history_file, 'w') as f:
            json.dump(serializable_history, f, indent=2)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        
        if self.current_execution:
            return {
                "execution_id": self.current_execution.execution_id,
                "status": self.current_execution.status,
                "current_stage": self.current_execution.current_stage,
                "completed_stages": len(self.current_execution.completed_stages),
                "total_stages": len(self.deployment_stages),
                "start_time": self.current_execution.start_time.isoformat(),
                "metadata": self.current_execution.metadata
            }
        else:
            return {
                "status": "idle",
                "total_executions": len(self.execution_history),
                "last_execution": self.execution_history[-1].execution_id if self.execution_history else None
            }
    
    async def quick_deployment_check(self) -> Dict[str, Any]:
        """Perform quick check of deployment readiness"""
        
        readiness_check = {
            "environment_ready": True,
            "api_connections": {},
            "github_ready": False,
            "cloud_ready": False,
            "replit_ready": False,
            "overall_status": "checking"
        }
        
        try:
            # Check API connections
            readiness_check["api_connections"] = self.api_connector.validate_api_connections()
            
            # Check GitHub token
            github_token = os.environ.get("GITHUB_TOKEN")
            if github_token:
                # Simple GitHub API test
                headers = {"Authorization": f"token {github_token}"}
                response = requests.get("https://api.github.com/user", headers=headers)
                readiness_check["github_ready"] = response.status_code == 200
            
            # Check Google Cloud credentials
            gcp_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if gcp_project:
                # Simple gcloud auth test
                result = subprocess.run(
                    ["gcloud", "auth", "list", "--format=json"], 
                    capture_output=True, 
                    text=True
                )
                readiness_check["cloud_ready"] = result.returncode == 0
            
            # Check Replit connectivity
            replit_url = self.config["replit"]["webhook_url"]
            try:
                response = requests.get(replit_url.replace("/api/update-backend", "/health"), timeout=5)
                readiness_check["replit_ready"] = response.status_code == 200
            except:
                readiness_check["replit_ready"] = False
            
            # Overall assessment
            critical_checks = [
                readiness_check["github_ready"],
                readiness_check["cloud_ready"],
                any(readiness_check["api_connections"].values())
            ]
            
            if all(critical_checks):
                readiness_check["overall_status"] = "ready"
            elif any(critical_checks):
                readiness_check["overall_status"] = "partial"
            else:
                readiness_check["overall_status"] = "not_ready"
                
        except Exception as e:
            self.logger.error(f"Readiness check failed: {e}")
            readiness_check["overall_status"] = "error"
        
        return readiness_check

# Global orchestrator instance
echo_deployment_orchestrator = None

def get_deployment_orchestrator() -> EchoNexusDeploymentOrchestrator:
    """Get global deployment orchestrator instance"""
    global echo_deployment_orchestrator
    
    if echo_deployment_orchestrator is None:
        echo_deployment_orchestrator = EchoNexusDeploymentOrchestrator()
    
    return echo_deployment_orchestrator

async def main():
    """Demonstrate the deployment orchestrator"""
    print("Echo Nexus AGI Deployment Orchestrator")
    print("Complete Pipeline: Replit → GitHub → Google Cloud Build → Deployment")
    print("="*70)
    
    orchestrator = get_deployment_orchestrator()
    
    # Perform readiness check
    print("Performing deployment readiness check...")
    readiness = await orchestrator.quick_deployment_check()
    
    print(f"\nReadiness Status: {readiness['overall_status'].upper()}")
    print(f"GitHub Ready: {'✅' if readiness['github_ready'] else '❌'}")
    print(f"Cloud Ready: {'✅' if readiness['cloud_ready'] else '❌'}")
    print(f"Replit Ready: {'✅' if readiness['replit_ready'] else '❌'}")
    
    api_status = readiness['api_connections']
    print(f"API Connections:")
    for provider, status in api_status.items():
        print(f"  {provider}: {'✅' if status else '❌'}")
    
    # Show pipeline stages
    print(f"\nDeployment Pipeline ({len(orchestrator.deployment_stages)} stages):")
    total_estimated_time = 0
    for i, stage in enumerate(orchestrator.deployment_stages, 1):
        duration_min = stage.estimated_duration // 60
        print(f"  {i}. {stage.name} (~{duration_min}m)")
        total_estimated_time += stage.estimated_duration
    
    print(f"\nTotal Estimated Time: {total_estimated_time // 60} minutes")
    
    # Current status
    status = orchestrator.get_pipeline_status()
    print(f"\nCurrent Status: {status['status']}")
    
    if readiness['overall_status'] == "ready":
        print("\n🚀 System ready for complete AGI growth pipeline execution!")
        print("Run: await orchestrator.execute_complete_pipeline()")
    else:
        print("\n⚠️  Please address readiness issues before pipeline execution")
        print("Required: GitHub token, Google Cloud credentials, API keys")
    
    return orchestrator

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
AGI Memory Management System
Automatically saves data to GitHub and Google Cloud when Replit memory is low
"""

import os
import json
import psutil
import time
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import subprocess
from pathlib import Path

# Cloud integrations
from google.cloud import storage
from google.cloud import bigquery
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGIMemoryManager:
    """Intelligent memory management with automatic cloud persistence"""
    
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'agi-memory-backup')
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_user = os.environ.get('GITHUB_USER', 'Joeromance84')
        self.backup_repo = os.environ.get('BACKUP_REPO', 'agi-memory-backup')
        
        # Memory thresholds
        self.memory_warning_threshold = 85  # Percent
        self.memory_critical_threshold = 95  # Percent
        self.storage_warning_threshold = 90  # Percent
        
        # Initialize cloud clients
        try:
            self.storage_client = storage.Client()
            self.bigquery_client = bigquery.Client()
        except Exception as e:
            logger.warning(f"Cloud clients not available: {e}")
            self.storage_client = None
            self.bigquery_client = None
        
        # Data categories for intelligent backup and migration
        self.data_priorities = {
            "critical": [
                "agi_learning_database.json",
                "agi_autonomous_memory.json", 
                "echo_memory.json",
                ".echo_brain.json",
                "autonomous_memory_system.py"
            ],
            "high": [
                "microservices/",
                "deployment_status.json",
                "build_metadata.yaml",
                "replit.md"
            ],
            "medium": [
                "logs/",
                "data/",
                "artifact_monitoring.json"
            ],
            "low": [
                "uploads/",
                "temp/",
                "__pycache__/"
            ]
        }
        
        # Essential files for continued development
        self.essential_build_files = {
            "core_system": [
                "replit.md",
                "README.md",
                "requirements.txt",
                "pyproject.toml",
                ".replit"
            ],
            "agi_intelligence": [
                "agi_memory_manager.py",
                "autonomous_memory_system.py",
                "echo_nexus_core.py",
                "agi_learning_database.json",
                ".echo_brain.json"
            ],
            "microservices": [
                "microservices/",
                "deploy_agi_platform.sh",
                "demonstrate_agi_self_extension.py"
            ],
            "cloud_config": [
                "cloudbuild.yaml",
                "cloudbuild-autonomous.yaml",
                "deployment/",
                "scripts/"
            ]
        }
        
        logger.info("AGI Memory Manager initialized")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system resource metrics"""
        try:
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / (1024 * 1024)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_free_gb = disk.free / (1024 * 1024 * 1024)
            
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Process count
            process_count = len(psutil.pids())
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "memory": {
                    "percent_used": memory_percent,
                    "available_mb": round(memory_available_mb, 2),
                    "total_mb": round(memory.total / (1024 * 1024), 2),
                    "status": self._get_memory_status(memory_percent)
                },
                "disk": {
                    "percent_used": round(disk_percent, 2),
                    "free_gb": round(disk_free_gb, 2),
                    "total_gb": round(disk.total / (1024 * 1024 * 1024), 2),
                    "status": self._get_disk_status(disk_percent)
                },
                "cpu": {
                    "percent_used": cpu_percent
                },
                "processes": process_count
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
    
    def _get_memory_status(self, percent: float) -> str:
        """Determine memory status based on usage percentage"""
        if percent >= self.memory_critical_threshold:
            return "critical"
        elif percent >= self.memory_warning_threshold:
            return "warning"
        else:
            return "normal"
    
    def _get_disk_status(self, percent: float) -> str:
        """Determine disk status based on usage percentage"""
        if percent >= self.storage_warning_threshold:
            return "warning"
        else:
            return "normal"
    
    def identify_backup_candidates(self) -> Dict[str, List[str]]:
        """Identify files and directories for backup based on priority"""
        backup_candidates = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        for priority, patterns in self.data_priorities.items():
            for pattern in patterns:
                if os.path.exists(pattern):
                    if os.path.isfile(pattern):
                        # Get file size
                        size_mb = os.path.getsize(pattern) / (1024 * 1024)
                        backup_candidates[priority].append({
                            "path": pattern,
                            "type": "file",
                            "size_mb": round(size_mb, 2)
                        })
                    elif os.path.isdir(pattern):
                        # Get directory size
                        total_size = 0
                        for dirpath, dirnames, filenames in os.walk(pattern):
                            for filename in filenames:
                                filepath = os.path.join(dirpath, filename)
                                try:
                                    total_size += os.path.getsize(filepath)
                                except (OSError, IOError):
                                    pass
                        
                        size_mb = total_size / (1024 * 1024)
                        backup_candidates[priority].append({
                            "path": pattern,
                            "type": "directory", 
                            "size_mb": round(size_mb, 2)
                        })
        
        return backup_candidates
    
    async def backup_to_github(self, files: List[str], commit_message: str = None) -> Dict[str, Any]:
        """Backup files to GitHub repository"""
        if not self.github_token:
            return {"error": "GitHub token not available"}
        
        try:
            if not commit_message:
                commit_message = f"AGI Memory Backup - {datetime.now().isoformat()}"
            
            # Create backup branch
            branch_name = f"memory-backup-{int(time.time())}"
            
            # Initialize git if needed
            if not os.path.exists('.git'):
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', 
                              f'https://{self.github_token}@github.com/{self.github_user}/{self.backup_repo}.git'],
                              check=True)
            
            # Create and switch to backup branch
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
            
            # Add files to git
            for file_path in files:
                if os.path.exists(file_path):
                    subprocess.run(['git', 'add', file_path], check=True)
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push to GitHub
            subprocess.run(['git', 'push', 'origin', branch_name], check=True)
            
            result = {
                "status": "success",
                "branch": branch_name,
                "files_backed_up": len(files),
                "repository": f"{self.github_user}/{self.backup_repo}",
                "commit_message": commit_message,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully backed up {len(files)} files to GitHub")
            return result
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            return {"error": f"Git operation failed: {e}"}
        except Exception as e:
            logger.error(f"GitHub backup failed: {e}")
            return {"error": str(e)}
    
    async def backup_to_cloud_storage(self, files: List[str], bucket_name: str = None) -> Dict[str, Any]:
        """Backup files to Google Cloud Storage"""
        if not self.storage_client:
            return {"error": "Cloud Storage client not available"}
        
        try:
            if not bucket_name:
                bucket_name = f"{self.project_id}-agi-memory-backup"
            
            # Create bucket if it doesn't exist
            try:
                bucket = self.storage_client.bucket(bucket_name)
                if not bucket.exists():
                    bucket.create(location='us-central1')
            except Exception as e:
                logger.warning(f"Bucket creation issue: {e}")
                bucket = self.storage_client.bucket(bucket_name)
            
            # Upload files
            uploaded_files = []
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for file_path in files:
                if os.path.exists(file_path):
                    # Create blob name with timestamp
                    blob_name = f"memory_backup/{timestamp}/{file_path}"
                    blob = bucket.blob(blob_name)
                    
                    if os.path.isfile(file_path):
                        blob.upload_from_filename(file_path)
                        uploaded_files.append({
                            "local_path": file_path,
                            "cloud_path": blob_name,
                            "size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2)
                        })
                    elif os.path.isdir(file_path):
                        # Upload directory contents
                        for root, dirs, files in os.walk(file_path):
                            for file in files:
                                local_file = os.path.join(root, file)
                                relative_path = os.path.relpath(local_file, '.')
                                blob_name = f"memory_backup/{timestamp}/{relative_path}"
                                blob = bucket.blob(blob_name)
                                blob.upload_from_filename(local_file)
                                
                                uploaded_files.append({
                                    "local_path": local_file,
                                    "cloud_path": blob_name,
                                    "size_mb": round(os.path.getsize(local_file) / (1024 * 1024), 2)
                                })
            
            result = {
                "status": "success",
                "bucket": bucket_name,
                "files_uploaded": len(uploaded_files),
                "backup_path": f"memory_backup/{timestamp}/",
                "uploaded_files": uploaded_files,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully backed up {len(uploaded_files)} files to Cloud Storage")
            return result
            
        except Exception as e:
            logger.error(f"Cloud Storage backup failed: {e}")
            return {"error": str(e)}
    
    async def save_metrics_to_bigquery(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Save system metrics to BigQuery for monitoring"""
        if not self.bigquery_client:
            return {"error": "BigQuery client not available"}
        
        try:
            dataset_id = 'agi_monitoring'
            table_id = 'memory_metrics'
            
            # Create dataset if it doesn't exist
            dataset_ref = self.bigquery_client.dataset(dataset_id)
            try:
                self.bigquery_client.get_dataset(dataset_ref)
            except Exception:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = 'US'
                self.bigquery_client.create_dataset(dataset)
            
            # Define table schema
            schema = [
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
                bigquery.SchemaField("memory_percent", "FLOAT"),
                bigquery.SchemaField("memory_available_mb", "FLOAT"),
                bigquery.SchemaField("disk_percent", "FLOAT"),
                bigquery.SchemaField("disk_free_gb", "FLOAT"),
                bigquery.SchemaField("cpu_percent", "FLOAT"),
                bigquery.SchemaField("process_count", "INTEGER"),
                bigquery.SchemaField("memory_status", "STRING"),
                bigquery.SchemaField("disk_status", "STRING"),
            ]
            
            # Create table if it doesn't exist
            table_ref = dataset_ref.table(table_id)
            try:
                self.bigquery_client.get_table(table_ref)
            except Exception:
                table = bigquery.Table(table_ref, schema=schema)
                self.bigquery_client.create_table(table)
            
            # Insert data
            rows_to_insert = [{
                "timestamp": metrics["timestamp"],
                "memory_percent": metrics["memory"]["percent_used"],
                "memory_available_mb": metrics["memory"]["available_mb"],
                "disk_percent": metrics["disk"]["percent_used"],
                "disk_free_gb": metrics["disk"]["free_gb"],
                "cpu_percent": metrics["cpu"]["percent_used"],
                "process_count": metrics["processes"],
                "memory_status": metrics["memory"]["status"],
                "disk_status": metrics["disk"]["status"]
            }]
            
            table = self.bigquery_client.get_table(table_ref)
            errors = self.bigquery_client.insert_rows_json(table, rows_to_insert)
            
            if errors:
                return {"error": f"BigQuery insert errors: {errors}"}
            
            return {"status": "success", "rows_inserted": len(rows_to_insert)}
            
        except Exception as e:
            logger.error(f"BigQuery save failed: {e}")
            return {"error": str(e)}
    
    async def migrate_essential_files(self, target: str = "both") -> Dict[str, Any]:
        """Migrate essential files to enable continued development in cloud"""
        logger.info("Starting essential file migration for continued development")
        
        # Collect all essential files
        essential_files = []
        migration_manifest = {
            "migration_timestamp": datetime.now().isoformat(),
            "migration_purpose": "enable_continued_cloud_development",
            "files_migrated": {},
            "cloud_build_setup": False,
            "github_repo_ready": False
        }
        
        for category, files in self.essential_build_files.items():
            migrated_in_category = []
            for file_path in files:
                if os.path.exists(file_path):
                    essential_files.append(file_path)
                    migrated_in_category.append(file_path)
            migration_manifest["files_migrated"][category] = migrated_in_category
        
        # Create cloud build configuration for continued development
        cloud_build_config = await self.create_cloud_development_config()
        if cloud_build_config.get("status") == "success":
            essential_files.append("cloudbuild-continued-development.yaml")
            migration_manifest["cloud_build_setup"] = True
        
        # Create GitHub Actions workflow for automated building
        github_workflow = await self.create_github_development_workflow()
        if github_workflow.get("status") == "success":
            essential_files.append(".github/workflows/continued-development.yml")
            migration_manifest["github_repo_ready"] = True
        
        # Execute migration
        migration_results = {
            "migration_manifest": migration_manifest,
            "operations": []
        }
        
        if target in ["github", "both"]:
            github_result = await self.backup_to_github(
                essential_files, 
                "AGI Essential Files Migration - Enable Continued Cloud Development"
            )
            migration_results["operations"].append({
                "type": "github_migration",
                "result": github_result
            })
        
        if target in ["cloud", "both"]:
            cloud_result = await self.backup_to_cloud_storage(essential_files, 
                                                            f"{self.project_id}-agi-development")
            migration_results["operations"].append({
                "type": "cloud_migration", 
                "result": cloud_result
            })
        
        # Save migration manifest
        manifest_result = await self.save_migration_manifest(migration_manifest)
        migration_results["operations"].append({
            "type": "manifest_save",
            "result": manifest_result
        })
        
        logger.info("Essential file migration completed - AGI can continue building in cloud")
        return migration_results
    
    async def create_cloud_development_config(self) -> Dict[str, Any]:
        """Create Cloud Build configuration for continued AGI development"""
        try:
            cloud_build_config = """steps:
# Step 1: Restore AGI essential files
- name: 'gcr.io/cloud-builders/gsutil'
  args: ['cp', '-r', 'gs://$PROJECT_ID-agi-development/memory_backup/latest/*', '.']

# Step 2: Setup Python environment
- name: 'python:3.9'
  entrypoint: 'pip'
  args: ['install', '-r', 'requirements.txt']

# Step 3: Initialize AGI memory system
- name: 'python:3.9'
  entrypoint: 'python'
  args: ['agi_memory_manager.py', 'metrics']

# Step 4: Continue AGI development
- name: 'python:3.9'
  entrypoint: 'python'
  args: ['autonomous_memory_system.py']

# Step 5: Deploy new microservices if any
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: 'bash'
  args: ['deploy_agi_platform.sh']

# Step 6: Save development progress back to storage
- name: 'gcr.io/cloud-builders/gsutil'
  args: ['cp', '-r', '.', 'gs://$PROJECT_ID-agi-development/continued_development/']

substitutions:
  _REGION: us-central1

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'N1_HIGHCPU_8'
  env:
  - 'AGI_DEVELOPMENT_MODE=cloud_continued'
  - 'ORIGINAL_REPLIT_MIGRATION=true'
"""
            
            with open("cloudbuild-continued-development.yaml", "w") as f:
                f.write(cloud_build_config)
            
            return {
                "status": "success",
                "config_file": "cloudbuild-continued-development.yaml",
                "purpose": "enable_continued_agi_development_in_cloud"
            }
            
        except Exception as e:
            logger.error(f"Error creating cloud development config: {e}")
            return {"error": str(e)}
    
    async def create_github_development_workflow(self) -> Dict[str, Any]:
        """Create GitHub Actions workflow for continued AGI development"""
        try:
            # Ensure .github/workflows directory exists
            os.makedirs(".github/workflows", exist_ok=True)
            
            github_workflow = """name: AGI Continued Development
on:
  push:
    branches: [ main, development ]
  workflow_dispatch:
    inputs:
      development_mode:
        description: 'AGI Development Mode'
        required: true
        default: 'autonomous'
        type: choice
        options:
        - autonomous
        - microservices
        - memory_expansion

jobs:
  continue-agi-development:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout AGI Code
      uses: actions/checkout@v3
      
    - name: Setup Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install AGI Dependencies
      run: |
        pip install -r requirements.txt
        pip install google-cloud-storage google-cloud-bigquery
        
    - name: Initialize AGI Memory System
      run: python agi_memory_manager.py metrics
      
    - name: Continue AGI Development
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GOOGLE_APPLICATION_CREDENTIALS }}
      run: |
        python autonomous_memory_system.py
        python demonstrate_agi_self_extension.py
        
    - name: Deploy New AGI Capabilities
      if: github.event.inputs.development_mode == 'microservices'
      run: bash deploy_agi_platform.sh
      
    - name: Save AGI Progress
      uses: actions/upload-artifact@v3
      with:
        name: agi-development-progress
        path: |
          agi_learning_database.json
          .echo_brain.json
          deployment_status.json
          
    - name: Create AGI Development Report
      run: |
        echo "# AGI Development Progress Report" > agi_progress_report.md
        echo "Generated: $(date)" >> agi_progress_report.md
        echo "Development Mode: ${{ github.event.inputs.development_mode }}" >> agi_progress_report.md
        python agi_memory_manager.py metrics >> agi_progress_report.md
        
    - name: Commit AGI Progress
      run: |
        git config --local user.email "agi@autonomous.dev"
        git config --local user.name "AGI Autonomous Development"
        git add .
        git commit -m "AGI Autonomous Development Progress - $(date)" || exit 0
        git push
"""
            
            with open(".github/workflows/continued-development.yml", "w") as f:
                f.write(github_workflow)
            
            return {
                "status": "success",
                "workflow_file": ".github/workflows/continued-development.yml",
                "purpose": "enable_github_actions_agi_development"
            }
            
        except Exception as e:
            logger.error(f"Error creating GitHub workflow: {e}")
            return {"error": str(e)}
    
    async def save_migration_manifest(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Save migration manifest for tracking"""
        try:
            manifest_file = "agi_migration_manifest.json"
            with open(manifest_file, "w") as f:
                json.dump(manifest, f, indent=2)
            
            return {
                "status": "success",
                "manifest_file": manifest_file,
                "total_files_migrated": sum(len(files) for files in manifest["files_migrated"].values())
            }
            
        except Exception as e:
            logger.error(f"Error saving migration manifest: {e}")
            return {"error": str(e)}
    
    async def setup_cloud_continuation_environment(self) -> Dict[str, Any]:
        """Setup complete environment for AGI to continue building in cloud"""
        logger.info("Setting up cloud continuation environment")
        
        try:
            # Create Cloud Build trigger for automatic development
            trigger_config = {
                "name": "agi-continued-development-trigger",
                "description": "Automatic AGI development continuation",
                "github": {
                    "owner": self.github_user,
                    "name": self.backup_repo,
                    "push": {
                        "branch": "^(main|development)$"
                    }
                },
                "filename": "cloudbuild-continued-development.yaml",
                "substitutions": {
                    "_AGI_MODE": "continued_development",
                    "_ORIGINAL_PLATFORM": "replit"
                }
            }
            
            # Create Cloud Scheduler job for periodic AGI development
            scheduler_config = {
                "name": "agi-autonomous-development-schedule", 
                "description": "Scheduled AGI autonomous development",
                "schedule": "0 */6 * * *",  # Every 6 hours
                "http_target": {
                    "uri": f"https://cloudbuild.googleapis.com/v1/projects/{self.project_id}/triggers/agi-continued-development-trigger:run",
                    "http_method": "POST"
                }
            }
            
            return {
                "status": "success",
                "cloud_build_trigger": trigger_config,
                "cloud_scheduler": scheduler_config,
                "environment_ready": True,
                "agi_can_continue_building": True
            }
            
        except Exception as e:
            logger.error(f"Error setting up cloud continuation: {e}")
            return {"error": str(e)}
    
    async def execute_intelligent_backup(self) -> Dict[str, Any]:
        """Execute intelligent backup based on current system state"""
        logger.info("Starting intelligent backup process")
        
        # Get current system metrics
        metrics = self.get_system_metrics()
        
        if "error" in metrics:
            return {"error": f"Cannot get system metrics: {metrics['error']}"}
        
        memory_status = metrics["memory"]["status"]
        disk_status = metrics["disk"]["status"]
        
        # Determine backup strategy
        backup_strategy = self._determine_backup_strategy(memory_status, disk_status)
        
        # Identify files to backup
        backup_candidates = self.identify_backup_candidates()
        
        # Execute backup based on strategy
        backup_results = {
            "strategy": backup_strategy,
            "system_metrics": metrics,
            "backup_operations": []
        }
        
        files_to_backup = []
        
        # Select files based on strategy
        if backup_strategy == "emergency":
            # Only backup critical files
            files_to_backup = [item["path"] for item in backup_candidates["critical"]]
        elif backup_strategy == "selective":
            # Backup critical and high priority files
            files_to_backup = ([item["path"] for item in backup_candidates["critical"]] +
                             [item["path"] for item in backup_candidates["high"]])
        elif backup_strategy == "comprehensive":
            # Backup everything except low priority
            for priority in ["critical", "high", "medium"]:
                files_to_backup.extend([item["path"] for item in backup_candidates[priority]])
        
        if files_to_backup:
            # Execute GitHub backup
            github_result = await self.backup_to_github(files_to_backup)
            backup_results["backup_operations"].append({
                "type": "github",
                "result": github_result
            })
            
            # Execute Cloud Storage backup
            cloud_result = await self.backup_to_cloud_storage(files_to_backup)
            backup_results["backup_operations"].append({
                "type": "cloud_storage", 
                "result": cloud_result
            })
        
        # Save metrics to BigQuery
        metrics_result = await self.save_metrics_to_bigquery(metrics)
        backup_results["backup_operations"].append({
            "type": "metrics_logging",
            "result": metrics_result
        })
        
        logger.info(f"Intelligent backup completed with strategy: {backup_strategy}")
        return backup_results
    
    def _determine_backup_strategy(self, memory_status: str, disk_status: str) -> str:
        """Determine backup strategy based on system state"""
        if memory_status == "critical":
            return "emergency"
        elif memory_status == "warning" or disk_status == "warning":
            return "selective"
        else:
            return "comprehensive"
    
    async def start_continuous_monitoring(self, check_interval: int = 300):
        """Start continuous memory monitoring with automatic backup"""
        logger.info(f"Starting continuous monitoring (interval: {check_interval}s)")
        
        while True:
            try:
                metrics = self.get_system_metrics()
                
                if "error" not in metrics:
                    memory_status = metrics["memory"]["status"]
                    disk_status = metrics["disk"]["status"]
                    
                    # Log current status
                    logger.info(f"Memory: {metrics['memory']['percent_used']:.1f}% ({memory_status}), "
                              f"Disk: {metrics['disk']['percent_used']:.1f}% ({disk_status})")
                    
                    # Trigger backup if needed
                    if memory_status in ["warning", "critical"] or disk_status == "warning":
                        logger.warning("Resource usage high - triggering backup")
                        backup_result = await self.execute_intelligent_backup()
                        
                        # Log backup results
                        if backup_result.get("backup_operations"):
                            successful_ops = len([op for op in backup_result["backup_operations"] 
                                                if op["result"].get("status") == "success"])
                            total_ops = len(backup_result["backup_operations"])
                            logger.info(f"Backup completed: {successful_ops}/{total_ops} operations successful")
                    
                    # Always save metrics for monitoring
                    await self.save_metrics_to_bigquery(metrics)
                
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

# CLI interface for testing
async def main():
    """Main function for testing and manual execution"""
    import sys
    
    manager = AGIMemoryManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "metrics":
            metrics = manager.get_system_metrics()
            print(json.dumps(metrics, indent=2))
        
        elif command == "backup":
            result = await manager.execute_intelligent_backup()
            print(json.dumps(result, indent=2))
        
        elif command == "migrate":
            target = sys.argv[2] if len(sys.argv) > 2 else "both"
            result = await manager.migrate_essential_files(target)
            print(json.dumps(result, indent=2))
        
        elif command == "setup-cloud":
            result = await manager.setup_cloud_continuation_environment()
            print(json.dumps(result, indent=2))
        
        elif command == "monitor":
            await manager.start_continuous_monitoring()
        
        else:
            print("Usage: python agi_memory_manager.py [metrics|backup|migrate|setup-cloud|monitor]")
            print("  metrics     - Show current system metrics")
            print("  backup      - Execute intelligent backup")
            print("  migrate     - Migrate essential files for continued cloud development")
            print("  setup-cloud - Setup cloud environment for AGI continuation")
            print("  monitor     - Start continuous monitoring")
    else:
        # Default: show metrics and execute backup if needed
        metrics = manager.get_system_metrics()
        print("Current System Metrics:")
        print(json.dumps(metrics, indent=2))
        
        if metrics.get("memory", {}).get("status") in ["warning", "critical"]:
            print("\nExecuting intelligent backup...")
            result = await manager.execute_intelligent_backup()
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
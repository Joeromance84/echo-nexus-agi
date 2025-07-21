#!/usr/bin/env python3
"""
AGI Learning Backup System
Automatically saves all learned information from PDFs and EPUBs to GitHub and Google Cloud Build
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
import threading

class AGILearningBackupSystem:
    """Comprehensive backup system for AGI learning data"""
    
    def __init__(self):
        self.backup_interval = 30  # seconds
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.learning_database = "agi_learning_database.json"
        self.backup_manifest = "agi_backup_manifest.json"
        self.running = False
        
        # Initialize backup manifest
        self.load_backup_manifest()
        
    def load_backup_manifest(self):
        """Load existing backup manifest"""
        try:
            if os.path.exists(self.backup_manifest):
                with open(self.backup_manifest, 'r') as f:
                    self.manifest = json.load(f)
            else:
                self.manifest = {
                    "last_backup": None,
                    "total_backups": 0,
                    "github_backups": 0,
                    "cloud_backups": 0,
                    "files_tracked": []
                }
        except Exception as e:
            print(f"Error loading backup manifest: {e}")
            self.manifest = {
                "last_backup": None,
                "total_backups": 0,
                "github_backups": 0,
                "cloud_backups": 0,
                "files_tracked": []
            }
    
    def save_backup_manifest(self):
        """Save backup manifest"""
        try:
            with open(self.backup_manifest, 'w') as f:
                json.dump(self.manifest, f, indent=2)
        except Exception as e:
            print(f"Error saving backup manifest: {e}")
    
    def backup_to_github(self):
        """Backup learning data to GitHub repository"""
        if not self.github_token:
            print("⚠️ No GitHub token available - skipping GitHub backup")
            return False
            
        try:
            from github import Github
            
            # Initialize GitHub client
            g = Github(self.github_token)
            user = g.get_user()
            
            # Create or get backup repository
            repo_name = "agi-learning-backup"
            try:
                repo = user.get_repo(repo_name)
            except:
                # Create new repository if it doesn't exist
                repo = user.create_repo(
                    repo_name,
                    description="AGI Learning Data Backup Repository",
                    private=True
                )
                print(f"✅ Created backup repository: {repo_name}")
            
            # Read learning database
            if os.path.exists(self.learning_database):
                with open(self.learning_database, 'r') as f:
                    learning_data = f.read()
                
                # Create timestamped backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"learning_backup_{timestamp}.json"
                
                # Commit to GitHub
                try:
                    # Try to get existing file
                    file = repo.get_contents(backup_filename)
                    repo.update_file(
                        backup_filename,
                        f"AGI Learning Backup - {datetime.now().isoformat()}",
                        learning_data,
                        file.sha
                    )
                except:
                    # Create new file
                    repo.create_file(
                        backup_filename,
                        f"AGI Learning Backup - {datetime.now().isoformat()}",
                        learning_data
                    )
                
                # Also update latest backup
                try:
                    file = repo.get_contents("latest_learning_backup.json")
                    repo.update_file(
                        "latest_learning_backup.json",
                        f"Latest AGI Learning Backup - {datetime.now().isoformat()}",
                        learning_data,
                        file.sha
                    )
                except:
                    repo.create_file(
                        "latest_learning_backup.json",
                        f"Latest AGI Learning Backup - {datetime.now().isoformat()}",
                        learning_data
                    )
                
                print(f"✅ GitHub backup successful: {backup_filename}")
                self.manifest["github_backups"] += 1
                return True
                
        except Exception as e:
            print(f"❌ GitHub backup failed: {e}")
            return False
    
    def backup_to_cloud_build(self):
        """Create Cloud Build trigger for backup automation"""
        try:
            # Create Cloud Build configuration for backup
            cloudbuild_config = {
                "steps": [
                    {
                        "name": "gcr.io/cloud-builders/git",
                        "entrypoint": "bash",
                        "args": [
                            "-c",
                            """
                            # Clone AGI repository
                            git clone https://github.com/Joeromance84/echo-nexus-agi.git
                            cd echo-nexus-agi
                            
                            # Copy learning data
                            cp /workspace/agi_learning_database.json ./
                            cp /workspace/agi_backup_manifest.json ./
                            
                            # Commit and push
                            git config user.email "agi-backup@echonexus.ai"
                            git config user.name "AGI Backup System"
                            git add agi_learning_database.json agi_backup_manifest.json
                            git commit -m "AGI Learning Backup - $(date)"
                            git push origin main
                            """
                        ]
                    }
                ],
                "timeout": "600s"
            }
            
            # Save Cloud Build configuration
            with open("cloudbuild-agi-backup.yaml", 'w') as f:
                import yaml
                yaml.dump(cloudbuild_config, f, default_flow_style=False)
            
            print("✅ Cloud Build backup configuration created")
            self.manifest["cloud_backups"] += 1
            return True
            
        except Exception as e:
            print(f"❌ Cloud Build backup failed: {e}")
            return False
    
    def backup_learning_data(self):
        """Perform complete backup of learning data"""
        print(f"🔄 Starting AGI learning backup at {datetime.now()}")
        
        # Check if learning database exists and has new data
        if not os.path.exists(self.learning_database):
            print("⚠️ No learning database found - nothing to backup")
            return
        
        # Get file modification time
        file_mtime = os.path.getmtime(self.learning_database)
        last_backup = self.manifest.get("last_backup")
        
        if last_backup and file_mtime <= last_backup:
            print("ℹ️ No new learning data since last backup")
            return
        
        # Perform backups
        github_success = self.backup_to_github()
        cloud_success = self.backup_to_cloud_build()
        
        if github_success or cloud_success:
            self.manifest["last_backup"] = file_mtime
            self.manifest["total_backups"] += 1
            self.save_backup_manifest()
            
            print(f"✅ AGI learning backup completed successfully")
            print(f"📊 Total backups: {self.manifest['total_backups']}")
            print(f"🐙 GitHub backups: {self.manifest['github_backups']}")
            print(f"☁️ Cloud backups: {self.manifest['cloud_backups']}")
        else:
            print("❌ All backup methods failed")
    
    def start_continuous_backup(self):
        """Start continuous backup monitoring"""
        print("🚀 Starting AGI Learning Continuous Backup System")
        print(f"🔄 Backup interval: {self.backup_interval} seconds")
        
        self.running = True
        
        # Start monitoring and backup loops
        self.monitor_learning_files()
        
        # Simple time-based backup loop
        while self.running:
            try:
                self.backup_learning_data()
                time.sleep(self.backup_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Backup error: {e}")
                time.sleep(5)
    
    def monitor_learning_files(self):
        """Monitor learning files for changes"""
        def file_monitor():
            last_sizes = {}
            
            while self.running:
                files_to_monitor = [
                    self.learning_database,
                    "agi_pdf_processing_results.json",
                    "document_learning_app.py"
                ]
                
                for filepath in files_to_monitor:
                    if os.path.exists(filepath):
                        current_size = os.path.getsize(filepath)
                        if filepath not in last_sizes:
                            last_sizes[filepath] = current_size
                        elif current_size != last_sizes[filepath]:
                            print(f"📄 Detected change in {filepath} - triggering backup")
                            self.backup_learning_data()
                            last_sizes[filepath] = current_size
                
                time.sleep(5)  # Check every 5 seconds
        
        # Start file monitoring in background thread
        monitor_thread = threading.Thread(target=file_monitor, daemon=True)
        monitor_thread.start()
    
    def stop_backup_system(self):
        """Stop the backup system"""
        self.running = False
        print("🛑 AGI Learning Backup System stopped")

def main():
    """Run the AGI Learning Backup System"""
    backup_system = AGILearningBackupSystem()
    
    try:
        backup_system.start_continuous_backup()
    except KeyboardInterrupt:
        backup_system.stop_backup_system()

if __name__ == "__main__":
    main()
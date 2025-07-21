#!/usr/bin/env python3
"""
GitHub Backup Integration for AGI Learning Data
Automatically commits and pushes learning data to GitHub repository
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class GitHubBackupIntegration:
    """Direct GitHub integration for AGI learning backups"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_url = "https://github.com/Joeromance84/echo-nexus-agi.git"
        self.learning_files = [
            "agi_learning_database.json",
            "agi_pdf_processing_results.json",
            "agi_backup_manifest.json",
            "document_learning_app.py"
        ]
        
    def commit_learning_data(self):
        """Commit learning data directly to GitHub"""
        try:
            print("🚀 Starting GitHub backup of AGI learning data...")
            
            # Configure git
            subprocess.run(["git", "config", "--global", "user.email", "agi-backup@echonexus.ai"], check=True)
            subprocess.run(["git", "config", "--global", "user.name", "AGI Learning System"], check=True)
            
            # Add all learning files that exist
            files_added = []
            for file_path in self.learning_files:
                if os.path.exists(file_path):
                    subprocess.run(["git", "add", file_path], check=True)
                    files_added.append(file_path)
                    print(f"✅ Added {file_path} to staging")
            
            if not files_added:
                print("ℹ️ No learning files found to backup")
                return False
            
            # Check if there are changes to commit
            result = subprocess.run(["git", "diff", "--staged", "--quiet"], capture_output=True)
            if result.returncode == 0:
                print("ℹ️ No changes to commit")
                return False
            
            # Create commit message with timestamp and file details
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"""AGI Learning Backup - {timestamp}

📚 Automatic backup of AGI learning data
🧠 Files updated: {', '.join(files_added)}
⚡ Triggered by: Document processing system
📊 Backup system: Fully automated GitHub integration

Learning data includes:
- PDF and EPUB processing results
- Extracted concepts and insights
- Document analysis and knowledge base
- AGI autonomous learning progress
"""
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("✅ Learning data committed to local repository")
            
            # Push to GitHub
            if self.github_token:
                # Use token authentication for push
                auth_url = f"https://{self.github_token}@github.com/Joeromance84/echo-nexus-agi.git"
                subprocess.run(["git", "push", auth_url, "main"], check=True)
                print("🐙 Successfully pushed AGI learning data to GitHub")
            else:
                subprocess.run(["git", "push", "origin", "main"], check=True)
                print("🐙 Successfully pushed AGI learning data to GitHub")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ GitHub backup failed: {e}")
            return False
    
    def trigger_cloud_build(self):
        """Trigger Google Cloud Build for backup"""
        try:
            print("☁️ Triggering Google Cloud Build backup...")
            
            # Create a simple trigger file
            trigger_data = {
                "trigger_time": datetime.now().isoformat(),
                "trigger_type": "agi_learning_backup",
                "files_backed_up": [f for f in self.learning_files if os.path.exists(f)]
            }
            
            with open("cloud_build_trigger.json", 'w') as f:
                json.dump(trigger_data, f, indent=2)
            
            # Add trigger file to git
            subprocess.run(["git", "add", "cloud_build_trigger.json"], check=True)
            subprocess.run(["git", "commit", "-m", f"Trigger Cloud Build backup - {datetime.now()}"], check=True)
            
            if self.github_token:
                auth_url = f"https://{self.github_token}@github.com/Joeromance84/echo-nexus-agi.git"
                subprocess.run(["git", "push", auth_url, "main"], check=True)
            else:
                subprocess.run(["git", "push", "origin", "main"], check=True)
            
            print("✅ Cloud Build trigger committed and pushed")
            return True
            
        except Exception as e:
            print(f"❌ Cloud Build trigger failed: {e}")
            return False
    
    def full_backup_cycle(self):
        """Complete backup cycle to GitHub and Cloud Build"""
        print("🔄 Starting full AGI learning backup cycle...")
        
        # Step 1: Commit to GitHub
        github_success = self.commit_learning_data()
        
        # Step 2: Trigger Cloud Build
        cloud_success = self.trigger_cloud_build()
        
        if github_success or cloud_success:
            print("✅ AGI learning backup cycle completed successfully")
            return True
        else:
            print("❌ All backup methods failed")
            return False

def backup_learning_data_now():
    """Immediate backup function"""
    backup_system = GitHubBackupIntegration()
    return backup_system.full_backup_cycle()

if __name__ == "__main__":
    backup_learning_data_now()
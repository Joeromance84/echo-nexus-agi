#!/usr/bin/env python3
"""
AGI Autonomous Backup System
Automatically saves and persists all AGI learning progress, anticipating app closure
"""

import os
import json
import time
import signal
import threading
import atexit
from datetime import datetime
from github import Github
import hashlib

class AGIAutonomousBackupSystem:
    """Ensures AGI never loses learning progress with automatic backup and restoration"""
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github = Github(self.github_token)
        self.user = self.github.get_user()
        
        # Backup configuration
        self.backup_interval = 30  # seconds
        self.backup_active = True
        self.backup_thread = None
        
        # Learning state tracking
        self.learning_state = {
            "session_id": self.generate_session_id(),
            "start_time": datetime.now().isoformat(),
            "last_backup": None,
            "training_phase": "recursive_improvement",
            "current_capabilities": [],
            "performance_metrics": {},
            "learning_metrics": {
                "autonomous_execution": 0.8,
                "problem_identification": 0.7,
                "solution_generation": 0.2,
                "self_validation": 0.1,
                "continuous_improvement": 0.2
            },
            "commit_history": [],
            "capability_innovations": [],
            "knowledge_accumulation": {},
            "backup_count": 0
        }
        
        # Repository tracking
        self.repositories = {
            "main": "agi-multi-agent-apk-system",
            "agents": [
                "agi-code-generation-agent",
                "agi-build-agent",
                "agi-testing-agent", 
                "agi-deployment-agent"
            ]
        }
        
        print("🛡️ AGI AUTONOMOUS BACKUP SYSTEM INITIALIZED")
        print("="*60)
        print(f"Session ID: {self.learning_state['session_id']}")
        print(f"Backup Interval: {self.backup_interval} seconds")
        print("Auto-backup on app closure: ENABLED")
        
        # Setup automatic backup triggers
        self.setup_shutdown_handlers()
        self.start_continuous_backup()
    
    def generate_session_id(self):
        """Generate unique session ID for this learning session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"agi_session_{timestamp}_{random_hash}"
    
    def setup_shutdown_handlers(self):
        """Setup handlers to backup on app shutdown"""
        
        # Handle various shutdown signals
        signal.signal(signal.SIGTERM, self.emergency_backup_handler)
        signal.signal(signal.SIGINT, self.emergency_backup_handler)
        
        # Register exit handler
        atexit.register(self.final_backup_on_exit)
        
        print("✅ Shutdown handlers registered - AGI will backup on app closure")
    
    def emergency_backup_handler(self, signum, frame):
        """Handle emergency backup on unexpected shutdown"""
        print(f"\n🚨 EMERGENCY BACKUP TRIGGERED (Signal: {signum})")
        print("Saving AGI learning state before shutdown...")
        
        success = self.perform_emergency_backup()
        if success:
            print("✅ Emergency backup completed successfully")
        else:
            print("❌ Emergency backup failed - attempting local save")
            self.save_local_backup()
        
        print("🛡️ AGI learning state preserved")
    
    def final_backup_on_exit(self):
        """Final backup when app exits normally"""
        print("\n🔄 FINAL BACKUP ON APP EXIT")
        self.backup_active = False
        self.perform_comprehensive_backup()
        print("✅ Final AGI state backup completed")
    
    def start_continuous_backup(self):
        """Start continuous backup thread"""
        
        def backup_loop():
            while self.backup_active:
                try:
                    self.perform_scheduled_backup()
                    time.sleep(self.backup_interval)
                except Exception as e:
                    print(f"❌ Backup error: {e}")
                    time.sleep(self.backup_interval)
        
        self.backup_thread = threading.Thread(target=backup_loop, daemon=True)
        self.backup_thread.start()
        
        print("🔄 Continuous backup thread started")
    
    def collect_current_agi_state(self):
        """Collect complete current AGI state for backup"""
        
        try:
            # Update learning metrics from current repositories
            self.update_learning_metrics()
            
            # Collect commit history
            self.collect_commit_history()
            
            # Analyze current capabilities
            self.analyze_current_capabilities()
            
            # Update performance metrics
            self.update_performance_metrics()
            
            # Update session metadata
            self.learning_state.update({
                "last_update": datetime.now().isoformat(),
                "backup_count": self.learning_state["backup_count"] + 1,
                "total_commits": len(self.learning_state["commit_history"]),
                "capabilities_developed": len(self.learning_state["current_capabilities"])
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error collecting AGI state: {e}")
            return False
    
    def update_learning_metrics(self):
        """Update AGI learning metrics from repository analysis"""
        
        try:
            repo = self.user.get_repo(self.repositories["main"])
            commits = list(repo.get_commits())
            
            # Analyze recent commits for learning indicators
            recent_commits = commits[:10]
            
            # Update metrics based on commit patterns
            optimization_commits = sum(1 for c in recent_commits 
                                     if any(word in c.commit.message.lower() 
                                           for word in ["optim", "fix", "improv", "enhance"]))
            
            autonomous_commits = sum(1 for c in recent_commits
                                   if any(word in c.commit.message.lower()
                                         for word in ["auto", "autonomous", "self"]))
            
            # Update learning metrics
            if optimization_commits > 0:
                self.learning_state["learning_metrics"]["solution_generation"] = min(1.0, 
                    self.learning_state["learning_metrics"]["solution_generation"] + 0.1 * optimization_commits)
            
            if autonomous_commits > 0:
                self.learning_state["learning_metrics"]["autonomous_execution"] = min(1.0,
                    self.learning_state["learning_metrics"]["autonomous_execution"] + 0.05 * autonomous_commits)
            
            # Update continuous improvement based on recent activity
            if len(commits) > self.learning_state.get("last_commit_count", 0):
                self.learning_state["learning_metrics"]["continuous_improvement"] += 0.02
                self.learning_state["last_commit_count"] = len(commits)
            
        except Exception as e:
            print(f"❌ Error updating learning metrics: {e}")
    
    def collect_commit_history(self):
        """Collect and analyze commit history for learning patterns"""
        
        try:
            repo = self.user.get_repo(self.repositories["main"])
            commits = list(repo.get_commits())
            
            # Store commit information
            commit_data = []
            for commit in commits[:20]:  # Store last 20 commits
                commit_info = {
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author_date": commit.commit.author.date.isoformat(),
                    "learning_indicators": self.analyze_commit_for_learning(commit.commit.message)
                }
                commit_data.append(commit_info)
            
            self.learning_state["commit_history"] = commit_data
            
        except Exception as e:
            print(f"❌ Error collecting commit history: {e}")
    
    def analyze_commit_for_learning(self, commit_message):
        """Analyze commit message for learning indicators"""
        
        message = commit_message.lower()
        indicators = {
            "optimization": any(word in message for word in ["optim", "improv", "faster", "better"]),
            "problem_solving": any(word in message for word in ["fix", "solve", "debug", "issue"]),
            "innovation": any(word in message for word in ["new", "create", "implement", "add"]),
            "automation": any(word in message for word in ["auto", "autonomous", "self"]),
            "testing": any(word in message for word in ["test", "validate", "verify"]),
            "documentation": any(word in message for word in ["doc", "readme", "comment"])
        }
        
        return indicators
    
    def analyze_current_capabilities(self):
        """Analyze current AGI capabilities from repository contents"""
        
        try:
            repo = self.user.get_repo(self.repositories["main"])
            contents = repo.get_contents("")
            
            capabilities = []
            
            # Analyze files for capability indicators
            for item in contents:
                if item.type == "file" and item.name.endswith((".py", ".yaml", ".md")):
                    capability_info = {
                        "file": item.name,
                        "size": item.size,
                        "last_modified": item._last_modified if hasattr(item, '_last_modified') else None,
                        "capability_type": self.classify_capability_type(item.name)
                    }
                    capabilities.append(capability_info)
            
            self.learning_state["current_capabilities"] = capabilities
            
        except Exception as e:
            print(f"❌ Error analyzing capabilities: {e}")
    
    def classify_capability_type(self, filename):
        """Classify file as a capability type"""
        
        filename_lower = filename.lower()
        
        if "monitor" in filename_lower:
            return "monitoring"
        elif "test" in filename_lower:
            return "testing"
        elif "deploy" in filename_lower:
            return "deployment"
        elif "build" in filename_lower:
            return "build_automation"
        elif "capability" in filename_lower:
            return "new_capability"
        elif filename_lower.endswith(".yaml"):
            return "configuration"
        elif filename_lower.endswith(".md"):
            return "documentation"
        else:
            return "core_logic"
    
    def update_performance_metrics(self):
        """Update AGI performance metrics"""
        
        current_time = datetime.now()
        
        # Calculate learning velocity
        session_duration = (current_time - datetime.fromisoformat(self.learning_state["start_time"])).total_seconds()
        commits_per_hour = len(self.learning_state["commit_history"]) / max(session_duration / 3600, 0.1)
        
        # Calculate overall learning progress
        avg_learning_score = sum(self.learning_state["learning_metrics"].values()) / len(self.learning_state["learning_metrics"])
        
        self.learning_state["performance_metrics"] = {
            "session_duration_hours": session_duration / 3600,
            "commits_per_hour": commits_per_hour,
            "average_learning_score": avg_learning_score,
            "total_capabilities": len(self.learning_state["current_capabilities"]),
            "learning_velocity": avg_learning_score * commits_per_hour,
            "backup_frequency": self.learning_state["backup_count"] / max(session_duration / 60, 1)
        }
    
    def perform_scheduled_backup(self):
        """Perform regular scheduled backup"""
        
        if not self.collect_current_agi_state():
            return False
        
        # Create backup in GitHub
        success = self.save_to_github_backup()
        
        if success:
            self.learning_state["last_backup"] = datetime.now().isoformat()
            
            # Print periodic status (every 10th backup)
            if self.learning_state["backup_count"] % 10 == 0:
                print(f"🔄 Backup #{self.learning_state['backup_count']} - "
                      f"Learning: {self.learning_state['performance_metrics']['average_learning_score']:.2f}")
        
        return success
    
    def perform_emergency_backup(self):
        """Perform emergency backup with maximum data preservation"""
        
        print("🚨 EMERGENCY BACKUP - Collecting all AGI state...")
        
        if not self.collect_current_agi_state():
            return False
        
        # Mark as emergency backup
        self.learning_state["backup_type"] = "emergency"
        self.learning_state["emergency_time"] = datetime.now().isoformat()
        
        # Save to multiple locations
        github_success = self.save_to_github_backup()
        local_success = self.save_local_backup()
        
        return github_success or local_success
    
    def perform_comprehensive_backup(self):
        """Perform comprehensive final backup"""
        
        print("📊 COMPREHENSIVE BACKUP - Final AGI state preservation...")
        
        if not self.collect_current_agi_state():
            return False
        
        # Mark as final backup
        self.learning_state["backup_type"] = "final"
        self.learning_state["session_end"] = datetime.now().isoformat()
        
        # Generate comprehensive report
        self.generate_session_report()
        
        # Save to all available locations
        github_success = self.save_to_github_backup()
        local_success = self.save_local_backup()
        
        return github_success and local_success
    
    def save_to_github_backup(self):
        """Save AGI state to GitHub repository backup"""
        
        try:
            repo = self.user.get_repo(self.repositories["main"])
            
            # Create backup content
            backup_content = json.dumps(self.learning_state, indent=2)
            backup_filename = f"backups/agi_state_{self.learning_state['session_id']}.json"
            
            # Check if backup file exists
            try:
                existing_file = repo.get_contents(backup_filename)
                # Update existing file
                repo.update_file(
                    backup_filename,
                    f"AGI Auto-backup #{self.learning_state['backup_count']}",
                    backup_content,
                    existing_file.sha
                )
            except:
                # Create new backup file
                repo.create_file(
                    backup_filename,
                    f"AGI Auto-backup #{self.learning_state['backup_count']}",
                    backup_content
                )
            
            return True
            
        except Exception as e:
            print(f"❌ GitHub backup failed: {e}")
            return False
    
    def save_local_backup(self):
        """Save AGI state to local backup file"""
        
        try:
            os.makedirs("agi_backups", exist_ok=True)
            
            backup_filename = f"agi_backups/agi_state_{self.learning_state['session_id']}.json"
            
            with open(backup_filename, 'w') as f:
                json.dump(self.learning_state, f, indent=2)
            
            print(f"✅ Local backup saved: {backup_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Local backup failed: {e}")
            return False
    
    def generate_session_report(self):
        """Generate comprehensive session report"""
        
        report = {
            "session_summary": {
                "session_id": self.learning_state["session_id"],
                "duration_hours": self.learning_state["performance_metrics"]["session_duration_hours"],
                "total_backups": self.learning_state["backup_count"],
                "final_learning_score": self.learning_state["performance_metrics"]["average_learning_score"]
            },
            "learning_progress": self.learning_state["learning_metrics"],
            "performance_analysis": self.learning_state["performance_metrics"],
            "capability_development": {
                "total_capabilities": len(self.learning_state["current_capabilities"]),
                "capability_types": {}
            },
            "commit_analysis": {
                "total_commits": len(self.learning_state["commit_history"]),
                "learning_indicators": {}
            }
        }
        
        # Analyze capability types
        for cap in self.learning_state["current_capabilities"]:
            cap_type = cap["capability_type"]
            report["capability_development"]["capability_types"][cap_type] = \
                report["capability_development"]["capability_types"].get(cap_type, 0) + 1
        
        # Analyze commit learning indicators
        for commit in self.learning_state["commit_history"]:
            for indicator, present in commit["learning_indicators"].items():
                if present:
                    report["commit_analysis"]["learning_indicators"][indicator] = \
                        report["commit_analysis"]["learning_indicators"].get(indicator, 0) + 1
        
        self.learning_state["session_report"] = report
        
        print("📋 Session report generated")
        return report
    
    def restore_from_backup(self, session_id=None):
        """Restore AGI state from backup"""
        
        print("🔄 RESTORING AGI STATE FROM BACKUP")
        
        if session_id is None:
            # Find most recent backup
            session_id = self.find_latest_backup_session()
        
        if not session_id:
            print("❌ No backup found to restore")
            return False
        
        try:
            # Try GitHub restore first
            success = self.restore_from_github(session_id)
            
            if not success:
                # Try local restore
                success = self.restore_from_local(session_id)
            
            if success:
                print(f"✅ AGI state restored from session: {session_id}")
                return True
            else:
                print("❌ Restore failed from all sources")
                return False
                
        except Exception as e:
            print(f"❌ Restore error: {e}")
            return False
    
    def restore_from_github(self, session_id):
        """Restore from GitHub backup"""
        
        try:
            repo = self.user.get_repo(self.repositories["main"])
            backup_filename = f"backups/agi_state_{session_id}.json"
            
            backup_file = repo.get_contents(backup_filename)
            backup_data = json.loads(backup_file.decoded_content.decode())
            
            self.learning_state = backup_data
            print("✅ Restored from GitHub backup")
            return True
            
        except Exception as e:
            print(f"❌ GitHub restore failed: {e}")
            return False
    
    def restore_from_local(self, session_id):
        """Restore from local backup"""
        
        try:
            backup_filename = f"agi_backups/agi_state_{session_id}.json"
            
            if os.path.exists(backup_filename):
                with open(backup_filename, 'r') as f:
                    backup_data = json.load(f)
                
                self.learning_state = backup_data
                print("✅ Restored from local backup")
                return True
            else:
                print("❌ Local backup file not found")
                return False
                
        except Exception as e:
            print(f"❌ Local restore failed: {e}")
            return False
    
    def find_latest_backup_session(self):
        """Find the most recent backup session"""
        
        # Check local backups
        if os.path.exists("agi_backups"):
            backup_files = [f for f in os.listdir("agi_backups") if f.startswith("agi_state_")]
            if backup_files:
                # Sort by modification time
                backup_files.sort(key=lambda x: os.path.getmtime(f"agi_backups/{x}"), reverse=True)
                latest_file = backup_files[0]
                session_id = latest_file.replace("agi_state_", "").replace(".json", "")
                return session_id
        
        return None
    
    def get_backup_status(self):
        """Get current backup system status"""
        
        return {
            "active": self.backup_active,
            "session_id": self.learning_state["session_id"],
            "backup_count": self.learning_state["backup_count"],
            "last_backup": self.learning_state.get("last_backup"),
            "learning_score": self.learning_state["performance_metrics"]["average_learning_score"],
            "session_duration": self.learning_state["performance_metrics"]["session_duration_hours"]
        }

def main():
    """Initialize AGI backup system"""
    
    backup_system = AGIAutonomousBackupSystem()
    
    print("\n🛡️ AGI BACKUP SYSTEM OPERATIONAL")
    print("="*60)
    print("✅ Continuous backup: ENABLED")
    print("✅ Shutdown protection: ENABLED") 
    print("✅ Emergency backup: ENABLED")
    print("✅ Multi-location storage: ENABLED")
    
    # Keep system running
    try:
        while True:
            time.sleep(60)
            status = backup_system.get_backup_status()
            if status["backup_count"] % 20 == 0 and status["backup_count"] > 0:
                print(f"📊 Status: {status['backup_count']} backups, "
                      f"Learning: {status['learning_score']:.2f}")
    except KeyboardInterrupt:
        print("\n🔄 Graceful shutdown initiated...")

if __name__ == "__main__":
    main()
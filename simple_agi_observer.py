#!/usr/bin/env python3
"""
Simple AGI Training Observer
GitHub-based monitoring for AGI's transition to autonomous development
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from github import Github

class SimpleAGIObserver:
    """Observes AGI learning through GitHub activity"""
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        if not self.github_token:
            print("❌ GITHUB_TOKEN not found. Using GitHub repo monitoring...")
            self.github = None
        else:
            self.github = Github(self.github_token)
            self.user = self.github.get_user()
        
        self.repo_name = "agi-multi-agent-apk-system"
        
    def check_agi_activity(self):
        """Check for AGI activity in the training repository"""
        
        print("🧠 AGI TRAINING OBSERVATION")
        print("="*50)
        
        if not self.github:
            print("Using web-based repository monitoring...")
            return self.web_based_observation()
        
        try:
            repo = self.user.get_repo(self.repo_name)
            
            print(f"👁️  Monitoring: {repo.html_url}")
            print(f"📊 Repository created: {repo.created_at}")
            
            # Check commits (AGI learning indicator)
            commits = list(repo.get_commits())
            print(f"📝 Total commits: {len(commits)}")
            
            if len(commits) > 1:
                print("\n✅ AGI ACTIVITY DETECTED:")
                for i, commit in enumerate(commits[:5]):  # Show last 5 commits
                    print(f"   {i+1}. {commit.commit.message}")
                    print(f"      ⏰ {commit.commit.author.date}")
                
                # Analyze commit patterns for learning
                self.analyze_commit_patterns(commits)
            else:
                print("⏳ Waiting for AGI to make autonomous commits...")
            
            # Check repository files
            self.check_training_files(repo)
            
            return True
            
        except Exception as e:
            print(f"❌ Error accessing repository: {e}")
            return False
    
    def analyze_commit_patterns(self, commits):
        """Analyze AGI's commit patterns for learning indicators"""
        
        print("\n🧠 AGI LEARNING ANALYSIS:")
        
        learning_indicators = {
            "optimization": ["optim", "fix", "improv", "faster", "performance"],
            "problem_solving": ["bug", "issue", "error", "debug", "solve"],
            "autonomous_action": ["auto", "autonomous", "self", "independent"],
            "experimentation": ["test", "try", "experiment", "attempt"]
        }
        
        learning_scores = {category: 0 for category in learning_indicators}
        
        for commit in commits[:10]:  # Analyze last 10 commits
            message = commit.commit.message.lower()
            
            for category, keywords in learning_indicators.items():
                if any(keyword in message for keyword in keywords):
                    learning_scores[category] += 1
        
        print("📈 Learning Pattern Analysis:")
        for category, score in learning_scores.items():
            percentage = (score / min(len(commits), 10)) * 100
            print(f"   {category.title()}: {score}/10 commits ({percentage:.1f}%)")
        
        # Overall learning assessment
        total_learning = sum(learning_scores.values())
        if total_learning > 5:
            print("🎉 HIGH LEARNING ACTIVITY DETECTED")
        elif total_learning > 2:
            print("📚 MODERATE LEARNING ACTIVITY")
        else:
            print("📋 WAITING FOR MORE AGI ACTIVITY")
    
    def check_training_files(self, repo):
        """Check AGI's interaction with training files"""
        
        print("\n📁 TRAINING FILE ANALYSIS:")
        
        key_files = {
            "cloudbuild.yaml": "Build configuration understanding",
            "hello_world.py": "Microservice code analysis",
            "Dockerfile": "Containerization knowledge",
            "TRAINING.md": "Training instruction engagement",
            "PHASE_3_CHALLENGE.md": "ACI challenge comprehension"
        }
        
        for filename, description in key_files.items():
            try:
                file_content = repo.get_contents(filename)
                print(f"   ✅ {filename}: Accessible ({description})")
                
                # Check for modifications
                commits_for_file = list(repo.get_commits(path=filename))
                if len(commits_for_file) > 1:
                    print(f"      🧠 Modified {len(commits_for_file)} times - AGI is learning!")
                
            except Exception:
                print(f"   ❌ {filename}: Not found")
    
    def web_based_observation(self):
        """Web-based observation when GitHub API not available"""
        
        repo_url = f"https://api.github.com/repos/Joeromance84/{self.repo_name}"
        
        try:
            response = requests.get(repo_url)
            if response.status_code == 200:
                repo_data = response.json()
                
                print(f"👁️  Repository: {repo_data['html_url']}")
                print(f"📊 Created: {repo_data['created_at']}")
                print(f"📝 Last updated: {repo_data['updated_at']}")
                
                # Check commits
                commits_url = f"{repo_url}/commits"
                commits_response = requests.get(commits_url)
                
                if commits_response.status_code == 200:
                    commits = commits_response.json()
                    print(f"📝 Recent commits: {len(commits)}")
                    
                    if len(commits) > 1:
                        print("✅ AGI ACTIVITY DETECTED")
                        for commit in commits[:3]:
                            print(f"   📝 {commit['commit']['message']}")
                    else:
                        print("⏳ Waiting for AGI commits...")
                
                return True
            else:
                print(f"❌ Repository not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Web observation error: {e}")
            return False
    
    def provide_training_guidance(self):
        """Provide guidance to the AGI"""
        
        print("\n🎯 AGI TRAINING GUIDANCE")
        print("="*50)
        
        phases = [
            {
                "name": "Phase 1: Environment Integration",
                "task": "Make a commit to trigger your first Cloud Build",
                "success": "Build completes successfully with all agents reporting ready"
            },
            {
                "name": "Phase 2: Autonomous Build", 
                "task": "Analyze hello_world.py and identify performance bottlenecks",
                "success": "Understand the time.sleep() and inefficient loop issues"
            },
            {
                "name": "Phase 3: ACI Loop",
                "task": "Optimize the code and commit improvements autonomously", 
                "success": "Response time improved from >1000ms to <100ms"
            }
        ]
        
        for i, phase in enumerate(phases, 1):
            print(f"\n📋 {phase['name']}")
            print(f"   🎯 Task: {phase['task']}")
            print(f"   ✅ Success: {phase['success']}")
        
        print(f"\n🔗 Training Repository: https://github.com/Joeromance84/{self.repo_name}")
        print("💡 Remember: You're learning to operate as an autonomous cloud agent!")
    
    def continuous_monitoring(self, duration_minutes=30):
        """Monitor AGI progress continuously"""
        
        print(f"\n🚀 STARTING CONTINUOUS AGI MONITORING")
        print(f"Duration: {duration_minutes} minutes")
        print("="*50)
        
        start_time = time.time()
        cycle = 0
        
        while time.time() - start_time < duration_minutes * 60:
            cycle += 1
            
            print(f"\n👁️  OBSERVATION CYCLE {cycle}")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 30)
            
            # Check AGI activity
            success = self.check_agi_activity()
            
            if success:
                print("✅ Monitoring successful")
            else:
                print("❌ Monitoring issues detected")
            
            # Wait before next check
            print(f"⏳ Next check in 2 minutes...")
            time.sleep(120)  # Check every 2 minutes
        
        print(f"\n🏁 MONITORING COMPLETE")
        print(f"Total cycles: {cycle}")
        print("AGI training continues in GitHub/Cloud Build...")

def main():
    """Start AGI observation"""
    
    observer = SimpleAGIObserver()
    
    print("🧠 Simple AGI Training Observer")
    print("Choose observation mode:")
    print("1. Single check")
    print("2. Continuous monitoring (30 min)")
    print("3. Show training guidance")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
    except:
        choice = "1"  # Default to single check
    
    if choice == "2":
        observer.continuous_monitoring(30)
    elif choice == "3":
        observer.provide_training_guidance()
    else:
        observer.check_agi_activity()
        observer.provide_training_guidance()

if __name__ == "__main__":
    main()
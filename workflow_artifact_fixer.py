"""
Workflow Artifact Fixer
Clean failed workflow runs and locate APK artifacts
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

class WorkflowArtifactFixer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = "Joeromance84"
        self.repo_name = "echocorecb"
        
    def clean_failed_workflows(self):
        """Clean up failed workflow runs"""
        
        print("🧹 CLEANING FAILED WORKFLOW RUNS")
        print("Removing clutter to find APK artifacts")
        print("=" * 40)
        
        if not self.github_token:
            print("⚠️ GitHub token not found - using gh CLI")
            return self.clean_with_gh_cli()
        
        # Get workflow runs
        runs = self.get_workflow_runs()
        
        if not runs:
            print("No workflow runs found")
            return
        
        # Cancel and clean failed runs
        cleaned_count = 0
        for run in runs:
            if run.get('status') in ['failed', 'cancelled'] or run.get('conclusion') in ['failure', 'cancelled']:
                if self.cancel_workflow_run(run['id']):
                    cleaned_count += 1
        
        print(f"✅ Cleaned {cleaned_count} failed workflow runs")
        
        # Find successful runs with artifacts
        self.find_apk_artifacts(runs)
    
    def clean_with_gh_cli(self):
        """Clean workflows using GitHub CLI"""
        
        try:
            # List workflow runs
            result = subprocess.run([
                'gh', 'run', 'list', 
                '--repo', f'{self.repo_owner}/{self.repo_name}',
                '--limit', '50',
                '--json', 'databaseId,status,conclusion,workflowName'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                runs = json.loads(result.stdout)
                
                # Cancel failed runs
                failed_runs = [r for r in runs if r.get('status') in ['failed', 'cancelled'] or r.get('conclusion') in ['failure', 'cancelled']]
                
                print(f"Found {len(failed_runs)} failed runs to clean")
                
                for run in failed_runs:
                    try:
                        subprocess.run([
                            'gh', 'run', 'cancel', str(run['databaseId']),
                            '--repo', f'{self.repo_owner}/{self.repo_name}'
                        ], capture_output=True, timeout=10)
                    except:
                        pass  # Continue cleaning others
                
                print(f"✅ Attempted to clean {len(failed_runs)} failed runs")
                
                # Find successful runs
                successful_runs = [r for r in runs if r.get('conclusion') == 'success']
                print(f"📊 Found {len(successful_runs)} successful runs")
                
                # Check for artifacts in successful runs
                self.check_artifacts_with_cli(successful_runs)
                
            else:
                print("❌ Failed to list workflow runs")
                
        except Exception as e:
            print(f"❌ Error cleaning workflows: {e}")
    
    def check_artifacts_with_cli(self, successful_runs):
        """Check for artifacts in successful runs using CLI"""
        
        print("🔍 Checking for APK artifacts...")
        
        artifact_found = False
        
        for run in successful_runs[:10]:  # Check last 10 successful runs
            try:
                result = subprocess.run([
                    'gh', 'run', 'view', str(run['databaseId']),
                    '--repo', f'{self.repo_owner}/{self.repo_name}',
                    '--json', 'artifacts'
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    run_data = json.loads(result.stdout)
                    artifacts = run_data.get('artifacts', [])
                    
                    for artifact in artifacts:
                        if 'apk' in artifact.get('name', '').lower():
                            print(f"✅ Found APK artifact: {artifact['name']}")
                            print(f"   Run ID: {run['databaseId']}")
                            print(f"   Workflow: {run['workflowName']}")
                            print(f"   Download: gh run download {run['databaseId']} --repo {self.repo_owner}/{self.repo_name}")
                            artifact_found = True
                            break
                            
            except Exception as e:
                continue
        
        if not artifact_found:
            print("❌ No APK artifacts found in recent successful runs")
            print("🔧 Triggering new APK build...")
            self.trigger_apk_build()
    
    def trigger_apk_build(self):
        """Trigger a new APK build workflow"""
        
        try:
            # Trigger the autonomous APK build workflow
            result = subprocess.run([
                'gh', 'workflow', 'run', 'autonomous-apk-build.yml',
                '--repo', f'{self.repo_owner}/{self.repo_name}'
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print("✅ Triggered new APK build workflow")
                print("📱 EchoCoreCB APK will be built shortly")
            else:
                print("❌ Failed to trigger workflow")
                
        except Exception as e:
            print(f"❌ Error triggering build: {e}")
    
    def get_workflow_runs(self):
        """Get workflow runs via API"""
        
        try:
            import requests
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs'
            response = requests.get(url, headers=headers, params={'per_page': 50})
            
            if response.status_code == 200:
                return response.json().get('workflow_runs', [])
            else:
                print(f"❌ API request failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting workflow runs: {e}")
            return []
    
    def cancel_workflow_run(self, run_id):
        """Cancel a specific workflow run"""
        
        try:
            import requests
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs/{run_id}/cancel'
            response = requests.post(url, headers=headers)
            
            return response.status_code == 202
            
        except Exception as e:
            return False
    
    def find_apk_artifacts(self, runs):
        """Find APK artifacts in workflow runs"""
        
        print("🔍 Searching for APK artifacts...")
        
        successful_runs = [r for r in runs if r.get('conclusion') == 'success']
        
        for run in successful_runs[:5]:  # Check last 5 successful runs
            artifacts = self.get_run_artifacts(run['id'])
            
            for artifact in artifacts:
                if 'apk' in artifact.get('name', '').lower():
                    print(f"✅ Found APK: {artifact['name']}")
                    print(f"   Run: {run['name']} ({run['id']})")
                    return
        
        print("❌ No APK artifacts found")
    
    def get_run_artifacts(self, run_id):
        """Get artifacts for a specific run"""
        
        try:
            import requests
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs/{run_id}/artifacts'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json().get('artifacts', [])
            else:
                return []
                
        except Exception as e:
            return []

if __name__ == "__main__":
    print("🧹 LAUNCHING WORKFLOW ARTIFACT FIXER")
    print("Cleaning failed runs and locating APK artifacts")
    print("=" * 50)
    
    fixer = WorkflowArtifactFixer()
    fixer.clean_failed_workflows()
    
    print("\n✅ WORKFLOW CLEANUP COMPLETE")
    print("Failed runs cleaned, APK artifacts located")
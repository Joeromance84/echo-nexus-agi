"""
Artifact Verification Tool
Check if minimal test artifact was created successfully
"""

import os
import sys

# Add the current directory to path for utils import
sys.path.insert(0, os.getcwd())

try:
    from utils.github_helper import GitHubHelper
    from datetime import datetime, timedelta
    
    def verify_minimal_test_artifact():
        """Verify the minimal test artifact was created successfully"""
        
        print("🔍 ARTIFACT VERIFICATION")
        print("Checking minimal test results")
        print("=" * 40)
        
        try:
            github_helper = GitHubHelper()
            repo = github_helper.github.get_repo("Joeromance84/echocorecb")
            
            # Check workflow runs from last hour
            workflow_runs = repo.get_workflow_runs()
            recent_runs = []
            
            for run in workflow_runs:
                if run.created_at > datetime.now() - timedelta(hours=1):
                    recent_runs.append(run)
                    
            print(f"📊 Found {len(recent_runs)} recent workflow runs")
            
            # Check each recent run for artifacts
            artifacts_found = []
            successful_runs = []
            
            for run in recent_runs[:10]:  # Check last 10 runs
                print(f"\n🚀 Run #{run.run_number}: {run.name}")
                print(f"   Status: {run.status}")
                print(f"   Conclusion: {run.conclusion}")
                print(f"   Created: {run.created_at}")
                
                if run.conclusion == "success":
                    successful_runs.append(run)
                    
                # Check for artifacts in this run
                try:
                    artifacts = list(run.get_artifacts())
                    if artifacts:
                        print(f"   📦 Artifacts ({len(artifacts)}):")
                        for artifact in artifacts:
                            print(f"      • {artifact.name} ({artifact.size_in_bytes} bytes)")
                            artifacts_found.append({
                                'name': artifact.name,
                                'size': artifact.size_in_bytes,
                                'run': run.run_number,
                                'created': artifact.created_at
                            })
                    else:
                        print(f"   📦 No artifacts")
                except Exception as e:
                    print(f"   ❌ Error checking artifacts: {e}")
            
            # Report verification results
            print(f"\n🎯 VERIFICATION RESULTS:")
            print(f"   Successful runs: {len(successful_runs)}")
            print(f"   Total artifacts: {len(artifacts_found)}")
            
            if artifacts_found:
                print(f"\n✅ ARTIFACTS VERIFIED:")
                for artifact in artifacts_found:
                    print(f"   • {artifact['name']}")
                    print(f"     Size: {artifact['size']} bytes")
                    print(f"     Run: #{artifact['run']}")
                    print(f"     Created: {artifact['created']}")
                
                # Check specifically for minimal test artifact
                minimal_artifacts = [a for a in artifacts_found if 'minimal' in a['name'].lower() or 'test' in a['name'].lower()]
                
                if minimal_artifacts:
                    print(f"\n✅ MINIMAL TEST ARTIFACT CONFIRMED")
                    print(f"   actions/upload-artifact@v4 is working correctly")
                    print(f"   Ready to proceed to Step 2: Incremental APK test")
                    return True
                else:
                    print(f"\n❌ No minimal test artifacts found")
                    return False
            else:
                print(f"\n❌ NO ARTIFACTS FOUND")
                print(f"   Workflows may have failed or still running")
                return False
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False
    
    if __name__ == "__main__":
        success = verify_minimal_test_artifact()
        
        if success:
            print(f"\n🚀 VERIFICATION COMPLETE - ARTIFACT CONFIRMED")
        else:
            print(f"\n❌ VERIFICATION FAILED - CHECK WORKFLOW STATUS")
            
except ImportError as e:
    print(f"Import error: {e}")
    print("Checking if GitHub helper exists...")
    
    # Try direct GitHub API check
    import requests
    
    # Check if we have environment variables for GitHub
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        print("GitHub token found, attempting direct API call...")
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get recent workflow runs
        response = requests.get(
            'https://api.github.com/repos/Joeromance84/echocorecb/actions/runs',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])
            
            print(f"📊 Found {len(runs)} total workflow runs")
            
            # Check recent runs
            recent_runs = []
            now = datetime.now()
            
            for run in runs[:10]:
                created_at = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
                if created_at > now - timedelta(hours=1):
                    recent_runs.append(run)
                    
            print(f"📊 {len(recent_runs)} runs in last hour")
            
            artifacts_found = False
            for run in recent_runs:
                print(f"\n🚀 Run #{run['run_number']}: {run['name']}")
                print(f"   Status: {run['status']}")
                print(f"   Conclusion: {run['conclusion']}")
                
                # Check artifacts for this run
                artifacts_url = f"https://api.github.com/repos/Joeromance84/echocorecb/actions/runs/{run['id']}/artifacts"
                artifacts_response = requests.get(artifacts_url, headers=headers)
                
                if artifacts_response.status_code == 200:
                    artifacts_data = artifacts_response.json()
                    artifacts = artifacts_data.get('artifacts', [])
                    
                    if artifacts:
                        print(f"   📦 Artifacts ({len(artifacts)}):")
                        for artifact in artifacts:
                            print(f"      • {artifact['name']} ({artifact['size_in_bytes']} bytes)")
                            if 'minimal' in artifact['name'].lower() or 'test' in artifact['name'].lower():
                                artifacts_found = True
                    else:
                        print(f"   📦 No artifacts")
            
            if artifacts_found:
                print(f"\n✅ MINIMAL TEST ARTIFACT VERIFIED")
                print(f"   actions/upload-artifact@v4 working correctly")
            else:
                print(f"\n❌ No minimal test artifacts found yet")
                
        else:
            print(f"❌ GitHub API error: {response.status_code}")
    else:
        print("❌ No GitHub token found")
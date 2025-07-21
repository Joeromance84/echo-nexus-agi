#!/usr/bin/env python3
"""
GitHub to Cloud Build Trigger Verification Script
Checks the status of GitHub-Cloud Build integration and triggers
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_command(cmd, check=False):
    """Run command with error handling"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_cloudbuild_files():
    """Check for Cloud Build configuration files"""
    cloudbuild_files = [
        "cloudbuild.yaml",
        "cloudbuild-autonomous.yaml", 
        "cloudbuild-federated.yaml",
        "cloudbuild-consciousness.yaml",
        "cloud_build/cloudbuild.yaml"
    ]
    
    found_files = []
    for file_path in cloudbuild_files:
        if Path(file_path).exists():
            found_files.append(file_path)
            log(f"✅ Found: {file_path}")
        else:
            log(f"❌ Missing: {file_path}")
    
    return found_files

def check_github_integration_files():
    """Check for GitHub integration scripts"""
    integration_files = [
        "github_to_cloudbuild_handler.sh",
        "cloudbuild_to_github_handler.sh", 
        "cloudbuild_trigger_intelligence.json",
        "cloudbuild_pubsub_config.json"
    ]
    
    found_files = []
    for file_path in integration_files:
        if Path(file_path).exists():
            found_files.append(file_path)
            log(f"✅ Found integration file: {file_path}")
        else:
            log(f"❌ Missing integration file: {file_path}")
    
    return found_files

def check_github_secrets():
    """Check for GitHub secrets in environment"""
    github_secrets = [
        "GITHUB_TOKEN",
        "GITHUB_USER", 
        "GOOGLE_CLOUD_PROJECT"
    ]
    
    found_secrets = {}
    for secret in github_secrets:
        value = os.environ.get(secret)
        if value:
            found_secrets[secret] = "configured"
            log(f"✅ Secret {secret}: configured")
        else:
            log(f"❌ Secret {secret}: not found")
    
    return found_secrets

def check_cloudbuild_triggers():
    """Attempt to check Cloud Build triggers"""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        log("❌ Cannot check triggers: GOOGLE_CLOUD_PROJECT not set")
        return False, []
    
    # Try to list triggers
    success, stdout, stderr = run_command(f"gcloud builds triggers list --project={project_id} --format=json")
    
    if success:
        try:
            triggers = json.loads(stdout) if stdout else []
            log(f"✅ Found {len(triggers)} Cloud Build triggers")
            
            for trigger in triggers:
                name = trigger.get('name', 'unnamed')
                repo = trigger.get('github', {}).get('name', 'unknown')
                branch = trigger.get('github', {}).get('push', {}).get('branch', 'unknown')
                log(f"  - Trigger: {name} (repo: {repo}, branch: {branch})")
            
            return True, triggers
        except json.JSONDecodeError:
            log("❌ Failed to parse triggers JSON")
            return False, []
    else:
        log(f"❌ Failed to list triggers: {stderr}")
        return False, []

def check_github_repo_connection():
    """Check GitHub repository configuration"""
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        log("❌ Cannot check GitHub repo: GITHUB_TOKEN not set")
        return False
    
    try:
        from github import Github
        g = Github(github_token)
        user = g.get_user()
        
        # Check for echo-ai-android repository
        try:
            repo = user.get_repo("echo-ai-android")
            log(f"✅ GitHub repo found: {repo.html_url}")
            
            # Check for webhook or Cloud Build integration
            hooks = list(repo.get_hooks())
            log(f"✅ Repository has {len(hooks)} webhooks")
            
            for hook in hooks:
                if 'cloud' in hook.config.get('url', '').lower():
                    log(f"  - Cloud Build webhook: {hook.config.get('url', 'unknown')}")
            
            return True
        except Exception as e:
            log(f"❌ Repository not found or inaccessible: {e}")
            return False
            
    except ImportError:
        log("❌ PyGithub not available for repository check")
        return False
    except Exception as e:
        log(f"❌ GitHub connection failed: {e}")
        return False

def create_trigger_setup_script():
    """Create script to set up GitHub-Cloud Build trigger"""
    
    setup_script = """#!/bin/bash
# GitHub to Cloud Build Trigger Setup Script

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-your-project-id}"
REPO_OWNER="Joeromance84"
REPO_NAME="echo-ai-android"
TRIGGER_NAME="echo-ai-android-build"

echo "🔧 Setting up GitHub to Cloud Build trigger..."

# Check authentication
echo "Checking gcloud authentication..."
gcloud auth list

# Check project
echo "Current project: $(gcloud config get-value project)"

# Create Cloud Build trigger for GitHub repository
echo "Creating Cloud Build trigger..."
gcloud builds triggers create github \\
  --repo-name="$REPO_NAME" \\
  --repo-owner="$REPO_OWNER" \\
  --branch-pattern=".*" \\
  --build-config="cloudbuild-android.yaml" \\
  --name="$TRIGGER_NAME" \\
  --description="Echo AI Android APK build trigger" \\
  --include-logs-with-status

echo "✅ Trigger setup complete!"
echo "Repository: https://github.com/$REPO_OWNER/$REPO_NAME"
echo "Trigger name: $TRIGGER_NAME"

# Test trigger
echo "Testing trigger..."
gcloud builds triggers run "$TRIGGER_NAME" --branch=main

echo "🎉 GitHub-Cloud Build integration configured!"
"""
    
    script_path = "scripts/setup_github_cloudbuild_trigger.sh"
    Path(script_path).write_text(setup_script)
    Path(script_path).chmod(0o755)
    
    return script_path

def main():
    """Main verification function"""
    log("🔍 Checking GitHub to Cloud Build Integration")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "cloudbuild_files": [],
        "integration_files": [],
        "github_secrets": {},
        "triggers_found": False,
        "github_repo_connected": False,
        "recommendations": []
    }
    
    # Check Cloud Build configuration files
    log("\n📄 Checking Cloud Build configuration files...")
    report["cloudbuild_files"] = check_cloudbuild_files()
    
    # Check integration files
    log("\n🔗 Checking GitHub integration files...")
    report["integration_files"] = check_github_integration_files()
    
    # Check environment secrets
    log("\n🔐 Checking environment secrets...")
    report["github_secrets"] = check_github_secrets()
    
    # Check Cloud Build triggers
    log("\n🎯 Checking Cloud Build triggers...")
    triggers_success, triggers = check_cloudbuild_triggers()
    report["triggers_found"] = triggers_success
    
    # Check GitHub repository connection
    log("\n🐙 Checking GitHub repository connection...")
    report["github_repo_connected"] = check_github_repo_connection()
    
    # Generate recommendations
    if not report["github_secrets"].get("GOOGLE_CLOUD_PROJECT"):
        report["recommendations"].append("Set GOOGLE_CLOUD_PROJECT environment variable")
    
    if not report["github_secrets"].get("GITHUB_TOKEN"):
        report["recommendations"].append("Set GITHUB_TOKEN environment variable")
    
    if not report["triggers_found"]:
        report["recommendations"].append("Create GitHub-Cloud Build trigger")
    
    if not report["github_repo_connected"]:
        report["recommendations"].append("Verify GitHub repository access")
    
    # Create setup script
    setup_script_path = create_trigger_setup_script()
    log(f"📜 Created setup script: {setup_script_path}")
    
    # Summary
    total_components = 4  # cloudbuild files, secrets, triggers, github repo
    working_components = sum([
        len(report["cloudbuild_files"]) > 0,
        len(report["github_secrets"]) > 0,
        report["triggers_found"],
        report["github_repo_connected"]
    ])
    
    log(f"\n📊 Integration Status: {working_components}/{total_components} components working")
    
    if working_components == total_components:
        log("🎉 GitHub-Cloud Build integration is fully configured!")
    else:
        log("⚠️ Integration setup incomplete")
        
        for rec in report["recommendations"]:
            log(f"  - {rec}")
    
    # Save report
    report_path = "github_cloudbuild_integration_report.json"
    Path(report_path).write_text(json.dumps(report, indent=2))
    log(f"📄 Integration report saved: {report_path}")
    
    return working_components == total_components

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
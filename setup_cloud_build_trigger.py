#!/usr/bin/env python3
"""
Google Cloud Build Trigger Setup for Echo AI Android
Creates GitHub-triggered Cloud Build for automatic APK generation
"""

import os
import json
import subprocess
from datetime import datetime

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_command(cmd, check=True):
    """Run command with error handling"""
    log(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False, "", e.stderr

def check_prerequisites():
    """Check if all prerequisites are met"""
    log("Checking prerequisites...")
    
    # Check environment variables
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        log("❌ GOOGLE_CLOUD_PROJECT environment variable not set")
        return False, None
    
    log(f"✅ Project ID: {project_id}")
    
    # Check gcloud authentication
    success, stdout, stderr = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'", check=False)
    if not success or not stdout.strip():
        log("❌ gcloud authentication required")
        return False, project_id
    
    log(f"✅ Authenticated as: {stdout.strip()}")
    
    # Check if Cloud Build API is enabled
    success, stdout, stderr = run_command(f"gcloud services list --enabled --filter='name:cloudbuild.googleapis.com' --format='value(name)' --project={project_id}", check=False)
    if not success or not stdout.strip():
        log("⚠️ Cloud Build API not enabled, attempting to enable...")
        success, _, _ = run_command(f"gcloud services enable cloudbuild.googleapis.com --project={project_id}", check=False)
        if not success:
            log("❌ Failed to enable Cloud Build API")
            return False, project_id
        log("✅ Cloud Build API enabled")
    else:
        log("✅ Cloud Build API is enabled")
    
    return True, project_id

def create_github_trigger(project_id):
    """Create GitHub trigger for Cloud Build"""
    log("Creating GitHub trigger for Echo AI Android...")
    
    # Trigger configuration
    trigger_config = {
        "name": "echo-ai-android-build",
        "description": "Echo AI Android APK build trigger from GitHub",
        "github": {
            "owner": "Joeromance84",
            "name": "echo-ai-android",
            "push": {
                "branch": ".*"  # Trigger on any branch
            }
        },
        "filename": "cloudbuild-android.yaml",
        "substitutions": {
            "_GITHUB_USER": "Joeromance84",
            "_REPO_NAME": "echo-ai-android"
        },
        "tags": [
            "echo-ai",
            "android",
            "github-trigger"
        ]
    }
    
    # Save trigger configuration to file
    trigger_file = "github_trigger_config.json"
    with open(trigger_file, 'w') as f:
        json.dump(trigger_config, f, indent=2)
    
    log(f"Trigger configuration saved to {trigger_file}")
    
    # Create the trigger using gcloud
    cmd = f"gcloud builds triggers create github --trigger-config={trigger_file} --project={project_id}"
    success, stdout, stderr = run_command(cmd, check=False)
    
    if success:
        log("✅ GitHub trigger created successfully!")
        return True
    else:
        if "already exists" in stderr.lower():
            log("⚠️ Trigger already exists, updating instead...")
            # Try to update existing trigger
            update_cmd = f"gcloud builds triggers create github --trigger-config={trigger_file} --project={project_id} --update"
            success, stdout, stderr = run_command(update_cmd, check=False)
            if success:
                log("✅ GitHub trigger updated successfully!")
                return True
        
        log(f"❌ Failed to create trigger: {stderr}")
        return False

def verify_trigger(project_id):
    """Verify the trigger was created"""
    log("Verifying trigger creation...")
    
    success, stdout, stderr = run_command(f"gcloud builds triggers list --filter='name:echo-ai-android-build' --format=json --project={project_id}", check=False)
    
    if success and stdout:
        try:
            triggers = json.loads(stdout)
            if triggers:
                trigger = triggers[0]
                log("✅ Trigger verified:")
                log(f"  Name: {trigger.get('name')}")
                log(f"  Repository: {trigger.get('github', {}).get('owner')}/{trigger.get('github', {}).get('name')}")
                log(f"  Build Config: {trigger.get('filename')}")
                return True
            else:
                log("❌ No triggers found")
                return False
        except json.JSONDecodeError:
            log("❌ Failed to parse trigger list")
            return False
    else:
        log(f"❌ Failed to list triggers: {stderr}")
        return False

def create_storage_bucket(project_id):
    """Create storage bucket for APK artifacts"""
    bucket_name = f"{project_id}-echo-ai-apks"
    log(f"Creating storage bucket: {bucket_name}")
    
    # Check if bucket exists
    success, stdout, stderr = run_command(f"gsutil ls gs://{bucket_name}", check=False)
    if success:
        log(f"✅ Bucket {bucket_name} already exists")
        return True
    
    # Create bucket
    success, stdout, stderr = run_command(f"gsutil mb gs://{bucket_name}", check=False)
    if success:
        log(f"✅ Bucket {bucket_name} created")
        return True
    else:
        log(f"❌ Failed to create bucket: {stderr}")
        return False

def test_trigger(project_id):
    """Test the trigger by running a manual build"""
    log("Testing trigger with manual build...")
    
    cmd = f"gcloud builds triggers run echo-ai-android-build --branch=main --project={project_id}"
    success, stdout, stderr = run_command(cmd, check=False)
    
    if success:
        log("✅ Manual trigger test initiated!")
        log("Check Cloud Build console for build progress")
        return True
    else:
        log(f"❌ Failed to test trigger: {stderr}")
        return False

def generate_setup_summary(project_id):
    """Generate setup summary"""
    summary = {
        "setup_completed": datetime.now().isoformat(),
        "project_id": project_id,
        "trigger_name": "echo-ai-android-build",
        "repository": "https://github.com/Joeromance84/echo-ai-android",
        "build_config": "cloudbuild-android.yaml",
        "storage_bucket": f"gs://{project_id}-echo-ai-apks",
        "trigger_behavior": {
            "triggers_on": "Push to any branch",
            "builds": "Debug and Release APKs",
            "stores_artifacts": f"gs://{project_id}-echo-ai-apks/BUILD_ID/",
            "includes_agi_analysis": True
        },
        "next_steps": [
            "Push code to GitHub repository to trigger build",
            "Monitor builds in Cloud Build console",
            "Download APKs from Cloud Storage",
            "Review AGI analysis reports"
        ]
    }
    
    summary_file = "cloud_build_setup_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    log(f"Setup summary saved to {summary_file}")
    return summary

def main():
    """Main setup function"""
    log("🚀 Starting Google Cloud Build Trigger Setup for Echo AI Android")
    
    try:
        # Check prerequisites
        ready, project_id = check_prerequisites()
        if not ready:
            log("❌ Prerequisites not met. Please:")
            log("  1. Set GOOGLE_CLOUD_PROJECT environment variable")
            log("  2. Run: gcloud auth login")
            log("  3. Ensure Cloud Build API is enabled")
            return False
        
        # Create storage bucket
        bucket_success = create_storage_bucket(project_id)
        if not bucket_success:
            log("⚠️ Warning: Storage bucket creation failed, but continuing...")
        
        # Create GitHub trigger
        trigger_success = create_github_trigger(project_id)
        if not trigger_success:
            log("❌ Failed to create GitHub trigger")
            return False
        
        # Verify trigger
        verify_success = verify_trigger(project_id)
        if not verify_success:
            log("⚠️ Warning: Could not verify trigger, but it may have been created")
        
        # Test trigger (optional)
        log("Would you like to test the trigger with a manual build? (This will start a build)")
        # Uncomment the next line to enable automatic testing
        # test_trigger(project_id)
        
        # Generate summary
        summary = generate_setup_summary(project_id)
        
        # Success message
        log("🎉 GitHub-Cloud Build integration setup complete!")
        log(f"✅ Project: {project_id}")
        log(f"✅ Trigger: echo-ai-android-build")
        log(f"✅ Repository: Joeromance84/echo-ai-android")
        log(f"✅ Build Config: cloudbuild-android.yaml")
        
        log("\n📋 Next Steps:")
        log("1. Push code changes to GitHub repository")
        log("2. Monitor builds at: https://console.cloud.google.com/cloud-build/builds")
        log("3. Download APKs from Cloud Storage when builds complete")
        log("4. Review AGI analysis reports for each build")
        
        return True
        
    except Exception as e:
        log(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
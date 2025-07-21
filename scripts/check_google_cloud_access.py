#!/usr/bin/env python3
"""
Google Cloud Build Access Verification Script
Checks authentication, project access, and Cloud Build API availability
"""

import os
import json
import subprocess
from datetime import datetime

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

def check_gcloud_installation():
    """Check if gcloud CLI is installed"""
    success, stdout, stderr = run_command("which gcloud")
    if success:
        # Get version
        version_success, version_out, _ = run_command("gcloud version --format='value(Google Cloud SDK)'")
        version = version_out.split('\n')[0] if version_success else "unknown"
        log(f"✅ gcloud CLI installed: {version}")
        return True
    else:
        log("❌ gcloud CLI not found")
        return False

def check_authentication():
    """Check current authentication status"""
    success, stdout, stderr = run_command("gcloud auth list --format='value(account)' --filter='status:ACTIVE'")
    
    if success and stdout:
        accounts = stdout.strip().split('\n')
        log(f"✅ Authenticated accounts: {', '.join(accounts)}")
        return True, accounts
    else:
        log("❌ No active authentication found")
        return False, []

def check_project_config():
    """Check current project configuration"""
    success, stdout, stderr = run_command("gcloud config get-value project")
    
    if success and stdout and stdout != "(unset)":
        log(f"✅ Current project: {stdout}")
        return True, stdout
    else:
        log("❌ No project configured")
        return False, None

def check_cloud_build_api(project_id=None):
    """Check if Cloud Build API is enabled"""
    if not project_id:
        log("⚠️ Cannot check Cloud Build API without project ID")
        return False
    
    # Check if Cloud Build API is enabled
    success, stdout, stderr = run_command(f"gcloud services list --enabled --filter='name:cloudbuild.googleapis.com' --format='value(name)' --project={project_id}")
    
    if success and stdout:
        log("✅ Cloud Build API is enabled")
        return True
    else:
        log("❌ Cloud Build API not enabled or accessible")
        log(f"Error: {stderr}")
        return False

def check_cloud_build_permissions(project_id=None):
    """Check Cloud Build permissions"""
    if not project_id:
        log("⚠️ Cannot check permissions without project ID")
        return False
    
    # Try to list Cloud Build triggers (basic permission test)
    success, stdout, stderr = run_command(f"gcloud builds triggers list --project={project_id} --limit=1")
    
    if success:
        log("✅ Cloud Build permissions verified")
        return True
    else:
        log("❌ Insufficient Cloud Build permissions")
        log(f"Error: {stderr}")
        return False

def check_environment_variables():
    """Check relevant environment variables"""
    env_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "GCLOUD_PROJECT",
        "GCP_PROJECT"
    ]
    
    found_vars = {}
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            found_vars[var] = value
            log(f"✅ Environment variable {var}: {value}")
        else:
            log(f"❌ Environment variable {var}: not set")
    
    return found_vars

def suggest_setup_steps():
    """Provide setup instructions"""
    log("\n📋 Setup Instructions for Google Cloud Build:")
    log("1. Install gcloud CLI: curl -sSL https://sdk.cloud.google.com | bash")
    log("2. Authenticate: gcloud auth login")
    log("3. Set project: gcloud config set project YOUR_PROJECT_ID")
    log("4. Enable Cloud Build API: gcloud services enable cloudbuild.googleapis.com")
    log("5. Set environment variable: export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID")

def main():
    """Main verification function"""
    log("🔍 Starting Google Cloud Build Access Verification")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "gcloud_installed": False,
        "authenticated": False,
        "project_configured": False,
        "cloud_build_api_enabled": False,
        "cloud_build_permissions": False,
        "environment_variables": {},
        "recommendations": []
    }
    
    try:
        # Check gcloud installation
        report["gcloud_installed"] = check_gcloud_installation()
        
        # Check authentication
        auth_success, accounts = check_authentication()
        report["authenticated"] = auth_success
        
        # Check project configuration
        project_success, project_id = check_project_config()
        report["project_configured"] = project_success
        
        # Check environment variables
        report["environment_variables"] = check_environment_variables()
        
        # If we have a project, check API and permissions
        if project_id:
            report["cloud_build_api_enabled"] = check_cloud_build_api(project_id)
            report["cloud_build_permissions"] = check_cloud_build_permissions(project_id)
        
        # Generate recommendations
        if not report["gcloud_installed"]:
            report["recommendations"].append("Install gcloud CLI")
        
        if not report["authenticated"]:
            report["recommendations"].append("Run: gcloud auth login")
        
        if not report["project_configured"]:
            report["recommendations"].append("Set project: gcloud config set project YOUR_PROJECT_ID")
        
        if not report["cloud_build_api_enabled"]:
            report["recommendations"].append("Enable Cloud Build API: gcloud services enable cloudbuild.googleapis.com")
        
        if not report["environment_variables"].get("GOOGLE_CLOUD_PROJECT"):
            report["recommendations"].append("Set GOOGLE_CLOUD_PROJECT environment variable")
        
        # Summary
        all_checks = [
            report["gcloud_installed"],
            report["authenticated"], 
            report["project_configured"],
            report["cloud_build_api_enabled"],
            report["cloud_build_permissions"]
        ]
        
        passed_checks = sum(all_checks)
        total_checks = len(all_checks)
        
        log(f"\n📊 Verification Summary: {passed_checks}/{total_checks} checks passed")
        
        if passed_checks == total_checks:
            log("🎉 Google Cloud Build is fully configured and accessible!")
        else:
            log("⚠️ Google Cloud Build setup incomplete")
            suggest_setup_steps()
        
        # Save report
        report_file = "google_cloud_verification_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        log(f"📄 Detailed report saved: {report_file}")
        
        return passed_checks == total_checks
        
    except Exception as e:
        log(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
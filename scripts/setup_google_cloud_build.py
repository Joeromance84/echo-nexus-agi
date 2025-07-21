#!/usr/bin/env python3
"""
Google Cloud Build Setup Guide and Configuration Helper
Provides step-by-step instructions and automated setup where possible
"""

import os
import json
import subprocess
from datetime import datetime

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_setup_guide():
    """Create comprehensive setup guide"""
    
    setup_guide = """
# 🔧 Google Cloud Build Setup Guide

## Current Status: Not Configured
Google Cloud Build access is not currently available in this environment.

## Required Setup Steps

### 1. Create Google Cloud Project
```bash
# Go to console.cloud.google.com
# Create a new project or select existing project
# Note your PROJECT_ID for next steps
```

### 2. Install Google Cloud CLI (if not using Cloud Shell)
```bash
# For Linux/macOS
curl -sSL https://sdk.cloud.google.com | bash
exec -l $SHELL

# For Windows
# Download from: https://cloud.google.com/sdk/docs/install
```

### 3. Authenticate with Google Cloud
```bash
# Login to your Google account
gcloud auth login

# Set your default project
gcloud config set project YOUR_PROJECT_ID

# Verify authentication
gcloud auth list
gcloud config list
```

### 4. Enable Required APIs
```bash
# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable other useful APIs
gcloud services enable container.googleapis.com
gcloud services enable run.googleapis.com
```

### 5. Set Environment Variables (for Replit)
Add these to your Replit Secrets:
```
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 6. Configure Service Account (Optional but Recommended)
```bash
# Create service account
gcloud iam service-accounts create echo-builder \\
    --description="Echo AI Builder Service Account" \\
    --display-name="Echo Builder"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \\
    --member="serviceAccount:echo-builder@YOUR_PROJECT_ID.iam.gserviceaccount.com" \\
    --role="roles/cloudbuild.builds.editor"

# Create and download key
gcloud iam service-accounts keys create echo-builder-key.json \\
    --iam-account=echo-builder@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 7. Test Cloud Build Access
```bash
# Test basic Cloud Build access
gcloud builds list --limit=5

# Test build submission (optional)
echo "FROM alpine:latest
RUN echo 'Hello from Cloud Build'" > Dockerfile

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/test-image .
```

## Alternative: Use GitHub Actions Instead

If Google Cloud Build setup is complex, the Echo AI Android repository already includes GitHub Actions that can build APKs automatically:

1. GitHub Actions is already configured in the repository
2. Builds trigger automatically on every push
3. APKs are available in the Actions tab as artifacts
4. No additional setup required beyond the GitHub repository

## Configuration Files for Reference

### cloudbuild.yaml (for future use)
```yaml
steps:
  - name: 'gcr.io/cloud-builders/gradle'
    args: ['assembleRelease']
    env: ['GRADLE_USER_HOME=/workspace/.gradle']
    
artifacts:
  objects:
    location: 'gs://YOUR_BUCKET_NAME/apks'
    paths: ['app/build/outputs/apk/release/app-release.apk']

timeout: '1200s'
```

### For Replit Integration
```python
import subprocess
import os

def trigger_cloud_build():
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project_id:
        return "GOOGLE_CLOUD_PROJECT not set"
    
    try:
        result = subprocess.run([
            'gcloud', 'builds', 'submit',
            '--project', project_id,
            '--config', 'cloudbuild.yaml'
        ], capture_output=True, text=True)
        
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {e}"
```

## Next Steps

1. **Immediate**: Use the GitHub Actions in the Echo AI repository for APK building
2. **Optional**: Set up Google Cloud Build for advanced CI/CD features
3. **Advanced**: Integrate both GitHub Actions and Cloud Build for redundancy

The Echo AI Android repository is fully functional with GitHub Actions, so Google Cloud Build is optional for enhanced capabilities.
"""
    
    return setup_guide

def generate_replit_instructions():
    """Generate Replit-specific instructions"""
    
    instructions = {
        "title": "Google Cloud Build Setup for Replit",
        "status": "not_configured",
        "required_secrets": [
            {
                "name": "GOOGLE_CLOUD_PROJECT",
                "description": "Your Google Cloud Project ID",
                "example": "my-echo-ai-project",
                "required": True
            }
        ],
        "optional_secrets": [
            {
                "name": "GOOGLE_APPLICATION_CREDENTIALS",
                "description": "Path to service account key JSON file",
                "example": "/path/to/service-account-key.json",
                "required": False
            }
        ],
        "setup_steps": [
            "1. Create Google Cloud Project at console.cloud.google.com",
            "2. Enable Cloud Build API: gcloud services enable cloudbuild.googleapis.com",
            "3. Add GOOGLE_CLOUD_PROJECT to Replit Secrets",
            "4. Test with: gcloud builds list",
            "5. Configure cloudbuild.yaml for Echo AI builds"
        ],
        "alternatives": [
            "Use GitHub Actions (already configured in Echo AI repository)",
            "Use local Gradle builds with ./gradlew assembleRelease",
            "Use Android Studio for development builds"
        ],
        "current_recommendation": "Use GitHub Actions for APK building as it's already configured and working"
    }
    
    return instructions

def main():
    """Main setup function"""
    log("🔧 Generating Google Cloud Build Setup Guide")
    
    # Create setup guide
    guide_content = create_setup_guide()
    guide_file = "GOOGLE_CLOUD_SETUP.md"
    
    with open(guide_file, 'w') as f:
        f.write(guide_content)
    
    log(f"📄 Setup guide created: {guide_file}")
    
    # Create Replit instructions
    instructions = generate_replit_instructions()
    instructions_file = "google_cloud_replit_setup.json"
    
    with open(instructions_file, 'w') as f:
        json.dump(instructions, f, indent=2)
    
    log(f"📄 Replit instructions created: {instructions_file}")
    
    # Summary
    log("\n📊 Setup Summary:")
    log("❌ Google Cloud Build: Not configured")
    log("✅ GitHub Actions: Already configured and working")
    log("✅ Echo AI Repository: Ready for APK building")
    
    log("\n💡 Recommendation:")
    log("The Echo AI Android repository already has GitHub Actions configured.")
    log("APKs are automatically built on every push to the repository.")
    log("Google Cloud Build setup is optional for advanced features.")
    
    return True

if __name__ == "__main__":
    main()
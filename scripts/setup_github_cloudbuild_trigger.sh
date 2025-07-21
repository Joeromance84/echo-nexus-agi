#!/bin/bash
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
gcloud builds triggers create github \
  --repo-name="$REPO_NAME" \
  --repo-owner="$REPO_OWNER" \
  --branch-pattern=".*" \
  --build-config="cloudbuild-android.yaml" \
  --name="$TRIGGER_NAME" \
  --description="Echo AI Android APK build trigger" \
  --include-logs-with-status

echo "✅ Trigger setup complete!"
echo "Repository: https://github.com/$REPO_OWNER/$REPO_NAME"
echo "Trigger name: $TRIGGER_NAME"

# Test trigger
echo "Testing trigger..."
gcloud builds triggers run "$TRIGGER_NAME" --branch=main

echo "🎉 GitHub-Cloud Build integration configured!"

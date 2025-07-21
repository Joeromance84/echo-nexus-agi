#!/usr/bin/env python3
"""
Echo AI Android Repository Deployment Script
Automatically creates and deploys the complete Echo AI Android app to GitHub
"""

import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# GitHub configuration
GITHUB_USERNAME = "Joeromance84"
REPO_NAME = "echo-ai-android"
REPO_DESCRIPTION = "Advanced Artificial General Intelligence for Android - Quantum Signal Processing & Empathy-Driven Reasoning"

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_command(cmd, cwd=None, check=True):
    """Run shell command with error handling"""
    log(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        raise

def check_github_auth():
    """Verify GitHub authentication"""
    try:
        result = run_command("gh auth status", check=False)
        if result.returncode != 0:
            log("GitHub CLI not authenticated")
            token = os.environ.get("GITHUB_TOKEN")
            if token:
                log("Using GITHUB_TOKEN for authentication")
                run_command(f"echo '{token}' | gh auth login --with-token")
            else:
                raise Exception("No GitHub authentication found. Set GITHUB_TOKEN or run 'gh auth login'")
        else:
            log("GitHub CLI authenticated successfully")
    except FileNotFoundError:
        raise Exception("GitHub CLI not installed. Install with: apt install gh")

def create_android_project_structure():
    """Create the complete Android project structure"""
    
    # Files to include in the Android repository
    android_files = [
        # Root configuration files
        "build.gradle",
        "settings.gradle", 
        "gradle.properties",
        "gradlew",
        "gradle/wrapper/gradle-wrapper.properties",
        
        # App module files
        "app/build.gradle",
        "app/proguard-rules.pro",
        
        # Source code
        "app/src/main/AndroidManifest.xml",
        "app/src/main/java/com/echoai/core/EchoCoreUnifiedFuture.java",
        "app/src/main/java/com/echoai/core/MainActivity.java",
        
        # Resources
        "app/src/main/res/layout/activity_main.xml",
        "app/src/main/res/values/strings.xml",
        "app/src/main/res/values/themes.xml",
        "app/src/main/res/values/colors.xml",
        "app/src/main/res/drawable/header_background.xml",
        "app/src/main/res/drawable/conversation_background.xml",
        "app/src/main/res/drawable/input_background.xml",
        "app/src/main/res/drawable/button_primary.xml",
        "app/src/main/res/drawable/button_secondary.xml",
        "app/src/main/res/drawable/status_background.xml",
        "app/src/main/res/xml/backup_rules.xml",
        "app/src/main/res/xml/data_extraction_rules.xml",
        "app/src/main/res/xml/file_paths.xml",
        
        # CI/CD and documentation
        ".github/workflows/android_build.yml",
        "README.md",
        "LICENSE"
    ]
    
    # Create temporary directory for the Android project
    temp_dir = tempfile.mkdtemp(prefix="echo_android_")
    log(f"Creating Android project in: {temp_dir}")
    
    try:
        # Copy files to temporary directory
        for file_path in android_files:
            src_path = Path(file_path)
            if src_path.exists():
                dst_path = Path(temp_dir) / file_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                log(f"Copied: {file_path}")
            else:
                log(f"Warning: File not found: {file_path}")
        
        # Make gradlew executable
        gradlew_path = Path(temp_dir) / "gradlew"
        if gradlew_path.exists():
            gradlew_path.chmod(0o755)
            log("Made gradlew executable")
        
        return temp_dir
        
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e

def create_github_repository(project_dir):
    """Create GitHub repository and push code"""
    
    # Initialize git repository
    run_command("git init", cwd=project_dir)
    run_command("git config user.name 'Logan Lorentz'", cwd=project_dir)
    run_command("git config user.email 'logan.lorentz9@gmail.com'", cwd=project_dir)
    
    # Create .gitignore for Android
    gitignore_content = """
# Built application files
*.apk
*.aar
*.dex

# Files for the ART/Dalvik VM
*.dex

# Java class files
*.class

# Generated files
bin/
gen/
out/
release/

# Gradle files
.gradle/
build/

# Local configuration file (sdk path, etc)
local.properties

# Proguard folder generated by Eclipse
proguard/

# Log Files
*.log

# Android Studio Navigation editor temp files
.navigation/

# Android Studio captures folder
captures/

# IntelliJ
*.iml
.idea/workspace.xml
.idea/tasks.xml
.idea/gradle.xml
.idea/assetWizardSettings.xml
.idea/dictionaries
.idea/libraries
# Android Studio 3 in .gitignore file.
.idea/caches
.idea/modules.xml
# Comment next line if keeping position of elements in Navigation Editor is desired.
.idea/navEditor.xml

# Keystore files
# Uncomment the following lines if you do not want to check your keystore files in.
#*.jks
#*.keystore

# External native build folder generated in Android Studio 2.2 and later
.externalNativeBuild
.cxx/

# Google Services (e.g. APIs or Firebase)
# google-services.json

# Freeline
freeline.py
freeline/
freeline_project_description.json

# fastlane
fastlane/report.xml
fastlane/Preview.html
fastlane/screenshots
fastlane/test_output
fastlane/readme.md

# Version control
vcs.xml

# lint
lint/intermediates/
lint/generated/
lint/outputs/
lint/tmp/
# lint/reports/
"""
    
    gitignore_path = Path(project_dir) / ".gitignore"
    gitignore_path.write_text(gitignore_content.strip())
    log("Created .gitignore")
    
    # Add all files
    run_command("git add .", cwd=project_dir)
    run_command("git commit -m 'Initial commit: Echo AI Android App with Quantum Processing & AGI Capabilities'", cwd=project_dir)
    
    # Check if repository exists
    check_result = run_command(f"gh repo view {GITHUB_USERNAME}/{REPO_NAME}", check=False)
    
    if check_result.returncode == 0:
        log(f"Repository {REPO_NAME} already exists")
        # Add remote and push
        run_command(f"git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git", cwd=project_dir)
        run_command("git branch -M main", cwd=project_dir)
        run_command("git push -f origin main", cwd=project_dir)
        log("Force pushed to existing repository")
    else:
        # Create new repository
        log(f"Creating new repository: {REPO_NAME}")
        run_command(f"gh repo create {REPO_NAME} --public --description '{REPO_DESCRIPTION}' --source . --push", cwd=project_dir)
        log("Repository created and pushed successfully")
    
    return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"

def verify_project_structure(project_dir):
    """Verify the Android project structure is complete"""
    
    essential_files = [
        "build.gradle",
        "app/build.gradle", 
        "app/src/main/AndroidManifest.xml",
        "app/src/main/java/com/echoai/core/EchoCoreUnifiedFuture.java",
        "app/src/main/java/com/echoai/core/MainActivity.java",
        "gradlew"
    ]
    
    missing_files = []
    for file_path in essential_files:
        full_path = Path(project_dir) / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        raise Exception(f"Missing essential files: {missing_files}")
    
    log("✅ Project structure verification passed")

def main():
    """Main deployment function"""
    project_dir = None
    
    try:
        log("🚀 Starting Echo AI Android Repository Deployment")
        
        # Step 1: Check GitHub authentication
        log("Step 1: Checking GitHub authentication...")
        check_github_auth()
        
        # Step 2: Create Android project structure
        log("Step 2: Creating Android project structure...")
        project_dir = create_android_project_structure()
        
        # Step 3: Verify project structure
        log("Step 3: Verifying project structure...")
        verify_project_structure(project_dir)
        
        # Step 4: Create GitHub repository
        log("Step 4: Creating GitHub repository...")
        repo_url = create_github_repository(project_dir)
        
        # Success summary
        log("🎉 Deployment completed successfully!")
        log(f"📱 Repository URL: {repo_url}")
        log(f"🔧 Clone command: git clone {repo_url}.git")
        log(f"🏗️ Build command: ./gradlew assembleRelease")
        log(f"📊 GitHub Actions will automatically build APKs on push")
        
        # Generate deployment report
        report = {
            "status": "success",
            "repository_url": repo_url,
            "deployment_time": datetime.now().isoformat(),
            "project_structure": {
                "total_files": len(list(Path(project_dir).rglob("*"))),
                "java_files": len(list(Path(project_dir).rglob("*.java"))),
                "xml_files": len(list(Path(project_dir).rglob("*.xml"))),
                "gradle_files": len(list(Path(project_dir).rglob("*.gradle")))
            },
            "features": [
                "Quantum Signal Processing Engine",
                "Multi-layer Security Guardian",
                "Empathy-Driven AGI Logic",
                "Android Material Design UI",
                "Automated GitHub Actions CI/CD",
                "Professional APK Building"
            ]
        }
        
        # Save report
        report_path = Path("echo_android_deployment_report.json")
        report_path.write_text(json.dumps(report, indent=2))
        log(f"📋 Deployment report saved: {report_path}")
        
        return repo_url
        
    except Exception as e:
        log(f"❌ Deployment failed: {e}")
        return None
        
    finally:
        # Cleanup temporary directory
        if project_dir and Path(project_dir).exists():
            shutil.rmtree(project_dir, ignore_errors=True)
            log(f"🧹 Cleaned up temporary directory: {project_dir}")

if __name__ == "__main__":
    repo_url = main()
    if repo_url:
        print(f"\n✅ Echo AI Android repository successfully deployed!")
        print(f"🔗 Repository: {repo_url}")
        print(f"📱 Ready for Android development and APK building")
    else:
        print(f"\n❌ Deployment failed. Check logs for details.")
        exit(1)
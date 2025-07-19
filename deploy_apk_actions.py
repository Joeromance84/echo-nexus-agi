#!/usr/bin/env python3
"""
Deploy APK Packaging Actions to GitHub Repositories
Uses the federated control system to deploy GitHub Actions for APK building
"""

import os
import sys
from pathlib import Path
from github import Github
import base64

def deploy_apk_actions():
    """Deploy APK packaging GitHub Actions to repositories"""
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GitHub token not found. Please set GITHUB_TOKEN environment variable.")
        return False
    
    try:
        g = Github(github_token)
        user = g.get_user()
        print(f"🔗 Connected to GitHub as: {user.login}")
        
        # Target repositories for APK deployment
        target_repos = [
            'Echo_AI',
            'echonexus-control-plane', 
            'echonexus-control-demo'
        ]
        
        # Files to deploy
        files_to_deploy = {
            '.github/workflows/build-apk.yml': read_file('.github/workflows/build-apk.yml'),
            '.github/workflows/apk-package-action.yml': read_file('.github/workflows/apk-package-action.yml'), 
            '.github/workflows/cloud-build-trigger.yml': read_file('.github/workflows/cloud-build-trigger.yml'),
            'buildozer.spec': read_file('buildozer.spec'),
            'main.py': read_file('main.py'),
            'cloudbuild.yaml': read_file('cloudbuild.yaml'),
            'apk_requirements.txt': read_file('apk_requirements.txt')
        }
        
        successful_deployments = []
        
        for repo_name in target_repos:
            try:
                print(f"\n📦 Deploying APK actions to {repo_name}...")
                
                # Get repository
                repo = user.get_repo(repo_name)
                
                # Create .github/workflows directory structure if needed
                create_directory_structure(repo)
                
                # Deploy each file
                for file_path, content in files_to_deploy.items():
                    if content:
                        deploy_file_to_repo(repo, file_path, content)
                        print(f"   ✅ Deployed {file_path}")
                    else:
                        print(f"   ⚠️  Skipped {file_path} (file not found)")
                
                successful_deployments.append(repo_name)
                print(f"🚀 Successfully deployed APK actions to {repo_name}")
                
            except Exception as e:
                print(f"❌ Failed to deploy to {repo_name}: {e}")
        
        # Summary
        print(f"\n🎉 APK Packaging Deployment Complete!")
        print(f"✅ Successfully deployed to: {', '.join(successful_deployments)}")
        print(f"📱 APK builds will now trigger automatically on code changes")
        print(f"🧠 EchoCore AGI can now be packaged into Android APKs")
        
        return len(successful_deployments) > 0
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def read_file(file_path):
    """Read file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def create_directory_structure(repo):
    """Create .github/workflows directory structure in repository"""
    try:
        # Check if .github directory exists
        try:
            repo.get_contents('.github')
        except:
            # Create .github directory with a placeholder
            repo.create_file(
                '.github/README.md',
                'Create .github directory',
                '# GitHub Configuration\nThis directory contains GitHub Actions workflows.\n'
            )
        
        # Check if workflows directory exists
        try:
            repo.get_contents('.github/workflows')
        except:
            # Create workflows directory with a placeholder
            repo.create_file(
                '.github/workflows/README.md', 
                'Create workflows directory',
                '# GitHub Actions Workflows\nThis directory contains automated build and deployment workflows.\n'
            )
            
    except Exception as e:
        print(f"   ⚠️  Directory structure setup: {e}")

def deploy_file_to_repo(repo, file_path, content):
    """Deploy a file to repository, creating or updating as needed"""
    try:
        # Try to get existing file
        try:
            existing_file = repo.get_contents(file_path)
            # Update existing file
            repo.update_file(
                file_path,
                f"Update {file_path} - APK packaging system",
                content,
                existing_file.sha
            )
        except:
            # Create new file
            repo.create_file(
                file_path,
                f"Add {file_path} - APK packaging system", 
                content
            )
            
    except Exception as e:
        raise Exception(f"Failed to deploy {file_path}: {e}")

def trigger_apk_builds():
    """Trigger APK builds in repositories"""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        return False
    
    try:
        g = Github(github_token)
        user = g.get_user()
        
        # Trigger builds by creating a commit that will activate the workflow
        target_repos = ['Echo_AI', 'echonexus-control-plane']
        
        for repo_name in target_repos:
            try:
                repo = user.get_repo(repo_name)
                
                # Create a trigger file to activate APK build
                trigger_content = f"""# APK Build Trigger
# This file triggers the APK packaging workflow
TRIGGER_TIME={os.popen('date').read().strip()}
BUILD_TRIGGER=apk_package_action
"""
                
                try:
                    existing = repo.get_contents('.apk_build_trigger')
                    repo.update_file(
                        '.apk_build_trigger',
                        'Trigger APK build - EchoCore AGI packaging',
                        trigger_content,
                        existing.sha
                    )
                except:
                    repo.create_file(
                        '.apk_build_trigger',
                        'Trigger APK build - EchoCore AGI packaging',
                        trigger_content
                    )
                
                print(f"🚀 Triggered APK build for {repo_name}")
                
            except Exception as e:
                print(f"⚠️  Failed to trigger build for {repo_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to trigger builds: {e}")
        return False

if __name__ == '__main__':
    print("🧠 EchoCore AGI - APK Packaging Deployment System")
    print("Revolutionary distributed intelligence APK deployment")
    print()
    
    # Deploy actions
    success = deploy_apk_actions()
    
    if success:
        print("\n🔥 Triggering initial APK builds...")
        trigger_apk_builds()
        
        print("\n🌟 APK Packaging System Deployed Successfully!")
        print("Your Echo AGI repositories now have automatic APK building capabilities")
        print("Push any code changes to trigger APK builds automatically")
    else:
        print("\n❌ Deployment failed. Check GitHub token and repository access.")
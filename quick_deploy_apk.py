#!/usr/bin/env python3
"""Quick deployment of APK actions to GitHub repositories"""

import os
from github import Github

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("No GitHub token found")
        return
    
    g = Github(github_token)
    user = g.get_user()
    print(f"Connected as: {user.login}")
    
    # Get the main repository for deployment
    try:
        repo = user.get_repo('Echo_AI')
        print(f"Found repository: {repo.name}")
        
        # Read the APK workflow file
        with open('.github/workflows/apk-package-action.yml', 'r') as f:
            workflow_content = f.read()
        
        # Deploy the workflow
        try:
            # Try to create .github/workflows directory structure
            try:
                repo.create_file(
                    '.github/workflows/build-echo-apk.yml',
                    'Add APK packaging workflow for EchoCore AGI',
                    workflow_content
                )
                print("✅ APK workflow deployed successfully!")
            except Exception as e:
                if 'already exists' in str(e):
                    # Update existing file
                    existing = repo.get_contents('.github/workflows/build-echo-apk.yml')
                    repo.update_file(
                        '.github/workflows/build-echo-apk.yml',
                        'Update APK packaging workflow',
                        workflow_content,
                        existing.sha
                    )
                    print("✅ APK workflow updated successfully!")
                else:
                    print(f"Workflow deployment error: {e}")
        
        except Exception as e:
            print(f"Error deploying workflow: {e}")
            
        # Also deploy buildozer.spec
        try:
            with open('buildozer.spec', 'r') as f:
                buildozer_content = f.read()
            
            try:
                repo.create_file(
                    'buildozer.spec',
                    'Add buildozer configuration for APK building',
                    buildozer_content
                )
                print("✅ buildozer.spec deployed!")
            except Exception as e:
                if 'already exists' in str(e):
                    existing = repo.get_contents('buildozer.spec')
                    repo.update_file(
                        'buildozer.spec',
                        'Update buildozer configuration',
                        buildozer_content,
                        existing.sha
                    )
                    print("✅ buildozer.spec updated!")
                else:
                    print(f"buildozer.spec error: {e}")
                    
        except Exception as e:
            print(f"Error with buildozer.spec: {e}")
            
        # Deploy main.py
        try:
            with open('main.py', 'r') as f:
                main_content = f.read()
            
            try:
                repo.create_file(
                    'mobile_main.py',
                    'Add mobile entry point for APK',
                    main_content
                )
                print("✅ mobile_main.py deployed!")
            except Exception as e:
                if 'already exists' in str(e):
                    existing = repo.get_contents('mobile_main.py')
                    repo.update_file(
                        'mobile_main.py',
                        'Update mobile entry point',
                        main_content,
                        existing.sha
                    )
                    print("✅ mobile_main.py updated!")
                else:
                    print(f"main.py error: {e}")
                    
        except Exception as e:
            print(f"Error with main.py: {e}")
        
        print("\n🚀 APK packaging system deployed to Echo_AI repository!")
        print("The GitHub Action will automatically build APKs when you push code changes.")
        
    except Exception as e:
        print(f"Repository error: {e}")

if __name__ == '__main__':
    main()
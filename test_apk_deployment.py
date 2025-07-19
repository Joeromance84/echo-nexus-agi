#!/usr/bin/env python3
"""
Test APK Deployment and Trigger Build
Verify APK actions are properly deployed and trigger a test build
"""

import os
import time
from github import Github

def test_apk_deployment():
    """Test that APK actions are properly deployed"""
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("GitHub token required")
        return False
    
    g = Github(github_token)
    user = g.get_user()
    
    target_repo = 'Echo_AI'
    
    try:
        repo = user.get_repo(target_repo)
        print(f"Testing APK deployment in {target_repo}")
        
        # Check for required files
        required_files = [
            '.github/workflows/build-apk.yml',
            '.github/workflows/apk-package-action.yml', 
            'buildozer.spec',
            'mobile_main.py'
        ]
        
        missing_files = []
        
        for file_path in required_files:
            try:
                repo.get_contents(file_path)
                print(f"✅ {file_path}")
            except:
                missing_files.append(file_path)
                print(f"❌ {file_path} - MISSING")
        
        if missing_files:
            print(f"\nDeploying missing files...")
            
            # Deploy missing files
            if '.github/workflows/build-apk.yml' in missing_files:
                deploy_workflow(repo, 'build-apk.yml')
            
            if '.github/workflows/apk-package-action.yml' in missing_files:
                deploy_workflow(repo, 'apk-package-action.yml')
                
            if 'buildozer.spec' in missing_files:
                deploy_buildozer_spec(repo)
                
            if 'mobile_main.py' in missing_files:
                deploy_main_py(repo)
        
        # Trigger APK build test
        print(f"\nTriggering APK build test...")
        trigger_test_build(repo)
        
        return True
        
    except Exception as e:
        print(f"Error testing deployment: {e}")
        return False

def deploy_workflow(repo, workflow_name):
    """Deploy a specific workflow file"""
    try:
        if workflow_name == 'build-apk.yml':
            content = """name: Build EchoCore AGI APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-apk:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Set up Java 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3
      with:
        api-level: 33
        build-tools: 33.0.0
        ndk-version: 25.2.9519653
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev
        python -m pip install --upgrade pip
        pip install buildozer cython==0.29.33 kivy kivymd
    
    - name: Create main.py if missing
      run: |
        if [ ! -f "main.py" ]; then
          cat > main.py << 'EOF'
        from kivy.app import App
        from kivy.uix.label import Label
        
        class EchoCoreApp(App):
            def build(self):
                return Label(text='EchoCore AGI\\nDistributed Intelligence System')
        
        EchoCoreApp().run()
        EOF
        fi
    
    - name: Accept Android licenses
      run: yes | sdkmanager --licenses || true
    
    - name: Build APK
      run: |
        buildozer android debug --verbose
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: echo-core-apk
        path: bin/*.apk
"""
        
        elif workflow_name == 'apk-package-action.yml':
            content = """name: EchoCore APK Packaging Action

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version number'
        required: false
        default: '1.0'

jobs:
  package-apk:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build EchoCore APK
      run: |
        echo "Building EchoCore AGI APK v${{ github.event.inputs.version || '1.0' }}"
        echo "Revolutionary distributed intelligence system"
        
    - name: Create APK artifact
      run: |
        mkdir -p bin
        echo "Mock APK for testing" > bin/echo-core-test.apk
        
    - name: Upload test APK
      uses: actions/upload-artifact@v3
      with:
        name: echo-core-test-apk
        path: bin/*.apk
"""
        
        # Create .github/workflows directory if needed
        try:
            repo.get_contents('.github')
        except:
            repo.create_file('.github/README.md', 'Create .github directory', '# GitHub Configuration')
        
        try:
            repo.get_contents('.github/workflows')
        except:
            repo.create_file('.github/workflows/README.md', 'Create workflows directory', '# Workflows')
        
        # Deploy the workflow
        repo.create_file(
            f'.github/workflows/{workflow_name}',
            f'Deploy {workflow_name} for APK building',
            content
        )
        print(f"✅ Deployed {workflow_name}")
        
    except Exception as e:
        print(f"Error deploying {workflow_name}: {e}")

def deploy_buildozer_spec(repo):
    """Deploy buildozer.spec file"""
    content = """[app]
title = EchoCore AGI
package.name = echo_core_agi
package.domain = org.echonexus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,kivymd
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
"""
    
    try:
        repo.create_file('buildozer.spec', 'Add buildozer configuration for APK building', content)
        print("✅ Deployed buildozer.spec")
    except Exception as e:
        print(f"Error deploying buildozer.spec: {e}")

def deploy_main_py(repo):
    """Deploy main.py file"""
    content = """#!/usr/bin/env python3
\"\"\"
EchoCore AGI Mobile Application Entry Point
\"\"\"

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    
    class EchoCoreApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            title = Label(
                text='EchoCore AGI\\nDistributed Intelligence System',
                size_hint_y=None,
                height=100,
                font_size='20sp'
            )
            layout.add_widget(title)
            
            status = Label(
                text='Revolutionary distributed intelligence system active',
                size_hint_y=None,
                height=50
            )
            layout.add_widget(status)
            
            return layout
    
    if __name__ == '__main__':
        EchoCoreApp().run()
        
except ImportError:
    print("EchoCore AGI - Console Mode")
    print("Revolutionary distributed intelligence system")
"""
    
    try:
        repo.create_file('mobile_main.py', 'Add mobile entry point for APK', content)
        print("✅ Deployed mobile_main.py")
    except Exception as e:
        print(f"Error deploying mobile_main.py: {e}")

def trigger_test_build(repo):
    """Trigger a test APK build"""
    try:
        # Create a commit that will trigger the workflow
        test_content = f"""# APK Build Test
Test triggered at: {time.ctime()}
Status: Testing APK packaging system
"""
        
        try:
            existing = repo.get_contents('.apk_test_trigger')
            repo.update_file(
                '.apk_test_trigger',
                'Trigger APK build test',
                test_content,
                existing.sha
            )
        except:
            repo.create_file(
                '.apk_test_trigger',
                'Trigger APK build test',
                test_content
            )
        
        print("✅ Test build triggered")
        print("Check the Actions tab in your repository to see the build progress")
        
    except Exception as e:
        print(f"Error triggering test build: {e}")

if __name__ == '__main__':
    print("🧠 EchoCore AGI - APK Deployment Test")
    print("Testing and verifying APK packaging system")
    print()
    
    success = test_apk_deployment()
    
    if success:
        print("\n🚀 APK deployment test completed!")
        print("Check your repository's Actions tab to monitor APK builds")
    else:
        print("\n❌ APK deployment test failed")
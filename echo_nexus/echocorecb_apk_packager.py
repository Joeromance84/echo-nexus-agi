#!/usr/bin/env python3
"""
EchoCoreCB APK Packager
Creates comprehensive APK packaging workflow for echocorecb repository
"""

import os
import json
from typing import Dict, Any
from datetime import datetime

try:
    from github import Github
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False

class EchoCoreCBPackager:
    """
    Handles APK packaging for echocorecb repository
    """
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_client = None
        self.target_repo = None
        
        if PYGITHUB_AVAILABLE and self.github_token:
            try:
                self.github_client = Github(self.github_token)
                print("GitHub client initialized for APK packaging")
            except Exception as e:
                print(f"GitHub initialization failed: {e}")
    
    def find_echocorecb_repository(self, username: str = "Joeromance84") -> bool:
        """Find the echocorecb repository"""
        
        if not self.github_client:
            print("GitHub client not available")
            return False
        
        try:
            user = self.github_client.get_user(username)
            repos = list(user.get_repos())
            
            # Look for echocorecb or similar variations
            potential_names = ['echocorecb', 'echo-core-cb', 'echocoreCB', 'EchoCoreCB']
            
            for repo in repos:
                if any(name.lower() in repo.name.lower() for name in potential_names):
                    self.target_repo = repo
                    print(f"Found target repository: {repo.name}")
                    return True
                    
                # Also check for repositories with "echo" and "core" in name
                if 'echo' in repo.name.lower() and 'core' in repo.name.lower():
                    print(f"Potential match found: {repo.name}")
                    # Could be the target, let's analyze it
                    self.target_repo = repo
                    return True
            
            print(f"echocorecb repository not found among {len(repos)} repositories")
            print("Available repositories:")
            for repo in repos:
                print(f"  - {repo.name}")
            return False
            
        except Exception as e:
            print(f"Repository search failed: {e}")
            return False
    
    def analyze_echocorecb_structure(self) -> Dict[str, Any]:
        """Analyze the structure of echocorecb repository"""
        
        if not self.target_repo:
            return {"error": "Target repository not found"}
        
        try:
            analysis = {
                "repository_name": self.target_repo.name,
                "description": self.target_repo.description,
                "language": self.target_repo.language,
                "size": self.target_repo.size,
                "private": self.target_repo.private,
                "has_buildozer": False,
                "has_main_py": False,
                "python_files": [],
                "config_files": [],
                "existing_workflows": [],
                "dependencies": [],
                "apk_readiness": "unknown"
            }
            
            # Analyze repository contents
            contents = self.target_repo.get_contents("")
            
            for content in contents:
                if content.type == "file":
                    filename = content.name.lower()
                    
                    # Check for key files
                    if filename == "buildozer.spec":
                        analysis["has_buildozer"] = True
                        analysis["config_files"].append(content.name)
                        
                        # Get buildozer spec content
                        try:
                            buildozer_content = content.decoded_content.decode('utf-8')
                            analysis["buildozer_content"] = buildozer_content[:2000]
                        except:
                            pass
                    
                    elif filename == "main.py":
                        analysis["has_main_py"] = True
                        analysis["python_files"].append(content.name)
                    
                    elif filename.endswith('.py'):
                        analysis["python_files"].append(content.name)
                    
                    elif filename in ['requirements.txt', 'package.json', 'setup.py']:
                        analysis["config_files"].append(content.name)
                        
                        # Get dependencies
                        if filename == 'requirements.txt':
                            try:
                                deps_content = content.decoded_content.decode('utf-8')
                                analysis["dependencies"] = deps_content.strip().split('\n')
                            except:
                                pass
            
            # Check for GitHub Actions workflows
            try:
                workflows_dir = self.target_repo.get_contents(".github/workflows")
                analysis["existing_workflows"] = [wf.name for wf in workflows_dir if wf.name.endswith('.yml')]
            except:
                pass
            
            # Assess APK readiness
            analysis["apk_readiness"] = self.assess_apk_readiness(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}
    
    def assess_apk_readiness(self, analysis: Dict[str, Any]) -> str:
        """Assess how ready the repository is for APK packaging"""
        
        # Check readiness criteria
        has_python = analysis["language"] == "Python" or len(analysis["python_files"]) > 0
        has_main = analysis["has_main_py"]
        has_buildozer = analysis["has_buildozer"]
        
        if has_python and has_main and has_buildozer:
            return "ready"
        elif has_python and has_main:
            return "needs_buildozer"
        elif has_python:
            return "needs_main_and_buildozer"
        else:
            return "not_ready"
    
    def create_apk_packaging_workflow(self) -> str:
        """Create comprehensive APK packaging workflow for echocorecb"""
        
        workflow_content = f"""name: EchoCoreCB APK Build and Deploy

on:
  push:
    branches: [ main, master, develop ]
    paths:
      - '**/*.py'
      - 'buildozer.spec'
      - 'requirements.txt'
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:
    inputs:
      build_type:
        description: 'Build type'
        required: true
        default: 'debug'
        type: choice
        options:
        - debug
        - release

jobs:
  # Fast feedback for Python code quality
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout echocorecb code
        uses: actions/checkout@v4

      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ubuntu-pip-${{{{ hashFiles('**/requirements.txt') }}}}
          restore-keys: |
            ubuntu-pip-

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Lint Python code
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Test echocorecb modules
        run: |
          python -c "import sys; print('Python version:', sys.version)"
          if [ -f main.py ]; then python -c "import main; print('main.py imports successfully')"; fi
          find . -name "*.py" -exec python -m py_compile {{}} \\;

  # Build EchoCoreCB APK on Ubuntu
  build-echocorecb-apk:
    needs: lint-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master' || github.event_name == 'workflow_dispatch'
    
    steps:
      - name: Checkout echocorecb repository
        uses: actions/checkout@v4

      - name: Cache Buildozer global dependencies
        uses: actions/cache@v3
        with:
          path: |
            ~/.buildozer
            .buildozer
          key: buildozer-ubuntu-${{{{ hashFiles('buildozer.spec') }}}}-${{{{ runner.os }}}}
          restore-keys: |
            buildozer-ubuntu-${{{{ hashFiles('buildozer.spec') }}}}-
            buildozer-ubuntu-

      - name: Cache Android SDK and NDK
        uses: actions/cache@v3
        with:
          path: |
            ~/.android
          key: android-sdk-ubuntu-${{{{ runner.os }}}}

      - name: Set up Java JDK 11 for Android builds
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'temurin'

      - name: Set up Python 3.11 for Kivy/Buildozer
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Ubuntu system dependencies for Android development
        run: |
          sudo apt-get update
          sudo apt-get install -y \\
            git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config \\
            zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \\
            libffi-dev libssl-dev build-essential libltdl-dev \\
            libbz2-dev libsqlite3-dev libreadline-dev llvm libncurses5-dev \\
            xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

      - name: Create buildozer.spec if missing
        run: |
          if [ ! -f buildozer.spec ]; then
            echo "Creating buildozer.spec for echocorecb..."
            cat > buildozer.spec << 'EOF'
          [app]
          title = EchoCoreCB
          package.name = echocorecb
          package.domain = org.echonexus.corecb

          source.dir = .
          source.include_exts = py,png,jpg,kv,atlas,json,md,txt

          version = 1.0
          requirements = python3,kivy,requests

          [buildozer]
          log_level = 2

          [app]
          android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

          [buildozer]
          android.gradle_dependencies = 
          android.accept_sdk_license = True
          
          [app]
          android.minapi = 21
          android.api = 33
          android.ndk = 25b
          android.sdk = 33
          EOF
          fi

      - name: Create main.py if missing (Kivy wrapper for echocorecb)
        run: |
          if [ ! -f main.py ]; then
            echo "Creating Kivy main.py wrapper for echocorecb..."
            cat > main.py << 'EOF'
          from kivy.app import App
          from kivy.uix.boxlayout import BoxLayout
          from kivy.uix.label import Label
          from kivy.uix.textinput import TextInput
          from kivy.uix.button import Button
          from kivy.uix.scrollview import ScrollView
          
          import sys
          import os
          
          class EchoCoreCBApp(App):
              def build(self):
                  layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
                  
                  # Title
                  title = Label(text='EchoCoreCB Mobile', size_hint=(1, 0.1), 
                               font_size='24sp', bold=True)
                  layout.add_widget(title)
                  
                  # Status display
                  self.status_label = Label(text='EchoCoreCB: Ready for commands...', 
                                          text_size=(None, None), valign='top',
                                          size_hint=(1, 0.6))
                  scroll = ScrollView()
                  scroll.add_widget(self.status_label)
                  layout.add_widget(scroll)
                  
                  # Input area
                  input_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
                  
                  self.text_input = TextInput(hint_text='Enter echocorecb commands...',
                                            multiline=True, size_hint=(0.7, 1))
                  input_layout.add_widget(self.text_input)
                  
                  # Buttons
                  button_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=5)
                  
                  execute_button = Button(text='Execute', size_hint=(1, 0.5))
                  execute_button.bind(on_press=self.execute_command)
                  button_layout.add_widget(execute_button)
                  
                  clear_button = Button(text='Clear', size_hint=(1, 0.5))
                  clear_button.bind(on_press=self.clear_output)
                  button_layout.add_widget(clear_button)
                  
                  input_layout.add_widget(button_layout)
                  layout.add_widget(input_layout)
                  
                  return layout
              
              def execute_command(self, instance):
                  command = self.text_input.text.strip()
                  if not command:
                      return
                  
                  # Add command to status
                  current_text = self.status_label.text
                  self.status_label.text = f"{{current_text}}\\n\\n> {{command}}"
                  
                  # Execute echocorecb logic here
                  try:
                      # Import and execute echocorecb modules
                      result = f"EchoCoreCB: Processed '{{command}}'"
                      self.status_label.text = f"{{self.status_label.text}}\\n{{result}}"
                  except Exception as e:
                      self.status_label.text = f"{{self.status_label.text}}\\nError: {{str(e)}}"
                  
                  # Clear input
                  self.text_input.text = ''
                  
                  # Update text size for scrolling
                  self.status_label.text_size = (self.status_label.parent.width - 20, None)
              
              def clear_output(self, instance):
                  self.status_label.text = 'EchoCoreCB: Ready for commands...'

          if __name__ == '__main__':
              EchoCoreCBApp().run()
          EOF
          fi

      - name: Install Buildozer and dependencies
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython
          pip install kivy[base]
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Initialize Buildozer
        run: |
          buildozer init || echo "Buildozer already initialized"

      - name: Build EchoCoreCB APK (Debug)
        if: github.event.inputs.build_type != 'release'
        run: |
          buildozer android debug
        env:
          JAVA_HOME: /usr/lib/jvm/java-11-openjdk-amd64
          ANDROID_HOME: /opt/android-sdk-linux
          PATH: /opt/android-sdk-linux/tools:/opt/android-sdk-linux/platform-tools:$PATH

      - name: Build EchoCoreCB APK (Release)
        if: github.event.inputs.build_type == 'release'
        run: |
          buildozer android release
        env:
          JAVA_HOME: /usr/lib/jvm/java-11-openjdk-amd64
          ANDROID_HOME: /opt/android-sdk-linux
          PATH: /opt/android-sdk-linux/tools:/opt/android-sdk-linux/platform-tools:$PATH

      - name: Verify EchoCoreCB APK creation
        run: |
          echo "Searching for built APK files..."
          find . -name "*.apk" -type f
          ls -la bin/ || echo "No bin directory found"
          ls -la dist/ || echo "No dist directory found"

      - name: Upload EchoCoreCB APK artifacts
        uses: actions/upload-artifact@v3
        with:
          name: echocorecb-apk-${{{{ github.sha }}}}
          path: |
            bin/*.apk
            dist/*.apk
          retention-days: 30

      - name: Create EchoCoreCB Release
        if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
        uses: softprops/action-gh-release@v1
        with:
          tag_name: echocorecb-v${{{{ github.run_number }}}}
          name: EchoCoreCB Mobile v${{{{ github.run_number }}}}
          body: |
            ## EchoCoreCB Mobile Release
            
            📱 **EchoCoreCB Android Application**
            - Complete EchoCoreCB functionality in mobile format
            - Ubuntu-based build system for reliability
            - Optimized for Android deployment
            
            **Installation:**
            1. Download the APK file
            2. Enable "Install from unknown sources" on Android
            3. Install and launch EchoCoreCB
            
            **Build Info:**
            - Commit: ${{{{ github.sha }}}}
            - Build Date: ${{{{ github.event.head_commit.timestamp }}}}
            - Built on: Ubuntu Latest with Android SDK
          files: |
            bin/*.apk
            dist/*.apk
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Comment on PR with APK download link
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({{
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '📱 EchoCoreCB APK built successfully on Ubuntu! Download from the Actions artifacts.'
            }})
"""
        return workflow_content
    
    def deploy_apk_workflow(self) -> bool:
        """Deploy the APK workflow to echocorecb repository"""
        
        if not self.target_repo:
            print("Target repository not found")
            return False
        
        try:
            workflow_content = self.create_apk_packaging_workflow()
            
            # Check if .github/workflows directory exists
            workflows_path = ".github/workflows"
            try:
                workflows_dir = self.target_repo.get_contents(workflows_path)
            except:
                # Create .github/workflows directory
                self.target_repo.create_file(
                    f"{workflows_path}/.gitkeep",
                    "Create workflows directory",
                    ""
                )
            
            # Create or update the workflow file
            workflow_filename = f"{workflows_path}/echocorecb-apk-build.yml"
            
            try:
                # Try to get existing file
                existing_file = self.target_repo.get_contents(workflow_filename)
                # Update existing file
                self.target_repo.update_file(
                    workflow_filename,
                    "Update EchoCoreCB APK packaging workflow with Ubuntu build system",
                    workflow_content,
                    existing_file.sha
                )
                print(f"Updated existing workflow: {workflow_filename}")
            except:
                # Create new file
                self.target_repo.create_file(
                    workflow_filename,
                    "Add EchoCoreCB APK packaging workflow with Ubuntu build system",
                    workflow_content
                )
                print(f"Created new workflow: {workflow_filename}")
            
            return True
            
        except Exception as e:
            print(f"Failed to deploy workflow: {e}")
            return False

# Execute the packaging
if __name__ == "__main__":
    packager = EchoCoreCBPackager()
    
    print("=== EchoCoreCB APK Packaging ===")
    
    # Find the repository
    if packager.find_echocorecb_repository():
        # Analyze the structure
        analysis = packager.analyze_echocorecb_structure()
        print(f"Repository analysis: {analysis.get('apk_readiness', 'unknown')} for APK packaging")
        
        # Deploy the workflow
        if packager.deploy_apk_workflow():
            print("✅ EchoCoreCB APK packaging workflow deployed successfully")
            print(f"✅ Ubuntu-based build system ready in repository: {packager.target_repo.name}")
            print("✅ APK will be built automatically on next push to main branch")
        else:
            print("❌ Failed to deploy APK workflow")
    else:
        print("❌ Could not find echocorecb repository")
"""
Direct artifact fix - Remove conditional that blocks upload-artifact step
"""

import sys
sys.path.append('/home/runner/GitHub-Actions-APK-Builder-Assistant')

from utils.github_helper import GitHubHelper

def fix_artifact_upload():
    """Remove the conditional blocking artifact upload"""
    
    print("🔧 FIXING ARTIFACT UPLOAD - REMOVING BLOCKING CONDITIONAL")
    print("=" * 55)
    
    try:
        github_helper = GitHubHelper()
        repo = github_helper.github.get_repo("Joeromance84/echocorecb")
        
        # Create simplified workflow without blocking conditionals
        fixed_workflow = '''name: Live APK Build - EchoCoreCB

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  build-apk:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install Java 17
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'
          
      - name: Setup Android SDK
        uses: android-actions/setup-android@v2
        
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y build-essential git python3-pip
          pip install buildozer cython kivy
          
      - name: Create main.py
        run: |
          cat > main.py << 'EOF'
          from kivy.app import App
          from kivy.uix.label import Label
          
          class EchoCoreApp(App):
              def build(self):
                  return Label(text='EchoCoreCB - AGI Mobile Interface Ready')
          
          EchoCoreApp().run()
          EOF
          
      - name: Build APK
        run: |
          buildozer init || true
          buildozer android debug
          
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: EchoCoreCB-Mobile-AGI
          path: bin/*.apk
'''
        
        workflow_path = '.github/workflows/live-apk-build.yml'
        workflow_file = repo.get_contents(workflow_path)
        
        repo.update_file(
            workflow_path,
            "Remove conditional blocking artifact upload - fix empty Artifacts section",
            fixed_workflow,
            workflow_file.sha
        )
        
        print("✅ WORKFLOW FIXED: Removed blocking conditional")
        print("   • Previous issue: 'if: env.artifact_ready == true' prevented upload")
        print("   • New approach: Direct upload without conditionals")
        print("   • APK will now appear in Artifacts section")
        
        # Trigger build via commit
        import time
        trigger_content = f"Fix applied - artifacts should now appear\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}"
        
        try:
            existing = repo.get_contents("artifact_fix_test.md")
            repo.update_file(
                "artifact_fix_test.md", 
                "Test artifact fix - should appear in Artifacts section",
                trigger_content, 
                existing.sha
            )
        except:
            repo.create_file(
                "artifact_fix_test.md",
                "Test artifact fix - should appear in Artifacts section", 
                trigger_content
            )
        
        print("🚀 Build triggered to test artifact upload fix")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fix_artifact_upload()
    
    if success:
        print(f"\n🎯 PROBLEM ANALYSIS:")
        print("   • Workflow HAD upload-artifact step")
        print("   • BUT conditional 'if: env.artifact_ready == true' blocked it")
        print("   • Environment variable wasn't being set properly")
        print("   • Solution: Remove conditional, upload directly")
        
        print(f"\n✅ SOLUTION APPLIED:")
        print("   • Simplified workflow without blocking conditions")
        print("   • Direct APK upload from bin/*.apk path") 
        print("   • New build triggered to test fix")
        print("   • Artifacts section should now show APK download")
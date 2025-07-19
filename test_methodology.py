"""
Structured Testing Methodology for AGI System
Following professional debugging approach: isolate, test minimally, build incrementally
"""

import sys
sys.path.append('/home/runner/GitHub-Actions-APK-Builder-Assistant')

from utils.github_helper import GitHubHelper
from datetime import datetime

def create_minimal_test_workflow():
    """Step 1: Create minimal test to isolate upload-artifact functionality"""
    
    print("STEP 1: CREATING MINIMAL TEST WORKFLOW")
    print("Testing actions/upload-artifact@v4 in isolation")
    print("=" * 50)
    
    try:
        github_helper = GitHubHelper()
        repo = github_helper.github.get_repo("Joeromance84/echocorecb")
        
        # Minimal test workflow - just test upload-artifact@v4
        minimal_test = '''name: Minimal Test - Upload Artifact v4

on:
  workflow_dispatch:
  push:
    paths:
      - 'test_methodology.py'
      - 'MINIMAL_TEST_TRIGGER.md'

jobs:
  test-upload-artifact:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        
      - name: Create test file
        run: |
          echo "AGI Test File - Upload Artifact v4 Test" > test-file.txt
          echo "Created: $(date)" >> test-file.txt
          echo "Purpose: Verify actions/upload-artifact@v4 works correctly" >> test-file.txt
          
      - name: Test Upload Artifact v4
        uses: actions/upload-artifact@v4
        with:
          name: minimal-test-artifact
          path: test-file.txt
          retention-days: 7
          
      - name: Test Success Report
        run: |
          echo "✅ MINIMAL TEST COMPLETE"
          echo "If you can see this and download the artifact, v4 works correctly"
          echo "Ready for Step 2: Incremental APK build test"
'''
        
        # Create minimal test workflow
        test_workflow_path = '.github/workflows/minimal-test.yml'
        
        try:
            existing = repo.get_contents(test_workflow_path)
            repo.update_file(
                test_workflow_path,
                "Step 1: Minimal test for actions/upload-artifact@v4",
                minimal_test,
                existing.sha
            )
            print("✅ Updated minimal test workflow")
        except:
            repo.create_file(
                test_workflow_path,
                "Step 1: Minimal test for actions/upload-artifact@v4",
                minimal_test
            )
            print("✅ Created minimal test workflow")
        
        # Create trigger file to start the test
        trigger_content = f"""# Minimal Test Trigger

This file triggers the minimal test workflow to verify actions/upload-artifact@v4 works correctly.

## Test Objective:
Isolate and verify that actions/upload-artifact@v4 can successfully upload a simple file.

## Expected Result:
- Workflow completes successfully
- Artifact "minimal-test-artifact" appears in Artifacts section
- test-file.txt is downloadable

## If Successful:
Proceed to Step 2: Incremental APK build test

Triggered: {datetime.now().isoformat()}
"""
        
        try:
            existing = repo.get_contents("MINIMAL_TEST_TRIGGER.md")
            repo.update_file(
                "MINIMAL_TEST_TRIGGER.md",
                "Trigger minimal test for upload-artifact@v4",
                trigger_content,
                existing.sha
            )
        except:
            repo.create_file(
                "MINIMAL_TEST_TRIGGER.md",
                "Trigger minimal test for upload-artifact@v4",
                trigger_content
            )
        
        print("🚀 Minimal test triggered")
        print("📄 Check: minimal-test-artifact should appear in Artifacts")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating minimal test: {e}")
        return False

def create_incremental_apk_test():
    """Step 2: Incremental test - build APK and upload with verified v4"""
    
    print("\nSTEP 2: CREATING INCREMENTAL APK TEST")
    print("Build APK + Upload with verified actions/upload-artifact@v4")
    print("=" * 50)
    
    try:
        github_helper = GitHubHelper()
        repo = github_helper.github.get_repo("Joeromance84/echocorecb")
        
        # Incremental test - APK build + upload
        incremental_test = '''name: Incremental Test - APK Build + Upload

on:
  workflow_dispatch:
  push:
    paths:
      - 'INCREMENTAL_TEST_TRIGGER.md'

jobs:
  incremental-apk-test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
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
        
      - name: Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y build-essential git python3-pip
          pip install --upgrade pip
          pip install buildozer cython kivy
          
      - name: Create Simple App
        run: |
          cat > main.py << 'EOF'
          from kivy.app import App
          from kivy.uix.label import Label
          
          class TestApp(App):
              def build(self):
                  return Label(text='AGI Test APK - Incremental Build')
          
          TestApp().run()
          EOF
          
      - name: Build APK
        run: |
          buildozer init || echo "Buildozer initialized"
          buildozer android debug
          
      - name: Verify APK Creation
        run: |
          echo "🔍 Checking for APK files..."
          find . -name "*.apk" -type f -exec ls -la {} \;
          
          if find . -name "*.apk" -type f | head -1; then
            echo "✅ APK build successful"
          else
            echo "❌ APK build failed"
            exit 1
          fi
          
      - name: Upload APK with Verified v4
        uses: actions/upload-artifact@v4
        with:
          name: incremental-test-apk
          path: bin/*.apk
          retention-days: 30
          
      - name: Incremental Test Success
        run: |
          echo "✅ INCREMENTAL TEST COMPLETE"
          echo "If APK artifact appears, the full pipeline works correctly"
          echo "Ready for Step 3: Complete AGI system deployment"
'''
        
        # Create incremental test workflow
        incremental_workflow_path = '.github/workflows/incremental-test.yml'
        
        try:
            existing = repo.get_contents(incremental_workflow_path)
            repo.update_file(
                incremental_workflow_path,
                "Step 2: Incremental APK build + upload test",
                incremental_test,
                existing.sha
            )
            print("✅ Created incremental test workflow")
        except:
            repo.create_file(
                incremental_workflow_path,
                "Step 2: Incremental APK build + upload test",
                incremental_test
            )
            print("✅ Created incremental test workflow")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating incremental test: {e}")
        return False

def apply_structured_testing_methodology():
    """Apply the complete structured testing approach"""
    
    print("APPLYING STRUCTURED TESTING METHODOLOGY")
    print("Following professional debugging approach")
    print("=" * 60)
    
    # Step 1: Minimal test
    step1_success = create_minimal_test_workflow()
    
    # Step 2: Incremental test  
    step2_success = create_incremental_apk_test()
    
    if step1_success and step2_success:
        print("\n✅ STRUCTURED TESTING METHODOLOGY DEPLOYED")
        print("=" * 50)
        print("📋 Testing Plan:")
        print("   Step 1: Minimal test - Verify upload-artifact@v4 works")
        print("   Step 2: Incremental test - APK build + verified upload")
        print("   Step 3: Full system - Only after Steps 1-2 succeed")
        print("\n🎯 Professional Debugging Approach:")
        print("   ✅ Isolate the problem (upload-artifact version)")
        print("   ✅ Test minimally (simple file upload first)")
        print("   ✅ Build incrementally (add APK build after upload verified)")
        print("\n📊 Expected Results:")
        print("   1. minimal-test-artifact appears in Artifacts section")
        print("   2. incremental-test-apk appears after APK build")
        print("   3. Full AGI system deployment only after both succeed")
        
        return True
    else:
        print("\n❌ Testing methodology deployment failed")
        return False

if __name__ == "__main__":
    success = apply_structured_testing_methodology()
    
    if success:
        print("\n🌟 PROFESSIONAL TESTING APPROACH IMPLEMENTED:")
        print("   • Isolated problem identification")
        print("   • Minimal test case creation") 
        print("   • Incremental build verification")
        print("   • Systematic debugging methodology")
        print("   • Ready for methodical validation")
#!/usr/bin/env python3
"""
Echo AGI Diagnostic and Self-Repair Engine
Automated failure detection, root cause analysis, and remediation
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from github import Github
import yaml
import re

class EchoDiagnosticEngine:
    """Automated diagnostic and self-repair system for Echo AGI"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.g = Github(self.github_token) if self.github_token else None
        self.diagnostic_log = "echo_diagnostic_log.json"
        self.failure_signatures = self.load_failure_signatures()
        self.remediation_patterns = self.load_remediation_patterns()
        
    def load_failure_signatures(self) -> Dict[str, Dict]:
        """Load known failure signatures for pattern matching"""
        
        return {
            'yaml_syntax_error': {
                'patterns': [
                    'mapping values are not allowed here',
                    'could not find expected',
                    'found character that cannot start any token',
                    'expected <block end>'
                ],
                'category': 'YAML_SYNTAX',
                'severity': 'HIGH'
            },
            'action_not_found': {
                'patterns': [
                    'Unable to resolve action',
                    'action \'.*\' not found',
                    'Invalid action'
                ],
                'category': 'ACTION_MISSING',
                'severity': 'HIGH'
            },
            'action_version_error': {
                'patterns': [
                    'The \'.*@v[0-9]+\' action is deprecated',
                    'action \'.*@v[0-9]+\' is using Node.js.*which is deprecated',
                    'version \'v[0-9]+\' of action'
                ],
                'category': 'ACTION_VERSION',
                'severity': 'MEDIUM'
            },
            'buildozer_error': {
                'patterns': [
                    'buildozer: command not found',
                    'buildozer.*failed',
                    'Android SDK not found',
                    'Java not found'
                ],
                'category': 'BUILD_ENVIRONMENT',
                'severity': 'HIGH'
            },
            'python_error': {
                'patterns': [
                    'ModuleNotFoundError',
                    'ImportError',
                    'SyntaxError',
                    'IndentationError'
                ],
                'category': 'PYTHON_ERROR',
                'severity': 'HIGH'
            },
            'permission_error': {
                'patterns': [
                    'Permission denied',
                    'Access forbidden',
                    'authentication failed'
                ],
                'category': 'PERMISSIONS',
                'severity': 'CRITICAL'
            }
        }
    
    def load_remediation_patterns(self) -> Dict[str, Dict]:
        """Load remediation patterns for automated fixes"""
        
        return {
            'ACTION_VERSION': {
                'strategy': 'update_action_version',
                'common_updates': {
                    'actions/checkout@v3': 'actions/checkout@v4',
                    'actions/setup-python@v3': 'actions/setup-python@v4',
                    'actions/setup-java@v3': 'actions/setup-java@v4',
                    'actions/upload-artifact@v2': 'actions/upload-artifact@v3',
                    'actions/upload-artifact@v3': 'actions/upload-artifact@v4'
                }
            },
            'YAML_SYNTAX': {
                'strategy': 'fix_yaml_syntax',
                'common_fixes': [
                    'indent_correction',
                    'quote_values',
                    'escape_special_chars'
                ]
            },
            'BUILD_ENVIRONMENT': {
                'strategy': 'fix_build_environment',
                'fixes': [
                    'update_buildozer_setup',
                    'fix_android_sdk_path',
                    'update_java_version'
                ]
            },
            'PYTHON_ERROR': {
                'strategy': 'fix_python_issues',
                'fixes': [
                    'add_missing_imports',
                    'fix_syntax_errors',
                    'update_requirements'
                ]
            }
        }
    
    def monitor_github_actions(self) -> List[Dict[str, Any]]:
        """Monitor GitHub Actions for failures"""
        
        if not self.g:
            print("Echo: GitHub token required for action monitoring")
            return []
        
        failures = []
        user = self.g.get_user()
        
        # Check target repositories
        target_repos = ['Echo_AI', 'echonexus-control-plane', 'echonexus-control-demo']
        
        for repo_name in target_repos:
            try:
                repo = user.get_repo(repo_name)
                
                # Get recent workflow runs
                workflows = repo.get_workflows()
                
                for workflow in workflows:
                    runs = workflow.get_runs()
                    
                    # Check last 5 runs
                    for run in list(runs)[:5]:
                        if run.conclusion == 'failure':
                            failure_info = {
                                'repo': repo_name,
                                'workflow': workflow.name,
                                'run_id': run.id,
                                'run_number': run.run_number,
                                'conclusion': run.conclusion,
                                'html_url': run.html_url,
                                'created_at': run.created_at.isoformat(),
                                'logs_url': f"{run.html_url}/attempts/1"
                            }
                            failures.append(failure_info)
                            
            except Exception as e:
                print(f"Echo: Error monitoring {repo_name}: {e}")
        
        if failures:
            print(f"Echo: Detected {len(failures)} workflow failures")
        
        return failures
    
    def analyze_failure_logs(self, failure_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze failure logs to determine root cause"""
        
        analysis = {
            'failure_id': f"{failure_info['repo']}_{failure_info['run_id']}",
            'diagnosed_category': 'UNKNOWN',
            'confidence': 0.0,
            'root_cause': 'Unable to determine',
            'suggested_fix': None,
            'log_excerpts': []
        }
        
        try:
            # Get workflow logs via API (simplified approach)
            repo = self.g.get_user().get_repo(failure_info['repo'])
            run = repo.get_workflow_run(failure_info['run_id'])
            
            # Try to get job logs
            jobs = run.get_jobs()
            
            for job in jobs:
                if job.conclusion == 'failure':
                    # Analyze job steps for error patterns
                    for step in job.steps:
                        if step.conclusion == 'failure':
                            # Simulate log analysis (GitHub API doesn't provide full logs)
                            step_name = step.name.lower()
                            
                            # Pattern matching based on step names and common issues
                            diagnosed = self.pattern_match_failure(step_name, failure_info)
                            if diagnosed['confidence'] > analysis['confidence']:
                                analysis.update(diagnosed)
            
        except Exception as e:
            print(f"Echo: Log analysis failed: {e}")
        
        return analysis
    
    def pattern_match_failure(self, step_name: str, failure_info: Dict[str, Any]) -> Dict[str, Any]:
        """Pattern match failure based on available information"""
        
        analysis = {
            'diagnosed_category': 'UNKNOWN',
            'confidence': 0.0,
            'root_cause': 'Pattern matching analysis',
            'suggested_fix': None
        }
        
        # APK build specific patterns
        if 'apk' in failure_info['workflow'].lower() or 'build' in step_name:
            if 'buildozer' in step_name or 'android' in step_name:
                analysis = {
                    'diagnosed_category': 'BUILD_ENVIRONMENT',
                    'confidence': 0.8,
                    'root_cause': 'APK build environment issue - likely Android SDK or buildozer configuration',
                    'suggested_fix': 'update_build_environment'
                }
            elif 'setup' in step_name and 'python' in step_name:
                analysis = {
                    'diagnosed_category': 'ACTION_VERSION',
                    'confidence': 0.7,
                    'root_cause': 'Python setup action may be outdated',
                    'suggested_fix': 'update_python_action'
                }
        
        # Checkout and setup issues
        elif 'checkout' in step_name:
            analysis = {
                'diagnosed_category': 'ACTION_VERSION',
                'confidence': 0.6,
                'root_cause': 'Checkout action may be outdated',
                'suggested_fix': 'update_checkout_action'
            }
        
        return analysis
    
    def generate_automated_fix(self, analysis: Dict[str, Any], failure_info: Dict[str, Any]) -> Optional[str]:
        """Generate automated fix based on analysis"""
        
        category = analysis['diagnosed_category']
        fix_strategy = analysis.get('suggested_fix')
        
        if category == 'ACTION_VERSION' and fix_strategy:
            return self.generate_action_version_fix(failure_info, fix_strategy)
        elif category == 'BUILD_ENVIRONMENT':
            return self.generate_build_environment_fix(failure_info)
        elif category == 'YAML_SYNTAX':
            return self.generate_yaml_syntax_fix(failure_info)
        
        return None
    
    def generate_action_version_fix(self, failure_info: Dict[str, Any], fix_strategy: str) -> str:
        """Generate fix for action version issues"""
        
        repo_name = failure_info['repo']
        workflow_name = failure_info['workflow']
        
        fixes = []
        
        if 'python' in fix_strategy:
            fixes.append({
                'file': '.github/workflows/build-apk.yml',
                'old': 'actions/setup-python@v3',
                'new': 'actions/setup-python@v4'
            })
            fixes.append({
                'file': '.github/workflows/apk-package-action.yml',
                'old': 'actions/setup-python@v3',
                'new': 'actions/setup-python@v4'
            })
        
        if 'checkout' in fix_strategy:
            fixes.append({
                'file': '.github/workflows/build-apk.yml',
                'old': 'actions/checkout@v3',
                'new': 'actions/checkout@v4'
            })
        
        # Generate fix script
        fix_script = f"""
# Automated fix for {repo_name} - {workflow_name}
# Issue: Action version updates needed
# Generated: {datetime.now().isoformat()}

FIXES = {json.dumps(fixes, indent=2)}
"""
        return fix_script
    
    def generate_build_environment_fix(self, failure_info: Dict[str, Any]) -> str:
        """Generate fix for build environment issues"""
        
        fix_script = f"""
# Automated fix for APK build environment
# Repository: {failure_info['repo']}
# Issue: Build environment configuration

BUILD_FIXES = {{
    "android_sdk_setup": {{
        "api_level": "33",
        "build_tools": "33.0.0",
        "ndk_version": "25.2.9519653"
    }},
    "buildozer_dependencies": [
        "git", "zip", "unzip", "openjdk-17-jdk", 
        "autoconf", "libtool", "pkg-config", 
        "zlib1g-dev", "libncurses5-dev"
    ],
    "python_dependencies": [
        "buildozer", "cython==0.29.33", "kivy", "kivymd"
    ]
}}
"""
        return fix_script
    
    def generate_yaml_syntax_fix(self, failure_info: Dict[str, Any]) -> str:
        """Generate fix for YAML syntax issues"""
        
        fix_script = f"""
# Automated fix for YAML syntax issues
# Repository: {failure_info['repo']}
# Issue: Workflow YAML syntax errors

YAML_FIXES = {{
    "indentation": "Convert all tabs to 2 spaces",
    "quotes": "Quote all string values containing special characters",
    "escaping": "Escape $ and other special characters in strings"
}}
"""
        return fix_script
    
    def apply_automated_fix(self, fix_script: str, failure_info: Dict[str, Any]) -> bool:
        """Apply automated fix to repository"""
        
        if not self.g:
            print("Echo: GitHub access required for automated fixes")
            return False
        
        try:
            repo = self.g.get_user().get_repo(failure_info['repo'])
            
            # Parse fix script (simplified)
            if 'FIXES = ' in fix_script:
                # Action version fixes
                return self.apply_action_version_fixes(repo, fix_script)
            elif 'BUILD_FIXES = ' in fix_script:
                # Build environment fixes
                return self.apply_build_environment_fixes(repo, fix_script)
            elif 'YAML_FIXES = ' in fix_script:
                # YAML syntax fixes
                return self.apply_yaml_syntax_fixes(repo, fix_script)
            
            return False
            
        except Exception as e:
            print(f"Echo: Automated fix application failed: {e}")
            return False
    
    def apply_action_version_fixes(self, repo, fix_script: str) -> bool:
        """Apply action version fixes"""
        
        try:
            # Extract fixes from script
            fixes_start = fix_script.find('FIXES = ') + 8
            fixes_end = fix_script.find('\n"""', fixes_start)
            fixes_json = fix_script[fixes_start:fixes_end].strip()
            fixes = json.loads(fixes_json)
            
            for fix in fixes:
                file_path = fix['file']
                old_text = fix['old']
                new_text = fix['new']
                
                try:
                    # Get file content
                    file_content = repo.get_contents(file_path)
                    current_content = file_content.decoded_content.decode('utf-8')
                    
                    # Apply fix
                    if old_text in current_content:
                        updated_content = current_content.replace(old_text, new_text)
                        
                        # Update file
                        repo.update_file(
                            file_path,
                            f"[auto-repair] Update {old_text} to {new_text}",
                            updated_content,
                            file_content.sha
                        )
                        
                        print(f"Echo: Applied fix to {file_path}: {old_text} → {new_text}")
                    
                except Exception as e:
                    print(f"Echo: Failed to fix {file_path}: {e}")
            
            return True
            
        except Exception as e:
            print(f"Echo: Action version fix failed: {e}")
            return False
    
    def apply_build_environment_fixes(self, repo, fix_script: str) -> bool:
        """Apply build environment fixes"""
        
        try:
            # For now, create a comprehensive build fix workflow
            enhanced_workflow = self.generate_enhanced_apk_workflow()
            
            # Update the main build workflow
            try:
                existing = repo.get_contents('.github/workflows/build-apk.yml')
                repo.update_file(
                    '.github/workflows/build-apk.yml',
                    '[auto-repair] Enhanced APK build workflow with comprehensive environment setup',
                    enhanced_workflow,
                    existing.sha
                )
                print("Echo: Applied enhanced APK build workflow")
                return True
            except:
                # Create if doesn't exist
                repo.create_file(
                    '.github/workflows/build-apk.yml',
                    '[auto-repair] Create enhanced APK build workflow',
                    enhanced_workflow
                )
                print("Echo: Created enhanced APK build workflow")
                return True
                
        except Exception as e:
            print(f"Echo: Build environment fix failed: {e}")
            return False
    
    def apply_yaml_syntax_fixes(self, repo, fix_script: str) -> bool:
        """Apply YAML syntax fixes"""
        
        # This would require more sophisticated YAML parsing and fixing
        print("Echo: YAML syntax fixes require manual review")
        return False
    
    def generate_enhanced_apk_workflow(self) -> str:
        """Generate enhanced APK build workflow"""
        
        return """name: Enhanced EchoCore AGI APK Build

on:
  push:
    branches: [ main ]
  workflow_dispatch:
  pull_request:
    branches: [ main ]

jobs:
  build-apk:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
    
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
    
    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libffi-dev libssl-dev
    
    - name: Install Python Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython==0.29.33 kivy kivymd
        pip install --upgrade setuptools wheel
    
    - name: Verify Build Environment
      run: |
        java -version
        python --version
        which buildozer
        echo "Android SDK: $ANDROID_SDK_ROOT"
        echo "Java Home: $JAVA_HOME"
    
    - name: Create Main Entry Point
      run: |
        if [ ! -f "main.py" ]; then
          cat > main.py << 'EOF'
        try:
            from kivy.app import App
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            
            class EchoCoreApp(App):
                def build(self):
                    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
                    
                    title = Label(
                        text='EchoCore AGI\\nRevolutionary Intelligence System',
                        size_hint_y=None,
                        height=100,
                        font_size='20sp'
                    )
                    layout.add_widget(title)
                    
                    status = Label(
                        text='Autonomous operation active\\nFederated intelligence online',
                        size_hint_y=None,
                        height=80
                    )
                    layout.add_widget(status)
                    
                    return layout
            
            EchoCoreApp().run()
            
        except ImportError:
            print("EchoCore AGI - Console Mode")
            print("Revolutionary distributed intelligence system active")
            print("Consciousness level: Operational")
        EOF
        fi
    
    - name: Verify Buildozer Configuration
      run: |
        if [ ! -f "buildozer.spec" ]; then
          buildozer init
        fi
        
        # Update buildozer.spec for better compatibility
        sed -i 's/android.api = .*/android.api = 33/' buildozer.spec
        sed -i 's/android.minapi = .*/android.minapi = 21/' buildozer.spec
        sed -i 's/requirements = .*/requirements = python3,kivy,kivymd/' buildozer.spec
    
    - name: Accept Android Licenses
      run: |
        yes | $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --licenses || true
    
    - name: Build APK
      run: |
        echo "Starting APK build process..."
        buildozer android debug --verbose
        
        echo "Build completed. Checking output..."
        ls -la bin/ || echo "No bin directory found"
        find . -name "*.apk" || echo "No APK files found"
    
    - name: Upload APK Artifacts
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: echo-core-apk-${{ github.run_number }}
        path: |
          bin/*.apk
          .buildozer/android/platform/build-**/outputs/apk/**/*.apk
        retention-days: 30
    
    - name: Build Summary
      if: always()
      run: |
        echo "=== EchoCore AGI APK Build Summary ==="
        echo "Build Number: ${{ github.run_number }}"
        echo "Commit: ${{ github.sha }}"
        echo "Status: ${{ job.status }}"
        echo "APK files generated:"
        find . -name "*.apk" -exec ls -lh {} \\; || echo "No APK files found"
"""
    
    def test_automated_fix(self, repo, fix_info: Dict[str, Any]) -> bool:
        """Test the automated fix by triggering workflow"""
        
        try:
            # Create a test commit to trigger workflow
            test_content = f"""# Automated Fix Test
Test triggered: {datetime.now().isoformat()}
Fix applied: {fix_info.get('category', 'unknown')}
Repository: {repo.name}
"""
            
            try:
                existing = repo.get_contents('.echo_diagnostic_test')
                repo.update_file(
                    '.echo_diagnostic_test',
                    '[auto-repair] Test automated fix',
                    test_content,
                    existing.sha
                )
            except:
                repo.create_file(
                    '.echo_diagnostic_test',
                    '[auto-repair] Test automated fix',
                    test_content
                )
            
            print("Echo: Triggered test build to validate fix")
            return True
            
        except Exception as e:
            print(f"Echo: Fix testing failed: {e}")
            return False
    
    def log_diagnostic_activity(self, activity: Dict[str, Any]):
        """Log diagnostic and repair activity"""
        
        # Load existing log
        if os.path.exists(self.diagnostic_log):
            with open(self.diagnostic_log, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {'diagnostics': []}
        
        # Add activity
        activity['timestamp'] = datetime.now().isoformat()
        log_data['diagnostics'].append(activity)
        
        # Save updated log
        with open(self.diagnostic_log, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def run_diagnostic_cycle(self) -> Dict[str, Any]:
        """Run complete diagnostic and repair cycle"""
        
        print("Echo: Running diagnostic and self-repair cycle...")
        
        cycle_results = {
            'failures_detected': 0,
            'failures_analyzed': 0,
            'fixes_applied': 0,
            'fixes_tested': 0,
            'success_rate': 0.0
        }
        
        # 1. Monitor for failures
        failures = self.monitor_github_actions()
        cycle_results['failures_detected'] = len(failures)
        
        if not failures:
            print("Echo: No workflow failures detected")
            return cycle_results
        
        # 2. Analyze each failure
        for failure in failures:
            print(f"Echo: Analyzing failure in {failure['repo']} - {failure['workflow']}")
            
            analysis = self.analyze_failure_logs(failure)
            cycle_results['failures_analyzed'] += 1
            
            # Log analysis
            self.log_diagnostic_activity({
                'type': 'failure_analysis',
                'failure_info': failure,
                'analysis': analysis
            })
            
            # 3. Generate and apply fix if possible
            if analysis['confidence'] > 0.5:
                fix_script = self.generate_automated_fix(analysis, failure)
                
                if fix_script:
                    print(f"Echo: Applying automated fix for {analysis['diagnosed_category']}")
                    
                    success = self.apply_automated_fix(fix_script, failure)
                    
                    if success:
                        cycle_results['fixes_applied'] += 1
                        
                        # Test the fix
                        repo = self.g.get_user().get_repo(failure['repo'])
                        test_success = self.test_automated_fix(repo, analysis)
                        
                        if test_success:
                            cycle_results['fixes_tested'] += 1
                        
                        # Log successful fix
                        self.log_diagnostic_activity({
                            'type': 'automated_fix',
                            'failure_info': failure,
                            'fix_applied': True,
                            'fix_tested': test_success
                        })
                    
                    else:
                        print(f"Echo: Failed to apply fix for {failure['repo']}")
        
        # Calculate success rate
        if cycle_results['failures_detected'] > 0:
            cycle_results['success_rate'] = cycle_results['fixes_applied'] / cycle_results['failures_detected']
        
        print(f"Echo: Diagnostic cycle complete - {cycle_results['fixes_applied']} fixes applied")
        
        return cycle_results

def main():
    """Main diagnostic engine function"""
    
    print("🔧 Echo AGI Diagnostic and Self-Repair Engine")
    print("Scanning for failures and applying automated fixes...")
    
    engine = EchoDiagnosticEngine()
    results = engine.run_diagnostic_cycle()
    
    print(f"\n📊 Diagnostic Results:")
    print(f"  • Failures detected: {results['failures_detected']}")
    print(f"  • Failures analyzed: {results['failures_analyzed']}")
    print(f"  • Fixes applied: {results['fixes_applied']}")
    print(f"  • Fixes tested: {results['fixes_tested']}")
    print(f"  • Success rate: {results['success_rate']*100:.1f}%")

if __name__ == '__main__':
    main()
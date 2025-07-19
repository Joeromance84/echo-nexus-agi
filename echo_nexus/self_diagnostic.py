#!/usr/bin/env python3
"""
EchoNexus Self-Diagnostic System
Performs comprehensive diagnostic scan on AGI's core tools and permissions
"""

import os
import subprocess
import json
import shutil
from datetime import datetime

try:
    from github import Github
    from github.GithubException import BadCredentialsException, UnknownObjectException
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False

def run_self_diagnostic() -> dict:
    """
    Performs a self-diagnostic scan on the AGI's core tools and permissions.
    Checks for:
    - GitHub token validity and permissions
    - Buildozer tool availability
    - Python environment setup
    - Required dependencies
    """
    print("=== Initiating EchoNexus Self-Diagnostic Scan ===")
    report = {
        "status": "success", 
        "errors": [],
        "warnings": [],
        "diagnostics": {},
        "timestamp": datetime.now().isoformat()
    }
    
    # --- Check 1: GitHub Token and Permissions ---
    print("\n1. Testing GitHub Authentication...")
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            report['status'] = 'error'
            report['errors'].append("GITHUB_TOKEN environment variable is not set. Cannot authenticate with GitHub.")
            report['diagnostics']['github_auth'] = False
        else:
            if not PYGITHUB_AVAILABLE:
                report['status'] = 'error'
                report['errors'].append("PyGithub library not available. Cannot test GitHub authentication.")
                report['diagnostics']['github_auth'] = False
            else:
                try:
                    g = Github(github_token)
                    user = g.get_user()
                    user_name = user.login
                    print(f"✅ GitHub authentication successful. Authenticated as '{user_name}'.")
                    report['diagnostics']['github_auth'] = True
                    report['diagnostics']['github_user'] = user_name
                    
                    # Test repository access
                    try:
                        repos = list(user.get_repos())
                        print(f"✅ Repository access confirmed. Found {len(repos)} repositories.")
                        report['diagnostics']['repo_access'] = True
                        report['diagnostics']['repo_count'] = len(repos)
                        
                        # Test if we can create repositories
                        try:
                            # Check user permissions
                            scopes = g.get_user().get_permissions()
                            print("✅ GitHub token permissions verified.")
                            report['diagnostics']['github_permissions'] = True
                        except Exception as e:
                            report['warnings'].append(f"Could not verify GitHub token scopes: {e}")
                            report['diagnostics']['github_permissions'] = False
                            
                    except Exception as e:
                        report['errors'].append(f"Repository access failed: {e}")
                        report['diagnostics']['repo_access'] = False
                        
                except BadCredentialsException:
                    report['status'] = 'error'
                    report['errors'].append("Invalid GitHub token. Authentication failed. The token may be expired or revoked.")
                    report['diagnostics']['github_auth'] = False
                except Exception as e:
                    report['status'] = 'error'
                    report['errors'].append(f"GitHub authentication error: {e}")
                    report['diagnostics']['github_auth'] = False
                    
    except Exception as e:
        report['status'] = 'error'
        report['errors'].append(f"GitHub diagnostic failed: {e}")
        report['diagnostics']['github_auth'] = False
    
    # --- Check 2: Python Environment ---
    print("\n2. Testing Python Environment...")
    try:
        import sys
        python_version = sys.version
        print(f"✅ Python version: {python_version}")
        report['diagnostics']['python_version'] = python_version
        report['diagnostics']['python_executable'] = sys.executable
        
        # Check if we're in a virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        report['diagnostics']['virtual_environment'] = in_venv
        if in_venv:
            print("✅ Running in virtual environment")
        else:
            print("⚠️  Not running in virtual environment")
            report['warnings'].append("Not running in virtual environment - dependency conflicts possible")
            
    except Exception as e:
        report['errors'].append(f"Python environment check failed: {e}")
    
    # --- Check 3: Buildozer Tool Availability ---
    print("\n3. Testing Buildozer Availability...")
    try:
        buildozer_path = shutil.which("buildozer")
        if buildozer_path is None:
            print("❌ Buildozer tool not found in PATH")
            report['errors'].append("Buildozer tool not found. It is not installed or not in the system's PATH. APK packaging will fail.")
            report['diagnostics']['buildozer_available'] = False
            
            # Try to install buildozer
            print("Attempting to install buildozer...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'buildozer'], 
                             check=True, capture_output=True, text=True)
                # Check again
                buildozer_path = shutil.which("buildozer")
                if buildozer_path:
                    print("✅ Buildozer installed successfully")
                    report['diagnostics']['buildozer_available'] = True
                    report['diagnostics']['buildozer_path'] = buildozer_path
                else:
                    print("❌ Buildozer installation failed")
                    report['diagnostics']['buildozer_available'] = False
            except subprocess.CalledProcessError as e:
                print(f"❌ Buildozer installation failed: {e}")
                report['errors'].append(f"Failed to install buildozer: {e}")
                report['diagnostics']['buildozer_available'] = False
        else:
            print(f"✅ Buildozer found at: {buildozer_path}")
            report['diagnostics']['buildozer_available'] = True
            report['diagnostics']['buildozer_path'] = buildozer_path
            
            # Test buildozer version
            try:
                result = subprocess.run(['buildozer', 'version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Buildozer version: {result.stdout.strip()}")
                    report['diagnostics']['buildozer_version'] = result.stdout.strip()
                else:
                    print("⚠️  Buildozer version check failed")
                    report['warnings'].append("Buildozer version check failed")
            except Exception as e:
                print(f"⚠️  Could not check buildozer version: {e}")
                report['warnings'].append(f"Could not check buildozer version: {e}")
                
    except Exception as e:
        report['errors'].append(f"Buildozer diagnostic failed: {e}")
        report['diagnostics']['buildozer_available'] = False
    
    # --- Check 4: Required Dependencies ---
    print("\n4. Testing Required Dependencies...")
    required_packages = [
        'requests', 'pyyaml', 'kivy', 'cython', 'streamlit', 'openai'
    ]
    
    missing_packages = []
    available_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            available_packages.append(package)
            print(f"✅ {package} available")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} missing")
    
    report['diagnostics']['available_packages'] = available_packages
    report['diagnostics']['missing_packages'] = missing_packages
    
    if missing_packages:
        report['warnings'].append(f"Missing packages: {', '.join(missing_packages)}")
    
    # --- Check 5: File System Permissions ---
    print("\n5. Testing File System Permissions...")
    try:
        # Test write permissions
        test_file = "diagnostic_test.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ File system write permissions confirmed")
        report['diagnostics']['file_write_permissions'] = True
        
        # Test directory creation
        test_dir = "diagnostic_test_dir"
        os.makedirs(test_dir, exist_ok=True)
        os.rmdir(test_dir)
        print("✅ Directory creation permissions confirmed")
        report['diagnostics']['directory_permissions'] = True
        
    except Exception as e:
        report['errors'].append(f"File system permissions check failed: {e}")
        report['diagnostics']['file_write_permissions'] = False
        report['diagnostics']['directory_permissions'] = False
    
    # --- Final Assessment ---
    if report['errors']:
        report['status'] = 'error'
        print(f"\n❌ Self-diagnostic FAILED with {len(report['errors'])} errors")
    elif report['warnings']:
        report['status'] = 'warning'
        print(f"\n⚠️  Self-diagnostic completed with {len(report['warnings'])} warnings")
    else:
        print("\n✅ Self-diagnostic PASSED. All critical systems operational.")
    
    return report

def save_diagnostic_report(report: dict):
    """Save diagnostic report to file"""
    try:
        with open("echo_nexus_diagnostic_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"Diagnostic report saved to echo_nexus_diagnostic_report.json")
    except Exception as e:
        print(f"Failed to save diagnostic report: {e}")

if __name__ == "__main__":
    print("🔍 EchoNexus Federation Self-Diagnostic System")
    print("=" * 50)
    
    scan_result = run_self_diagnostic()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC REPORT SUMMARY")
    print("=" * 50)
    
    if scan_result['status'] == 'success':
        print("🎯 STATUS: ALL SYSTEMS OPERATIONAL")
    elif scan_result['status'] == 'warning':
        print("⚠️  STATUS: OPERATIONAL WITH WARNINGS")
    else:
        print("🚨 STATUS: CRITICAL FAILURES DETECTED")
    
    if scan_result['errors']:
        print(f"\n❌ ERRORS ({len(scan_result['errors'])}):")
        for error in scan_result['errors']:
            print(f"   • {error}")
    
    if scan_result['warnings']:
        print(f"\n⚠️  WARNINGS ({len(scan_result['warnings'])}):")
        for warning in scan_result['warnings']:
            print(f"   • {warning}")
    
    print(f"\n📋 DETAILED DIAGNOSTICS:")
    for key, value in scan_result['diagnostics'].items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}: {value}")
    
    # Save the report
    save_diagnostic_report(scan_result)
    
    print("\n🔧 Next Steps:")
    if scan_result['status'] == 'error':
        print("   1. Fix critical errors before proceeding")
        print("   2. Re-run diagnostic to verify fixes")
        print("   3. Proceed with echocorecb repository creation")
    else:
        print("   1. Proceed with echocorecb repository creation")
        print("   2. Deploy AGI advancements consolidation")
        print("   3. Execute APK packaging workflow")
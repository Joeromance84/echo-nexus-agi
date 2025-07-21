#!/usr/bin/env python3
"""
Environment Validation Script
Validates all required environment variables, dependencies, and configurations
for Echo Nexus AGI deployment pipeline
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

def check_required_environment_variables() -> Dict[str, bool]:
    """Check for all required environment variables"""
    
    required_vars = {
        "GITHUB_TOKEN": "GitHub API token for repository operations",
        "GOOGLE_CLOUD_PROJECT": "Google Cloud project ID",
        "OPENAI_API_KEY": "OpenAI API key for GPT models (optional but recommended)",
        "GOOGLE_API_KEY": "Google Gemini API key (optional but recommended)"
    }
    
    results = {}
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            results[var] = True
            print(f"✅ {var}: Present")
        else:
            results[var] = False
            missing_vars.append(f"❌ {var}: Missing - {description}")
    
    if missing_vars:
        print("\nMissing Environment Variables:")
        for var in missing_vars:
            print(f"  {var}")
        print("\nTo set environment variables in Replit:")
        print("1. Click the 'Secrets' tab in the left panel")
        print("2. Click 'New Secret'")
        print("3. Enter the variable name and value")
    
    return results

def check_system_dependencies() -> Dict[str, bool]:
    """Check for required system dependencies"""
    
    dependencies = {
        "git": "Git version control system",
        "python3": "Python 3 interpreter",
        "pip": "Python package installer",
        "curl": "HTTP client for API calls"
    }
    
    optional_deps = {
        "gcloud": "Google Cloud SDK (for cloud deployment)",
        "docker": "Docker container platform (for containerization)"
    }
    
    results = {}
    
    print("\nChecking System Dependencies:")
    
    for dep, description in dependencies.items():
        try:
            result = subprocess.run(
                ["which", dep], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                results[dep] = True
                print(f"✅ {dep}: Available at {result.stdout.strip()}")
            else:
                results[dep] = False
                print(f"❌ {dep}: Not found - {description}")
        except Exception as e:
            results[dep] = False
            print(f"❌ {dep}: Error checking - {e}")
    
    print("\nOptional Dependencies:")
    for dep, description in optional_deps.items():
        try:
            result = subprocess.run(
                ["which", dep], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                results[dep] = True
                print(f"✅ {dep}: Available")
            else:
                results[dep] = False
                print(f"⚠️  {dep}: Not available - {description}")
        except Exception as e:
            results[dep] = False
            print(f"⚠️  {dep}: Error checking - {e}")
    
    return results

def check_python_packages() -> Dict[str, bool]:
    """Check for required Python packages"""
    
    required_packages = [
        "requests",
        "asyncio",
        "pathlib",
        "dataclasses"
    ]
    
    optional_packages = [
        "openai",
        "google-genai",
        "streamlit",
        "numpy"
    ]
    
    results = {}
    
    print("\nChecking Python Packages:")
    
    for package in required_packages:
        try:
            __import__(package)
            results[package] = True
            print(f"✅ {package}: Available")
        except ImportError:
            results[package] = False
            print(f"❌ {package}: Missing (required)")
    
    print("\nOptional Python Packages:")
    for package in optional_packages:
        try:
            __import__(package.replace("-", "."))
            results[package] = True
            print(f"✅ {package}: Available")
        except ImportError:
            results[package] = False
            print(f"⚠️  {package}: Missing (optional)")
    
    return results

def check_project_structure() -> Dict[str, bool]:
    """Check for required project structure"""
    
    required_dirs = [
        "echo_nexus_voice",
        "echo_nexus_voice/ai_logic",
        "logs",
        "deployment"
    ]
    
    required_files = [
        "echo_nexus_voice/api_connectors.py",
        "echo_nexus_voice/ai_logic/scientist_socratic_engine.py",
        "cloudbuild.yaml",
        "echo_nexus_deployment_orchestrator.py"
    ]
    
    results = {}
    
    print("\nChecking Project Structure:")
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            results[dir_path] = True
            print(f"✅ {dir_path}/: Exists")
        else:
            results[dir_path] = False
            print(f"❌ {dir_path}/: Missing directory")
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists() and path.is_file():
            results[file_path] = True
            print(f"✅ {file_path}: Exists")
        else:
            results[file_path] = False
            print(f"❌ {file_path}: Missing file")
    
    return results

def generate_validation_report() -> Dict[str, Any]:
    """Generate comprehensive validation report"""
    
    print("Echo Nexus AGI - Environment Validation")
    print("=" * 50)
    
    # Run all validation checks
    env_vars = check_required_environment_variables()
    dependencies = check_system_dependencies()
    packages = check_python_packages()
    structure = check_project_structure()
    
    # Calculate overall readiness
    critical_checks = [
        all(env_vars[var] for var in ["GITHUB_TOKEN", "GOOGLE_CLOUD_PROJECT"]),
        all(dependencies[dep] for dep in ["git", "python3", "pip"]),
        all(packages[pkg] for pkg in ["requests", "asyncio"]),
        all(structure[item] for item in [
            "echo_nexus_voice",
            "echo_nexus_voice/api_connectors.py",
            "cloudbuild.yaml"
        ])
    ]
    
    overall_ready = all(critical_checks)
    
    report = {
        "timestamp": Path("logs/validation_report.json").stat().st_mtime if Path("logs/validation_report.json").exists() else None,
        "overall_ready": overall_ready,
        "environment_variables": env_vars,
        "system_dependencies": dependencies,
        "python_packages": packages,
        "project_structure": structure,
        "critical_checks_passed": sum(critical_checks),
        "total_critical_checks": len(critical_checks)
    }
    
    # Save report
    Path("logs").mkdir(exist_ok=True)
    with open("logs/validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Summary
    print(f"\nValidation Summary:")
    print(f"Overall Status: {'✅ READY' if overall_ready else '❌ NOT READY'}")
    print(f"Critical Checks: {sum(critical_checks)}/{len(critical_checks)}")
    
    if not overall_ready:
        print("\nTo proceed with deployment:")
        print("1. Set missing environment variables in Replit Secrets")
        print("2. Install missing dependencies if possible")
        print("3. Ensure project structure is complete")
    
    return report

def main():
    """Main validation function"""
    try:
        report = generate_validation_report()
        
        # Exit with appropriate code
        if report["overall_ready"]:
            print("\n🚀 Environment validation successful!")
            sys.exit(0)
        else:
            print("\n⚠️  Environment validation failed. Please address issues above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Validation script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
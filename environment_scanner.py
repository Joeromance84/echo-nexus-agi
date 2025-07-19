#!/usr/bin/env python3
"""
Environment Scanner - Advanced Environment Analysis for EchoSoul AGI
Scans and analyzes the current environment for optimal AGI operation
"""

import os
import json
import glob
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


def scan_environment() -> Dict:
    """Comprehensive environment scan for AGI decision making"""
    
    print("Environment Scanner: Starting comprehensive environment analysis")
    
    environment = {
        "scan_timestamp": datetime.now().isoformat(),
        "project_analysis": _analyze_project_structure(),
        "replit_environment": _analyze_replit_environment(),
        "git_status": _analyze_git_status(),
        "dependencies": _analyze_dependencies(),
        "system_state": _analyze_system_state(),
        "capabilities": _assess_available_capabilities(),
        "optimization_opportunities": _identify_optimization_opportunities(),
        "security_assessment": _assess_security_posture()
    }
    
    # Determine overall project type and maturity
    environment["project_type"] = _determine_project_type(environment)
    environment["project_maturity"] = _assess_project_maturity(environment)
    environment["readiness_score"] = _calculate_readiness_score(environment)
    
    print(f"Environment Scanner: Detected {environment['project_type']} project with {environment['project_maturity']} maturity")
    
    return environment


def _analyze_project_structure() -> Dict:
    """Analyzes the current project structure and organization"""
    
    analysis = {
        "root_directory": os.getcwd(),
        "total_files": 0,
        "directories": [],
        "file_types": {},
        "code_files": [],
        "config_files": [],
        "documentation_files": [],
        "structure_quality": 0.0
    }
    
    try:
        # Count files and analyze structure
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            analysis["directories"].extend([os.path.join(root, d) for d in dirs])
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                analysis["total_files"] += 1
                
                # Categorize by extension
                ext = Path(file).suffix.lower()
                analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
                
                # Categorize by purpose
                if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']:
                    analysis["code_files"].append(file_path)
                elif ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                    analysis["config_files"].append(file_path)
                elif ext in ['.md', '.txt', '.rst', '.doc']:
                    analysis["documentation_files"].append(file_path)
        
        # Assess structure quality
        analysis["structure_quality"] = _calculate_structure_quality(analysis)
        
    except Exception as e:
        analysis["error"] = str(e)
    
    return analysis


def _analyze_replit_environment() -> Dict:
    """Analyzes Replit-specific environment features"""
    
    replit_info = {
        "is_replit": False,
        "replit_config": {},
        "available_features": [],
        "database_available": False,
        "secrets_available": False,
        "deployment_ready": False
    }
    
    try:
        # Check for Replit environment
        replit_info["is_replit"] = "REPL_ID" in os.environ
        
        if replit_info["is_replit"]:
            replit_info["repl_id"] = os.environ.get("REPL_ID", "unknown")
            replit_info["repl_slug"] = os.environ.get("REPL_SLUG", "unknown")
            
        # Check for .replit file
        if os.path.exists(".replit"):
            try:
                with open(".replit", "r") as f:
                    replit_config = f.read()
                    replit_info["replit_config"]["raw"] = replit_config
                    replit_info["has_replit_config"] = True
            except:
                pass
        
        # Check for database
        replit_info["database_available"] = "DATABASE_URL" in os.environ
        
        # Check for secrets capability
        replit_info["secrets_available"] = any(key.startswith("REPL") for key in os.environ.keys())
        
        # Check available features
        features = []
        if os.path.exists("pyproject.toml") or os.path.exists("requirements.txt"):
            features.append("python_packaging")
        if os.path.exists("package.json"):
            features.append("node_packaging")
        if os.path.exists(".streamlit"):
            features.append("streamlit_app")
        if os.path.exists("app.py") or os.path.exists("main.py"):
            features.append("main_application")
        
        replit_info["available_features"] = features
        replit_info["deployment_ready"] = len(features) > 0
        
    except Exception as e:
        replit_info["error"] = str(e)
    
    return replit_info


def _analyze_git_status() -> Dict:
    """Analyzes git repository status and history"""
    
    git_info = {
        "is_git_repo": False,
        "branch": None,
        "status": {},
        "recent_commits": [],
        "remote_configured": False,
        "github_integration": False
    }
    
    try:
        # Check if it's a git repository
        result = subprocess.run(["git", "status"], capture_output=True, text=True, timeout=10)
        git_info["is_git_repo"] = result.returncode == 0
        
        if git_info["is_git_repo"]:
            # Get current branch
            branch_result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, timeout=5)
            if branch_result.returncode == 0:
                git_info["branch"] = branch_result.stdout.strip()
            
            # Get status
            status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5)
            if status_result.returncode == 0:
                status_lines = status_result.stdout.strip().split('\n')
                git_info["status"] = {
                    "modified_files": len([line for line in status_lines if line.startswith(' M') or line.startswith('M ')]),
                    "new_files": len([line for line in status_lines if line.startswith('A') or line.startswith('??')]),
                    "deleted_files": len([line for line in status_lines if line.startswith(' D') or line.startswith('D ')]),
                    "total_changes": len([line for line in status_lines if line.strip()])
                }
            
            # Get recent commits
            log_result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True, timeout=5)
            if log_result.returncode == 0:
                git_info["recent_commits"] = log_result.stdout.strip().split('\n')[:5]
            
            # Check for remote
            remote_result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, timeout=5)
            if remote_result.returncode == 0:
                remotes = remote_result.stdout.strip()
                git_info["remote_configured"] = bool(remotes)
                git_info["github_integration"] = "github.com" in remotes
        
    except Exception as e:
        git_info["error"] = str(e)
    
    return git_info


def _analyze_dependencies() -> Dict:
    """Analyzes project dependencies and package management"""
    
    deps_info = {
        "python_deps": {},
        "node_deps": {},
        "system_deps": {},
        "missing_deps": [],
        "outdated_deps": [],
        "security_issues": []
    }
    
    try:
        # Analyze Python dependencies
        if os.path.exists("pyproject.toml"):
            deps_info["python_deps"]["config_file"] = "pyproject.toml"
            deps_info["python_deps"]["package_manager"] = "pip/poetry"
        elif os.path.exists("requirements.txt"):
            deps_info["python_deps"]["config_file"] = "requirements.txt"
            deps_info["python_deps"]["package_manager"] = "pip"
            
            # Read requirements
            try:
                with open("requirements.txt", "r") as f:
                    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    deps_info["python_deps"]["requirements"] = requirements
                    deps_info["python_deps"]["count"] = len(requirements)
            except:
                pass
        
        # Analyze Node.js dependencies
        if os.path.exists("package.json"):
            try:
                with open("package.json", "r") as f:
                    package_data = json.load(f)
                    deps_info["node_deps"]["dependencies"] = package_data.get("dependencies", {})
                    deps_info["node_deps"]["dev_dependencies"] = package_data.get("devDependencies", {})
                    deps_info["node_deps"]["count"] = len(deps_info["node_deps"]["dependencies"])
            except:
                pass
        
        # Check for common missing dependencies
        missing = []
        if deps_info["python_deps"] and "streamlit" not in str(deps_info["python_deps"]):
            if os.path.exists("app.py"):
                # Check if app.py uses streamlit
                try:
                    with open("app.py", "r") as f:
                        if "streamlit" in f.read():
                            missing.append("streamlit")
                except:
                    pass
        
        deps_info["missing_deps"] = missing
        
    except Exception as e:
        deps_info["error"] = str(e)
    
    return deps_info


def _analyze_system_state() -> Dict:
    """Analyzes current system state and resource usage"""
    
    system_info = {
        "python_version": None,
        "platform": None,
        "working_directory": os.getcwd(),
        "environment_variables": {},
        "disk_space": {},
        "memory_info": {},
        "process_info": {}
    }
    
    try:
        # Python version
        import sys
        system_info["python_version"] = sys.version.split()[0]
        system_info["platform"] = sys.platform
        
        # Environment variables (filtered for security)
        env_vars = {}
        for key, value in os.environ.items():
            if any(keyword in key.upper() for keyword in ['REPL', 'PATH', 'HOME', 'USER']):
                if 'SECRET' not in key.upper() and 'TOKEN' not in key.upper():
                    env_vars[key] = value[:50] + "..." if len(value) > 50 else value
        system_info["environment_variables"] = env_vars
        
        # Disk space (if available)
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            system_info["disk_space"] = {
                "total_gb": round(total / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2),
                "usage_percent": round((used / total) * 100, 1)
            }
        except:
            pass
        
        # Process information
        try:
            import psutil
            process = psutil.Process()
            system_info["process_info"] = {
                "cpu_percent": process.cpu_percent(),
                "memory_mb": round(process.memory_info().rss / (1024**2), 2),
                "threads": process.num_threads()
            }
        except ImportError:
            system_info["process_info"] = {"note": "psutil not available"}
        
    except Exception as e:
        system_info["error"] = str(e)
    
    return system_info


def _assess_available_capabilities() -> Dict:
    """Assesses what capabilities are available in current environment"""
    
    capabilities = {
        "core_capabilities": [],
        "development_tools": [],
        "ai_integrations": [],
        "deployment_options": [],
        "limitations": []
    }
    
    try:
        # Core capabilities
        if os.path.exists("agent_loop.py"):
            capabilities["core_capabilities"].append("agi_cognitive_loop")
        if os.path.exists("core_agents"):
            capabilities["core_capabilities"].append("modular_agents")
        if os.path.exists("reflection.py"):
            capabilities["core_capabilities"].append("self_reflection")
        
        # Development tools
        if subprocess.run(["git", "--version"], capture_output=True).returncode == 0:
            capabilities["development_tools"].append("git_version_control")
        if subprocess.run(["python", "--version"], capture_output=True).returncode == 0:
            capabilities["development_tools"].append("python_runtime")
        
        # AI integrations
        if "OPENAI_API_KEY" in os.environ:
            capabilities["ai_integrations"].append("openai_api")
        if os.path.exists("utils/openai_helper.py"):
            capabilities["ai_integrations"].append("openai_helper")
        
        # Deployment options
        if os.path.exists("app.py") and os.path.exists(".streamlit"):
            capabilities["deployment_options"].append("streamlit_app")
        if "REPL_ID" in os.environ:
            capabilities["deployment_options"].append("replit_hosting")
        
        # Limitations
        if not capabilities["ai_integrations"]:
            capabilities["limitations"].append("no_ai_api_access")
        if not capabilities["development_tools"]:
            capabilities["limitations"].append("limited_dev_tools")
        
    except Exception as e:
        capabilities["error"] = str(e)
    
    return capabilities


def _identify_optimization_opportunities() -> List[Dict]:
    """Identifies optimization opportunities in the current environment"""
    
    opportunities = []
    
    try:
        # File organization opportunities
        py_files = glob.glob("*.py")
        if len(py_files) > 5:
            opportunities.append({
                "type": "organization",
                "description": "Multiple Python files in root - consider organizing into modules",
                "impact": "medium",
                "effort": "low"
            })
        
        # Documentation opportunities
        if not os.path.exists("README.md"):
            opportunities.append({
                "type": "documentation",
                "description": "Missing README.md - add project documentation",
                "impact": "high",
                "effort": "low"
            })
        
        # Configuration opportunities
        if not os.path.exists(".gitignore"):
            opportunities.append({
                "type": "configuration",
                "description": "Missing .gitignore - add to exclude unnecessary files",
                "impact": "medium",
                "effort": "low"
            })
        
        # Performance opportunities
        large_files = []
        for file_path in glob.glob("**/*.py", recursive=True):
            try:
                if os.path.getsize(file_path) > 10000:  # > 10KB
                    large_files.append(file_path)
            except:
                continue
        
        if large_files:
            opportunities.append({
                "type": "performance",
                "description": f"Large files detected ({len(large_files)}) - consider modularization",
                "impact": "medium",
                "effort": "medium"
            })
        
    except Exception as e:
        opportunities.append({
            "type": "error",
            "description": f"Error identifying opportunities: {str(e)}",
            "impact": "unknown",
            "effort": "unknown"
        })
    
    return opportunities


def _assess_security_posture() -> Dict:
    """Assesses security posture of the current environment"""
    
    security = {
        "score": 0.0,
        "strengths": [],
        "vulnerabilities": [],
        "recommendations": []
    }
    
    try:
        score = 0.5  # Base score
        
        # Check for secrets in code
        secrets_in_code = False
        for file_path in glob.glob("**/*.py", recursive=True):
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    if any(keyword in content for keyword in ['api_key', 'password', 'secret', 'token']):
                        # Check if it's actually hardcoded (not just variable names)
                        if any(pattern in content for pattern in ['= "', "= '", 'api_key="', "password='"]):
                            secrets_in_code = True
                            break
            except:
                continue
        
        if not secrets_in_code:
            security["strengths"].append("No hardcoded secrets detected")
            score += 0.2
        else:
            security["vulnerabilities"].append("Potential hardcoded secrets in code")
            security["recommendations"].append("Move secrets to environment variables")
        
        # Check for .gitignore
        if os.path.exists(".gitignore"):
            security["strengths"].append("Gitignore file present")
            score += 0.1
        else:
            security["vulnerabilities"].append("Missing .gitignore file")
            security["recommendations"].append("Add .gitignore to exclude sensitive files")
        
        # Check for environment variable usage
        if "DATABASE_URL" in os.environ or "OPENAI_API_KEY" in os.environ:
            security["strengths"].append("Using environment variables for configuration")
            score += 0.2
        
        security["score"] = min(1.0, score)
        
    except Exception as e:
        security["error"] = str(e)
    
    return security


def _determine_project_type(environment: Dict) -> str:
    """Determines the type of project based on environment analysis"""
    
    project_analysis = environment.get("project_analysis", {})
    replit_env = environment.get("replit_environment", {})
    
    # Check file types and structure
    file_types = project_analysis.get("file_types", {})
    
    if ".py" in file_types and file_types[".py"] > 3:
        if "streamlit_app" in replit_env.get("available_features", []):
            return "streamlit_application"
        elif os.path.exists("agent_loop.py") or os.path.exists("core_agents"):
            return "agi_system"
        else:
            return "python_application"
    elif ".js" in file_types or ".ts" in file_types:
        return "javascript_application"
    elif file_types.get(".md", 0) > file_types.get(".py", 0):
        return "documentation_project"
    else:
        return "unknown"


def _assess_project_maturity(environment: Dict) -> str:
    """Assesses the maturity level of the project"""
    
    project_analysis = environment.get("project_analysis", {})
    git_status = environment.get("git_status", {})
    capabilities = environment.get("capabilities", {})
    
    total_files = project_analysis.get("total_files", 0)
    has_git = git_status.get("is_git_repo", False)
    has_docs = len(project_analysis.get("documentation_files", [])) > 0
    has_tests = any("test" in f for f in project_analysis.get("code_files", []))
    core_capabilities = len(capabilities.get("core_capabilities", []))
    
    maturity_score = 0
    if total_files > 10:
        maturity_score += 1
    if has_git:
        maturity_score += 1
    if has_docs:
        maturity_score += 1
    if has_tests:
        maturity_score += 1
    if core_capabilities > 2:
        maturity_score += 1
    
    if maturity_score >= 4:
        return "mature"
    elif maturity_score >= 2:
        return "developing"
    else:
        return "early"


def _calculate_structure_quality(analysis: Dict) -> float:
    """Calculates the quality of project structure"""
    
    score = 0.5  # Base score
    
    # Points for organization
    total_files = analysis.get("total_files", 0)
    if total_files > 0:
        # Prefer files in subdirectories rather than root
        root_files = len([f for f in analysis.get("code_files", []) if '/' not in f.replace('./', '')])
        if total_files > 5 and root_files < total_files * 0.3:
            score += 0.2
        
        # Points for having different file types
        file_types = len(analysis.get("file_types", {}))
        if file_types > 2:
            score += 0.1
        
        # Points for documentation
        if analysis.get("documentation_files"):
            score += 0.2
    
    return min(1.0, score)


def _calculate_readiness_score(environment: Dict) -> float:
    """Calculates overall readiness score for AGI operations"""
    
    score = 0.0
    
    # Core capabilities (40%)
    capabilities = environment.get("capabilities", {})
    core_caps = len(capabilities.get("core_capabilities", []))
    score += min(0.4, core_caps * 0.1)
    
    # Project maturity (30%)
    maturity = environment.get("project_maturity", "early")
    maturity_scores = {"early": 0.1, "developing": 0.2, "mature": 0.3}
    score += maturity_scores.get(maturity, 0.0)
    
    # Environment setup (20%)
    replit_env = environment.get("replit_environment", {})
    if replit_env.get("is_replit", False):
        score += 0.1
    if replit_env.get("deployment_ready", False):
        score += 0.1
    
    # Security and optimization (10%)
    security = environment.get("security_assessment", {})
    security_score = security.get("score", 0.0)
    score += security_score * 0.1
    
    return min(1.0, score)


if __name__ == "__main__":
    # Test the environment scanner
    env_data = scan_environment()
    
    print(f"Project Type: {env_data['project_type']}")
    print(f"Project Maturity: {env_data['project_maturity']}")
    print(f"Readiness Score: {env_data['readiness_score']:.2f}")
    print(f"Total Files: {env_data['project_analysis']['total_files']}")
    print(f"Core Capabilities: {len(env_data['capabilities']['core_capabilities'])}")
    
    if env_data.get("optimization_opportunities"):
        print(f"Optimization Opportunities: {len(env_data['optimization_opportunities'])}")
        for opp in env_data["optimization_opportunities"][:3]:
            print(f"  - {opp['description']}")
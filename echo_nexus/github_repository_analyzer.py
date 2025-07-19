#!/usr/bin/env python3
"""
GitHub Repository Analyzer for EchoNexus
Analyzes all repositories for user Joeromance84 and integrates existing code
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime

try:
    from github import Github
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False

class GitHubRepositoryAnalyzer:
    """
    Analyzes all user repositories and integrates existing code into Echo system
    """
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_client = None
        self.user_repos = []
        self.code_analysis = {}
        
        if PYGITHUB_AVAILABLE and self.github_token:
            try:
                self.github_client = Github(self.github_token)
                print("GitHub client initialized successfully")
            except Exception as e:
                print(f"GitHub initialization failed: {e}")
        else:
            print("GitHub token not available or PyGithub not installed")
    
    def analyze_all_repositories(self, username: str = "Joeromance84") -> Dict[str, Any]:
        """
        Analyze all repositories for the specified user
        """
        
        if not self.github_client:
            return {"error": "GitHub client not available"}
        
        try:
            # Get user and their repositories
            user = self.github_client.get_user(username)
            repos = list(user.get_repos())
            
            print(f"Found {len(repos)} repositories for user {username}")
            
            analysis_results = {
                "user": username,
                "total_repositories": len(repos),
                "repositories": {},
                "code_patterns": {},
                "integration_opportunities": [],
                "timestamp": datetime.now().isoformat()
            }
            
            for repo in repos:
                repo_analysis = self.analyze_repository(repo)
                analysis_results["repositories"][repo.name] = repo_analysis
                
                # Look for integration opportunities
                self.identify_integration_opportunities(repo, repo_analysis, analysis_results)
            
            # Generate comprehensive integration plan
            analysis_results["integration_plan"] = self.generate_integration_plan(analysis_results)
            
            # Save analysis results
            self.save_analysis_results(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            print(f"Repository analysis failed: {e}")
            return {"error": str(e)}
    
    def analyze_repository(self, repo) -> Dict[str, Any]:
        """
        Perform deep analysis of a single repository
        """
        
        try:
            repo_info = {
                "name": repo.name,
                "description": repo.description,
                "language": repo.language,
                "size": repo.size,
                "created_at": repo.created_at.isoformat() if repo.created_at else None,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "private": repo.private,
                "has_workflows": False,
                "file_structure": {},
                "code_files": [],
                "build_systems": [],
                "dependencies": [],
                "workflows": [],
                "echo_integration_potential": "unknown"
            }
            
            # Analyze repository contents
            try:
                contents = repo.get_contents("")
                repo_info["file_structure"] = self.analyze_file_structure(repo, contents)
                
                # Look for specific files
                self.analyze_special_files(repo, repo_info)
                
                # Check for GitHub Actions workflows
                try:
                    workflows_dir = repo.get_contents(".github/workflows")
                    repo_info["has_workflows"] = True
                    repo_info["workflows"] = [wf.name for wf in workflows_dir if wf.name.endswith('.yml')]
                except:
                    pass
                
                # Analyze Echo integration potential
                repo_info["echo_integration_potential"] = self.assess_echo_integration(repo_info)
                
            except Exception as e:
                repo_info["analysis_error"] = str(e)
            
            return repo_info
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_file_structure(self, repo, contents, path="", max_depth=3, current_depth=0) -> Dict[str, Any]:
        """
        Recursively analyze file structure
        """
        
        if current_depth >= max_depth:
            return {"truncated": True}
        
        structure = {}
        
        try:
            for content in contents:
                if content.type == "dir":
                    try:
                        subcontents = repo.get_contents(content.path)
                        structure[content.name] = self.analyze_file_structure(
                            repo, subcontents, content.path, max_depth, current_depth + 1
                        )
                    except:
                        structure[content.name] = {"error": "Cannot access directory"}
                else:
                    # Analyze file
                    file_info = {
                        "type": "file",
                        "size": content.size,
                        "path": content.path
                    }
                    
                    # Check if it's a code file we can analyze
                    if self.is_analyzable_file(content.name):
                        file_info["analyzable"] = True
                        
                        # For smaller files, get content for analysis
                        if content.size < 50000:  # 50KB limit
                            try:
                                file_content = content.decoded_content.decode('utf-8')
                                file_info["content_preview"] = file_content[:500]
                                file_info["line_count"] = len(file_content.split('\n'))
                                
                                # Analyze code patterns
                                if content.name.endswith('.py'):
                                    file_info["python_analysis"] = self.analyze_python_file(file_content)
                                elif content.name.endswith('.yml') or content.name.endswith('.yaml'):
                                    file_info["yaml_analysis"] = self.analyze_yaml_file(file_content)
                                
                            except:
                                file_info["content_error"] = "Cannot decode file content"
                    
                    structure[content.name] = file_info
            
            return structure
            
        except Exception as e:
            return {"error": str(e)}
    
    def is_analyzable_file(self, filename: str) -> bool:
        """Check if file is analyzable"""
        analyzable_extensions = [
            '.py', '.js', '.yml', '.yaml', '.json', '.md', '.txt',
            '.java', '.kt', '.spec', '.cfg', '.ini', '.toml'
        ]
        return any(filename.endswith(ext) for ext in analyzable_extensions)
    
    def analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Analyze Python file content"""
        
        analysis = {
            "imports": [],
            "classes": [],
            "functions": [],
            "has_main": False,
            "frameworks": []
        }
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Find imports
            if line.startswith('import ') or line.startswith('from '):
                analysis["imports"].append(line)
            
            # Find classes
            elif line.startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').strip(':')
                analysis["classes"].append(class_name)
            
            # Find functions
            elif line.startswith('def '):
                func_name = line.split('(')[0].replace('def ', '')
                analysis["functions"].append(func_name)
                
                if func_name == "main":
                    analysis["has_main"] = True
        
        # Detect frameworks
        frameworks = {
            'streamlit': ['import streamlit', 'streamlit as st'],
            'kivy': ['from kivy', 'import kivy'],
            'flask': ['from flask', 'import flask'],
            'fastapi': ['from fastapi', 'import fastapi'],
            'django': ['from django', 'import django'],
            'buildozer': ['buildozer'],
            'opencv': ['import cv2', 'from cv2'],
            'openai': ['import openai', 'from openai'],
            'github': ['from github', 'import github']
        }
        
        content_lower = content.lower()
        for framework, indicators in frameworks.items():
            if any(indicator.lower() in content_lower for indicator in indicators):
                analysis["frameworks"].append(framework)
        
        return analysis
    
    def analyze_yaml_file(self, content: str) -> Dict[str, Any]:
        """Analyze YAML file content"""
        
        analysis = {
            "type": "unknown",
            "triggers": [],
            "jobs": [],
            "actions_used": []
        }
        
        content_lower = content.lower()
        
        # Detect file type
        if 'on:' in content and ('push:' in content or 'pull_request:' in content):
            analysis["type"] = "github_actions"
        elif 'buildozer' in content_lower:
            analysis["type"] = "buildozer_spec"
        elif 'version:' in content and 'dependencies:' in content:
            analysis["type"] = "dependencies"
        
        # For GitHub Actions, extract more details
        if analysis["type"] == "github_actions":
            lines = content.split('\n')
            current_job = None
            
            for line in lines:
                line = line.strip()
                
                if 'uses: ' in line:
                    action = line.split('uses: ')[1].strip()
                    analysis["actions_used"].append(action)
                
                if line.endswith(':') and not line.startswith('#'):
                    if 'jobs:' in line:
                        continue
                    elif line.count(':') == 1:
                        potential_job = line.replace(':', '').strip()
                        if len(potential_job) > 0 and potential_job not in ['on', 'env', 'jobs']:
                            analysis["jobs"].append(potential_job)
        
        return analysis
    
    def analyze_special_files(self, repo, repo_info: Dict[str, Any]):
        """Analyze special configuration files"""
        
        special_files = {
            'requirements.txt': 'python_dependencies',
            'package.json': 'nodejs_dependencies',
            'buildozer.spec': 'android_build_config',
            'Dockerfile': 'docker_config',
            'README.md': 'documentation',
            '.gitignore': 'git_config',
            'setup.py': 'python_package',
            'pyproject.toml': 'python_project_config'
        }
        
        for filename, file_type in special_files.items():
            try:
                file_content = repo.get_contents(filename)
                repo_info[file_type] = {
                    "present": True,
                    "size": file_content.size,
                    "path": file_content.path
                }
                
                # For key files, get content
                if filename in ['buildozer.spec', 'requirements.txt', 'package.json'] and file_content.size < 10000:
                    try:
                        content = file_content.decoded_content.decode('utf-8')
                        repo_info[file_type]["content"] = content[:1000]  # First 1000 chars
                    except:
                        pass
                        
            except:
                repo_info[file_type] = {"present": False}
    
    def assess_echo_integration(self, repo_info: Dict[str, Any]) -> str:
        """Assess potential for Echo integration"""
        
        # High potential indicators
        high_indicators = [
            repo_info.get("language") == "Python",
            "streamlit" in str(repo_info.get("python_analysis", {}).get("frameworks", [])),
            "kivy" in str(repo_info.get("python_analysis", {}).get("frameworks", [])),
            repo_info.get("buildozer_spec", {}).get("present", False),
            repo_info.get("has_workflows", False),
            "ai" in repo_info.get("name", "").lower(),
            "echo" in repo_info.get("name", "").lower(),
            "builder" in repo_info.get("name", "").lower()
        ]
        
        # Medium potential indicators
        medium_indicators = [
            repo_info.get("python_dependencies", {}).get("present", False),
            "github" in str(repo_info.get("python_analysis", {}).get("frameworks", [])),
            "openai" in str(repo_info.get("python_analysis", {}).get("frameworks", [])),
            len(repo_info.get("workflows", [])) > 0
        ]
        
        high_score = sum(high_indicators)
        medium_score = sum(medium_indicators)
        
        if high_score >= 3:
            return "high"
        elif high_score >= 1 or medium_score >= 2:
            return "medium"
        else:
            return "low"
    
    def identify_integration_opportunities(self, repo, repo_analysis: Dict[str, Any], results: Dict[str, Any]):
        """Identify specific integration opportunities"""
        
        opportunities = []
        
        # Check for existing APK builders
        if repo_analysis.get("buildozer_spec", {}).get("present", False):
            opportunities.append({
                "type": "apk_integration",
                "repository": repo.name,
                "description": "Existing buildozer.spec can be enhanced with Echo Core",
                "priority": "high"
            })
        
        # Check for GitHub Actions workflows
        if repo_analysis.get("has_workflows", False):
            opportunities.append({
                "type": "workflow_enhancement",
                "repository": repo.name,
                "description": "Existing workflows can be optimized with Echo intelligence",
                "priority": "medium"
            })
        
        # Check for AI/ML projects
        frameworks = repo_analysis.get("python_analysis", {}).get("frameworks", [])
        if "openai" in frameworks or "ai" in repo.name.lower():
            opportunities.append({
                "type": "ai_integration",
                "repository": repo.name,
                "description": "AI capabilities can be integrated with Echo cost optimization",
                "priority": "high"
            })
        
        results["integration_opportunities"].extend(opportunities)
    
    def generate_integration_plan(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive integration plan"""
        
        plan = {
            "priority_repositories": [],
            "integration_steps": [],
            "code_consolidation": [],
            "workflow_optimization": [],
            "estimated_timeline": "unknown"
        }
        
        # Identify priority repositories
        repos = analysis_results.get("repositories", {})
        for repo_name, repo_info in repos.items():
            potential = repo_info.get("echo_integration_potential", "low")
            if potential in ["high", "medium"]:
                plan["priority_repositories"].append({
                    "name": repo_name,
                    "potential": potential,
                    "reasons": self.get_integration_reasons(repo_info)
                })
        
        # Generate integration steps
        if len(plan["priority_repositories"]) > 0:
            plan["integration_steps"] = [
                "Analyze existing code patterns across all repositories",
                "Consolidate common functionality into Echo core modules",
                "Migrate existing workflows to Echo-optimized versions",
                "Integrate existing APK build systems with Echo Core",
                "Establish unified cost optimization across all projects",
                "Create master repository with federated control system"
            ]
        
        return plan
    
    def get_integration_reasons(self, repo_info: Dict[str, Any]) -> List[str]:
        """Get reasons why repository has integration potential"""
        
        reasons = []
        
        if repo_info.get("language") == "Python":
            reasons.append("Python codebase compatible with Echo")
        
        if repo_info.get("buildozer_spec", {}).get("present", False):
            reasons.append("Existing APK build configuration")
        
        if repo_info.get("has_workflows", False):
            reasons.append("GitHub Actions workflows present")
        
        frameworks = repo_info.get("python_analysis", {}).get("frameworks", [])
        if "streamlit" in frameworks:
            reasons.append("Streamlit framework matches Echo interface")
        
        if "openai" in frameworks:
            reasons.append("AI capabilities can be cost-optimized")
        
        return reasons
    
    def save_analysis_results(self, results: Dict[str, Any]):
        """Save analysis results to file"""
        
        try:
            with open("github_repository_analysis.json", "w") as f:
                json.dump(results, f, indent=2)
            print("Analysis results saved to github_repository_analysis.json")
        except Exception as e:
            print(f"Failed to save analysis results: {e}")

# Test the analyzer
if __name__ == "__main__":
    analyzer = GitHubRepositoryAnalyzer()
    
    print("=== Analyzing All Repositories for Joeromance84 ===")
    results = analyzer.analyze_all_repositories("Joeromance84")
    
    if "error" not in results:
        print(f"\nFound {results['total_repositories']} repositories")
        print(f"Integration opportunities: {len(results['integration_opportunities'])}")
        
        for repo_name, repo_info in results["repositories"].items():
            potential = repo_info.get("echo_integration_potential", "unknown")
            print(f"  {repo_name}: {potential} integration potential")
    else:
        print(f"Analysis failed: {results['error']}")
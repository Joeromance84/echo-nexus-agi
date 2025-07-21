#!/usr/bin/env python3
"""
GitHub Status Checker - Monitor repository and push protection status
"""

import requests
import os
from datetime import datetime

def check_github_push_status():
    """Check GitHub repository accessibility and push status"""
    try:
        # Check if we have GitHub token
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            return "⚠️ No GitHub token found in environment"
        
        # Test GitHub API access
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(
            "https://api.github.com/user", 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return f"✅ GitHub API accessible (User: {user_data.get('login', 'Unknown')})"
        elif response.status_code == 401:
            return "🚫 GitHub token invalid or expired"
        elif response.status_code == 403:
            return "🚫 GitHub token lacks required permissions"
        else:
            return f"⚠️ GitHub API response: {response.status_code}"
            
    except requests.RequestException as e:
        return f"❌ GitHub connection failed: {str(e)}"
    except Exception as e:
        return f"❌ GitHub status check error: {str(e)}"

def check_repo_status(repo_owner, repo_name):
    """Check specific repository status"""
    try:
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            return "⚠️ No GitHub token for repo check"
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            return {
                "status": "✅ Repository accessible",
                "private": repo_data.get('private', False),
                "last_push": repo_data.get('pushed_at', 'Unknown'),
                "default_branch": repo_data.get('default_branch', 'main')
            }
        elif response.status_code == 404:
            return {"status": "❌ Repository not found or no access"}
        else:
            return {"status": f"⚠️ Repository check failed: {response.status_code}"}
            
    except Exception as e:
        return {"status": f"❌ Repository status error: {str(e)}"}

def get_push_protection_info():
    """Get information about push protection blocks"""
    return {
        "common_causes": [
            "Hardcoded GitHub tokens in commit history",
            "API keys or secrets in code files", 
            "Personal access tokens in configuration"
        ],
        "solutions": [
            "Use environment variables for secrets",
            "Add secrets to .gitignore",
            "Use GitHub Secrets for CI/CD",
            "Clean commit history with git filter-repo"
        ]
    }
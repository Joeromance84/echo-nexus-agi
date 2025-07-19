#!/usr/bin/env python3
"""
GitHub Authentication and Repository Verification System
Secure GitHub integration with token validation and repository access
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import webbrowser
import urllib.parse

class GitHubAuthenticator:
    """
    GitHub authentication and repository verification system
    """
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.auth_cache_file = '.github_auth_cache.json'
        self.user_info = None
        self.repositories = []
        
    def verify_connection(self) -> Dict[str, Any]:
        """Verify GitHub connection and retrieve user information"""
        
        if not self.github_token:
            return {
                'status': 'error',
                'message': 'No GitHub token found. Please set GITHUB_TOKEN environment variable.',
                'authenticated': False,
                'setup_required': True
            }
        
        try:
            # Test authentication with user endpoint
            headers = {
                'Authorization': f'Bearer {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(f'{self.base_url}/user', headers=headers)
            
            if response.status_code == 200:
                self.user_info = response.json()
                
                # Cache authentication info
                self._cache_auth_info(self.user_info)
                
                return {
                    'status': 'success',
                    'message': 'GitHub connection verified successfully',
                    'authenticated': True,
                    'user': {
                        'login': self.user_info.get('login'),
                        'name': self.user_info.get('name'),
                        'email': self.user_info.get('email'),
                        'public_repos': self.user_info.get('public_repos'),
                        'private_repos': self.user_info.get('total_private_repos', 0)
                    },
                    'token_scopes': response.headers.get('X-OAuth-Scopes', '').split(', ') if response.headers.get('X-OAuth-Scopes') else []
                }
            
            elif response.status_code == 401:
                return {
                    'status': 'error',
                    'message': 'GitHub token is invalid or expired',
                    'authenticated': False,
                    'setup_required': True
                }
            
            else:
                return {
                    'status': 'error',
                    'message': f'GitHub API error: {response.status_code} - {response.text}',
                    'authenticated': False
                }
        
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}',
                'authenticated': False
            }
    
    def get_repositories(self, include_private: bool = True, per_page: int = 100) -> Dict[str, Any]:
        """Retrieve user's GitHub repositories"""
        
        if not self.github_token:
            return {
                'status': 'error',
                'message': 'GitHub token required',
                'repositories': []
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            repositories = []
            page = 1
            
            while True:
                params = {
                    'type': 'all' if include_private else 'public',
                    'sort': 'updated',
                    'direction': 'desc',
                    'per_page': per_page,
                    'page': page
                }
                
                response = requests.get(f'{self.base_url}/user/repos', headers=headers, params=params)
                
                if response.status_code != 200:
                    break
                
                page_repos = response.json()
                if not page_repos:
                    break
                
                repositories.extend(page_repos)
                
                # Stop if we got less than a full page
                if len(page_repos) < per_page:
                    break
                
                page += 1
            
            # Process and filter repositories
            processed_repos = []
            for repo in repositories:
                processed_repos.append({
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo.get('description', ''),
                    'private': repo['private'],
                    'url': repo['html_url'],
                    'clone_url': repo['clone_url'],
                    'ssh_url': repo['ssh_url'],
                    'language': repo.get('language'),
                    'size': repo['size'],
                    'updated_at': repo['updated_at'],
                    'has_actions': self._check_github_actions(repo['full_name']),
                    'default_branch': repo['default_branch']
                })
            
            self.repositories = processed_repos
            
            return {
                'status': 'success',
                'message': f'Retrieved {len(processed_repos)} repositories',
                'repositories': processed_repos,
                'total_count': len(processed_repos)
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to retrieve repositories: {str(e)}',
                'repositories': []
            }
    
    def _check_github_actions(self, repo_full_name: str) -> bool:
        """Check if repository has GitHub Actions workflows"""
        
        try:
            headers = {
                'Authorization': f'Bearer {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(f'{self.base_url}/repos/{repo_full_name}/actions/workflows', headers=headers)
            
            if response.status_code == 200:
                workflows = response.json()
                return workflows.get('total_count', 0) > 0
            
            return False
        
        except Exception:
            return False
    
    def create_processor_repository(self, repo_name: str, description: str, processor_type: str) -> Dict[str, Any]:
        """Create a new repository for EchoNexus processor"""
        
        if not self.github_token:
            return {
                'status': 'error',
                'message': 'GitHub token required'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            repo_data = {
                'name': repo_name,
                'description': f'{description} - EchoNexus {processor_type} Processor',
                'private': False,
                'auto_init': True,
                'gitignore_template': 'Python',
                'license_template': 'mit'
            }
            
            response = requests.post(f'{self.base_url}/user/repos', headers=headers, json=repo_data)
            
            if response.status_code == 201:
                repo_info = response.json()
                
                # Add EchoNexus workflow template
                workflow_result = self._add_processor_workflow(repo_info['full_name'], processor_type)
                
                return {
                    'status': 'success',
                    'message': f'Repository {repo_name} created successfully',
                    'repository': {
                        'name': repo_info['name'],
                        'full_name': repo_info['full_name'],
                        'url': repo_info['html_url'],
                        'clone_url': repo_info['clone_url']
                    },
                    'workflow_added': workflow_result['status'] == 'success'
                }
            
            else:
                error_data = response.json()
                return {
                    'status': 'error',
                    'message': f'Failed to create repository: {error_data.get("message", response.text)}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Repository creation failed: {str(e)}'
            }
    
    def _add_processor_workflow(self, repo_full_name: str, processor_type: str) -> Dict[str, Any]:
        """Add EchoNexus processor workflow to repository"""
        
        try:
            # Load workflow template
            workflow_template_path = Path('templates/github_action_template.yml')
            if not workflow_template_path.exists():
                return {
                    'status': 'error',
                    'message': 'Workflow template not found'
                }
            
            with open(workflow_template_path, 'r') as f:
                workflow_content = f.read()
            
            # Customize workflow for processor type
            workflow_content = workflow_content.replace(
                'EchoNexus Processor Template',
                f'EchoNexus {processor_type.title()} Processor'
            )
            
            # Create workflow file in repository
            headers = {
                'Authorization': f'Bearer {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            file_data = {
                'message': f'Add EchoNexus {processor_type} processor workflow',
                'content': self._encode_content(workflow_content)
            }
            
            response = requests.put(
                f'{self.base_url}/repos/{repo_full_name}/contents/.github/workflows/processor.yml',
                headers=headers,
                json=file_data
            )
            
            if response.status_code in [200, 201]:
                return {
                    'status': 'success',
                    'message': 'Workflow added successfully'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Failed to add workflow: {response.text}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Workflow addition failed: {str(e)}'
            }
    
    def _encode_content(self, content: str) -> str:
        """Encode content for GitHub API"""
        import base64
        return base64.b64encode(content.encode()).decode()
    
    def setup_processor_network(self, processors: List[str]) -> Dict[str, Any]:
        """Setup complete processor network for EchoNexus"""
        
        setup_results = {
            'status': 'in_progress',
            'processors': {},
            'created_repos': [],
            'failed_repos': []
        }
        
        for processor in processors:
            repo_name = f'echo-nexus-{processor.replace("_", "-")}'
            
            print(f"Creating processor repository: {repo_name}")
            
            result = self.create_processor_repository(
                repo_name=repo_name,
                description=f'EchoNexus {processor.replace("_", " ").title()} Processor',
                processor_type=processor
            )
            
            setup_results['processors'][processor] = result
            
            if result['status'] == 'success':
                setup_results['created_repos'].append(result['repository'])
            else:
                setup_results['failed_repos'].append({
                    'processor': processor,
                    'error': result['message']
                })
            
            # Brief pause between repository creations
            time.sleep(1)
        
        setup_results['status'] = 'completed'
        setup_results['success_count'] = len(setup_results['created_repos'])
        setup_results['failure_count'] = len(setup_results['failed_repos'])
        
        return setup_results
    
    def generate_auth_instructions(self) -> Dict[str, Any]:
        """Generate instructions for GitHub authentication setup"""
        
        return {
            'instructions': [
                {
                    'step': 1,
                    'title': 'Create GitHub Personal Access Token',
                    'description': 'Go to GitHub Settings > Developer settings > Personal access tokens',
                    'url': 'https://github.com/settings/tokens/new',
                    'required_scopes': [
                        'repo (Full control of private repositories)',
                        'workflow (Update GitHub Action workflows)',
                        'admin:repo_hook (Admin access to repository hooks)',
                        'user (Read user profile data)'
                    ]
                },
                {
                    'step': 2,
                    'title': 'Set Environment Variable',
                    'description': 'Set the GITHUB_TOKEN environment variable in Replit',
                    'instructions': [
                        'Open Replit Secrets panel',
                        'Add new secret: GITHUB_TOKEN',
                        'Paste your GitHub Personal Access Token as the value',
                        'Save the secret'
                    ]
                },
                {
                    'step': 3,
                    'title': 'Verify Connection',
                    'description': 'Run the verification function to test the connection',
                    'command': 'python -c "from utils.github_authenticator import GitHubAuthenticator; auth = GitHubAuthenticator(); print(auth.verify_connection())"'
                }
            ],
            'token_requirements': {
                'minimum_scopes': ['repo', 'workflow', 'user'],
                'recommended_scopes': ['repo', 'workflow', 'admin:repo_hook', 'user', 'admin:org'],
                'expiration': 'No expiration recommended for continuous operation'
            }
        }
    
    def _cache_auth_info(self, user_info: Dict[str, Any]):
        """Cache authentication information"""
        
        try:
            cache_data = {
                'user_info': user_info,
                'cached_at': datetime.now().isoformat(),
                'token_hash': hash(self.github_token) if self.github_token else None
            }
            
            with open(self.auth_cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        
        except Exception as e:
            print(f"Warning: Could not cache auth info: {e}")
    
    def get_cached_auth_info(self) -> Optional[Dict[str, Any]]:
        """Get cached authentication information"""
        
        try:
            if os.path.exists(self.auth_cache_file):
                with open(self.auth_cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is recent (within 24 hours)
                cached_time = datetime.fromisoformat(cache_data['cached_at'])
                if (datetime.now() - cached_time).total_seconds() < 86400:
                    return cache_data
            
            return None
        
        except Exception:
            return None


def interactive_github_setup():
    """Interactive GitHub setup and verification"""
    
    print("EchoNexus GitHub Integration Setup")
    print("=" * 40)
    
    authenticator = GitHubAuthenticator()
    
    # Check current connection status
    print("Checking GitHub connection...")
    connection_status = authenticator.verify_connection()
    
    if connection_status['authenticated']:
        print(f"✓ Connected as: {connection_status['user']['login']}")
        print(f"✓ Public repositories: {connection_status['user']['public_repos']}")
        print(f"✓ Private repositories: {connection_status['user']['private_repos']}")
        
        # Get repositories
        print("\nRetrieving repositories...")
        repos_result = authenticator.get_repositories()
        
        if repos_result['status'] == 'success':
            print(f"✓ Found {repos_result['total_count']} repositories")
            
            # Show some repository details
            for repo in repos_result['repositories'][:5]:
                actions_status = "✓" if repo['has_actions'] else "✗"
                print(f"  {actions_status} {repo['name']} ({repo['language'] or 'Unknown'})")
            
            if len(repos_result['repositories']) > 5:
                print(f"  ... and {len(repos_result['repositories']) - 5} more")
        
        # Setup processor network option
        setup_network = input("\nSetup EchoNexus processor network? (y/n): ").lower().strip()
        
        if setup_network == 'y':
            processors = [
                'text_analysis',
                'code_generation', 
                'diagnostic_scan',
                'workflow_synthesis',
                'knowledge_synthesis'
            ]
            
            print(f"\nSetting up {len(processors)} processor repositories...")
            setup_result = authenticator.setup_processor_network(processors)
            
            print(f"✓ Created {setup_result['success_count']} repositories")
            if setup_result['failure_count'] > 0:
                print(f"✗ Failed to create {setup_result['failure_count']} repositories")
                for failed in setup_result['failed_repos']:
                    print(f"  - {failed['processor']}: {failed['error']}")
    
    else:
        print(f"✗ Connection failed: {connection_status['message']}")
        
        if connection_status.get('setup_required'):
            print("\nSetup Instructions:")
            instructions = authenticator.generate_auth_instructions()
            
            for instruction in instructions['instructions']:
                print(f"\n{instruction['step']}. {instruction['title']}")
                print(f"   {instruction['description']}")
                
                if 'url' in instruction:
                    print(f"   URL: {instruction['url']}")
                
                if 'required_scopes' in instruction:
                    print("   Required scopes:")
                    for scope in instruction['required_scopes']:
                        print(f"     - {scope}")
                
                if 'instructions' in instruction:
                    for sub_instruction in instruction['instructions']:
                        print(f"     • {sub_instruction}")
                
                if 'command' in instruction:
                    print(f"   Command: {instruction['command']}")
    
    print("\nGitHub setup completed!")


if __name__ == "__main__":
    interactive_github_setup()
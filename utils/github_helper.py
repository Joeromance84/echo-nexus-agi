import os
import requests
from typing import Dict, List, Any, Optional
import base64
import json
from github import Github
from github.GithubException import GithubException, UnknownObjectException, BadCredentialsException

class GitHubHelper:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", None)
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "APK-Builder-Assistant"
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            # Initialize PyGithub client for advanced API operations
            self.github = Github(self.token)
        else:
            self.github = None
    
    def validate_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Validate if repository exists and is accessible
        """
        result = {
            'valid': False,
            'accessible': False,
            'has_workflows': False,
            'has_buildozer_spec': False,
            'error': None
        }
        
        try:
            # Extract owner and repo from URL
            if 'github.com' in repo_url:
                parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                else:
                    result['error'] = "Invalid GitHub repository URL format"
                    return result
            else:
                result['error'] = "Not a GitHub repository URL"
                return result
            
            # Check if repository exists
            repo_response = self._make_request(f"/repos/{owner}/{repo}")
            if repo_response.status_code == 200:
                result['valid'] = True
                result['accessible'] = True
                
                # Check for workflows directory
                workflows_response = self._make_request(f"/repos/{owner}/{repo}/contents/.github/workflows")
                if workflows_response.status_code == 200:
                    result['has_workflows'] = True
                
                # Check for buildozer.spec
                buildozer_response = self._make_request(f"/repos/{owner}/{repo}/contents/buildozer.spec")
                if buildozer_response.status_code == 200:
                    result['has_buildozer_spec'] = True
                
            elif repo_response.status_code == 404:
                result['error'] = "Repository not found or not accessible"
            elif repo_response.status_code == 403:
                result['error'] = "Access forbidden - check permissions"
            else:
                result['error'] = f"API error: {repo_response.status_code}"
                
        except Exception as e:
            result['error'] = f"Error validating repository: {str(e)}"
        
        return result
    
    def get_workflow_runs(self, owner: str, repo: str, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get workflow run history for a repository
        """
        result = {
            'success': False,
            'runs': [],
            'error': None
        }
        
        try:
            if not self.token:
                result['error'] = "GitHub token required for accessing workflow runs"
                return result
            
            endpoint = f"/repos/{owner}/{repo}/actions/runs"
            if workflow_id:
                endpoint = f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
            
            response = self._make_request(endpoint)
            
            if response.status_code == 200:
                data = response.json()
                result['success'] = True
                result['runs'] = data.get('workflow_runs', [])
            else:
                result['error'] = f"Failed to fetch workflow runs: {response.status_code}"
                
        except Exception as e:
            result['error'] = f"Error fetching workflow runs: {str(e)}"
        
        return result
    
    def analyze_workflow_failures(self, owner: str, repo: str, run_id: str) -> Dict[str, Any]:
        """
        Analyze a failed workflow run to identify common issues
        """
        result = {
            'success': False,
            'analysis': {},
            'suggestions': [],
            'error': None
        }
        
        try:
            if not self.token:
                result['error'] = "GitHub token required for accessing workflow details"
                return result
            
            # Get workflow run details
            run_response = self._make_request(f"/repos/{owner}/{repo}/actions/runs/{run_id}")
            if run_response.status_code != 200:
                result['error'] = f"Failed to fetch workflow run: {run_response.status_code}"
                return result
            
            run_data = run_response.json()
            
            # Get job details
            jobs_response = self._make_request(f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs")
            if jobs_response.status_code != 200:
                result['error'] = f"Failed to fetch job details: {jobs_response.status_code}"
                return result
            
            jobs_data = jobs_response.json()
            
            # Analyze failures
            result['analysis'] = self._analyze_job_failures(jobs_data.get('jobs', []))
            result['suggestions'] = self._generate_failure_suggestions(result['analysis'])
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Error analyzing workflow failures: {str(e)}"
        
        return result
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> requests.Response:
        """
        Make authenticated request to GitHub API
        """
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            return requests.get(url, headers=self.headers)
        elif method == "POST":
            return requests.post(url, headers=self.headers, json=data)
        elif method == "PUT":
            return requests.put(url, headers=self.headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    def _analyze_job_failures(self, jobs: List[Dict]) -> Dict[str, Any]:
        """
        Analyze job failures and categorize common issues
        """
        analysis = {
            'failed_jobs': [],
            'common_issues': [],
            'error_patterns': {}
        }
        
        for job in jobs:
            if job.get('conclusion') == 'failure':
                job_analysis = {
                    'name': job.get('name'),
                    'started_at': job.get('started_at'),
                    'completed_at': job.get('completed_at'),
                    'steps': []
                }
                
                # Analyze failed steps
                for step in job.get('steps', []):
                    if step.get('conclusion') == 'failure':
                        step_analysis = {
                            'name': step.get('name'),
                            'number': step.get('number'),
                            'started_at': step.get('started_at'),
                            'completed_at': step.get('completed_at')
                        }
                        job_analysis['steps'].append(step_analysis)
                
                analysis['failed_jobs'].append(job_analysis)
        
        return analysis
    
    def _generate_failure_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate suggestions based on failure analysis
        """
        suggestions = []
        
        if not analysis.get('failed_jobs'):
            return suggestions
        
        # Common APK build failure suggestions
        suggestions.extend([
            "Check Java version compatibility (OpenJDK 8 or 11 recommended)",
            "Verify Android SDK installation and configuration",
            "Ensure buildozer.spec file is properly configured",
            "Check Python version compatibility with your dependencies",
            "Verify all required system packages are installed",
            "Check if sufficient disk space is available for the build",
            "Review dependency versions in requirements.txt",
            "Ensure proper permissions for build tools"
        ])
        
        return suggestions
    
    def create_workflow_file(self, owner: str, repo: str, workflow_content: str, 
                           filename: str, commit_message: str) -> Dict[str, Any]:
        """
        Create or update a workflow file in the repository
        """
        result = {
            'success': False,
            'sha': None,
            'error': None
        }
        
        try:
            if not self.token:
                result['error'] = "GitHub token required for creating workflow files"
                return result
            
            # Check if file exists
            file_path = f".github/workflows/{filename}"
            existing_response = self._make_request(f"/repos/{owner}/{repo}/contents/{file_path}")
            
            data = {
                "message": commit_message,
                "content": base64.b64encode(workflow_content.encode()).decode(),
                "branch": "main"  # Default to main branch
            }
            
            # If file exists, include SHA for update
            if existing_response.status_code == 200:
                existing_data = existing_response.json()
                data["sha"] = existing_data["sha"]
            
            # Create/update file
            response = self._make_request(f"/repos/{owner}/{repo}/contents/{file_path}", "PUT", data)
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                result['success'] = True
                result['sha'] = response_data.get('content', {}).get('sha')
            else:
                result['error'] = f"Failed to create workflow file: {response.status_code}"
                
        except Exception as e:
            result['error'] = f"Error creating workflow file: {str(e)}"
        
        return result
    
    def get_repository_structure(self, owner: str, repo: str, path: str = "") -> Dict[str, Any]:
        """
        Get repository file structure
        """
        result = {
            'success': False,
            'contents': [],
            'error': None
        }
        
        try:
            endpoint = f"/repos/{owner}/{repo}/contents"
            if path:
                endpoint += f"/{path}"
            
            response = self._make_request(endpoint)
            
            if response.status_code == 200:
                result['success'] = True
                result['contents'] = response.json()
            else:
                result['error'] = f"Failed to fetch repository contents: {response.status_code}"
                
        except Exception as e:
            result['error'] = f"Error fetching repository structure: {str(e)}"
        
        return result
    
    # ========== ADVANCED PYGITHUB API METHODS ==========
    
    def smart_file_check(self, repo_url: str, file_path: str) -> Dict[str, Any]:
        """
        Advanced file checking using PyGithub - checks without cloning entire repo
        Example: Check if cloudbuild.yaml exists before triggering build
        """
        result = {
            'exists': False,
            'content': None,
            'sha': None,
            'size': None,
            'encoding': None,
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for file operations"
                return result
            
            # Parse repository from URL
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                result['error'] = "Invalid repository URL"
                return result
            
            # Get repository object
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            try:
                # Get file content without cloning
                file_content = repo.get_contents(file_path)
                result['exists'] = True
                result['content'] = file_content.decoded_content.decode('utf-8')
                result['sha'] = file_content.sha
                result['size'] = file_content.size
                result['encoding'] = file_content.encoding
                
            except UnknownObjectException:
                # File doesn't exist - this is not an error, just info
                result['exists'] = False
                
        except BadCredentialsException:
            result['error'] = "Invalid GitHub token or insufficient permissions"
        except GithubException as e:
            result['error'] = f"GitHub API error: {e.data.get('message', str(e))}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def smart_workflow_deploy(self, repo_url: str, workflow_content: str, 
                            workflow_name: str, commit_message: str = None) -> Dict[str, Any]:
        """
        Advanced workflow deployment with automatic conflict resolution
        Creates/updates workflow files with intelligent handling
        """
        result = {
            'success': False,
            'action': None,  # 'created' or 'updated'
            'commit_sha': None,
            'workflow_path': None,
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for workflow deployment"
                return result
            
            # Parse repository
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                result['error'] = "Invalid repository URL"
                return result
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Ensure workflow filename has .yml extension
            if not workflow_name.endswith(('.yml', '.yaml')):
                workflow_name += '.yml'
            
            workflow_path = f".github/workflows/{workflow_name}"
            result['workflow_path'] = workflow_path
            
            # Default commit message
            if not commit_message:
                commit_message = f"Add/Update {workflow_name} via APK Builder Assistant"
            
            try:
                # Check if file exists
                existing_file = repo.get_contents(workflow_path)
                
                # File exists - update it
                repo.update_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_content,
                    sha=existing_file.sha
                )
                result['action'] = 'updated'
                
            except UnknownObjectException:
                # File doesn't exist - create it
                # First ensure .github/workflows directory exists
                try:
                    repo.get_contents(".github/workflows")
                except UnknownObjectException:
                    # Create .github/workflows directory
                    repo.create_file(
                        path=".github/workflows/.gitkeep",
                        message="Create workflows directory",
                        content=""
                    )
                
                # Create the workflow file
                repo.create_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_content
                )
                result['action'] = 'created'
            
            result['success'] = True
            
        except BadCredentialsException:
            result['error'] = "Invalid GitHub token or insufficient permissions"
        except GithubException as e:
            result['error'] = f"GitHub API error: {e.data.get('message', str(e))}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def monitor_build_status(self, repo_url: str, workflow_name: str = None) -> Dict[str, Any]:
        """
        Real-time monitoring of GitHub Actions build status
        Returns live status instead of just starting build and hoping for the best
        """
        result = {
            'success': False,
            'runs': [],
            'latest_run': None,
            'active_runs': [],
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for monitoring builds"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                result['error'] = "Invalid repository URL"
                return result
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Get workflow runs
            workflow_runs = repo.get_workflow_runs()
            
            runs_data = []
            active_runs = []
            
            for run in workflow_runs[:10]:  # Get last 10 runs
                run_data = {
                    'id': run.id,
                    'name': run.name,
                    'status': run.status,
                    'conclusion': run.conclusion,
                    'created_at': run.created_at.isoformat(),
                    'updated_at': run.updated_at.isoformat(),
                    'head_branch': run.head_branch,
                    'head_sha': run.head_sha[:8],
                    'workflow_name': run.workflow.name if run.workflow else 'Unknown',
                    'html_url': run.html_url
                }
                
                runs_data.append(run_data)
                
                # Track active runs (in_progress, queued, requested)
                if run.status in ['in_progress', 'queued', 'requested']:
                    active_runs.append(run_data)
            
            result['success'] = True
            result['runs'] = runs_data
            result['latest_run'] = runs_data[0] if runs_data else None
            result['active_runs'] = active_runs
            
        except BadCredentialsException:
            result['error'] = "Invalid GitHub token or insufficient permissions"
        except GithubException as e:
            result['error'] = f"GitHub API error: {e.data.get('message', str(e))}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def auto_setup_repository(self, repo_url: str, project_type: str = "kivy") -> Dict[str, Any]:
        """
        Automatically set up repository with required files for APK building
        Creates buildozer.spec, requirements.txt, and GitHub workflow if missing
        """
        result = {
            'success': False,
            'files_created': [],
            'files_updated': [],
            'setup_complete': False,
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for repository setup"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                result['error'] = "Invalid repository URL"
                return result
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # 1. Check/Create buildozer.spec
            buildozer_check = self.smart_file_check(repo_url, "buildozer.spec")
            if not buildozer_check['exists']:
                buildozer_content = self._generate_buildozer_spec(project_type)
                repo.create_file(
                    path="buildozer.spec",
                    message="Add buildozer.spec for APK building",
                    content=buildozer_content
                )
                result['files_created'].append('buildozer.spec')
            
            # 2. Check/Create requirements.txt
            requirements_check = self.smart_file_check(repo_url, "requirements.txt")
            if not requirements_check['exists']:
                requirements_content = self._generate_requirements_txt(project_type)
                repo.create_file(
                    path="requirements.txt",
                    message="Add requirements.txt for dependencies",
                    content=requirements_content
                )
                result['files_created'].append('requirements.txt')
            
            # 3. Check/Create GitHub workflow
            workflow_check = self.smart_file_check(repo_url, ".github/workflows/build-apk.yml")
            if not workflow_check['exists']:
                from templates.workflow_templates import WorkflowTemplates
                templates = WorkflowTemplates()
                workflow_content = templates.get_template('basic_apk_build')['content']
                
                deploy_result = self.smart_workflow_deploy(
                    repo_url, workflow_content, "build-apk.yml", 
                    "Add GitHub Actions workflow for APK building"
                )
                if deploy_result['success']:
                    result['files_created'].append('.github/workflows/build-apk.yml')
            
            result['success'] = True
            result['setup_complete'] = len(result['files_created']) > 0 or len(result['files_updated']) > 0
            
        except Exception as e:
            result['error'] = f"Error during repository setup: {str(e)}"
        
        return result
    
    def _parse_repo_url(self, repo_url: str) -> tuple:
        """Parse GitHub repository URL to extract owner and repo name"""
        try:
            # Handle various GitHub URL formats
            if 'github.com' in repo_url:
                # Remove protocol and trailing .git
                clean_url = repo_url.replace('https://', '').replace('http://', '').replace('.git', '')
                parts = clean_url.replace('github.com/', '').split('/')
                
                if len(parts) >= 2:
                    return parts[0], parts[1]
            
            return None, None
        except Exception:
            return None, None
    
    def _generate_buildozer_spec(self, project_type: str) -> str:
        """Generate a basic buildozer.spec file for the project"""
        return '''[app]
title = My App
package.name = myapp
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 21b
'''
    
    def _generate_requirements_txt(self, project_type: str) -> str:
        """Generate a basic requirements.txt file"""
        if project_type == "kivy":
            return '''kivy>=2.1.0
buildozer>=1.4.0
'''
        else:
            return '''# Add your Python dependencies here
# Example:
# requests>=2.25.0
# numpy>=1.20.0
'''
    
    def check_github_connection(self, target_username: str = None) -> Dict[str, Any]:
        """
        Checks if the GITHUB_TOKEN has a valid connection to GitHub
        Optionally verifies connection to a specific username
        """
        result = {
            'connected': False,
            'authenticated_user': None,
            'correct_user': False,
            'message': '',
            'error': None
        }
        
        try:
            if not self.token:
                result['error'] = "GITHUB_TOKEN is not set in environment variables"
                result['message'] = "No GitHub token found. Please add GITHUB_TOKEN to your secrets."
                return result
            
            if not self.github:
                result['error'] = "PyGithub client not initialized"
                result['message'] = "GitHub client initialization failed"
                return result
            
            # Get the authenticated user's information
            authenticated_user = self.github.get_user()
            authenticated_username = authenticated_user.login
            
            result['connected'] = True
            result['authenticated_user'] = authenticated_username
            
            if target_username:
                # Check if authenticated user matches target username
                if authenticated_username.lower() == target_username.lower():
                    result['correct_user'] = True
                    result['message'] = f"✅ Success: Connected as {authenticated_username}"
                else:
                    result['correct_user'] = False
                    result['message'] = f"❌ Wrong user: Connected as {authenticated_username}, expected {target_username}"
            else:
                # Just verify connection without specific user check
                result['correct_user'] = True
                result['message'] = f"✅ Success: Connected to GitHub as {authenticated_username}"
                
        except BadCredentialsException:
            result['error'] = "Invalid GitHub token or insufficient permissions"
            result['message'] = "❌ Authentication failed: Invalid token or expired credentials"
        except GithubException as e:
            result['error'] = f"GitHub API error: {e.data.get('message', str(e))}"
            result['message'] = f"❌ GitHub API error: {e.data.get('message', str(e))}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
            result['message'] = f"❌ Connection failed: {str(e)}"
        
        return result

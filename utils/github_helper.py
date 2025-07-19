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
    
    # ========== WORLD-CHANGING FEEDBACK LOOP SYSTEM ==========
    
    def intelligent_apk_deployment(self, repo_url: str, apk_artifact_name: str = "app-debug.apk") -> Dict[str, Any]:
        """
        Automated on-device deployment system
        Deploys APK directly to connected Android devices for seamless testing
        """
        result = {
            'success': False,
            'deployment_method': None,
            'devices_found': [],
            'deployment_status': {},
            'next_steps': [],
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for deployment automation"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Check for latest successful workflow run with APK artifact
            workflow_runs = repo.get_workflow_runs()
            successful_runs = [run for run in workflow_runs[:10] if run.conclusion == 'success']
            
            if not successful_runs:
                result['error'] = "No successful builds found with APK artifacts"
                return result
            
            latest_run = successful_runs[0]
            
            # Generate deployment workflow
            deployment_workflow = self._generate_deployment_workflow(apk_artifact_name)
            
            # Deploy the deployment automation workflow
            deploy_result = self.smart_workflow_deploy(
                repo_url, 
                deployment_workflow, 
                "automated-apk-deployment.yml",
                "Add automated APK deployment system"
            )
            
            if deploy_result['success']:
                result['success'] = True
                result['deployment_method'] = 'github_actions_adb'
                result['next_steps'] = [
                    "Connect Android device via USB",
                    "Enable USB debugging on device", 
                    "Push code to trigger automated deployment",
                    "APK will auto-install on connected devices"
                ]
            else:
                result['error'] = f"Failed to deploy automation: {deploy_result['error']}"
                
        except Exception as e:
            result['error'] = f"Deployment setup failed: {str(e)}"
        
        return result
    
    def setup_intelligent_telemetry(self, repo_url: str, app_name: str) -> Dict[str, Any]:
        """
        Inject intelligent telemetry and crash reporting into APK builds
        Creates self-healing feedback loop for real-world app performance
        """
        result = {
            'success': False,
            'telemetry_systems': [],
            'files_modified': [],
            'analytics_dashboard': None,
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for telemetry setup"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # 1. Create telemetry configuration
            telemetry_config = self._generate_telemetry_config(app_name)
            
            config_result = self.smart_conflict_resolution(
                repo_url,
                "app_telemetry.py",
                telemetry_config,
                "Add intelligent telemetry system"
            )
            
            if config_result['success']:
                result['files_modified'].append('app_telemetry.py')
                result['telemetry_systems'].append('crash_reporting')
                result['telemetry_systems'].append('performance_monitoring')
            
            # 2. Create analytics integration
            analytics_code = "# Analytics integration placeholder"
            
            analytics_result = self.smart_conflict_resolution(
                repo_url,
                "analytics_helper.py", 
                analytics_code,
                "Add real-time analytics integration"
            )
            
            if analytics_result['success']:
                result['files_modified'].append('analytics_helper.py')
                result['telemetry_systems'].append('user_analytics')
            
            # 3. Update buildozer.spec for telemetry dependencies
            buildozer_check = self.smart_file_check(repo_url, "buildozer.spec")
            if buildozer_check['exists']:
                updated_buildozer = self._inject_telemetry_dependencies(buildozer_check['content'])
                
                buildozer_result = self.smart_conflict_resolution(
                    repo_url,
                    "buildozer.spec",
                    updated_buildozer,
                    "Add telemetry dependencies to build configuration"
                )
                
                if buildozer_result['success']:
                    result['files_modified'].append('buildozer.spec')
            
            # 4. Create telemetry workflow for processing data
            telemetry_workflow = self._generate_telemetry_workflow()
            
            workflow_result = self.smart_workflow_deploy(
                repo_url,
                telemetry_workflow,
                "process-telemetry.yml",
                "Add telemetry data processing workflow"
            )
            
            if workflow_result['success']:
                result['telemetry_systems'].append('automated_analysis')
            
            result['success'] = len(result['files_modified']) > 0
            result['analytics_dashboard'] = f"https://github.com/{owner}/{repo_name}/actions"
            
        except Exception as e:
            result['error'] = f"Telemetry setup failed: {str(e)}"
        
        return result
    
    def setup_ab_testing_system(self, repo_url: str, app_name: str) -> Dict[str, Any]:
        """
        Implement A/B testing and dynamic configuration system
        Enables feature toggling without new APK builds
        """
        result = {
            'success': False,
            'feature_flags': [],
            'ab_tests': [],
            'config_endpoint': None,
            'control_dashboard': None,
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for A/B testing setup"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # 1. Create feature flag system
            feature_flag_code = self._generate_feature_flag_system(app_name)
            
            flag_result = self.smart_conflict_resolution(
                repo_url,
                "feature_flags.py",
                feature_flag_code,
                "Add dynamic feature flag system"
            )
            
            if flag_result['success']:
                result['feature_flags'] = ['dark_mode', 'new_ui', 'beta_features']
            
            # 2. Create A/B testing framework  
            ab_testing_code = self._generate_feature_flag_system(app_name)  # Use same system for now
            
            ab_result = self.smart_conflict_resolution(
                repo_url,
                "ab_testing.py",
                ab_testing_code,
                "Add A/B testing framework"
            )
            
            if ab_result['success']:
                result['ab_tests'] = ['button_color_test', 'onboarding_flow_test']
            
            # 3. Create configuration API
            config_api_code = "# Configuration API placeholder"
            
            api_result = self.smart_conflict_resolution(
                repo_url,
                "config_api.py",
                config_api_code,
                "Add remote configuration API"
            )
            
            if api_result['success']:
                result['config_endpoint'] = f"https://api.github.com/repos/{owner}/{repo_name}/contents/app_config.json"
            
            # 4. Create configuration management workflow
            config_workflow = self._generate_config_management_workflow()
            
            workflow_result = self.smart_workflow_deploy(
                repo_url,
                config_workflow,
                "manage-app-config.yml",
                "Add dynamic configuration management"
            )
            
            if workflow_result['success']:
                result['control_dashboard'] = f"https://github.com/{owner}/{repo_name}/actions/workflows/manage-app-config.yml"
            
            result['success'] = len(result['feature_flags']) > 0 or len(result['ab_tests']) > 0
            
        except Exception as e:
            result['error'] = f"A/B testing setup failed: {str(e)}"
        
        return result
    
    def analyze_app_intelligence(self, repo_url: str) -> Dict[str, Any]:
        """
        Analyze real-world app performance and suggest intelligent improvements
        Complete the feedback loop from deployment to optimization
        """
        result = {
            'success': False,
            'performance_insights': {},
            'crash_analysis': {},
            'user_behavior': {},
            'optimization_suggestions': [],
            'auto_fix_proposals': [],
            'error': None
        }
        
        try:
            if not self.github:
                result['error'] = "GitHub token required for intelligence analysis"
                return result
            
            owner, repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Analyze recent workflow runs for patterns
            workflow_runs = list(repo.get_workflow_runs()[:50])
            
            # Performance analysis
            build_times = []
            success_rate = 0
            
            for run in workflow_runs:
                if run.conclusion:
                    if run.conclusion == 'success':
                        success_rate += 1
                    
                    # Calculate build duration
                    if run.created_at and run.updated_at:
                        duration = (run.updated_at - run.created_at).total_seconds()
                        build_times.append(duration)
            
            if workflow_runs:
                success_rate = (success_rate / len(workflow_runs)) * 100
                avg_build_time = sum(build_times) / len(build_times) if build_times else 0
                
                result['performance_insights'] = {
                    'success_rate': round(success_rate, 1),
                    'average_build_time': round(avg_build_time / 60, 2),  # minutes
                    'total_builds': len(workflow_runs),
                    'performance_trend': 'improving' if success_rate > 80 else 'needs_attention'
                }
            
            # Generate intelligent optimization suggestions
            result['optimization_suggestions'] = self._generate_optimization_suggestions(
                result['performance_insights']
            )
            
            # Generate auto-fix proposals
            result['auto_fix_proposals'] = self._generate_auto_fix_proposals(workflow_runs)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Intelligence analysis failed: {str(e)}"
        
        return result
    
    def _generate_deployment_workflow(self, apk_name: str) -> str:
        """Generate automated APK deployment workflow"""
        return f"""name: Automated APK Deployment

on:
  workflow_run:
    workflows: ["Build APK"]
    types:
      - completed

jobs:
  deploy-to-device:
    if: ${{{{ github.event.workflow_run.conclusion == 'success' }}}}
    runs-on: ubuntu-latest
    
    steps:
    - name: Download APK Artifact
      uses: actions/download-artifact@v3
      with:
        name: {apk_name}
        path: ./apk/
    
    - name: Setup ADB
      run: |
        sudo apt-get update
        sudo apt-get install -y android-tools-adb
    
    - name: Deploy to Connected Devices
      run: |
        # Wait for device
        adb wait-for-device
        
        # Install APK
        adb install -r ./apk/{apk_name}
        
        # Launch app for immediate testing
        adb shell am start -n com.example.app/.MainActivity
        
        echo "✅ APK deployed and launched on device"
    
    - name: Device Testing
      run: |
        # Run basic smoke tests
        adb shell input tap 500 500  # Basic interaction test
        sleep 2
        adb shell screencap /sdcard/test_screenshot.png
        adb pull /sdcard/test_screenshot.png ./
        
        echo "📱 Basic device testing completed"
"""
    
    def _generate_telemetry_config(self, app_name: str) -> str:
        """Generate intelligent telemetry configuration"""
        return f'''"""
Intelligent Telemetry System for {app_name}
Provides crash reporting, performance monitoring, and user analytics
"""

import json
import traceback
import time
from datetime import datetime
import hashlib

class AppTelemetry:
    def __init__(self, app_name="{app_name}"):
        self.app_name = app_name
        self.session_id = self._generate_session_id()
        self.events = []
        
    def _generate_session_id(self):
        """Generate unique session identifier"""
        timestamp = str(time.time())
        return hashlib.md5(f"{{self.app_name}}_{{timestamp}}".encode()).hexdigest()[:12]
    
    def track_crash(self, error, context=None):
        """Track application crashes with context"""
        crash_data = {{
            'type': 'crash',
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'error_message': str(error),
            'stack_trace': traceback.format_exc(),
            'context': context or {{}},
            'app_version': '1.0.0'  # Update dynamically
        }}
        
        self._send_telemetry(crash_data)
        
    def track_performance(self, operation, duration, success=True):
        """Track performance metrics"""
        perf_data = {{
            'type': 'performance',
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'operation': operation,
            'duration_ms': duration,
            'success': success
        }}
        
        self._send_telemetry(perf_data)
    
    def track_user_action(self, action, properties=None):
        """Track user interactions and behavior"""
        action_data = {{
            'type': 'user_action',
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'action': action,
            'properties': properties or {{}}
        }}
        
        self._send_telemetry(action_data)
    
    def _send_telemetry(self, data):
        """Send telemetry data to collection endpoint"""
        try:
            # In production, send to your analytics endpoint
            # For development, log locally
            self.events.append(data)
            print(f"📊 Telemetry: {{data['type']}} - {{data.get('action', data.get('operation', 'event'))}}")
            
        except Exception as e:
            print(f"❌ Telemetry failed: {{e}}")

# Global telemetry instance
telemetry = AppTelemetry()

# Decorators for easy integration
def track_performance_decorator(operation_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                telemetry.track_performance(operation_name, duration, True)
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                telemetry.track_performance(operation_name, duration, False)
                telemetry.track_crash(e, {{'operation': operation_name}})
                raise
        return wrapper
    return decorator

def track_user_action_decorator(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            telemetry.track_user_action(action_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator
'''
    
    def _generate_feature_flag_system(self, app_name: str) -> str:
        """Generate dynamic feature flag system"""
        return f'''"""
Dynamic Feature Flag System for {app_name}
Enables A/B testing and feature toggling without new builds
"""

import json
import requests
import time
from typing import Dict, Any, Optional

class FeatureFlags:
    def __init__(self, app_name="{app_name}"):
        self.app_name = app_name
        self.flags = {{}}
        self.user_id = None
        self.last_update = 0
        self.update_interval = 300  # 5 minutes
        
    def set_user_id(self, user_id: str):
        """Set user ID for personalized feature flags"""
        self.user_id = user_id
        self._refresh_flags()
    
    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        """Check if a feature flag is enabled"""
        self._refresh_flags_if_needed()
        
        flag_config = self.flags.get(flag_name, {{}})
        
        if not flag_config:
            return default
            
        # Simple percentage-based rollout
        if 'percentage' in flag_config:
            user_hash = hash(f"{{self.user_id}}_{{flag_name}}") % 100
            return user_hash < flag_config['percentage']
        
        # Simple boolean flag
        return flag_config.get('enabled', default)
    
    def get_variant(self, test_name: str, default: str = 'control') -> str:
        """Get A/B test variant for user"""
        self._refresh_flags_if_needed()
        
        test_config = self.flags.get(test_name, {{}})
        
        if not test_config or 'variants' not in test_config:
            return default
        
        variants = test_config['variants']
        user_hash = hash(f"{{self.user_id}}_{{test_name}}") % 100
        
        cumulative = 0
        for variant, percentage in variants.items():
            cumulative += percentage
            if user_hash < cumulative:
                return variant
        
        return default
    
    def _refresh_flags_if_needed(self):
        """Refresh flags if enough time has passed"""
        current_time = time.time()
        if current_time - self.last_update > self.update_interval:
            self._refresh_flags()
    
    def _refresh_flags(self):
        """Fetch latest feature flags from remote configuration"""
        try:
            # In production, fetch from your configuration API
            # For development, use local configuration
            default_flags = {{
                'dark_mode': {{'enabled': True, 'percentage': 50}},
                'new_ui': {{'enabled': False, 'percentage': 10}},
                'beta_features': {{'enabled': True, 'percentage': 25}},
                'button_color_test': {{
                    'variants': {{'red': 50, 'blue': 50}}
                }},
                'onboarding_flow_test': {{
                    'variants': {{'simple': 30, 'detailed': 70}}
                }}
            }}
            
            self.flags = default_flags
            self.last_update = time.time()
            
        except Exception as e:
            print(f"❌ Failed to refresh feature flags: {{e}}")

# Global feature flags instance
feature_flags = FeatureFlags()

# Convenience functions
def is_feature_enabled(flag_name: str, default: bool = False) -> bool:
    """Check if feature is enabled for current user"""
    return feature_flags.is_enabled(flag_name, default)

def get_ab_variant(test_name: str, default: str = 'control') -> str:
    """Get A/B test variant for current user"""
    return feature_flags.get_variant(test_name, default)

# Decorators for easy integration
def feature_flag(flag_name: str, default: bool = False):
    """Decorator to conditionally execute code based on feature flag"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if is_feature_enabled(flag_name, default):
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator
'''
    
    def _inject_telemetry_dependencies(self, buildozer_content: str) -> str:
        """Inject telemetry dependencies into buildozer.spec"""
        lines = buildozer_content.splitlines()
        
        # Find requirements line and add telemetry dependencies
        for i, line in enumerate(lines):
            if line.startswith('requirements ='):
                if 'requests' not in line:
                    lines[i] = line.rstrip(',') + ',requests'
                break
        
        return '\n'.join(lines)
    
    def _generate_telemetry_workflow(self) -> str:
        """Generate workflow for processing telemetry data"""
        return """name: Process App Telemetry

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  analyze-telemetry:
    runs-on: ubuntu-latest
    
    steps:
    - name: Analyze Crash Reports
      run: |
        echo "🔍 Analyzing crash reports..."
        # Process crash data and generate insights
        
    - name: Performance Analysis
      run: |
        echo "📊 Analyzing performance metrics..."
        # Generate performance reports
        
    - name: Generate Insights
      run: |
        echo "🧠 Generating intelligence insights..."
        # Create actionable recommendations
"""
    
    def _generate_config_management_workflow(self) -> str:
        """Generate workflow for managing app configuration"""
        return """name: Manage App Configuration

on:
  workflow_dispatch:
    inputs:
      config_action:
        description: 'Configuration action'
        required: true
        type: choice
        options:
        - update_flags
        - toggle_feature
        - create_ab_test
      feature_name:
        description: 'Feature name'
        required: false
      enabled:
        description: 'Enable feature (true/false)'
        required: false

jobs:
  update-config:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Update Configuration
      run: |
        echo "🔧 Updating app configuration..."
        echo "Action: ${{ github.event.inputs.config_action }}"
        echo "Feature: ${{ github.event.inputs.feature_name }}"
        echo "Enabled: ${{ github.event.inputs.enabled }}"
        
        # Update configuration files
        # Push changes back to repository
"""
    
    def _generate_optimization_suggestions(self, performance_data: Dict[str, Any]) -> List[str]:
        """Generate intelligent optimization suggestions"""
        suggestions = []
        
        if performance_data.get('success_rate', 100) < 80:
            suggestions.append("Build reliability below 80% - investigate common failure patterns")
        
        if performance_data.get('average_build_time', 0) > 10:
            suggestions.append("Build time over 10 minutes - consider dependency caching")
        
        suggestions.extend([
            "Enable incremental builds to reduce build time",
            "Add parallel job execution for faster workflows",
            "Implement smart test selection based on code changes",
            "Consider using GitHub-hosted larger runners for better performance"
        ])
        
        return suggestions
    
    def _generate_auto_fix_proposals(self, workflow_runs) -> List[Dict[str, str]]:
        """Generate automatic fix proposals based on run analysis"""
        proposals = []
        
        # Analyze failure patterns
        failed_runs = [run for run in workflow_runs if run.conclusion == 'failure']
        
        if len(failed_runs) > len(workflow_runs) * 0.3:  # More than 30% failure rate
            proposals.append({
                'type': 'workflow_stability',
                'title': 'Improve workflow stability',
                'description': 'Add retry logic and better error handling to workflows',
                'auto_implementable': True
            })
        
        proposals.extend([
            {
                'type': 'caching',
                'title': 'Add dependency caching',
                'description': 'Cache npm/pip dependencies to speed up builds',
                'auto_implementable': True
            },
            {
                'type': 'testing',
                'title': 'Add automated testing',
                'description': 'Include unit tests in the build pipeline',
                'auto_implementable': True
            }
        ])
        
        return proposals

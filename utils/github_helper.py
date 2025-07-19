import os
import requests
from typing import Dict, List, Any, Optional
import base64
import json

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

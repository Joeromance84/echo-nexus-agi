from typing import Dict, List, Any
import yaml
import re

class GitHubPolicies:
    def __init__(self):
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """Load GitHub Actions policies and compliance rules"""
        return {
            "security_policies": {
                "description": "Security best practices for GitHub Actions workflows",
                "requirements": [
                    "Use secrets for sensitive data, never hardcode credentials",
                    "Pin action versions to specific tags or SHAs",
                    "Limit permissions using GITHUB_TOKEN with minimal scope",
                    "Validate inputs and sanitize outputs",
                    "Use trusted actions from verified publishers",
                    "Avoid exposing sensitive information in logs"
                ],
                "examples": [
                    """permissions:
  contents: read
  actions: read""",
                    """- name: Use secret
  env:
    API_KEY: ${{ secrets.API_KEY }}"""
                ],
                "common_violations": [
                    "Hardcoded passwords or API keys in workflow files",
                    "Using actions with @main or @master instead of pinned versions",
                    "Excessive permissions for GITHUB_TOKEN",
                    "Exposing secrets in echo statements or logs"
                ]
            },
            
            "resource_usage": {
                "description": "GitHub Actions resource usage and billing policies",
                "requirements": [
                    "Optimize workflow execution time to minimize billing",
                    "Use caching to reduce redundant downloads",
                    "Cancel redundant workflows to save resources",
                    "Use appropriate runner types for workload",
                    "Avoid unnecessary parallel jobs",
                    "Clean up artifacts after use"
                ],
                "examples": [
                    """concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true""",
                    """- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}"""
                ],
                "common_violations": [
                    "Running unnecessary parallel jobs that exceed limits",
                    "Not using caching for dependencies",
                    "Keeping artifacts longer than necessary",
                    "Running workflows on every commit without filtering"
                ]
            },
            
            "workflow_limits": {
                "description": "GitHub Actions workflow execution limits and constraints",
                "requirements": [
                    "Job execution time must not exceed 6 hours",
                    "Maximum 20 concurrent jobs per repository",
                    "Workflow run time limited to 35 days",
                    "API rate limits apply to GitHub API calls",
                    "Storage limits for artifacts and logs",
                    "Matrix jobs limited to 20 concurrent jobs"
                ],
                "examples": [
                    """timeout-minutes: 60  # Set reasonable timeout""",
                    """strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
  max-parallel: 2  # Limit concurrent jobs"""
                ],
                "common_violations": [
                    "Jobs running longer than necessary without timeouts",
                    "Matrix strategies creating too many concurrent jobs",
                    "Workflows with infinite loops or hanging processes",
                    "Excessive API calls causing rate limiting"
                ]
            },
            
            "content_policies": {
                "description": "GitHub Terms of Service and acceptable use policies",
                "requirements": [
                    "No cryptocurrency mining in workflows",
                    "No malicious code or security exploits",
                    "No unauthorized data collection or privacy violations",
                    "No spam or abuse of the platform",
                    "Respect intellectual property rights",
                    "No illegal or harmful content"
                ],
                "examples": [
                    """# Good: Legitimate build process
- name: Build application
  run: python setup.py build""",
                    """# Good: Testing legitimate functionality
- name: Run tests
  run: pytest tests/"""
                ],
                "common_violations": [
                    "Using runners for cryptocurrency mining",
                    "Attempting to exploit GitHub's infrastructure",
                    "Distributing malware or harmful software",
                    "Violating rate limits intentionally"
                ]
            },
            
            "apk_build_compliance": {
                "description": "Specific compliance requirements for APK building workflows",
                "requirements": [
                    "Use legitimate Android SDK and build tools",
                    "Respect Google Play Store policies if distributing",
                    "Include proper licensing information",
                    "Use signed APKs for production releases",
                    "Follow Android app security best practices",
                    "Avoid including prohibited content in APKs"
                ],
                "examples": [
                    """- name: Build APK
  run: buildozer android release""",
                    """- name: Sign APK
  env:
    KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
  run: |
    jarsigner -keystore release.keystore app.apk"""
                ],
                "common_violations": [
                    "Building APKs with malicious code",
                    "Using unauthorized or pirated development tools",
                    "Including copyrighted content without permission",
                    "Creating APKs that violate platform policies"
                ]
            }
        }
    
    def check_compliance(self, workflow_yaml: str) -> Dict[str, Any]:
        """
        Check workflow compliance against GitHub policies
        """
        result = {
            'compliant': True,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        try:
            workflow = yaml.safe_load(workflow_yaml)
            workflow_str = workflow_yaml.lower()
            
            # Security checks
            self._check_security_compliance(workflow, workflow_str, result)
            
            # Resource usage checks
            self._check_resource_compliance(workflow, workflow_str, result)
            
            # Workflow limits checks
            self._check_limits_compliance(workflow, workflow_str, result)
            
            # Content policy checks
            self._check_content_compliance(workflow, workflow_str, result)
            
            # APK-specific checks
            self._check_apk_compliance(workflow, workflow_str, result)
            
            # Overall compliance
            if result['issues']:
                result['compliant'] = False
                
        except yaml.YAMLError:
            result['issues'].append("Invalid YAML syntax")
            result['compliant'] = False
        except Exception as e:
            result['issues'].append(f"Error checking compliance: {str(e)}")
            result['compliant'] = False
        
        return result
    
    def _check_security_compliance(self, workflow: Dict, workflow_str: str, result: Dict):
        """Check security-related compliance"""
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*[:=]\s*["\']?[a-zA-Z0-9@#$%^&*()]+["\']?',
            r'token\s*[:=]\s*["\']?[a-zA-Z0-9]+["\']?',
            r'key\s*[:=]\s*["\']?[a-zA-Z0-9]+["\']?',
            r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9]+["\']?'
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, workflow_str, re.IGNORECASE):
                if '${{ secrets.' not in workflow_str:
                    result['issues'].append("Potential hardcoded secret detected. Use GitHub Secrets instead.")
        
        # Check for unpinned actions
        if 'jobs' in workflow:
            for job_name, job_config in workflow['jobs'].items():
                if 'steps' in job_config:
                    for step in job_config['steps']:
                        if 'uses' in step:
                            action = step['uses']
                            if '@main' in action or '@master' in action:
                                result['warnings'].append(f"Action '{action}' uses unpinned version. Consider pinning to specific version.")
        
        # Check permissions
        if 'permissions' not in workflow:
            result['recommendations'].append("Consider adding explicit permissions to limit GITHUB_TOKEN scope")
        
        # Check for secrets exposure in logs
        if 'echo' in workflow_str and '${{' in workflow_str:
            result['warnings'].append("Be careful not to expose secrets in echo statements")
    
    def _check_resource_compliance(self, workflow: Dict, workflow_str: str, result: Dict):
        """Check resource usage compliance"""
        
        # Check for caching
        if 'cache' not in workflow_str:
            result['recommendations'].append("Consider using actions/cache to improve build performance")
        
        # Check for concurrency control
        if 'concurrency' not in workflow:
            result['recommendations'].append("Consider adding concurrency control to cancel redundant workflows")
        
        # Check for artifact retention
        if 'upload-artifact' in workflow_str:
            if 'retention-days' not in workflow_str:
                result['warnings'].append("Consider setting retention-days for artifacts to manage storage costs")
        
        # Check for unnecessary parallel execution
        if 'jobs' in workflow and len(workflow['jobs']) > 10:
            result['warnings'].append("Large number of parallel jobs may exceed limits and increase costs")
    
    def _check_limits_compliance(self, workflow: Dict, workflow_str: str, result: Dict):
        """Check workflow limits compliance"""
        
        # Check for timeouts
        timeout_found = False
        if 'jobs' in workflow:
            for job_name, job_config in workflow['jobs'].items():
                if 'timeout-minutes' in job_config:
                    timeout_found = True
                    timeout = job_config['timeout-minutes']
                    if timeout > 360:  # 6 hours
                        result['issues'].append(f"Job '{job_name}' timeout ({timeout} min) exceeds 6-hour limit")
        
        if not timeout_found:
            result['recommendations'].append("Consider adding timeout-minutes to jobs to prevent runaway processes")
        
        # Check matrix strategy limits
        if 'strategy' in workflow_str and 'matrix' in workflow_str:
            if 'jobs' in workflow:
                for job_name, job_config in workflow['jobs'].items():
                    if 'strategy' in job_config and 'matrix' in job_config['strategy']:
                        matrix = job_config['strategy']['matrix']
                        if isinstance(matrix, dict):
                            total_combinations = 1
                            for key, values in matrix.items():
                                if isinstance(values, list):
                                    total_combinations *= len(values)
                            
                            if total_combinations > 20:
                                result['issues'].append(f"Matrix in job '{job_name}' creates {total_combinations} combinations, exceeding limit of 20")
    
    def _check_content_compliance(self, workflow: Dict, workflow_str: str, result: Dict):
        """Check content policy compliance"""
        
        # Check for cryptocurrency mining indicators
        mining_keywords = ['mining', 'miner', 'cryptocurrency', 'bitcoin', 'ethereum', 'monero', 'hashrate']
        for keyword in mining_keywords:
            if keyword in workflow_str:
                result['warnings'].append(f"Workflow contains '{keyword}' - ensure this is not for cryptocurrency mining")
        
        # Check for suspicious network activity
        suspicious_patterns = [
            r'curl.*-X\s+POST.*password',
            r'wget.*--post-data',
            r'nc\s+-l',  # netcat listening
            r'nmap\s+',   # network scanning
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, workflow_str, re.IGNORECASE):
                result['warnings'].append("Suspicious network activity detected - ensure compliance with ToS")
    
    def _check_apk_compliance(self, workflow: Dict, workflow_str: str, result: Dict):
        """Check APK build specific compliance"""
        
        # Check for legitimate build tools
        if 'buildozer' in workflow_str or 'gradle' in workflow_str:
            # This is good - using legitimate Android build tools
            pass
        elif 'android' in workflow_str:
            result['recommendations'].append("Ensure you're using legitimate Android development tools")
        
        # Check for signing (recommended for production)
        if 'release' in workflow_str:
            if 'keystore' not in workflow_str and 'signing' not in workflow_str:
                result['recommendations'].append("Consider adding APK signing for release builds")
        
        # Check for proper artifact handling
        if 'apk' in workflow_str:
            if 'upload-artifact' not in workflow_str:
                result['recommendations'].append("Consider uploading APK as workflow artifact")
        
        # Check for license compliance
        if 'license' not in workflow_str:
            result['recommendations'].append("Ensure proper licensing compliance for your APK")
    
    def get_policy_guide(self) -> Dict[str, Any]:
        """Get comprehensive policy guide"""
        return self.policies
    
    def get_policy_category(self, category: str) -> Dict[str, Any]:
        """Get specific policy category"""
        return self.policies.get(category, {})
    
    def get_compliance_checklist(self) -> List[Dict[str, Any]]:
        """Get compliance checklist for workflows"""
        checklist = []
        
        for category_name, category_data in self.policies.items():
            for requirement in category_data.get('requirements', []):
                checklist.append({
                    'category': category_name.replace('_', ' ').title(),
                    'requirement': requirement,
                    'critical': category_name in ['security_policies', 'content_policies']
                })
        
        return checklist
    
    def generate_compliance_report(self, workflow_yaml: str) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        compliance_result = self.check_compliance(workflow_yaml)
        checklist = self.get_compliance_checklist()
        
        report = {
            'overall_compliance': compliance_result['compliant'],
            'summary': {
                'issues': len(compliance_result['issues']),
                'warnings': len(compliance_result['warnings']),
                'recommendations': len(compliance_result['recommendations'])
            },
            'details': compliance_result,
            'checklist': checklist,
            'next_steps': []
        }
        
        # Generate next steps
        if compliance_result['issues']:
            report['next_steps'].append("⚠️ Address critical compliance issues before deploying workflow")
        
        if compliance_result['warnings']:
            report['next_steps'].append("📋 Review warnings and consider addressing them")
        
        if compliance_result['recommendations']:
            report['next_steps'].append("💡 Implement recommendations for better workflow practices")
        
        if compliance_result['compliant']:
            report['next_steps'].append("✅ Workflow appears compliant - ready for deployment")
        
        return report

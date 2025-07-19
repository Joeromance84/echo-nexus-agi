import yaml
import re
from typing import Dict, List, Any

class WorkflowValidator:
    def __init__(self):
        self.required_fields = ['name', 'on', 'jobs']
        self.job_required_fields = ['runs-on', 'steps']
        self.step_required_fields = []  # Steps can be flexible
        
    def validate_workflow(self, workflow_yaml: str) -> Dict[str, Any]:
        """
        Validate GitHub Actions workflow YAML
        Returns dict with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        try:
            # Parse YAML
            workflow = yaml.safe_load(workflow_yaml)
            
            if not isinstance(workflow, dict):
                result['errors'].append("Workflow must be a valid YAML object")
                return result
            
            # Validate top-level structure
            self._validate_top_level(workflow, result)
            
            # Validate jobs
            if 'jobs' in workflow:
                self._validate_jobs(workflow['jobs'], result)
            
            # APK-specific validations
            self._validate_apk_build_specifics(workflow, result)
            
            # Security checks
            self._validate_security(workflow, result)
            
            # Performance suggestions
            self._suggest_optimizations(workflow, result)
            
            # If no errors found, mark as valid
            if not result['errors']:
                result['valid'] = True
                
        except yaml.YAMLError as e:
            result['errors'].append(f"Invalid YAML syntax: {str(e)}")
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
            
        return result
    
    def _validate_top_level(self, workflow: Dict, result: Dict):
        """Validate top-level workflow structure"""
        for field in self.required_fields:
            if field not in workflow:
                result['errors'].append(f"Missing required field: '{field}'")
        
        # Validate 'on' triggers
        if 'on' in workflow:
            self._validate_triggers(workflow['on'], result)
        
        # Check for workflow name
        if 'name' in workflow:
            if not isinstance(workflow['name'], str) or not workflow['name'].strip():
                result['warnings'].append("Workflow name should be a non-empty string")
    
    def _validate_triggers(self, triggers: Any, result: Dict):
        """Validate workflow triggers"""
        if isinstance(triggers, str):
            # Single trigger
            if triggers not in ['push', 'pull_request', 'workflow_dispatch', 'schedule']:
                result['warnings'].append(f"Uncommon trigger type: '{triggers}'")
        elif isinstance(triggers, dict):
            # Multiple triggers
            for trigger in triggers:
                if trigger not in ['push', 'pull_request', 'workflow_dispatch', 'schedule', 'release']:
                    result['warnings'].append(f"Uncommon trigger type: '{trigger}'")
        elif isinstance(triggers, list):
            # List of triggers
            for trigger in triggers:
                if trigger not in ['push', 'pull_request', 'workflow_dispatch', 'schedule', 'release']:
                    result['warnings'].append(f"Uncommon trigger type: '{trigger}'")
    
    def _validate_jobs(self, jobs: Dict, result: Dict):
        """Validate jobs section"""
        if not isinstance(jobs, dict):
            result['errors'].append("Jobs section must be a dictionary")
            return
        
        if not jobs:
            result['errors'].append("At least one job must be defined")
            return
        
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                result['errors'].append(f"Job '{job_name}' must be a dictionary")
                continue
                
            # Validate required job fields
            for field in self.job_required_fields:
                if field not in job_config:
                    result['errors'].append(f"Job '{job_name}' missing required field: '{field}'")
            
            # Validate runs-on
            if 'runs-on' in job_config:
                runs_on = job_config['runs-on']
                if isinstance(runs_on, str):
                    if 'ubuntu' not in runs_on.lower() and 'macos' not in runs_on.lower() and 'windows' not in runs_on.lower():
                        result['warnings'].append(f"Job '{job_name}' uses uncommon runner: '{runs_on}'")
                    # For APK builds, recommend Ubuntu
                    if 'ubuntu' not in runs_on.lower():
                        result['suggestions'].append(f"Job '{job_name}': Consider using Ubuntu runner for APK builds")
            
            # Validate steps
            if 'steps' in job_config:
                self._validate_steps(job_config['steps'], job_name, result)
    
    def _validate_steps(self, steps: List, job_name: str, result: Dict):
        """Validate job steps"""
        if not isinstance(steps, list):
            result['errors'].append(f"Steps in job '{job_name}' must be a list")
            return
        
        if not steps:
            result['warnings'].append(f"Job '{job_name}' has no steps defined")
            return
        
        checkout_found = False
        python_setup_found = False
        
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                result['errors'].append(f"Step {i+1} in job '{job_name}' must be a dictionary")
                continue
            
            # Check for required action or run
            if 'uses' not in step and 'run' not in step:
                result['errors'].append(f"Step {i+1} in job '{job_name}' must have either 'uses' or 'run'")
            
            # Check for checkout action
            if 'uses' in step and 'checkout' in step['uses']:
                checkout_found = True
                # Validate checkout version
                if '@v' in step['uses']:
                    version = step['uses'].split('@v')[1]
                    if int(version[0]) < 3:
                        result['warnings'].append(f"Consider updating checkout action to v3 or later")
            
            # Check for Python setup
            if 'uses' in step and 'setup-python' in step['uses']:
                python_setup_found = True
                # Validate Python setup version
                if '@v' in step['uses']:
                    version = step['uses'].split('@v')[1]
                    if int(version[0]) < 4:
                        result['warnings'].append(f"Consider updating setup-python action to v4 or later")
        
        # APK build specific checks
        if not checkout_found:
            result['warnings'].append(f"Job '{job_name}': Consider adding checkout action to access repository code")
        
        if not python_setup_found:
            result['suggestions'].append(f"Job '{job_name}': Consider adding Python setup for APK building")
    
    def _validate_apk_build_specifics(self, workflow: Dict, result: Dict):
        """Validate APK-specific build requirements"""
        workflow_str = yaml.dump(workflow).lower()
        
        # Check for buildozer
        if 'buildozer' not in workflow_str:
            result['suggestions'].append("Consider using 'buildozer' for APK building")
        
        # Check for Java setup
        if 'java' not in workflow_str and 'openjdk' not in workflow_str:
            result['suggestions'].append("APK builds typically require Java/OpenJDK setup")
        
        # Check for Android SDK
        if 'android' not in workflow_str and 'sdk' not in workflow_str:
            result['suggestions'].append("Consider setting up Android SDK for APK building")
        
        # Check for artifact upload
        if 'upload-artifact' not in workflow_str:
            result['suggestions'].append("Consider uploading built APK as an artifact")
        
        # Check for caching
        if 'cache' not in workflow_str:
            result['suggestions'].append("Consider adding caching to speed up builds")
    
    def _validate_security(self, workflow: Dict, result: Dict):
        """Validate security best practices"""
        workflow_str = yaml.dump(workflow)
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*:\s*["\']?[^"\'\s]+["\']?',
            r'token\s*:\s*["\']?[^"\'\s]+["\']?',
            r'key\s*:\s*["\']?[^"\'\s]+["\']?',
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, workflow_str, re.IGNORECASE):
                result['warnings'].append("Potential hardcoded secret detected. Use GitHub Secrets instead.")
        
        # Check for proper secret usage
        if '${{ secrets.' not in workflow_str and 'password' in workflow_str.lower():
            result['warnings'].append("Consider using GitHub Secrets for sensitive data")
    
    def _suggest_optimizations(self, workflow: Dict, result: Dict):
        """Suggest performance and best practice optimizations"""
        workflow_str = yaml.dump(workflow).lower()
        
        # Suggest parallel jobs if possible
        if 'jobs' in workflow and len(workflow['jobs']) == 1:
            result['suggestions'].append("Consider splitting build into parallel jobs for faster execution")
        
        # Suggest matrix builds for multiple targets
        has_matrix = False
        for job_name, job_config in workflow.get('jobs', {}).items():
            if 'strategy' in job_config and 'matrix' in job_config['strategy']:
                has_matrix = True
                break
        
        if not has_matrix:
            result['suggestions'].append("Consider using matrix strategy for building multiple APK variants")
        
        # Suggest conditional execution
        if 'if:' not in workflow_str:
            result['suggestions'].append("Consider adding conditional execution to optimize workflow runs")
    
    def validate_buildozer_spec(self, spec_content: str) -> Dict[str, Any]:
        """Validate buildozer.spec configuration"""
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        try:
            lines = spec_content.split('\n')
            sections = {}
            current_section = None
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Section header
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    sections[current_section] = {}
                    continue
                
                # Key-value pair
                if '=' in line and current_section:
                    key, value = line.split('=', 1)
                    sections[current_section][key.strip()] = value.strip()
            
            # Validate required sections
            required_sections = ['app', 'buildozer']
            for section in required_sections:
                if section not in sections:
                    result['errors'].append(f"Missing required section: [{section}]")
            
            # Validate app section
            if 'app' in sections:
                self._validate_app_section(sections['app'], result)
            
            # Validate buildozer section
            if 'buildozer' in sections:
                self._validate_buildozer_section(sections['buildozer'], result)
            
            if not result['errors']:
                result['valid'] = True
                
        except Exception as e:
            result['errors'].append(f"Error parsing buildozer.spec: {str(e)}")
        
        return result
    
    def _validate_app_section(self, app_config: Dict, result: Dict):
        """Validate [app] section of buildozer.spec"""
        required_fields = ['title', 'package.name', 'package.domain']
        
        for field in required_fields:
            if field not in app_config:
                result['errors'].append(f"Missing required field in [app]: {field}")
        
        # Validate package name format
        if 'package.name' in app_config:
            package_name = app_config['package.name']
            if not re.match(r'^[a-z][a-z0-9_]*$', package_name):
                result['warnings'].append("Package name should contain only lowercase letters, numbers, and underscores")
        
        # Validate domain format
        if 'package.domain' in app_config:
            domain = app_config['package.domain']
            if not re.match(r'^[a-z][a-z0-9.]*[a-z0-9]$', domain):
                result['warnings'].append("Package domain should be in reverse domain format (e.g., org.example)")
    
    def _validate_buildozer_section(self, buildozer_config: Dict, result: Dict):
        """Validate [buildozer] section of buildozer.spec"""
        # Check log level
        if 'log_level' in buildozer_config:
            try:
                log_level = int(buildozer_config['log_level'])
                if log_level < 0 or log_level > 2:
                    result['warnings'].append("Log level should be 0, 1, or 2")
            except ValueError:
                result['warnings'].append("Log level should be a number")
        
        # Suggest useful configurations
        result['suggestions'].append("Consider setting log_level = 2 for detailed build output")

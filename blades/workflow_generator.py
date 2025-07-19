#!/usr/bin/env python3
"""
Workflow Generator Blade - Advanced GitHub Actions and Plugin Creation System
Creates, manages, and evolves GitHub workflows, actions, and automation tools
"""

import os
import json
import yaml
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

class WorkflowGenerator:
    """
    Advanced GitHub Actions workflow generator with AI-driven optimization
    """
    
    def __init__(self):
        self.workflow_templates = self._load_workflow_templates()
        self.action_registry = self._load_action_registry()
        self.generated_workflows = {}
        
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """Load pre-defined workflow templates"""
        
        return {
            'python_ci': {
                'name': 'Python CI/CD Pipeline',
                'description': 'Complete Python testing, linting, and deployment',
                'triggers': ['push', 'pull_request'],
                'jobs': {
                    'test': {
                        'runs-on': 'ubuntu-latest',
                        'strategy': {
                            'matrix': {
                                'python-version': ['3.8', '3.9', '3.10', '3.11']
                            }
                        },
                        'steps': [
                            'checkout',
                            'setup-python',
                            'install-dependencies',
                            'lint-with-flake8',
                            'test-with-pytest'
                        ]
                    },
                    'deploy': {
                        'needs': 'test',
                        'runs-on': 'ubuntu-latest',
                        'if': "github.ref == 'refs/heads/main'",
                        'steps': [
                            'checkout',
                            'setup-python',
                            'build-package',
                            'deploy-to-pypi'
                        ]
                    }
                }
            },
            'ai_code_review': {
                'name': 'AI Code Review',
                'description': 'Automated code review using AI analysis',
                'triggers': ['pull_request'],
                'jobs': {
                    'ai_review': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            'checkout',
                            'setup-python',
                            'run-ai-analysis',
                            'post-review-comments'
                        ]
                    }
                }
            },
            'auto_documentation': {
                'name': 'Auto Documentation Generator',
                'description': 'Automatically generate and update documentation',
                'triggers': ['push'],
                'jobs': {
                    'docs': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            'checkout',
                            'setup-python',
                            'generate-docs',
                            'commit-docs',
                            'deploy-docs'
                        ]
                    }
                }
            },
            'security_scan': {
                'name': 'Security Analysis',
                'description': 'Comprehensive security scanning and vulnerability detection',
                'triggers': ['push', 'pull_request', 'schedule'],
                'jobs': {
                    'security': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            'checkout',
                            'security-scan',
                            'dependency-check',
                            'code-analysis',
                            'upload-results'
                        ]
                    }
                }
            },
            'replit_sync': {
                'name': 'Replit Synchronization',
                'description': 'Sync changes between GitHub and Replit',
                'triggers': ['push'],
                'jobs': {
                    'sync': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            'checkout',
                            'sync-to-replit',
                            'notify-completion'
                        ]
                    }
                }
            }
        }
    
    def _load_action_registry(self) -> Dict[str, Any]:
        """Registry of available GitHub Actions and their configurations"""
        
        return {
            'checkout': {
                'uses': 'actions/checkout@v4',
                'description': 'Check out repository code'
            },
            'setup-python': {
                'uses': 'actions/setup-python@v4',
                'with': {
                    'python-version': '${{ matrix.python-version }}'
                },
                'description': 'Set up Python environment'
            },
            'setup-node': {
                'uses': 'actions/setup-node@v3',
                'with': {
                    'node-version': '18'
                },
                'description': 'Set up Node.js environment'
            },
            'cache-dependencies': {
                'uses': 'actions/cache@v3',
                'with': {
                    'path': '~/.cache/pip',
                    'key': '${{ runner.os }}-pip-${{ hashFiles(\'**/requirements.txt\') }}'
                },
                'description': 'Cache Python dependencies'
            },
            'install-dependencies': {
                'name': 'Install dependencies',
                'run': 'pip install -r requirements.txt',
                'description': 'Install Python dependencies'
            },
            'lint-with-flake8': {
                'name': 'Lint with flake8',
                'run': 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics',
                'description': 'Run Python linting'
            },
            'test-with-pytest': {
                'name': 'Test with pytest',
                'run': 'pytest --cov=./ --cov-report=xml',
                'description': 'Run Python tests with coverage'
            },
            'upload-coverage': {
                'uses': 'codecov/codecov-action@v3',
                'with': {
                    'file': './coverage.xml'
                },
                'description': 'Upload test coverage results'
            },
            'security-scan': {
                'uses': 'github/codeql-action/init@v2',
                'with': {
                    'languages': 'python'
                },
                'description': 'Initialize CodeQL security scanning'
            },
            'dependency-check': {
                'name': 'Run dependency check',
                'run': 'safety check',
                'description': 'Check for known security vulnerabilities'
            },
            'build-package': {
                'name': 'Build package',
                'run': 'python setup.py sdist bdist_wheel',
                'description': 'Build Python package'
            },
            'deploy-to-pypi': {
                'uses': 'pypa/gh-action-pypi-publish@v1.5.1',
                'with': {
                    'password': '${{ secrets.PYPI_API_TOKEN }}'
                },
                'description': 'Deploy package to PyPI'
            }
        }
    
    def generate_workflow(self, workflow_type: str, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete GitHub Actions workflow"""
        
        if workflow_type not in self.workflow_templates:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        template = self.workflow_templates[workflow_type]
        
        workflow = {
            'name': template['name'],
            'on': self._generate_triggers(template['triggers'], project_config),
            'jobs': {}
        }
        
        # Generate jobs
        for job_name, job_config in template['jobs'].items():
            workflow['jobs'][job_name] = self._generate_job(job_config, project_config)
        
        # Add environment variables and secrets
        if 'env' in project_config:
            workflow['env'] = project_config['env']
        
        self.generated_workflows[workflow_type] = workflow
        
        return workflow
    
    def _generate_triggers(self, triggers: List[str], project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow triggers based on project configuration"""
        
        trigger_config = {}
        
        for trigger in triggers:
            if trigger == 'push':
                trigger_config['push'] = {
                    'branches': project_config.get('main_branches', ['main', 'master'])
                }
            elif trigger == 'pull_request':
                trigger_config['pull_request'] = {
                    'branches': project_config.get('main_branches', ['main', 'master'])
                }
            elif trigger == 'schedule':
                # Daily at 2 AM UTC
                trigger_config['schedule'] = [{'cron': '0 2 * * *'}]
            elif trigger == 'workflow_dispatch':
                trigger_config['workflow_dispatch'] = {}
        
        return trigger_config
    
    def _generate_job(self, job_config: Dict[str, Any], project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete job configuration"""
        
        job = {
            'runs-on': job_config.get('runs-on', 'ubuntu-latest'),
            'steps': []
        }
        
        # Add job-level configurations
        if 'strategy' in job_config:
            job['strategy'] = job_config['strategy']
        
        if 'if' in job_config:
            job['if'] = job_config['if']
        
        if 'needs' in job_config:
            job['needs'] = job_config['needs']
        
        # Generate steps
        for step_name in job_config.get('steps', []):
            step = self._generate_step(step_name, project_config)
            if step:
                job['steps'].append(step)
        
        return job
    
    def _generate_step(self, step_name: str, project_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a workflow step"""
        
        if step_name not in self.action_registry:
            return None
        
        action_config = self.action_registry[step_name].copy()
        
        # Remove description from the actual step
        action_config.pop('description', None)
        
        # Customize step based on project configuration
        if step_name == 'setup-python' and 'python_version' in project_config:
            if 'with' not in action_config:
                action_config['with'] = {}
            action_config['with']['python-version'] = project_config['python_version']
        
        return action_config
    
    def create_custom_action(self, action_name: str, action_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom GitHub Action"""
        
        action = {
            'name': action_config.get('name', action_name),
            'description': action_config.get('description', f'Custom action: {action_name}'),
            'inputs': action_config.get('inputs', {}),
            'outputs': action_config.get('outputs', {}),
            'runs': {
                'using': action_config.get('using', 'composite'),
                'steps': action_config.get('steps', [])
            }
        }
        
        return action
    
    def generate_ai_powered_workflow(self, task_description: str, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an AI-powered workflow based on natural language description"""
        
        # Parse task description to identify workflow components
        workflow_analysis = self._analyze_task_description(task_description)
        
        # Generate base workflow structure
        workflow = {
            'name': workflow_analysis['name'],
            'on': workflow_analysis['triggers'],
            'jobs': {}
        }
        
        # Generate jobs based on analysis
        for job_name, job_requirements in workflow_analysis['jobs'].items():
            workflow['jobs'][job_name] = self._generate_ai_job(job_requirements, project_context)
        
        return workflow
    
    def _analyze_task_description(self, description: str) -> Dict[str, Any]:
        """Analyze natural language task description to extract workflow requirements"""
        
        description_lower = description.lower()
        
        analysis = {
            'name': self._extract_workflow_name(description),
            'triggers': self._extract_triggers(description_lower),
            'jobs': {}
        }
        
        # Identify job types based on keywords
        if any(word in description_lower for word in ['test', 'testing', 'pytest', 'unittest']):
            analysis['jobs']['test'] = {
                'type': 'testing',
                'requirements': ['setup-python', 'install-dependencies', 'test-with-pytest']
            }
        
        if any(word in description_lower for word in ['lint', 'linting', 'flake8', 'pylint']):
            analysis['jobs']['lint'] = {
                'type': 'linting',
                'requirements': ['setup-python', 'install-dependencies', 'lint-with-flake8']
            }
        
        if any(word in description_lower for word in ['deploy', 'deployment', 'publish']):
            analysis['jobs']['deploy'] = {
                'type': 'deployment',
                'requirements': ['setup-python', 'build-package', 'deploy-to-pypi']
            }
        
        if any(word in description_lower for word in ['security', 'scan', 'vulnerability']):
            analysis['jobs']['security'] = {
                'type': 'security',
                'requirements': ['security-scan', 'dependency-check']
            }
        
        # Default to basic CI if no specific jobs identified
        if not analysis['jobs']:
            analysis['jobs']['ci'] = {
                'type': 'continuous_integration',
                'requirements': ['setup-python', 'install-dependencies', 'test-with-pytest']
            }
        
        return analysis
    
    def _extract_workflow_name(self, description: str) -> str:
        """Extract workflow name from description"""
        
        # Simple name extraction - could be enhanced with NLP
        words = description.split()
        if len(words) > 0:
            return ' '.join(words[:5]).title()
        else:
            return 'Custom Workflow'
    
    def _extract_triggers(self, description: str) -> Dict[str, Any]:
        """Extract workflow triggers from description"""
        
        triggers = {}
        
        if 'pull request' in description or 'pr' in description:
            triggers['pull_request'] = {'branches': ['main']}
        
        if 'push' in description or 'commit' in description:
            triggers['push'] = {'branches': ['main']}
        
        if 'schedule' in description or 'daily' in description or 'nightly' in description:
            triggers['schedule'] = [{'cron': '0 2 * * *'}]
        
        # Default to push trigger if none specified
        if not triggers:
            triggers['push'] = {'branches': ['main']}
        
        return triggers
    
    def _generate_ai_job(self, job_requirements: Dict[str, Any], project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a job configuration based on AI analysis"""
        
        job = {
            'runs-on': 'ubuntu-latest',
            'steps': []
        }
        
        # Always start with checkout
        job['steps'].append(self._generate_step('checkout', project_context))
        
        # Add required steps
        for requirement in job_requirements.get('requirements', []):
            step = self._generate_step(requirement, project_context)
            if step:
                job['steps'].append(step)
        
        return job
    
    def optimize_workflow(self, workflow: Dict[str, Any], optimization_goals: List[str]) -> Dict[str, Any]:
        """Optimize workflow based on specified goals"""
        
        optimized = workflow.copy()
        
        for goal in optimization_goals:
            if goal == 'speed':
                optimized = self._optimize_for_speed(optimized)
            elif goal == 'cost':
                optimized = self._optimize_for_cost(optimized)
            elif goal == 'security':
                optimized = self._optimize_for_security(optimized)
            elif goal == 'reliability':
                optimized = self._optimize_for_reliability(optimized)
        
        return optimized
    
    def _optimize_for_speed(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow for execution speed"""
        
        # Add caching for dependencies
        for job_name, job in workflow['jobs'].items():
            steps = job.get('steps', [])
            
            # Find setup steps and add caching
            for i, step in enumerate(steps):
                if step.get('uses') == 'actions/setup-python@v4':
                    # Insert cache step after Python setup
                    cache_step = self.action_registry['cache-dependencies'].copy()
                    steps.insert(i + 1, cache_step)
                    break
        
        return workflow
    
    def _optimize_for_cost(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow for cost efficiency"""
        
        # Use smaller runner sizes where possible
        for job in workflow['jobs'].values():
            if job.get('runs-on') == 'ubuntu-latest':
                job['runs-on'] = 'ubuntu-20.04'  # Potentially cheaper
        
        return workflow
    
    def _optimize_for_security(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow for security"""
        
        # Add security scanning if not present
        security_job_exists = any(
            'security' in job_name.lower() for job_name in workflow['jobs'].keys()
        )
        
        if not security_job_exists:
            workflow['jobs']['security'] = self._generate_job(
                self.workflow_templates['security_scan']['jobs']['security'],
                {}
            )
        
        return workflow
    
    def _optimize_for_reliability(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow for reliability"""
        
        # Add retry logic and better error handling
        for job in workflow['jobs'].values():
            if 'strategy' not in job:
                job['strategy'] = {}
            
            job['strategy']['fail-fast'] = False
            
            # Add timeout to prevent hanging jobs
            job['timeout-minutes'] = 30
        
        return workflow
    
    def export_workflow_file(self, workflow: Dict[str, Any], filename: str) -> str:
        """Export workflow to YAML file"""
        
        # Ensure .github/workflows directory exists
        workflow_dir = Path('.github/workflows')
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate YAML content
        yaml_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)
        
        # Write to file
        filepath = workflow_dir / f"{filename}.yml"
        with open(filepath, 'w') as f:
            f.write(yaml_content)
        
        return str(filepath)
    
    def generate_workflow_from_template(self, template_name: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow from template with customizations"""
        
        if template_name not in self.workflow_templates:
            available = ', '.join(self.workflow_templates.keys())
            raise ValueError(f"Template '{template_name}' not found. Available: {available}")
        
        # Start with base template
        workflow = self.generate_workflow(template_name, customizations)
        
        # Apply customizations
        if 'additional_steps' in customizations:
            for job_name, additional_steps in customizations['additional_steps'].items():
                if job_name in workflow['jobs']:
                    for step_name in additional_steps:
                        step = self._generate_step(step_name, customizations)
                        if step:
                            workflow['jobs'][job_name]['steps'].append(step)
        
        return workflow
    
    def create_replit_integration_workflow(self) -> Dict[str, Any]:
        """Create a workflow specifically for Replit integration"""
        
        workflow = {
            'name': 'Replit Integration',
            'on': {
                'push': {'branches': ['main']},
                'pull_request': {'branches': ['main']}
            },
            'jobs': {
                'sync_to_replit': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Setup Python',
                            'uses': 'actions/setup-python@v4',
                            'with': {
                                'python-version': '3.11'
                            }
                        },
                        {
                            'name': 'Install dependencies',
                            'run': 'pip install -r requirements.txt'
                        },
                        {
                            'name': 'Run tests',
                            'run': 'python -m pytest'
                        },
                        {
                            'name': 'Sync to Replit',
                            'run': 'python scripts/sync_to_replit.py',
                            'env': {
                                'REPLIT_TOKEN': '${{ secrets.REPLIT_TOKEN }}'
                            }
                        }
                    ]
                }
            }
        }
        
        return workflow
    
    def get_workflow_suggestions(self, project_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze project structure and suggest appropriate workflows"""
        
        suggestions = []
        
        # Analyze project files
        files = project_structure.get('files', [])
        
        # Python project detection
        if any(f.endswith('.py') for f in files) or 'requirements.txt' in files:
            suggestions.append({
                'template': 'python_ci',
                'confidence': 0.9,
                'reason': 'Python files detected'
            })
        
        # AI/ML project detection
        if any(keyword in str(files).lower() for keyword in ['model', 'train', 'neural', 'ai', 'ml']):
            suggestions.append({
                'template': 'ai_code_review',
                'confidence': 0.7,
                'reason': 'AI/ML project detected'
            })
        
        # Documentation detection
        if any(f.endswith('.md') for f in files) or 'docs' in str(files).lower():
            suggestions.append({
                'template': 'auto_documentation',
                'confidence': 0.6,
                'reason': 'Documentation files detected'
            })
        
        # Security-sensitive project detection
        if any(keyword in str(files).lower() for keyword in ['auth', 'login', 'password', 'token', 'secret']):
            suggestions.append({
                'template': 'security_scan',
                'confidence': 0.8,
                'reason': 'Security-sensitive code detected'
            })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions


def demonstrate_workflow_generation():
    """Demonstrate workflow generation capabilities"""
    
    print("Workflow Generator Demonstration")
    print("=" * 40)
    
    generator = WorkflowGenerator()
    
    # Example 1: Generate Python CI workflow
    project_config = {
        'python_version': '3.11',
        'main_branches': ['main', 'develop'],
        'env': {
            'PYTHONPATH': './src'
        }
    }
    
    python_workflow = generator.generate_workflow('python_ci', project_config)
    print("Generated Python CI workflow:")
    print(yaml.dump(python_workflow, default_flow_style=False)[:500] + "...")
    
    # Example 2: AI-powered workflow generation
    ai_workflow = generator.generate_ai_powered_workflow(
        "Create a workflow that runs tests on every pull request and deploys to production on main branch pushes",
        project_config
    )
    print("\nAI-generated workflow:")
    print(yaml.dump(ai_workflow, default_flow_style=False)[:500] + "...")
    
    # Example 3: Workflow optimization
    optimized_workflow = generator.optimize_workflow(python_workflow, ['speed', 'security'])
    print("\nOptimized workflow (speed + security):")
    print(f"Jobs: {list(optimized_workflow['jobs'].keys())}")
    
    # Example 4: Project analysis and suggestions
    project_structure = {
        'files': ['main.py', 'requirements.txt', 'README.md', 'tests/test_main.py']
    }
    suggestions = generator.get_workflow_suggestions(project_structure)
    print(f"\nWorkflow suggestions: {[s['template'] for s in suggestions]}")
    
    print("\nWorkflow Generator demonstration completed!")


if __name__ == "__main__":
    demonstrate_workflow_generation()
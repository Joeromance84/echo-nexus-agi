#!/usr/bin/env python3
"""
GitHub Free Tier Optimizer for EchoNexus
Maximizes GitHub Actions, Codespaces, and repository features within free limits
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class GitHubUsage:
    """Track GitHub resource usage"""
    actions_minutes_used: int = 0
    storage_gb_used: float = 0.0
    lfs_bandwidth_gb: float = 0.0
    codespaces_hours: int = 0
    private_repos: int = 0
    last_updated: str = datetime.now().isoformat()

class GitHubFreeTierOptimizer:
    """
    Optimizes GitHub usage to maximize free tier benefits:
    
    Free Tier Limits:
    - Actions: 2,000 minutes/month for private repos (unlimited for public)
    - Storage: 500MB packages + 1GB LFS
    - Codespaces: 120 core hours/month + 15GB storage
    - Private repos: Unlimited (changed from 3 in 2019)
    - Bandwidth: 1GB/month for LFS
    """
    
    def __init__(self):
        self.usage_file = "echo_github_usage.json"
        self.free_limits = {
            'actions_minutes': 2000,  # Per month for private repos
            'storage_gb': 0.5,        # Package storage
            'lfs_storage_gb': 1.0,    # Git LFS storage
            'lfs_bandwidth_gb': 1.0,  # Git LFS bandwidth per month
            'codespaces_hours': 120,  # Core hours per month
            'codespaces_storage_gb': 15  # Storage for Codespaces
        }
        self.load_usage_data()
    
    def load_usage_data(self):
        """Load current GitHub usage data"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    self.usage = GitHubUsage(**data)
            else:
                self.usage = GitHubUsage()
        except Exception as e:
            print(f"Warning: Could not load GitHub usage data: {e}")
            self.usage = GitHubUsage()
    
    def optimize_actions_workflows(self) -> Dict[str, Any]:
        """
        Generate optimized GitHub Actions workflow configurations
        """
        
        optimizations = {
            'runner_strategy': {
                'primary': 'ubuntu-latest',
                'reason': '1x minute multiplier (vs 2x Windows, 10x macOS)',
                'cost_savings': 'Up to 10x more builds with Linux runners'
            },
            
            'caching_strategy': {
                'dependencies': 'Cache pip/npm/cargo dependencies aggressively',
                'build_artifacts': 'Cache intermediate build outputs',
                'docker_layers': 'Use registry caching for Docker builds',
                'example': '''
    - uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
                '''
            },
            
            'workflow_splitting': {
                'fast_feedback': 'Separate linting/testing (2-5 min) from builds (10-30 min)',
                'conditional_execution': 'Skip expensive jobs on draft PRs',
                'parallel_jobs': 'Use matrix strategy for parallel execution',
                'example_matrix': '''
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10, 3.11]
    os: [ubuntu-latest]  # Only Linux for free tier efficiency
                '''
            },
            
            'public_repo_strategy': {
                'unlimited_minutes': 'Public repos get unlimited Actions minutes',
                'recommendation': 'Consider open-sourcing core EchoNexus modules',
                'benefits': 'Unlimited CI/CD + community contributions'
            },
            
            'self_hosted_runners': {
                'when_to_use': 'For heavy workloads exceeding 2000 min/month',
                'setup': 'Use spare hardware or cloud VMs for dedicated builds',
                'cost_comparison': 'Self-hosted can be cheaper than GitHub minutes for heavy usage'
            }
        }
        
        return optimizations
    
    def optimize_storage_usage(self) -> Dict[str, Any]:
        """
        Optimize GitHub storage usage within free limits
        """
        
        storage_opts = {
            'package_registry': {
                'limit': '500MB free',
                'strategy': 'Use external registries (Docker Hub, PyPI) for large packages',
                'optimization': 'Keep only latest versions in GitHub Packages'
            },
            
            'git_lfs': {
                'limit': '1GB storage + 1GB bandwidth/month',
                'best_practices': [
                    'Use LFS for binary assets (models, datasets, APKs)',
                    'Implement LFS bandwidth tracking',
                    'Consider external storage for large files'
                ],
                'tracking_example': '''
# Track APK files with LFS
*.apk filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
models/** filter=lfs diff=lfs merge=lfs -text
                '''
            },
            
            'repository_cleanup': {
                'large_files': 'Use BFG Repo-Cleaner to remove large history',
                'branches': 'Delete merged feature branches regularly',
                'releases': 'Use releases for distributing large binaries'
            }
        }
        
        return storage_opts
    
    def generate_cost_free_workflow(self, workflow_type: str) -> str:
        """
        Generate optimized workflow YAML for maximum free tier efficiency
        """
        
        if workflow_type == "apk_build":
            return self._generate_apk_workflow()
        elif workflow_type == "python_ci":
            return self._generate_python_ci_workflow()
        elif workflow_type == "federated_deploy":
            return self._generate_federated_deploy_workflow()
        else:
            return self._generate_basic_workflow()
    
    def _generate_apk_workflow(self) -> str:
        """Generate cost-optimized APK build workflow"""
        
        return '''name: EchoNexus APK Build (Free Tier Optimized)

on:
  push:
    branches: [ main, develop ]
    paths: 
      - 'app/**'
      - 'buildozer.spec'
  pull_request:
    branches: [ main ]

jobs:
  # Fast feedback job (2-3 minutes)
  lint-and-test:
    runs-on: ubuntu-latest  # 1x multiplier
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install flake8 pytest
          
      - name: Lint code
        run: flake8 app/
        
      - name: Run tests
        run: pytest tests/

  # APK build job (only on main branch to conserve minutes)
  build-apk:
    needs: lint-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache Buildozer dependencies
        uses: actions/cache@v3
        with:
          path: |
            ~/.buildozer
            .buildozer
          key: buildozer-${{ hashFiles('buildozer.spec') }}
          
      - name: Build APK with Buildozer
        run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-11-jdk python3-pip
          pip3 install buildozer cython
          buildozer android debug
          
      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
        with:
          name: echo-nexus-apk
          path: bin/*.apk
          retention-days: 7  # Limit storage usage
'''
    
    def _generate_python_ci_workflow(self) -> str:
        """Generate Python CI workflow optimized for free tier"""
        
        return '''name: EchoNexus Python CI (Free Tier Optimized)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest  # Linux for 1x multiplier
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
      fail-fast: false  # Continue other jobs if one fails
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-${{ matrix.python-version }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-${{ matrix.python-version }}-pip-
            
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
          
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          
      - name: Test with pytest
        run: |
          pytest tests/ --cov=echo_nexus --cov-report=xml
          
      - name: Upload coverage reports
        if: matrix.python-version == '3.11'  # Only upload once
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
'''
    
    def _generate_federated_deploy_workflow(self) -> str:
        """Generate federated deployment workflow"""
        
        return '''name: EchoNexus Federated Deploy (Cost Optimized)

on:
  push:
    branches: [ main ]
    paths: 
      - 'federated_control_plane.py'
      - 'echo_nexus/**'
  workflow_dispatch:  # Manual trigger

jobs:
  # Deploy to multiple platforms efficiently
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [replit, github-pages, heroku]
      max-parallel: 3  # Control concurrency
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache deployment artifacts
        uses: actions/cache@v3
        with:
          path: |
            dist/
            build/
          key: deploy-${{ matrix.platform }}-${{ github.sha }}
          
      - name: Deploy to ${{ matrix.platform }}
        run: |
          case "${{ matrix.platform }}" in
            "replit")
              echo "Deploying to Replit..."
              # Replit deployment logic
              ;;
            "github-pages")
              echo "Deploying to GitHub Pages..."
              # GitHub Pages deployment
              ;;
            "heroku")
              echo "Deploying to Heroku..."
              # Heroku deployment
              ;;
          esac
          
      - name: Notify deployment status
        if: always()
        run: |
          echo "Deployment to ${{ matrix.platform }}: ${{ job.status }}"
'''
    
    def _generate_basic_workflow(self) -> str:
        """Generate basic optimized workflow template"""
        
        return '''name: EchoNexus Basic Workflow (Free Tier Optimized)

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  basic-checks:
    runs-on: ubuntu-latest  # Always use Linux for free tier
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache
          key: ${{ runner.os }}-cache-${{ hashFiles('**/*') }}
          
      - name: Run basic checks
        run: |
          echo "EchoNexus basic workflow executing..."
          # Add your commands here
'''
    
    def estimate_monthly_usage(self) -> Dict[str, Any]:
        """Estimate monthly GitHub resource usage"""
        
        # Get current usage (would integrate with GitHub API in practice)
        current_usage = self.usage
        
        # Calculate projections
        days_in_month = 30
        current_day = datetime.now().day
        projected_actions = (current_usage.actions_minutes_used / current_day) * days_in_month
        
        usage_projection = {
            'actions_minutes': {
                'used': current_usage.actions_minutes_used,
                'projected': int(projected_actions),
                'limit': self.free_limits['actions_minutes'],
                'utilization_percent': (projected_actions / self.free_limits['actions_minutes']) * 100,
                'status': 'healthy' if projected_actions < 1600 else 'warning' if projected_actions < 1900 else 'critical'
            },
            
            'storage': {
                'used_gb': current_usage.storage_gb_used,
                'limit_gb': self.free_limits['storage_gb'],
                'utilization_percent': (current_usage.storage_gb_used / self.free_limits['storage_gb']) * 100
            },
            
            'recommendations': self._generate_usage_recommendations(projected_actions)
        }
        
        return usage_projection
    
    def _generate_usage_recommendations(self, projected_minutes: float) -> List[str]:
        """Generate usage optimization recommendations"""
        
        recommendations = []
        
        if projected_minutes > 1800:
            recommendations.append("Consider making repositories public for unlimited Actions minutes")
            recommendations.append("Implement more aggressive caching to reduce build times")
            recommendations.append("Use conditional job execution to skip unnecessary builds")
        
        if projected_minutes > 1600:
            recommendations.append("Split workflows into fast feedback + comprehensive builds")
            recommendations.append("Use matrix builds only where necessary")
        
        recommendations.append("Always use ubuntu-latest runners (1x multiplier vs 2x/10x for other OS)")
        recommendations.append("Cache dependencies aggressively to reduce setup time")
        
        return recommendations
    
    def save_usage_data(self):
        """Save usage tracking data"""
        try:
            data = {
                'actions_minutes_used': self.usage.actions_minutes_used,
                'storage_gb_used': self.usage.storage_gb_used,
                'lfs_bandwidth_gb': self.usage.lfs_bandwidth_gb,
                'codespaces_hours': self.usage.codespaces_hours,
                'private_repos': self.usage.private_repos,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save GitHub usage data: {e}")

# Test the optimizer
if __name__ == "__main__":
    optimizer = GitHubFreeTierOptimizer()
    
    print("=== GitHub Free Tier Optimization Report ===")
    
    # Actions optimization
    actions_opts = optimizer.optimize_actions_workflows()
    print("Actions Optimizations:")
    for category, details in actions_opts.items():
        print(f"  {category}: {details.get('reason', details)}")
    
    # Generate sample workflow
    print("\n=== Sample Optimized Workflow ===")
    workflow = optimizer.generate_cost_free_workflow("apk_build")
    print(workflow[:500] + "...")
    
    # Usage estimation
    print("\n=== Usage Projection ===")
    usage = optimizer.estimate_monthly_usage()
    print(json.dumps(usage, indent=2))
#!/usr/bin/env python3
"""
Google Cloud Build Templates Library
Pre-built templates for common CI/CD patterns with intelligent platform selection
"""

import yaml
from typing import Dict, List, Any

class CloudBuildTemplates:
    """
    Comprehensive library of Cloud Build templates for different project types
    Provides direct translation from GitHub Actions patterns
    """
    
    def __init__(self):
        self.base_substitutions = {
            '_PROJECT_ID': '$PROJECT_ID',
            '_BUILD_ID': '$BUILD_ID',
            '_REPO_NAME': '$REPO_NAME',
            '_BRANCH_NAME': '$BRANCH_NAME',
            '_COMMIT_SHA': '$COMMIT_SHA',
            '_SHORT_SHA': '$SHORT_SHA'
        }
    
    def python_kivy_apk_template(self) -> Dict[str, Any]:
        """Cloud Build template for Python/Kivy APK building"""
        
        return {
            'steps': [
                # Step 1: Setup Python environment
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'],
                    'env': [
                        'PYTHONPATH=/workspace',
                        'PIP_CACHE_DIR=/workspace/.pip-cache'
                    ]
                },
                
                # Step 2: Install project dependencies
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['pip', 'install', '-r', 'requirements.txt'],
                    'env': ['PYTHONPATH=/workspace']
                },
                
                # Step 3: Install Kivy and Buildozer
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': [
                        'pip', 'install', 
                        'kivy[base]', 'buildozer', 'cython==0.29.33', 
                        'pyjnius', 'plyer'
                    ],
                    'timeout': '600s'
                },
                
                # Step 4: Setup Android SDK
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'entrypoint': 'bash',
                    'args': [
                        '-c',
                        '''
                        export ANDROID_HOME=/opt/android-sdk
                        export ANDROID_SDK_ROOT=/opt/android-sdk
                        export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
                        mkdir -p $ANDROID_HOME
                        '''
                    ],
                    'env': [
                        'ANDROID_HOME=/opt/android-sdk',
                        'ANDROID_SDK_ROOT=/opt/android-sdk'
                    ]
                },
                
                # Step 5: Initialize Buildozer
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'init'],
                    'env': [
                        'ANDROID_HOME=/opt/android-sdk',
                        'ANDROID_SDK_ROOT=/opt/android-sdk'
                    ]
                },
                
                # Step 6: Build APK
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'android', 'debug'],
                    'timeout': '3600s',  # 1 hour for APK builds
                    'env': [
                        'ANDROID_HOME=/opt/android-sdk',
                        'ANDROID_SDK_ROOT=/opt/android-sdk',
                        'BUILDOZER_BUILD_DIR=/workspace/.buildozer'
                    ]
                },
                
                # Step 7: Copy APK to standardized location
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'entrypoint': 'bash',
                    'args': [
                        '-c',
                        '''
                        mkdir -p /workspace/artifacts
                        cp bin/*.apk /workspace/artifacts/ || echo "No APK found in bin/"
                        ls -la /workspace/artifacts/
                        '''
                    ]
                },
                
                # Step 8: Upload to Cloud Storage
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'args': [
                        'gsutil', '-m', 'cp', '-r',
                        '/workspace/artifacts/*',
                        'gs://${_STORAGE_BUCKET}/${_REPO_NAME}/${_BUILD_ID}/'
                    ]
                }
            ],
            
            'timeout': '7200s',  # 2 hours total timeout
            
            'options': {
                'substitution_option': 'ALLOW_LOOSE',
                'dynamic_substitutions': True,
                'logging': 'CLOUD_LOGGING_ONLY',
                'disk_size_gb': 100,  # Larger disk for Android builds
                'machine_type': 'E2_HIGHCPU_8'  # High CPU for faster builds
            },
            
            'substitutions': {
                '_STORAGE_BUCKET': '${PROJECT_ID}-apk-builds',
                '_APK_NAME': 'app-debug',
                **self.base_substitutions
            },
            
            'artifacts': {
                'objects': {
                    'location': 'gs://${_STORAGE_BUCKET}/${_REPO_NAME}/${_BUILD_ID}',
                    'paths': ['/workspace/artifacts/*']
                }
            }
        }
    
    def docker_containerized_build_template(self) -> Dict[str, Any]:
        """Cloud Build template using Docker for reproducible builds"""
        
        return {
            'steps': [
                # Step 1: Build custom Android build environment
                {
                    'name': 'gcr.io/cloud-builders/docker',
                    'args': [
                        'build',
                        '-t', 'gcr.io/${PROJECT_ID}/android-kivy-builder:${BUILD_ID}',
                        '-f', 'docker/Dockerfile.android',
                        '.'
                    ]
                },
                
                # Step 2: Run build inside container
                {
                    'name': 'gcr.io/${PROJECT_ID}/android-kivy-builder:${BUILD_ID}',
                    'args': ['buildozer', 'android', 'debug'],
                    'timeout': '3600s'
                },
                
                # Step 3: Extract artifacts
                {
                    'name': 'gcr.io/cloud-builders/docker',
                    'entrypoint': 'bash',
                    'args': [
                        '-c',
                        '''
                        docker create --name temp gcr.io/${PROJECT_ID}/android-kivy-builder:${BUILD_ID}
                        docker cp temp:/app/bin ./artifacts
                        docker rm temp
                        '''
                    ]
                },
                
                # Step 4: Upload artifacts
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'args': [
                        'gsutil', 'cp', '-r', 'artifacts/*',
                        'gs://${_STORAGE_BUCKET}/${BUILD_ID}/'
                    ]
                }
            ],
            
            'timeout': '5400s',  # 1.5 hours
            'substitutions': {
                '_STORAGE_BUCKET': '${PROJECT_ID}-builds',
                **self.base_substitutions
            }
        }
    
    def multi_stage_pipeline_template(self) -> Dict[str, Any]:
        """Complex multi-stage pipeline with testing, building, and deployment"""
        
        return {
            'steps': [
                # Stage 1: Code Quality & Testing
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['pip', 'install', 'pytest', 'flake8', 'black'],
                    'id': 'install-test-deps'
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['black', '--check', '.'],
                    'id': 'code-formatting',
                    'waitFor': ['install-test-deps']
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['flake8', '.'],
                    'id': 'linting',
                    'waitFor': ['install-test-deps']
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['pytest', '-v'],
                    'id': 'unit-tests',
                    'waitFor': ['code-formatting', 'linting']
                },
                
                # Stage 2: Build APK
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['pip', 'install', '-r', 'requirements.txt'],
                    'id': 'install-deps',
                    'waitFor': ['unit-tests']
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'android', 'debug'],
                    'id': 'build-apk',
                    'timeout': '3600s',
                    'waitFor': ['install-deps']
                },
                
                # Stage 3: Security Scanning
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'args': [
                        'beta', 'container', 'images', 'scan',
                        'bin/*.apk'
                    ],
                    'id': 'security-scan',
                    'waitFor': ['build-apk']
                },
                
                # Stage 4: Deploy/Upload
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'args': [
                        'gsutil', 'cp', 'bin/*.apk',
                        'gs://${_STORAGE_BUCKET}/releases/${TAG_NAME}/'
                    ],
                    'id': 'deploy',
                    'waitFor': ['security-scan']
                }
            ],
            
            'timeout': '7200s',
            'substitutions': {
                '_STORAGE_BUCKET': '${PROJECT_ID}-releases',
                **self.base_substitutions
            }
        }
    
    def parallel_build_template(self) -> Dict[str, Any]:
        """Parallel builds for multiple architectures/versions"""
        
        return {
            'steps': [
                # Parallel APK builds for different architectures
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'android', 'debug', '--arch=arm64-v8a'],
                    'id': 'build-arm64',
                    'timeout': '3600s'
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'android', 'debug', '--arch=armeabi-v7a'],
                    'id': 'build-arm32',
                    'timeout': '3600s'
                },
                
                {
                    'name': 'gcr.io/cloud-builders/python',
                    'args': ['buildozer', 'android', 'debug', '--arch=x86_64'],
                    'id': 'build-x86',
                    'timeout': '3600s'
                },
                
                # Collect all builds
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'entrypoint': 'bash',
                    'args': [
                        '-c',
                        '''
                        mkdir -p /workspace/all-builds
                        cp bin/*arm64* /workspace/all-builds/app-arm64.apk || true
                        cp bin/*armeabi* /workspace/all-builds/app-arm32.apk || true
                        cp bin/*x86* /workspace/all-builds/app-x86.apk || true
                        ls -la /workspace/all-builds/
                        '''
                    ],
                    'waitFor': ['build-arm64', 'build-arm32', 'build-x86']
                },
                
                # Upload all builds
                {
                    'name': 'gcr.io/cloud-builders/gcloud',
                    'args': [
                        'gsutil', '-m', 'cp', '/workspace/all-builds/*',
                        'gs://${_STORAGE_BUCKET}/multi-arch/${BUILD_ID}/'
                    ],
                    'waitFor': ['-']  # Wait for previous step
                }
            ],
            
            'timeout': '7200s',
            'options': {
                'machine_type': 'E2_HIGHCPU_32',  # High-end machine for parallel builds
                'disk_size_gb': 200
            }
        }

class CloudBuildTriggerTemplates:
    """Templates for Cloud Build triggers with different activation patterns"""
    
    @staticmethod
    def github_push_trigger(repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Standard push trigger for GitHub repositories"""
        
        return {
            'name': f'github-push-{repo_name}',
            'description': f'Build {repo_name} on push to main branch',
            'github': {
                'owner': repo_owner,
                'name': repo_name,
                'push': {
                    'branch': '^main$'
                }
            },
            'filename': 'cloudbuild.yaml',
            'substitutions': {
                '_TRIGGER_TYPE': 'push',
                '_REPO_FULL_NAME': f'{repo_owner}/{repo_name}'
            }
        }
    
    @staticmethod
    def github_pr_trigger(repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Pull request trigger for GitHub repositories"""
        
        return {
            'name': f'github-pr-{repo_name}',
            'description': f'Test {repo_name} on pull requests',
            'github': {
                'owner': repo_owner,
                'name': repo_name,
                'pullRequest': {
                    'branch': '^main$',
                    'commentControl': 'COMMENTS_ENABLED'
                }
            },
            'filename': 'cloudbuild-pr.yaml',
            'substitutions': {
                '_TRIGGER_TYPE': 'pull_request',
                '_REPO_FULL_NAME': f'{repo_owner}/{repo_name}'
            }
        }
    
    @staticmethod
    def release_trigger(repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Release trigger for tagged versions"""
        
        return {
            'name': f'github-release-{repo_name}',
            'description': f'Release build for {repo_name} on tags',
            'github': {
                'owner': repo_owner,
                'name': repo_name,
                'push': {
                    'tag': '^v.*'
                }
            },
            'filename': 'cloudbuild-release.yaml',
            'substitutions': {
                '_TRIGGER_TYPE': 'release',
                '_REPO_FULL_NAME': f'{repo_owner}/{repo_name}',
                '_RELEASE_BUILD': 'true'
            }
        }
    
    @staticmethod
    def manual_trigger(repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Manual trigger for on-demand builds"""
        
        return {
            'name': f'manual-build-{repo_name}',
            'description': f'Manual build trigger for {repo_name}',
            'github': {
                'owner': repo_owner,
                'name': repo_name,
                'push': {
                    'branch': '.*'  # Any branch
                }
            },
            'disabled': True,  # Must be manually enabled
            'filename': 'cloudbuild.yaml',
            'substitutions': {
                '_TRIGGER_TYPE': 'manual',
                '_REPO_FULL_NAME': f'{repo_owner}/{repo_name}'
            }
        }

def generate_cloudbuild_yaml(template_name: str, **kwargs) -> str:
    """Generate cloudbuild.yaml from template"""
    
    templates = CloudBuildTemplates()
    
    template_map = {
        'kivy_apk': templates.python_kivy_apk_template,
        'docker_build': templates.docker_containerized_build_template,
        'multi_stage': templates.multi_stage_pipeline_template,
        'parallel_build': templates.parallel_build_template
    }
    
    if template_name not in template_map:
        raise ValueError(f"Unknown template: {template_name}")
    
    config = template_map[template_name]()
    
    # Apply any custom substitutions
    if 'substitutions' in kwargs:
        config['substitutions'].update(kwargs['substitutions'])
    
    return yaml.dump(config, default_flow_style=False, sort_keys=False)

def main():
    """Demonstrate Cloud Build templates"""
    
    print("🏗️ Cloud Build Templates Library")
    print("=" * 50)
    
    templates = CloudBuildTemplates()
    
    # Generate example configurations
    print("Available templates:")
    print("1. Python/Kivy APK Build")
    print("2. Docker Containerized Build")
    print("3. Multi-stage Pipeline")
    print("4. Parallel Architecture Build")
    
    # Example: Generate Kivy APK template
    kivy_config = templates.python_kivy_apk_template()
    
    print(f"\nKivy APK template has {len(kivy_config['steps'])} build steps")
    print(f"Timeout: {kivy_config['timeout']}")
    print(f"Machine type: {kivy_config['options']['machine_type']}")
    
    # Generate YAML output
    yaml_output = generate_cloudbuild_yaml('kivy_apk')
    
    print("\nGenerated cloudbuild.yaml preview:")
    print("-" * 30)
    print(yaml_output[:500] + "..." if len(yaml_output) > 500 else yaml_output)
    
    print("\n✅ Cloud Build templates ready for deployment!")

if __name__ == "__main__":
    main()
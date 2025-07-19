#!/usr/bin/env python3
"""
Secure Google Cloud Build Authentication System
Implements secure Service Account authentication with comprehensive verification
"""

import os
import json
import subprocess
import tempfile
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuthenticationResult:
    """Results of authentication attempt"""
    success: bool
    service_account_email: str
    project_id: str
    error_message: str = ""
    verification_details: Dict[str, Any] = None

class GoogleCloudAuthenticator:
    """
    Secure Google Cloud Build authentication using Service Account credentials
    Follows security best practices with least-privilege access
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auth_result = None
        
    def setup_authentication(self) -> AuthenticationResult:
        """
        Setup Google Cloud authentication using Service Account from Replit Secrets
        Implements the comprehensive 3-phase authentication plan
        """
        
        # Phase 1: Retrieve Service Account credentials from Replit Secrets
        credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if not credentials_json:
            return AuthenticationResult(
                success=False,
                service_account_email="",
                project_id="",
                error_message="GOOGLE_APPLICATION_CREDENTIALS_JSON secret not found in Replit environment"
            )
        
        try:
            # Parse credentials to extract service account info
            credentials_data = json.loads(credentials_json)
            service_account_email = credentials_data.get('client_email', '')
            project_id = credentials_data.get('project_id', '')
            
            if not service_account_email or not project_id:
                return AuthenticationResult(
                    success=False,
                    service_account_email="",
                    project_id="",
                    error_message="Invalid service account credentials format"
                )
            
            # Phase 2: Create temporary credentials file for gcloud
            success = self._configure_gcloud_credentials(credentials_json)
            
            if not success:
                return AuthenticationResult(
                    success=False,
                    service_account_email=service_account_email,
                    project_id=project_id,
                    error_message="Failed to configure gcloud credentials"
                )
            
            # Phase 3: Verify authentication and test Cloud Build access
            verification_result = self._verify_authentication_and_permissions()
            
            self.auth_result = AuthenticationResult(
                success=verification_result['success'],
                service_account_email=service_account_email,
                project_id=project_id,
                error_message=verification_result.get('error', ''),
                verification_details=verification_result
            )
            
            return self.auth_result
            
        except json.JSONDecodeError as e:
            return AuthenticationResult(
                success=False,
                service_account_email="",
                project_id="",
                error_message=f"Invalid JSON in credentials: {str(e)}"
            )
        except Exception as e:
            return AuthenticationResult(
                success=False,
                service_account_email="",
                project_id="",
                error_message=f"Authentication setup failed: {str(e)}"
            )
    
    def _configure_gcloud_credentials(self, credentials_json: str) -> bool:
        """Configure gcloud CLI with service account credentials"""
        
        try:
            # Create temporary file for credentials
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file.write(credentials_json)
                temp_credentials_path = temp_file.name
            
            # Set environment variable for Google Cloud libraries
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_credentials_path
            
            # Activate service account with gcloud
            activate_cmd = [
                'gcloud', 'auth', 'activate-service-account',
                '--key-file', temp_credentials_path
            ]
            
            result = subprocess.run(
                activate_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.logger.error(f"gcloud auth activation failed: {result.stderr}")
                return False
            
            # Set project for gcloud
            credentials_data = json.loads(credentials_json)
            project_id = credentials_data.get('project_id')
            
            if project_id:
                set_project_cmd = ['gcloud', 'config', 'set', 'project', project_id]
                subprocess.run(set_project_cmd, capture_output=True, timeout=15)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure gcloud credentials: {str(e)}")
            return False
    
    def _verify_authentication_and_permissions(self) -> Dict[str, Any]:
        """
        Comprehensive verification of authentication and Cloud Build permissions
        Implements the verification tests from the authentication plan
        """
        
        verification_results = {
            'success': False,
            'tests_passed': [],
            'tests_failed': [],
            'auth_list_result': None,
            'dry_run_result': None,
            'permissions_check': None
        }
        
        # Test 1: Verify gcloud authentication
        auth_test = self._test_gcloud_auth_list()
        verification_results['auth_list_result'] = auth_test
        
        if auth_test['success']:
            verification_results['tests_passed'].append('gcloud_auth_list')
        else:
            verification_results['tests_failed'].append('gcloud_auth_list')
            verification_results['error'] = auth_test['error']
            return verification_results
        
        # Test 2: Check Cloud Build permissions
        permissions_test = self._test_cloud_build_permissions()
        verification_results['permissions_check'] = permissions_test
        
        if permissions_test['success']:
            verification_results['tests_passed'].append('cloud_build_permissions')
        else:
            verification_results['tests_failed'].append('cloud_build_permissions')
            verification_results['error'] = permissions_test['error']
            return verification_results
        
        # Test 3: Dry run Cloud Build submission
        dry_run_test = self._test_cloud_build_dry_run()
        verification_results['dry_run_result'] = dry_run_test
        
        if dry_run_test['success']:
            verification_results['tests_passed'].append('cloud_build_dry_run')
            verification_results['success'] = True
        else:
            verification_results['tests_failed'].append('cloud_build_dry_run')
            verification_results['error'] = dry_run_test['error']
        
        return verification_results
    
    def _test_gcloud_auth_list(self) -> Dict[str, Any]:
        """Test gcloud auth list command to verify authentication"""
        
        try:
            result = subprocess.run(
                ['gcloud', 'auth', 'list', '--format=json'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f"gcloud auth list failed: {result.stderr}"
                }
            
            auth_accounts = json.loads(result.stdout)
            
            if not auth_accounts:
                return {
                    'success': False,
                    'error': "No authenticated accounts found"
                }
            
            # Find active service account
            active_account = None
            for account in auth_accounts:
                if account.get('status') == 'ACTIVE':
                    active_account = account
                    break
            
            if not active_account:
                return {
                    'success': False,
                    'error': "No active authenticated account found"
                }
            
            return {
                'success': True,
                'active_account': active_account['account'],
                'account_type': active_account.get('type', 'unknown')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"gcloud auth list test failed: {str(e)}"
            }
    
    def _test_cloud_build_permissions(self) -> Dict[str, Any]:
        """Test Cloud Build API access and permissions"""
        
        try:
            # Test listing Cloud Build triggers (requires read permissions)
            result = subprocess.run(
                ['gcloud', 'builds', 'triggers', 'list', '--format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f"Cloud Build permissions test failed: {result.stderr}"
                }
            
            # If we can list triggers, we have at least read access
            triggers = json.loads(result.stdout)
            
            return {
                'success': True,
                'triggers_found': len(triggers),
                'api_accessible': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Cloud Build permissions test failed: {str(e)}"
            }
    
    def _test_cloud_build_dry_run(self) -> Dict[str, Any]:
        """Test Cloud Build submission with a simple dry run build"""
        
        try:
            # Create simple cloudbuild.yaml content for testing
            test_cloudbuild = {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'entrypoint': 'bash',
                        'args': ['-c', 'echo "Authentication successful. Build verified!"']
                    }
                ],
                'timeout': '60s'
            }
            
            # Create temporary cloudbuild.yaml file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
                json.dump(test_cloudbuild, temp_file)
                temp_config_path = temp_file.name
            
            # Submit dry run build
            result = subprocess.run([
                'gcloud', 'builds', 'submit',
                '--config', temp_config_path,
                '--no-source',  # No source code needed for this test
                '--async'  # Don't wait for completion
            ], capture_output=True, text=True, timeout=60)
            
            # Clean up temporary file
            os.unlink(temp_config_path)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f"Cloud Build dry run failed: {result.stderr}"
                }
            
            # Parse build submission result
            output_lines = result.stdout.strip().split('\n')
            build_id = None
            
            for line in output_lines:
                if 'BUILD_ID:' in line or 'ID:' in line:
                    build_id = line.split(':')[-1].strip()
                    break
            
            return {
                'success': True,
                'build_id': build_id,
                'build_submitted': True,
                'message': 'Cloud Build dry run submitted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Cloud Build dry run test failed: {str(e)}"
            }
    
    def get_authentication_status(self) -> Optional[AuthenticationResult]:
        """Get current authentication status"""
        return self.auth_result
    
    def generate_setup_instructions(self) -> str:
        """Generate detailed setup instructions for Google Cloud authentication"""
        
        return """
🔐 Google Cloud Build Authentication Setup Instructions

Phase 1: Google Cloud Service Account Creation
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Navigate to IAM & Admin > Service Accounts
3. Click "Create Service Account"
4. Name: replit-builder-agi
5. Description: Service account for Replit AGI automated builds
6. Grant role: Cloud Build Editor
7. Click "Done"

Phase 2: Service Account Key Generation  
1. Click on your new service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose JSON format
5. Download the JSON file (keep it secure!)

Phase 3: Replit Secret Configuration
1. In Replit, click the lock icon (Secrets)
2. Add new secret:
   - Key: GOOGLE_APPLICATION_CREDENTIALS_JSON
   - Value: Paste the ENTIRE contents of the downloaded JSON file
3. Save the secret

Phase 4: Verification
Run the authentication setup to verify all components are working correctly.
The system will test gcloud authentication, permissions, and Cloud Build access.

Security Notes:
- The JSON key is your AGI's credential - keep it secure
- Service account has minimal permissions (Cloud Build Editor only)
- Credentials are stored securely in Replit Secrets
- All authentication is verifiable and auditable
"""

def main():
    """Demonstrate Google Cloud authentication system"""
    
    print("🔐 Google Cloud Build Authentication System")
    print("=" * 60)
    
    authenticator = GoogleCloudAuthenticator()
    
    # Check if credentials are available
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
        print("⚠️ GOOGLE_APPLICATION_CREDENTIALS_JSON not found in environment")
        print("\nSetup Instructions:")
        print(authenticator.generate_setup_instructions())
        return
    
    print("Setting up Google Cloud authentication...")
    auth_result = authenticator.setup_authentication()
    
    if auth_result.success:
        print("✅ Authentication successful!")
        print(f"Service Account: {auth_result.service_account_email}")
        print(f"Project ID: {auth_result.project_id}")
        
        if auth_result.verification_details:
            details = auth_result.verification_details
            print(f"Tests passed: {', '.join(details['tests_passed'])}")
            
            if details.get('dry_run_result', {}).get('build_id'):
                print(f"Test build ID: {details['dry_run_result']['build_id']}")
    else:
        print("❌ Authentication failed!")
        print(f"Error: {auth_result.error_message}")
        
        if "not found" in auth_result.error_message:
            print("\nSetup Instructions:")
            print(authenticator.generate_setup_instructions())

if __name__ == "__main__":
    main()
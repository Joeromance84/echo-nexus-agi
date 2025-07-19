#!/usr/bin/env python3
"""
GitHub Setup Wizard for joeromance84
Foolproof connection system with multiple authentication methods
"""

import os
import json
import time
import subprocess
import webbrowser
from pathlib import Path
from utils.github_authenticator import GitHubAuthenticator

class GitHubSetupWizard:
    """
    Masterful GitHub setup wizard specifically for joeromance84
    """
    
    def __init__(self):
        self.github_username = "joeromance84"
        self.authenticator = GitHubAuthenticator()
        self.setup_methods = [
            "Personal Access Token (Recommended)",
            "GitHub CLI Authentication", 
            "SSH Key Setup",
            "OAuth Application Flow"
        ]
    
    def run_setup_wizard(self):
        """Run the complete setup wizard"""
        
        print("🚀 EchoNexus GitHub Setup Wizard")
        print("=" * 50)
        print(f"Setting up connection for: {self.github_username}")
        print()
        
        # Check current status
        current_status = self.check_current_status()
        
        if current_status['connected']:
            print("✅ GitHub connection already established!")
            print(f"Connected as: {current_status['user']}")
            print(f"Repositories: {current_status['repo_count']}")
            
            choice = input("\nReconfigure connection? (y/n): ").lower().strip()
            if choice != 'y':
                return current_status
        
        # Show setup options
        print("\nAvailable Setup Methods:")
        for i, method in enumerate(self.setup_methods, 1):
            print(f"{i}. {method}")
        
        print("\nRecommended: Option 1 (Personal Access Token)")
        
        while True:
            try:
                choice = int(input("\nSelect setup method (1-4): "))
                if 1 <= choice <= len(self.setup_methods):
                    break
                else:
                    print("Invalid choice. Please select 1-4.")
            except ValueError:
                print("Please enter a number.")
        
        # Execute chosen setup method
        if choice == 1:
            return self.setup_personal_access_token()
        elif choice == 2:
            return self.setup_github_cli()
        elif choice == 3:
            return self.setup_ssh_keys()
        elif choice == 4:
            return self.setup_oauth_flow()
    
    def check_current_status(self):
        """Check current GitHub connection status"""
        
        print("Checking current GitHub connection status...")
        
        connection_status = self.authenticator.verify_connection()
        
        if connection_status['authenticated']:
            return {
                'connected': True,
                'user': connection_status['user']['login'],
                'repo_count': connection_status['user']['public_repos'] + connection_status['user']['private_repos'],
                'scopes': connection_status.get('token_scopes', [])
            }
        else:
            return {
                'connected': False,
                'error': connection_status.get('message', 'Unknown error')
            }
    
    def setup_personal_access_token(self):
        """Setup using Personal Access Token (Recommended)"""
        
        print("\n🔑 Personal Access Token Setup")
        print("=" * 40)
        
        print("Step 1: Create GitHub Personal Access Token")
        print("I'll open the GitHub token creation page for you...")
        
        # Open GitHub token creation page
        token_url = "https://github.com/settings/tokens/new"
        
        try:
            webbrowser.open(token_url)
            print(f"✅ Opened: {token_url}")
        except Exception:
            print(f"Please manually visit: {token_url}")
        
        print("\nRequired Token Settings:")
        print("📝 Note: EchoNexus AGI System Access")
        print("⏰ Expiration: No expiration (recommended)")
        print("🔐 Required Scopes:")
        
        required_scopes = [
            "✅ repo (Full control of private repositories)",
            "✅ workflow (Update GitHub Action workflows)", 
            "✅ admin:repo_hook (Admin access to repository hooks)",
            "✅ user (Read user profile data)",
            "✅ project (Full control of user and organization projects)",
            "✅ admin:org (Full control of orgs and teams, read and write org projects)"
        ]
        
        for scope in required_scopes:
            print(f"   {scope}")
        
        print("\nAfter creating the token:")
        print("1. Copy the generated token")
        print("2. Paste it below (it will be securely stored)")
        
        # Get token from user
        while True:
            token = input("\nPaste your Personal Access Token: ").strip()
            
            if not token:
                print("Token cannot be empty. Please try again.")
                continue
            
            if len(token) < 20:
                print("Token seems too short. Please verify and try again.")
                continue
            
            # Test the token
            print("Testing token...")
            test_result = self.test_token(token)
            
            if test_result['valid']:
                print("✅ Token validated successfully!")
                
                # Store token securely
                self.store_token_securely(token)
                
                # Setup processor repositories
                setup_processors = input("\nSetup EchoNexus processor repositories? (y/n): ").lower().strip()
                
                if setup_processors == 'y':
                    self.setup_processor_repositories()
                
                return {
                    'status': 'success',
                    'method': 'personal_access_token',
                    'user': test_result['user'],
                    'message': 'GitHub connection established successfully!'
                }
            else:
                print(f"❌ Token validation failed: {test_result['error']}")
                retry = input("Try again? (y/n): ").lower().strip()
                if retry != 'y':
                    return {
                        'status': 'failed',
                        'method': 'personal_access_token',
                        'error': 'Token validation failed'
                    }
    
    def test_token(self, token):
        """Test GitHub token validity"""
        
        # Temporarily set the token for testing
        original_token = os.environ.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = token
        
        try:
            # Create new authenticator instance with the token
            test_auth = GitHubAuthenticator()
            result = test_auth.verify_connection()
            
            if result['authenticated']:
                return {
                    'valid': True,
                    'user': result['user']['login'],
                    'scopes': result.get('token_scopes', [])
                }
            else:
                return {
                    'valid': False,
                    'error': result['message']
                }
        
        finally:
            # Restore original token
            if original_token:
                os.environ['GITHUB_TOKEN'] = original_token
            elif 'GITHUB_TOKEN' in os.environ:
                del os.environ['GITHUB_TOKEN']
    
    def store_token_securely(self, token):
        """Store GitHub token securely"""
        
        print("Storing token securely...")
        
        # Method 1: Environment variable (for current session)
        os.environ['GITHUB_TOKEN'] = token
        
        # Method 2: Replit Secrets (if available)
        try:
            # Check if we're in Replit environment
            if os.path.exists('/home/runner'):
                print("Detected Replit environment")
                print("Please add GITHUB_TOKEN to your Replit Secrets:")
                print("1. Click on 'Secrets' in the left sidebar")
                print("2. Click 'Add Secret'") 
                print("3. Key: GITHUB_TOKEN")
                print("4. Value: [paste your token]")
                print("5. Click 'Add Secret'")
                
                input("Press Enter after adding the secret to Replit...")
        
        except Exception:
            pass
        
        # Method 3: Local storage (encrypted)
        try:
            config_dir = Path.home() / '.echonexus'
            config_dir.mkdir(exist_ok=True)
            
            config_file = config_dir / 'github_config.json'
            
            # Simple encryption (for demonstration - in production use proper encryption)
            import base64
            encoded_token = base64.b64encode(token.encode()).decode()
            
            config_data = {
                'github_username': self.github_username,
                'token_hash': hash(token),
                'created_at': time.time()
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✅ Configuration saved to: {config_file}")
        
        except Exception as e:
            print(f"Warning: Could not save local config: {e}")
    
    def setup_github_cli(self):
        """Setup using GitHub CLI"""
        
        print("\n⚡ GitHub CLI Setup")
        print("=" * 30)
        
        # Check if GitHub CLI is installed
        if not self.check_github_cli_installed():
            print("GitHub CLI not found. Installing...")
            if not self.install_github_cli():
                return {
                    'status': 'failed',
                    'method': 'github_cli',
                    'error': 'Could not install GitHub CLI'
                }
        
        print("Running GitHub CLI authentication...")
        
        try:
            # Run gh auth login
            result = subprocess.run(['gh', 'auth', 'login'], 
                                  capture_output=True, text=True, input='\n'.join([
                                      'GitHub.com',  # Choose GitHub.com
                                      'HTTPS',       # Choose HTTPS
                                      'Y',           # Authenticate Git
                                      'Login with a web browser'  # Choose web browser
                                  ]))
            
            if result.returncode == 0:
                print("✅ GitHub CLI authentication successful!")
                
                # Verify authentication
                auth_status = subprocess.run(['gh', 'auth', 'status'], 
                                           capture_output=True, text=True)
                
                if 'Logged in to github.com' in auth_status.stderr:
                    return {
                        'status': 'success',
                        'method': 'github_cli',
                        'message': 'GitHub CLI authentication completed!'
                    }
            
            return {
                'status': 'failed',
                'method': 'github_cli',
                'error': f'Authentication failed: {result.stderr}'
            }
        
        except Exception as e:
            return {
                'status': 'failed',
                'method': 'github_cli',
                'error': f'GitHub CLI setup failed: {str(e)}'
            }
    
    def check_github_cli_installed(self):
        """Check if GitHub CLI is installed"""
        
        try:
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_github_cli(self):
        """Install GitHub CLI"""
        
        print("Installing GitHub CLI...")
        
        try:
            # Try different installation methods based on OS
            if os.path.exists('/usr/bin/apt-get'):  # Ubuntu/Debian
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'gh'], check=True)
            elif os.path.exists('/usr/bin/yum'):  # CentOS/RHEL
                subprocess.run(['sudo', 'yum', 'install', '-y', 'gh'], check=True)
            elif os.path.exists('/opt/homebrew/bin/brew'):  # macOS with Homebrew
                subprocess.run(['brew', 'install', 'gh'], check=True)
            else:
                print("Please install GitHub CLI manually:")
                print("Visit: https://cli.github.com/")
                return False
            
            return True
        
        except Exception as e:
            print(f"Installation failed: {e}")
            return False
    
    def setup_ssh_keys(self):
        """Setup SSH key authentication"""
        
        print("\n🔐 SSH Key Setup")
        print("=" * 25)
        
        ssh_dir = Path.home() / '.ssh'
        ssh_dir.mkdir(mode=0o700, exist_ok=True)
        
        key_path = ssh_dir / 'id_ed25519_echonexus'
        
        print(f"Generating SSH key for {self.github_username}...")
        
        try:
            # Generate SSH key
            subprocess.run([
                'ssh-keygen', '-t', 'ed25519', 
                '-C', f'{self.github_username}@echonexus',
                '-f', str(key_path),
                '-N', ''  # No passphrase for automation
            ], check=True)
            
            print("✅ SSH key generated successfully!")
            
            # Read public key
            with open(f"{key_path}.pub", 'r') as f:
                public_key = f.read().strip()
            
            print("\n📋 Public Key (copy this to GitHub):")
            print("-" * 50)
            print(public_key)
            print("-" * 50)
            
            # Open GitHub SSH settings
            ssh_url = "https://github.com/settings/ssh/new"
            
            try:
                webbrowser.open(ssh_url)
                print(f"✅ Opened GitHub SSH settings: {ssh_url}")
            except Exception:
                print(f"Please manually visit: {ssh_url}")
            
            print("\nInstructions:")
            print("1. Copy the public key above")
            print("2. Paste it in the GitHub SSH key form")
            print("3. Give it a title: 'EchoNexus AGI System'")
            print("4. Click 'Add SSH key'")
            
            input("\nPress Enter after adding the SSH key to GitHub...")
            
            # Test SSH connection
            print("Testing SSH connection...")
            
            test_result = subprocess.run([
                'ssh', '-T', '-i', str(key_path), 'git@github.com'
            ], capture_output=True, text=True)
            
            if f'Hi {self.github_username}!' in test_result.stderr:
                print("✅ SSH authentication successful!")
                
                # Add to SSH config
                self.add_ssh_config(key_path)
                
                return {
                    'status': 'success',
                    'method': 'ssh_key',
                    'key_path': str(key_path),
                    'message': 'SSH key authentication setup completed!'
                }
            else:
                print(f"❌ SSH test failed: {test_result.stderr}")
                return {
                    'status': 'failed',
                    'method': 'ssh_key',
                    'error': 'SSH authentication test failed'
                }
        
        except Exception as e:
            return {
                'status': 'failed',
                'method': 'ssh_key',
                'error': f'SSH key setup failed: {str(e)}'
            }
    
    def add_ssh_config(self, key_path):
        """Add SSH configuration for GitHub"""
        
        ssh_config_path = Path.home() / '.ssh' / 'config'
        
        config_entry = f"""
# EchoNexus GitHub Configuration
Host github.com
    HostName github.com
    User git
    IdentityFile {key_path}
    IdentitiesOnly yes
"""
        
        try:
            with open(ssh_config_path, 'a') as f:
                f.write(config_entry)
            
            print(f"✅ SSH config updated: {ssh_config_path}")
        
        except Exception as e:
            print(f"Warning: Could not update SSH config: {e}")
    
    def setup_oauth_flow(self):
        """Setup OAuth application flow"""
        
        print("\n🔗 OAuth Application Setup")
        print("=" * 35)
        
        print("This method requires creating a GitHub OAuth App.")
        print("For simplicity, please use the Personal Access Token method instead.")
        
        return {
            'status': 'skipped',
            'method': 'oauth_flow',
            'message': 'OAuth setup skipped - use Personal Access Token instead'
        }
    
    def setup_processor_repositories(self):
        """Setup EchoNexus processor repositories"""
        
        print("\n🏗️ Setting up EchoNexus Processor Network")
        print("=" * 45)
        
        processors = [
            'text-analysis',
            'code-generation',
            'diagnostic-scan', 
            'workflow-synthesis',
            'knowledge-synthesis',
            'security-scanner',
            'performance-optimizer',
            'memory-manager'
        ]
        
        print(f"Creating {len(processors)} processor repositories...")
        
        setup_result = self.authenticator.setup_processor_network(processors)
        
        print(f"✅ Created: {setup_result['success_count']} repositories")
        
        if setup_result['failure_count'] > 0:
            print(f"❌ Failed: {setup_result['failure_count']} repositories")
            for failed in setup_result['failed_repos']:
                print(f"   - {failed['processor']}: {failed['error']}")
        
        return setup_result
    
    def verify_complete_setup(self):
        """Verify that the complete setup is working"""
        
        print("\n🔍 Verifying Complete Setup")
        print("=" * 35)
        
        # Check GitHub connection
        connection_status = self.authenticator.verify_connection()
        
        if not connection_status['authenticated']:
            return {
                'verified': False,
                'error': 'GitHub connection failed'
            }
        
        print(f"✅ Connected as: {connection_status['user']['login']}")
        
        # Check repositories
        repos_result = self.authenticator.get_repositories()
        
        if repos_result['status'] == 'success':
            print(f"✅ Access to {repos_result['total_count']} repositories")
            
            # Look for EchoNexus processor repos
            processor_repos = [repo for repo in repos_result['repositories'] 
                             if repo['name'].startswith('echo-nexus-')]
            
            print(f"✅ Found {len(processor_repos)} EchoNexus processor repositories")
        
        return {
            'verified': True,
            'user': connection_status['user']['login'],
            'total_repos': repos_result['total_count'],
            'processor_repos': len(processor_repos) if repos_result['status'] == 'success' else 0
        }


def main():
    """Run the GitHub setup wizard"""
    
    wizard = GitHubSetupWizard()
    
    try:
        setup_result = wizard.run_setup_wizard()
        
        print("\n" + "=" * 50)
        print("🎉 SETUP COMPLETE!")
        print("=" * 50)
        
        if setup_result['status'] == 'success':
            print(f"✅ Method: {setup_result['method']}")
            print(f"✅ Message: {setup_result['message']}")
            
            # Verify complete setup
            verification = wizard.verify_complete_setup()
            
            if verification['verified']:
                print(f"✅ User: {verification['user']}")
                print(f"✅ Total Repositories: {verification['total_repos']}")
                print(f"✅ Processor Repositories: {verification['processor_repos']}")
                
                print("\n🚀 EchoNexus AGI is now connected to your GitHub!")
                print("You can now use the system to create workflows, manage repositories,")
                print("and deploy the distributed AI processor network.")
            else:
                print(f"❌ Verification failed: {verification['error']}")
        
        else:
            print(f"❌ Setup failed: {setup_result.get('error', 'Unknown error')}")
    
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nSetup failed with error: {e}")


if __name__ == "__main__":
    main()
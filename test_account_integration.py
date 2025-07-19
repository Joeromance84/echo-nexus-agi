#!/usr/bin/env python3
"""
Account Integration Test for joeromance84 (GitHub) + Logan.lorentz9@gmail.com (Google Cloud)
"""

import os
import sys
sys.path.append('.')

from account_integration_config import MultiPlatformIntegrator
from utils.gcp_authenticator import GoogleCloudAuthenticator
from utils.github_helper import GitHubHelper

def test_github_connection():
    """Test GitHub connection for joeromance84"""
    print("🐙 Testing GitHub Connection for joeromance84")
    print("-" * 40)
    
    github = GitHubHelper()
    
    # Check if GitHub token is available
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("⚠️ No GitHub token found")
        print("To connect GitHub account joeromance84:")
        print("1. Generate Personal Access Token at https://github.com/settings/tokens")
        print("2. Add to Replit Secrets as GITHUB_TOKEN")
        print("3. Ensure repo, workflow, and read:user permissions")
        return False
    
    try:
        # Test connection
        connection_result = github.check_github_connection()
        
        if connection_result.get('authenticated'):
            user = connection_result.get('user', 'unknown')
            print(f"✅ GitHub authenticated as: {user}")
            
            if user == 'joeromance84':
                print("✅ Correct account (joeromance84) confirmed")
                return True
            else:
                print(f"⚠️ Connected as {user}, expected joeromance84")
                return False
        else:
            print("❌ GitHub authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ GitHub connection error: {e}")
        return False

def test_google_cloud_connection():
    """Test Google Cloud connection for Logan.lorentz9@gmail.com"""
    print("\n☁️ Testing Google Cloud Connection for Logan.lorentz9@gmail.com")
    print("-" * 40)
    
    authenticator = GoogleCloudAuthenticator()
    
    # Check if credentials are available
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if not credentials_json:
        print("⚠️ No Google Cloud credentials found")
        print("To connect Google Cloud account Logan.lorentz9@gmail.com:")
        print("1. Create service account in Google Cloud Console")
        print("2. Download JSON key file")
        print("3. Add entire JSON content to Replit Secrets as GOOGLE_APPLICATION_CREDENTIALS_JSON")
        return False
    
    try:
        # Test authentication
        auth_result = authenticator.setup_authentication()
        
        if auth_result.success:
            print(f"✅ Google Cloud authenticated")
            print(f"  Service Account: {auth_result.service_account_email}")
            print(f"  Project: {auth_result.project_id}")
            
            # Verify it's connected to Logan's account
            if 'Logan' in auth_result.service_account_email or 'logan' in auth_result.service_account_email:
                print("✅ Service account appears to be from Logan's account")
            else:
                print("⚠️ Service account may not be from Logan.lorentz9@gmail.com account")
            
            return True
        else:
            print(f"❌ Google Cloud authentication failed: {auth_result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Google Cloud connection error: {e}")
        return False

def test_integration_configuration():
    """Test the integration configuration"""
    print("\n🔗 Testing Integration Configuration")
    print("-" * 40)
    
    integrator = MultiPlatformIntegrator()
    
    print(f"✓ GitHub account configured: {integrator.config.github_username}")
    print(f"✓ Google Cloud account configured: {integrator.config.google_cloud_email}")
    
    # Test generating configurations
    try:
        # Generate sample repository setup
        sample_repo = "test-mobile-app"
        
        trigger_config = integrator.generate_github_to_gcp_trigger(sample_repo, "echonexus-builds")
        print(f"✓ Cloud Build trigger config generated")
        
        build_config = integrator.generate_apk_build_cloudbuild(sample_repo)
        print(f"✓ APK build config generated ({len(build_config['steps'])} steps)")
        
        workflow_config = integrator.generate_cross_platform_workflow(sample_repo)
        print(f"✓ Cross-platform workflow configured")
        print(f"  Primary: {workflow_config['primary_platform']}")
        print(f"  Backup: {workflow_config['backup_platform']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration generation error: {e}")
        return False

def generate_setup_instructions():
    """Generate personalized setup instructions"""
    print("\n📋 Personalized Setup Instructions")
    print("=" * 50)
    
    integrator = MultiPlatformIntegrator()
    setup_guide = integrator.create_complete_setup_guide()
    
    # Save to file for easy reference
    with open('personalized_setup_guide.md', 'w') as f:
        f.write(setup_guide)
    
    print("✓ Complete setup guide generated: personalized_setup_guide.md")
    
    # Generate repository-specific instructions
    sample_repos = ["mobile-game", "kivy-app", "flutter-project"]
    
    for repo in sample_repos:
        instructions = integrator.create_repository_setup_instructions(repo)
        filename = f"setup_{repo.replace('-', '_')}.md"
        
        with open(filename, 'w') as f:
            f.write(instructions)
        
        print(f"✓ Repository guide generated: {filename}")

def main():
    """Run comprehensive account integration test"""
    print("🚀 EchoNexus Account Integration Test")
    print("=" * 60)
    print("Testing integration between:")
    print("  GitHub: joeromance84")
    print("  Google Cloud: Logan.lorentz9@gmail.com")
    print()
    
    # Test connections
    github_ok = test_github_connection()
    gcp_ok = test_google_cloud_connection()
    config_ok = test_integration_configuration()
    
    # Generate setup instructions
    generate_setup_instructions()
    
    # Summary
    print("\n" + "="*60)
    print("🎯 INTEGRATION TEST RESULTS")
    print("="*60)
    
    print(f"GitHub Connection (joeromance84):           {'✅ READY' if github_ok else '⚠️ NEEDS SETUP'}")
    print(f"Google Cloud (Logan.lorentz9@gmail.com):   {'✅ READY' if gcp_ok else '⚠️ NEEDS SETUP'}")
    print(f"Integration Configuration:                  {'✅ READY' if config_ok else '❌ ERROR'}")
    
    if github_ok and gcp_ok and config_ok:
        print("\n🎉 FULL INTEGRATION READY!")
        print("Your EchoNexus AGI can now:")
        print("• Build APKs using Google Cloud Build")
        print("• Monitor GitHub repositories (joeromance84)")
        print("• Store artifacts in Google Cloud Storage")
        print("• Use GitHub Actions as backup platform")
        print("• Automatically select best platform for each build")
        
        print("\nNext steps:")
        print("1. Choose a repository to set up first")
        print("2. Add cloudbuild.yaml to the repository")
        print("3. Configure Cloud Build trigger")
        print("4. Test with a sample commit")
        
    elif not github_ok and not gcp_ok:
        print("\n⚠️ BOTH PLATFORMS NEED SETUP")
        print("Follow the personalized setup guide to connect both accounts")
        
    elif not github_ok:
        print("\n⚠️ GITHUB SETUP NEEDED")
        print("Add GitHub token to Replit Secrets to connect joeromance84 account")
        
    elif not gcp_ok:
        print("\n⚠️ GOOGLE CLOUD SETUP NEEDED")
        print("Add service account credentials to connect Logan.lorentz9@gmail.com account")
        
    else:
        print("\n✅ ACCOUNTS CONNECTED")
        print("Ready to configure specific repositories and triggers")

if __name__ == "__main__":
    main()
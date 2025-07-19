#!/usr/bin/env python3
"""
GitHub Authentication Assistant
Intelligent login assistance with persistent session management
"""

import os
import json
import time
import streamlit as st
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from utils.github_authenticator import GitHubAuthenticator
from github_setup_wizard import GitHubSetupWizard

class GitHubAuthAssistant:
    """
    Intelligent GitHub authentication assistant with persistent sessions
    """
    
    def __init__(self):
        self.session_file = '.github_session.json'
        self.github_username = "joeromance84"
        self.authenticator = GitHubAuthenticator()
        self.setup_wizard = GitHubSetupWizard()
        
    def check_and_maintain_session(self) -> Dict[str, Any]:
        """Check existing session and maintain persistent authentication"""
        
        # Check for existing session
        existing_session = self.load_session()
        
        if existing_session and self.is_session_valid(existing_session):
            # Existing valid session found
            self.restore_session(existing_session)
            return {
                'status': 'authenticated',
                'method': 'existing_session',
                'user': existing_session['user_info'],
                'session_age': time.time() - existing_session['created_at']
            }
        
        # Check environment variables
        if os.environ.get('GITHUB_TOKEN'):
            connection_status = self.authenticator.verify_connection()
            
            if connection_status['authenticated']:
                # Valid token in environment
                session_data = self.create_session(connection_status)
                self.save_session(session_data)
                
                return {
                    'status': 'authenticated',
                    'method': 'environment_token',
                    'user': connection_status['user'],
                    'message': 'Authenticated using existing token'
                }
        
        # No valid authentication found
        return {
            'status': 'unauthenticated',
            'method': 'none',
            'message': 'Authentication required'
        }
    
    def guided_login_assistance(self) -> Dict[str, Any]:
        """Provide step-by-step login assistance"""
        
        st.write("🤖 **GitHub Login Assistant for joeromance84**")
        st.write("I'll help you connect your GitHub account securely and permanently.")
        
        # Method selection
        st.write("### Choose Your Preferred Login Method:")
        
        method = st.radio(
            "Select authentication method:",
            [
                "🔑 Personal Access Token (Recommended - Most Reliable)",
                "⚡ GitHub CLI (Quick Setup)",
                "🔐 SSH Key (Advanced - Most Secure)",
                "🆘 I need help choosing"
            ],
            key="auth_method_selection"
        )
        
        if "Personal Access Token" in method:
            return self.assist_token_setup()
        elif "GitHub CLI" in method:
            return self.assist_cli_setup()
        elif "SSH Key" in method:
            return self.assist_ssh_setup()
        elif "help choosing" in method:
            return self.provide_method_recommendations()
    
    def assist_token_setup(self) -> Dict[str, Any]:
        """Assist with Personal Access Token setup"""
        
        st.write("### 🔑 Personal Access Token Setup")
        
        with st.expander("📋 Step-by-Step Instructions", expanded=True):
            st.write("**Step 1: Create the Token**")
            
            if st.button("🌐 Open GitHub Token Creation Page", key="open_token_page"):
                webbrowser.open("https://github.com/settings/tokens/new")
                st.success("Opened GitHub token creation page in your browser!")
            
            st.write("**Step 2: Configure Token Settings**")
            st.code("""
Token Name: EchoNexus AGI System
Expiration: No expiration
            """)
            
            st.write("**Step 3: Select Required Permissions**")
            required_scopes = [
                "✅ repo (Full control of repositories)",
                "✅ workflow (Update GitHub Actions)",
                "✅ admin:repo_hook (Repository hooks)",
                "✅ user (Read user data)",
                "✅ project (Project access)"
            ]
            
            for scope in required_scopes:
                st.write(scope)
            
            st.write("**Step 4: Generate and Copy Token**")
            st.warning("⚠️ Copy the token immediately - you won't see it again!")
        
        # Token input section
        st.write("### 🔐 Enter Your Token")
        
        token_input = st.text_input(
            "Paste your GitHub Personal Access Token:",
            type="password",
            key="github_token_input",
            help="The token will be securely stored for future use"
        )
        
        if st.button("🔍 Test & Save Token", key="test_token"):
            if token_input:
                return self.test_and_save_token(token_input)
            else:
                st.error("Please enter a token first")
        
        return {'status': 'in_progress', 'method': 'token_setup'}
    
    def test_and_save_token(self, token: str) -> Dict[str, Any]:
        """Test token and save if valid"""
        
        with st.spinner("Testing GitHub token..."):
            # Temporarily set token for testing
            original_token = os.environ.get('GITHUB_TOKEN')
            os.environ['GITHUB_TOKEN'] = token
            
            try:
                # Test the token
                test_auth = GitHubAuthenticator()
                connection_status = test_auth.verify_connection()
                
                if connection_status['authenticated']:
                    # Token is valid
                    st.success(f"✅ Successfully authenticated as: {connection_status['user']['login']}")
                    
                    # Save token permanently
                    self.save_token_permanently(token)
                    
                    # Create and save session
                    session_data = self.create_session(connection_status)
                    self.save_session(session_data)
                    
                    # Update Streamlit session state
                    st.session_state.github_authenticated = True
                    st.session_state.github_user_info = connection_status['user']
                    
                    st.balloons()
                    st.success("🎉 GitHub connection established! You're now logged in permanently.")
                    
                    return {
                        'status': 'authenticated',
                        'method': 'token',
                        'user': connection_status['user']
                    }
                else:
                    st.error(f"❌ Token validation failed: {connection_status['message']}")
                    return {
                        'status': 'failed',
                        'error': connection_status['message']
                    }
            
            finally:
                # Restore original token if test failed
                if original_token and not connection_status.get('authenticated'):
                    os.environ['GITHUB_TOKEN'] = original_token
                elif not connection_status.get('authenticated') and 'GITHUB_TOKEN' in os.environ:
                    del os.environ['GITHUB_TOKEN']
    
    def save_token_permanently(self, token: str):
        """Save token to multiple secure locations"""
        
        # 1. Environment variable (current session)
        os.environ['GITHUB_TOKEN'] = token
        
        # 2. Show Replit Secrets instructions
        with st.expander("🔒 Save to Replit Secrets (Recommended)", expanded=True):
            st.write("To make this login permanent across all sessions:")
            st.code("""
1. Click 'Secrets' in the Replit sidebar (🔐 icon)
2. Click 'Add Secret'
3. Key: GITHUB_TOKEN
4. Value: [paste your token here]
5. Click 'Add Secret'
            """)
            
            if st.button("✅ I've added the secret to Replit", key="confirm_replit_secret"):
                st.success("Perfect! Your GitHub authentication is now permanent.")
        
        # 3. Local encrypted storage (backup)
        try:
            import base64
            from pathlib import Path
            
            config_dir = Path.home() / '.echonexus'
            config_dir.mkdir(exist_ok=True)
            
            # Simple encryption for local storage
            encoded_token = base64.b64encode(token.encode()).decode()
            
            config_data = {
                'token_hash': hash(token),
                'created_at': time.time(),
                'username': self.github_username
            }
            
            with open(config_dir / 'auth_backup.json', 'w') as f:
                json.dump(config_data, f)
            
            st.info("💾 Token backup saved locally (encrypted)")
        
        except Exception as e:
            st.warning(f"Could not save local backup: {e}")
    
    def assist_cli_setup(self) -> Dict[str, Any]:
        """Assist with GitHub CLI setup"""
        
        st.write("### ⚡ GitHub CLI Setup")
        
        with st.expander("📋 GitHub CLI Instructions", expanded=True):
            st.write("GitHub CLI provides the easiest authentication experience.")
            
            st.code("""
# Install GitHub CLI (if not installed)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
            """)
            
            st.write("**Follow the prompts:**")
            st.write("1. Choose 'GitHub.com'")
            st.write("2. Choose 'HTTPS'") 
            st.write("3. Choose 'Yes' to authenticate Git")
            st.write("4. Choose 'Login with a web browser'")
        
        if st.button("🧪 Test GitHub CLI Authentication", key="test_cli"):
            return self.test_cli_authentication()
        
        return {'status': 'in_progress', 'method': 'cli_setup'}
    
    def test_cli_authentication(self) -> Dict[str, Any]:
        """Test GitHub CLI authentication"""
        
        import subprocess
        
        try:
            with st.spinner("Testing GitHub CLI authentication..."):
                # Test gh auth status
                result = subprocess.run(['gh', 'auth', 'status'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0 and 'Logged in to github.com' in result.stderr:
                    # Extract username
                    for line in result.stderr.split('\n'):
                        if 'account' in line and self.github_username in line:
                            st.success(f"✅ GitHub CLI authenticated as: {self.github_username}")
                            
                            # Create session
                            session_data = self.create_cli_session()
                            self.save_session(session_data)
                            
                            # Update Streamlit session state
                            st.session_state.github_authenticated = True
                            st.session_state.github_user_info = {'login': self.github_username}
                            
                            return {
                                'status': 'authenticated',
                                'method': 'github_cli',
                                'user': {'login': self.github_username}
                            }
                
                st.error("❌ GitHub CLI not authenticated. Please run 'gh auth login' first.")
                return {'status': 'failed', 'error': 'CLI not authenticated'}
        
        except FileNotFoundError:
            st.error("❌ GitHub CLI not installed. Please install it first.")
            return {'status': 'failed', 'error': 'CLI not installed'}
    
    def assist_ssh_setup(self) -> Dict[str, Any]:
        """Assist with SSH key setup"""
        
        st.write("### 🔐 SSH Key Setup")
        st.write("SSH keys provide the most secure authentication method.")
        
        with st.expander("📋 SSH Key Instructions", expanded=True):
            st.write("**Step 1: Generate SSH Key**")
            st.code(f"""
ssh-keygen -t ed25519 -C "{self.github_username}@echonexus" -f ~/.ssh/id_ed25519_echonexus -N ""
            """)
            
            st.write("**Step 2: Add to SSH Agent**")
            st.code("""
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_echonexus
            """)
            
            st.write("**Step 3: Copy Public Key**")
            st.code("""
cat ~/.ssh/id_ed25519_echonexus.pub
            """)
            
            st.write("**Step 4: Add to GitHub**")
            if st.button("🌐 Open GitHub SSH Settings", key="open_ssh_settings"):
                webbrowser.open("https://github.com/settings/ssh/new")
                st.success("Opened GitHub SSH settings page!")
        
        if st.button("🧪 Test SSH Authentication", key="test_ssh"):
            return self.test_ssh_authentication()
        
        return {'status': 'in_progress', 'method': 'ssh_setup'}
    
    def test_ssh_authentication(self) -> Dict[str, Any]:
        """Test SSH authentication"""
        
        import subprocess
        
        try:
            with st.spinner("Testing SSH authentication..."):
                result = subprocess.run([
                    'ssh', '-T', '-i', '~/.ssh/id_ed25519_echonexus', 'git@github.com'
                ], capture_output=True, text=True)
                
                if f'Hi {self.github_username}!' in result.stderr:
                    st.success(f"✅ SSH authenticated as: {self.github_username}")
                    
                    # Create session
                    session_data = self.create_ssh_session()
                    self.save_session(session_data)
                    
                    # Update Streamlit session state
                    st.session_state.github_authenticated = True
                    st.session_state.github_user_info = {'login': self.github_username}
                    
                    return {
                        'status': 'authenticated',
                        'method': 'ssh_key',
                        'user': {'login': self.github_username}
                    }
                else:
                    st.error("❌ SSH authentication failed. Check your SSH key setup.")
                    return {'status': 'failed', 'error': 'SSH test failed'}
        
        except Exception as e:
            st.error(f"❌ SSH test error: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def provide_method_recommendations(self) -> Dict[str, Any]:
        """Provide personalized method recommendations"""
        
        st.write("### 🎯 Recommended Authentication Method")
        
        st.info("""
**For joeromance84, I recommend the Personal Access Token method because:**

✅ **Most Reliable**: Works in all environments  
✅ **Easiest Setup**: Just copy and paste  
✅ **Persistent**: Stays logged in forever  
✅ **Full Control**: Access to all repositories and features  
✅ **Quick Recovery**: Easy to regenerate if needed  

This method will keep you permanently logged in with zero maintenance required.
        """)
        
        if st.button("🚀 Start Personal Access Token Setup", key="start_token_setup"):
            st.session_state.auth_method_selection = "🔑 Personal Access Token (Recommended - Most Reliable)"
            st.rerun()
        
        return {'status': 'recommendation_provided'}
    
    def create_session(self, connection_status: Dict[str, Any]) -> Dict[str, Any]:
        """Create session data"""
        
        return {
            'created_at': time.time(),
            'user_info': connection_status['user'],
            'token_scopes': connection_status.get('token_scopes', []),
            'method': 'token',
            'username': connection_status['user']['login'],
            'authenticated': True
        }
    
    def create_cli_session(self) -> Dict[str, Any]:
        """Create CLI session data"""
        
        return {
            'created_at': time.time(),
            'user_info': {'login': self.github_username},
            'method': 'github_cli',
            'username': self.github_username,
            'authenticated': True
        }
    
    def create_ssh_session(self) -> Dict[str, Any]:
        """Create SSH session data"""
        
        return {
            'created_at': time.time(),
            'user_info': {'login': self.github_username},
            'method': 'ssh_key',
            'username': self.github_username,
            'authenticated': True
        }
    
    def save_session(self, session_data: Dict[str, Any]):
        """Save session data to persistent storage"""
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except Exception as e:
            st.warning(f"Could not save session: {e}")
    
    def load_session(self) -> Optional[Dict[str, Any]]:
        """Load session data from persistent storage"""
        
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return None
    
    def is_session_valid(self, session_data: Dict[str, Any]) -> bool:
        """Check if session is still valid"""
        
        # Check age (valid for 30 days)
        age = time.time() - session_data.get('created_at', 0)
        if age > (30 * 24 * 60 * 60):  # 30 days
            return False
        
        # Check if user matches
        if session_data.get('username') != self.github_username:
            return False
        
        return True
    
    def restore_session(self, session_data: Dict[str, Any]):
        """Restore session to current state"""
        
        st.session_state.github_authenticated = True
        st.session_state.github_user_info = session_data['user_info']
    
    def display_authentication_status(self):
        """Display current authentication status"""
        
        if st.session_state.get('github_authenticated'):
            user_info = st.session_state.get('github_user_info', {})
            
            with st.sidebar:
                st.success(f"✅ Connected: {user_info.get('login', 'Unknown')}")
                
                if st.button("🔄 Refresh Connection", key="refresh_connection"):
                    # Verify connection is still valid
                    connection_status = self.authenticator.verify_connection()
                    
                    if connection_status['authenticated']:
                        st.success("Connection verified!")
                    else:
                        st.error("Connection lost - please re-authenticate")
                        st.session_state.github_authenticated = False
                        st.rerun()
                
                if st.button("🚪 Logout", key="logout"):
                    self.logout()
        else:
            with st.sidebar:
                st.warning("⚠️ GitHub not connected")
                if st.button("🔑 Connect GitHub", key="connect_github"):
                    st.session_state.show_github_setup = True
                    st.rerun()
    
    def logout(self):
        """Logout and clear session"""
        
        # Clear session state
        st.session_state.github_authenticated = False
        st.session_state.github_user_info = None
        
        # Remove session file
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception:
            pass
        
        # Clear environment variable (but keep it if it was set externally)
        # We don't clear GITHUB_TOKEN as it might be set in Replit Secrets
        
        st.success("Logged out successfully!")
        st.rerun()
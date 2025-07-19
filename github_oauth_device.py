#!/usr/bin/env python3
"""
GitHub OAuth Device Flow Authentication
User-friendly authentication using device codes that work with GitHub mobile app
"""

import os
import json
import time
import requests
import streamlit as st
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class GitHubDeviceAuth:
    """
    GitHub OAuth Device Flow authentication for easy mobile/desktop login
    """
    
    def __init__(self):
        self.client_id = "Ov23liXP1ZZZ9F2Y3mJ8"  # Public OAuth App ID for EchoNexus
        self.device_code_url = "https://github.com/login/device/code"
        self.access_token_url = "https://github.com/login/oauth/access_token"
        self.verify_url = "https://github.com/login/device"
        self.session_file = '.github_oauth_session.json'
        
    def start_device_flow(self) -> Dict[str, Any]:
        """Start OAuth device flow and get device code"""
        
        try:
            # Request device code
            response = requests.post(
                self.device_code_url,
                data={
                    'client_id': self.client_id,
                    'scope': 'repo workflow user admin:repo_hook project admin:org'
                },
                headers={'Accept': 'application/json'}
            )
            
            if response.status_code == 200:
                device_data = response.json()
                
                return {
                    'status': 'success',
                    'device_code': device_data['device_code'],
                    'user_code': device_data['user_code'],
                    'verification_uri': device_data['verification_uri'],
                    'verification_uri_complete': device_data.get('verification_uri_complete'),
                    'expires_in': device_data['expires_in'],
                    'interval': device_data['interval']
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Failed to start device flow: {response.text}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Device flow error: {str(e)}'
            }
    
    def display_device_flow_ui(self, device_data: Dict[str, Any]):
        """Display device flow UI in Streamlit"""
        
        st.success("🎉 Device authentication started!")
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📱 Step 1: Open GitHub on your device")
            
            # Show verification URL
            st.code(device_data['verification_uri'], language="text")
            
            # Show user code prominently
            st.subheader("🔢 Step 2: Enter this code:")
            st.markdown(f"## `{device_data['user_code']}`")
            
            # Instructions
            st.info("""
            **How to authenticate:**
            1. Open the GitHub app on your phone or visit github.com/login/device
            2. Enter the code shown above
            3. Approve the EchoNexus application
            4. Wait for automatic connection below
            """)
            
            # Quick link button
            verification_uri_complete = device_data.get('verification_uri_complete')
            if verification_uri_complete:
                st.markdown(f"**Quick Link:** [Open GitHub with code]({verification_uri_complete})")
        
        with col2:
            # Generate QR code for easy mobile scanning
            if device_data.get('verification_uri_complete'):
                st.subheader("📲 QR Code")
                qr_img = self.generate_qr_code(device_data['verification_uri_complete'])
                st.image(qr_img, caption="Scan with your phone", width=200)
            
            # Show expiration timer
            expires_in = device_data['expires_in']
            st.subheader("⏰ Time Remaining")
            st.info(f"{expires_in // 60} minutes {expires_in % 60} seconds")
    
    def generate_qr_code(self, url: str) -> io.BytesIO:
        """Generate QR code for the verification URL"""
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to BytesIO for Streamlit
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return img_buffer
    
    def poll_for_token(self, device_code: str, interval: int = 5) -> Dict[str, Any]:
        """Poll GitHub for access token"""
        
        try:
            response = requests.post(
                self.access_token_url,
                data={
                    'client_id': self.client_id,
                    'device_code': device_code,
                    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
                },
                headers={'Accept': 'application/json'}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                
                if 'access_token' in token_data:
                    return {
                        'status': 'success',
                        'access_token': token_data['access_token'],
                        'token_type': token_data.get('token_type', 'bearer'),
                        'scope': token_data.get('scope', '')
                    }
                elif 'error' in token_data:
                    error = token_data['error']
                    
                    if error == 'authorization_pending':
                        return {'status': 'pending'}
                    elif error == 'slow_down':
                        return {'status': 'slow_down'}
                    elif error == 'expired_token':
                        return {'status': 'expired'}
                    elif error == 'access_denied':
                        return {'status': 'denied'}
                    else:
                        return {'status': 'error', 'message': token_data.get('error_description', error)}
            
            return {
                'status': 'error',
                'message': f'Token request failed: {response.text}'
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Token polling error: {str(e)}'
            }
    
    def verify_token(self, access_token: str) -> Dict[str, Any]:
        """Verify the access token by getting user info"""
        
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get('https://api.github.com/user', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                
                return {
                    'status': 'success',
                    'authenticated': True,
                    'user': {
                        'login': user_data['login'],
                        'name': user_data.get('name'),
                        'email': user_data.get('email'),
                        'public_repos': user_data.get('public_repos', 0),
                        'private_repos': user_data.get('total_private_repos', 0)
                    }
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Token verification failed: {response.text}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Token verification error: {str(e)}'
            }
    
    def save_oauth_session(self, access_token: str, user_data: Dict[str, Any]):
        """Save OAuth session data"""
        
        session_data = {
            'access_token': access_token,
            'user_data': user_data,
            'created_at': datetime.now().isoformat(),
            'method': 'oauth_device_flow'
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Also set as environment variable for immediate use
            os.environ['GITHUB_TOKEN'] = access_token
            
            return True
        except Exception as e:
            st.error(f"Could not save session: {e}")
            return False
    
    def load_oauth_session(self) -> Optional[Dict[str, Any]]:
        """Load saved OAuth session"""
        
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Check if session is recent (within 30 days)
                created_at = datetime.fromisoformat(session_data['created_at'])
                if (datetime.now() - created_at).days < 30:
                    return session_data
            
            return None
        except Exception:
            return None
    
    def streamlit_device_auth_flow(self) -> Dict[str, Any]:
        """Complete device authentication flow in Streamlit"""
        
        # Check for existing session
        existing_session = self.load_oauth_session()
        if existing_session:
            # Verify token is still valid
            token_verification = self.verify_token(existing_session['access_token'])
            
            if token_verification['status'] == 'success':
                os.environ['GITHUB_TOKEN'] = existing_session['access_token']
                return {
                    'status': 'authenticated',
                    'method': 'existing_oauth_session',
                    'user': token_verification['user']
                }
        
        # Start new device flow
        st.write("### 📱 GitHub Device Authentication")
        st.write("Authenticate easily using your GitHub mobile app or any browser!")
        
        if st.button("🚀 Start Device Authentication", key=f"start_device_auth_{int(time.time())}"):
            # Start device flow
            device_result = self.start_device_flow()
            
            if device_result['status'] == 'success':
                # Store device data in session state
                st.session_state.device_auth_data = device_result
                st.session_state.device_auth_started = True
                st.rerun()
        
        # Handle ongoing device flow
        if st.session_state.get('device_auth_started') and st.session_state.get('device_auth_data'):
            device_data = st.session_state.device_auth_data
            
            # Display UI
            self.display_device_flow_ui(device_data)
            
            # Auto-refresh section
            st.subheader("🔄 Waiting for authentication...")
            
            # Create placeholder for status updates
            status_placeholder = st.empty()
            progress_placeholder = st.empty()
            
            # Polling loop
            max_attempts = device_data['expires_in'] // device_data['interval']
            
            for attempt in range(max_attempts):
                with status_placeholder.container():
                    st.info(f"⏳ Checking authentication... (attempt {attempt + 1}/{max_attempts})")
                
                with progress_placeholder.container():
                    progress_percent = (attempt + 1) / max_attempts
                    st.progress(progress_percent)
                
                # Poll for token
                token_result = self.poll_for_token(
                    device_data['device_code'], 
                    device_data['interval']
                )
                
                if token_result['status'] == 'success':
                    # Verify token
                    verification = self.verify_token(token_result['access_token'])
                    
                    if verification['status'] == 'success':
                        # Save session
                        self.save_oauth_session(token_result['access_token'], verification['user'])
                        
                        with status_placeholder.container():
                            st.success("🎉 Authentication successful!")
                        
                        with progress_placeholder.container():
                            st.progress(1.0)
                        
                        # Clear device auth state
                        st.session_state.device_auth_started = False
                        st.session_state.device_auth_data = None
                        
                        return {
                            'status': 'authenticated',
                            'method': 'oauth_device_flow',
                            'user': verification['user']
                        }
                
                elif token_result['status'] == 'denied':
                    with status_placeholder.container():
                        st.error("❌ Authentication was denied. Please try again.")
                    st.session_state.device_auth_started = False
                    return {'status': 'denied'}
                
                elif token_result['status'] == 'expired':
                    with status_placeholder.container():
                        st.error("⏰ Authentication code expired. Please start over.")
                    st.session_state.device_auth_started = False
                    return {'status': 'expired'}
                
                elif token_result['status'] == 'error':
                    with status_placeholder.container():
                        st.error(f"❌ Error: {token_result['message']}")
                    st.session_state.device_auth_started = False
                    return {'status': 'error', 'message': token_result['message']}
                
                # Wait before next poll (with some UI updates)
                time.sleep(device_data['interval'])
            
            # Timeout
            with status_placeholder.container():
                st.error("⏰ Authentication timed out. Please try again.")
            st.session_state.device_auth_started = False
            return {'status': 'timeout'}
        
        return {'status': 'waiting_for_start'}


def main():
    """Test the device authentication flow"""
    
    print("🔐 GitHub OAuth Device Flow Test")
    print("=" * 40)
    
    device_auth = GitHubDeviceAuth()
    
    # Start device flow
    print("Starting device authentication flow...")
    device_result = device_auth.start_device_flow()
    
    if device_result['status'] == 'success':
        print(f"✅ Device flow started successfully!")
        print(f"📱 Go to: {device_result['verification_uri']}")
        print(f"🔢 Enter code: {device_result['user_code']}")
        print(f"⏰ Expires in: {device_result['expires_in']} seconds")
        
        # Poll for token
        print("\n⏳ Waiting for authorization...")
        
        max_attempts = device_result['expires_in'] // device_result['interval']
        
        for attempt in range(max_attempts):
            print(f"   Checking... (attempt {attempt + 1}/{max_attempts})")
            
            token_result = device_auth.poll_for_token(
                device_result['device_code'],
                device_result['interval']
            )
            
            if token_result['status'] == 'success':
                print("✅ Token received!")
                
                # Verify token
                verification = device_auth.verify_token(token_result['access_token'])
                
                if verification['status'] == 'success':
                    user = verification['user']
                    print(f"✅ Authenticated as: {user['login']}")
                    print(f"   Name: {user.get('name', 'Not specified')}")
                    print(f"   Public repos: {user['public_repos']}")
                    
                    # Save session
                    device_auth.save_oauth_session(token_result['access_token'], user)
                    print("✅ Session saved!")
                    
                    return True
                else:
                    print(f"❌ Token verification failed: {verification['message']}")
                    return False
            
            elif token_result['status'] in ['denied', 'expired', 'error']:
                print(f"❌ Authentication failed: {token_result['status']}")
                if 'message' in token_result:
                    print(f"   {token_result['message']}")
                return False
            
            # Wait before next poll
            time.sleep(device_result['interval'])
        
        print("⏰ Authentication timed out")
        return False
    
    else:
        print(f"❌ Failed to start device flow: {device_result['message']}")
        return False


if __name__ == "__main__":
    main()
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
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configure surgical logging for device auth debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DEVICE_AUTH - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('device_auth_debug.log'),
        logging.StreamHandler()
    ]
)

class GitHubDeviceAuth:
    """
    GitHub OAuth Device Flow authentication for easy mobile/desktop login
    """
    
    def __init__(self):
        # GitHub CLI's public client ID - well-tested and reliable
        self.client_id = "178c6fc778ccc68e1d6a"
        self.device_code_url = "https://github.com/login/device/code"
        self.access_token_url = "https://github.com/login/oauth/access_token"
        self.verify_url = "https://github.com/login/device"
        self.session_file = '.github_oauth_session.json'
        
    def start_device_flow(self) -> Dict[str, Any]:
        """Start OAuth device flow and get device code"""
        
        logging.info(f"🚀 STEP 1: Initial POST to /device/code initiated with client_id: {self.client_id}")
        
        try:
            # Request device code
            logging.info(f"📡 Making request to: {self.device_code_url}")
            response = requests.post(
                self.device_code_url,
                data={
                    'client_id': self.client_id,
                    'scope': 'repo workflow user admin:repo_hook project admin:org'
                },
                headers={'Accept': 'application/json'}
            )
            
            logging.info(f"📊 Response status code: {response.status_code}")
            logging.info(f"📋 Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                device_data = response.json()
                
                logging.info(f"✅ STEP 1 SUCCESS: Received device code, user code, and verification URI")
                logging.info(f"📱 User code is: {device_data['user_code']}")
                logging.info(f"🔗 Verification URI: {device_data['verification_uri']}")
                logging.info(f"⏰ Expires in: {device_data['expires_in']} seconds")
                logging.info(f"🔄 Polling interval: {device_data['interval']} seconds")
                
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
                error_msg = f'Failed to start device flow: {response.status_code} - {response.text}'
                logging.error(f"❌ STEP 1 FAILED: {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
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
        """Poll GitHub for access token with surgical logging"""
        
        # Create a unique poll ID for tracking
        poll_id = int(time.time() * 1000) % 10000
        logging.info(f"🔄 POLL #{poll_id}: Starting token poll attempt")
        logging.info(f"📡 POLL #{poll_id}: Making request to {self.access_token_url}")
        logging.info(f"🆔 POLL #{poll_id}: Using device_code: {device_code[:10]}...{device_code[-10:]}")
        
        try:
            response = requests.post(
                self.access_token_url,
                data={
                    'client_id': self.client_id,
                    'device_code': device_code,
                    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
                },
                headers={'Accept': 'application/json'},
                timeout=30  # Add timeout to prevent hanging
            )
            
            logging.info(f"📊 POLL #{poll_id}: Response status code: {response.status_code}")
            logging.info(f"⏱️ POLL #{poll_id}: Response time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                token_data = response.json()
                logging.info(f"📋 POLL #{poll_id}: Response data keys: {list(token_data.keys())}")
                
                if 'access_token' in token_data:
                    logging.info(f"✅ POLL #{poll_id}: SUCCESS! Received access token")
                    logging.info(f"🔑 POLL #{poll_id}: Token type: {token_data.get('token_type', 'bearer')}")
                    logging.info(f"🎯 POLL #{poll_id}: Scope: {token_data.get('scope', 'none')}")
                    return {
                        'status': 'success',
                        'access_token': token_data['access_token'],
                        'token_type': token_data.get('token_type', 'bearer'),
                        'scope': token_data.get('scope', '')
                    }
                elif 'error' in token_data:
                    error = token_data['error']
                    error_desc = token_data.get('error_description', 'No description')
                    logging.info(f"⚠️ POLL #{poll_id}: GitHub returned error: {error}")
                    logging.info(f"📝 POLL #{poll_id}: Error description: {error_desc}")
                    
                    if error == 'authorization_pending':
                        logging.info(f"⏳ POLL #{poll_id}: Authorization still pending - user hasn't completed auth yet")
                        return {'status': 'authorization_pending'}
                    elif error == 'slow_down':
                        logging.warning(f"🐌 POLL #{poll_id}: Rate limited - need to slow down polling")
                        return {'status': 'slow_down'}
                    elif error == 'expired_token':
                        logging.error(f"⏰ POLL #{poll_id}: Device code expired")
                        return {'status': 'expired'}
                    elif error == 'access_denied':
                        logging.error(f"🚫 POLL #{poll_id}: User denied authorization")
                        return {'status': 'denied'}
                    else:
                        logging.error(f"❌ POLL #{poll_id}: Unknown error: {error}")
                        return {'status': 'error', 'message': f"{error}: {error_desc}"}
                else:
                    logging.warning(f"🤔 POLL #{poll_id}: Unexpected response structure")
                    return {'status': 'authorization_pending'}  # Default assumption
            else:
                error_msg = f'Token request failed: {response.status_code} - {response.text}'
                logging.error(f"💥 POLL #{poll_id}: HTTP error: {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
        
        except Exception as e:
            error_msg = f'Token polling error: {str(e)}'
            logging.error(f"💥 POLL #{poll_id}: Exception: {error_msg}")
            return {
                'status': 'error',
                'message': error_msg
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
        
        # Initialize device auth state
        if 'device_auth_started' not in st.session_state:
            st.session_state.device_auth_started = False
        if 'device_auth_data' not in st.session_state:
            st.session_state.device_auth_data = None
        
        # Start new device flow
        st.write("### 📱 GitHub Device Authentication")
        st.write("Authenticate easily using your GitHub mobile app or any browser!")
        
        # Debug information
        with st.expander("🔧 Debug Info", expanded=False):
            st.write(f"Client ID: {self.client_id}")
            st.write(f"Device auth started: {st.session_state.device_auth_started}")
            st.write(f"Device data available: {st.session_state.device_auth_data is not None}")
        
        if not st.session_state.device_auth_started:
            button_key = f"start_device_auth_btn_{id(self)}_{int(time.time())}"
            if st.button("🚀 Start Device Authentication", key=button_key):
                with st.spinner("Starting device authentication flow..."):
                    # Start device flow
                    device_result = self.start_device_flow()
                    
                    st.write("Device flow result:", device_result)  # Debug
                    
                    if device_result['status'] == 'success':
                        # Store device data in session state
                        st.session_state.device_auth_data = device_result
                        st.session_state.device_auth_started = True
                        st.success("Device flow started! Please check the instructions below.")
                        st.rerun()
                    else:
                        st.error(f"Failed to start device flow: {device_result.get('message', 'Unknown error')}")
                        return device_result
        
        # Handle ongoing device flow
        if st.session_state.device_auth_started and st.session_state.device_auth_data:
            device_data = st.session_state.device_auth_data
            
            # Display UI
            self.display_device_flow_ui(device_data)
            
            # Manual check button instead of automatic polling
            st.subheader("🔄 Check Authentication Status")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Check Now", key="check_auth_btn"):
                    with st.spinner("Checking authentication..."):
                        token_result = self.poll_for_token(device_data['device_code'])
                        
                        if token_result['status'] == 'success':
                            # Verify token
                            verification = self.verify_token(token_result['access_token'])
                            
                            if verification['status'] == 'success':
                                # Save session
                                self.save_oauth_session(token_result['access_token'], verification['user'])
                                
                                st.success("🎉 Authentication successful!")
                                st.balloons()
                                
                                # Clear device auth state
                                st.session_state.device_auth_started = False
                                st.session_state.device_auth_data = None
                                
                                return {
                                    'status': 'authenticated',
                                    'method': 'oauth_device_flow',
                                    'user': verification['user']
                                }
                            else:
                                st.error(f"Token verification failed: {verification.get('message', 'Unknown error')}")
                        
                        elif token_result['status'] == 'authorization_pending':
                            st.info("⏳ Still waiting for authorization. Please complete the authentication in your GitHub app.")
                        
                        elif token_result['status'] == 'denied':
                            st.error("❌ Authentication was denied. Please try again.")
                            st.session_state.device_auth_started = False
                            return {'status': 'denied'}
                        
                        elif token_result['status'] == 'expired':
                            st.error("⏰ Authentication code expired. Please start over.")
                            st.session_state.device_auth_started = False
                            return {'status': 'expired'}
                        
                        elif token_result['status'] == 'error':
                            st.error(f"❌ Error: {token_result.get('message', 'Unknown error')}")
                            st.session_state.device_auth_started = False
                            return {'status': 'error', 'message': token_result.get('message')}
            
            with col2:
                if st.button("🔄 Start Over", key="restart_auth_btn"):
                    st.session_state.device_auth_started = False
                    st.session_state.device_auth_data = None
                    st.rerun()
            
            # Auto-refresh option
            if st.checkbox("🔄 Auto-refresh every 5 seconds", key="auto_refresh_checkbox"):
                time.sleep(5)
                st.rerun()
        
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
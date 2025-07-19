#!/usr/bin/env python3
"""
Test script for GitHub Device Authentication
Tests the complete OAuth device flow
"""

import sys
import time
from github_oauth_device import GitHubDeviceAuth

def test_device_authentication():
    """Test the complete device authentication flow"""
    
    print("🧪 Testing GitHub Device Authentication")
    print("=" * 50)
    
    # Initialize device auth
    device_auth = GitHubDeviceAuth()
    
    # Test 1: Start device flow
    print("\n📱 Step 1: Starting device flow...")
    device_result = device_auth.start_device_flow()
    
    if device_result['status'] != 'success':
        print(f"❌ Failed to start device flow: {device_result.get('message')}")
        return False
    
    print("✅ Device flow started successfully!")
    print(f"   Visit: {device_result['verification_uri']}")
    print(f"   Enter code: {device_result['user_code']}")
    print(f"   Expires in: {device_result['expires_in']} seconds")
    
    # Test 2: Generate QR code
    print("\n🔲 Step 2: Generating QR code...")
    try:
        qr_code = device_auth.generate_qr_code(device_result['verification_uri'])
        if qr_code:
            print("✅ QR code generated successfully")
        else:
            print("⚠️ QR code generation failed")
    except Exception as e:
        print(f"⚠️ QR code generation error: {e}")
    
    # Test 3: Check token polling (without authentication)
    print("\n🔄 Step 3: Testing token polling...")
    poll_result = device_auth.poll_for_token(device_result['device_code'])
    
    if poll_result['status'] == 'authorization_pending':
        print("✅ Polling works correctly - waiting for user authorization")
    elif poll_result['status'] == 'slow_down':
        print("✅ Rate limiting works correctly")
    else:
        print(f"⚠️ Unexpected poll result: {poll_result}")
    
    # Test 4: Session management
    print("\n💾 Step 4: Testing session management...")
    test_token = "test_token_12345"
    test_user = {"login": "testuser", "id": 123}
    
    # Save test session
    device_auth.save_oauth_session(test_token, test_user)
    print("✅ Session saved")
    
    # Load test session
    loaded_session = device_auth.load_oauth_session()
    if loaded_session and loaded_session['access_token'] == test_token:
        print("✅ Session loaded correctly")
    else:
        print("❌ Session loading failed")
    
    # Clean up test session
    import os
    if os.path.exists(device_auth.session_file):
        os.remove(device_auth.session_file)
        print("✅ Test session cleaned up")
    
    print("\n🎉 Device authentication test complete!")
    print("\nTo complete the authentication:")
    print(f"1. Open: {device_result['verification_uri']}")
    print(f"2. Enter code: {device_result['user_code']}")
    print("3. Use the Streamlit app to check authentication status")
    
    return True

if __name__ == "__main__":
    success = test_device_authentication()
    sys.exit(0 if success else 1)
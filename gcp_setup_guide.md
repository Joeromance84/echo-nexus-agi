# EchoNexus Multi-Platform Setup Guide

## Account Configuration
- **GitHub Account**: joeromance84
- **Google Cloud Account**: Logan.lorentz9@gmail.com

## Overview
This guide configures secure integration between GitHub (joeromance84) and Google Cloud Build (Logan.lorentz9@gmail.com) for the EchoNexus AGI system.

## Phase 1: Google Cloud Project Setup

### 1.1 Create or Select Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with **Logan.lorentz9@gmail.com**
3. Create a new project or select existing:
   - **Recommended project name**: `echonexus-builds`
   - **Project ID**: `echonexus-builds-[random]` (Google will suggest)

### 1.2 Enable Required APIs
Navigate to **APIs & Services > Library** and enable:
- ✅ Cloud Build API
- ✅ Cloud Storage API
- ✅ Container Registry API
- ✅ IAM Service Account Credentials API

## Phase 2: Service Account Creation (Security Best Practice)

### 2.1 Create Service Account
1. Navigate to **IAM & Admin > Service Accounts**
2. Click **Create Service Account**
3. Configure:
   - **Name**: `replit-echonexus-builder`
   - **Description**: `Service account for EchoNexus AGI automated builds`
   - **Service account ID**: `replit-echonexus-builder`

### 2.2 Assign Minimal Permissions (Least Privilege)
Grant only these specific roles:
- ✅ **Cloud Build Editor** - Allows creating and managing builds
- ✅ **Storage Object Admin** - Allows managing build artifacts
- ✅ **Service Account User** - Allows using the service account

**DO NOT** assign:
- ❌ Project Owner
- ❌ Project Editor
- ❌ Compute Admin

### 2.3 Generate Service Account Key
1. Click on your new service account
2. Go to **Keys** tab
3. Click **Add Key > Create new key**
4. Select **JSON** format
5. Download the JSON file
6. **IMPORTANT**: Keep this file secure - it contains your credentials

## Phase 3: Replit Integration

### 3.1 Store Credentials Securely
1. In your Replit project, click the **🔒 Secrets** icon
2. Add new secret:
   - **Key**: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value**: Paste the ENTIRE contents of the downloaded JSON file

### 3.2 Project Configuration
Add this to your project environment:
- **Key**: `GCP_PROJECT_ID`
- **Value**: Your project ID (e.g., `echonexus-builds-123456`)

## Phase 4: Verification and Testing

### 4.1 Test Authentication
Run the authentication test to verify everything is working:

```python
from utils.gcp_authenticator import GoogleCloudAuthenticator

authenticator = GoogleCloudAuthenticator()
auth_result = authenticator.setup_authentication()

if auth_result.success:
    print(f"✅ Authentication successful!")
    print(f"Service Account: {auth_result.service_account_email}")
    print(f"Project: {auth_result.project_id}")
else:
    print(f"❌ Authentication failed: {auth_result.error_message}")
```

### 4.2 Cloud Storage Setup
Create a storage bucket for build artifacts:
1. Go to **Cloud Storage > Browser**
2. Click **Create Bucket**
3. Configure:
   - **Name**: `echonexus-apk-builds` (or your project-id + `-apk-builds`)
   - **Location**: Choose closest region
   - **Storage class**: Standard
   - **Access control**: Uniform

## Phase 5: First Build Test

### 5.1 Simple Test Build
Create a test `cloudbuild.yaml`:

```yaml
steps:
- name: 'gcr.io/cloud-builders/gcloud'
  entrypoint: 'bash'
  args: ['-c', 'echo "EchoNexus AGI - Authentication successful!"']
timeout: '60s'
```

### 5.2 Submit Test Build
```bash
gcloud builds submit --config=cloudbuild.yaml --no-source
```

## Security Checklist

- ✅ Service account has minimal required permissions
- ✅ JSON credentials stored in Replit Secrets (not in code)
- ✅ Project ID configured as environment variable
- ✅ Authentication verification completed
- ✅ Test build submitted successfully

## Troubleshooting

### Common Issues

**Error: "Permission denied"**
- Verify service account has Cloud Build Editor role
- Check that APIs are enabled
- Ensure project ID is correct

**Error: "Authentication failed"**
- Verify JSON credentials are complete and valid
- Check that secret key name is exactly `GOOGLE_APPLICATION_CREDENTIALS_JSON`
- Ensure no extra spaces or characters in the JSON

**Error: "Project not found"**
- Verify project ID is correct
- Ensure you have access to the project
- Check that billing is enabled on the project

### Support
If you encounter issues:
1. Check the authentication logs in Replit
2. Verify all steps in this guide
3. Test with a simple gcloud command first

## Next Steps

Once authentication is working:
1. ✅ Configure GitHub repository triggers
2. ✅ Set up APK build pipelines
3. ✅ Enable build monitoring and notifications
4. ✅ Configure artifact storage and distribution

Your EchoNexus AGI will then have full Google Cloud Build capabilities with secure, automated authentication.
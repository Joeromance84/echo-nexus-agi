
# Complete EchoNexus Multi-Platform Setup

## Account Integration
- **GitHub**: joeromance84
- **Google Cloud**: Logan.lorentz9@gmail.com

## Phase 1: Google Cloud Project Setup

1. **Sign in to Google Cloud Console** with Logan.lorentz9@gmail.com
2. **Create Project**: echonexus-builds-[suffix]
3. **Enable APIs**:
   - Cloud Build API
   - Cloud Storage API
   - Container Registry API
   - IAM Service Account Credentials API

## Phase 2: Service Account Configuration

1. **Create Service Account**:
   - Name: `echonexus-github-builder`
   - Roles: Cloud Build Editor, Storage Object Admin

2. **Generate JSON Key**:
   - Download service account JSON key
   - Store in Replit Secrets as `GOOGLE_APPLICATION_CREDENTIALS_JSON`

## Phase 3: GitHub Repository Integration

For each repository owned by joeromance84:

1. **Add cloudbuild.yaml** to repository root
2. **Configure Cloud Build trigger** to watch repository
3. **Set up backup GitHub Actions workflow**
4. **Test integration** with sample push

## Phase 4: Storage and Artifacts

1. **Create Storage Bucket**: echonexus-builds
2. **Configure IAM** for service account access
3. **Set up artifact organization** structure
4. **Enable build notifications**

## Phase 5: Testing and Verification

```bash
# Test authentication
python -c "from utils.gcp_authenticator import GoogleCloudAuthenticator; print(GoogleCloudAuthenticator().setup_authentication())"

# Test GitHub connection
python -c "from utils.github_helper import GitHubHelper; print(GitHubHelper().check_github_connection())"

# Submit test build
gcloud builds submit --config=cloudbuild.yaml --substitutions=_REPO_NAME=test-repo
```

## Security Checklist

- ✅ Service account has minimal required permissions
- ✅ JSON credentials stored securely in Replit Secrets
- ✅ GitHub token has appropriate repository access
- ✅ Build triggers configured with branch restrictions
- ✅ Storage bucket access properly configured
- ✅ Backup build system (GitHub Actions) configured

## Repository-Specific Setup

To set up a specific repository, run:
```python
integrator = MultiPlatformIntegrator()
instructions = integrator.create_repository_setup_instructions("your-repo-name")
print(instructions)
```

## Monitoring and Maintenance

- **Build Status**: Monitor via Google Cloud Console
- **Cost Tracking**: Set up billing alerts for build usage
- **Performance**: Track build times and success rates
- **Security**: Regular audit of permissions and access

Your EchoNexus AGI will now have seamless integration between GitHub (joeromance84) and Google Cloud Build (Logan.lorentz9@gmail.com) with intelligent platform selection and automatic failover capabilities.

# Echo Nexus AGI - Complete Deployment Setup Instructions

## Actionable Proven Plan Implementation

This document provides step-by-step instructions to implement the complete Echo Nexus AGI growth pipeline: **Replit → GitHub → Google Cloud Build → Deployment**.

## Phase 1: Environment Preparation

### 1.1 Replit Environment Setup

**In your Replit workspace:**

1. **Install Required Packages**
   ```bash
   pip install openai google-genai requests streamlit numpy
   ```

2. **Set Environment Variables** (Replit Secrets tab)
   ```
   GITHUB_TOKEN=<your_github_personal_access_token>
   GOOGLE_CLOUD_PROJECT=<your_gcp_project_id>
   OPENAI_API_KEY=<your_openai_api_key>
   GOOGLE_API_KEY=<your_gemini_api_key>
   ```

3. **Validate Environment**
   ```bash
   python scripts/validate_environment.py
   python scripts/check_api_connections.py
   ```

### 1.2 GitHub Repository Setup

**Create GitHub Personal Access Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with permissions: `repo`, `workflow`, `admin:repo_hook`
3. Add token to Replit Secrets as `GITHUB_TOKEN`

**Repository Configuration:**
- Repository name: `echo-nexus-agi`
- Visibility: Private (recommended)
- Initialize with README: Yes

### 1.3 Google Cloud Platform Setup

**Project Setup:**
1. Create new GCP project: https://console.cloud.google.com/
2. Enable APIs:
   - Cloud Build API
   - Cloud Run API
   - Container Registry API
   - Cloud Storage API

**Authentication Setup:**
```bash
# Install Google Cloud SDK (if not in Replit)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

## Phase 2: Pipeline Deployment

### 2.1 Initialize Deployment Orchestrator

**Run deployment orchestrator:**
```python
import asyncio
from echo_nexus_deployment_orchestrator import get_deployment_orchestrator

async def deploy():
    orchestrator = get_deployment_orchestrator()
    
    # Check readiness
    readiness = await orchestrator.quick_deployment_check()
    print(f"Deployment readiness: {readiness['overall_status']}")
    
    if readiness['overall_status'] == 'ready':
        # Execute complete pipeline
        execution = await orchestrator.execute_complete_pipeline()
        return execution
    else:
        print("Address readiness issues before deployment")
        return readiness

# Run deployment
asyncio.run(deploy())
```

### 2.2 Manual Pipeline Execution (Alternative)

**Step 1: Code Modularization**
```bash
python scripts/modularize_agi_code.py
python scripts/generate_module_interfaces.py
```

**Step 2: GitHub Integration**
```bash
python scripts/setup_github_repository.py
git add .
git commit -m "Initial Echo Nexus AGI commit"
git push origin main
```

**Step 3: Cloud Build Setup**
```bash
gcloud builds triggers create github \
  --repo-name=echo-nexus-agi \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern=main \
  --build-config=cloudbuild.yaml
```

**Step 4: Deploy to Cloud Run**
```bash
gcloud run deploy echo-nexus-agi \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 4 \
  --allow-unauthenticated
```

## Phase 3: Integration and Testing

### 3.1 Update Replit Configuration

**Modify your main Replit app to use cloud backend:**

```python
import os
import requests

# Cloud Run endpoint
AGI_ENDPOINT = os.environ.get('AGI_ENDPOINT', 'http://localhost:8080')

async def query_agi(prompt, context=None):
    """Query the deployed AGI backend"""
    try:
        response = requests.post(
            f"{AGI_ENDPOINT}/api/query",
            json={
                "prompt": prompt,
                "context": context or {},
                "source": "replit"
            },
            timeout=30
        )
        return response.json()
    except Exception as e:
        print(f"AGI query failed: {e}")
        return {"error": str(e)}
```

### 3.2 Run Integration Tests

```bash
python scripts/run_integration_tests.py
python scripts/performance_benchmarking.py
```

## Phase 4: Monitoring and Maintenance

### 4.1 Setup Monitoring

```bash
python scripts/setup_monitoring.py
python scripts/configure_alerts.py
```

### 4.2 Continuous Growth Pipeline

**Automatic Triggers:**
- Every push to `main` branch triggers Cloud Build
- Cloud Build executes AGI training and deployment
- Updated models deployed to Cloud Run automatically

**Manual Growth Cycles:**
```bash
# Add new capabilities
git add new_features/
git commit -m "Add enhanced reasoning capabilities"
git push origin main  # Triggers automatic deployment
```

## Troubleshooting

### Common Issues

**1. Environment Variables Missing**
```bash
# Check all required variables are set
python scripts/validate_environment.py
```

**2. API Connection Failures**
```bash
# Test all API connections
python scripts/check_api_connections.py
```

**3. Cloud Build Failures**
```bash
# Check build logs
gcloud builds log --region=us-central1 BUILD_ID
```

**4. Cloud Run Deployment Issues**
```bash
# Check service logs
gcloud run services logs read echo-nexus-agi --region=us-central1
```

### Emergency Rollback

**If deployment fails:**
```bash
python scripts/emergency_rollback.py
```

**Manual rollback:**
```bash
# Rollback to previous Cloud Run revision
gcloud run services update-traffic echo-nexus-agi \
  --to-revisions=PREVIOUS_REVISION=100 \
  --region=us-central1
```

## Success Criteria

**Deployment is successful when:**

✅ Environment validation passes  
✅ All API connections working  
✅ GitHub repository created and configured  
✅ Cloud Build pipeline active  
✅ AGI deployed to Cloud Run  
✅ Replit integration updated  
✅ Integration tests passing  
✅ Monitoring active  

**Performance Indicators:**
- Response time < 2 seconds
- 99% uptime
- Automatic scaling working
- AGI capabilities enhanced over baseline

## Next Steps

After successful deployment:

1. **Monitor Performance**: Use Cloud Console to monitor AGI performance
2. **Continuous Improvement**: Regular pushes to trigger AGI growth cycles
3. **Feature Development**: Add new capabilities in modular format
4. **User Feedback**: Collect and integrate user feedback for AGI enhancement
5. **Scale Management**: Monitor and adjust Cloud Run scaling parameters

## Support and Documentation

- **Logs**: Check `logs/` directory for detailed execution logs
- **Status**: Run `python echo_nexus_deployment_orchestrator.py` for current status
- **Health Checks**: Monitor `/health` endpoint on deployed service
- **API Documentation**: Available at `/docs` on deployed service

## Security Best Practices

1. **Keep API keys secure** in Replit Secrets
2. **Use least privilege** for service accounts
3. **Regular security updates** through automated pipeline
4. **Monitor access logs** in Cloud Console
5. **Implement rate limiting** on public endpoints

This deployment plan transforms Echo Nexus from a Replit prototype into a scalable, production-ready AGI system with continuous growth capabilities.
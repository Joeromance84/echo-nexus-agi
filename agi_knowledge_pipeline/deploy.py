#!/usr/bin/env python3
"""
AGI Knowledge Pipeline Deployment Script
Automated deployment of the event-driven knowledge ingestion system
"""

import subprocess
import json
import os
import time
from datetime import datetime

class AGIKnowledgePipelineDeployer:
    """Handles deployment of the complete AGI knowledge pipeline"""
    
    def __init__(self, project_id: str, region: str = "us-central1"):
        self.project_id = project_id
        self.region = region
        self.function_name = "agi-knowledge-ingestion"
        self.raw_bucket = f"{project_id}-agi-knowledge-raw"
        self.processed_bucket = f"{project_id}-agi-processed"
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking deployment prerequisites...")
        
        # Check gcloud authentication
        try:
            result = subprocess.run(['gcloud', 'auth', 'list'], 
                                 capture_output=True, text=True, check=True)
            if "ACTIVE" not in result.stdout:
                print("❌ Please authenticate with gcloud: gcloud auth login")
                return False
        except subprocess.CalledProcessError:
            print("❌ gcloud CLI not found. Please install Google Cloud SDK")
            return False
        
        # Check project access
        try:
            subprocess.run(['gcloud', 'config', 'set', 'project', self.project_id], 
                         check=True, capture_output=True)
            print(f"✅ Project {self.project_id} configured")
        except subprocess.CalledProcessError:
            print(f"❌ Cannot access project {self.project_id}")
            return False
        
        return True
    
    def enable_required_apis(self):
        """Enable required Google Cloud APIs"""
        print("🔧 Enabling required APIs...")
        
        apis = [
            "cloudfunctions.googleapis.com",
            "storage.googleapis.com", 
            "aiplatform.googleapis.com",
            "logging.googleapis.com",
            "eventarc.googleapis.com"
        ]
        
        for api in apis:
            try:
                print(f"  Enabling {api}...")
                subprocess.run([
                    'gcloud', 'services', 'enable', api,
                    '--project', self.project_id
                ], check=True, capture_output=True)
                time.sleep(2)  # Rate limiting
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Failed to enable {api}: {e}")
        
        print("✅ APIs enabled")
    
    def create_storage_buckets(self):
        """Create required Cloud Storage buckets"""
        print("📦 Creating storage buckets...")
        
        buckets = [
            (self.raw_bucket, "Raw knowledge files (PDFs, EPUBs)"),
            (self.processed_bucket, "Processed knowledge chunks and embeddings")
        ]
        
        for bucket_name, description in buckets:
            try:
                # Check if bucket exists
                result = subprocess.run([
                    'gcloud', 'storage', 'buckets', 'describe', f'gs://{bucket_name}'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"  ✅ Bucket gs://{bucket_name} already exists")
                else:
                    # Create bucket
                    subprocess.run([
                        'gcloud', 'storage', 'buckets', 'create', f'gs://{bucket_name}',
                        '--location', self.region,
                        '--project', self.project_id
                    ], check=True, capture_output=True)
                    print(f"  ✅ Created bucket gs://{bucket_name}")
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create bucket {bucket_name}: {e}")
                return False
        
        return True
    
    def deploy_cloud_function(self):
        """Deploy the AGI knowledge ingestion Cloud Function"""
        print("🚀 Deploying AGI Knowledge Ingestion Cloud Function...")
        
        # Prepare environment variables
        env_vars = [
            f"GOOGLE_CLOUD_PROJECT={self.project_id}",
            f"GOOGLE_CLOUD_REGION={self.region}",
            f"PROCESSED_BUCKET={self.processed_bucket}",
            "CHUNK_SIZE=1000",
            "CHUNK_OVERLAP=200"
        ]
        
        try:
            deploy_cmd = [
                'gcloud', 'functions', 'deploy', self.function_name,
                '--gen2',
                '--runtime=python311',
                f'--region={self.region}',
                '--source=.',
                '--entry-point=agi_knowledge_ingestion',
                f'--trigger-bucket={self.raw_bucket}',
                '--memory=2Gi',
                '--timeout=540s',
                '--max-instances=10',
                '--set-env-vars=' + ','.join(env_vars),
                f'--project={self.project_id}'
            ]
            
            print(f"  Deploying function with trigger on gs://{self.raw_bucket}")
            
            result = subprocess.run(deploy_cmd, capture_output=True, text=True, check=True)
            
            print("✅ Cloud Function deployed successfully!")
            print(f"  Function URL: {self.extract_function_url(result.stdout)}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to deploy Cloud Function: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def extract_function_url(self, deploy_output: str) -> str:
        """Extract function URL from deployment output"""
        lines = deploy_output.split('\n')
        for line in lines:
            if 'url:' in line.lower():
                return line.split(':', 1)[1].strip()
        return "URL not found in deployment output"
    
    def setup_iam_permissions(self):
        """Setup required IAM permissions"""
        print("🔐 Setting up IAM permissions...")
        
        try:
            # Get the Cloud Function service account
            result = subprocess.run([
                'gcloud', 'functions', 'describe', self.function_name,
                f'--region={self.region}',
                '--format=value(serviceConfig.serviceAccountEmail)'
            ], capture_output=True, text=True, check=True)
            
            service_account = result.stdout.strip()
            
            if service_account:
                # Grant necessary permissions
                permissions = [
                    "roles/storage.objectAdmin",
                    "roles/aiplatform.user",
                    "roles/logging.logWriter"
                ]
                
                for permission in permissions:
                    subprocess.run([
                        'gcloud', 'projects', 'add-iam-policy-binding', self.project_id,
                        f'--member=serviceAccount:{service_account}',
                        f'--role={permission}'
                    ], check=True, capture_output=True)
                
                print(f"✅ IAM permissions configured for {service_account}")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ IAM setup warning: {e}")
    
    def create_test_files(self):
        """Create test files and documentation"""
        print("📝 Creating test files and documentation...")
        
        # Create test script
        test_script = '''#!/usr/bin/env python3
"""
Test script for AGI Knowledge Pipeline
"""

import subprocess
import sys
import time

def test_pipeline(project_id, raw_bucket):
    """Test the AGI knowledge pipeline"""
    print("🧪 Testing AGI Knowledge Pipeline...")
    
    # Create a test PDF (placeholder)
    test_content = """
    This is a test document for the AGI Knowledge Pipeline.
    
    It contains multiple paragraphs to test the chunking algorithm.
    The system should extract this text and create embeddings.
    
    This demonstrates the automated knowledge ingestion process.
    """
    
    with open('test_document.txt', 'w') as f:
        f.write(test_content)
    
    # Upload test file
    try:
        subprocess.run([
            'gcloud', 'storage', 'cp', 'test_document.txt', 
            f'gs://{raw_bucket}/test_document.txt'
        ], check=True)
        
        print("✅ Test file uploaded - pipeline should trigger automatically")
        print("📊 Check Cloud Functions logs for processing status")
        print(f"   gcloud functions logs read agi-knowledge-ingestion --region=us-central1")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upload test file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_pipeline.py <project_id> <raw_bucket>")
        sys.exit(1)
    
    test_pipeline(sys.argv[1], sys.argv[2])
'''
        
        with open('test_pipeline.py', 'w') as f:
            f.write(test_script)
        
        # Create deployment documentation
        docs = f'''# AGI Knowledge Pipeline Deployment

## Architecture Overview

The AGI Knowledge Pipeline is an event-driven system that automatically processes PDFs and EPUBs into AGI-accessible knowledge.

### Components Deployed:

1. **Cloud Storage Buckets:**
   - Raw Files: gs://{self.raw_bucket}
   - Processed Data: gs://{self.processed_bucket}

2. **Cloud Function:**
   - Name: {self.function_name}
   - Region: {self.region}
   - Trigger: File uploads to raw bucket

3. **Processing Pipeline:**
   - Text extraction (PDF/EPUB)
   - Intelligent chunking with context preservation
   - Vector embedding generation (Vertex AI)
   - Knowledge indexing for AGI access

## Usage

1. **Upload Knowledge Files:**
   ```bash
   gcloud storage cp your_document.pdf gs://{self.raw_bucket}/
   ```

2. **Monitor Processing:**
   ```bash
   gcloud functions logs read {self.function_name} --region={self.region}
   ```

3. **Access Processed Knowledge:**
   - Processed chunks: gs://{self.processed_bucket}/processed/
   - AGI Index: gs://{self.processed_bucket}/agi_knowledge_index/

## Testing

Run the test script:
```bash
python test_pipeline.py {self.project_id} {self.raw_bucket}
```

## Monitoring

- Cloud Function logs: Google Cloud Console > Cloud Functions
- Storage activity: Google Cloud Console > Cloud Storage
- Processing metrics: Check function execution logs

Deployment completed: {datetime.now().isoformat()}
'''
        
        with open('DEPLOYMENT_README.md', 'w') as f:
            f.write(docs)
        
        print("✅ Test files and documentation created")
    
    def deploy_complete_pipeline(self):
        """Deploy the complete AGI knowledge pipeline"""
        print("🌟 DEPLOYING AGI KNOWLEDGE PIPELINE")
        print("=" * 60)
        print("Creating event-driven automated knowledge ingestion for AGI")
        print("=" * 60)
        
        steps = [
            ("Prerequisites Check", self.check_prerequisites),
            ("API Enablement", self.enable_required_apis),
            ("Storage Setup", self.create_storage_buckets),
            ("Function Deployment", self.deploy_cloud_function),
            ("IAM Configuration", self.setup_iam_permissions),
            ("Test Files Creation", self.create_test_files)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                result = step_func()
                if result is False:
                    print(f"❌ {step_name} failed - stopping deployment")
                    return False
                print(f"✅ {step_name} completed")
            except Exception as e:
                print(f"❌ {step_name} error: {e}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 AGI KNOWLEDGE PIPELINE DEPLOYMENT COMPLETE!")
        print("=" * 60)
        print(f"📦 Raw files bucket: gs://{self.raw_bucket}")
        print(f"📊 Processed data bucket: gs://{self.processed_bucket}")
        print(f"⚡ Function name: {self.function_name}")
        print(f"🌍 Region: {self.region}")
        print("\n🚀 To test the pipeline:")
        print(f"   gcloud storage cp your_document.pdf gs://{self.raw_bucket}/")
        print("\n📊 To monitor processing:")
        print(f"   gcloud functions logs read {self.function_name} --region={self.region}")
        print("\n💡 Your AGI can now automatically ingest knowledge from uploaded documents!")
        
        return True

def main():
    """Main deployment function"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <your-google-cloud-project-id>")
        print("Example: python deploy.py my-agi-project-123")
        sys.exit(1)
    
    project_id = sys.argv[1]
    
    print("🤖 AGI KNOWLEDGE PIPELINE DEPLOYMENT")
    print("=" * 50)
    print("This will deploy an automated knowledge ingestion system")
    print(f"Project: {project_id}")
    print("=" * 50)
    
    deployer = AGIKnowledgePipelineDeployer(project_id)
    success = deployer.deploy_complete_pipeline()
    
    if success:
        print("\n✨ Deployment successful! Your AGI knowledge pipeline is ready.")
    else:
        print("\n💥 Deployment failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
EchoNexus Cloud Storage Manager
Intelligent cloud resource utilization for large-scale document processing
"""

import os
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile
import logging

class CloudStorageManager:
    """Manages cloud storage and processing for large documents"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.gcp_project_id = os.getenv('GCP_PROJECT_ID', 'echo-nexus-federation')
        self.cloud_bucket_name = f"echo-nexus-documents-{int(time.time())}"
        
        # Cloud processing triggers
        self.cloud_pipeline_repo = "echonexus-document-processor"
        self.processing_workflow = "document-ingestion.yml"
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_cloud_storage_bucket(self) -> Dict[str, Any]:
        """Create Google Cloud Storage bucket for document processing"""
        
        try:
            # Generate cloud build configuration
            cloudbuild_config = self._generate_cloudbuild_config()
            
            # Create repository for cloud processing
            repo_result = self._create_cloud_processing_repo()
            
            return {
                'success': True,
                'bucket_name': self.cloud_bucket_name,
                'repository': repo_result.get('repo_url'),
                'cloudbuild_config': cloudbuild_config
            }
            
        except Exception as e:
            self.logger.error(f"Cloud bucket creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_cloud_processing_repo(self) -> Dict[str, Any]:
        """Create GitHub repository for cloud document processing"""
        
        try:
            from github import Github
            
            if not self.github_token:
                return {'error': 'GitHub token required'}
            
            g = Github(self.github_token)
            user = g.get_user()
            
            # Create repository
            repo = user.create_repo(
                name=self.cloud_pipeline_repo,
                description="EchoNexus cloud document processing pipeline",
                private=False,
                auto_init=True
            )
            
            # Add workflow file
            workflow_content = self._generate_processing_workflow()
            
            repo.create_file(
                path=f".github/workflows/{self.processing_workflow}",
                message="Add document processing workflow",
                content=workflow_content
            )
            
            # Add processing script
            processor_script = self._generate_processor_script()
            
            repo.create_file(
                path="process_documents.py",
                message="Add document processor script",
                content=processor_script
            )
            
            # Add requirements
            requirements = self._generate_requirements()
            
            repo.create_file(
                path="requirements.txt",
                message="Add Python requirements",
                content=requirements
            )
            
            return {
                'success': True,
                'repo_url': repo.html_url,
                'repo_name': repo.name
            }
            
        except Exception as e:
            self.logger.error(f"Repository creation failed: {e}")
            return {'error': str(e)}
    
    def _generate_cloudbuild_config(self) -> str:
        """Generate Google Cloud Build configuration"""
        
        return f"""steps:
  # Step 1: Setup Python environment
  - name: 'python:3.11'
    entrypoint: 'pip'
    args: ['install', '-r', 'requirements.txt']

  # Step 2: Download documents from Cloud Storage
  - name: 'gcr.io/cloud-builders/gsutil'
    args: ['cp', '-r', 'gs://{self.cloud_bucket_name}/*', './documents/']

  # Step 3: Process documents
  - name: 'python:3.11'
    entrypoint: 'python'
    args: ['process_documents.py', '--input-dir', './documents/', '--output-dir', './processed/']
    env:
      - 'OPENAI_API_KEY=${{_OPENAI_API_KEY}}'
      - 'PROCESSING_MODE=cloud'
      - 'MAX_MEMORY_GB=8'

  # Step 4: Upload processed vectors to Cloud Storage
  - name: 'gcr.io/cloud-builders/gsutil'
    args: ['cp', '-r', './processed/*', 'gs://{self.cloud_bucket_name}-processed/']

  # Step 5: Trigger webhook notification
  - name: 'gcr.io/cloud-builders/curl'
    args: 
      - '-X'
      - 'POST'
      - '-H'
      - 'Content-Type: application/json'
      - '-d'
      - '{{"status": "completed", "bucket": "{self.cloud_bucket_name}-processed"}}'
      - 'https://api.github.com/repos/${{_GITHUB_USER}}/Echo_AI/dispatches'
      - '-H'
      - 'Authorization: token ${{_GITHUB_TOKEN}}'

options:
  machineType: 'E2_HIGHCPU_8'
  diskSizeGb: '100'

timeout: '3600s'

substitutions:
  _OPENAI_API_KEY: ''
  _GITHUB_TOKEN: ''
  _GITHUB_USER: ''
"""
    
    def _generate_processing_workflow(self) -> str:
        """Generate GitHub Actions workflow for document processing"""
        
        return f"""name: EchoNexus Document Processing Pipeline

on:
  workflow_dispatch:
    inputs:
      bucket_name:
        description: 'Cloud Storage bucket containing documents'
        required: true
        type: string
      processing_mode:
        description: 'Processing mode'
        required: true
        default: 'batch'
        type: choice
        options:
        - batch
        - streaming
        - memory_optimized

  repository_dispatch:
    types: [process_documents]

jobs:
  setup-cloud-processing:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Setup Google Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        project_id: ${{{{ secrets.GCP_PROJECT_ID }}}}
        service_account_key: ${{{{ secrets.GCP_SA_KEY }}}}
        export_default_credentials: true
    
    - name: Trigger Cloud Build Processing
      env:
        OPENAI_API_KEY: ${{{{ secrets.OPENAI_API_KEY }}}}
        GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
      run: |
        # Create Cloud Build trigger
        gcloud builds submit \\
          --config=cloudbuild.yaml \\
          --substitutions=_OPENAI_API_KEY="${{OPENAI_API_KEY}}",_GITHUB_TOKEN="${{GITHUB_TOKEN}}" \\
          .
    
    - name: Monitor Processing Status
      run: |
        echo "Monitoring cloud processing..."
        python monitor_cloud_processing.py \\
          --bucket-name="${{{{ github.event.inputs.bucket_name || 'default-bucket' }}}}" \\
          --timeout=3600
    
    - name: Validate Processing Results
      run: |
        echo "Validating processing results..."
        python validate_processing.py \\
          --output-bucket="{self.cloud_bucket_name}-processed"
    
    - name: Update Knowledge Base
      env:
        GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
      run: |
        # Trigger knowledge base update
        curl -X POST \\
          -H "Authorization: token ${{GITHUB_TOKEN}}" \\
          -H "Accept: application/vnd.github.v3+json" \\
          https://api.github.com/repos/${{{{ github.repository_owner }}}}/Echo_AI/dispatches \\
          -d '{{"event_type":"knowledge_base_update","client_payload":{{"bucket":"{self.cloud_bucket_name}-processed"}}}}'
"""
    
    def _generate_processor_script(self) -> str:
        """Generate cloud document processor script"""
        
        return '''#!/usr/bin/env python3
"""
EchoNexus Cloud Document Processor
High-performance document processing for large-scale ingestion
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import tempfile
import logging
from datetime import datetime

# Document processing libraries
try:
    import fitz  # PyMuPDF
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Required library missing: {e}")
    sys.exit(1)

# Vector processing
import numpy as np
from openai import OpenAI

class CloudDocumentProcessor:
    """High-performance cloud document processor"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.batch_size = 50
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def process_documents_batch(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """Process all documents in batch mode"""
        
        results = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'total_chunks': 0,
            'total_vectors': 0,
            'processing_time': 0
        }
        
        start_time = datetime.now()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all documents
        input_path = Path(input_dir)
        documents = list(input_path.glob('**/*.pdf')) + list(input_path.glob('**/*.epub'))
        
        results['total_files'] = len(documents)
        
        self.logger.info(f"Processing {len(documents)} documents")
        
        for doc_path in documents:
            try:
                doc_result = self.process_single_document(doc_path, output_dir)
                
                if doc_result['success']:
                    results['processed_files'] += 1
                    results['total_chunks'] += doc_result['chunks_count']
                    results['total_vectors'] += doc_result['vectors_count']
                else:
                    results['failed_files'] += 1
                    self.logger.error(f"Failed to process {doc_path}: {doc_result.get('error')}")
                
            except Exception as e:
                results['failed_files'] += 1
                self.logger.error(f"Error processing {doc_path}: {e}")
        
        results['processing_time'] = (datetime.now() - start_time).total_seconds()
        
        # Save processing summary
        summary_file = os.path.join(output_dir, 'processing_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def process_single_document(self, doc_path: Path, output_dir: str) -> Dict[str, Any]:
        """Process a single document"""
        
        result = {
            'success': False,
            'chunks_count': 0,
            'vectors_count': 0,
            'file_size': 0
        }
        
        try:
            # Extract text
            text_content = self.extract_text(doc_path)
            
            if not text_content:
                result['error'] = 'No text extracted'
                return result
            
            # Create chunks
            chunks = self.create_chunks(text_content)
            result['chunks_count'] = len(chunks)
            
            # Generate vectors
            vectors = self.generate_vectors_batch(chunks)
            result['vectors_count'] = len(vectors)
            
            # Save results
            doc_id = self.generate_doc_id(doc_path.name)
            self.save_document_data(doc_id, doc_path.name, chunks, vectors, output_dir)
            
            result['success'] = True
            result['file_size'] = doc_path.stat().st_size
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def extract_text(self, doc_path: Path) -> str:
        """Extract text from document"""
        
        if doc_path.suffix.lower() == '.pdf':
            return self.extract_pdf_text(doc_path)
        elif doc_path.suffix.lower() in ['.epub', '.epub3']:
            return self.extract_epub_text(doc_path)
        else:
            return ""
    
    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        
        try:
            doc = fitz.open(pdf_path)
            text_content = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text_content += page.get_text() + "\\n"
            
            doc.close()
            return text_content
        
        except Exception as e:
            self.logger.error(f"PDF extraction error: {e}")
            return ""
    
    def extract_epub_text(self, epub_path: Path) -> str:
        """Extract text from EPUB"""
        
        try:
            book = epub.read_epub(epub_path)
            text_content = ""
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content().decode('utf-8')
                    soup = BeautifulSoup(content, 'html.parser')
                    text_content += soup.get_text() + "\\n"
            
            return text_content
        
        except Exception as e:
            self.logger.error(f"EPUB extraction error: {e}")
            return ""
    
    def create_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Create text chunks"""
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            if end < len(text):
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + 100:
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start_pos': start,
                    'end_pos': end
                })
                chunk_id += 1
            
            start = end - self.chunk_overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def generate_vectors_batch(self, chunks: List[Dict[str, Any]]) -> List[np.ndarray]:
        """Generate vectors in batches"""
        
        vectors = []
        
        for i in range(0, len(chunks), self.batch_size):
            batch_chunks = chunks[i:i + self.batch_size]
            batch_texts = [chunk['text'] for chunk in batch_chunks]
            
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=batch_texts
                )
                
                for embedding_data in response.data:
                    vector = np.array(embedding_data.embedding)
                    vectors.append(vector)
                
            except Exception as e:
                self.logger.error(f"Vector generation error: {e}")
                # Add zero vectors for failed batch
                for _ in batch_chunks:
                    vectors.append(np.zeros(1536))
        
        return vectors
    
    def generate_doc_id(self, filename: str) -> str:
        """Generate document ID"""
        import hashlib
        return hashlib.md5(filename.encode()).hexdigest()
    
    def save_document_data(self, doc_id: str, filename: str, chunks: List[Dict], 
                          vectors: List[np.ndarray], output_dir: str):
        """Save processed document data"""
        
        # Save vectors
        vectors_file = os.path.join(output_dir, f"{doc_id}_vectors.npy")
        np.save(vectors_file, np.array(vectors))
        
        # Save chunks
        chunks_file = os.path.join(output_dir, f"{doc_id}_chunks.json")
        with open(chunks_file, 'w') as f:
            json.dump(chunks, f, indent=2)
        
        # Save metadata
        metadata = {
            'doc_id': doc_id,
            'filename': filename,
            'chunks_count': len(chunks),
            'vectors_count': len(vectors),
            'processed_at': datetime.now().isoformat(),
            'vectors_file': vectors_file,
            'chunks_file': chunks_file
        }
        
        metadata_file = os.path.join(output_dir, f"{doc_id}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='EchoNexus Cloud Document Processor')
    parser.add_argument('--input-dir', required=True, help='Input directory containing documents')
    parser.add_argument('--output-dir', required=True, help='Output directory for processed data')
    parser.add_argument('--mode', default='batch', choices=['batch', 'streaming'], help='Processing mode')
    
    args = parser.parse_args()
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable required")
        sys.exit(1)
    
    processor = CloudDocumentProcessor(openai_api_key)
    
    print(f"Starting document processing...")
    print(f"Input: {args.input_dir}")
    print(f"Output: {args.output_dir}")
    print(f"Mode: {args.mode}")
    
    results = processor.process_documents_batch(args.input_dir, args.output_dir)
    
    print(f"\\nProcessing completed:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Processed: {results['processed_files']}")
    print(f"  Failed: {results['failed_files']}")
    print(f"  Total chunks: {results['total_chunks']}")
    print(f"  Total vectors: {results['total_vectors']}")
    print(f"  Processing time: {results['processing_time']:.2f} seconds")

if __name__ == '__main__':
    main()
'''
    
    def _generate_requirements(self) -> str:
        """Generate Python requirements"""
        
        return """PyMuPDF>=1.23.0
ebooklib>=0.18
beautifulsoup4>=4.12.0
numpy>=1.24.0
openai>=1.3.0
google-cloud-storage>=2.10.0
psutil>=5.9.0
requests>=2.31.0
"""
    
    def trigger_cloud_processing(self, bucket_name: str, processing_mode: str = 'batch') -> Dict[str, Any]:
        """Trigger cloud document processing"""
        
        try:
            from github import Github
            
            if not self.github_token:
                return {'error': 'GitHub token required'}
            
            g = Github(self.github_token)
            
            # Get the processing repository
            try:
                repo = g.get_user().get_repo(self.cloud_pipeline_repo)
            except:
                # Repository doesn't exist, create it
                create_result = self._create_cloud_processing_repo()
                if not create_result.get('success'):
                    return create_result
                repo = g.get_user().get_repo(self.cloud_pipeline_repo)
            
            # Trigger workflow
            workflow_dispatch = {
                'ref': 'main',
                'inputs': {
                    'bucket_name': bucket_name,
                    'processing_mode': processing_mode
                }
            }
            
            # Get workflow
            workflows = repo.get_workflows()
            target_workflow = None
            
            for workflow in workflows:
                if self.processing_workflow in workflow.path:
                    target_workflow = workflow
                    break
            
            if target_workflow:
                target_workflow.create_dispatch('main', workflow_dispatch['inputs'])
                
                return {
                    'success': True,
                    'workflow_id': target_workflow.id,
                    'repository': repo.html_url,
                    'triggered_at': datetime.now().isoformat()
                }
            else:
                return {'error': 'Processing workflow not found'}
            
        except Exception as e:
            self.logger.error(f"Cloud processing trigger failed: {e}")
            return {'error': str(e)}
    
    def monitor_cloud_processing(self, workflow_id: int, timeout_seconds: int = 3600) -> Dict[str, Any]:
        """Monitor cloud processing status"""
        
        try:
            from github import Github
            
            g = Github(self.github_token)
            repo = g.get_user().get_repo(self.cloud_pipeline_repo)
            
            start_time = time.time()
            
            while time.time() - start_time < timeout_seconds:
                # Get workflow runs
                runs = repo.get_workflow_runs()
                
                for run in runs:
                    if run.workflow_id == workflow_id:
                        if run.conclusion == 'success':
                            return {
                                'status': 'completed',
                                'success': True,
                                'run_url': run.html_url,
                                'duration': time.time() - start_time
                            }
                        elif run.conclusion == 'failure':
                            return {
                                'status': 'failed',
                                'success': False,
                                'run_url': run.html_url,
                                'error': 'Workflow execution failed'
                            }
                        elif run.status == 'in_progress':
                            self.logger.info(f"Processing in progress... ({run.status})")
                
                time.sleep(30)  # Check every 30 seconds
            
            return {
                'status': 'timeout',
                'success': False,
                'error': 'Processing timeout exceeded'
            }
            
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
            return {'error': str(e)}
    
    def get_cloud_storage_info(self) -> Dict[str, Any]:
        """Get cloud storage configuration info"""
        
        return {
            'bucket_name': self.cloud_bucket_name,
            'processing_repo': self.cloud_pipeline_repo,
            'workflow_file': self.processing_workflow,
            'supported_formats': ['pdf', 'epub'],
            'max_file_size_gb': 10,
            'batch_processing': True,
            'auto_cleanup': True
        }

def main():
    """Test cloud storage manager"""
    
    print("☁️ EchoNexus Cloud Storage Manager")
    print("Intelligent cloud resource utilization for document processing")
    
    manager = CloudStorageManager()
    info = manager.get_cloud_storage_info()
    
    print(f"\n📊 Cloud Configuration:")
    print(f"  • Bucket: {info['bucket_name']}")
    print(f"  • Repository: {info['processing_repo']}")
    print(f"  • Supported formats: {', '.join(info['supported_formats'])}")
    print(f"  • Max file size: {info['max_file_size_gb']} GB")

if __name__ == '__main__':
    main()
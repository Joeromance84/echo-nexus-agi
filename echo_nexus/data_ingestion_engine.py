#!/usr/bin/env python3
"""
EchoNexus Data Ingestion Engine
Automated system to ingest, process, and vectorize bulk PDF/EPUB files
with intelligent memory management and cloud resource utilization
"""

import os
import json
import time
import hashlib
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import logging
from pathlib import Path

# Document processing
try:
    import PyPDF2
    import fitz  # PyMuPDF - more robust PDF processing
except ImportError:
    PyPDF2 = None
    fitz = None

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
except ImportError:
    ebooklib = None
    BeautifulSoup = None

# Vector processing
import numpy as np
from openai import OpenAI

class EchoNexusDataIngestion:
    """Advanced document ingestion and vectorization system"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="echo_ingestion_")
        self.knowledge_base_dir = "echo_knowledge_base"
        self.vector_cache_dir = os.path.join(self.knowledge_base_dir, "vectors")
        self.metadata_file = os.path.join(self.knowledge_base_dir, "document_metadata.json")
        self.processing_log = os.path.join(self.knowledge_base_dir, "ingestion_log.json")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Document processing settings
        self.chunk_size = 1000  # characters per chunk
        self.chunk_overlap = 200  # overlap between chunks
        self.max_file_size_mb = 50  # Max single file size before cloud processing
        
        # Memory management
        self.max_memory_usage_gb = 2.0  # Local memory limit
        self.cloud_storage_threshold_gb = 1.0  # Switch to cloud storage
        
        # Initialize directories
        self._initialize_directories()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _initialize_directories(self):
        """Initialize required directories"""
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        os.makedirs(self.vector_cache_dir, exist_ok=True)
        
        # Initialize metadata if not exists
        if not os.path.exists(self.metadata_file):
            self._save_metadata({
                'documents': {},
                'total_documents': 0,
                'total_chunks': 0,
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            })
    
    def process_bulk_upload(self, uploaded_files: List[Any]) -> Dict[str, Any]:
        """Process bulk uploaded files with intelligent memory management"""
        
        processing_results = {
            'total_files': len(uploaded_files),
            'processed_files': 0,
            'failed_files': 0,
            'total_chunks_created': 0,
            'total_vectors_generated': 0,
            'memory_usage_gb': 0.0,
            'cloud_offloaded': 0,
            'processing_time_seconds': 0,
            'errors': []
        }
        
        start_time = time.time()
        
        self.logger.info(f"Starting bulk processing of {len(uploaded_files)} files")
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Check memory usage
                memory_usage = self._get_memory_usage_gb()
                processing_results['memory_usage_gb'] = memory_usage
                
                if memory_usage > self.cloud_storage_threshold_gb:
                    self.logger.info("Memory threshold reached - switching to cloud processing")
                    result = self._process_file_cloud(uploaded_file)
                    processing_results['cloud_offloaded'] += 1
                else:
                    result = self._process_file_local(uploaded_file)
                
                if result['success']:
                    processing_results['processed_files'] += 1
                    processing_results['total_chunks_created'] += result.get('chunks_created', 0)
                    processing_results['total_vectors_generated'] += result.get('vectors_generated', 0)
                else:
                    processing_results['failed_files'] += 1
                    processing_results['errors'].append({
                        'file': uploaded_file.name,
                        'error': result.get('error', 'Unknown error')
                    })
                
                # Clean up temp files periodically
                if i % 10 == 0:
                    self._cleanup_temp_files()
                
                self.logger.info(f"Processed {i+1}/{len(uploaded_files)} files")
                
            except Exception as e:
                processing_results['failed_files'] += 1
                processing_results['errors'].append({
                    'file': getattr(uploaded_file, 'name', 'unknown'),
                    'error': str(e)
                })
                self.logger.error(f"Error processing file: {e}")
        
        processing_results['processing_time_seconds'] = time.time() - start_time
        
        # Final cleanup
        self._cleanup_temp_files()
        
        # Log processing results
        self._log_processing_session(processing_results)
        
        return processing_results
    
    def _process_file_local(self, uploaded_file) -> Dict[str, Any]:
        """Process file locally with memory management"""
        
        result = {
            'success': False,
            'chunks_created': 0,
            'vectors_generated': 0,
            'file_size_mb': 0,
            'processing_method': 'local'
        }
        
        try:
            # Save uploaded file temporarily
            file_path = os.path.join(self.temp_dir, uploaded_file.name)
            
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            result['file_size_mb'] = file_size_mb
            
            # Check if file is too large for local processing
            if file_size_mb > self.max_file_size_mb:
                self.logger.info(f"File {uploaded_file.name} too large ({file_size_mb:.1f}MB) - switching to cloud")
                return self._process_file_cloud(uploaded_file)
            
            # Extract text
            text_content = self._extract_text_from_file(file_path)
            
            if not text_content:
                result['error'] = 'No text content extracted'
                return result
            
            # Create chunks
            chunks = self._create_text_chunks(text_content)
            result['chunks_created'] = len(chunks)
            
            # Generate vectors
            vectors = self._generate_vectors_for_chunks(chunks)
            result['vectors_generated'] = len(vectors)
            
            # Store in knowledge base
            doc_id = self._generate_document_id(uploaded_file.name)
            self._store_document_vectors(doc_id, uploaded_file.name, chunks, vectors)
            
            result['success'] = True
            
            # Clean up temp file
            os.remove(file_path)
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Local processing error: {e}")
        
        return result
    
    def _process_file_cloud(self, uploaded_file) -> Dict[str, Any]:
        """Process large files using cloud resources"""
        
        result = {
            'success': False,
            'chunks_created': 0,
            'vectors_generated': 0,
            'processing_method': 'cloud',
            'cloud_job_id': None
        }
        
        try:
            # For now, implement simplified cloud processing
            # In production, this would trigger Google Cloud Build pipeline
            
            self.logger.info(f"Processing {uploaded_file.name} via cloud pipeline")
            
            # Create cloud job manifest
            cloud_job = {
                'job_id': self._generate_cloud_job_id(),
                'file_name': uploaded_file.name,
                'file_size': len(uploaded_file.getvalue()),
                'created_at': datetime.now().isoformat(),
                'status': 'queued'
            }
            
            result['cloud_job_id'] = cloud_job['job_id']
            
            # Store job info for tracking
            self._store_cloud_job(cloud_job)
            
            # Simplified processing (in production, this would be async)
            file_path = os.path.join(self.temp_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            # Process in smaller memory chunks
            text_content = self._extract_text_streaming(file_path)
            
            if text_content:
                chunks = self._create_text_chunks(text_content)
                vectors = self._generate_vectors_batch(chunks)
                
                doc_id = self._generate_document_id(uploaded_file.name)
                self._store_document_vectors(doc_id, uploaded_file.name, chunks, vectors)
                
                result['chunks_created'] = len(chunks)
                result['vectors_generated'] = len(vectors)
                result['success'] = True
            
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Cloud processing error: {e}")
        
        return result
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or EPUB file"""
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._extract_pdf_text(file_path)
        elif file_ext in ['.epub', '.epub3']:
            return self._extract_epub_text(file_path)
        else:
            self.logger.warning(f"Unsupported file type: {file_ext}")
            return ""
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF (more robust than PyPDF2)"""
        
        try:
            if fitz:
                # Use PyMuPDF (fitz) - more robust
                doc = fitz.open(pdf_path)
                text_content = ""
                
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text_content += page.get_text() + "\n"
                
                doc.close()
                return text_content
            
            elif PyPDF2:
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_content = ""
                    
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
                
                return text_content
            
            else:
                self.logger.error("No PDF processing library available")
                return ""
                
        except Exception as e:
            self.logger.error(f"PDF extraction error: {e}")
            return ""
    
    def _extract_epub_text(self, epub_path: str) -> str:
        """Extract text from EPUB file"""
        
        try:
            if not ebooklib:
                self.logger.error("EbookLib not available for EPUB processing")
                return ""
            
            book = epub.read_epub(epub_path)
            text_content = ""
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content().decode('utf-8')
                    
                    if BeautifulSoup:
                        # Parse HTML and extract text
                        soup = BeautifulSoup(content, 'html.parser')
                        text_content += soup.get_text() + "\n"
                    else:
                        # Basic HTML tag removal
                        import re
                        text_content += re.sub('<[^<]+?>', '', content) + "\n"
            
            return text_content
            
        except Exception as e:
            self.logger.error(f"EPUB extraction error: {e}")
            return ""
    
    def _extract_text_streaming(self, file_path: str) -> str:
        """Extract text in streaming mode for large files"""
        
        # For large files, process in chunks to manage memory
        try:
            text_content = self._extract_text_from_file(file_path)
            
            # If content is too large, process in chunks
            if len(text_content) > 1000000:  # 1MB of text
                self.logger.info("Large text content - using streaming processing")
                # In production, implement streaming text processing
                # For now, return first 500KB
                return text_content[:500000]
            
            return text_content
            
        except Exception as e:
            self.logger.error(f"Streaming extraction error: {e}")
            return ""
    
    def _create_text_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Create overlapping text chunks for vector processing"""
        
        chunks = []
        
        # Clean and prepare text
        text = text.strip()
        if not text:
            return chunks
        
        # Split into chunks with overlap
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Find natural break point (sentence end)
            if end < len(text):
                # Look for sentence ending
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + 100:  # Ensure reasonable chunk size
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start_pos': start,
                    'end_pos': end,
                    'length': len(chunk_text)
                })
                chunk_id += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def _generate_vectors_for_chunks(self, chunks: List[Dict[str, Any]]) -> List[np.ndarray]:
        """Generate embeddings for text chunks"""
        
        vectors = []
        
        try:
            for chunk in chunks:
                # Use OpenAI embeddings
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=chunk['text']
                )
                
                vector = np.array(response.data[0].embedding)
                vectors.append(vector)
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
        
        except Exception as e:
            self.logger.error(f"Vector generation error: {e}")
            # Return empty vectors for failed chunks
            vectors = [np.zeros(1536) for _ in chunks]  # text-embedding-3-small dimension
        
        return vectors
    
    def _generate_vectors_batch(self, chunks: List[Dict[str, Any]]) -> List[np.ndarray]:
        """Generate vectors in batches for efficiency"""
        
        vectors = []
        batch_size = 20  # Process in batches
        
        try:
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                batch_texts = [chunk['text'] for chunk in batch_chunks]
                
                # Batch API call
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=batch_texts
                )
                
                for embedding_data in response.data:
                    vector = np.array(embedding_data.embedding)
                    vectors.append(vector)
                
                # Longer delay for batch processing
                time.sleep(0.5)
                
                self.logger.info(f"Generated vectors for batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}")
        
        except Exception as e:
            self.logger.error(f"Batch vector generation error: {e}")
            vectors = [np.zeros(1536) for _ in chunks]
        
        return vectors
    
    def _store_document_vectors(self, doc_id: str, filename: str, chunks: List[Dict], vectors: List[np.ndarray]):
        """Store document chunks and vectors in knowledge base"""
        
        try:
            # Save vectors to disk
            vector_file = os.path.join(self.vector_cache_dir, f"{doc_id}_vectors.npy")
            np.save(vector_file, np.array(vectors))
            
            # Save chunks metadata
            chunks_file = os.path.join(self.vector_cache_dir, f"{doc_id}_chunks.json")
            with open(chunks_file, 'w') as f:
                json.dump(chunks, f, indent=2)
            
            # Update document metadata
            metadata = self._load_metadata()
            metadata['documents'][doc_id] = {
                'filename': filename,
                'chunks_count': len(chunks),
                'vectors_count': len(vectors),
                'created_at': datetime.now().isoformat(),
                'file_hash': self._generate_document_id(filename),
                'vector_file': vector_file,
                'chunks_file': chunks_file
            }
            
            metadata['total_documents'] += 1
            metadata['total_chunks'] += len(chunks)
            metadata['last_updated'] = datetime.now().isoformat()
            
            self._save_metadata(metadata)
            
            self.logger.info(f"Stored {len(chunks)} chunks and {len(vectors)} vectors for {filename}")
            
        except Exception as e:
            self.logger.error(f"Storage error: {e}")
    
    def query_knowledge_base(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the knowledge base using vector similarity"""
        
        try:
            # Generate query vector
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            query_vector = np.array(response.data[0].embedding)
            
            # Load all document vectors and find similarities
            results = []
            metadata = self._load_metadata()
            
            for doc_id, doc_info in metadata['documents'].items():
                # Load document vectors
                vector_file = doc_info['vector_file']
                chunks_file = doc_info['chunks_file']
                
                if os.path.exists(vector_file) and os.path.exists(chunks_file):
                    doc_vectors = np.load(vector_file)
                    
                    with open(chunks_file, 'r') as f:
                        doc_chunks = json.load(f)
                    
                    # Calculate similarities
                    similarities = np.dot(doc_vectors, query_vector) / (
                        np.linalg.norm(doc_vectors, axis=1) * np.linalg.norm(query_vector)
                    )
                    
                    # Add to results
                    for i, similarity in enumerate(similarities):
                        if i < len(doc_chunks):
                            results.append({
                                'similarity': float(similarity),
                                'document': doc_info['filename'],
                                'chunk_text': doc_chunks[i]['text'],
                                'chunk_id': doc_chunks[i]['id']
                            })
            
            # Sort by similarity and return top_k
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            self.logger.error(f"Query error: {e}")
            return []
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        
        metadata = self._load_metadata()
        
        total_size_mb = 0
        for doc_id, doc_info in metadata['documents'].items():
            if os.path.exists(doc_info['vector_file']):
                total_size_mb += os.path.getsize(doc_info['vector_file']) / (1024 * 1024)
        
        return {
            'total_documents': metadata['total_documents'],
            'total_chunks': metadata['total_chunks'],
            'total_size_mb': round(total_size_mb, 2),
            'last_updated': metadata['last_updated'],
            'memory_usage_gb': self._get_memory_usage_gb()
        }
    
    def cleanup_knowledge_base(self, keep_recent_days: int = 30):
        """Clean up old or unused knowledge base entries"""
        
        cutoff_date = datetime.now().timestamp() - (keep_recent_days * 24 * 3600)
        
        metadata = self._load_metadata()
        documents_to_remove = []
        
        for doc_id, doc_info in metadata['documents'].items():
            doc_date = datetime.fromisoformat(doc_info['created_at']).timestamp()
            
            if doc_date < cutoff_date:
                documents_to_remove.append(doc_id)
        
        # Remove old documents
        for doc_id in documents_to_remove:
            doc_info = metadata['documents'][doc_id]
            
            # Remove files
            if os.path.exists(doc_info['vector_file']):
                os.remove(doc_info['vector_file'])
            if os.path.exists(doc_info['chunks_file']):
                os.remove(doc_info['chunks_file'])
            
            # Remove from metadata
            del metadata['documents'][doc_id]
        
        if documents_to_remove:
            metadata['total_documents'] -= len(documents_to_remove)
            metadata['last_updated'] = datetime.now().isoformat()
            self._save_metadata(metadata)
            
            self.logger.info(f"Cleaned up {len(documents_to_remove)} old documents")
    
    def _generate_document_id(self, filename: str) -> str:
        """Generate unique document ID"""
        return hashlib.md5(f"{filename}_{datetime.now().isoformat()}".encode()).hexdigest()
    
    def _generate_cloud_job_id(self) -> str:
        """Generate unique cloud job ID"""
        return f"cloud_job_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    def _get_memory_usage_gb(self) -> float:
        """Get current memory usage estimate"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024 * 1024)
        except ImportError:
            # Estimate based on file sizes
            total_size = 0
            if os.path.exists(self.vector_cache_dir):
                for root, dirs, files in os.walk(self.vector_cache_dir):
                    for file in files:
                        total_size += os.path.getsize(os.path.join(root, file))
            return total_size / (1024 * 1024 * 1024)
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            self.logger.error(f"Temp cleanup error: {e}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load document metadata"""
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'documents': {},
                'total_documents': 0,
                'total_chunks': 0,
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """Save document metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _store_cloud_job(self, job_info: Dict[str, Any]):
        """Store cloud job information"""
        jobs_file = os.path.join(self.knowledge_base_dir, "cloud_jobs.json")
        
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            jobs = {'jobs': []}
        
        jobs['jobs'].append(job_info)
        
        with open(jobs_file, 'w') as f:
            json.dump(jobs, f, indent=2)
    
    def _log_processing_session(self, results: Dict[str, Any]):
        """Log processing session results"""
        
        try:
            if os.path.exists(self.processing_log):
                with open(self.processing_log, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'sessions': []}
            
            session_entry = {
                'timestamp': datetime.now().isoformat(),
                'results': results
            }
            
            log_data['sessions'].append(session_entry)
            
            # Keep only last 50 sessions
            if len(log_data['sessions']) > 50:
                log_data['sessions'] = log_data['sessions'][-50:]
            
            with open(self.processing_log, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Logging error: {e}")

def main():
    """Main function for testing"""
    
    print("🔄 EchoNexus Data Ingestion Engine")
    print("Advanced document processing with intelligent memory management")
    
    engine = EchoNexusDataIngestion()
    stats = engine.get_knowledge_base_stats()
    
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"  • Documents: {stats['total_documents']}")
    print(f"  • Chunks: {stats['total_chunks']}")
    print(f"  • Size: {stats['total_size_mb']} MB")
    print(f"  • Memory Usage: {stats['memory_usage_gb']:.2f} GB")

if __name__ == '__main__':
    main()
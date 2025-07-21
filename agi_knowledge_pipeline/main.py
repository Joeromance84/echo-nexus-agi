#!/usr/bin/env python3
"""
AGI Knowledge Ingestion Pipeline
Event-driven automated processing of PDFs and EPUBs for AGI consumption
"""

import functions_framework
import json
import os
import tempfile
from datetime import datetime
from google.cloud import storage
from google.cloud import aiplatform
from google.cloud import logging as cloud_logging
import fitz  # PyMuPDF for PDF processing
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import hashlib
from typing import List, Dict, Any

# Initialize Google Cloud clients
storage_client = storage.Client()
logging_client = cloud_logging.Client()
logging_client.setup_logging()

# Configuration
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')
REGION = os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', f'{PROJECT_ID}-agi-processed')
VECTOR_INDEX_ID = os.environ.get('VECTOR_INDEX_ID')
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '200'))

# Initialize Vertex AI
if PROJECT_ID:
    aiplatform.init(project=PROJECT_ID, location=REGION)

class AGIKnowledgeProcessor:
    """Advanced processor for converting documents into AGI-accessible knowledge"""
    
    def __init__(self):
        self.embedding_model = None
        self.processed_files = set()
        self.processing_stats = {
            'files_processed': 0,
            'chunks_created': 0,
            'embeddings_generated': 0,
            'errors': 0
        }
    
    def initialize_embedding_model(self):
        """Initialize the text embedding model"""
        try:
            from vertexai.language_models import TextEmbeddingModel
            self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
            print("✅ Embedding model initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️ Failed to initialize embedding model: {e}")
            return False
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            text_content = ""
            with fitz.open(file_path) as doc:
                for page_num, page in enumerate(doc):
                    page_text = page.get_text()
                    if page_text.strip():
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            print(f"📄 Extracted {len(text_content)} characters from PDF")
            return text_content
            
        except Exception as e:
            print(f"❌ Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_epub(self, file_path: str) -> str:
        """Extract text content from EPUB file"""
        try:
            text_content = ""
            book = epub.read_epub(file_path)
            
            # Extract metadata
            title = book.get_metadata('DC', 'title')
            creator = book.get_metadata('DC', 'creator')
            
            if title:
                text_content += f"Title: {title[0][0]}\n"
            if creator:
                text_content += f"Author: {creator[0][0]}\n"
            text_content += "\n" + "="*50 + "\n\n"
            
            # Extract text from chapters
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    chapter_text = soup.get_text()
                    if chapter_text.strip():
                        text_content += f"{chapter_text}\n\n"
            
            print(f"📚 Extracted {len(text_content)} characters from EPUB")
            return text_content
            
        except Exception as e:
            print(f"❌ Error extracting EPUB text: {e}")
            return ""
    
    def intelligent_chunking(self, text: str, file_name: str) -> List[Dict[str, Any]]:
        """Advanced text chunking with context preservation"""
        chunks = []
        
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split by natural boundaries (paragraphs, sections)
        sections = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        chunk_id = 0
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Check if adding this section would exceed chunk size
            if len(current_chunk) + len(section) + 1 > CHUNK_SIZE:
                if current_chunk:
                    # Save current chunk
                    chunks.append({
                        'id': f"{file_name}_{chunk_id}",
                        'text': current_chunk.strip(),
                        'source_file': file_name,
                        'chunk_index': chunk_id,
                        'character_count': len(current_chunk),
                        'created_at': datetime.now().isoformat()
                    })
                    chunk_id += 1
                
                # Start new chunk with overlap if needed
                if len(current_chunk) > CHUNK_OVERLAP:
                    overlap_text = current_chunk[-CHUNK_OVERLAP:]
                    current_chunk = overlap_text + " " + section
                else:
                    current_chunk = section
            else:
                # Add section to current chunk
                if current_chunk:
                    current_chunk += " " + section
                else:
                    current_chunk = section
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                'id': f"{file_name}_{chunk_id}",
                'text': current_chunk.strip(),
                'source_file': file_name,
                'chunk_index': chunk_id,
                'character_count': len(current_chunk),
                'created_at': datetime.now().isoformat()
            })
        
        print(f"📝 Created {len(chunks)} intelligent chunks")
        return chunks
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate vector embeddings for text chunks"""
        if not self.embedding_model:
            print("⚠️ Embedding model not initialized")
            return chunks
        
        try:
            enriched_chunks = []
            batch_size = 100  # Process in batches for efficiency
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                texts = [chunk['text'] for chunk in batch]
                
                # Generate embeddings
                embeddings = self.embedding_model.get_embeddings(texts)
                
                # Enrich chunks with embeddings
                for j, chunk in enumerate(batch):
                    if j < len(embeddings):
                        chunk['embedding'] = embeddings[j].values
                        chunk['embedding_model'] = "textembedding-gecko@003"
                        chunk['embedding_dimensions'] = len(embeddings[j].values)
                    enriched_chunks.append(chunk)
                
                print(f"🧠 Generated embeddings for batch {i//batch_size + 1}")
            
            self.processing_stats['embeddings_generated'] += len(enriched_chunks)
            return enriched_chunks
            
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            self.processing_stats['errors'] += 1
            return chunks
    
    def store_processed_data(self, chunks: List[Dict[str, Any]], original_file_name: str):
        """Store processed chunks in Cloud Storage"""
        try:
            # Create processed data structure
            processed_data = {
                'metadata': {
                    'original_file': original_file_name,
                    'processing_timestamp': datetime.now().isoformat(),
                    'total_chunks': len(chunks),
                    'processor_version': '1.0',
                    'chunk_size': CHUNK_SIZE,
                    'chunk_overlap': CHUNK_OVERLAP
                },
                'chunks': chunks,
                'statistics': {
                    'total_characters': sum(chunk['character_count'] for chunk in chunks),
                    'embeddings_generated': len([c for c in chunks if 'embedding' in c]),
                    'average_chunk_size': sum(chunk['character_count'] for chunk in chunks) / len(chunks) if chunks else 0
                }
            }
            
            # Upload to processed bucket
            bucket = storage_client.bucket(PROCESSED_BUCKET)
            
            # Generate unique filename
            file_hash = hashlib.md5(original_file_name.encode()).hexdigest()[:8]
            processed_filename = f"processed/{datetime.now().strftime('%Y/%m/%d')}/{file_hash}_{original_file_name}.json"
            
            blob = bucket.blob(processed_filename)
            blob.upload_from_string(
                json.dumps(processed_data, indent=2),
                content_type='application/json'
            )
            
            print(f"💾 Stored processed data: gs://{PROCESSED_BUCKET}/{processed_filename}")
            
            # Update AGI knowledge index
            self.update_agi_knowledge_index(chunks, original_file_name)
            
        except Exception as e:
            print(f"❌ Error storing processed data: {e}")
            self.processing_stats['errors'] += 1
    
    def update_agi_knowledge_index(self, chunks: List[Dict[str, Any]], source_file: str):
        """Update the AGI knowledge index with new chunks"""
        try:
            # Create knowledge index entry
            index_entry = {
                'source_file': source_file,
                'chunk_count': len(chunks),
                'processing_timestamp': datetime.now().isoformat(),
                'status': 'indexed',
                'chunks': [
                    {
                        'id': chunk['id'],
                        'text_preview': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                        'character_count': chunk['character_count'],
                        'has_embedding': 'embedding' in chunk
                    }
                    for chunk in chunks
                ]
            }
            
            # Store in AGI knowledge index
            bucket = storage_client.bucket(PROCESSED_BUCKET)
            index_blob = bucket.blob(f"agi_knowledge_index/{source_file}_index.json")
            index_blob.upload_from_string(
                json.dumps(index_entry, indent=2),
                content_type='application/json'
            )
            
            print(f"🧠 Updated AGI knowledge index for {source_file}")
            
        except Exception as e:
            print(f"⚠️ Error updating AGI knowledge index: {e}")
    
    def process_file(self, bucket_name: str, file_name: str) -> bool:
        """Main file processing pipeline"""
        try:
            print(f"🚀 Starting AGI knowledge processing for: {file_name}")
            
            # Download file
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
                blob.download_to_filename(temp_file.name)
                temp_file_path = temp_file.name
            
            # Extract text based on file type
            text_content = ""
            if file_name.lower().endswith('.pdf'):
                text_content = self.extract_text_from_pdf(temp_file_path)
            elif file_name.lower().endswith('.epub'):
                text_content = self.extract_text_from_epub(temp_file_path)
            else:
                print(f"⚠️ Unsupported file type: {file_name}")
                return False
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            if not text_content.strip():
                print(f"⚠️ No text content extracted from {file_name}")
                return False
            
            # Create intelligent chunks
            chunks = self.intelligent_chunking(text_content, file_name)
            
            if not chunks:
                print(f"⚠️ No chunks created from {file_name}")
                return False
            
            # Generate embeddings
            if self.initialize_embedding_model():
                chunks = self.generate_embeddings(chunks)
            
            # Store processed data
            self.store_processed_data(chunks, file_name)
            
            # Update statistics
            self.processing_stats['files_processed'] += 1
            self.processing_stats['chunks_created'] += len(chunks)
            
            print(f"✅ Successfully processed {file_name}")
            print(f"📊 Stats: {self.processing_stats}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
            self.processing_stats['errors'] += 1
            return False

# Global processor instance
processor = AGIKnowledgeProcessor()

@functions_framework.cloud_event
def agi_knowledge_ingestion(cloud_event):
    """
    AGI Knowledge Ingestion Cloud Function
    Triggered by file uploads to process documents for AGI consumption
    """
    try:
        # Parse the event
        data = cloud_event.data
        bucket_name = data['bucket']
        file_name = data['name']
        event_type = data.get('eventType', 'unknown')
        
        print(f"🎯 AGI Knowledge Ingestion Triggered")
        print(f"📁 Bucket: {bucket_name}")
        print(f"📄 File: {file_name}")
        print(f"🔄 Event: {event_type}")
        
        # Only process creation events
        if 'finalize' not in event_type.lower() and 'create' not in event_type.lower():
            print(f"⏭️ Ignoring event type: {event_type}")
            return
        
        # Filter supported file types
        if not (file_name.lower().endswith('.pdf') or file_name.lower().endswith('.epub')):
            print(f"⏭️ Skipping unsupported file type: {file_name}")
            return
        
        # Process the file
        success = processor.process_file(bucket_name, file_name)
        
        if success:
            print(f"🎉 AGI knowledge successfully ingested from {file_name}")
            
            # Log success for monitoring
            print(json.dumps({
                'event': 'agi_knowledge_ingestion_success',
                'file': file_name,
                'bucket': bucket_name,
                'timestamp': datetime.now().isoformat(),
                'stats': processor.processing_stats
            }))
        else:
            print(f"💥 AGI knowledge ingestion failed for {file_name}")
            
            # Log failure for monitoring
            print(json.dumps({
                'event': 'agi_knowledge_ingestion_failure',
                'file': file_name,
                'bucket': bucket_name,
                'timestamp': datetime.now().isoformat(),
                'stats': processor.processing_stats
            }))
    
    except Exception as e:
        print(f"💥 Critical error in AGI knowledge ingestion: {e}")
        print(json.dumps({
            'event': 'agi_knowledge_ingestion_critical_error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }))

if __name__ == "__main__":
    # Local testing functionality
    print("🧪 AGI Knowledge Pipeline - Local Testing Mode")
    print("This function is designed to run in Google Cloud Functions")
    print("For local testing, implement test scenarios here")
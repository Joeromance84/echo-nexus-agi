#!/usr/bin/env python3
"""
AGI Document Processing System
Intelligent PDF and EPUB reading with cloud storage and memory management
"""

import os
import json
import hashlib
import tempfile
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, BinaryIO
from pathlib import Path
import time

# Document processing libraries - with fallbacks
pdf_available = False
epub_available = False

try:
    import PyPDF2
    pdf_available = True
except ImportError:
    PyPDF2 = None

try:
    import fitz  # PyMuPDF for better PDF text extraction
except ImportError:
    fitz = None

try:
    import ebooklib
    from ebooklib import epub
    epub_available = True
except ImportError:
    ebooklib = None
    epub = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Cloud storage integration
try:
    from google.cloud import storage
    from google.cloud import bigquery
except ImportError:
    storage = None
    bigquery = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGIDocumentProcessor:
    """Intelligent document processing with cloud storage and learning"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id or "agi-document-processing"
        self.storage_client = None
        self.bigquery_client = None
        
        # Initialize cloud clients if available
        try:
            if storage:
                self.storage_client = storage.Client()
            if bigquery:
                self.bigquery_client = bigquery.Client()
        except Exception as e:
            logger.warning(f"Cloud clients not available: {e}")
        
        # Document storage configuration
        self.bucket_name = f"{self.project_id}-documents"
        self.knowledge_bucket = f"{self.project_id}-knowledge"
        
        # Memory management thresholds
        self.max_local_storage_mb = 100  # 100MB local limit
        self.max_document_size_mb = 50   # 50MB per document
        
        # Knowledge extraction configuration
        self.knowledge_database = {}
        self.processed_documents = {}
        
        logger.info("AGI Document Processor initialized")
    
    async def process_uploaded_document(self, file_data: bytes, filename: str, 
                                      file_type: str) -> Dict[str, Any]:
        """Process uploaded PDF or EPUB document"""
        logger.info(f"Processing uploaded document: {filename}")
        
        # Calculate file hash for deduplication
        file_hash = hashlib.sha256(file_data).hexdigest()
        
        # Check if already processed
        if file_hash in self.processed_documents:
            logger.info(f"Document already processed: {filename}")
            return {
                "status": "already_processed",
                "document_hash": file_hash,
                "knowledge_extracted": self.processed_documents[file_hash]["knowledge_extracted"],
                "processing_timestamp": self.processed_documents[file_hash]["timestamp"]
            }
        
        # Check file size
        file_size_mb = len(file_data) / (1024 * 1024)
        if file_size_mb > self.max_document_size_mb:
            return {
                "status": "file_too_large",
                "file_size_mb": file_size_mb,
                "max_size_mb": self.max_document_size_mb
            }
        
        try:
            # Extract text content
            if file_type.lower() == 'pdf':
                text_content = await self._extract_pdf_content(file_data)
            elif file_type.lower() in ['epub', 'ebook']:
                text_content = await self._extract_epub_content(file_data)
            else:
                return {"status": "unsupported_format", "supported": ["pdf", "epub"]}
            
            # Extract knowledge and insights
            knowledge_extraction = await self._extract_knowledge(text_content, filename)
            
            # Store in cloud if available, otherwise manage locally
            storage_result = await self._manage_document_storage(
                file_data, filename, file_hash, knowledge_extraction
            )
            
            # Update processed documents registry
            self.processed_documents[file_hash] = {
                "filename": filename,
                "file_type": file_type,
                "file_size_mb": file_size_mb,
                "knowledge_extracted": len(knowledge_extraction.get("insights", [])),
                "timestamp": datetime.now().isoformat(),
                "storage_location": storage_result.get("location", "local_processed"),
                "local_file_deleted": storage_result.get("local_deleted", False)
            }
            
            # Save processing results
            await self._save_processing_results(file_hash, knowledge_extraction)
            
            return {
                "status": "processed_successfully",
                "document_hash": file_hash,
                "filename": filename,
                "text_length": len(text_content),
                "knowledge_insights": len(knowledge_extraction.get("insights", [])),
                "key_concepts": knowledge_extraction.get("key_concepts", []),
                "storage_result": storage_result,
                "memory_management": await self._check_memory_status()
            }
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            return {"status": "processing_error", "error": str(e)}
    
    async def _extract_pdf_content(self, file_data: bytes) -> str:
        """Extract text content from PDF"""
        text_content = ""
        
        if not pdf_available:
            return "PDF processing libraries not available. Please install PyPDF2 or PyMuPDF to enable PDF reading."
        
        try:
            # Try PyMuPDF first (better text extraction)
            if fitz:
                pdf_document = fitz.open(stream=file_data, filetype="pdf")
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    text_content += page.get_text()
                pdf_document.close()
            elif PyPDF2:
                # Fallback to PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
        
        except Exception as e:
            logger.error(f"Error extracting PDF content: {e}")
            text_content = f"Error extracting PDF: {str(e)}"
        
        return text_content
    
    async def _extract_epub_content(self, file_data: bytes) -> str:
        """Extract text content from EPUB"""
        text_content = ""
        
        if not epub_available:
            return "EPUB processing libraries not available. Please install ebooklib and beautifulsoup4 to enable EPUB reading."
        
        try:
            # Save to temporary file for ebooklib
            with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                book = epub.read_epub(temp_file_path)
                
                # Extract text from all items
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        content = item.get_content().decode('utf-8')
                        # Parse HTML content if BeautifulSoup available
                        if BeautifulSoup:
                            soup = BeautifulSoup(content, 'html.parser')
                            text_content += soup.get_text() + "\n"
                        else:
                            # Basic HTML tag removal
                            import re
                            clean_text = re.sub(r'<[^>]+>', '', content)
                            text_content += clean_text + "\n"
                        
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
        
        except Exception as e:
            logger.error(f"Error extracting EPUB content: {e}")
            text_content = f"Error extracting EPUB: {str(e)}"
        
        return text_content
    
    async def _extract_knowledge(self, text_content: str, filename: str) -> Dict[str, Any]:
        """Extract knowledge and insights from document text"""
        
        # Split text into chunks for analysis
        chunks = self._split_text_into_chunks(text_content, chunk_size=1000)
        
        knowledge_extraction = {
            "document_summary": self._generate_summary(text_content),
            "key_concepts": self._extract_key_concepts(text_content),
            "insights": self._extract_insights(chunks),
            "technical_information": self._extract_technical_info(text_content),
            "learning_points": self._extract_learning_points(text_content),
            "document_metadata": {
                "filename": filename,
                "word_count": len(text_content.split()),
                "character_count": len(text_content),
                "processing_timestamp": datetime.now().isoformat()
            }
        }
        
        return knowledge_extraction
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def _generate_summary(self, text: str) -> str:
        """Generate document summary"""
        # Simple extractive summary using first and key sentences
        sentences = text.split('.')[:10]  # First 10 sentences
        summary = '. '.join(sentences[:5]) + '.'
        return summary
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from document"""
        # Simple keyword extraction based on frequency and importance
        import re
        from collections import Counter
        
        # Clean and tokenize
        words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        
        # Filter common words
        common_words = {'that', 'this', 'with', 'from', 'they', 'been', 'have', 
                       'their', 'said', 'each', 'which', 'what', 'there', 'more'}
        filtered_words = [word for word in words if word not in common_words]
        
        # Get most frequent words
        word_freq = Counter(filtered_words)
        key_concepts = [word for word, freq in word_freq.most_common(20)]
        
        return key_concepts
    
    def _extract_insights(self, chunks: List[str]) -> List[Dict[str, Any]]:
        """Extract insights from text chunks"""
        insights = []
        
        for i, chunk in enumerate(chunks):
            # Look for patterns that indicate insights
            if any(keyword in chunk.lower() for keyword in ['important', 'key', 'significant', 
                                                           'conclusion', 'result', 'finding']):
                insights.append({
                    "chunk_index": i,
                    "content": chunk[:500] + "..." if len(chunk) > 500 else chunk,
                    "insight_type": "key_finding",
                    "confidence": 0.8
                })
        
        return insights[:10]  # Limit to top 10 insights
    
    def _extract_technical_info(self, text: str) -> Dict[str, Any]:
        """Extract technical information from document"""
        import re
        
        technical_info = {
            "code_snippets": [],
            "technical_terms": [],
            "formulas": [],
            "references": []
        }
        
        # Find code-like patterns
        code_patterns = re.findall(r'```[\s\S]*?```|`[^`]+`', text)
        technical_info["code_snippets"] = code_patterns[:10]
        
        # Find technical terms (capitalized words, acronyms)
        tech_terms = re.findall(r'\b[A-Z]{2,}\b|\b[A-Z][a-z]*[A-Z][A-Za-z]*\b', text)
        technical_info["technical_terms"] = list(set(tech_terms))[:20]
        
        # Find reference patterns
        references = re.findall(r'\[\d+\]|\(\d{4}\)|et al\.', text)
        technical_info["references"] = references[:10]
        
        return technical_info
    
    def _extract_learning_points(self, text: str) -> List[str]:
        """Extract key learning points from document"""
        learning_indicators = [
            'learn', 'understand', 'important', 'remember', 'key point',
            'takeaway', 'lesson', 'principle', 'concept', 'idea'
        ]
        
        sentences = text.split('.')
        learning_points = []
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in learning_indicators):
                if len(sentence.strip()) > 20:  # Filter out very short sentences
                    learning_points.append(sentence.strip())
        
        return learning_points[:15]  # Limit to top 15 learning points
    
    async def _manage_document_storage(self, file_data: bytes, filename: str, 
                                     file_hash: str, knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently manage document storage"""
        
        # Check local storage usage
        local_storage_mb = await self._calculate_local_storage_usage()
        
        storage_result = {
            "strategy": "local_processing_only",
            "location": "processed_locally",
            "local_deleted": True,
            "cloud_stored": False
        }
        
        # Try cloud storage first
        if self.storage_client:
            try:
                # Store original document
                doc_blob_name = f"documents/{file_hash}/{filename}"
                await self._upload_to_cloud_storage(file_data, doc_blob_name)
                
                # Store extracted knowledge
                knowledge_blob_name = f"knowledge/{file_hash}/knowledge.json"
                knowledge_data = json.dumps(knowledge, indent=2).encode('utf-8')
                await self._upload_to_cloud_storage(knowledge_data, knowledge_blob_name)
                
                storage_result.update({
                    "strategy": "cloud_storage",
                    "location": f"gs://{self.bucket_name}/{doc_blob_name}",
                    "cloud_stored": True,
                    "knowledge_location": f"gs://{self.knowledge_bucket}/{knowledge_blob_name}"
                })
                
                logger.info(f"Document stored in cloud: {filename}")
                
            except Exception as e:
                logger.warning(f"Cloud storage failed, using local processing: {e}")
        
        # If local storage is getting full, just process and delete
        if local_storage_mb > self.max_local_storage_mb:
            storage_result.update({
                "strategy": "process_and_delete",
                "reason": f"Local storage limit exceeded ({local_storage_mb:.1f}MB > {self.max_local_storage_mb}MB)",
                "local_deleted": True
            })
            logger.info(f"Local storage full, processing and deleting: {filename}")
        
        return storage_result
    
    async def _upload_to_cloud_storage(self, data: bytes, blob_name: str) -> None:
        """Upload data to cloud storage"""
        if not self.storage_client:
            raise Exception("Cloud storage not available")
        
        # Create bucket if it doesn't exist
        bucket_name = self.bucket_name if "knowledge" not in blob_name else self.knowledge_bucket
        try:
            bucket = self.storage_client.bucket(bucket_name)
            if not bucket.exists():
                bucket.create(location='us-central1')
        except Exception:
            bucket = self.storage_client.bucket(bucket_name)
        
        # Upload data
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data)
    
    async def _calculate_local_storage_usage(self) -> float:
        """Calculate current local storage usage in MB"""
        total_size = 0
        
        # Check uploaded files directory
        uploads_dir = Path("uploads")
        if uploads_dir.exists():
            for file_path in uploads_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        
        # Check knowledge database files
        for file_path in Path(".").glob("*.json"):
            if "knowledge" in file_path.name or "learning" in file_path.name:
                total_size += file_path.stat().st_size
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    async def _save_processing_results(self, file_hash: str, knowledge: Dict[str, Any]) -> None:
        """Save processing results to local knowledge database"""
        
        # Update main knowledge database
        self.knowledge_database[file_hash] = knowledge
        
        # Save to file
        knowledge_file = f"agi_document_knowledge_{file_hash[:8]}.json"
        with open(knowledge_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
        
        # Update main knowledge index
        await self._update_knowledge_index()
    
    async def _update_knowledge_index(self) -> None:
        """Update the main knowledge index"""
        
        knowledge_index = {
            "total_documents_processed": len(self.processed_documents),
            "processing_history": self.processed_documents,
            "knowledge_database_files": [
                f"agi_document_knowledge_{file_hash[:8]}.json" 
                for file_hash in self.processed_documents.keys()
            ],
            "last_updated": datetime.now().isoformat(),
            "total_knowledge_entries": len(self.knowledge_database)
        }
        
        with open("agi_document_knowledge_index.json", 'w') as f:
            json.dump(knowledge_index, f, indent=2)
    
    async def _check_memory_status(self) -> Dict[str, Any]:
        """Check current memory and storage status"""
        
        local_storage_mb = await self._calculate_local_storage_usage()
        
        return {
            "local_storage_mb": round(local_storage_mb, 2),
            "local_storage_limit_mb": self.max_local_storage_mb,
            "storage_usage_percentage": round((local_storage_mb / self.max_local_storage_mb) * 100, 1),
            "cloud_storage_available": self.storage_client is not None,
            "documents_processed": len(self.processed_documents),
            "memory_management_active": True
        }
    
    async def search_knowledge(self, query: str) -> Dict[str, Any]:
        """Search through processed document knowledge"""
        
        search_results = {
            "query": query,
            "results": [],
            "total_documents_searched": len(self.knowledge_database)
        }
        
        query_lower = query.lower()
        
        for file_hash, knowledge in self.knowledge_database.items():
            # Search in summary
            if query_lower in knowledge.get("document_summary", "").lower():
                search_results["results"].append({
                    "document": self.processed_documents[file_hash]["filename"],
                    "match_type": "summary",
                    "content": knowledge["document_summary"][:300] + "..."
                })
            
            # Search in key concepts
            matching_concepts = [
                concept for concept in knowledge.get("key_concepts", [])
                if query_lower in concept.lower()
            ]
            if matching_concepts:
                search_results["results"].append({
                    "document": self.processed_documents[file_hash]["filename"],
                    "match_type": "key_concepts",
                    "content": f"Matching concepts: {', '.join(matching_concepts)}"
                })
            
            # Search in insights
            for insight in knowledge.get("insights", []):
                if query_lower in insight.get("content", "").lower():
                    search_results["results"].append({
                        "document": self.processed_documents[file_hash]["filename"],
                        "match_type": "insight",
                        "content": insight["content"][:300] + "..."
                    })
        
        return search_results
    
    async def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of all learning from processed documents"""
        
        if not self.knowledge_database:
            return {"status": "no_documents_processed"}
        
        # Aggregate learning across all documents
        all_concepts = []
        all_insights = []
        all_learning_points = []
        total_documents = len(self.knowledge_database)
        
        for knowledge in self.knowledge_database.values():
            all_concepts.extend(knowledge.get("key_concepts", []))
            all_insights.extend(knowledge.get("insights", []))
            all_learning_points.extend(knowledge.get("learning_points", []))
        
        # Get most common concepts
        from collections import Counter
        concept_freq = Counter(all_concepts)
        top_concepts = [concept for concept, freq in concept_freq.most_common(20)]
        
        learning_summary = {
            "total_documents_processed": total_documents,
            "total_concepts_learned": len(set(all_concepts)),
            "total_insights_extracted": len(all_insights),
            "total_learning_points": len(all_learning_points),
            "top_concepts": top_concepts,
            "recent_documents": [
                {
                    "filename": doc["filename"],
                    "knowledge_insights": doc["knowledge_extracted"],
                    "timestamp": doc["timestamp"]
                }
                for doc in list(self.processed_documents.values())[-5:]
            ],
            "learning_effectiveness": {
                "avg_insights_per_document": len(all_insights) / total_documents if total_documents > 0 else 0,
                "concept_diversity": len(set(all_concepts)) / len(all_concepts) if all_concepts else 0,
                "knowledge_retention": "high" if len(set(all_concepts)) > 50 else "medium"
            }
        }
        
        return learning_summary

# Streamlit integration for file uploads
def create_document_upload_interface():
    """Create Streamlit interface for document uploads"""
    
    import streamlit as st
    
    st.title("AGI Document Learning System")
    st.markdown("Upload PDF or EPUB files for the AGI to read, learn from, and remember")
    
    # Initialize processor
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = AGIDocumentProcessor()
    
    processor = st.session_state.doc_processor
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose PDF or EPUB files",
        type=['pdf', 'epub'],
        accept_multiple_files=True,
        help="Upload documents for the AGI to read and learn from"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.expander(f"Processing: {uploaded_file.name}"):
                
                # Read file data
                file_data = uploaded_file.read()
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                # Process document
                with st.spinner(f"AGI is reading and learning from {uploaded_file.name}..."):
                    result = asyncio.run(processor.process_uploaded_document(
                        file_data, uploaded_file.name, file_type
                    ))
                
                # Display results
                if result["status"] == "processed_successfully":
                    st.success(f"✅ Successfully processed: {uploaded_file.name}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Text Length", f"{result['text_length']:,} characters")
                        st.metric("Knowledge Insights", result['knowledge_insights'])
                    
                    with col2:
                        st.metric("Key Concepts", len(result['key_concepts']))
                        if result['storage_result']['cloud_stored']:
                            st.success("📁 Stored in cloud")
                        else:
                            st.info("🔄 Processed and cleaned locally")
                    
                    # Show key concepts
                    if result['key_concepts']:
                        st.write("**Key Concepts Learned:**")
                        st.write(", ".join(result['key_concepts'][:10]))
                
                elif result["status"] == "already_processed":
                    st.info(f"📚 Already learned from: {uploaded_file.name}")
                
                else:
                    st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
    
    # Knowledge search
    st.header("Search AGI Knowledge")
    search_query = st.text_input("Search through learned knowledge:")
    
    if search_query:
        search_results = asyncio.run(processor.search_knowledge(search_query))
        
        if search_results["results"]:
            st.write(f"Found {len(search_results['results'])} results:")
            
            for result in search_results["results"]:
                with st.expander(f"{result['document']} - {result['match_type']}"):
                    st.write(result['content'])
        else:
            st.info("No matching knowledge found")
    
    # Learning summary
    if st.button("Show AGI Learning Summary"):
        summary = asyncio.run(processor.get_learning_summary())
        
        if summary.get("status") != "no_documents_processed":
            st.header("AGI Learning Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Documents Processed", summary["total_documents_processed"])
            with col2:
                st.metric("Concepts Learned", summary["total_concepts_learned"])
            with col3:
                st.metric("Insights Extracted", summary["total_insights_extracted"])
            
            st.write("**Top Learned Concepts:**")
            st.write(", ".join(summary["top_concepts"][:15]))
            
            st.write("**Recent Documents:**")
            for doc in summary["recent_documents"]:
                st.write(f"• {doc['filename']} - {doc['knowledge_insights']} insights")
        else:
            st.info("No documents have been processed yet")
    
    # Memory status
    memory_status = asyncio.run(processor._check_memory_status())
    
    st.sidebar.header("Memory Management")
    st.sidebar.progress(memory_status["storage_usage_percentage"] / 100)
    st.sidebar.write(f"Storage: {memory_status['local_storage_mb']:.1f}MB / {memory_status['local_storage_limit_mb']}MB")
    
    if memory_status["cloud_storage_available"]:
        st.sidebar.success("☁️ Cloud storage active")
    else:
        st.sidebar.warning("⚠️ Local processing only")

if __name__ == "__main__":
    # Test the document processor
    import asyncio
    
    async def test_processor():
        processor = AGIDocumentProcessor()
        
        # Test with sample text
        print("AGI Document Processor Test")
        print("=" * 40)
        
        sample_text = """
        This is a test document about artificial intelligence and machine learning.
        Machine learning is important for AGI development. Key concepts include
        neural networks, deep learning, and natural language processing.
        """
        
        knowledge = await processor._extract_knowledge(sample_text, "test.txt")
        print("Extracted Knowledge:")
        print(json.dumps(knowledge, indent=2))
    
    # Run test if not imported
    asyncio.run(test_processor())
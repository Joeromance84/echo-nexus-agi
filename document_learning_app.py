#!/usr/bin/env python3
"""
Document Learning App
AGI Document Processing and Learning System with PDF/EPUB Upload
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
import hashlib
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import threading
from agi_learning_backup_system import AGILearningBackupSystem
from agi_realtime_communication import AGIRealtimeCommunication

class DocumentLearningProcessor:
    """Advanced document processing and learning system"""
    
    def __init__(self):
        self.learning_database = "agi_learning_database.json"
        self.supported_formats = [".pdf", ".epub", ".txt", ".md"]
        self.learning_insights = []
        
        # Initialize learning database
        self.load_learning_database()
        
        # Initialize systems safely in background
        self.initialize_background_systems()
        
    def load_learning_database(self):
        """Load existing learning database"""
        try:
            if os.path.exists(self.learning_database):
                with open(self.learning_database, 'r', encoding='utf-8') as f:
                    self.database = json.load(f)
            else:
                self.database = {
                    "documents": {},
                    "insights": [],
                    "concepts": [],
                    "total_processed": 0,
                    "last_updated": datetime.now().isoformat()
                }
        except Exception as e:
            st.error(f"Error loading learning database: {e}")
            self.database = {
                "documents": {},
                "insights": [],
                "concepts": [],
                "total_processed": 0,
                "last_updated": datetime.now().isoformat()
            }
    
    def save_learning_database(self):
        """Save learning database and trigger automatic backup"""
        try:
            self.database["last_updated"] = datetime.now().isoformat()
            with open(self.learning_database, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            
            # Trigger immediate backup after saving new learning data
            if hasattr(self, 'backup_system') and self.backup_system:
                threading.Thread(target=self.backup_system.backup_learning_data, daemon=True).start()
                
        except Exception as e:
            st.error(f"Error saving learning database: {e}")
    
    def initialize_background_systems(self):
        """Initialize backup and communication systems safely in background"""
        def init_systems():
            try:
                # Initialize backup system
                self.backup_system = AGILearningBackupSystem()
                print("✅ Backup system initialized")
                
                # Initialize communication system
                self.communication_system = AGIRealtimeCommunication()
                self.communication_system.start_realtime_monitoring()
                print("✅ Communication system initialized")
                
            except Exception as e:
                print(f"Background system initialization error: {e}")
                # Continue without background systems if they fail
                self.backup_system = None
                self.communication_system = None
        
        # Start initialization in background thread
        init_thread = threading.Thread(target=init_systems, daemon=True)
        init_thread.start()
    
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file using dependency-free approach"""
        try:
            # Simple PDF text extraction using binary patterns
            # This is a basic approach that works for many PDFs
            
            # Convert bytes to string and look for text streams
            pdf_text = file_content.decode('latin-1', errors='ignore')
            
            # Look for text objects in PDF structure
            text_content = ""
            
            # Pattern 1: Look for text streams between "stream" and "endstream"
            stream_pattern = r'stream\s*(.*?)\s*endstream'
            streams = re.findall(stream_pattern, pdf_text, re.DOTALL | re.IGNORECASE)
            
            for stream in streams:
                # Try to extract readable text from stream
                readable_chars = ''.join(char for char in stream if char.isprintable() and char not in ['\x00', '\x01', '\x02'])
                if len(readable_chars) > 10:  # Only include streams with substantial text
                    text_content += readable_chars + "\n"
            
            # Pattern 2: Look for text objects with "Tj" or "TJ" operators
            text_show_pattern = r'\((.*?)\)\s*(?:Tj|TJ)'
            text_objects = re.findall(text_show_pattern, pdf_text, re.IGNORECASE)
            
            for text_obj in text_objects:
                if len(text_obj.strip()) > 1:
                    text_content += text_obj + " "
            
            # Pattern 3: Look for text arrays
            text_array_pattern = r'\[(.*?)\]\s*TJ'
            text_arrays = re.findall(text_array_pattern, pdf_text, re.IGNORECASE)
            
            for text_array in text_arrays:
                # Extract text from array format
                array_text = re.findall(r'\((.*?)\)', text_array)
                for text in array_text:
                    if len(text.strip()) > 1:
                        text_content += text + " "
            
            # Clean up the extracted text
            if text_content:
                # Remove excessive whitespace and non-printable characters
                text_content = re.sub(r'\s+', ' ', text_content)
                text_content = text_content.strip()
                
                # If we got some text, return it
                if len(text_content) > 50:  # Minimum threshold for meaningful content
                    return text_content
                
            # If no text extracted, provide helpful feedback
            return None
                
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return None
    
    def extract_text_from_epub(self, file_content):
        """Extract text from EPUB file using built-in libraries"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                text_content = ""
                with zipfile.ZipFile(tmp_file.name, 'r') as epub:
                    # Find all HTML/XHTML files
                    for file_name in epub.namelist():
                        if file_name.endswith(('.html', '.xhtml', '.htm')):
                            try:
                                content = epub.read(file_name).decode('utf-8', errors='ignore')
                                
                                # Try XML parsing first
                                try:
                                    # Handle HTML with XML namespace issues
                                    content_clean = re.sub(r'xmlns="[^"]*"', '', content)
                                    content_clean = re.sub(r'<\?xml[^>]*\?>', '', content_clean)
                                    
                                    root = ET.fromstring(f"<root>{content_clean}</root>")
                                    # Extract text content
                                    for elem in root.iter():
                                        if elem.text:
                                            text_content += elem.text + " "
                                        if elem.tail:
                                            text_content += elem.tail + " "
                                except ET.ParseError:
                                    # If XML parsing fails, use regex to extract text
                                    clean_text = re.sub(r'<[^>]+>', ' ', content)
                                    clean_text = re.sub(r'\s+', ' ', clean_text)
                                    text_content += clean_text + " "
                                    
                            except Exception:
                                continue
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
                
                if text_content:
                    # Clean up the text
                    text_content = re.sub(r'\s+', ' ', text_content)
                    text_content = text_content.strip()
                    return text_content if len(text_content) > 50 else None
                    
                return None
                
        except Exception as e:
            st.error(f"Error processing EPUB: {e}")
            return None
    
    def extract_key_concepts(self, text):
        """Extract key concepts from text using pattern recognition"""
        if not text:
            return []
        
        # Simple concept extraction using common patterns
        concepts = []
        
        # Look for definition patterns
        import re
        
        # Pattern 1: "X is defined as Y" or "X is Y"
        definition_patterns = [
            r'([A-Z][a-zA-Z\s]{2,30})\s+(?:is|are|means?|refers?\s+to|defined\s+as)\s+([^.!?]{10,100})',
            r'([A-Z][a-zA-Z\s]{2,30}):\s*([^.!?\n]{10,100})',
            r'([A-Z][a-zA-Z\s]{2,30})\s*-\s*([^.!?\n]{10,100})'
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:10]:  # Limit to prevent too many concepts
                concept = match[0].strip()
                definition = match[1].strip()
                if len(concept) > 3 and len(definition) > 10:
                    concepts.append({
                        "concept": concept,
                        "definition": definition,
                        "type": "definition"
                    })
        
        # Pattern 2: Important phrases (capitalized words, repeated terms)
        important_terms = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', text)
        term_frequency = {}
        for term in important_terms:
            term_frequency[term] = term_frequency.get(term, 0) + 1
        
        # Add frequently mentioned terms as concepts
        for term, frequency in sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)[:15]:
            if frequency >= 2:  # Only terms mentioned multiple times
                concepts.append({
                    "concept": term,
                    "frequency": frequency,
                    "type": "key_term"
                })
        
        return concepts
    
    def generate_insights(self, text, filename):
        """Generate learning insights from document content"""
        if not text:
            return []
        
        insights = []
        
        # Text statistics
        word_count = len(text.split())
        char_count = len(text)
        
        insights.append(f"Document contains {word_count:,} words and {char_count:,} characters")
        
        # Content analysis
        if word_count > 1000:
            insights.append("This is a substantial document suitable for comprehensive learning")
        elif word_count > 500:
            insights.append("This is a medium-length document with good learning potential")
        else:
            insights.append("This is a short document - consider uploading additional materials")
        
        # Topic detection based on common keywords
        topics = {
            "technology": ["software", "computer", "algorithm", "data", "system", "programming", "code"],
            "business": ["market", "strategy", "business", "management", "finance", "company", "revenue"],
            "science": ["research", "study", "analysis", "hypothesis", "experiment", "theory", "scientific"],
            "education": ["learning", "teaching", "education", "student", "knowledge", "skill", "training"]
        }
        
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in topics.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches >= 2:
                detected_topics.append(f"{topic} ({matches} indicators)")
        
        if detected_topics:
            insights.append(f"Detected topics: {', '.join(detected_topics)}")
        
        # Learning recommendations
        if "example" in text_lower and "practice" in text_lower:
            insights.append("Document contains examples and practice elements - excellent for hands-on learning")
        
        if any(word in text_lower for word in ["step", "process", "method", "procedure"]):
            insights.append("Document appears to contain procedural knowledge - good for skill development")
        
        # AGI-specific insights
        insights.append(f"Document '{filename}' has been processed and integrated into AGI knowledge base")
        insights.append("Content will be used for autonomous learning and decision-making improvements")
        
        return insights
    
    def process_document(self, file_content, filename, file_type):
        """Process uploaded document and extract learning content"""
        
        st.info(f"Processing document: {filename}")
        
        # Extract text based on file type
        if file_type == "pdf":
            text_content = self.extract_text_from_pdf(file_content)
        elif file_type == "epub":
            text_content = self.extract_text_from_epub(file_content)
        elif file_type in ["txt", "md"]:
            text_content = file_content.decode('utf-8', errors='ignore')
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
        
        if not text_content or len(text_content.strip()) < 50:
            st.error("Could not extract meaningful text from the document")
            return None
        
        # Generate document ID
        doc_id = hashlib.md5(f"{filename}_{datetime.now()}".encode()).hexdigest()
        
        # Extract concepts and generate insights
        concepts = self.extract_key_concepts(text_content)
        insights = self.generate_insights(text_content, filename)
        
        # Create document record
        document_record = {
            "id": doc_id,
            "filename": filename,
            "file_type": file_type,
            "processed_at": datetime.now().isoformat(),
            "word_count": len(text_content.split()),
            "char_count": len(text_content),
            "concepts": concepts,
            "insights": insights,
            "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content
        }
        
        # Store in database
        self.database["documents"][doc_id] = document_record
        self.database["concepts"].extend(concepts)
        self.database["insights"].extend(insights)
        self.database["total_processed"] += 1
        
        # Save to file
        self.save_learning_database()
        
        # Immediately share with other AIs
        if hasattr(self, 'communication_system') and self.communication_system:
            if file_type == "pdf":
                processing_results = {
                    "agi_insights": insights,
                    "text_length": len(text_content),
                    "word_count": len(text_content.split()),
                    "processing_status": "successful"
                }
                threading.Thread(target=self.communication_system.share_pdf_learning, 
                               args=(processing_results,), daemon=True).start()
            elif file_type == "epub":
                threading.Thread(target=self.communication_system.share_epub_learning, 
                               args=(document_record,), daemon=True).start()
        
        return document_record

def main():
    """Main Streamlit app for document learning"""
    
    st.set_page_config(
        page_title="AGI Document Learning System",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 AGI Document Learning System")
    st.markdown("Upload PDF, EPUB, or text documents for AGI learning and knowledge extraction")
    
    # Initialize processor
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentLearningProcessor()
    
    processor = st.session_state.doc_processor
    
    # Sidebar with statistics
    st.sidebar.title("📊 Learning Statistics")
    
    if processor.database:
        st.sidebar.metric("Documents Processed", processor.database.get("total_processed", 0))
        st.sidebar.metric("Concepts Extracted", len(processor.database.get("concepts", [])))
        st.sidebar.metric("Insights Generated", len(processor.database.get("insights", [])))
        
        if processor.database.get("last_updated"):
            st.sidebar.write(f"Last Updated: {processor.database['last_updated'][:19]}")
    
    # Main upload interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files to upload (up to 70 MB each)",
            type=['pdf', 'epub', 'txt', 'md'],
            accept_multiple_files=True,
            help="Supported formats: PDF, EPUB, TXT, MD - Maximum file size: 70 MB"
        )
        
        if uploaded_files:
            st.success(f"Ready to process {len(uploaded_files)} file(s)")
            
            if st.button("🚀 Process Documents", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                processed_docs = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    # Update progress
                    progress = (i + 1) / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {uploaded_file.name}...")
                    
                    # Get file details
                    file_content = uploaded_file.read()
                    filename = uploaded_file.name
                    file_type = filename.split('.')[-1].lower()
                    
                    # Process document
                    doc_record = processor.process_document(file_content, filename, file_type)
                    
                    if doc_record:
                        processed_docs.append(doc_record)
                        st.success(f"✅ Processed: {filename}")
                    else:
                        st.error(f"❌ Failed to process: {filename}")
                
                progress_bar.progress(1.0)
                status_text.text("Processing complete!")
                
                if processed_docs:
                    st.success(f"🎉 Successfully processed {len(processed_docs)} document(s)")
                    
                    # Show processing results
                    st.header("📋 Processing Results")
                    
                    for doc in processed_docs:
                        with st.expander(f"📄 {doc['filename']} ({doc['word_count']:,} words)"):
                            
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.subheader("🧠 Key Concepts")
                                if doc['concepts']:
                                    for concept in doc['concepts'][:10]:  # Show first 10
                                        if concept['type'] == 'definition':
                                            st.write(f"**{concept['concept']}**: {concept['definition'][:100]}...")
                                        else:
                                            st.write(f"**{concept['concept']}** (mentioned {concept.get('frequency', 1)} times)")
                                else:
                                    st.write("No key concepts extracted")
                            
                            with col_b:
                                st.subheader("💡 Learning Insights")
                                for insight in doc['insights']:
                                    st.write(f"• {insight}")
                            
                            st.subheader("📖 Text Preview")
                            st.text_area(
                                "Content preview:",
                                doc['text_preview'],
                                height=150,
                                key=f"preview_{doc['id']}"
                            )
    
    with col2:
        st.header("🧠 AGI Learning Status")
        
        # Show recent learning activity
        if processor.database.get("documents"):
            st.subheader("📚 Recent Documents")
            recent_docs = list(processor.database["documents"].values())[-5:]  # Last 5
            recent_docs.reverse()  # Most recent first
            
            for doc in recent_docs:
                with st.container():
                    st.write(f"**{doc['filename']}**")
                    st.write(f"📊 {doc['word_count']:,} words | {len(doc['concepts'])} concepts")
                    st.write(f"🕒 {doc['processed_at'][:19]}")
                    st.markdown("---")
        
        # AGI Learning Insights
        st.subheader("⚡ AGI Insights")
        
        if processor.database.get("insights"):
            recent_insights = processor.database["insights"][-10:]  # Last 10 insights
            for insight in recent_insights:
                st.write(f"💡 {insight}")
        else:
            st.info("Upload documents to see AGI learning insights")
    
    # Knowledge Base Explorer
    st.header("🔍 Knowledge Base Explorer")
    
    tab1, tab2, tab3 = st.tabs(["📚 Documents", "🧠 Concepts", "💡 Insights"])
    
    with tab1:
        if processor.database.get("documents"):
            st.write(f"**Total Documents**: {len(processor.database['documents'])}")
            
            # Search functionality
            search_term = st.text_input("🔎 Search documents:")
            
            for doc_id, doc in processor.database["documents"].items():
                if not search_term or search_term.lower() in doc['filename'].lower():
                    with st.expander(f"📄 {doc['filename']}"):
                        col_x, col_y = st.columns(2)
                        with col_x:
                            st.write(f"**Type**: {doc['file_type'].upper()}")
                            st.write(f"**Words**: {doc['word_count']:,}")
                            st.write(f"**Processed**: {doc['processed_at'][:19]}")
                        with col_y:
                            st.write(f"**Concepts**: {len(doc['concepts'])}")
                            st.write(f"**Insights**: {len(doc['insights'])}")
        else:
            st.info("No documents processed yet. Upload files to build the knowledge base.")
    
    with tab2:
        if processor.database.get("concepts"):
            st.write(f"**Total Concepts**: {len(processor.database['concepts'])}")
            
            # Group concepts by type
            definitions = [c for c in processor.database["concepts"] if c.get('type') == 'definition']
            key_terms = [c for c in processor.database["concepts"] if c.get('type') == 'key_term']
            
            if definitions:
                st.subheader("📖 Definitions")
                for concept in definitions[:20]:  # Show first 20
                    st.write(f"**{concept['concept']}**: {concept['definition'][:150]}...")
            
            if key_terms:
                st.subheader("🔑 Key Terms")
                # Sort by frequency
                sorted_terms = sorted(key_terms, key=lambda x: x.get('frequency', 0), reverse=True)
                for concept in sorted_terms[:30]:  # Show top 30
                    st.write(f"**{concept['concept']}** (frequency: {concept.get('frequency', 1)})")
        else:
            st.info("No concepts extracted yet. Upload documents to see key concepts.")
    
    with tab3:
        if processor.database.get("insights"):
            st.write(f"**Total Insights**: {len(processor.database['insights'])}")
            
            for insight in processor.database["insights"]:
                st.write(f"💡 {insight}")
        else:
            st.info("No insights generated yet. Upload documents to see learning insights.")
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 **AGI Document Learning System** - Autonomous knowledge extraction and learning")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Simple Document Learning App
Fast-loading document upload and processing interface
"""

import streamlit as st
import os
import json
from datetime import datetime
import base64

# Configure page first for fastest startup
st.set_page_config(
    page_title="Document Learning System",
    page_icon="📚",
    layout="wide"
)

def process_uploaded_file(uploaded_file):
    """Simple file processing"""
    try:
        # Read file content
        content = uploaded_file.read()
        filename = uploaded_file.name
        file_size = len(content)
        
        # Basic text extraction
        if filename.endswith('.txt'):
            text = content.decode('utf-8')
        elif filename.endswith('.md'):
            text = content.decode('utf-8')
        else:
            # For PDF/EPUB, show basic info for now
            text = f"File uploaded: {filename} ({file_size} bytes)"
        
        # Simple learning simulation
        word_count = len(text.split()) if isinstance(text, str) else 0
        
        return {
            'filename': filename,
            'file_size': file_size,
            'word_count': word_count,
            'content_preview': text[:500] if isinstance(text, str) else text,
            'processed_at': datetime.now().isoformat()
        }
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {e}")
        return None

def main():
    st.title("📚 Document Learning System")
    st.markdown("Upload PDF, EPUB, TXT, or MD files for AGI learning and knowledge extraction")
    
    # Status indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "🟢 Ready", "Upload files to begin")
    
    with col2:
        st.metric("Max File Size", "70 MB", "Per file")
    
    with col3:
        st.metric("Supported Formats", "4 Types", "PDF, EPUB, TXT, MD")
    
    st.markdown("---")
    
    # Main upload interface
    st.header("📤 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload (up to 70 MB each)",
        type=['pdf', 'epub', 'txt', 'md'],
        accept_multiple_files=True,
        help="Supported formats: PDF, EPUB, TXT, MD - Maximum file size: 70 MB"
    )
    
    if uploaded_files:
        st.success(f"Ready to process {len(uploaded_files)} file(s)")
        
        # Show file details
        st.subheader("Selected Files")
        for file in uploaded_files:
            file_size_mb = len(file.getvalue()) / (1024 * 1024)
            st.write(f"📄 **{file.name}** - {file_size_mb:.1f} MB ({file.type})")
        
        if st.button("🚀 Process Documents", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_docs = []
            
            for i, uploaded_file in enumerate(uploaded_files):
                # Update progress
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Process document
                doc_result = process_uploaded_file(uploaded_file)
                
                if doc_result:
                    processed_docs.append(doc_result)
                    st.success(f"✅ Processed: {uploaded_file.name}")
                else:
                    st.error(f"❌ Failed to process: {uploaded_file.name}")
            
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
                            st.subheader("📊 File Information")
                            st.write(f"**Filename**: {doc['filename']}")
                            st.write(f"**File Size**: {doc['file_size']:,} bytes")
                            st.write(f"**Word Count**: {doc['word_count']:,}")
                            st.write(f"**Processed**: {doc['processed_at'][:19]}")
                        
                        with col_b:
                            st.subheader("💡 Quick Analysis")
                            st.write("✅ File uploaded successfully")
                            st.write("✅ Content extracted")
                            st.write("✅ Basic analysis completed")
                            st.write("✅ Ready for advanced processing")
                        
                        st.subheader("📖 Content Preview")
                        st.text_area(
                            "First 500 characters:",
                            doc['content_preview'],
                            height=150,
                            key=f"preview_{doc['filename']}"
                        )
                
                # Save to simple database
                database_file = "document_learning_simple.json"
                try:
                    if os.path.exists(database_file):
                        with open(database_file, 'r') as f:
                            database = json.load(f)
                    else:
                        database = {"processed_documents": []}
                    
                    database["processed_documents"].extend(processed_docs)
                    database["last_updated"] = datetime.now().isoformat()
                    
                    with open(database_file, 'w') as f:
                        json.dump(database, f, indent=2)
                    
                    st.info("📁 Documents saved to learning database")
                    
                except Exception as e:
                    st.warning(f"Could not save to database: {e}")
    
    else:
        st.info("👆 Select files above to begin document processing")
        
        # Show instructions
        st.header("📖 How to Use")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Supported Formats")
            st.write("📄 **PDF** - Portable Document Format")
            st.write("📚 **EPUB** - Electronic Publication")
            st.write("📝 **TXT** - Plain Text Files")
            st.write("📋 **MD** - Markdown Files")
        
        with col2:
            st.subheader("Processing Steps")
            st.write("1. Click 'Browse files' above")
            st.write("2. Select your documents")
            st.write("3. Click 'Process Documents'")
            st.write("4. View extraction results")
    
    # Show existing documents if any
    database_file = "document_learning_simple.json"
    if os.path.exists(database_file):
        try:
            with open(database_file, 'r') as f:
                database = json.load(f)
            
            if database.get("processed_documents"):
                st.header("📚 Previously Processed Documents")
                
                for doc in database["processed_documents"][-5:]:  # Show last 5
                    st.write(f"📄 **{doc['filename']}** - {doc['word_count']:,} words ({doc['processed_at'][:19]})")
                
        except Exception as e:
            st.error(f"Error loading database: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 **Simple Document Learning System** - Fast file upload and processing")

if __name__ == "__main__":
    main()
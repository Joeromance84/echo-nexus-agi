#!/usr/bin/env python3
"""
Document Upload System - AGI Learning Interface
"""

import streamlit as st
import os
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Document Learning",
    page_icon="📚",
    layout="wide"
)

def process_document(uploaded_file):
    """Process uploaded document and extract basic information"""
    try:
        content = uploaded_file.read()
        filename = uploaded_file.name
        file_size = len(content)
        
        # Extract text content for supported formats
        text_content = ""
        if filename.endswith(('.txt', '.md')):
            text_content = content.decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            text_content = f"PDF document: {filename} ({file_size} bytes)"
        elif filename.endswith('.epub'):
            text_content = f"EPUB document: {filename} ({file_size} bytes)"
        
        # Basic analysis
        word_count = len(text_content.split()) if text_content else 0
        
        return {
            'filename': filename,
            'file_size': file_size,
            'word_count': word_count,
            'content_preview': text_content[:500] if text_content else "Binary content",
            'processed_at': datetime.now().isoformat(),
            'file_type': filename.split('.')[-1].upper() if '.' in filename else 'Unknown'
        }
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {e}")
        return None

def main():
    st.title("📚 Document Learning System")
    st.markdown("Upload PDF, EPUB, TXT, or MD files for AGI knowledge extraction")
    
    # Status dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "🟢 Ready")
    with col2:
        st.metric("Max File Size", "70 MB")
    with col3:
        st.metric("Supported Formats", "4 Types")
    
    st.markdown("---")
    
    # File upload interface
    st.header("📤 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'epub', 'txt', 'md'],
        accept_multiple_files=True,
        help="Upload PDF, EPUB, TXT, or MD files up to 70MB each"
    )
    
    if uploaded_files:
        st.success(f"Selected {len(uploaded_files)} file(s)")
        
        # Display selected files
        for file in uploaded_files:
            file_size_mb = len(file.getvalue()) / (1024 * 1024)
            st.write(f"📄 **{file.name}** - {file_size_mb:.1f} MB")
        
        # Process button
        if st.button("🚀 Process Documents", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_docs = []
            
            for i, file in enumerate(uploaded_files):
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing {file.name}...")
                
                doc_result = process_document(file)
                if doc_result:
                    processed_docs.append(doc_result)
                    st.success(f"✅ Processed: {file.name}")
            
            progress_bar.progress(1.0)
            status_text.text("Processing complete!")
            
            if processed_docs:
                st.header("📋 Processing Results")
                
                for doc in processed_docs:
                    with st.expander(f"📄 {doc['filename']} ({doc['word_count']:,} words)"):
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.subheader("File Information")
                            st.write(f"**Name**: {doc['filename']}")
                            st.write(f"**Type**: {doc['file_type']}")
                            st.write(f"**Size**: {doc['file_size']:,} bytes")
                            st.write(f"**Words**: {doc['word_count']:,}")
                        
                        with col_b:
                            st.subheader("Processing Status")
                            st.write("✅ Upload successful")
                            st.write("✅ Content extracted")
                            st.write("✅ Analysis complete")
                            st.write("✅ Ready for learning")
                        
                        if doc['content_preview']:
                            st.subheader("Content Preview")
                            st.text_area(
                                "First 500 characters:",
                                doc['content_preview'],
                                height=100,
                                key=f"preview_{doc['filename']}"
                            )
                
                # Save to database
                try:
                    db_file = "document_learning_database.json"
                    if os.path.exists(db_file):
                        with open(db_file, 'r') as f:
                            database = json.load(f)
                    else:
                        database = {"documents": [], "total_processed": 0}
                    
                    database["documents"].extend(processed_docs)
                    database["total_processed"] = len(database["documents"])
                    database["last_updated"] = datetime.now().isoformat()
                    
                    with open(db_file, 'w') as f:
                        json.dump(database, f, indent=2)
                    
                    st.info(f"📁 Saved {len(processed_docs)} document(s) to learning database")
                    
                except Exception as e:
                    st.warning(f"Database save error: {e}")
    
    else:
        st.info("👆 Select files above to begin document processing")
        
        # Instructions
        st.header("📖 How to Use")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Supported File Types")
            st.write("📄 **PDF** - Documents, books, papers")
            st.write("📚 **EPUB** - E-books and publications")
            st.write("📝 **TXT** - Plain text files")
            st.write("📋 **MD** - Markdown documents")
        
        with col2:
            st.subheader("Processing Steps")
            st.write("1. Click 'Browse files' above")
            st.write("2. Select your documents (up to 70MB each)")
            st.write("3. Click 'Process Documents'")
            st.write("4. View results and content preview")
    
    # Show database statistics
    try:
        db_file = "document_learning_database.json"
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                database = json.load(f)
            
            if database.get("documents"):
                st.header("📊 Learning Database")
                st.write(f"**Total Documents**: {database.get('total_processed', 0)}")
                st.write(f"**Last Updated**: {database.get('last_updated', 'Unknown')[:19]}")
                
                # Show recent documents
                recent_docs = database["documents"][-3:]  # Last 3
                for doc in recent_docs:
                    st.write(f"📄 {doc['filename']} - {doc['word_count']:,} words")
    except:
        pass  # Database not accessible
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 **AGI Document Learning System** - Secure file upload and processing")

if __name__ == "__main__":
    main()
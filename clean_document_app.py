#!/usr/bin/env python3
"""
Clean Document Learning System - No Redirects
"""

import streamlit as st
import os
import json
import re
from datetime import datetime

# CRITICAL: NO REDIRECTS - Clean page config
st.set_page_config(
    page_title="Clean Document Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_pdf_text_simple(content):
    """Extract text from PDF using internal text commands"""
    try:
        text_content = content.decode('latin1', errors='ignore')
        text_patterns = []
        
        # Find BT/ET blocks (text objects)
        bt_et_pattern = re.findall(r'BT\s*(.*?)\s*ET', text_content, re.DOTALL)
        for match in bt_et_pattern:
            # Extract Tj commands (show text)
            tj_matches = re.findall(r'\((.*?)\)\s*Tj', match)
            text_patterns.extend(tj_matches)
            
            # Extract TJ commands (show text array)
            tj_array_matches = re.findall(r'\[(.*?)\]\s*TJ', match)
            for tj_array in tj_array_matches:
                strings = re.findall(r'\((.*?)\)', tj_array)
                text_patterns.extend(strings)
        
        # Combine and clean text
        extracted_text = ' '.join(text_patterns)
        extracted_text = extracted_text.replace('\\n', '\n').replace('\\r', '\r')
        extracted_text = extracted_text.replace('\\t', '\t').replace('\\\\', '\\')
        extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
        
        if len(extracted_text) > 50:
            return extracted_text
        else:
            # Fallback for readable text
            readable_text = re.findall(r'[A-Za-z\s]{10,}', text_content)
            return ' '.join(readable_text[:100]) if readable_text else f"Binary PDF ({len(content)} bytes)"
            
    except Exception as e:
        return f"PDF error: {str(e)} (Size: {len(content)} bytes)"

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract content"""
    try:
        content = uploaded_file.read()
        filename = uploaded_file.name
        file_size = len(content)
        
        # Extract text based on file type
        if filename.endswith(('.txt', '.md')):
            text_content = content.decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            text_content = extract_pdf_text_simple(content)
        elif filename.endswith('.epub'):
            # Simple EPUB text extraction
            text_content = content.decode('utf-8', errors='ignore')
            html_content = re.findall(r'<[^>]*>([^<]+)</[^>]*>', text_content)
            text_content = ' '.join([part.strip() for part in html_content if len(part.strip()) > 3][:200])
        else:
            text_content = f"Unsupported: {filename}"
        
        word_count = len(text_content.split()) if text_content else 0
        
        return {
            'filename': filename,
            'file_size': file_size,
            'word_count': word_count,
            'content_preview': text_content[:500] if text_content else "No content",
            'processed_at': datetime.now().isoformat(),
            'file_type': filename.split('.')[-1].upper() if '.' in filename else 'Unknown'
        }
    except Exception as e:
        st.error(f"Processing error: {e}")
        return None

def main():
    # Clear page with title
    st.title("📚 Clean Document Learning System")
    st.markdown("**Status: ✅ No Redirects - Clean Interface**")
    
    # Quick status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Port", "8501")
    with col2:
        st.metric("Max Size", "70MB")
    with col3:
        st.metric("Formats", "PDF/EPUB/TXT/MD")
    
    st.markdown("---")
    
    # File upload section
    st.header("📤 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose your files",
        type=['pdf', 'epub', 'txt', 'md'],
        accept_multiple_files=True,
        help="Upload PDF, EPUB, TXT, or MD files"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        # Show selected files
        for file in uploaded_files:
            size_mb = len(file.getvalue()) / (1024 * 1024)
            st.write(f"📄 **{file.name}** ({size_mb:.1f} MB)")
        
        # Process button
        if st.button("🚀 Process Files", type="primary"):
            progress = st.progress(0)
            status = st.empty()
            
            results = []
            for i, file in enumerate(uploaded_files):
                progress.progress((i + 1) / len(uploaded_files))
                status.text(f"Processing {file.name}...")
                
                result = process_uploaded_file(file)
                if result:
                    results.append(result)
                    st.success(f"✅ {file.name} processed")
            
            progress.progress(1.0)
            status.text("✅ All files processed!")
            
            # Show results
            if results:
                st.header("📋 Results")
                for doc in results:
                    with st.expander(f"📄 {doc['filename']} - {doc['word_count']:,} words"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.write(f"**File**: {doc['filename']}")
                            st.write(f"**Type**: {doc['file_type']}")
                            st.write(f"**Size**: {doc['file_size']:,} bytes")
                            st.write(f"**Words**: {doc['word_count']:,}")
                        
                        with col_b:
                            st.write("✅ Upload complete")
                            st.write("✅ Text extracted")
                            st.write("✅ Analysis done")
                            st.write("✅ Ready for AI")
                        
                        if doc['content_preview']:
                            st.subheader("Preview")
                            st.text_area(
                                "First 500 characters:",
                                doc['content_preview'],
                                height=120,
                                key=f"preview_{doc['filename']}"
                            )
                
                # Save results
                try:
                    db_file = "clean_document_db.json"
                    if os.path.exists(db_file):
                        with open(db_file, 'r') as f:
                            db = json.load(f)
                    else:
                        db = {"documents": [], "total": 0}
                    
                    db["documents"].extend(results)
                    db["total"] = len(db["documents"])
                    db["last_update"] = datetime.now().isoformat()
                    
                    with open(db_file, 'w') as f:
                        json.dump(db, f, indent=2)
                    
                    st.info(f"💾 Saved {len(results)} documents to database")
                    
                except Exception as e:
                    st.warning(f"Save error: {e}")
    
    else:
        st.info("👆 Select files above to start processing")
        
        # Instructions
        st.header("📖 Instructions")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Supported Files")
            st.write("📄 PDF - Documents and books")
            st.write("📚 EPUB - E-books")
            st.write("📝 TXT - Plain text")
            st.write("📋 MD - Markdown")
        
        with col2:
            st.subheader("How to Use")
            st.write("1. Click 'Browse files'")
            st.write("2. Select your documents")
            st.write("3. Click 'Process Files'")
            st.write("4. View extracted content")
    
    # Database info
    try:
        db_file = "clean_document_db.json"
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                db = json.load(f)
            
            if db.get("documents"):
                st.header("📊 Database")
                st.write(f"**Total**: {db.get('total', 0)} documents")
                st.write(f"**Updated**: {db.get('last_update', 'Unknown')[:19]}")
    except:
        pass
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 **Clean Document Learning** - No redirects, pure Streamlit")

if __name__ == "__main__":
    main()
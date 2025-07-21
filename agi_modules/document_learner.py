#!/usr/bin/env python3
"""
Document Learner AGI Module - Advanced document processing
"""

import streamlit as st
import re
from datetime import datetime

def run():
    """Main document learning interface"""
    st.markdown("### 📚 Advanced Document Processing")
    st.markdown("*Upload and analyze documents with AI-powered content extraction*")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a document for AI analysis",
        type=['pdf', 'epub', 'txt'],
        help="Supports PDF, EPUB, and text files up to 70MB"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"📄 Uploaded: {uploaded_file.name}")
            st.info(f"Size: {uploaded_file.size:,} bytes")
        
        with col2:
            if st.button("🔍 Process Document"):
                process_document(uploaded_file)

def process_document(uploaded_file):
    """Process the uploaded document"""
    with st.spinner("Processing document..."):
        content = uploaded_file.read()
        
        # Determine file type and extract content
        if uploaded_file.name.endswith('.pdf'):
            text_content = extract_pdf_text_simple(content)
        elif uploaded_file.name.endswith('.epub'):
            text_content = extract_epub_text_simple(content)
        else:
            text_content = content.decode('utf-8', errors='ignore')
        
        # Display results
        st.markdown("#### 📄 Extracted Content")
        
        # Show preview
        preview_text = text_content[:1000] + "..." if len(text_content) > 1000 else text_content
        st.text_area("Document Preview", preview_text, height=200)
        
        # Analytics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", len(text_content.split()))
        with col2:
            st.metric("Character Count", len(text_content))
        with col3:
            st.metric("Estimated Reading Time", f"{len(text_content.split()) // 200} min")
        
        # Key insights
        st.markdown("#### 🧠 AI Analysis")
        
        # Extract key phrases (simple implementation)
        words = text_content.split()
        if words:
            # Most common words (excluding common stop words)
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            filtered_words = [word.lower().strip('.,!?";') for word in words if word.lower() not in stop_words and len(word) > 3]
            
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_words:
                st.markdown("**Key Terms:**")
                for word, freq in top_words:
                    st.text(f"• {word} ({freq}x)")
        
        # Save processing log
        log_entry = f"[{datetime.now()}] Processed {uploaded_file.name} - {len(text_content)} chars\n"
        with open("logs/document_learner.log", "a") as f:
            f.write(log_entry)

def extract_pdf_text_simple(content):
    """Simple PDF text extraction without external dependencies"""
    try:
        text_content = content.decode('latin1', errors='ignore')
        
        # Extract text between BT/ET blocks
        bt_et_pattern = re.findall(r'BT\s*(.*?)\s*ET', text_content, re.DOTALL)
        text_patterns = []
        
        for match in bt_et_pattern:
            # Extract text from Tj commands
            tj_matches = re.findall(r'\((.*?)\)\s*Tj', match)
            text_patterns.extend(tj_matches)
            
            # Extract text from TJ commands  
            tj_array_matches = re.findall(r'\[(.*?)\]\s*TJ', match)
            for tj_array in tj_array_matches:
                strings = re.findall(r'\((.*?)\)', tj_array)
                text_patterns.extend(strings)
        
        # Combine and clean extracted text
        extracted_text = ' '.join(text_patterns)
        extracted_text = extracted_text.replace('\\n', '\n').replace('\\r', '\r')
        extracted_text = extracted_text.replace('\\t', '\t').replace('\\\\', '\\')
        extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
        
        return extracted_text if len(extracted_text) > 50 else f"PDF content ({len(content)} bytes)"
    except Exception as e:
        return f"PDF processing error: {str(e)} (Size: {len(content)} bytes)"

def extract_epub_text_simple(content):
    """Simple EPUB text extraction without external dependencies"""
    try:
        text_content = content.decode('utf-8', errors='ignore')
        
        # Look for HTML-like content
        html_content = re.findall(r'<[^>]*>([^<]+)</[^>]*>', text_content)
        text_parts = [part.strip() for part in html_content if len(part.strip()) > 3]
        
        return ' '.join(text_parts[:200]) if text_parts else f"EPUB content ({len(content)} bytes)"
    except Exception as e:
        return f"EPUB processing error: {str(e)} (Size: {len(content)} bytes)"
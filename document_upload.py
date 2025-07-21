#!/usr/bin/env python3
"""
Ultra-Simple Document Upload App
Minimal file upload interface that always works
"""

import streamlit as st
import os
from datetime import datetime

# Page config - fastest possible
st.set_page_config(
    page_title="Document Upload",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 Document Upload System")
    st.markdown("Upload your files for processing")
    
    # Simple file uploader
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'epub', 'txt', 'md'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"Selected {len(uploaded_files)} file(s)")
        
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size} bytes)")
        
        if st.button("Process Files"):
            st.success("Files ready for processing!")
            
            for file in uploaded_files:
                with st.expander(f"File: {file.name}"):
                    st.write(f"Name: {file.name}")
                    st.write(f"Size: {file.size} bytes")
                    st.write(f"Type: {file.type}")
                    
                    if file.name.endswith(('.txt', '.md')):
                        try:
                            content = file.read().decode('utf-8')
                            st.text_area("Content:", content[:500], height=100)
                        except:
                            st.write("Content preview not available")
    else:
        st.info("Select files above to upload")

if __name__ == "__main__":
    main()
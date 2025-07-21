#!/usr/bin/env python3
"""
AGI Document Learning Streamlit App
Complete interface for uploading, processing, and learning from documents
"""

import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from agi_document_processor import AGIDocumentProcessor
import tempfile

# Configure Streamlit page
st.set_page_config(
    page_title="AGI Document Learning System",
    page_icon="📚",
    layout="wide"
)

def main():
    """Main Streamlit application"""
    
    st.title("📚 AGI Document Learning System")
    st.markdown("Upload PDF or EPUB files for the AGI to read, learn from, and intelligently manage")
    
    # Initialize processor in session state
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = AGIDocumentProcessor()
        st.session_state.processing_history = []
    
    processor = st.session_state.doc_processor
    
    # Sidebar - Memory and System Status
    with st.sidebar:
        st.header("🧠 AGI Memory Status")
        
        # Get memory status
        memory_status = asyncio.run(processor._check_memory_status())
        
        # Progress bar for storage usage
        storage_percent = memory_status["storage_usage_percentage"]
        st.progress(storage_percent / 100)
        st.write(f"**Storage:** {memory_status['local_storage_mb']:.1f}MB / {memory_status['local_storage_limit_mb']}MB")
        
        # Cloud storage status
        if memory_status["cloud_storage_available"]:
            st.success("☁️ Cloud storage active")
            st.write("Documents automatically saved to cloud")
        else:
            st.warning("⚠️ Local processing only")
            st.write("Files processed and deleted to save space")
        
        # System stats
        st.metric("Documents Processed", memory_status["documents_processed"])
        
        # Memory management explanation
        st.info("""
        **Smart Memory Management:**
        - Files automatically saved to cloud when possible
        - Large files processed and deleted locally
        - Knowledge extracted and preserved
        - No memory overflow issues
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Documents")
        
        # File upload widget
        uploaded_files = st.file_uploader(
            "Choose PDF or EPUB files",
            type=['pdf', 'epub'],
            accept_multiple_files=True,
            help="Upload documents for the AGI to read and learn from. Files are automatically managed to prevent memory issues."
        )
        
        # Process uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                process_single_file(uploaded_file, processor)
    
    with col2:
        st.header("🔍 Search Knowledge")
        
        # Knowledge search
        search_query = st.text_input(
            "Search learned knowledge:",
            placeholder="Enter keywords to search..."
        )
        
        if search_query:
            search_results = asyncio.run(processor.search_knowledge(search_query))
            
            if search_results["results"]:
                st.success(f"Found {len(search_results['results'])} results")
                
                for i, result in enumerate(search_results["results"][:5]):  # Limit to 5 results
                    with st.expander(f"📄 {result['document']} ({result['match_type']})"):
                        st.write(result['content'])
            else:
                st.info("No matching knowledge found")
    
    # Learning Summary Section
    st.header("🧠 AGI Learning Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Show Learning Summary"):
            show_learning_summary(processor)
    
    with col2:
        if st.button("📚 View Knowledge Database"):
            show_knowledge_database(processor)
    
    with col3:
        if st.button("🔄 Memory Cleanup"):
            perform_memory_cleanup(processor)
    
    # Recent Processing History
    if st.session_state.processing_history:
        st.header("📋 Recent Processing History")
        
        for entry in reversed(st.session_state.processing_history[-5:]):  # Show last 5
            with st.expander(f"✅ {entry['filename']} - {entry['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Status:** {entry['status']}")
                    st.write(f"**Knowledge Insights:** {entry.get('knowledge_insights', 0)}")
                
                with col2:
                    st.write(f"**Storage:** {entry.get('storage_strategy', 'Unknown')}")
                    if entry.get('key_concepts'):
                        st.write(f"**Key Concepts:** {', '.join(entry['key_concepts'][:5])}")

def process_single_file(uploaded_file, processor):
    """Process a single uploaded file"""
    
    with st.expander(f"🔄 Processing: {uploaded_file.name}", expanded=True):
        
        # Read file data
        file_data = uploaded_file.read()
        file_type = uploaded_file.name.split('.')[-1].lower()
        file_size_mb = len(file_data) / (1024 * 1024)
        
        st.write(f"**File Size:** {file_size_mb:.2f} MB")
        st.write(f"**File Type:** {file_type.upper()}")
        
        # Show processing status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Process document
            status_text.text("🔍 Extracting text content...")
            progress_bar.progress(25)
            
            result = asyncio.run(processor.process_uploaded_document(
                file_data, uploaded_file.name, file_type
            ))
            
            status_text.text("🧠 Analyzing and extracting knowledge...")
            progress_bar.progress(75)
            
            # Display results based on status
            if result["status"] == "processed_successfully":
                progress_bar.progress(100)
                status_text.text("✅ Processing complete!")
                
                # Success metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Text Length", f"{result['text_length']:,} chars")
                
                with col2:
                    st.metric("Knowledge Insights", result['knowledge_insights'])
                
                with col3:
                    st.metric("Key Concepts", len(result['key_concepts']))
                
                # Storage strategy
                storage_result = result['storage_result']
                if storage_result['cloud_stored']:
                    st.success("☁️ Document saved to cloud storage")
                else:
                    st.info("🔄 Document processed locally and cleaned up")
                
                # Show key concepts
                if result['key_concepts']:
                    st.write("**🎯 Key Concepts Learned:**")
                    concepts_text = ", ".join(result['key_concepts'][:8])
                    st.write(concepts_text)
                
                # Memory status after processing
                memory_status = result['memory_management']
                if memory_status['storage_usage_percentage'] > 80:
                    st.warning(f"⚠️ Storage usage: {memory_status['storage_usage_percentage']:.1f}%")
                
                # Add to processing history
                st.session_state.processing_history.append({
                    'filename': uploaded_file.name,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'status': 'success',
                    'knowledge_insights': result['knowledge_insights'],
                    'key_concepts': result['key_concepts'][:5],
                    'storage_strategy': storage_result['strategy']
                })
                
            elif result["status"] == "already_processed":
                progress_bar.progress(100)
                status_text.text("📚 Already learned from this document!")
                st.info(f"This document was previously processed with {result['knowledge_extracted']} insights extracted.")
                
            elif result["status"] == "file_too_large":
                progress_bar.progress(0)
                status_text.text("❌ File too large")
                st.error(f"File size ({result['file_size_mb']:.1f} MB) exceeds limit ({result['max_size_mb']} MB)")
                
            else:
                progress_bar.progress(0)
                status_text.text("❌ Processing failed")
                st.error(f"Processing failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("❌ Error occurred")
            st.error(f"Error processing file: {str(e)}")

def show_learning_summary(processor):
    """Display comprehensive learning summary"""
    
    summary = asyncio.run(processor.get_learning_summary())
    
    if summary.get("status") == "no_documents_processed":
        st.info("No documents have been processed yet. Upload some files to begin learning!")
        return
    
    st.subheader("📊 Learning Analytics")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents", summary["total_documents_processed"])
    
    with col2:
        st.metric("Concepts", summary["total_concepts_learned"])
    
    with col3:
        st.metric("Insights", summary["total_insights_extracted"])
    
    with col4:
        st.metric("Learning Points", summary["total_learning_points"])
    
    # Learning effectiveness
    effectiveness = summary["learning_effectiveness"]
    
    st.subheader("🎯 Learning Effectiveness")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Avg Insights/Document", f"{effectiveness['avg_insights_per_document']:.1f}")
    
    with col2:
        st.metric("Knowledge Retention", effectiveness['knowledge_retention'].title())
    
    # Top concepts
    if summary["top_concepts"]:
        st.subheader("🧠 Most Important Concepts")
        concepts_text = " • ".join(summary["top_concepts"][:15])
        st.write(concepts_text)
    
    # Recent documents
    if summary["recent_documents"]:
        st.subheader("📚 Recent Learning")
        for doc in summary["recent_documents"]:
            st.write(f"• **{doc['filename']}** - {doc['knowledge_insights']} insights extracted")

def show_knowledge_database(processor):
    """Display knowledge database contents"""
    
    st.subheader("🗄️ Knowledge Database")
    
    if not processor.processed_documents:
        st.info("Knowledge database is empty. Process some documents first!")
        return
    
    # Document list
    for file_hash, doc_info in processor.processed_documents.items():
        with st.expander(f"📄 {doc_info['filename']}"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**File Type:** {doc_info['file_type'].upper()}")
                st.write(f"**Size:** {doc_info['file_size_mb']:.2f} MB")
                st.write(f"**Processed:** {doc_info['timestamp'][:19]}")
            
            with col2:
                st.write(f"**Knowledge Insights:** {doc_info['knowledge_extracted']}")
                st.write(f"**Storage:** {doc_info.get('storage_location', 'Local')}")
                st.write(f"**Local Deleted:** {'Yes' if doc_info.get('local_file_deleted') else 'No'}")
            
            # Show knowledge if available
            if file_hash in processor.knowledge_database:
                knowledge = processor.knowledge_database[file_hash]
                
                if knowledge.get("key_concepts"):
                    st.write("**Key Concepts:**")
                    st.write(", ".join(knowledge["key_concepts"][:10]))
                
                if knowledge.get("document_summary"):
                    st.write("**Summary:**")
                    st.write(knowledge["document_summary"][:300] + "...")

def perform_memory_cleanup(processor):
    """Perform memory cleanup and show results"""
    
    st.subheader("🧹 Memory Cleanup")
    
    # Get current status
    before_status = asyncio.run(processor._check_memory_status())
    
    st.write("**Before Cleanup:**")
    st.write(f"• Storage Usage: {before_status['local_storage_mb']:.2f} MB")
    st.write(f"• Usage Percentage: {before_status['storage_usage_percentage']:.1f}%")
    
    # Simulate cleanup (in real implementation, this would clean temporary files)
    cleanup_results = {
        "files_cleaned": 0,
        "space_freed_mb": 0.0,
        "knowledge_preserved": True
    }
    
    # Check for temporary files to clean
    import tempfile
    import glob
    
    temp_files = glob.glob(os.path.join(tempfile.gettempdir(), "*.pdf")) + \
                glob.glob(os.path.join(tempfile.gettempdir(), "*.epub"))
    
    for temp_file in temp_files:
        try:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            os.remove(temp_file)
            cleanup_results["files_cleaned"] += 1
            cleanup_results["space_freed_mb"] += file_size
        except:
            pass
    
    # Show cleanup results
    if cleanup_results["files_cleaned"] > 0:
        st.success(f"✅ Cleaned {cleanup_results['files_cleaned']} temporary files")
        st.success(f"✅ Freed {cleanup_results['space_freed_mb']:.2f} MB of space")
    else:
        st.info("ℹ️ No temporary files found to clean")
    
    # After cleanup status
    after_status = asyncio.run(processor._check_memory_status())
    
    st.write("**After Cleanup:**")
    st.write(f"• Storage Usage: {after_status['local_storage_mb']:.2f} MB")
    st.write(f"• Usage Percentage: {after_status['storage_usage_percentage']:.1f}%")
    
    st.success("🧠 All knowledge and learning preserved!")

if __name__ == "__main__":
    main()
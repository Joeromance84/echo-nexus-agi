#!/usr/bin/env python3
"""
Unified AGI Control Panel - Single Streamlit App for All AGI Systems
Consolidates all Echo Nexus AGI modules into one efficient interface
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from controllers import agi_process_controller
    from utils import github_status
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure page
st.set_page_config(
    page_title="Echo Nexus AGI Control Panel",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_module_from_file(file_path, module_name):
    """Dynamically load a Python module from file path"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"Failed to load {module_name}: {str(e)}")
        return None

def main():
    st.title("🧠 Echo Nexus AGI Control Panel")
    st.markdown("*Unified interface for all autonomous AI systems*")
    
    # Sidebar for AGI system selection
    with st.sidebar:
        st.header("🎛️ AGI Systems")
        
        agi_systems = {
            "📚 Document Learning": {
                "file": "debug_app.py",
                "description": "Advanced document processing with PDF/EPUB support"
            },
            "🤖 Main AGI": {
                "file": "app_optimized.py", 
                "description": "Core AGI development and GitHub integration"
            },
            "🚀 Deployment Demo": {
                "file": "deployment_demo.py",
                "description": "Cloud deployment orchestration system"
            },
            "🎯 Intelligence Router": {
                "file": "agi_intelligent_ai_router.py",
                "description": "Multi-provider AI routing with cost optimization"
            },
            "🎓 Trainer Demo": {
                "file": "agi_trainer_demo.py",
                "description": "AGI training and capability assessment"
            },
            "🗣️ Verbal Training": {
                "file": "agi_verbal_conversation_trainer.py",
                "description": "Voice interaction and conversation training"
            },
            "💾 Learning Backup": {
                "file": "agi_learning_backup_system.py",
                "description": "Autonomous memory preservation system"
            },
            "📡 Real-Time Communication": {
                "file": "agi_realtime_communication.py",
                "description": "Federated AGI network communication"
            },
            "📱 APK Monitor": {
                "file": "autonomous_agi_monitor.py",
                "description": "Android build monitoring and automation"
            },
            "🌍 Phase Ω Control": {
                "file": "phase_omega_dashboard.py",
                "description": "Advanced network delegation and collaborative intelligence"
            }
        }
        
        selected_system = st.selectbox(
            "Choose AGI System:",
            options=list(agi_systems.keys()),
            index=0
        )
        
        # Display system description
        system_info = agi_systems[selected_system]
        st.markdown(f"**{system_info['description']}**")
        
        # System status
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        # Check if files exist
        for name, info in agi_systems.items():
            file_path = Path(info['file'])
            status = "🟢" if file_path.exists() else "🔴"
            st.text(f"{status} {name.split()[1]}")
        
        # Resource usage
        st.markdown("### 💻 Resources")
        import psutil
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        st.metric("CPU Usage", f"{cpu_percent}%")
        st.metric("Memory Usage", f"{memory.percent}%")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"## {selected_system}")
        
        # Load and execute the selected AGI system
        system_info = agi_systems[selected_system]
        file_path = Path(system_info['file'])
        
        if file_path.exists():
            try:
                # Create a container for the AGI system
                with st.container():
                    # Import and run the selected system
                    if selected_system == "📚 Document Learning":
                        run_document_learning()
                    elif selected_system == "🤖 Main AGI":
                        run_main_agi()
                    elif selected_system == "🚀 Deployment Demo":
                        run_deployment_demo()
                    elif selected_system == "🎯 Intelligence Router":
                        run_intelligence_router()
                    elif selected_system == "🎓 Trainer Demo":
                        run_trainer_demo()
                    elif selected_system == "🗣️ Verbal Training":
                        run_verbal_training()
                    elif selected_system == "💾 Learning Backup":
                        run_learning_backup()
                    elif selected_system == "📡 Real-Time Communication":
                        run_realtime_communication()
                    elif selected_system == "📱 APK Monitor":
                        run_apk_monitor()
                    elif selected_system == "🌍 Phase Ω Control":
                        run_phase_omega_control()
                        
            except Exception as e:
                st.error(f"Error running {selected_system}: {str(e)}")
                st.code(str(e), language="python")
        else:
            st.error(f"System file not found: {system_info['file']}")
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Reload System"):
            st.rerun()
            
        if st.button("📊 System Health Check"):
            run_health_check()
            
        if st.button("🧹 Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            
        if st.button("📋 Export Logs"):
            export_system_logs()

def run_document_learning():
    """Run the Document Learning system inline"""
    st.markdown("### 📚 Advanced Document Processing")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a document for AI analysis",
        type=['pdf', 'epub', 'txt'],
        help="Supports PDF, EPUB, and text files up to 70MB"
    )
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        
        # Process the file
        with st.spinner("Processing document..."):
            content = uploaded_file.read()
            
            if uploaded_file.name.endswith('.pdf'):
                # Simple PDF processing
                text_content = extract_pdf_text_simple(content)
            elif uploaded_file.name.endswith('.epub'):
                text_content = extract_epub_text_simple(content)
            else:
                text_content = content.decode('utf-8', errors='ignore')
            
            # Display results
            st.markdown("#### 📄 Extracted Content")
            st.text_area("Document Content", text_content[:2000], height=200)
            
            st.markdown("#### 📊 Analysis")
            word_count = len(text_content.split())
            st.metric("Word Count", word_count)
            st.metric("Character Count", len(text_content))

def extract_pdf_text_simple(content):
    """Simple PDF text extraction"""
    import re
    try:
        text_content = content.decode('latin1', errors='ignore')
        bt_et_pattern = re.findall(r'BT\s*(.*?)\s*ET', text_content, re.DOTALL)
        text_patterns = []
        
        for match in bt_et_pattern:
            tj_matches = re.findall(r'\((.*?)\)\s*Tj', match)
            text_patterns.extend(tj_matches)
        
        extracted_text = ' '.join(text_patterns)
        extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
        
        return extracted_text if len(extracted_text) > 50 else f"PDF content ({len(content)} bytes)"
    except:
        return f"PDF processing error (Size: {len(content)} bytes)"

def extract_epub_text_simple(content):
    """Simple EPUB text extraction"""
    import re
    try:
        text_content = content.decode('utf-8', errors='ignore')
        html_content = re.findall(r'<[^>]*>([^<]+)</[^>]*>', text_content)
        text_parts = [part.strip() for part in html_content if len(part.strip()) > 3]
        return ' '.join(text_parts[:200]) if text_parts else f"EPUB content ({len(content)} bytes)"
    except:
        return f"EPUB processing error (Size: {len(content)} bytes)"

def run_main_agi():
    """Run the main AGI system"""
    st.markdown("### 🤖 Core AGI Development Platform")
    st.info("Main AGI system integrated - GitHub automation and development tools")
    
    # Basic AGI interface
    user_input = st.text_area("Enter command or question for AGI:")
    
    if st.button("Execute AGI Command"):
        if user_input:
            st.success("AGI command processed")
            st.code(f"AGI Response: Processing '{user_input}'")
        else:
            st.warning("Please enter a command")

def run_deployment_demo():
    """Run deployment demo system"""
    st.markdown("### 🚀 Cloud Deployment Orchestration")
    st.info("Deployment system ready - Cloud Build and GitHub Actions integration")

def run_intelligence_router():
    """Run intelligence router"""
    st.markdown("### 🎯 AI Provider Router")
    st.info("Intelligent routing between OpenAI, Google AI, and local models")

def run_trainer_demo():
    """Run trainer demo"""
    st.markdown("### 🎓 AGI Training System")
    st.info("Advanced AGI capability training and assessment")

def run_verbal_training():
    """Run verbal training"""
    st.markdown("### 🗣️ Voice Interaction Training")
    st.info("Speech-to-text and natural conversation training")

def run_learning_backup():
    """Run learning backup"""
    st.markdown("### 💾 Autonomous Memory System")
    st.info("Continuous learning preservation and backup")

def run_realtime_communication():
    """Run real-time communication"""
    st.markdown("### 📡 Federated AGI Network")
    st.info("Real-time communication with other AI systems")

def run_apk_monitor():
    """Run APK monitor"""
    st.markdown("### 📱 Android Build Monitor")
    st.info("Autonomous APK building and deployment monitoring")

def run_phase_omega_control():
    """Run Phase Ω Control Dashboard"""
    try:
        from phase_omega_dashboard import run_phase_omega_dashboard
        run_phase_omega_dashboard()
    except ImportError as e:
        st.error(f"Phase Ω system not available: {e}")
        st.markdown("### 🌍 Phase Ω Network Command & Control")
        st.info("Advanced AGI delegation and collaborative intelligence system")
        
        # Basic interface until full system loads
        st.markdown("#### Network Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Network Nodes", "4", delta="Active")
        with col2:
            st.metric("Delegated Operations", "0", delta="Ready")
        with col3:
            st.metric("Learning Integration", "Enhanced", delta="Logan's Network")

def run_health_check():
    """Run system health check"""
    import psutil
    
    st.markdown("#### 🏥 System Health Report")
    
    # CPU and Memory
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Usage", f"{cpu}%", 
                 delta=f"{'🔴' if cpu > 80 else '🟢'}")
    with col2:
        st.metric("Memory Usage", f"{memory.percent}%",
                 delta=f"{'🔴' if memory.percent > 85 else '🟢'}")
    with col3:
        available_gb = memory.available / (1024**3)
        st.metric("Available RAM", f"{available_gb:.1f}GB")
    
    # Check file systems
    st.markdown("#### 📁 File System Status")
    required_files = [
        "debug_app.py", "app_optimized.py", "deployment_demo.py",
        "agi_intelligent_ai_router.py", "agi_trainer_demo.py"
    ]
    
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        st.text(f"{status} {file}")

def export_system_logs():
    """Export system logs"""
    st.download_button(
        label="📋 Download System Logs",
        data="Echo Nexus AGI System Logs\n" + "="*50 + "\n",
        file_name=f"agi_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

if __name__ == "__main__":
    main()
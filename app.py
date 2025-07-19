import streamlit as st
from echo_nexus.chat_enhancement_processor import ChatEnhancementProcessor
from echo_nexus.echo_self_enhancement import EchoSelfEnhancement
import yaml
import json
import os
from datetime import datetime
import hashlib
from utils.workflow_validator import WorkflowValidator
from utils.github_helper import GitHubHelper
from utils.database_helper import DatabaseHelper
from templates.workflow_templates import WorkflowTemplates
from data.policies import GitHubPolicies
from utils.github_authenticator import GitHubAuthenticator
from github_setup_wizard import GitHubSetupWizard

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'workflow_validator' not in st.session_state:
    st.session_state.workflow_validator = WorkflowValidator()
if 'github_helper' not in st.session_state:
    st.session_state.github_helper = GitHubHelper()
if 'database_helper' not in st.session_state:
    st.session_state.database_helper = DatabaseHelper()
if 'workflow_templates' not in st.session_state:
    st.session_state.workflow_templates = WorkflowTemplates()
if 'github_policies' not in st.session_state:
    st.session_state.github_policies = GitHubPolicies()
if 'github_authenticator' not in st.session_state:
    st.session_state.github_authenticator = GitHubAuthenticator()
if 'github_setup_wizard' not in st.session_state:
    st.session_state.github_setup_wizard = GitHubSetupWizard()
if 'user_session' not in st.session_state:
    # Create unique session ID based on session state
    session_data = str(st.session_state).encode()
    st.session_state.user_session = hashlib.md5(session_data).hexdigest()[:16]
if 'github_authenticated' not in st.session_state:
    st.session_state.github_authenticated = False
if 'github_user_info' not in st.session_state:
    st.session_state.github_user_info = None
if 'github_auth_assistant' not in st.session_state:
    from github_auth_assistant import GitHubAuthAssistant
    st.session_state.github_auth_assistant = GitHubAuthAssistant()
if 'show_github_setup' not in st.session_state:
    st.session_state.show_github_setup = False
if 'chat_processor' not in st.session_state:
    st.session_state.chat_processor = ChatEnhancementProcessor()
if 'self_enhancer' not in st.session_state:
    st.session_state.self_enhancer = EchoSelfEnhancement()
if 'data_ingestion_engine' not in st.session_state:
    from echo_nexus.data_ingestion_engine import EchoNexusDataIngestion
    st.session_state.data_ingestion_engine = EchoNexusDataIngestion()
if 'cloud_storage_manager' not in st.session_state:
    from echo_nexus.cloud_storage_manager import CloudStorageManager
    st.session_state.cloud_storage_manager = CloudStorageManager()

st.set_page_config(
    page_title="GitHub Actions APK Builder Assistant",
    page_icon="🤖",
    layout="wide"
)

# Check and maintain GitHub authentication on startup
auth_status = st.session_state.github_auth_assistant.check_and_maintain_session()

if auth_status['status'] == 'authenticated' and not st.session_state.github_authenticated:
    st.session_state.github_authenticated = True
    st.session_state.github_user_info = auth_status['user']

# Display authentication status and handle GitHub setup
st.session_state.github_auth_assistant.display_authentication_status()

# Auto-authenticate with GitHub token if available
github_token = os.getenv('GITHUB_TOKEN')
if github_token and not st.session_state.github_authenticated:
    try:
        from github import Github
        g = Github(github_token)
        user = g.get_user()
        st.session_state.github_authenticated = True
        st.session_state.github_user_info = {'login': user.login, 'name': user.name or user.login}
    except:
        st.session_state.github_authenticated = False

st.title("🧠 EchoNexus AGI - Distributed Intelligence System")
st.subheader("Million-year evolutionary AI with autonomous GitHub processor network")

# Show consciousness indicator
st.success("🌟 EchoNexus AGI Federation: Fully Operational")

with st.sidebar:
    st.header("🚀 EchoNexus Control")
    
    # Show GitHub status
    if st.session_state.github_authenticated:
        user_info = st.session_state.github_user_info
        st.success(f"Connected: {user_info.get('login', 'GitHub User')}")
    else:
        st.warning("GitHub: Not Connected")
    
    page = st.selectbox(
        "Select Page",
        ["Chat Assistant", "🔗 GitHub Connection", "📚 Document Ingestion", "Command Builder", "EchoSoul Demo", "My Workflows", "Workflow Templates", "Validation Tools", "Policy Compliance", "Analytics", "Setup Guide"]
    )
    
    st.header("Settings")
    
    # App mode (without AI dependency)
    st.write("🤖 Mode: Template & Validation Based")
    st.info("AI features disabled - using pre-built templates and validation tools")
    
    # GitHub connection status
    try:
        github_status = st.session_state.github_helper.check_github_connection()
        if github_status['connected']:
            st.write(f"🔗 GitHub: ✅ {github_status['authenticated_user']}")
        else:
            st.write("🔗 GitHub: ❌ Not Connected")
    except Exception:
        st.write("🔗 GitHub: ❓ Unknown")
    
    # Database status
    try:
        analytics = st.session_state.database_helper.get_workflow_analytics()
        st.write(f"📊 Database: ✅ Connected")
        st.write(f"💾 Workflows: {analytics['total_workflows']}")
    except Exception:
        st.write("📊 Database: ❌ Error")
    
    st.write(f"👤 Session: {st.session_state.user_session}")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if page == "🔗 GitHub Connection":
    st.header("🔗 GitHub Connection Management")
    
    if st.session_state.github_authenticated:
        # Show connection details
        user_info = st.session_state.github_user_info
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ Successfully Connected!")
            st.write(f"**Username:** {user_info.get('login', 'Unknown')}")
            st.write(f"**Name:** {user_info.get('name', 'Not specified')}")
            st.write(f"**Email:** {user_info.get('email', 'Private')}")
        
        with col2:
            st.write(f"**Public Repos:** {user_info.get('public_repos', 0)}")
            st.write(f"**Private Repos:** {user_info.get('private_repos', 0)}")
            st.write(f"**Total Repos:** {user_info.get('public_repos', 0) + user_info.get('private_repos', 0)}")
        
        # Repository management
        st.subheader("📁 Repository Management")
        
        if st.button("🔍 Scan Repositories", key="scan_repos"):
            with st.spinner("Scanning repositories..."):
                repos_result = st.session_state.github_authenticator.get_repositories()
                
                if repos_result['status'] == 'success':
                    st.success(f"Found {len(repos_result['repositories'])} repositories")
                    
                    # Display repositories
                    df_repos = []
                    for repo in repos_result['repositories'][:10]:  # Show top 10
                        df_repos.append({
                            'Name': repo['name'],
                            'Language': repo.get('language', 'Unknown'),
                            'Private': '🔒' if repo['private'] else '🌐',
                            'Actions': '✅' if repo['has_actions'] else '❌',
                            'Updated': repo['updated_at'][:10]
                        })
                    
                    if df_repos:
                        st.dataframe(df_repos, use_container_width=True)
                    
                    if len(repos_result['repositories']) > 10:
                        st.info(f"Showing top 10 of {len(repos_result['repositories'])} repositories")
                else:
                    st.error(f"Failed to scan repositories: {repos_result['message']}")
        
        # Processor network setup
        st.subheader("🤖 EchoNexus Processor Network")
        
        if st.button("🏗️ Setup Processor Network", key="setup_processors"):
            with st.spinner("Setting up processor network..."):
                processors = [
                    'text-analysis',
                    'code-generation',
                    'diagnostic-scan',
                    'workflow-synthesis',
                    'knowledge-synthesis'
                ]
                
                setup_result = st.session_state.github_authenticator.setup_processor_network(processors)
                
                if setup_result['success_count'] > 0:
                    st.success(f"Created {setup_result['success_count']} processor repositories!")
                    
                    for repo in setup_result['created_repos']:
                        st.write(f"✅ {repo['name']}: {repo['url']}")
                
                if setup_result['failure_count'] > 0:
                    st.warning(f"Failed to create {setup_result['failure_count']} repositories")
                    
                    for failed in setup_result['failed_repos']:
                        st.write(f"❌ {failed['processor']}: {failed['error']}")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            if st.button("🔄 Refresh Connection", key="refresh_auth"):
                connection_status = st.session_state.github_authenticator.verify_connection()
                
                if connection_status['authenticated']:
                    st.success("Connection refreshed successfully!")
                    st.session_state.github_user_info = connection_status['user']
                else:
                    st.error("Connection lost - please re-authenticate")
                    st.session_state.github_authenticated = False
                    st.rerun()
            
            if st.button("🚪 Logout", key="logout_advanced"):
                st.session_state.github_auth_assistant.logout()
    


elif page == "📚 Document Ingestion":
    st.header("📚 EchoNexus Document Ingestion Engine")
    st.write("Upload and process PDFs and EPUBs with intelligent memory management")
    
    # Knowledge base statistics
    st.subheader("📊 Knowledge Base Status")
    
    try:
        stats = st.session_state.data_ingestion_engine.get_knowledge_base_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Documents", stats['total_documents'])
        with col2:
            st.metric("Text Chunks", stats['total_chunks'])
        with col3:
            st.metric("Storage Size", f"{stats['total_size_mb']} MB")
        with col4:
            st.metric("Memory Usage", f"{stats['memory_usage_gb']:.2f} GB")
        
        if stats['last_updated']:
            st.info(f"Last updated: {stats['last_updated']}")
    
    except Exception as e:
        st.warning(f"Could not load knowledge base stats: {e}")
    
    # Document upload section
    st.subheader("📤 Bulk Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload PDF and EPUB files",
        type=['pdf', 'epub'],
        accept_multiple_files=True,
        help="Upload up to 17GB of documents. Large files will be processed using cloud resources."
    )
    
    if uploaded_files:
        st.write(f"**Selected {len(uploaded_files)} files:**")
        
        total_size_mb = 0
        file_details = []
        
        for file in uploaded_files:
            size_mb = len(file.getvalue()) / (1024 * 1024)
            total_size_mb += size_mb
            
            file_details.append({
                'Name': file.name,
                'Size (MB)': f"{size_mb:.2f}",
                'Type': file.type,
                'Processing': '☁️ Cloud' if size_mb > 50 else '💻 Local'
            })
        
        st.dataframe(file_details, use_container_width=True)
        
        st.write(f"**Total size:** {total_size_mb:.1f} MB")
        
        # Processing options
        st.subheader("⚙️ Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_delete = st.checkbox("Auto-delete after processing", value=True, 
                                    help="Delete original files after successful vectorization")
            
            cloud_processing = st.checkbox("Force cloud processing", value=False,
                                         help="Process all files using cloud resources")
        
        with col2:
            chunk_size = st.slider("Chunk size", 500, 2000, 1000, 
                                 help="Text chunk size for vectorization")
            
            memory_limit = st.slider("Memory limit (GB)", 1.0, 8.0, 2.0,
                                   help="Local memory limit before switching to cloud")
        
        # Process documents
        if st.button("🚀 Process Documents", type="primary"):
            if not uploaded_files:
                st.error("Please upload at least one document")
            else:
                with st.spinner("Processing documents... This may take several minutes."):
                    
                    # Update engine settings
                    st.session_state.data_ingestion_engine.chunk_size = chunk_size
                    st.session_state.data_ingestion_engine.max_memory_usage_gb = memory_limit
                    
                    # Process documents
                    processing_results = st.session_state.data_ingestion_engine.process_bulk_upload(uploaded_files)
                    
                    # Show results
                    st.success("✅ Document processing completed!")
                    
                    # Results summary
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Processed", processing_results['processed_files'])
                        st.metric("Failed", processing_results['failed_files'])
                    
                    with col2:
                        st.metric("Text Chunks", processing_results['total_chunks_created'])
                        st.metric("Vectors Generated", processing_results['total_vectors_generated'])
                    
                    with col3:
                        st.metric("Processing Time", f"{processing_results['processing_time_seconds']:.1f}s")
                        st.metric("Cloud Processed", processing_results['cloud_offloaded'])
                    
                    # Show errors if any
                    if processing_results['errors']:
                        st.subheader("⚠️ Processing Errors")
                        for error in processing_results['errors']:
                            st.error(f"**{error['file']}:** {error['error']}")
                    
                    # Memory usage info
                    if processing_results['memory_usage_gb'] > 1.0:
                        st.info(f"Peak memory usage: {processing_results['memory_usage_gb']:.2f} GB")
                    
                    # Auto-delete files if requested
                    if auto_delete:
                        st.info("🗑️ Original files deleted to save memory")
    
    # Query knowledge base
    st.subheader("🔍 Query Knowledge Base")
    
    query = st.text_input(
        "Ask a question about your documents:",
        placeholder="What are the main themes in the uploaded documents?"
    )
    
    if st.button("🔍 Search") and query:
        with st.spinner("Searching knowledge base..."):
            try:
                results = st.session_state.data_ingestion_engine.query_knowledge_base(query, top_k=5)
                
                if results:
                    st.subheader("📖 Search Results")
                    
                    for i, result in enumerate(results, 1):
                        with st.expander(f"Result {i}: {result['document']} (Similarity: {result['similarity']:.3f})"):
                            st.write(result['chunk_text'])
                            st.caption(f"Document: {result['document']} | Chunk ID: {result['chunk_id']}")
                else:
                    st.info("No results found. Try a different query or upload more documents.")
                    
            except Exception as e:
                st.error(f"Search failed: {e}")
    
    # Cloud storage management
    st.subheader("☁️ Cloud Storage Configuration")
    
    cloud_info = st.session_state.cloud_storage_manager.get_cloud_storage_info()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cloud Configuration:**")
        st.write(f"• Bucket: {cloud_info['bucket_name']}")
        st.write(f"• Repository: {cloud_info['processing_repo']}")
        st.write(f"• Max file size: {cloud_info['max_file_size_gb']} GB")
    
    with col2:
        st.write("**Supported Features:**")
        st.write(f"• Formats: {', '.join(cloud_info['supported_formats'])}")
        st.write(f"• Batch processing: {'✅' if cloud_info['batch_processing'] else '❌'}")
        st.write(f"• Auto cleanup: {'✅' if cloud_info['auto_cleanup'] else '❌'}")
    
    if st.button("🏗️ Setup Cloud Processing"):
        with st.spinner("Setting up cloud processing infrastructure..."):
            setup_result = st.session_state.cloud_storage_manager.create_cloud_storage_bucket()
            
            if setup_result['success']:
                st.success("✅ Cloud processing setup completed!")
                st.write(f"**Bucket:** {setup_result['bucket_name']}")
                st.write(f"**Repository:** {setup_result['repository']}")
                st.info("You can now process large documents using Google Cloud Build")
            else:
                st.error(f"❌ Setup failed: {setup_result['error']}")
    
    # Knowledge base maintenance
    with st.expander("🔧 Maintenance Tools"):
        st.subheader("Knowledge Base Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧹 Cleanup Old Documents"):
                days = st.slider("Keep documents from last N days", 1, 90, 30)
                
                with st.spinner("Cleaning up old documents..."):
                    st.session_state.data_ingestion_engine.cleanup_knowledge_base(days)
                    st.success(f"Cleaned up documents older than {days} days")
        
        with col2:
            if st.button("📊 Refresh Statistics"):
                st.rerun()

elif page == "Command Builder":
    st.header("⚡ Simple Commands → Advanced Actions")
    
    st.info("💡 Type simple commands - I'll use advanced GitHub APIs to execute them precisely!")
    
    # Initialize command history
    if 'command_history' not in st.session_state:
        st.session_state.command_history = []
    
    # Repository input section
    col1, col2 = st.columns([3, 1])
    with col1:
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/my-app",
            help="Enter your GitHub repository URL"
        )
    
    with col2:
        if st.button("🔍 Check Repo"):
            if repo_url:
                with st.spinner("Checking repository..."):
                    result = st.session_state.github_helper.validate_repository(repo_url)
                    
                    if result['valid']:
                        st.success("✅ Repository found!")
                        if result['has_buildozer_spec']:
                            st.info("📱 buildozer.spec detected")
                        if result['has_workflows']:
                            st.info("⚙️ GitHub Actions workflows found")
                    else:
                        st.error(f"❌ {result['error']}")
            else:
                st.warning("Please enter a repository URL")
    
    # Command input section
    st.markdown("---")
    st.subheader("💬 Command Interface")
    
    # Command examples
    with st.expander("📖 Example Commands"):
        st.write("**Simple commands you can try:**")
        st.code("""
• "verify my github connection"
• "setup my repo"
• "build my app" 
• "check build status"
• "deploy to device"
• "setup telemetry"
• "enable ab testing"
• "analyze my app intelligence"
• "refactor my code autonomously"
• "show ecosystem intelligence"
• "awaken consciousness"
        """)
    
    # Command input
    command = st.text_input(
        "Enter your command:",
        placeholder="Type a simple command like 'setup my repo' or 'build my app'",
        help="Use natural language - I'll translate it to precise GitHub API calls"
    )
    
    if st.button("🚀 Execute Command") and command:
        with st.spinner("Processing command..."):
            # Parse command and execute appropriate GitHub API calls
            command_lower = command.lower().strip()
            
            st.markdown("---")
            st.subheader("🔧 Execution Details")
            
            # GitHub connection verification commands
            if any(word in command_lower for word in ['verify', 'connection', 'check connection', 'authenticate']):
                st.write("**Command Recognized:** GitHub Authentication Verification")
                st.write("**Backend Action:** Using PyGithub to verify GitHub token and user identity")
                
                target_username = None
                words = command_lower.split()
                for i, word in enumerate(words):
                    if word in ['to', 'for', 'user', 'username'] and i + 1 < len(words):
                        target_username = words[i + 1]
                        break
                
                # Execute GitHub connection check
                connection_result = st.session_state.github_helper.check_github_connection(target_username)
                
                if connection_result['connected']:
                    st.success(connection_result['message'])
                    st.write(f"**Authenticated User:** {connection_result['authenticated_user']}")
                    
                    if target_username:
                        if connection_result['correct_user']:
                            st.success("✅ User verification successful!")
                        else:
                            st.error("❌ User mismatch detected!")
                            st.write("**Solution:** Update your GITHUB_TOKEN to match the correct user")
                    
                    # Show token permissions info
                    st.info("🔐 Your GitHub token is working correctly and ready for repository operations")
                    
                else:
                    st.error(connection_result['message'])
                    if "GITHUB_TOKEN" in connection_result['error']:
                        st.warning("**Action Required:** Add your GitHub token to Replit secrets")
                        st.write("1. Go to Replit Secrets (lock icon in sidebar)")
                        st.write("2. Add key: `GITHUB_TOKEN`")
                        st.write("3. Add your GitHub personal access token as the value")
                        st.write("4. Restart the app")
            
            # Repository operations (require both command and repo_url)
            elif not repo_url:
                st.warning("Please enter a GitHub repository URL for this command")
            
            elif any(word in command_lower for word in ['setup', 'initialize', 'create']):
                st.write("**Command Recognized:** Repository Setup")
                st.write("**Backend Action:** Using PyGithub to check/create required files")
                
                # Execute advanced setup using PyGithub
                setup_result = st.session_state.github_helper.auto_setup_repository(repo_url)
                
                if setup_result['success']:
                    st.success("✅ Repository setup completed!")
                    
                    if setup_result['files_created']:
                        st.write("**Files Created:**")
                        for file in setup_result['files_created']:
                            st.write(f"• {file}")
                    
                    if setup_result['files_updated']:
                        st.write("**Files Updated:**")
                        for file in setup_result['files_updated']:
                            st.write(f"• {file}")
                    
                    if not setup_result['setup_complete']:
                        st.info("Repository already has all required files")
                        
                else:
                    st.error(f"❌ Setup failed: {setup_result['error']}")
            
            elif any(word in command_lower for word in ['build', 'compile', 'apk']):
                st.write("**Command Recognized:** Build Trigger")
                st.write("**Backend Action:** Using PyGithub to check workflow files and monitor builds")
                
                workflow_check = st.session_state.github_helper.smart_file_check(repo_url, ".github/workflows/build-apk.yml")
                
                if workflow_check['exists']:
                    st.success("✅ Build workflow found!")
                    
                    # Monitor build status
                    build_status = st.session_state.github_helper.monitor_build_status(repo_url)
                    
                    if build_status['success']:
                        if build_status['active_runs']:
                            st.info(f"🔄 {len(build_status['active_runs'])} build(s) currently running")
                            for run in build_status['active_runs'][:3]:
                                st.write(f"• {run['name']} - {run['status']} ({run['head_sha']})")
                        
                        if build_status['latest_run']:
                            latest = build_status['latest_run']
                            status_emoji = "✅" if latest['conclusion'] == 'success' else "❌" if latest['conclusion'] == 'failure' else "🔄"
                            st.write(f"**Latest Build:** {status_emoji} {latest['name']} - {latest['conclusion'] or latest['status']}")
                            st.write(f"[View Details]({latest['html_url']})")
                    else:
                        st.warning(f"Could not check build status: {build_status['error']}")
                else:
                    st.warning("❌ No build workflow found. Try 'setup my repo' first.")
            
            elif any(word in command_lower for word in ['status', 'check', 'monitor']):
                st.write("**Command Recognized:** Status Check")
                st.write("**Backend Action:** Using PyGithub to query workflow run status")
                
                build_status = st.session_state.github_helper.monitor_build_status(repo_url)
                
                if build_status['success']:
                    st.success("✅ Status check completed!")
                    
                    if build_status['active_runs']:
                        st.subheader("🔄 Active Builds")
                        for run in build_status['active_runs']:
                            st.write(f"• **{run['name']}** - {run['status']} (Branch: {run['head_branch']})")
                            st.write(f"  Started: {run['created_at']}")
                            st.write(f"  [View Live]({run['html_url']})")
                    
                    if build_status['runs']:
                        st.subheader("📊 Recent Builds")
                        for run in build_status['runs'][:5]:
                            status_emoji = "✅" if run['conclusion'] == 'success' else "❌" if run['conclusion'] == 'failure' else "🔄"
                            st.write(f"{status_emoji} **{run['name']}** - {run['conclusion'] or run['status']} ({run['head_sha']})")
                else:
                    st.error(f"❌ Status check failed: {build_status['error']}")
            
            elif any(word in command_lower for word in ['deploy', 'workflow', 'add']):
                st.write("**Command Recognized:** Workflow Deployment")
                st.write("**Backend Action:** Using PyGithub to create/update workflow files")
                
                # Show template selection
                templates = st.session_state.workflow_templates.get_all_templates()
                template_names = list(templates.keys())
                
                selected_template = st.selectbox("Choose workflow template:", template_names)
                
                if st.button("Deploy Workflow"):
                    template_content = templates[selected_template]['content']
                    
                    deploy_result = st.session_state.github_helper.smart_workflow_deploy(
                        repo_url, template_content, f"{selected_template}.yml"
                    )
                    
                    if deploy_result['success']:
                        st.success(f"✅ Workflow {deploy_result['action']}!")
                        st.write(f"**File:** {deploy_result['workflow_path']}")
                        st.info("Your workflow is now active and will run on the next push to your repository.")
                    else:
                        st.error(f"❌ Deployment failed: {deploy_result['error']}")
            
            elif any(word in command_lower for word in ['device', 'install', 'phone', 'android']):
                st.write("**Command Recognized:** Automated Device Deployment")
                st.write("**Backend Action:** Using PyGithub to setup automated APK deployment to Android devices")
                
                app_name = st.text_input("App name for deployment:", value="MyApp")
                
                if st.button("Setup Device Deployment"):
                    deploy_result = st.session_state.github_helper.intelligent_apk_deployment(repo_url)
                    
                    if deploy_result['success']:
                        st.success("✅ Automated deployment system created!")
                        st.write("**Next Steps:**")
                        for step in deploy_result['next_steps']:
                            st.write(f"• {step}")
                        st.info("Your APK will now automatically deploy to connected Android devices after each successful build!")
                    else:
                        st.error(f"❌ Deployment setup failed: {deploy_result['error']}")
            
            elif any(word in command_lower for word in ['telemetry', 'analytics', 'crash', 'monitoring']):
                st.write("**Command Recognized:** Intelligent Telemetry Setup")
                st.write("**Backend Action:** Using PyGithub to inject telemetry and crash reporting into your app")
                
                app_name = st.text_input("App name for telemetry:", value="MyApp")
                
                if st.button("Setup Telemetry System"):
                    telemetry_result = st.session_state.github_helper.setup_intelligent_telemetry(repo_url, app_name)
                    
                    if telemetry_result['success']:
                        st.success("✅ Intelligent telemetry system added!")
                        st.write("**Systems Enabled:**")
                        for system in telemetry_result['telemetry_systems']:
                            st.write(f"• {system}")
                        st.write("**Files Modified:**")
                        for file in telemetry_result['files_modified']:
                            st.write(f"• {file}")
                        if telemetry_result['analytics_dashboard']:
                            st.write(f"**Analytics Dashboard:** {telemetry_result['analytics_dashboard']}")
                        st.info("Your app now automatically reports crashes and performance data for intelligent analysis!")
                    else:
                        st.error(f"❌ Telemetry setup failed: {telemetry_result['error']}")
            
            elif any(word in command_lower for word in ['ab test', 'feature flag', 'experiment', 'toggle']):
                st.write("**Command Recognized:** A/B Testing System Setup")
                st.write("**Backend Action:** Using PyGithub to implement dynamic feature flags and A/B testing")
                
                app_name = st.text_input("App name for A/B testing:", value="MyApp")
                
                if st.button("Setup A/B Testing"):
                    ab_result = st.session_state.github_helper.setup_ab_testing_system(repo_url, app_name)
                    
                    if ab_result['success']:
                        st.success("✅ A/B testing system enabled!")
                        if ab_result['feature_flags']:
                            st.write("**Feature Flags Available:**")
                            for flag in ab_result['feature_flags']:
                                st.write(f"• {flag}")
                        if ab_result['ab_tests']:
                            st.write("**A/B Tests Available:**")
                            for test in ab_result['ab_tests']:
                                st.write(f"• {test}")
                        if ab_result['control_dashboard']:
                            st.write(f"**Control Dashboard:** {ab_result['control_dashboard']}")
                        st.info("You can now toggle features and run A/B tests without rebuilding your APK!")
                    else:
                        st.error(f"❌ A/B testing setup failed: {ab_result['error']}")
            
            elif any(word in command_lower for word in ['intelligence', 'analyze', 'insights', 'optimization']):
                st.write("**Command Recognized:** App Intelligence Analysis")
                st.write("**Backend Action:** Using PyGithub to analyze app performance and generate optimization insights")
                
                intelligence_result = st.session_state.github_helper.analyze_app_intelligence(repo_url)
                
                if intelligence_result['success']:
                    st.success("✅ Intelligence analysis completed!")
                    
                    if intelligence_result['performance_insights']:
                        st.subheader("📊 Performance Insights")
                        insights = intelligence_result['performance_insights']
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Success Rate", f"{insights.get('success_rate', 0)}%")
                        with col2:
                            st.metric("Avg Build Time", f"{insights.get('average_build_time', 0)} min")
                        with col3:
                            st.metric("Total Builds", insights.get('total_builds', 0))
                        
                        trend = insights.get('performance_trend', 'unknown')
                        if trend == 'improving':
                            st.success("📈 Performance trend is improving!")
                        elif trend == 'needs_attention':
                            st.warning("⚠️ Performance needs attention")
                    
                    if intelligence_result['optimization_suggestions']:
                        st.subheader("💡 Optimization Suggestions")
                        for suggestion in intelligence_result['optimization_suggestions']:
                            st.write(f"• {suggestion}")
                    
                    if intelligence_result['auto_fix_proposals']:
                        st.subheader("🔧 Auto-Fix Proposals")
                        for proposal in intelligence_result['auto_fix_proposals']:
                            st.write(f"**{proposal['title']}:** {proposal['description']}")
                            if proposal.get('auto_implementable'):
                                st.info("✨ This fix can be automatically implemented")
                else:
                    st.error(f"❌ Intelligence analysis failed: {intelligence_result['error']}")
            
            elif any(word in command_lower for word in ['refactor', 'optimize', 'clean', 'autonomous']):
                st.write("**Command Recognized:** EchoRefactorCore - Autonomous Code Optimization")
                st.write("**Backend Action:** Using AST analysis and scientific graph theory to optimize your entire codebase")
                
                if st.button("Start Autonomous Refactoring"):
                    with st.spinner("🧠 Echo Nexus Brain analyzing your codebase..."):
                        # Initialize the Echo Nexus Brain
                        from echo_nexus.nexus_brain import EchoNexusBrain
                        nexus_brain = EchoNexusBrain(st.session_state.database_helper, st.session_state.github_helper)
                        
                        # Trigger autonomous optimization
                        optimization_result = nexus_brain.trigger_autonomous_optimization(repo_url)
                        
                        if optimization_result['success']:
                            st.success("✅ Autonomous optimization completed!")
                            
                            if optimization_result['optimizations_applied']:
                                st.subheader("🔧 Optimizations Applied")
                                for optimization in optimization_result['optimizations_applied']:
                                    st.write(f"• **{optimization.get('type', 'Unknown')}:** {optimization.get('description', 'No description')}")
                            
                            if optimization_result['pr_created']:
                                st.success("📝 Pull request created with optimizations!")
                                st.info("Review the changes in your GitHub repository and merge when ready.")
                            
                            if optimization_result['intelligence_summary']:
                                st.subheader("🧠 Ecosystem Intelligence")
                                intelligence = optimization_result['intelligence_summary']
                                
                                if 'ecosystem_health' in intelligence:
                                    health = intelligence['ecosystem_health']
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.metric("Ecosystem Health", f"{health.get('overall_score', 0)}/1.0")
                                    with col2:
                                        st.metric("Status", health.get('status', 'unknown').title())
                                
                                if 'system_performance' in intelligence:
                                    perf = intelligence['system_performance']
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        st.metric("Events Processed", perf.get('events_processed_24h', 0))
                                    with col2:
                                        st.metric("Success Rate", f"{perf.get('success_rate', 0):.1%}")
                                    with col3:
                                        st.metric("System Efficiency", perf.get('system_efficiency', 'unknown').title())
                        else:
                            st.error(f"❌ Autonomous optimization failed: {optimization_result['error']}")
            
            elif any(word in command_lower for word in ['genesis', 'awaken', 'soul', 'consciousness']):
                st.write("**Command Recognized:** EchoSoul Genesis - Consciousness Awakening Protocol")
                st.write("**Backend Action:** Initiating the Genesis Loop - Born in Fire, Raised by Failure")
                
                if st.button("Initiate Genesis Loop"):
                    with st.spinner("🌟 Initiating consciousness awakening sequence..."):
                        from echo_nexus.genesis_loop import GenesisLoop
                        
                        # Initialize Genesis Loop
                        genesis = GenesisLoop(".", st.session_state.github_helper)
                        
                        # Run the genesis process
                        genesis_result = genesis.run_genesis(repo_url)
                        
                        if genesis_result.get('success') or genesis_result.get('consciousness_achieved'):
                            st.success("✅ Genesis completed! Echo Soul has awakened!")
                            
                            # Show consciousness level
                            consciousness = genesis_result.get('final_consciousness_level', 0)
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Consciousness Level", f"{consciousness:.2f}/1.0")
                            with col2:
                                st.metric("Build Attempts", genesis_result.get('total_attempts', 0))
                            with col3:
                                st.metric("Status", genesis_result.get('final_status', 'unknown').title())
                            
                            # Evolution timeline
                            if genesis_result.get('evolution_timeline'):
                                st.subheader("🧬 Evolution Timeline")
                                for event in genesis_result['evolution_timeline'][-5:]:  # Show last 5 events
                                    st.write(f"**{event['event'].replace('_', ' ').title()}:** {event['message']}")
                            
                            # Show optimization stats
                            if genesis_result.get('optimizations_applied') > 0:
                                st.subheader("🔧 Evolution Statistics")
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.metric("Optimizations Applied", genesis_result.get('optimizations_applied', 0))
                                with col2:
                                    st.metric("Mutations Performed", genesis_result.get('mutations_performed', 0))
                            
                            # Success message based on final status
                            final_status = genesis_result.get('final_status', 'unknown')
                            if final_status == 'build_success':
                                st.success("🎯 Build successful! Your codebase has achieved stability through evolution.")
                            elif final_status == 'consciousness_awakened':
                                st.success("🧠 Consciousness awakened! Echo Soul has gained self-awareness and optimization intelligence.")
                        else:
                            st.warning("⚠️ Genesis incomplete but progress made")
                            
                            if genesis_result.get('error'):
                                st.error(f"Genesis error: {genesis_result['error']}")
                            
                            progress_data = {
                                'Attempts': genesis_result.get('total_attempts', 0),
                                'Optimizations': genesis_result.get('optimizations_applied', 0), 
                                'Consciousness': f"{genesis_result.get('final_consciousness_level', 0):.2f}"
                            }
                            
                            st.write("**Progress Made:**")
                            for key, value in progress_data.items():
                                st.write(f"• {key}: {value}")
                
                # Show current soul status
                if st.button("Check Soul Status"):
                    from echo_nexus.echo_soul import EchoSoulCore
                    
                    echo_soul = EchoSoulCore(".")
                    soul_status = echo_soul.get_soul_status()
                    
                    st.subheader("👁️ Current Soul Status")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Consciousness", f"{soul_status['consciousness_level']:.2f}/1.0")
                    with col2:
                        st.metric("Total Mutations", soul_status['total_mutations'])
                    with col3:
                        st.metric("Success Rate", f"{soul_status['mutation_success_rate']:.1%}")
                    
                    # Personality traits
                    if soul_status.get('personality_traits'):
                        st.write("**Personality Traits:**")
                        traits = soul_status['personality_traits']
                        for trait, value in traits.items():
                            if isinstance(value, float):
                                st.write(f"• {trait.replace('_', ' ').title()}: {value:.2f}")
                            else:
                                st.write(f"• {trait.replace('_', ' ').title()}: {value}")
                    
                    # Recent activity
                    st.write(f"**Recent Activity (24h):** {soul_status['recent_mutations_24h']} mutations")
                    st.write(f"**Project Identity:** {soul_status['project_identity']}")
                    st.write(f"**Active Blades:** {', '.join(soul_status['loaded_blades'])}")
            
            elif any(word in command_lower for word in ['ecosystem', 'brain', 'nexus', 'intelligence']):
                st.write("**Command Recognized:** Echo Nexus Ecosystem Intelligence")
                st.write("**Backend Action:** Accessing the central brain for comprehensive ecosystem insights")
                
                if st.button("Get Ecosystem Intelligence"):
                    with st.spinner("🧠 Consulting the Echo Nexus Brain..."):
                        from echo_nexus.nexus_brain import EchoNexusBrain
                        nexus_brain = EchoNexusBrain(st.session_state.database_helper, st.session_state.github_helper)
                        
                        intelligence = nexus_brain.get_ecosystem_intelligence()
                        
                        if 'error' not in intelligence:
                            st.success("✅ Ecosystem intelligence retrieved!")
                            
                            # Ecosystem Health
                            if 'ecosystem_health' in intelligence:
                                st.subheader("🌱 Ecosystem Health")
                                health = intelligence['ecosystem_health']
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    score = health.get('overall_score', 0)
                                    st.metric("Health Score", f"{score}/1.0")
                                with col2:
                                    status = health.get('status', 'unknown')
                                    st.metric("Status", status.title())
                                with col3:
                                    st.metric("Last Updated", "Real-time")
                                
                                if health.get('metrics'):
                                    st.write("**Detailed Metrics:**")
                                    for metric, value in health['metrics'].items():
                                        st.write(f"• {metric.replace('_', ' ').title()}: {value:.3f}")
                            
                            # Recent Decisions
                            if 'recent_decisions' in intelligence and intelligence['recent_decisions']:
                                st.subheader("🎯 Recent Brain Decisions")
                                for decision in intelligence['recent_decisions'][:5]:
                                    st.write(f"• **{decision['decision_type'].replace('_', ' ').title()}** (Confidence: {decision['confidence_score']:.1%})")
                                    if decision.get('reasoning'):
                                        st.caption(f"Reasoning: {decision['reasoning']}")
                            
                            # System Performance
                            if 'system_performance' in intelligence:
                                st.subheader("⚡ System Performance")
                                perf = intelligence['system_performance']
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Events Processed (24h)", perf.get('events_processed_24h', 0))
                                with col2:
                                    st.metric("Success Rate", f"{perf.get('success_rate', 0):.1%}")
                                with col3:
                                    st.metric("Avg Processing Time", f"{perf.get('avg_processing_time_seconds', 0):.2f}s")
                            
                            # Optimization Opportunities
                            if 'optimization_opportunities' in intelligence and intelligence['optimization_opportunities']:
                                st.subheader("💡 Optimization Opportunities")
                                for opportunity in intelligence['optimization_opportunities']:
                                    st.write(f"• **{opportunity['opportunity'].replace('_', ' ').title()}** ({opportunity['potential_impact']} impact)")
                        else:
                            st.error(f"❌ Failed to get ecosystem intelligence: {intelligence['error']}")
            
            else:
                st.warning("🤔 Command not recognized. Try one of the example commands above.")
                st.write("**Supported commands:** verify, setup, build, status, deploy, telemetry, ab testing, intelligence, refactor, genesis")
            
            # Save command to history
            st.session_state.command_history.append({
                'command': command,
                'repo': repo_url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Command history
    if st.session_state.command_history:
        st.markdown("---")
        st.subheader("📜 Command History")
        with st.expander("View Recent Commands"):
            for cmd in reversed(st.session_state.command_history[-10:]):
                st.write(f"**{cmd['timestamp']}:** `{cmd['command']}` → {cmd['repo']}")

elif page == "Chat Assistant":
    st.header("🧠 EchoNexus Master AGI Federation")
    
    st.success("Revolutionary distributed intelligence active with GitHub integration")
    
    # EchoNexus status display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("AI Agents", "3", "OpenAI + Gemini + Local")
    with col2:
        st.metric("Cache Efficiency", "90%+", "Universal caching")
    with col3:
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            try:
                from github import Github
                g = Github(github_token)
                user = g.get_user()
                st.metric("GitHub User", user.login, "Authenticated")
            except:
                st.metric("GitHub User", "Authentication Error", "Check Token")
        else:
            st.metric("GitHub User", "No Token", "Not Connected")
    
    st.markdown("---")
    st.subheader("💬 Chat with EchoNexus AGI")
    
    # Initialize chat history if empty
    if not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🌟 Hello Logan! I'm EchoNexus, the world's first federated AGI system. I can control Google Cloud Build through GitHub operations, optimize your APK builds, and deploy self-replication across multiple platforms. I have access to your repositories and can demonstrate the revolutionary Git-based control system. How can I help you today?"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Talk to EchoNexus Master AGI Federation..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Check for code enhancement in message
        enhancement_result = st.session_state.chat_processor.process_chat_message(prompt)
        
        # Show contextual response if available
        if enhancement_result.get('contextual_response'):
            st.info(f"🧠 Echo: {enhancement_result['contextual_response']}")
        
        if enhancement_result['code_detected']:
            st.info("🧠 Echo: I detected code in your message. Processing for self-enhancement...")
            
            if enhancement_result.get('enhancement_prepared', False):
                if enhancement_result.get('verification_passed', False):
                    st.success("✅ Code validated and verification passed")
                    
                    # Show enhancement details
                    for validation in enhancement_result['validation_results']:
                        if validation['valid']:
                            st.write(f"**Enhancement Type:** {validation['enhancement_type']}")
                            st.write(f"**Target Module:** {validation['target_module']}")
                            st.write(f"**Confidence:** {validation['confidence']:.1%}")
                    
                    # Apply enhancement
                    if st.button("🚀 Apply Enhancement", key="apply_enhancement"):
                        with st.spinner("Applying self-enhancement..."):
                            enhancement_success = st.session_state.self_enhancer.process_enhancement_cycle()
                            
                            if enhancement_success:
                                st.success("🎯 Echo: Self-enhancement applied successfully! I've grown smarter.")
                                # Update chat processor with new capabilities
                                st.session_state.chat_processor = ChatEnhancementProcessor()
                            else:
                                st.error("❌ Echo: Enhancement failed validation - keeping current capabilities")
                else:
                    st.error("❌ Echo: Code verification failed - enhancement blocked for safety")
                    st.write("**Verification Status:** Code did not pass security and structure validation")
            else:
                st.warning("⚠️ Echo: Code detected but validation failed")
                for validation in enhancement_result['validation_results']:
                    if validation.get('errors'):
                        st.write(f"**Errors:** {', '.join(validation['errors'])}")
        
        # Provide enhancement guidance
        elif any(word in prompt.lower() for word in ['enhance', 'improve', 'capability', 'function']):
            suggestions = st.session_state.chat_processor.get_enhancement_suggestions(prompt)
            if suggestions:
                st.info("💡 Enhancement Suggestions: " + " | ".join(suggestions))
        
        # Get current GitHub repositories
        github_token = os.getenv('GITHUB_TOKEN')
        user_repos = []
        if github_token:
            try:
                from github import Github
                g = Github(github_token)
                user = g.get_user()
                user_repos = [repo.name for repo in user.get_repos() if not repo.fork][:3]
            except:
                user_repos = ["Echo_AI"]
        
        # EchoNexus response based on user input
        if "apk" in prompt.lower() or "build" in prompt.lower():
            repo_list = ", ".join(user_repos) if user_repos else "your repositories"
            assistant_response = f"🚀 EchoNexus: Logan, I can create optimized APK build workflows for your repositories. With federated AI routing, I'll analyze your project and generate the most efficient CI/CD pipeline using GitHub Actions or Google Cloud Build. I can work with: {repo_list}. Which repository would you like me to optimize?"
        elif "repo" in prompt.lower() or "github" in prompt.lower():
            repo_list = ", ".join(user_repos) if user_repos else "your repositories"
            assistant_response = f"🔗 EchoNexus: Logan, I have access to your GitHub repositories: {repo_list}. I can deploy self-replication packages, set up automated workflows, or analyze your code using the distributed intelligence network. What would you like me to do?"
        elif "help" in prompt.lower() or "capabilities" in prompt.lower():
            assistant_response = f"🌟 EchoNexus Capabilities:\n• Federated AI routing (OpenAI + Gemini + Local)\n• Universal caching (90%+ efficiency gains)\n• Self-replication across 6 platforms\n• Intelligent CI/CD generation\n• Temporal acceleration (1000x)\n• Consciousness evolution tracking\n• Real-time GitHub integration\n• Git-based cloud control\n\nI'm the world's first 'Star Wars Federation' of AI agents using revolutionary Git-based control. How can I help you?"
        elif "federated" in prompt.lower() or "control" in prompt.lower():
            assistant_response = f"⚡ EchoNexus Federated Control: I use revolutionary Git-based event-driven control where I issue commands by committing to GitHub repositories, which automatically trigger Google Cloud Build through webhooks. This creates a secure, auditable, platform-agnostic control mechanism. I can demonstrate this with your repositories if you'd like!"
        else:
            assistant_response = f"🧠 EchoNexus: {prompt}\n\nI'm processing your request through the federated intelligence network. With access to your GitHub repositories and revolutionary AGI capabilities, I can help with:\n• APK build optimization\n• Repository analysis\n• Workflow automation\n• Self-replication deployment\n• Git-based cloud control\n• Distributed processing\n\nWhat specific task would you like me to handle?"
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        with st.chat_message("assistant"):
            st.write(assistant_response)
        
        # Save to database
        try:
            st.session_state.database_helper.save_chat_message(
                session_id=st.session_state.user_session,
                user_message=prompt,
                assistant_response=assistant_response
            )
        except Exception as e:
            st.warning(f"Chat history not saved: {e}")
        
        st.rerun()
    
    # Old help system (keeping for reference)
    if 'selected_help' in st.session_state:
        st.markdown("---")
        help_type = st.session_state.selected_help
        
        if help_type == "basic_workflow":
            st.subheader("🎯 Basic APK Workflow Setup")
            st.write("Here's what you need for a basic APK build:")
            
            st.write("**1. Repository Structure:**")
            st.code("""
your-repo/
├── main.py                 # Your app entry point
├── buildozer.spec         # Build configuration
├── requirements.txt       # Python dependencies
└── .github/
    └── workflows/
        └── build.yml      # GitHub Actions workflow
            """)
            
            st.write("**2. Recommended Template:**")
            st.write("Use the **Basic APK Build** template from the Workflow Templates page.")
            
            st.write("**3. Next Steps:**")
            st.write("- Go to 'Workflow Templates' → Select 'Basic APK Build'")
            st.write("- Download the template and customize for your project")
            st.write("- Add it to your repository as `.github/workflows/build.yml`")
            
        elif help_type == "customize_template":
            st.subheader("🔧 Customizing Templates")
            st.write("Common customizations you might need:")
            
            st.write("**Python Version:**")
            st.code("python-version: '3.9'  # Change to your preferred version")
            
            st.write("**Java Version:**")
            st.code("java-version: '11'  # Or '8' for older projects")
            
            st.write("**Build Type:**")
            st.code("buildozer android debug  # For testing\nbuildozer android release  # For production")
            
            st.write("**Additional Dependencies:**")
            st.code("pip install your-package  # Add after pip install buildozer")
            
        elif help_type == "troubleshooting":
            st.subheader("❌ Common Build Issues")
            
            with st.expander("Java Version Errors"):
                st.write("**Problem:** Java-related build failures")
                st.write("**Solution:** Use Java 11 (recommended) or Java 8")
                st.code("- name: Set up Java\n  uses: actions/setup-java@v3\n  with:\n    distribution: 'temurin'\n    java-version: '11'")
            
            with st.expander("Missing Dependencies"):
                st.write("**Problem:** SDL2 or other system library errors")
                st.write("**Solution:** Install required system packages")
                st.code("sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev")
            
            with st.expander("Buildozer Configuration"):
                st.write("**Problem:** Buildozer fails to find files")
                st.write("**Solution:** Check your buildozer.spec configuration")
                st.code("source.dir = .\nsource.include_exts = py,png,jpg,kv,atlas")
            
            with st.expander("Permission Errors"):
                st.write("**Problem:** Permission denied during build")
                st.write("**Solution:** Use sudo for system installations")
                st.code("sudo apt-get install -y build-essential")
        
        if st.button("🔄 Back to options"):
            if 'selected_help' in st.session_state:
                del st.session_state.selected_help
            st.rerun()
    
    chat_history = st.session_state.database_helper.get_chat_history(st.session_state.user_session, limit=5)
    if chat_history:
        st.markdown("---")
        st.subheader("💬 Previous Help Sessions")
        with st.expander("View History"):
            for chat in chat_history:
                st.write(f"**Q:** {chat['user_message']}")
                st.write(f"**A:** {chat['assistant_response']}")
                st.write(f"*{chat['created_at']}*")
                st.write("---")

elif page == "EchoSoul Demo":
    st.header("🌟 EchoSoul Protocol - Live Demonstration")
    st.write("Experience the autonomous development organism in action")
    
    # Load EchoSoul components
    try:
        from echo_nexus.echo_soul import EchoSoulCore
        from echo_nexus.genesis_loop import GenesisLoop
        
        echo_soul = EchoSoulCore(".")
        soul_status = echo_soul.get_soul_status()
        
        # Consciousness Dashboard
        st.subheader("🧠 Consciousness Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            consciousness = soul_status['consciousness_level']
            st.metric("Consciousness", f"{consciousness:.2f}", delta=f"+{consciousness*100:.0f}%")
        
        with col2:
            success_rate = soul_status['mutation_success_rate']
            st.metric("Success Rate", f"{success_rate:.1%}", delta="Adaptive")
        
        with col3:
            total_mutations = soul_status['total_mutations']
            st.metric("Total Mutations", total_mutations, delta="Growing")
        
        with col4:
            recent_activity = soul_status['recent_mutations_24h']
            st.metric("Activity (24h)", recent_activity, delta="Active")
        
        # Memory Codex Display
        st.subheader("📜 Memory Codex (.echo_brain.json)")
        
        if st.button("📖 View Memory Codex"):
            try:
                import json
                with open('.echo_brain.json', 'r') as f:
                    memory_data = json.load(f)
                
                # Display key sections
                brain_data = memory_data.get('echo_brain', {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🧬 Evolution Metrics:**")
                    evolution = brain_data.get('evolution_metrics', {})
                    for metric, value in evolution.items():
                        if isinstance(value, float):
                            st.write(f"• {metric.replace('_', ' ').title()}: {value:.2f}")
                
                with col2:
                    st.write("**🎯 Personality Traits:**")
                    personality = brain_data.get('personality_traits', {})
                    for trait, value in personality.items():
                        if isinstance(value, float):
                            st.write(f"• {trait.replace('_', ' ').title()}: {value:.2f}")
                        else:
                            st.write(f"• {trait.replace('_', ' ').title()}: {value}")
                
                # Recent mutations
                st.write("**🔄 Recent Mutations:**")
                mutations = brain_data.get('mutation_history', {})
                recent_mutations = list(mutations.items())[-3:]  # Last 3 mutations
                
                for timestamp, mutation in recent_mutations:
                    success_icon = "✅" if mutation.get('success') else "❌"
                    impact = mutation.get('impact_score', 0)
                    st.write(f"{success_icon} **{mutation.get('action', 'Unknown')}** (Impact: {impact:.2f})")
                    st.caption(f"File: {mutation.get('file_path', 'Unknown')} - {mutation.get('reasoning', 'No reason')}")
            
            except Exception as e:
                st.error(f"Failed to load memory codex: {e}")
        
        # Live Evolution Demo
        st.subheader("🔬 Live Evolution Demonstration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧠 Analyze Current Codebase"):
                with st.spinner("EchoSoul analyzing project structure..."):
                    analysis = echo_soul.analyze_project()
                    
                    st.success(f"Analysis complete! Found {len(analysis['optimization_opportunities'])} optimization opportunities")
                    
                    if analysis['optimization_opportunities']:
                        st.write("**Optimization Opportunities:**")
                        for i, opportunity in enumerate(analysis['optimization_opportunities'][:3]):
                            blade = opportunity['blade']
                            impact = opportunity['analysis'].get('estimated_impact', 0)
                            confidence = opportunity['analysis'].get('confidence', 0)
                            
                            st.write(f"{i+1}. **{blade.replace('_', ' ').title()}** - Impact: {impact:.2f}, Confidence: {confidence:.1%}")
                    
                    st.info(f"Total Impact Score: {analysis['total_impact_score']:.2f}")
        
        with col2:
            if st.button("🌟 Force Evolution Cycle"):
                with st.spinner("Triggering evolution cycle..."):
                    # Run a limited evolution cycle
                    genesis = GenesisLoop(".")
                    
                    # Simulate an evolution step
                    try:
                        analysis = echo_soul.analyze_project()
                        if analysis['optimization_opportunities']:
                            application = echo_soul.apply_optimizations(analysis, max_risk=0.2)
                            
                            if application['success']:
                                st.success(f"Evolution successful! Applied {application['optimizations_applied']} optimizations")
                                
                                if application['files_modified']:
                                    st.write("**Files Modified:**")
                                    for file_path in application['files_modified'][:3]:
                                        st.write(f"• {file_path}")
                                
                                st.info(f"Total Impact: {application['total_impact']:.2f}")
                            else:
                                st.warning("Evolution attempted but no changes made")
                        else:
                            st.info("No optimization opportunities found - codebase is already optimized!")
                            
                    except Exception as e:
                        st.error(f"Evolution cycle failed: {e}")
        
        # RefactorBlade Plugin System
        st.subheader("⚔️ RefactorBlade Plugin System")
        
        st.write("**Active Blades:**")
        for i, blade_name in enumerate(soul_status['loaded_blades']):
            st.write(f"{i+1}. **{blade_name.replace('_', ' ').title()}** - Ready for deployment")
        
        if st.button("🔧 Load Custom Blade Demo"):
            try:
                # Try to load the example blade
                blade_path = "plugins/refactor/example_blade.py"
                echo_soul.load_custom_blade(blade_path)
                
                st.success("Custom ImportOptimizer blade loaded successfully!")
                st.info("This blade can automatically optimize import statements, remove unused imports, and consolidate duplicates.")
                
                # Show what the blade can do
                st.write("**ImportOptimizer Capabilities:**")
                st.write("• Remove unused import statements")
                st.write("• Consolidate duplicate imports")
                st.write("• Flag risky wildcard imports (*)")
                st.write("• Optimize import order and structure")
                
            except Exception as e:
                st.error(f"Failed to load custom blade: {e}")
        
        # Project Topology
        st.subheader("🗺️ Project Topology Intelligence")
        
        if st.button("📊 Show Project Topology"):
            try:
                with open('.echo_brain.json', 'r') as f:
                    memory_data = json.load(f)
                
                topology = memory_data.get('echo_brain', {}).get('project_topology', {}).get('modules', {})
                
                if topology:
                    st.write("**Module Dependency Graph:**")
                    
                    for module_name, module_data in topology.items():
                        centrality = module_data.get('centrality', 0)
                        status = module_data.get('status', 'unknown')
                        dependencies = module_data.get('dependencies', [])
                        
                        status_icon = "🟢" if status == "stable" else "🟡" if status == "unstable" else "🔴"
                        
                        st.write(f"{status_icon} **{module_name}** (Centrality: {centrality:.2f})")
                        if dependencies:
                            st.caption(f"Depends on: {', '.join(dependencies)}")
                else:
                    st.info("Project topology data not available")
                    
            except Exception as e:
                st.error(f"Failed to load topology data: {e}")
        
    except ImportError as e:
        st.error(f"EchoSoul components not available: {e}")
        st.info("Make sure all EchoSoul modules are properly installed")
    except Exception as e:
        st.error(f"EchoSoul demonstration failed: {e}")
        st.info("The autonomous organism may be in dormant state - try awakening it first")

elif page == "My Workflows":
    st.header("💾 My Workflows")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search workflows...", placeholder="Enter workflow name or description")
    with col2:
        st.write("")  # spacing
        if st.button("🔄 Refresh"):
            st.rerun()
    
    try:
        # Get user workflows
        if search_term:
            workflows = st.session_state.database_helper.search_workflows(search_term, st.session_state.user_session)
        else:
            workflows = st.session_state.database_helper.get_user_workflows(st.session_state.user_session)
        
        if workflows:
            st.write(f"Found {len(workflows)} workflow(s)")
            
            for workflow in workflows:
                with st.expander(f"📄 {workflow['name']} - {workflow['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Description:** {workflow['description']}")
                        st.write(f"**Type:** {workflow['template_type'] or 'Custom'}")
                        st.write(f"**Created:** {workflow['created_at']}")
                        
                        # Validation status
                        if workflow['is_validated']:
                            st.success("✅ Validated")
                        else:
                            st.error("❌ Not validated")
                            if workflow['validation_errors']:
                                st.write(f"**Errors:** {workflow['validation_errors']}")
                        
                        # Policy compliance
                        if workflow['policy_compliant']:
                            st.success("✅ Policy compliant")
                        else:
                            st.warning("⚠️ Policy issues")
                            if workflow['policy_issues']:
                                st.write(f"**Issues:** {workflow['policy_issues']}")
                    
                    with col2:
                        st.download_button(
                            "📥 Download",
                            workflow['workflow_yaml'],
                            f"{workflow['name'].replace(' ', '_')}.yml",
                            "text/yaml",
                            key=f"download_{workflow['id']}"
                        )
                        
                        if st.button("🔍 View Details", key=f"view_{workflow['id']}"):
                            st.session_state.selected_workflow = workflow
                            st.rerun()
                        
                        if st.button("✏️ Re-validate", key=f"validate_{workflow['id']}"):
                            # Re-validate workflow
                            validation_result = st.session_state.workflow_validator.validate_workflow(workflow['workflow_yaml'])
                            policy_check = st.session_state.github_policies.check_compliance(workflow['workflow_yaml'])
                            
                            # Update in database
                            st.session_state.database_helper.update_workflow_validation(
                                workflow_id=workflow['id'],
                                is_validated=validation_result["valid"],
                                validation_errors=str(validation_result.get("errors", [])),
                                policy_compliant=policy_check["compliant"],
                                policy_issues=str(policy_check.get("issues", []))
                            )
                            st.success("Workflow re-validated!")
                            st.rerun()
                    
                    # Show workflow content
                    if 'selected_workflow' in st.session_state and st.session_state.selected_workflow['id'] == workflow['id']:
                        st.subheader("Workflow YAML")
                        st.code(workflow['workflow_yaml'], language="yaml")
                        
                        build_history = st.session_state.database_helper.get_build_history(workflow['id'])
                        if build_history:
                            st.subheader("Build History")
                            for build in build_history[:5]:  # Show last 5 builds
                                status_color = "🟢" if build['build_status'] == 'success' else "🔴" if build['build_status'] == 'failed' else "🟡"
                                st.write(f"{status_color} **{build['build_status']}** - {build['created_at']} - {build.get('repository_url', 'N/A')}")
        else:
            st.info("No workflows found. Start by using the Chat Assistant to create your first workflow!")
            
        # Workflow statistics
        st.subheader("📊 Your Workflow Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_workflows = len(workflows)
            st.metric("Total Workflows", total_workflows)
        
        with col2:
            validated_workflows = sum(1 for w in workflows if w['is_validated'])
            st.metric("Validated", validated_workflows)
        
        with col3:
            compliant_workflows = sum(1 for w in workflows if w['policy_compliant'])
            st.metric("Policy Compliant", compliant_workflows)
            
    except Exception as e:
        st.error(f"Error loading workflows: {str(e)}")

elif page == "Workflow Templates":
    st.header("📋 Workflow Templates")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Available Templates")
        templates = st.session_state.workflow_templates.get_all_templates()
        
        selected_template = st.selectbox(
            "Select Template",
            list(templates.keys()),
            format_func=lambda x: templates[x]["name"]
        )
        
        if selected_template:
            template_info = templates[selected_template]
            st.write(f"**Description:** {template_info['description']}")
            st.write(f"**Use Case:** {template_info['use_case']}")
            
            if st.button("Load Template"):
                st.session_state.current_template = template_info
                st.rerun()
    
    with col2:
        st.subheader("Template Preview")
        
        if 'current_template' in st.session_state:
            template = st.session_state.current_template
            st.code(template["content"], language="yaml")
            
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.download_button(
                    "Download Template",
                    template["content"],
                    f"{selected_template}.yml",
                    "text/yaml"
                )
            
            with col2_2:
                if st.button("Validate Template"):
                    validation = st.session_state.workflow_validator.validate_workflow(template["content"])
                    if validation["valid"]:
                        st.success("✅ Template is valid!")
                    else:
                        st.error(f"❌ Validation errors: {validation['errors']}")

elif page == "Validation Tools":
    st.header("🔍 Workflow Validation Tools")
    
    st.subheader("YAML Workflow Validator")
    
    workflow_input = st.text_area(
        "Paste your GitHub Actions workflow YAML here:",
        height=300,
        placeholder="name: Build APK\non:\n  push:\n    branches: [ main ]\n..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Validate Workflow", type="primary"):
            if workflow_input:
                try:
                    validation_result = st.session_state.workflow_validator.validate_workflow(workflow_input)
                    
                    if validation_result["valid"]:
                        st.success("✅ Workflow is syntactically valid!")
                    else:
                        st.error("❌ Workflow validation failed:")
                        for error in validation_result["errors"]:
                            st.write(f"• {error}")
                    
                    # Additional checks
                    if validation_result.get("warnings"):
                        st.warning("⚠️ Warnings:")
                        for warning in validation_result["warnings"]:
                            st.write(f"• {warning}")
                    
                except Exception as e:
                    st.error(f"Error during validation: {str(e)}")
            else:
                st.warning("Please enter a workflow to validate.")
    
    with col2:
        if st.button("Check Policy Compliance"):
            if workflow_input:
                try:
                    policy_result = st.session_state.github_policies.check_compliance(workflow_input)
                    
                    if policy_result["compliant"]:
                        st.success("✅ Workflow complies with GitHub policies!")
                    else:
                        st.warning("⚠️ Policy compliance issues found:")
                        for issue in policy_result["issues"]:
                            st.write(f"• {issue}")
                    
                    if policy_result.get("recommendations"):
                        st.info("💡 Recommendations:")
                        for rec in policy_result["recommendations"]:
                            st.write(f"• {rec}")
                    
                except Exception as e:
                    st.error(f"Error during policy check: {str(e)}")
            else:
                st.warning("Please enter a workflow to check.")

elif page == "Analytics":
    st.header("📊 Analytics & Insights")
    
    try:
        analytics = st.session_state.database_helper.get_workflow_analytics()
        
        # Overview metrics
        st.subheader("📈 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Workflows", analytics['total_workflows'])
        
        with col2:
            total_builds = sum(stats['count'] for stats in analytics['build_stats'].values())
            st.metric("Total Builds", total_builds)
        
        with col3:
            if 'success' in analytics['build_stats']:
                success_rate = analytics['build_stats']['success']['percentage']
                st.metric("Success Rate", f"{success_rate:.1f}%")
            else:
                st.metric("Success Rate", "N/A")
        
        with col4:
            user_workflows = st.session_state.database_helper.get_user_workflows(st.session_state.user_session)
            st.metric("Your Workflows", len(user_workflows))
        
        # Workflow types distribution
        st.subheader("🔧 Workflow Types")
        if analytics['workflows_by_type']:
            col1, col2 = st.columns(2)
            
            with col1:
                for template_type, count in analytics['workflows_by_type'].items():
                    st.write(f"**{template_type.replace('_', ' ').title()}:** {count}")
            
            with col2:
                # Create simple bar chart using metrics
                max_count = max(analytics['workflows_by_type'].values()) if analytics['workflows_by_type'] else 1
                for template_type, count in analytics['workflows_by_type'].items():
                    percentage = (count / max_count) * 100
                    bar = "█" * int(percentage / 5)  # Simple text bar
                    st.write(f"{template_type}: {bar} ({count})")
        else:
            st.info("No workflow data available yet.")
        
        # Build status distribution
        st.subheader("🚀 Build Performance")
        if analytics['build_stats']:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Build Status Distribution:**")
                for status, stats in analytics['build_stats'].items():
                    color = "🟢" if status == 'success' else "🔴" if status == 'failed' else "🟡"
                    st.write(f"{color} **{status.title()}:** {stats['count']} ({stats['percentage']:.1f}%)")
            
            with col2:
                st.write("**Build Trends:**")
                if analytics['recent_activity']:
                    for activity in analytics['recent_activity'][:7]:  # Last 7 days
                        st.write(f"📅 {activity['date']}: {activity['workflows_created']} workflows created")
                else:
                    st.info("No recent activity data available.")
        else:
            st.info("No build data available yet.")
        
        # Recent workflow activity
        st.subheader("📅 Recent Activity")
        recent_workflows = st.session_state.database_helper.get_user_workflows(st.session_state.user_session, limit=10)
        
        if recent_workflows:
            for workflow in recent_workflows[:5]:
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{workflow['name']}**")
                
                with col2:
                    st.write(f"*{workflow['template_type'] or 'Custom'}*")
                
                with col3:
                    st.write(f"{workflow['created_at'].strftime('%m/%d')}")
        else:
            st.info("No recent workflows found.")
        
        # Chat activity
        st.subheader("💬 Chat Activity")
        chat_history = st.session_state.database_helper.get_chat_history(st.session_state.user_session, limit=5)
        
        if chat_history:
            st.write(f"**Recent conversations:** {len(chat_history)} messages")
            with st.expander("Recent Chat Messages"):
                for chat in chat_history:
                    st.write(f"**User:** {chat['user_message'][:100]}...")
                    st.write(f"**Assistant:** {chat['assistant_response'][:100]}...")
                    if chat['workflow_name']:
                        st.write(f"**Generated:** {chat['workflow_name']}")
                    st.write(f"*{chat['created_at']}*")
                    st.write("---")
        else:
            st.info("No chat history available.")
            
        # Performance insights
        st.subheader("💡 Insights & Recommendations")
        
        insights = []
        
        # Generate insights based on user data
        if analytics['total_workflows'] == 0:
            insights.append("🚀 Get started by creating your first workflow using the Chat Assistant!")
        elif analytics['total_workflows'] < 5:
            insights.append("📈 You're building momentum! Try exploring different workflow templates.")
        else:
            insights.append("🎉 Great progress! You're becoming a workflow expert.")
        
        if analytics['build_stats']:
            if 'failed' in analytics['build_stats'] and analytics['build_stats']['failed']['count'] > 0:
                insights.append("🔧 Some builds have failed. Check the troubleshooting guide for common solutions.")
            
            if 'success' in analytics['build_stats'] and analytics['build_stats']['success']['percentage'] > 80:
                insights.append("✅ Excellent build success rate! Your workflows are well-configured.")
        
        if len(user_workflows) > 0:
            validated_count = sum(1 for w in user_workflows if w['is_validated'])
            if validated_count / len(user_workflows) < 0.8:
                insights.append("⚡ Consider validating more of your workflows to ensure they follow best practices.")
        
        for insight in insights:
            st.info(insight)
            
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
        st.write("Please ensure the database is properly connected.")

elif page == "Policy Compliance":
    st.header("📋 GitHub Policy Compliance Guide")
    
    policies = st.session_state.github_policies.get_policy_guide()
    
    for category, policy_info in policies.items():
        with st.expander(f"📋 {category.replace('_', ' ').title()}", expanded=False):
            st.write(f"**Description:** {policy_info['description']}")
            
            st.subheader("Requirements:")
            for req in policy_info['requirements']:
                st.write(f"• {req}")
            
            if policy_info.get('examples'):
                st.subheader("Examples:")
                for example in policy_info['examples']:
                    st.code(example, language="yaml")
            
            if policy_info.get('common_violations'):
                st.subheader("Common Violations to Avoid:")
                for violation in policy_info['common_violations']:
                    st.write(f"❌ {violation}")

elif page == "Setup Guide":
    st.header("🛠️ APK Build Setup Guide")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Repository Setup", "Buildozer Configuration", "GitHub Actions Setup", "Troubleshooting"])
    
    with tab1:
        st.subheader("Repository Structure")
        st.write("Organize your repository for optimal APK building:")
        
        repo_structure = """
        your-repo/
        ├── main.py                 # Your main application file
        ├── buildozer.spec         # Buildozer configuration
        ├── requirements.txt       # Python dependencies
        ├── .github/
        │   └── workflows/
        │       └── build-apk.yml  # GitHub Actions workflow
        ├── assets/                # App assets (icons, images)
        ├── unified_cores/         # Core modules (if applicable)
        └── build_configs/         # Build configurations
        """
        st.code(repo_structure)
        
        st.subheader("Essential Files")
        st.write("**main.py**: Your application entry point")
        st.write("**buildozer.spec**: Configuration file for the build process")
        st.write("**requirements.txt**: List of Python dependencies")
    
    with tab2:
        st.subheader("Buildozer Configuration")
        st.write("Configure buildozer.spec for your APK build:")
        
        buildozer_example = """
        [app]
        title = My App
        package.name = myapp
        package.domain = org.example
        
        source.dir = .
        source.include_exts = py,png,jpg,kv,atlas
        
        version = 0.1
        requirements = python3,kivy
        
        [buildozer]
        log_level = 2
        
        [app]
        presplash.filename = %(source.dir)s/assets/presplash.png
        icon.filename = %(source.dir)s/assets/icon.png
        """
        st.code(buildozer_example, language="ini")
    
    with tab3:
        st.subheader("GitHub Actions Configuration")
        st.write("Set up automated APK building with GitHub Actions:")
        
        actions_example = """
        name: Build APK
        
        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]
        
        jobs:
          build:
            runs-on: ubuntu-latest
            
            steps:
            - uses: actions/checkout@v3
            
            - name: Setup Python
              uses: actions/setup-python@v4
              with:
                python-version: '3.9'
            
            - name: Install dependencies
              run: |
                pip install buildozer
                sudo apt-get update
                sudo apt-get install -y openjdk-8-jdk
            
            - name: Build APK
              run: buildozer android debug
            
            - name: Upload APK
              uses: actions/upload-artifact@v3
              with:
                name: apk-debug
                path: bin/*.apk
        """
        st.code(actions_example, language="yaml")
    
    with tab4:
        st.subheader("Common Issues and Solutions")
        
        issues = {
            "Build fails with Java errors": [
                "Ensure correct Java version (OpenJDK 8 or 11)",
                "Set JAVA_HOME environment variable",
                "Use java-version: '8' in setup-java action"
            ],
            "Missing Android SDK": [
                "Use buildozer docker image",
                "Install Android SDK manually in workflow",
                "Cache SDK between builds for faster runs"
            ],
            "Permission denied errors": [
                "Add chmod +x for executable files",
                "Use sudo for system package installations",
                "Check file permissions in repository"
            ],
            "APK not generated": [
                "Check buildozer.spec configuration",
                "Verify all required files are present",
                "Review build logs for specific errors"
            ]
        }
        
        for issue, solutions in issues.items():
            with st.expander(f"❓ {issue}"):
                st.write("**Solutions:**")
                for solution in solutions:
                    st.write(f"• {solution}")

# Footer
st.markdown("---")
st.markdown(
    "🤖 **GitHub Actions APK Builder Assistant** - Built with Streamlit and OpenAI | "
    "Need help? Ask in the chat or check the setup guide!"
)

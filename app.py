import streamlit as st
import yaml
import json
import os
from datetime import datetime
import hashlib
# from utils.openai_helper import WorkflowAssistant  # Removed OpenAI dependency
from utils.workflow_validator import WorkflowValidator
from utils.github_helper import GitHubHelper
from utils.database_helper import DatabaseHelper
from templates.workflow_templates import WorkflowTemplates
from data.policies import GitHubPolicies

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
# if 'workflow_assistant' not in st.session_state:
    # st.session_state.workflow_assistant = WorkflowAssistant()  # Removed OpenAI dependency
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
if 'user_session' not in st.session_state:
    # Create unique session ID based on session state
    session_data = str(st.session_state).encode()
    st.session_state.user_session = hashlib.md5(session_data).hexdigest()[:16]

st.set_page_config(
    page_title="GitHub Actions APK Builder Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GitHub Actions APK Builder Assistant")
st.subheader("Interactive AI assistant for creating and troubleshooting GitHub Actions workflows for APK building")

# Sidebar for navigation and settings
with st.sidebar:
    st.header("Navigation")
    page = st.selectbox(
        "Select Page",
        ["Command Builder", "Chat Assistant", "My Workflows", "Workflow Templates", "Validation Tools", "Policy Compliance", "Analytics", "Setup Guide"]
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

if page == "Command Builder":
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
                
                # Extract username if specified in command
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
                
                # Check for workflow files
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
                st.write("**Supported commands:** verify, setup, build, status, deploy, telemetry, ab testing, intelligence")
            
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
    st.header("🛠️ Workflow Assistant (Template-Based)")
    
    st.info("💡 AI features are disabled. Use this page to get help with templates and guidance!")
    
    # Quick help sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Quick Start")
        if st.button("🎯 I need a basic APK workflow"):
            st.session_state.selected_help = "basic_workflow"
            st.rerun()
        
        if st.button("🔧 I want to customize a template"):
            st.session_state.selected_help = "customize_template"
            st.rerun()
        
        if st.button("❌ My build is failing"):
            st.session_state.selected_help = "troubleshooting"
            st.rerun()
    
    with col2:
        st.subheader("📋 Resources")
        if st.button("📖 View all templates"):
            st.session_state.go_to_page = "Workflow Templates"
            st.rerun()
        
        if st.button("🔍 Validate my workflow"):
            st.session_state.go_to_page = "Validation Tools"
            st.rerun()
        
        if st.button("📜 Check policy compliance"):
            st.session_state.go_to_page = "Policy Compliance"
            st.rerun()
    
    # Handle page navigation
    if 'go_to_page' in st.session_state:
        page = st.session_state.go_to_page
        del st.session_state.go_to_page
        st.rerun()
    
    # Display contextual help
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
    
    # Show recent chat history if any
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
                        
                        # Get build history for this workflow
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
    
    # Text area for workflow input
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

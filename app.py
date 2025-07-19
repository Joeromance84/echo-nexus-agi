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
        ["Chat Assistant", "My Workflows", "Workflow Templates", "Validation Tools", "Policy Compliance", "Analytics", "Setup Guide"]
    )
    
    st.header("Settings")
    
    # App mode (without AI dependency)
    st.write("🤖 Mode: Template & Validation Based")
    st.info("AI features disabled - using pre-built templates and validation tools")
    
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

if page == "Chat Assistant":
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

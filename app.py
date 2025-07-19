import streamlit as st
import yaml
import json
import os
from datetime import datetime
from utils.openai_helper import WorkflowAssistant
from utils.workflow_validator import WorkflowValidator
from utils.github_helper import GitHubHelper
from templates.workflow_templates import WorkflowTemplates
from data.policies import GitHubPolicies

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'workflow_assistant' not in st.session_state:
    st.session_state.workflow_assistant = WorkflowAssistant()
if 'workflow_validator' not in st.session_state:
    st.session_state.workflow_validator = WorkflowValidator()
if 'github_helper' not in st.session_state:
    st.session_state.github_helper = GitHubHelper()
if 'workflow_templates' not in st.session_state:
    st.session_state.workflow_templates = WorkflowTemplates()
if 'github_policies' not in st.session_state:
    st.session_state.github_policies = GitHubPolicies()

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
        ["Chat Assistant", "Workflow Templates", "Validation Tools", "Policy Compliance", "Setup Guide"]
    )
    
    st.header("Settings")
    api_key_status = "✅ Connected" if os.getenv("OPENAI_API_KEY") else "❌ Not Connected"
    st.write(f"OpenAI API: {api_key_status}")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if page == "Chat Assistant":
    st.header("💬 Interactive Workflow Assistant")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "workflow" in message and message["workflow"]:
                    st.code(message["workflow"], language="yaml")
                    st.download_button(
                        "Download Workflow",
                        message["workflow"],
                        f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml",
                        "text/yaml"
                    )

    # Chat input
    if prompt := st.chat_input("Ask about GitHub Actions workflows for APK building..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.workflow_assistant.process_request(prompt)
                    
                    st.write(response["message"])
                    
                    workflow_yaml = None
                    if response.get("workflow"):
                        workflow_yaml = response["workflow"]
                        st.code(workflow_yaml, language="yaml")
                        
                        # Validate workflow
                        validation_result = st.session_state.workflow_validator.validate_workflow(workflow_yaml)
                        if validation_result["valid"]:
                            st.success("✅ Workflow is valid!")
                        else:
                            st.error(f"❌ Workflow validation failed: {validation_result['errors']}")
                        
                        # Check policy compliance
                        policy_check = st.session_state.github_policies.check_compliance(workflow_yaml)
                        if policy_check["compliant"]:
                            st.success("✅ Workflow complies with GitHub policies!")
                        else:
                            st.warning(f"⚠️ Policy concerns: {policy_check['issues']}")
                        
                        st.download_button(
                            "Download Workflow",
                            workflow_yaml,
                            f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml",
                            "text/yaml"
                        )
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["message"],
                        "workflow": workflow_yaml
                    })
                    
                except Exception as e:
                    error_msg = f"Error processing request: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "workflow": None
                    })

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

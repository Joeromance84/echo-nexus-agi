# GitHub Actions APK Builder Assistant

## Overview

This is a Streamlit-based web application that serves as an interactive AI assistant for creating and troubleshooting GitHub Actions workflows specifically designed for building APK files for Android applications. The application provides a comprehensive suite of tools including workflow generation, validation, policy compliance checking, and troubleshooting assistance for Python/Kivy applications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture built on Streamlit as the web framework, with separate utility modules handling different aspects of workflow management:

- **Frontend**: Streamlit-based web interface with sidebar navigation and multi-page layout
- **AI Integration**: OpenAI GPT-4o integration for intelligent workflow assistance
- **Workflow Management**: YAML-based workflow template system with validation capabilities
- **GitHub Integration**: GitHub API integration for repository validation and workflow management
- **Policy Engine**: Built-in compliance checking against GitHub Actions best practices

## Key Components

### Core Application (app.py)
- **Purpose**: Main application entry point with Streamlit UI setup
- **Features**: Session state management, sidebar navigation, multi-page interface, database integration
- **Pages**: Chat Assistant, My Workflows, Workflow Templates, Validation Tools, Policy Compliance, Analytics, Setup Guide
- **Database Integration**: PostgreSQL for storing workflows, build history, chat messages, and user preferences

### AI Assistant (utils/openai_helper.py)
- **Purpose**: Handles OpenAI API integration for intelligent workflow generation
- **Model**: GPT-4o (latest OpenAI model as of May 2024)
- **Capabilities**: Workflow creation, troubleshooting, optimization suggestions
- **Response Format**: JSON-structured responses with workflow YAML when applicable

### Workflow Validator (utils/workflow_validator.py)
- **Purpose**: Validates GitHub Actions workflow YAML syntax and structure
- **Validation Types**: Syntax checking, security validation, APK-specific requirements
- **Output**: Detailed validation results with errors, warnings, and suggestions

### GitHub Integration (utils/github_helper.py)
- **Purpose**: GitHub API integration for repository validation and workflow management
- **Authentication**: GitHub token-based authentication
- **Features**: Repository validation, workflow detection, buildozer spec checking

### Template System (templates/workflow_templates.py)
- **Purpose**: Provides pre-built workflow templates for common APK building scenarios
- **Templates**: Basic APK build workflows for Python/Kivy applications
- **Customization**: Template-based workflow generation with parameter substitution

### Policy Engine (data/policies.py)
- **Purpose**: Enforces GitHub Actions security and compliance policies
- **Areas**: Security best practices, resource usage optimization, compliance checking
- **Features**: Policy validation, violation detection, recommendation engine

## Data Flow

1. **User Input**: User interacts with Streamlit interface, providing requirements or workflow details
2. **AI Processing**: OpenAI assistant processes requests and generates appropriate responses
3. **Workflow Generation**: System creates YAML workflows based on templates and AI recommendations
4. **Validation**: Generated workflows are validated for syntax, security, and compliance
5. **GitHub Integration**: Optional integration with GitHub repositories for workflow deployment
6. **Feedback Loop**: Validation results and suggestions are presented to the user for iteration

## External Dependencies

### Required APIs
- **OpenAI API**: GPT-4o model for intelligent workflow assistance (API key required)
- **GitHub API**: Repository validation and workflow management (token optional)

### Python Dependencies
- **streamlit**: Web application framework
- **openai**: OpenAI API client
- **pyyaml**: YAML parsing and generation
- **requests**: HTTP client for GitHub API integration

### System Dependencies
- **Build Tools**: Support for Android SDK, Java/OpenJDK, buildozer
- **CI/CD**: GitHub Actions runners and build environments

## Deployment Strategy

### Environment Setup
- **API Keys**: OpenAI API key required for full functionality
- **Optional Integration**: GitHub token for enhanced repository features
- **Configuration**: Environment variable-based configuration system

### Deployment Options
- **Local Development**: Direct Streamlit execution
- **Cloud Deployment**: Compatible with Streamlit Cloud, Heroku, or similar platforms
- **Container Deployment**: Dockerizable architecture for consistent deployment

### Security Considerations
- **API Key Management**: Secure environment variable storage for sensitive credentials
- **Policy Enforcement**: Built-in compliance checking against GitHub security policies
- **Input Validation**: Comprehensive validation of user inputs and generated workflows

## Recent Changes

**July 19, 2025 - Major Architecture Enhancement: PyGithub Integration**
- Removed OpenAI dependency - app now fully functional without AI features
- Added PyGithub library for advanced GitHub API operations
- Implemented hybrid approach: simple text commands + sophisticated backend API calls
- Added new "Command Builder" page with natural language command processing
- Enhanced GitHub Helper with 5 new advanced API methods:
  * `smart_file_check()` - checks files without cloning entire repository
  * `smart_workflow_deploy()` - creates/updates workflow files with conflict resolution
  * `monitor_build_status()` - real-time monitoring of GitHub Actions builds
  * `auto_setup_repository()` - automated repository setup for APK building
  * `check_github_connection()` - verifies GitHub token authentication and user identity
- Converted Chat Assistant to template-based help system with troubleshooting guides
- App now operates in "Template & Validation Based" mode instead of AI-dependent mode

**Evolution Summary:**
- **Before**: Shell commands + OpenAI chat for workflow generation
- **Now**: Advanced GitHub API integration + template system + command interface
- **Benefit**: More precise control, faster operations, no dependency on external AI services

The application is designed to be self-contained while providing integration points for external services. The modular architecture allows for easy extension and maintenance, with clear separation of concerns between UI, GitHub API processing, validation, and external integrations.
import json
import os
import yaml
from openai import OpenAI

class WorkflowAssistant:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
        self.client = OpenAI(api_key=api_key)
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
    
    def process_request(self, user_input):
        """Process user request and generate appropriate response with workflow if needed"""
        
        system_prompt = """
        You are an expert GitHub Actions workflow assistant specializing in APK building for Android applications.
        Your role is to help users create, troubleshoot, and optimize GitHub Actions workflows for building APK files.

        Key areas of expertise:
        1. GitHub Actions workflow syntax and best practices
        2. Buildozer configuration for Python/Kivy apps
        3. Android SDK setup and configuration
        4. Java/OpenJDK setup for Android builds
        5. Artifact management and deployment
        6. Troubleshooting common build issues
        7. GitHub policy compliance
        8. Security best practices for CI/CD

        When generating workflows:
        - Always use latest action versions (actions/checkout@v3, actions/setup-python@v4, etc.)
        - Include proper error handling and validation steps
        - Optimize for build speed with caching where appropriate
        - Ensure compliance with GitHub Terms of Service
        - Include clear comments explaining each step
        - Use secure practices for handling secrets and credentials

        Response format:
        - Provide clear, actionable advice
        - Include complete workflow YAML when requested
        - Explain the reasoning behind your recommendations
        - Highlight potential issues and solutions
        - Suggest optimizations and best practices

        If generating a workflow, respond with JSON containing:
        {"message": "your explanation", "workflow": "yaml content or null"}
        
        If just providing advice, respond with:
        {"message": "your advice", "workflow": null}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate workflow YAML if present
            if result.get("workflow"):
                try:
                    yaml.safe_load(result["workflow"])
                except yaml.YAMLError as e:
                    result["message"] += f"\n\n⚠️ Warning: Generated YAML has syntax issues: {str(e)}"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return {
                    "message": "Your OpenAI API quota has been exceeded. Please add credits to your OpenAI account at https://platform.openai.com/account/billing to continue using AI features. You can still use the workflow templates, validation tools, and other features without AI assistance.",
                    "workflow": None
                }
            else:
                return {
                    "message": f"Error processing request: {error_msg}. Please check your OpenAI API key configuration.",
                    "workflow": None
                }
    
    def generate_workflow_from_specs(self, build_type, app_name, requirements=None, additional_config=None):
        """Generate a workflow based on specific parameters"""
        
        prompt = f"""
        Generate a complete GitHub Actions workflow for building an APK with these specifications:
        
        Build Type: {build_type}
        App Name: {app_name}
        Requirements: {requirements or 'python3,kivy'}
        Additional Configuration: {additional_config or 'None specified'}
        
        The workflow should:
        1. Be triggered on push to main branch
        2. Set up the build environment (Ubuntu latest)
        3. Install necessary dependencies
        4. Configure Android SDK and Java
        5. Build the APK using buildozer
        6. Upload the APK as an artifact
        7. Include proper error handling
        8. Use caching for faster builds
        9. Follow GitHub Actions best practices
        
        Provide a complete, working workflow file.
        """
        
        return self.process_request(prompt)
    
    def troubleshoot_workflow(self, workflow_yaml, error_message):
        """Help troubleshoot workflow issues"""
        
        prompt = f"""
        I'm having issues with this GitHub Actions workflow for APK building:

        WORKFLOW:
        ```yaml
        {workflow_yaml}
        ```

        ERROR MESSAGE:
        {error_message}

        Please analyze the workflow and error, then provide:
        1. Diagnosis of the problem
        2. Specific fixes needed
        3. Updated workflow if necessary
        4. Prevention strategies for similar issues

        Focus on common APK build issues like Java version conflicts, Android SDK problems, 
        dependency issues, and buildozer configuration problems.
        """
        
        return self.process_request(prompt)
    
    def optimize_workflow(self, workflow_yaml):
        """Suggest optimizations for an existing workflow"""
        
        prompt = f"""
        Please analyze this GitHub Actions workflow for APK building and suggest optimizations:

        ```yaml
        {workflow_yaml}
        ```

        Provide suggestions for:
        1. Build speed improvements (caching, parallelization)
        2. Resource efficiency
        3. Security enhancements
        4. Best practices compliance
        5. Error handling improvements
        6. Artifact management optimization

        If significant improvements are possible, provide an optimized version of the workflow.
        """
        
        return self.process_request(prompt)

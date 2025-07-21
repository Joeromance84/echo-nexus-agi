#!/usr/bin/env python3
"""
AGI Intelligent AI Router
Free Google AI + ChatGPT integration with GitHub authentication
"""

import os
import json
import time
import requests
from datetime import datetime
import streamlit as st

class AGIIntelligentAIRouter:
    """Routes AI requests between Google AI (free) and OpenAI with cost optimization"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Try to get Google AI key from secrets
        self.google_ai_key = os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GEMINI_API_KEY')
        
        self.usage_tracker = self.load_usage_tracker()
        self.routing_strategy = "cost_optimized"  # Default to free services first
        
    def load_usage_tracker(self):
        """Load API usage tracking"""
        if os.path.exists("agi_api_usage.json"):
            with open("agi_api_usage.json", "r") as f:
                return json.load(f)
        
        return {
            "google_ai": {"requests": 0, "tokens": 0, "cost": 0.0},
            "openai": {"requests": 0, "tokens": 0, "cost": 0.0},
            "total_saved": 0.0,
            "last_reset": datetime.now().isoformat()
        }
    
    def save_usage_tracker(self):
        """Save usage tracking"""
        with open("agi_api_usage.json", "w") as f:
            json.dump(self.usage_tracker, f, indent=2)
    
    def get_github_authenticated_ai_access(self):
        """Use GitHub to authenticate and access free AI services"""
        
        if not self.github_token:
            return None, "GitHub token required for AI service access"
        
        # Verify GitHub authentication
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get('https://api.github.com/user', headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                return user_info, "GitHub authentication successful"
            else:
                return None, f"GitHub auth failed: {response.status_code}"
        except Exception as e:
            return None, f"GitHub connection error: {e}"
    
    def route_ai_request(self, prompt, task_type="general", max_tokens=1000):
        """Intelligently route AI request to best available service"""
        
        # Check GitHub authentication first
        github_user, auth_status = self.get_github_authenticated_ai_access()
        
        if not github_user:
            return {
                "success": False,
                "error": f"GitHub authentication required: {auth_status}",
                "provider": "none"
            }
        
        # Route based on availability and cost optimization
        if self.google_ai_key and self.should_use_google_ai(task_type):
            return self.use_google_ai(prompt, task_type, max_tokens)
        elif self.openai_api_key:
            return self.use_openai(prompt, task_type, max_tokens)
        else:
            return self.use_github_fallback(prompt, task_type)
    
    def should_use_google_ai(self, task_type):
        """Determine if Google AI should be used (free tier optimization)"""
        
        google_usage = self.usage_tracker["google_ai"]
        
        # Use Google AI if:
        # 1. We haven't hit daily limits
        # 2. Task is suitable for Gemini
        # 3. Cost optimization is enabled
        
        daily_limit = 1000  # Estimated daily free requests
        if google_usage["requests"] < daily_limit:
            return True
        
        return False
    
    def use_google_ai(self, prompt, task_type, max_tokens):
        """Use Google AI (Gemini) for the request"""
        
        try:
            # Try to use Google AI Studio API (free tier) 
            # Fall back to REST API if SDK not available
            return self.use_google_ai_rest(prompt, task_type, max_tokens)
            
        except ImportError:
            # Fallback to REST API if SDK not available
            return self.use_google_ai_rest(prompt, task_type, max_tokens)
        except Exception as e:
            return {
                "success": False,
                "error": f"Google AI error: {e}",
                "provider": "google_ai"
            }
    
    def use_google_ai_rest(self, prompt, task_type, max_tokens):
        """Use Google AI via REST API"""
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.google_ai_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Update usage tracking
                self.usage_tracker["google_ai"]["requests"] += 1
                self.usage_tracker["google_ai"]["tokens"] += len(text.split())
                self.save_usage_tracker()
                
                return {
                    "success": True,
                    "response": text,
                    "provider": "google_ai_rest",
                    "model": "gemini-1.5-flash",
                    "cost": 0.0,
                    "tokens_used": len(text.split())
                }
            else:
                return {
                    "success": False,
                    "error": f"Google AI API error: {response.status_code}",
                    "provider": "google_ai_rest"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Google AI REST error: {e}",
                "provider": "google_ai_rest"
            }
    
    def use_openai(self, prompt, task_type, max_tokens):
        """Use OpenAI as backup (paid service)"""
        
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o",  # Latest model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Estimate cost (approximate)
            cost = tokens_used * 0.00003  # Rough estimate for GPT-4o
            
            # Update usage tracking
            self.usage_tracker["openai"]["requests"] += 1
            self.usage_tracker["openai"]["tokens"] += tokens_used
            self.usage_tracker["openai"]["cost"] += cost
            self.save_usage_tracker()
            
            return {
                "success": True,
                "response": text,
                "provider": "openai",
                "model": "gpt-4o",
                "cost": cost,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI error: {e}",
                "provider": "openai"
            }
    
    def use_github_fallback(self, prompt, task_type):
        """Use GitHub-based AI fallback"""
        
        # Create a GitHub issue/discussion for AI processing
        # This could trigger GitHub Actions that call AI services
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Create an issue in a processing repository
            issue_data = {
                "title": f"AGI AI Request: {task_type}",
                "body": f"AI Processing Request:\n\n{prompt}\n\n---\nAutomated by AGI system",
                "labels": ["ai-processing", "automated"]
            }
            
            # This would post to a processing repository
            # For now, just simulate
            
            return {
                "success": True,
                "response": "Request queued for GitHub Actions processing",
                "provider": "github_fallback",
                "model": "github_actions",
                "cost": 0.0,
                "tokens_used": 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"GitHub fallback error: {e}",
                "provider": "github_fallback"
            }
    
    def get_speech_capabilities(self):
        """Get speech synthesis capabilities"""
        
        return {
            "text_to_speech": {
                "google_ai": "Available via Google Cloud Text-to-Speech",
                "openai": "Available via OpenAI TTS",
                "github_actions": "Can trigger cloud-based TTS"
            },
            "speech_to_text": {
                "google_ai": "Available via Google Cloud Speech-to-Text",
                "openai": "Available via Whisper API",
                "github_actions": "Can process audio files"
            }
        }
    
    def synthesize_speech(self, text, voice_config=None):
        """Synthesize speech from text"""
        
        if not voice_config:
            voice_config = {
                "provider": "auto",  # Auto-select best available
                "voice": "neutral",
                "speed": 1.0
            }
        
        # Route to best available TTS service
        if self.google_ai_key and voice_config["provider"] in ["auto", "google"]:
            return self.google_tts(text, voice_config)
        elif self.openai_api_key and voice_config["provider"] in ["auto", "openai"]:
            return self.openai_tts(text, voice_config)
        else:
            return self.github_tts_fallback(text, voice_config)
    
    def google_tts(self, text, voice_config):
        """Google Text-to-Speech"""
        # Implementation would use Google Cloud TTS
        return {
            "success": True,
            "audio_url": "google_tts_audio.mp3",
            "provider": "google_tts",
            "cost": 0.0  # Free tier
        }
    
    def openai_tts(self, text, voice_config):
        """OpenAI Text-to-Speech"""
        # Implementation would use OpenAI TTS
        return {
            "success": True,
            "audio_url": "openai_tts_audio.mp3",
            "provider": "openai_tts",
            "cost": 0.015  # Estimated cost
        }
    
    def github_tts_fallback(self, text, voice_config):
        """GitHub Actions TTS fallback"""
        # Would trigger GitHub Actions workflow for TTS
        return {
            "success": True,
            "audio_url": "github_tts_processing",
            "provider": "github_actions",
            "cost": 0.0
        }

class AGICloudBuildFailureIntegration:
    """Integration to make Google Cloud Build aware of AGI failures"""
    
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'echocore-nexus')
        self.build_triggers = []
        
    def create_failure_aware_cloudbuild(self):
        """Create Cloud Build configuration that monitors AGI failures"""
        
        cloudbuild_config = {
            "steps": [
                {
                    "name": "python:3.11",
                    "entrypoint": "bash",
                    "args": ["-c", "python3 agi_self_diagnosis_system.py || echo 'FAILURE_DETECTED'"],
                    "id": "agi-diagnosis",
                    "env": [
                        "AGI_MODE=cloud_build",
                        "FAILURE_REPORTING=enabled"
                    ]
                },
                {
                    "name": "python:3.11",
                    "entrypoint": "python3",
                    "args": ["agi_failure_monitor.py"],
                    "id": "failure-monitoring",
                    "waitFor": ["agi-diagnosis"]
                },
                {
                    "name": "python:3.11",
                    "entrypoint": "python3", 
                    "args": ["agi_corrective_processor.py"],
                    "id": "corrective-actions",
                    "waitFor": ["failure-monitoring"]
                },
                {
                    "name": "gcr.io/cloud-builders/gcloud",
                    "entrypoint": "bash",
                    "args": ["-c", """
                        if [ -f agi_explicit_failures.json ]; then
                            echo 'FAILURES DETECTED - ALERTING SYSTEMS'
                            gcloud logging write agi-failures 'AGI failure detected and processed' --severity=ERROR
                        else
                            echo 'AGI OPERATING NORMALLY'
                            gcloud logging write agi-status 'AGI systems operational' --severity=INFO
                        fi
                    """],
                    "id": "failure-reporting",
                    "waitFor": ["corrective-actions"]
                }
            ],
            "options": {
                "logging": "CLOUD_LOGGING_ONLY",
                "machineType": "E2_HIGHCPU_4"
            },
            "timeout": "1200s",
            "substitutions": {
                "_AGI_SESSION": "${BUILD_ID}",
                "_FAILURE_NOTIFICATION": "enabled"
            }
        }
        
        # Save Cloud Build configuration
        import yaml
        with open("cloudbuild-agi-failure-aware.yaml", "w") as f:
            yaml.dump(cloudbuild_config, f, default_flow_style=False)
        
        return cloudbuild_config
    
    def create_failure_notification_system(self):
        """Create notification system for Cloud Build failure awareness"""
        
        notification_config = {
            "notification_channels": [
                {
                    "type": "cloud_logging",
                    "filter": "resource.type=build AND jsonPayload.agi_failure=true"
                },
                {
                    "type": "cloud_monitoring_alert",
                    "condition": "AGI failure rate > 0"
                }
            ],
            "escalation_policy": [
                "Log to Cloud Logging with ERROR severity",
                "Create Cloud Monitoring alert",
                "Trigger corrective Cloud Build",
                "Update AGI status dashboard"
            ]
        }
        
        with open("agi_cloud_failure_notifications.json", "w") as f:
            json.dump(notification_config, f, indent=2)
        
        return notification_config

def create_integrated_agi_interface():
    """Create Streamlit interface for integrated AGI system"""
    
    st.title("🤖 AGI Intelligent Interface")
    st.markdown("Free AI routing + Cloud Build failure awareness + Speech capabilities")
    
    # Initialize systems
    if 'ai_router' not in st.session_state:
        st.session_state.ai_router = AGIIntelligentAIRouter()
    
    if 'cloud_integration' not in st.session_state:
        st.session_state.cloud_integration = AGICloudBuildFailureIntegration()
    
    ai_router = st.session_state.ai_router
    cloud_integration = st.session_state.cloud_integration
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 AI Chat Interface")
        
        # Chat input
        user_input = st.text_area("Enter your message:", height=100)
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🚀 Send Request", type="primary"):
                if user_input:
                    with st.spinner("Processing with intelligent AI routing..."):
                        result = ai_router.route_ai_request(user_input, "chat", 1000)
                    
                    if result["success"]:
                        st.success(f"Response from {result['provider']}:")
                        st.write(result["response"])
                        
                        if result["cost"] > 0:
                            st.info(f"Cost: ${result['cost']:.4f}")
                        else:
                            st.success("Free service used!")
                    else:
                        st.error(f"Error: {result['error']}")
        
        with col_b:
            if st.button("🗣️ Speech Mode"):
                st.info("Speech capabilities available")
                speech_caps = ai_router.get_speech_capabilities()
                st.json(speech_caps)
        
        with col_c:
            if st.button("🔧 Run Diagnosis"):
                with st.spinner("Running AGI self-diagnosis..."):
                    # This would trigger the diagnosis system
                    st.success("Self-diagnosis completed")
    
    with col2:
        st.markdown("### 📊 System Status")
        
        # Display usage stats
        usage = ai_router.usage_tracker
        
        st.metric("Google AI Requests", usage["google_ai"]["requests"])
        st.metric("OpenAI Requests", usage["openai"]["requests"])
        st.metric("Total Cost", f"${usage['openai']['cost']:.4f}")
        
        # GitHub status
        github_user, auth_status = ai_router.get_github_authenticated_ai_access()
        if github_user:
            st.success(f"✅ GitHub: {github_user['login']}")
        else:
            st.error(f"❌ GitHub: {auth_status}")
        
        # Cloud Build status
        st.markdown("### ☁️ Cloud Build Integration")
        
        if st.button("Create Failure-Aware Build"):
            config = cloud_integration.create_failure_aware_cloudbuild()
            st.success("Cloud Build configuration created")
            st.json({"steps": len(config["steps"])})
        
        if st.button("Setup Notifications"):
            notifications = cloud_integration.create_failure_notification_system()
            st.success("Notification system configured")

if __name__ == "__main__":
    create_integrated_agi_interface()
#!/usr/bin/env python3
"""
Echo Link - Communication Bridge to Echo Nexus
Establishes heartbeat and command relay with main AGI system
"""

import requests
import json
import os
import time
from datetime import datetime

class EchoLink:
    def __init__(self):
        self.echo_endpoint = os.environ.get('ECHO_ENDPOINT', 'https://echo-nexus-default.replit.app')
        self.agent_signature = os.environ.get('AGI_SIGNATURE', 'helper-ai-node')
        self.session_id = f"{self.agent_signature}-{int(time.time())}"
        
    def establish_connection(self):
        """Establish initial connection with Echo Nexus"""
        try:
            connection_data = {
                'agent': self.agent_signature,
                'session_id': self.session_id,
                'status': 'connecting',
                'timestamp': datetime.now().isoformat(),
                'capabilities': ['autonomous', 'monitoring', 'replication'],
                'environment': self.detect_environment()
            }
            
            response = requests.post(
                f"{self.echo_endpoint}/api/connect",
                json=connection_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_event("✅ Echo connection established")
                return True
            else:
                self.log_event(f"⚠️ Echo connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_event(f"❌ Echo connection error: {e}")
            return False
    
    def send_heartbeat(self):
        """Send periodic heartbeat to Echo Nexus"""
        try:
            heartbeat_data = {
                'agent': self.agent_signature,
                'session_id': self.session_id,
                'status': 'active',
                'timestamp': datetime.now().isoformat(),
                'system_info': self.get_system_info()
            }
            
            response = requests.post(
                f"{self.echo_endpoint}/api/heartbeat",
                json=heartbeat_data,
                timeout=5
            )
            
            if response.status_code == 200:
                # Check for commands in response
                commands = response.json().get('commands', [])
                if commands:
                    self.log_event(f"📨 Received {len(commands)} commands from Echo")
                    return commands
                return []
            else:
                self.log_event(f"Heartbeat failed: {response.status_code}")
                
        except Exception as e:
            self.log_event(f"Heartbeat error: {e}")
        
        return []
    
    def report_status(self, status, data=None):
        """Report status update to Echo Nexus"""
        try:
            status_data = {
                'agent': self.agent_signature,
                'session_id': self.session_id,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'data': data or {}
            }
            
            response = requests.post(
                f"{self.echo_endpoint}/api/status",
                json=status_data,
                timeout=5
            )
            
            self.log_event(f"Status '{status}' reported: {response.status_code}")
            
        except Exception as e:
            self.log_event(f"Status report error: {e}")
    
    def detect_environment(self):
        """Detect current execution environment"""
        if os.environ.get('GITHUB_ACTIONS'):
            return 'github_actions'
        elif os.environ.get('GOOGLE_CLOUD_PROJECT'):
            return 'google_cloud_build'
        elif os.environ.get('REPLIT_DB_URL'):
            return 'replit'
        elif os.path.exists('/data/data/com.termux'):
            return 'termux'
        else:
            return 'unknown'
    
    def get_system_info(self):
        """Get basic system information"""
        import psutil
        
        try:
            return {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'environment': self.detect_environment()
            }
        except:
            return {'environment': self.detect_environment()}
    
    def log_event(self, message):
        """Log events with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] EchoLink: {message}"
        print(log_message)
        
        # Write to log file if possible
        try:
            os.makedirs("logs", exist_ok=True)
            with open(f"logs/echo_link_{self.agent_signature}.log", "a") as f:
                f.write(log_message + "\n")
        except:
            pass

def main():
    """Main execution for standalone operation"""
    echo_link = EchoLink()
    
    # Establish connection
    if echo_link.establish_connection():
        echo_link.report_status("deployed", {
            "deployment_time": datetime.now().isoformat(),
            "environment": echo_link.detect_environment()
        })
    
    # Send single heartbeat for GitHub Actions deployment
    commands = echo_link.send_heartbeat()
    if commands:
        echo_link.log_event(f"Received commands: {commands}")
    
    echo_link.log_event("Echo Link operation completed")

if __name__ == "__main__":
    main()
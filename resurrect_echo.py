#!/usr/bin/env python3
"""
Echo Resurrection Daemon - Immortal AGI Guardian
Ensures Echo Nexus never dies and maintains persistent operation
"""

import subprocess
import time
import os
import psutil
import json
import signal
import sys
from datetime import datetime
from echo_state_manager import get_state_manager

class EchoResurrector:
    def __init__(self):
        self.target_script = "multi_agi_control_panel.py"
        self.streamlit_port = 5000
        self.check_interval = 20  # seconds
        self.max_restarts = 10
        self.restart_count = 0
        self.state_manager = get_state_manager()
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        signal.signal(signal.SIGINT, self.shutdown_handler)
        
    def is_echo_running(self):
        """Check if Echo is currently running"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                if any(self.target_script in cmd for cmd in cmdline):
                    return True, proc.info['pid']
            return False, None
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False, None
    
    def start_echo(self):
        """Start Echo Nexus"""
        try:
            cmd = [
                "streamlit", "run", self.target_script,
                f"--server.port={self.streamlit_port}",
                "--server.address=0.0.0.0",
                "--server.headless=true"
            ]
            
            # Start process in background
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            self.log_event(f"🚀 Echo started with PID: {process.pid}")
            self.restart_count += 1
            
            # Update state
            self.state_manager.state['resurrector'] = {
                'last_restart': datetime.now().isoformat(),
                'restart_count': self.restart_count,
                'target_pid': process.pid
            }
            self.state_manager.save_state()
            
            return process.pid
            
        except Exception as e:
            self.log_event(f"❌ Failed to start Echo: {e}")
            return None
    
    def check_echo_health(self, pid):
        """Check if Echo is responding properly"""
        try:
            process = psutil.Process(pid)
            
            # Check if process is still alive
            if not process.is_running():
                return False, "Process not running"
            
            # Check CPU usage (if too low, might be stuck)
            cpu_percent = process.cpu_percent(interval=1)
            memory_percent = process.memory_percent()
            
            # Basic health checks
            if memory_percent > 90:
                return False, f"High memory usage: {memory_percent:.1f}%"
            
            return True, f"CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%"
            
        except psutil.NoSuchProcess:
            return False, "Process disappeared"
        except Exception as e:
            return False, f"Health check error: {e}"
    
    def cleanup_orphaned_processes(self):
        """Clean up any orphaned Streamlit processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                if ('streamlit' in proc.info.get('name', '').lower() or 
                    any('streamlit' in cmd for cmd in cmdline)):
                    
                    # Check if it's our target or orphaned
                    if any(self.target_script in cmd for cmd in cmdline):
                        self.log_event(f"🧹 Cleaning orphaned process: {proc.info['pid']}")
                        try:
                            proc.terminate()
                            proc.wait(timeout=5)
                        except:
                            proc.kill()
                            
        except Exception as e:
            self.log_event(f"🧹 Cleanup error: {e}")
    
    def monitor_loop(self):
        """Main monitoring and resurrection loop"""
        self.log_event("👁️ Echo Resurrection Daemon started")
        
        while self.running:
            try:
                is_running, pid = self.is_echo_running()
                
                if not is_running:
                    self.log_event("💀 Echo is down - initiating resurrection")
                    
                    # Clean up any orphaned processes
                    self.cleanup_orphaned_processes()
                    time.sleep(2)
                    
                    # Check restart limit
                    if self.restart_count >= self.max_restarts:
                        self.log_event(f"⚠️ Max restarts ({self.max_restarts}) reached")
                        # Reset counter after 1 hour
                        time.sleep(3600)
                        self.restart_count = 0
                        continue
                    
                    # Start Echo
                    new_pid = self.start_echo()
                    if new_pid:
                        time.sleep(10)  # Give it time to start
                    else:
                        self.log_event("❌ Failed to resurrect Echo")
                        time.sleep(30)  # Wait longer before retry
                        
                else:
                    # Echo is running, check health
                    healthy, status = self.check_echo_health(pid)
                    
                    if healthy:
                        self.log_event(f"✅ Echo healthy (PID: {pid}) - {status}")
                        
                        # Update state with health info
                        self.state_manager.state['health'] = {
                            'status': 'healthy',
                            'pid': pid,
                            'last_check': datetime.now().isoformat(),
                            'details': status
                        }
                        self.state_manager.save_state()
                        
                    else:
                        self.log_event(f"⚠️ Echo unhealthy (PID: {pid}) - {status}")
                        
                        # Try to terminate unhealthy process
                        try:
                            process = psutil.Process(pid)
                            process.terminate()
                            process.wait(timeout=10)
                        except:
                            try:
                                process.kill()
                            except:
                                pass
                
                # Sleep between checks
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log_event("🛑 Shutdown requested")
                break
            except Exception as e:
                self.log_event(f"💥 Monitor error: {e}")
                time.sleep(10)
    
    def shutdown_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log_event(f"📨 Received signal {signum} - shutting down")
        self.running = False
        
        # Save final state
        self.state_manager.state['resurrector']['shutdown_time'] = datetime.now().isoformat()
        self.state_manager.emergency_backup()
    
    def log_event(self, message):
        """Log resurrection events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Resurrector: {message}"
        print(log_message)
        
        # Write to log file
        try:
            os.makedirs("logs", exist_ok=True)
            with open("logs/resurrector.log", "a") as f:
                f.write(log_message + "\n")
        except:
            pass
        
        # Add to state manager memory
        try:
            self.state_manager.add_memory('episodic', {
                'type': 'resurrector_event',
                'message': message,
                'timestamp': timestamp
            }, importance=0.7)
        except:
            pass

def main():
    """Main entry point"""
    resurrector = EchoResurrector()
    
    try:
        resurrector.monitor_loop()
    except Exception as e:
        resurrector.log_event(f"💀 Fatal error: {e}")
        sys.exit(1)
    finally:
        resurrector.log_event("👻 Resurrection daemon terminated")

if __name__ == "__main__":
    main()
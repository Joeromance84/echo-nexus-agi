#!/usr/bin/env python3
"""
AGI Process Controller - Manage individual AGI system lifecycles
"""

import subprocess
import os
import psutil
from datetime import datetime

running_processes = {}

def start_agi(name, script_path):
    """Start an AGI process"""
    if name in running_processes:
        proc = running_processes[name]
        if proc.poll() is None:  # Still running
            return f"{name} is already running (PID {proc.pid})"
    
    try:
        # Start the process with logging
        log_file = f"logs/{name.lower().replace(' ', '_')}.log"
        os.makedirs("logs", exist_ok=True)
        
        process = subprocess.Popen(
            ["python", script_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        running_processes[name] = process
        
        # Log the start
        with open(log_file, "a") as f:
            f.write(f"\n[{datetime.now()}] {name} started with PID {process.pid}\n")
        
        return f"{name} started successfully (PID {process.pid})"
    except Exception as e:
        return f"Failed to start {name}: {str(e)}"

def stop_agi(name):
    """Stop an AGI process"""
    if name not in running_processes:
        return f"{name} is not running"
    
    try:
        process = running_processes[name]
        if process.poll() is None:  # Still running
            process.terminate()
            process.wait(timeout=5)  # Wait up to 5 seconds
        
        del running_processes[name]
        
        # Log the stop
        log_file = f"logs/{name.lower().replace(' ', '_')}.log"
        with open(log_file, "a") as f:
            f.write(f"[{datetime.now()}] {name} terminated\n")
        
        return f"{name} stopped successfully"
    except subprocess.TimeoutExpired:
        process.kill()
        return f"{name} force-killed (was unresponsive)"
    except Exception as e:
        return f"Error stopping {name}: {str(e)}"

def list_running():
    """List all running AGI processes"""
    active = {}
    for name, proc in list(running_processes.items()):
        if proc.poll() is None:  # Still running
            try:
                p = psutil.Process(proc.pid)
                active[name] = {
                    "pid": proc.pid,
                    "cpu_percent": p.cpu_percent(),
                    "memory_mb": p.memory_info().rss / 1024 / 1024,
                    "status": p.status()
                }
            except psutil.NoSuchProcess:
                # Process died, clean up
                del running_processes[name]
        else:
            # Process finished, clean up
            del running_processes[name]
    
    return active

def get_system_stats():
    """Get overall system statistics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_gb": memory.available / (1024**3),
        "memory_total_gb": memory.total / (1024**3)
    }
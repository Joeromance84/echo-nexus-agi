#!/usr/bin/env python3
"""
Enhanced Streamlit Launcher for Replit
Auto-detects environment and launches with optimal settings
"""

import socket
import subprocess
import sys
import os
from pathlib import Path

def detect_environment():
    """Detect if running in Replit, VS Code, Docker, etc."""
    if os.environ.get('REPLIT_DB_URL'):
        return 'replit'
    elif os.environ.get('CODESPACES'):
        return 'codespaces'
    elif os.path.exists('/.dockerenv'):
        return 'docker'
    else:
        return 'local'

def find_open_port(start=5000, end=5099):
    """Find an open port in the specified range"""
    for port in range(start, end):
        with socket.socket() as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No open ports available in range {start}-{end}")

def get_replit_url(port):
    """Generate the Replit public URL"""
    repl_slug = os.environ.get('REPL_SLUG', 'unknown')
    repl_owner = os.environ.get('REPL_OWNER', 'unknown')
    return f"https://{repl_slug}--{repl_owner}.replit.app:{port}"

def launch_streamlit(app_file, auto_port=True):
    """Launch Streamlit with environment-optimized settings"""
    if not Path(app_file).exists():
        print(f"❌ Streamlit app not found: {app_file}")
        sys.exit(1)

    env = detect_environment()
    print(f"🔍 Environment detected: {env}")

    if auto_port:
        port = find_open_port()
        print(f"✅ Found open port: {port}")
    else:
        port = 8501  # Default Streamlit port

    # Environment-specific configurations
    cmd = ["streamlit", "run", app_file]
    
    if env == 'replit':
        cmd.extend([
            "--server.port", str(port),
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false"
        ])
        public_url = get_replit_url(port)
        print(f"🌐 Replit URL: {public_url}")
    elif env == 'codespaces':
        cmd.extend([
            "--server.port", str(port),
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
    else:
        cmd.extend([
            "--server.port", str(port)
        ])

    print(f"🚀 Launching: {' '.join(cmd)}")
    print(f"📍 Local access: http://localhost:{port}")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  Streamlit stopped by user")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python replit_streamlit_launcher.py <app.py> [--no-auto-port]")
        print("Example: python replit_streamlit_launcher.py debug_app.py")
        sys.exit(1)
    
    app_file = sys.argv[1]
    auto_port = "--no-auto-port" not in sys.argv
    
    launch_streamlit(app_file, auto_port)
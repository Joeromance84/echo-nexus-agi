#!/usr/bin/env python3
"""
Replit Port Finder - Auto-detect available ports in safe range
Based on programming guru's recommendation
"""

import socket

def find_open_port(start=5000, end=5099):
    """Find an open port in Replit's safe range (5000-5099)"""
    for port in range(start, end):
        with socket.socket() as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No open ports available in range {start}-{end}")

def check_replit_used_ports():
    """Check which ports are already used by other Streamlit apps"""
    used_ports = []
    replit_ports = [5000, 5002, 5003, 5005, 5006]  # Known used ports
    
    for port in replit_ports:
        with socket.socket() as s:
            try:
                s.bind(('', port))
                print(f"Port {port}: Available")
            except OSError:
                print(f"Port {port}: In use")
                used_ports.append(port)
    
    return used_ports

if __name__ == "__main__":
    print("🔍 Replit Port Analysis")
    print("=" * 40)
    
    # Check known Replit ports
    used = check_replit_used_ports()
    print(f"\nUsed ports: {used}")
    
    # Find next available port
    try:
        next_port = find_open_port()
        print(f"✅ Next available port: {next_port}")
        print(f"📝 Recommended command:")
        print(f"streamlit run app.py --server.port {next_port} --server.address 0.0.0.0")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
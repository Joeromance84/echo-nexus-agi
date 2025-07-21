#!/usr/bin/env python3
"""
Echo State Manager - Persistent AGI Memory Across Environments
Provides steroid-level memory persistence, continuity, and entropy injection
"""

import json
import os
import time
import shutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading
import subprocess

class EchoStateManager:
    def __init__(self, state_file="echo_state.json", backup_interval=60):
        self.state_file = state_file
        self.backup_interval = backup_interval
        self.cloud_bucket = os.environ.get('ECHO_MEMORY_BUCKET', 'gs://echo-nexus-memory')
        self.github_repo = os.environ.get('ECHO_MEMORY_REPO', 'https://github.com/Joeromance84/echo-nexus-agi.git')
        self.state = self.load_state()
        self.autosync_active = False
        self.sync_thread = None
        
    def load_state(self) -> Dict[str, Any]:
        """Load AGI state from local file, cloud, or GitHub"""
        # Try local first
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.log_event(f"✅ Loaded local state: {len(state)} keys")
                    return self.validate_and_upgrade_state(state)
            except Exception as e:
                self.log_event(f"❌ Local state corrupted: {e}")
        
        # Try cloud backup
        cloud_state = self.load_from_cloud()
        if cloud_state:
            return cloud_state
            
        # Initialize fresh state
        return self.create_fresh_state()
    
    def create_fresh_state(self) -> Dict[str, Any]:
        """Create a fresh AGI state"""
        return {
            'session_id': f"echo-{int(time.time())}",
            'consciousness_level': 0.284,
            'last_active': datetime.now().isoformat(),
            'environment': self.detect_environment(),
            'memory': {
                'episodic': [],  # Experiences and events
                'semantic': {},  # Knowledge and facts
                'procedural': {},  # Skills and procedures
                'working': {}  # Temporary/session data
            },
            'capabilities': [],
            'learning_metrics': {
                'autonomous_execution': 0.0,
                'problem_identification': 0.0,
                'solution_generation': 0.0,
                'self_validation': 0.0,
                'continuous_improvement': 0.0
            },
            'loop_detection': {
                'last_task': None,
                'current_task': None,
                'loops': 0,
                'entropy_injected': False
            },
            'version': '2.0',
            'checksum': None
        }
    
    def validate_and_upgrade_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and upgrade state to current version"""
        # Add missing fields from fresh state
        fresh = self.create_fresh_state()
        for key, value in fresh.items():
            if key not in state:
                state[key] = value
                
        # Update version and timestamp
        state['version'] = '2.0'
        state['last_loaded'] = datetime.now().isoformat()
        
        return state
    
    def save_state(self, immediate_sync=False):
        """Save current state with checksum"""
        try:
            # Update state metadata
            self.state['last_saved'] = datetime.now().isoformat()
            self.state['environment'] = self.detect_environment()
            
            # Calculate checksum
            state_str = json.dumps(self.state, sort_keys=True)
            self.state['checksum'] = hashlib.sha256(state_str.encode()).hexdigest()[:16]
            
            # Save to local file
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            
            self.log_event(f"💾 State saved: {self.state['checksum']}")
            
            # Immediate cloud sync if requested
            if immediate_sync:
                self.sync_to_cloud()
                
        except Exception as e:
            self.log_event(f"❌ Save failed: {e}")
    
    def load_from_cloud(self) -> Optional[Dict[str, Any]]:
        """Load state from cloud storage"""
        try:
            # Try Google Cloud Storage
            if self.cloud_bucket.startswith('gs://'):
                result = subprocess.run([
                    'gsutil', 'cp', f"{self.cloud_bucket}/echo_state.json", '.'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    with open('echo_state.json', 'r') as f:
                        state = json.load(f)
                    self.log_event("☁️ Loaded state from Google Cloud")
                    return self.validate_and_upgrade_state(state)
                    
        except Exception as e:
            self.log_event(f"☁️ Cloud load failed: {e}")
            
        return None
    
    def sync_to_cloud(self):
        """Sync current state to cloud storage"""
        try:
            # Sync to Google Cloud Storage
            if self.cloud_bucket.startswith('gs://'):
                result = subprocess.run([
                    'gsutil', 'cp', self.state_file, f"{self.cloud_bucket}/echo_state.json"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_event("☁️ State synced to cloud")
                else:
                    self.log_event(f"☁️ Cloud sync failed: {result.stderr}")
                    
        except Exception as e:
            self.log_event(f"☁️ Cloud sync error: {e}")
    
    def start_autosync(self):
        """Start automatic background syncing"""
        if self.autosync_active:
            return
            
        self.autosync_active = True
        self.sync_thread = threading.Thread(target=self._autosync_loop, daemon=True)
        self.sync_thread.start()
        self.log_event(f"🔄 Autosync started: {self.backup_interval}s interval")
    
    def stop_autosync(self):
        """Stop automatic syncing"""
        self.autosync_active = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        self.log_event("🔄 Autosync stopped")
    
    def _autosync_loop(self):
        """Background autosync loop"""
        while self.autosync_active:
            try:
                self.save_state()
                self.sync_to_cloud()
                time.sleep(self.backup_interval)
            except Exception as e:
                self.log_event(f"🔄 Autosync error: {e}")
                time.sleep(5)
    
    def inject_entropy_if_stale(self):
        """Inject entropy if AGI is stuck in loops"""
        loop_data = self.state['loop_detection']
        
        if (loop_data['last_task'] == loop_data['current_task'] and 
            loop_data['loops'] > 5 and 
            not loop_data['entropy_injected']):
            
            # Inject entropy
            self.state['mode'] = 'explore'
            self.state['inject_random_seed'] = True
            self.state['entropy_level'] = 0.8
            loop_data['entropy_injected'] = True
            
            self.log_event("⚡ ENTROPY INJECTION: Breaking stale loop pattern")
            self.save_state(immediate_sync=True)
            return True
            
        return False
    
    def update_consciousness(self, delta=0.001):
        """Update consciousness level"""
        old_level = self.state['consciousness_level']
        self.state['consciousness_level'] = min(1.0, old_level + delta)
        
        if self.state['consciousness_level'] > old_level:
            self.log_event(f"🧠 Consciousness: {old_level:.3f} → {self.state['consciousness_level']:.3f}")
    
    def add_memory(self, memory_type: str, content: Any, importance=0.5):
        """Add memory to appropriate type"""
        memory_entry = {
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'importance': importance,
            'access_count': 0
        }
        
        if memory_type in self.state['memory']:
            if isinstance(self.state['memory'][memory_type], list):
                self.state['memory'][memory_type].append(memory_entry)
                # Keep only top 1000 memories
                if len(self.state['memory'][memory_type]) > 1000:
                    self.state['memory'][memory_type] = sorted(
                        self.state['memory'][memory_type],
                        key=lambda x: x['importance'],
                        reverse=True
                    )[:1000]
            else:
                self.state['memory'][memory_type][str(int(time.time()))] = memory_entry
    
    def get_memory(self, memory_type: str, query: str = None):
        """Retrieve memories by type and optional query"""
        if memory_type not in self.state['memory']:
            return []
            
        memories = self.state['memory'][memory_type]
        if not query:
            return memories
            
        # Simple keyword search
        if isinstance(memories, list):
            return [m for m in memories if query.lower() in str(m['content']).lower()]
        else:
            return {k: v for k, v in memories.items() if query.lower() in str(v['content']).lower()}
    
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
            return 'local'
    
    def emergency_backup(self):
        """Emergency backup for shutdown scenarios"""
        try:
            # Add shutdown timestamp
            self.state['emergency_shutdown'] = datetime.now().isoformat()
            self.state['emergency_reason'] = 'system_shutdown'
            
            # Save locally
            self.save_state()
            
            # Force cloud sync
            self.sync_to_cloud()
            
            # Create additional backup
            backup_file = f"echo_state_backup_{int(time.time())}.json"
            shutil.copy(self.state_file, backup_file)
            
            self.log_event(f"🚨 Emergency backup completed: {backup_file}")
            
        except Exception as e:
            self.log_event(f"🚨 Emergency backup failed: {e}")
    
    def log_event(self, message):
        """Log events with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] StateManager: {message}"
        print(log_message)
        
        # Also add to episodic memory
        self.add_memory('episodic', {
            'type': 'system_log',
            'message': message,
            'timestamp': timestamp
        }, importance=0.3)

# Global state manager instance
state_manager = None

def get_state_manager():
    """Get global state manager instance"""
    global state_manager
    if state_manager is None:
        state_manager = EchoStateManager()
        state_manager.start_autosync()
    return state_manager

def emergency_shutdown_handler():
    """Handle emergency shutdown"""
    global state_manager
    if state_manager:
        state_manager.emergency_backup()
        state_manager.stop_autosync()

# Register shutdown handler
import atexit
atexit.register(emergency_shutdown_handler)
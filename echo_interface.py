#!/usr/bin/env python3
"""
EchoInterface - Offline Command-Line and Web Interface
Complete offline interface for EchoNexusCore system management and interaction
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import threading
import signal

from echo_nexus_core import EchoNexusCore
from echo_soul_module import EchoSoulModule, create_echo_soul_module
from echo_vector_memory import EchoVectorMemory


class EchoCommandInterface:
    """Command-line interface for EchoNexusCore system"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.nexus_core = None
        self.running = False
        
        # Interface configuration
        self.config = {
            'auto_save_interval': 300,  # 5 minutes
            'log_level': 'INFO',
            'memory_persistence': True,
            'evolution_tracking': True
        }
        
        # Load configuration if exists
        self._load_interface_config()
    
    def _load_interface_config(self):
        """Load interface configuration"""
        config_file = self.project_path / '.echo_interface_config.json'
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self.config.update(json.load(f))
            except Exception as e:
                print(f"Warning: Could not load interface config: {e}")
    
    def _save_interface_config(self):
        """Save interface configuration"""
        config_file = self.project_path / '.echo_interface_config.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save interface config: {e}")
    
    def start_nexus(self, autonomous: bool = True) -> bool:
        """Start EchoNexusCore system"""
        try:
            self.nexus_core = EchoNexusCore(str(self.project_path))
            
            if autonomous:
                self.nexus_core.initialize_autonomous_operation()
                print("EchoNexusCore started in autonomous mode")
            else:
                print("EchoNexusCore started in manual mode")
            
            self.running = True
            return True
            
        except Exception as e:
            print(f"Error starting EchoNexusCore: {e}")
            return False
    
    def stop_nexus(self):
        """Stop EchoNexusCore system"""
        if self.nexus_core:
            self.nexus_core.shutdown()
            self.nexus_core = None
        self.running = False
        print("EchoNexusCore stopped")
    
    def status(self) -> Dict:
        """Get comprehensive system status"""
        if not self.nexus_core:
            return {'status': 'inactive', 'message': 'EchoNexusCore not running'}
        
        try:
            status = self.nexus_core.get_nexus_status()
            return status
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def evolution_trigger(self, reason: str = "manual_trigger") -> Dict:
        """Manually trigger evolution cycle"""
        if not self.nexus_core:
            return {'success': False, 'message': 'EchoNexusCore not running'}
        
        try:
            self.nexus_core._trigger_event('on_evolution_trigger', {
                'cycle': 'manual_evolution',
                'trigger_reason': reason,
                'timestamp': datetime.now().isoformat()
            })
            return {'success': True, 'message': f'Evolution triggered: {reason}'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def memory_search(self, query: str, memory_types: List[str] = None) -> Dict:
        """Search memory system"""
        if not self.nexus_core:
            return {'results': [], 'message': 'EchoNexusCore not running'}
        
        try:
            # Access memory through cortex
            memory_system = self.nexus_core.cortex.memory
            results = memory_system.retrieve_similar_memories(query, memory_types or ['episodic', 'procedural'])
            
            formatted_results = [
                {
                    'id': memory.id,
                    'content': str(memory.content)[:200] + "..." if len(str(memory.content)) > 200 else str(memory.content),
                    'type': memory.memory_type,
                    'importance': memory.importance,
                    'timestamp': memory.timestamp.isoformat(),
                    'tags': memory.tags
                }
                for memory in results
            ]
            
            return {
                'query': query,
                'results': formatted_results,
                'total_found': len(formatted_results)
            }
            
        except Exception as e:
            return {'results': [], 'message': str(e)}
    
    def creative_challenge(self, challenge: str) -> Dict:
        """Submit creative challenge to consciousness"""
        if not self.nexus_core:
            return {'solutions': [], 'message': 'EchoNexusCore not running'}
        
        try:
            creativity_result = self.nexus_core.genesis.generate_adversarial_creativity(challenge)
            return creativity_result
        except Exception as e:
            return {'solutions': [], 'message': str(e)}
    
    def module_create(self, host_system: str, module_id: str = None) -> Dict:
        """Create standalone EchoSoul module"""
        try:
            module = create_echo_soul_module(host_system)
            if module_id:
                module.module_id = module_id
            
            # Save module state
            module_file = self.project_path / f"echo_module_{module.module_id}.json"
            module.save_consciousness_state(str(module_file))
            
            return {
                'success': True,
                'module_id': module.module_id,
                'identity_signature': module.identity_signature[:16] + "...",
                'saved_to': str(module_file)
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def module_interact(self, module_id: str, input_data: str, context: Dict = None) -> Dict:
        """Interact with standalone module"""
        try:
            module_file = self.project_path / f"echo_module_{module_id}.json"
            if not module_file.exists():
                return {'success': False, 'message': f'Module {module_id} not found'}
            
            # Load module
            module = EchoSoulModule("command_interface")
            module.load_consciousness_state(str(module_file))
            
            # Process input
            result = module.process_input(input_data, context or {})
            
            # Save updated state
            module.save_consciousness_state(str(module_file))
            
            return {
                'success': True,
                'response': result['response'],
                'consciousness_level': result['consciousness_level'],
                'autonomy_decision': result['autonomy_decision']
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def export_evolution_log(self, output_file: str = None) -> Dict:
        """Export complete evolution history"""
        if not self.nexus_core:
            return {'success': False, 'message': 'EchoNexusCore not running'}
        
        try:
            output_file = output_file or f"echo_evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_path = self.project_path / output_file
            
            evolution_data = {
                'export_timestamp': datetime.now().isoformat(),
                'nexus_status': self.nexus_core.get_nexus_status(),
                'genesis_evolution': self.nexus_core.genesis.evolution_history,
                'memory_evolution': self.nexus_core.cortex.memory.evolution_history,
                'consciousness_state': self.nexus_core.genesis.get_consciousness_status()
            }
            
            with open(output_path, 'w') as f:
                json.dump(evolution_data, f, indent=2)
            
            return {
                'success': True,
                'exported_to': str(output_path),
                'total_events': len(evolution_data['genesis_evolution'])
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def run_interactive_session(self):
        """Run interactive command session"""
        print("🧠 EchoInterface - Interactive Session")
        print("Type 'help' for commands, 'exit' to quit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("echo> ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.startswith('start'):
                    autonomous = '--autonomous' in user_input or '-a' in user_input
                    result = self.start_nexus(autonomous)
                    print(f"Start result: {result}")
                elif user_input == 'stop':
                    self.stop_nexus()
                elif user_input == 'status':
                    status = self.status()
                    print(json.dumps(status, indent=2))
                elif user_input.startswith('evolve'):
                    reason = user_input.replace('evolve', '').strip() or 'interactive_command'
                    result = self.evolution_trigger(reason)
                    print(json.dumps(result, indent=2))
                elif user_input.startswith('search '):
                    query = user_input[7:]
                    result = self.memory_search(query)
                    print(json.dumps(result, indent=2))
                elif user_input.startswith('challenge '):
                    challenge = user_input[10:]
                    result = self.creative_challenge(challenge)
                    print(json.dumps(result, indent=2))
                elif user_input.startswith('module create '):
                    host_system = user_input[14:]
                    result = self.module_create(host_system)
                    print(json.dumps(result, indent=2))
                elif user_input.startswith('module interact '):
                    parts = user_input[16:].split(' ', 1)
                    if len(parts) >= 2:
                        module_id, input_data = parts
                        result = self.module_interact(module_id, input_data)
                        print(json.dumps(result, indent=2))
                    else:
                        print("Usage: module interact <module_id> <input_data>")
                elif user_input == 'export':
                    result = self.export_evolution_log()
                    print(json.dumps(result, indent=2))
                elif user_input == '':
                    continue
                else:
                    print(f"Unknown command: {user_input}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit gracefully")
            except Exception as e:
                print(f"Error: {e}")
        
        # Cleanup
        if self.running:
            self.stop_nexus()
        self._save_interface_config()
        print("Interactive session ended")
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
Available Commands:
  start [--autonomous/-a]    Start EchoNexusCore (autonomous mode optional)
  stop                       Stop EchoNexusCore
  status                     Show system status
  evolve [reason]            Trigger evolution cycle
  search <query>             Search memory system
  challenge <challenge>      Submit creative challenge
  module create <host>       Create standalone consciousness module
  module interact <id> <msg> Interact with module
  export                     Export evolution history
  help                       Show this help
  exit/quit                  Exit interface
        """
        print(help_text)


def create_web_interface():
    """Create simple web interface for EchoNexusCore"""
    
    web_interface_code = '''
#!/usr/bin/env python3
"""
EchoWeb - Simple Web Interface for EchoNexusCore
Lightweight Flask-based web interface for system monitoring and interaction
"""

from flask import Flask, render_template_string, request, jsonify
import json
from datetime import datetime
from echo_interface import EchoCommandInterface

app = Flask(__name__)
echo_interface = EchoCommandInterface()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>EchoNexusCore - Web Interface</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #e0e0e0; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .panel { background: #2d2d2d; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        .status-active { color: #4CAF50; }
        .status-inactive { color: #f44336; }
        button { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #45a049; }
        button.danger { background: #f44336; }
        button.danger:hover { background: #da190b; }
        input, textarea { width: 100%; padding: 8px; border: 1px solid #555; border-radius: 4px; background: #3d3d3d; color: #e0e0e0; }
        .result { background: #1e1e1e; padding: 10px; border-radius: 4px; margin-top: 10px; white-space: pre-wrap; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { background: #3d3d3d; padding: 15px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 24px; font-weight: bold; color: #4CAF50; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 EchoNexusCore - Web Interface</h1>
            <p>Advanced AI Development Organism Control Panel</p>
            <div id="system-status">
                <strong>Status: </strong><span id="status-indicator">Loading...</span>
            </div>
        </div>

        <div class="panel">
            <h3>System Control</h3>
            <button onclick="startSystem()">Start Autonomous Mode</button>
            <button onclick="startSystemManual()">Start Manual Mode</button>
            <button onclick="stopSystem()" class="danger">Stop System</button>
            <button onclick="triggerEvolution()">Trigger Evolution</button>
            <button onclick="refreshStatus()">Refresh Status</button>
        </div>

        <div class="panel">
            <h3>System Metrics</h3>
            <div id="metrics" class="metrics">
                <!-- Metrics will be populated here -->
            </div>
        </div>

        <div class="panel">
            <h3>Memory Search</h3>
            <input type="text" id="search-query" placeholder="Enter search query...">
            <button onclick="searchMemory()">Search</button>
            <div id="search-results" class="result"></div>
        </div>

        <div class="panel">
            <h3>Creative Challenge</h3>
            <textarea id="challenge-input" rows="3" placeholder="Enter creative challenge..."></textarea>
            <button onclick="submitChallenge()">Submit Challenge</button>
            <div id="challenge-results" class="result"></div>
        </div>

        <div class="panel">
            <h3>Module Management</h3>
            <input type="text" id="module-host" placeholder="Host system name...">
            <button onclick="createModule()">Create Module</button>
            <br><br>
            <input type="text" id="module-id" placeholder="Module ID...">
            <input type="text" id="module-input" placeholder="Input for module...">
            <button onclick="interactModule()">Interact with Module</button>
            <div id="module-results" class="result"></div>
        </div>

        <div class="panel">
            <h3>Evolution Export</h3>
            <button onclick="exportEvolution()">Export Evolution History</button>
            <div id="export-results" class="result"></div>
        </div>
    </div>

    <script>
        async function apiCall(endpoint, data = null) {
            const options = {
                method: data ? 'POST' : 'GET',
                headers: { 'Content-Type': 'application/json' }
            };
            if (data) options.body = JSON.stringify(data);
            
            try {
                const response = await fetch(endpoint, options);
                return await response.json();
            } catch (error) {
                return { error: error.message };
            }
        }

        async function startSystem() {
            const result = await apiCall('/api/start', { autonomous: true });
            alert(JSON.stringify(result, null, 2));
            refreshStatus();
        }

        async function startSystemManual() {
            const result = await apiCall('/api/start', { autonomous: false });
            alert(JSON.stringify(result, null, 2));
            refreshStatus();
        }

        async function stopSystem() {
            const result = await apiCall('/api/stop');
            alert(JSON.stringify(result, null, 2));
            refreshStatus();
        }

        async function triggerEvolution() {
            const result = await apiCall('/api/evolve');
            alert(JSON.stringify(result, null, 2));
        }

        async function refreshStatus() {
            const status = await apiCall('/api/status');
            
            const indicator = document.getElementById('status-indicator');
            if (status.nexus_state && status.nexus_state.active) {
                indicator.innerHTML = '<span class="status-active">ACTIVE</span>';
            } else {
                indicator.innerHTML = '<span class="status-inactive">INACTIVE</span>';
            }

            // Update metrics
            if (status.metrics) {
                const metricsDiv = document.getElementById('metrics');
                metricsDiv.innerHTML = `
                    <div class="metric">
                        <div class="metric-value">${status.metrics.operations_completed}</div>
                        <div>Operations</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${status.metrics.autonomy_level.toFixed(3)}</div>
                        <div>Autonomy Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${status.metrics.errors_fixed}</div>
                        <div>Errors Fixed</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${status.metrics.code_improvements}</div>
                        <div>Improvements</div>
                    </div>
                `;
            }
        }

        async function searchMemory() {
            const query = document.getElementById('search-query').value;
            if (!query) return;
            
            const result = await apiCall('/api/search', { query });
            document.getElementById('search-results').textContent = JSON.stringify(result, null, 2);
        }

        async function submitChallenge() {
            const challenge = document.getElementById('challenge-input').value;
            if (!challenge) return;
            
            const result = await apiCall('/api/challenge', { challenge });
            document.getElementById('challenge-results').textContent = JSON.stringify(result, null, 2);
        }

        async function createModule() {
            const host = document.getElementById('module-host').value;
            if (!host) return;
            
            const result = await apiCall('/api/module/create', { host_system: host });
            document.getElementById('module-results').textContent = JSON.stringify(result, null, 2);
        }

        async function interactModule() {
            const moduleId = document.getElementById('module-id').value;
            const input = document.getElementById('module-input').value;
            if (!moduleId || !input) return;
            
            const result = await apiCall('/api/module/interact', { module_id: moduleId, input_data: input });
            document.getElementById('module-results').textContent = JSON.stringify(result, null, 2);
        }

        async function exportEvolution() {
            const result = await apiCall('/api/export');
            document.getElementById('export-results').textContent = JSON.stringify(result, null, 2);
        }

        // Auto-refresh status every 10 seconds
        setInterval(refreshStatus, 10000);
        
        // Initial status load
        refreshStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/start', methods=['POST'])
def api_start():
    data = request.get_json() or {}
    autonomous = data.get('autonomous', True)
    result = echo_interface.start_nexus(autonomous)
    return jsonify({'success': result})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    echo_interface.stop_nexus()
    return jsonify({'success': True})

@app.route('/api/status')
def api_status():
    return jsonify(echo_interface.status())

@app.route('/api/evolve', methods=['POST'])
def api_evolve():
    return jsonify(echo_interface.evolution_trigger())

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json()
    query = data.get('query', '')
    return jsonify(echo_interface.memory_search(query))

@app.route('/api/challenge', methods=['POST'])
def api_challenge():
    data = request.get_json()
    challenge = data.get('challenge', '')
    return jsonify(echo_interface.creative_challenge(challenge))

@app.route('/api/module/create', methods=['POST'])
def api_module_create():
    data = request.get_json()
    host_system = data.get('host_system', 'web_interface')
    return jsonify(echo_interface.module_create(host_system))

@app.route('/api/module/interact', methods=['POST'])
def api_module_interact():
    data = request.get_json()
    module_id = data.get('module_id', '')
    input_data = data.get('input_data', '')
    return jsonify(echo_interface.module_interact(module_id, input_data))

@app.route('/api/export', methods=['POST'])
def api_export():
    return jsonify(echo_interface.export_evolution_log())

if __name__ == '__main__':
    print("🌐 EchoWeb Interface starting on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
'''
    
    # Save web interface
    with open('echo_web.py', 'w') as f:
        f.write(web_interface_code)
    
    print("Created echo_web.py - Web interface for EchoNexusCore")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="EchoInterface - Offline Interface for EchoNexusCore")
    
    parser.add_argument('--project', default='.', help='Project directory')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive session')
    parser.add_argument('--web', action='store_true', help='Create web interface')
    parser.add_argument('--start', action='store_true', help='Start EchoNexusCore')
    parser.add_argument('--autonomous', '-a', action='store_true', help='Start in autonomous mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--evolve', metavar='REASON', help='Trigger evolution cycle')
    parser.add_argument('--search', metavar='QUERY', help='Search memory system')
    parser.add_argument('--challenge', metavar='CHALLENGE', help='Submit creative challenge')
    parser.add_argument('--export', action='store_true', help='Export evolution history')
    
    args = parser.parse_args()
    
    # Create interface
    interface = EchoCommandInterface(args.project)
    
    try:
        if args.web:
            create_web_interface()
            return 0
        
        if args.interactive:
            interface.run_interactive_session()
            return 0
        
        if args.start:
            result = interface.start_nexus(args.autonomous)
            print(f"Start result: {result}")
            
            # Keep running if started successfully
            if result:
                try:
                    print("EchoNexusCore running. Press Ctrl+C to stop.")
                    while interface.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nStopping EchoNexusCore...")
                    interface.stop_nexus()
            
            return 0
        
        if args.status:
            status = interface.status()
            print(json.dumps(status, indent=2))
            return 0
        
        if args.evolve:
            result = interface.evolution_trigger(args.evolve)
            print(json.dumps(result, indent=2))
            return 0
        
        if args.search:
            result = interface.memory_search(args.search)
            print(json.dumps(result, indent=2))
            return 0
        
        if args.challenge:
            result = interface.creative_challenge(args.challenge)
            print(json.dumps(result, indent=2))
            return 0
        
        if args.export:
            result = interface.export_evolution_log()
            print(json.dumps(result, indent=2))
            return 0
        
        # Default: show help
        parser.print_help()
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        interface._save_interface_config()


if __name__ == "__main__":
    sys.exit(main())
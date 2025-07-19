
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

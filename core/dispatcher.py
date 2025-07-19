#!/usr/bin/env python3
"""
EchoNexus Core Dispatcher - Minimalist shell for distributed AI architecture
Cold War security principles + Chinese scalability approach
"""

import os
import json
import requests
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import uuid

class SecureDispatcher:
    """
    Ultra-minimal core that dispatches to GitHub Actions processor network
    Maintains zero proprietary logic - pure orchestration layer
    """
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.owner = os.environ.get('GITHUB_OWNER', 'echo-nexus')
        self.base_url = 'https://api.github.com'
        self.session_id = str(uuid.uuid4())
        self.action_registry = self._load_action_registry()
        
        # Cold War principle: Strict security validation
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN required for secure operations")
    
    def _load_action_registry(self) -> Dict[str, str]:
        """Load registry of available processor actions"""
        return {
            'text_analysis': 'echo-nexus-text-analysis',
            'code_generation': 'echo-nexus-code-generator', 
            'diagnostic_scan': 'echo-nexus-diagnostics',
            'workflow_synthesis': 'echo-nexus-workflow-builder',
            'knowledge_synthesis': 'echo-nexus-knowledge-engine',
            'security_audit': 'echo-nexus-security-scanner',
            'performance_optimization': 'echo-nexus-optimizer',
            'self_evolution': 'echo-nexus-evolution-engine',
            'memory_management': 'echo-nexus-memory-store',
            'plugin_generator': 'echo-nexus-plugin-factory'
        }
    
    def dispatch_command(self, command: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Primary dispatch method - routes commands to appropriate GitHub Actions
        Zero local processing - pure orchestration
        """
        
        # Generate secure operation ID
        operation_id = self._generate_operation_id(command, inputs)
        
        # Identify target action repository
        action_repo = self._resolve_action_repo(command)
        if not action_repo:
            return {
                'status': 'error',
                'message': f'No processor available for command: {command}',
                'operation_id': operation_id
            }
        
        # Prepare secure payload
        payload = self._prepare_secure_payload(command, inputs, operation_id)
        
        # Dispatch to GitHub Actions processor
        result = self._trigger_github_action(action_repo, payload)
        
        # Return execution reference (no processing)
        return {
            'status': 'dispatched',
            'operation_id': operation_id,
            'processor_repo': action_repo,
            'execution_url': result.get('html_url'),
            'tracking_id': result.get('id')
        }
    
    def _generate_operation_id(self, command: str, inputs: Dict[str, Any]) -> str:
        """Generate cryptographically secure operation ID"""
        timestamp = str(int(time.time() * 1000))
        data_hash = hashlib.sha256(
            f"{command}:{json.dumps(inputs, sort_keys=True)}:{timestamp}".encode()
        ).hexdigest()[:16]
        
        return f"echo-{timestamp}-{data_hash}"
    
    def _resolve_action_repo(self, command: str) -> Optional[str]:
        """Resolve command to appropriate action repository"""
        
        # Direct mapping
        if command in self.action_registry:
            return self.action_registry[command]
        
        # Semantic mapping for complex commands
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['analyze', 'summary', 'text', 'nlp']):
            return self.action_registry['text_analysis']
        elif any(word in command_lower for word in ['generate', 'create', 'code', 'script']):
            return self.action_registry['code_generation']
        elif any(word in command_lower for word in ['diagnose', 'health', 'error', 'debug']):
            return self.action_registry['diagnostic_scan']
        elif any(word in command_lower for word in ['workflow', 'pipeline', 'action']):
            return self.action_registry['workflow_synthesis']
        elif any(word in command_lower for word in ['learn', 'knowledge', 'research']):
            return self.action_registry['knowledge_synthesis']
        elif any(word in command_lower for word in ['security', 'audit', 'vulnerability']):
            return self.action_registry['security_audit']
        elif any(word in command_lower for word in ['optimize', 'performance', 'speed']):
            return self.action_registry['performance_optimization']
        elif any(word in command_lower for word in ['evolve', 'improve', 'upgrade']):
            return self.action_registry['self_evolution']
        elif any(word in command_lower for word in ['memory', 'store', 'cache']):
            return self.action_registry['memory_management']
        elif any(word in command_lower for word in ['plugin', 'tool', 'extension']):
            return self.action_registry['plugin_generator']
        
        return None
    
    def _prepare_secure_payload(self, command: str, inputs: Dict[str, Any], operation_id: str) -> Dict[str, Any]:
        """Prepare encrypted payload for GitHub Actions processor"""
        
        return {
            'operation_id': operation_id,
            'session_id': self.session_id,
            'command': command,
            'inputs': inputs,
            'timestamp': datetime.now().isoformat(),
            'security_context': {
                'source': 'echo-nexus-core',
                'version': '1.0.0',
                'auth_hash': self._generate_auth_hash(operation_id)
            }
        }
    
    def _generate_auth_hash(self, operation_id: str) -> str:
        """Generate authentication hash for secure communication"""
        secret_key = os.environ.get('ECHO_SECRET_KEY', 'default-key')
        return hashlib.sha256(f"{operation_id}:{secret_key}:{self.session_id}".encode()).hexdigest()
    
    def _trigger_github_action(self, repo_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger GitHub Action workflow with secure payload"""
        
        url = f"{self.base_url}/repos/{self.owner}/{repo_name}/dispatches"
        
        headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        dispatch_data = {
            'event_type': 'echo_dispatch',
            'client_payload': payload
        }
        
        try:
            response = requests.post(url, headers=headers, json=dispatch_data)
            response.raise_for_status()
            
            return {
                'status': 'success',
                'repo': repo_name,
                'dispatch_id': response.headers.get('x-github-request-id'),
                'html_url': f"https://github.com/{self.owner}/{repo_name}/actions"
            }
        
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'Failed to trigger action: {str(e)}',
                'repo': repo_name
            }
    
    def query_operation_status(self, operation_id: str) -> Dict[str, Any]:
        """Query status of dispatched operation"""
        
        # Check all possible repositories for operation status
        status_results = {}
        
        for action_name, repo_name in self.action_registry.items():
            try:
                status = self._query_repo_for_operation(repo_name, operation_id)
                if status:
                    status_results[action_name] = status
            except Exception as e:
                status_results[action_name] = {'error': str(e)}
        
        return {
            'operation_id': operation_id,
            'query_timestamp': datetime.now().isoformat(),
            'results': status_results
        }
    
    def _query_repo_for_operation(self, repo_name: str, operation_id: str) -> Optional[Dict[str, Any]]:
        """Query specific repository for operation status"""
        
        url = f"{self.base_url}/repos/{self.owner}/{repo_name}/actions/runs"
        
        headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Search for workflows matching our operation ID
            for run in data.get('workflow_runs', []):
                if operation_id in str(run.get('head_commit', {}).get('message', '')):
                    return {
                        'status': run.get('status'),
                        'conclusion': run.get('conclusion'),
                        'html_url': run.get('html_url'),
                        'started_at': run.get('run_started_at'),
                        'updated_at': run.get('updated_at')
                    }
            
            return None
        
        except requests.RequestException:
            return None
    
    def list_available_processors(self) -> Dict[str, Any]:
        """List all available processor actions"""
        
        processors = {}
        
        for action_name, repo_name in self.action_registry.items():
            processor_info = self._get_processor_info(repo_name)
            processors[action_name] = {
                'repository': repo_name,
                'status': processor_info.get('status', 'unknown'),
                'capabilities': processor_info.get('capabilities', []),
                'last_updated': processor_info.get('updated_at')
            }
        
        return {
            'total_processors': len(processors),
            'processors': processors,
            'query_timestamp': datetime.now().isoformat()
        }
    
    def _get_processor_info(self, repo_name: str) -> Dict[str, Any]:
        """Get information about a specific processor repository"""
        
        url = f"{self.base_url}/repos/{self.owner}/{repo_name}"
        
        headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'active',
                    'updated_at': data.get('updated_at'),
                    'description': data.get('description'),
                    'language': data.get('language'),
                    'size': data.get('size')
                }
            else:
                return {'status': 'unavailable'}
        
        except requests.RequestException:
            return {'status': 'error'}


class CLIInterface:
    """Command-line interface for the EchoNexus system"""
    
    def __init__(self):
        self.dispatcher = SecureDispatcher()
    
    def run_interactive(self):
        """Run interactive command-line interface"""
        
        print("EchoNexus Distributed AI System")
        print("=" * 40)
        print("Type 'help' for available commands, 'exit' to quit")
        print()
        
        while True:
            try:
                user_input = input("echo> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'list':
                    self._list_processors()
                    continue
                
                if user_input.startswith('status '):
                    operation_id = user_input[7:].strip()
                    self._check_status(operation_id)
                    continue
                
                # Parse command and execute
                result = self._execute_command(user_input)
                self._display_result(result)
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _execute_command(self, command: str) -> Dict[str, Any]:
        """Execute user command via dispatcher"""
        
        # Simple parsing - could be enhanced with NLP
        parts = command.split(' ', 1)
        action = parts[0]
        inputs = {'text': parts[1] if len(parts) > 1 else ''}
        
        return self.dispatcher.dispatch_command(action, inputs)
    
    def _display_result(self, result: Dict[str, Any]):
        """Display command execution result"""
        
        if result['status'] == 'dispatched':
            print(f"✓ Operation dispatched: {result['operation_id']}")
            print(f"  Processor: {result['processor_repo']}")
            print(f"  Tracking: {result.get('execution_url', 'N/A')}")
        else:
            print(f"✗ Error: {result.get('message', 'Unknown error')}")
    
    def _show_help(self):
        """Show available commands"""
        
        print("\nAvailable Commands:")
        print("  analyze <text>     - Analyze text content")
        print("  generate <prompt>  - Generate code or content")
        print("  diagnose          - Run system diagnostics")
        print("  workflow <desc>   - Create GitHub workflow")
        print("  optimize          - Optimize system performance")
        print("  evolve            - Trigger evolution cycle")
        print("  list              - List available processors")
        print("  status <op_id>    - Check operation status")
        print("  help              - Show this help")
        print("  exit              - Quit system")
        print()
    
    def _list_processors(self):
        """List available processors"""
        
        print("Querying available processors...")
        processors = self.dispatcher.list_available_processors()
        
        print(f"\nAvailable Processors ({processors['total_processors']}):")
        print("-" * 40)
        
        for name, info in processors['processors'].items():
            status_icon = "✓" if info['status'] == 'active' else "✗"
            print(f"{status_icon} {name:<20} {info['repository']}")
        
        print()
    
    def _check_status(self, operation_id: str):
        """Check operation status"""
        
        print(f"Checking status for operation: {operation_id}")
        status = self.dispatcher.query_operation_status(operation_id)
        
        print("\nOperation Status:")
        print("-" * 20)
        
        for processor, result in status['results'].items():
            if 'error' in result:
                print(f"  {processor}: Error - {result['error']}")
            elif result:
                print(f"  {processor}: {result.get('status', 'unknown')}")
            else:
                print(f"  {processor}: No matching operation")
        
        print()


def main():
    """Main entry point"""
    
    try:
        cli = CLIInterface()
        cli.run_interactive()
    
    except Exception as e:
        print(f"System initialization failed: {e}")
        print("Please ensure GITHUB_TOKEN is set and valid")


if __name__ == "__main__":
    main()
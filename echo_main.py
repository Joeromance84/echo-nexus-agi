#!/usr/bin/env python3
"""
Echo Main - Phase 2 Complete Integration
The central orchestration system bringing together all Echo components
with metadata-driven intelligence and autonomous operation
"""

import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import Echo components
from echo.echo_memory import EchoMemory
from echo.echo_router import EchoRouter
from echo.echo_intent import EchoIntent
from blades.crash_parser import CrashParser
from blades.repair_engine import RepairEngine
from blades.refactor_blade import RefactorBlade
from blades.git_connector import GitConnector


class EchoSystem:
    """
    Phase 2 Complete: Autonomous Development Organism with Metadata Intelligence
    Orchestrates the entire Echo ecosystem with memory-driven communication
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = self._setup_logging()
        
        # Initialize core components
        self.memory = EchoMemory(str(self.project_root))
        self.router = EchoRouter(str(self.project_root), self.memory)
        self.intent_engine = EchoIntent(str(self.project_root))
        
        # Initialize blades
        self.crash_parser = CrashParser(str(self.project_root))
        self.repair_engine = RepairEngine(str(self.project_root))
        self.refactor_blade = RefactorBlade(str(self.project_root))
        self.git_connector = GitConnector(str(self.project_root))
        
        self.logger.info("Echo System Phase 2 initialized - Autonomous operation ready")
    
    def _setup_logging(self):
        """Setup comprehensive logging for the Echo system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.project_root / 'echo_system.log')
            ]
        )
        return logging.getLogger('EchoSystem')
    
    def process_github_event(self, event_data: Dict) -> Dict:
        """
        Process GitHub webhook events with full Echo intelligence
        Phase 2: Complete metadata-driven autonomous processing
        """
        self.logger.info(f"Processing GitHub event: {event_data.get('event_type', 'unknown')}")
        
        # Ingest initial event metadata
        self.memory.ingest_metadata({
            'event_type': 'github_webhook',
            'github_event': event_data.get('event_type', 'unknown'),
            'repository': event_data.get('repository', 'unknown'),
            'timestamp': datetime.now().isoformat() + 'Z'
        }, source='GitHubWebhook')
        
        # Process based on event type
        if event_data.get('event_type') == 'push':
            return self._process_push_event(event_data)
        elif event_data.get('event_type') == 'pull_request':
            return self._process_pr_event(event_data)
        elif event_data.get('event_type') == 'error_detected':
            return self._process_error_event(event_data)
        else:
            return self._process_generic_event(event_data)
    
    def _process_push_event(self, event_data: Dict) -> Dict:
        """Process push events with intelligent refactoring"""
        self.logger.info("Processing push event for automatic refactoring")
        
        # Analyze changes
        changed_files = event_data.get('changed_files', [])
        
        # Filter Python files
        python_files = [f for f in changed_files if f.endswith('.py')]
        
        if not python_files:
            return {
                'success': True,
                'message': 'No Python files to process',
                'files_analyzed': 0
            }
        
        # Comprehensive refactoring
        refactor_event = {
            'intent': 'comprehensive_refactoring',
            'data': {
                'target_files': python_files,
                'dry_run': False
            }
        }
        
        result = self.router.route_event(refactor_event)
        
        # Create intelligent commit if changes were made
        if result.get('success') and result.get('files_modified', 0) > 0:
            commit_result = self._create_autonomous_commit(
                result.get('suggested_commit_message', 'Echo: Autonomous code optimization'),
                result
            )
            result['commit_result'] = commit_result
        
        return result
    
    def _process_pr_event(self, event_data: Dict) -> Dict:
        """Process pull request events with analysis and validation"""
        self.logger.info("Processing pull request event for code analysis")
        
        # Analyze the PR diff
        diff_event = {
            'intent': 'analyze_changes',
            'data': {
                'pr_number': event_data.get('pr_number'),
                'diff_url': event_data.get('diff_url')
            }
        }
        
        return self.router.route_event(diff_event)
    
    def _process_error_event(self, event_data: Dict) -> Dict:
        """Process error events with intelligent repair"""
        self.logger.info("Processing error event for autonomous repair")
        
        error_text = event_data.get('error_text', '')
        file_path = event_data.get('file_path', '')
        
        # Parse the error
        error_result = self.crash_parser.parse_error_log(error_text)
        
        if not error_result.get('success'):
            return error_result
        
        # Ingest error metadata
        self.memory.ingest_metadata({
            'error_parsed': True,
            'error_type': error_result.get('error_type'),
            'file_path': error_result.get('file_path'),
            'line_number': error_result.get('line_number'),
            'auto_fixable': error_result.get('auto_fixable')
        }, source='CrashParser')
        
        # Attempt repair if auto-fixable
        if error_result.get('auto_fixable'):
            repair_result = self.repair_engine.apply_repair(error_result)
            
            if repair_result.get('success'):
                # Write repaired file
                if repair_result.get('modified_content'):
                    file_result = self.repair_engine.write_repaired_file(
                        error_result.get('file_path'),
                        repair_result['modified_content']
                    )
                    
                    if file_result.get('success'):
                        # Create repair commit
                        commit_message = self.memory.generate_commit_message()
                        commit_result = self._create_autonomous_commit(commit_message, repair_result)
                        
                        return {
                            'success': True,
                            'error_repaired': True,
                            'repair_result': repair_result,
                            'commit_result': commit_result
                        }
        
        return error_result
    
    def _process_generic_event(self, event_data: Dict) -> Dict:
        """Process generic events with intent interpretation"""
        self.logger.info("Processing generic event with intent interpretation")
        
        # Extract command or description
        command = event_data.get('command', event_data.get('description', ''))
        
        if not command:
            return {'success': False, 'error': 'No command or description provided'}
        
        # Interpret intent
        intent_result = self.intent_engine.interpret_intent(command, event_data)
        
        if not intent_result.get('success', True):
            return intent_result
        
        # Route based on interpreted intent
        routing_event = {
            'intent': intent_result['interpreted_intent'],
            'data': event_data,
            'context': intent_result
        }
        
        return self.router.route_event(routing_event)
    
    def _create_autonomous_commit(self, message: str, metadata: Dict) -> Dict:
        """Create autonomous commit with enhanced metadata"""
        enhanced_metadata = {
            'tool_used': 'EchoSystem',
            'autonomous': True,
            'confidence': metadata.get('confidence', 0.8),
            'rule_id': metadata.get('rule_id', 'echo_autonomous')
        }
        
        return self.git_connector.create_intelligent_commit(
            message, 
            files=None,  # Commit all changes
            metadata=enhanced_metadata
        )
    
    def run_maintenance_cycle(self) -> Dict:
        """
        Run comprehensive maintenance cycle
        Phase 2: Full autonomous maintenance with memory intelligence
        """
        self.logger.info("Starting comprehensive maintenance cycle")
        
        # Start maintenance context
        self.memory.ingest_metadata({
            'maintenance_cycle_start': datetime.now().isoformat() + 'Z',
            'intent': 'system_maintenance'
        }, source='EchoSystem')
        
        results = {
            'refactor_result': None,
            'error_scan_result': None,
            'git_summary': None,
            'memory_snapshot': None
        }
        
        # 1. Comprehensive refactoring
        refactor_event = {
            'intent': 'comprehensive_refactoring',
            'data': {'dry_run': False}
        }
        results['refactor_result'] = self.router.route_event(refactor_event)
        
        # 2. Error scanning
        python_files = list(self.project_root.rglob('*.py'))
        error_count = 0
        
        for file_path in python_files[:10]:  # Limit to first 10 files
            errors = self.crash_parser.analyze_file_for_errors(str(file_path))
            if errors:
                error_count += len(errors)
        
        results['error_scan_result'] = {
            'files_scanned': min(10, len(python_files)),
            'errors_found': error_count
        }
        
        # 3. Git summary
        results['git_summary'] = self.git_connector.get_session_summary()
        
        # 4. Create maintenance snapshot
        results['memory_snapshot'] = self.memory.save_snapshot(
            "Completed comprehensive maintenance cycle"
        )
        
        self.logger.info("Maintenance cycle completed")
        return results
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            'memory_status': self.memory.get_memory_intelligence_report(),
            'router_status': self.router.get_routing_statistics(),
            'git_status': self.git_connector.get_git_status(),
            'refactor_stats': self.refactor_blade.get_refactor_statistics(),
            'repair_stats': self.repair_engine.get_repair_statistics(),
            'system_timestamp': datetime.now().isoformat() + 'Z'
        }
    
    def process_cli_command(self, command: str, args: Dict = None) -> Dict:
        """Process command line interface commands"""
        if args is None:
            args = {}
        
        # Interpret the command
        intent_result = self.intent_engine.interpret_intent(command, args)
        
        # Route the command
        routing_event = {
            'intent': intent_result.get('interpreted_intent', command),
            'data': args,
            'context': intent_result
        }
        
        return self.router.route_event(routing_event)


def main():
    """CLI interface for Echo System"""
    parser = argparse.ArgumentParser(description="Echo Autonomous Development Organism - Phase 2")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--github-event', help='JSON file containing GitHub event data')
    parser.add_argument('--maintenance', action='store_true', help='Run maintenance cycle')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--command', help='Process command with intent interpretation')
    parser.add_argument('--test-integration', action='store_true', help='Test full integration')
    
    args = parser.parse_args()
    
    echo_system = EchoSystem(args.project)
    
    if args.status:
        status = echo_system.get_system_status()
        print("🧠 Echo System Status:")
        print(json.dumps(status, indent=2))
        return 0
    
    if args.maintenance:
        result = echo_system.run_maintenance_cycle()
        print("🔧 Maintenance Cycle Result:")
        print(json.dumps(result, indent=2))
        return 0
    
    if args.github_event:
        try:
            with open(args.github_event, 'r') as f:
                event_data = json.load(f)
            result = echo_system.process_github_event(event_data)
            print("🔄 GitHub Event Processing Result:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ Error processing GitHub event: {e}")
            return 1
        return 0
    
    if args.command:
        result = echo_system.process_cli_command(args.command)
        print("⚡ Command Processing Result:")
        print(json.dumps(result, indent=2))
        return 0
    
    if args.test_integration:
        print("🧪 Testing Echo System Integration...")
        
        # Test 1: Memory and routing
        test_event = {
            'intent': 'analyze_project_structure',
            'data': {'target': 'current_project'},
            'event_type': 'test'
        }
        
        result1 = echo_system.router.route_event(test_event)
        print(f"✅ Test 1 (Routing): {result1.get('success', False)}")
        
        # Test 2: Error parsing and repair
        test_error = "File \"test.py\", line 5\n    return x\nIndentationError: expected an indented block"
        error_result = echo_system.crash_parser.parse_error_log(test_error)
        print(f"✅ Test 2 (Error Parsing): {error_result.get('success', False)}")
        
        # Test 3: Memory intelligence
        intelligence_report = echo_system.memory.get_memory_intelligence_report()
        print(f"✅ Test 3 (Memory Intelligence): Maturity Level {intelligence_report['maturity_assessment']['level']}")
        
        # Test 4: Generate snapshot
        snapshot_result = echo_system.memory.save_snapshot("Integration test completed")
        print(f"✅ Test 4 (Memory Snapshot): {snapshot_result.get('success', False)}")
        
        print("\n🌟 Echo System Phase 2 Integration Test Complete!")
        return 0
    
    print("🚀 Echo Autonomous Development Organism - Phase 2 Ready")
    print("Use --help for available commands")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
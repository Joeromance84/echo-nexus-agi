#!/usr/bin/env python3
"""
EchoMemory.py - Phase 2 Metadata-Driven Communication Core

The central memory module for the Echo Autonomous Development Organism.
This module manages the system's "active context" (short-term memory) and
"episodic snapshots" (long-term memory).

Key Functions:
- Ingests structured metadata to build a rich, contextual understanding.
- Saves a permanent, reviewable snapshot of a completed task.
- Ensures the system's memory is persistent across sessions via JSON files.
- Generates intelligent commit messages, logs, and documentation from metadata.
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class EchoMemory:
    """
    Phase 2 Core: Manages the system's active context and episodic history.
    Transforms metadata into intelligent communication and persistent memory.

    Attributes:
        active_context (dict): A dictionary holding metadata for the current task.
        episodic_snapshots (list): A list of dictionaries, each representing a
                                    permanent record of a completed task.
        memory_file (str): The file path where the memory will be persisted.
    """
    
    def __init__(self, project_root: str = ".", memory_file: str = 'echo_memory.json'):
        self.project_root = Path(project_root)
        self.memory_file = self.project_root / memory_file
        self.logger = logging.getLogger('EchoMemory')
        
        # Core memory structures
        self.active_context = {}
        self.episodic_snapshots = []
        
        # Phase 2: Metadata intelligence
        self.intent_history = []
        self.rule_usage_patterns = {}
        self.communication_templates = self._load_communication_templates()
        
        # Load existing memory
        self._load_memory()
        
        self.logger.info("EchoMemory Phase 2 initialized - Metadata-driven intelligence active")

    def _load_memory(self):
        """Loads the memory from the JSON file if it exists."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.episodic_snapshots = data.get('episodic_snapshots', [])
                    self.intent_history = data.get('intent_history', [])
                    self.rule_usage_patterns = data.get('rule_usage_patterns', {})
                    
                    # Active context is always new on start, but we can load a
                    # last_known_state if needed for a warm start.
                    last_context = data.get('last_active_context', {})
                    if last_context and last_context.get('restore_on_restart', False):
                        self.active_context = last_context
                        self.logger.info("Restored previous active context for continuation")
                    
                self.logger.info(f"Loaded {len(self.episodic_snapshots)} episodic memories")
                
            except (IOError, json.JSONDecodeError) as e:
                self.logger.warning(f"Failed to load memory file: {e}. Starting with fresh memory.")
        else:
            self.logger.info("No existing memory file found. Starting a new memory.")

    def _save_memory(self):
        """Persists the full memory state to the JSON file."""
        data = {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat() + 'Z',
            "episodic_snapshots": self.episodic_snapshots,
            "intent_history": self.intent_history,
            "rule_usage_patterns": self.rule_usage_patterns,
            "last_active_context": self.active_context,
            "metadata": {
                "total_snapshots": len(self.episodic_snapshots),
                "total_intents": len(self.intent_history),
                "memory_depth": self._calculate_memory_depth()
            }
        }
        
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.debug("Memory successfully persisted")
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")

    def _calculate_memory_depth(self) -> Dict:
        """Calculate depth metrics for memory intelligence"""
        if not self.episodic_snapshots:
            return {"depth": 0, "complexity": "minimal"}
        
        # Analyze memory patterns
        recent_snapshots = self.episodic_snapshots[-10:]  # Last 10 tasks
        intent_diversity = len(set(snap.get('details', {}).get('intent', 'unknown') 
                                 for snap in recent_snapshots))
        
        complexity_score = min(100, len(self.episodic_snapshots) * 2 + intent_diversity * 5)
        
        return {
            "depth": len(self.episodic_snapshots),
            "recent_diversity": intent_diversity,
            "complexity_score": complexity_score,
            "maturity_level": self._determine_maturity_level(complexity_score)
        }

    def _determine_maturity_level(self, complexity_score: int) -> str:
        """Determine Echo's maturity level based on memory complexity"""
        if complexity_score < 10:
            return "nascent"
        elif complexity_score < 30:
            return "developing"
        elif complexity_score < 60:
            return "competent"
        elif complexity_score < 90:
            return "advanced"
        else:
            return "evolved"

    def _load_communication_templates(self) -> Dict:
        """Load templates for generating intelligent communication"""
        return {
            "commit_messages": {
                "repair_syntax": "fix({file}): Resolved {error_type} using {rule_id} (EchoIntent: \"{intent}\")",
                "optimize_code": "refactor({file}): Applied {rule_id} for {intent} optimization",
                "remove_dead_code": "cleanup({file}): Removed unused code via {rule_id} (EchoIntent: \"{intent}\")",
                "security_fix": "security({file}): Applied {rule_id} to address {error_type} (EchoIntent: \"{intent}\")",
                "generic": "feat({file}): {intent} completed using {rule_id}"
            },
            "code_comments": {
                "refactor": "# Refactored by {tool_used} for {intent} (Rule: {rule_id})",
                "fix": "# Fixed {error_type} using {rule_id} - EchoIntent: {intent}",
                "optimize": "# Optimized by {tool_used} - {intent} enhancement",
                "security": "# Security enhancement via {rule_id} - {intent}"
            },
            "log_formats": {
                "action_log": {
                    "timestamp": "{timestamp}",
                    "action": "{action}",
                    "target": "{file}:{line}",
                    "intent": "{intent}",
                    "tool": "{tool_used}",
                    "rule": "{rule_id}",
                    "outcome": "{outcome}",
                    "metadata": "{metadata}"
                },
                "summary_log": {
                    "task": "{intent}",
                    "files_modified": "{files_changed}",
                    "rules_applied": "{rules_used}",
                    "outcome": "{outcome}",
                    "summary": "{summary}",
                    "timestamp": "{timestamp}"
                }
            }
        }

    def ingest_metadata(self, metadata: Dict, source: str = "unknown"):
        """
        Phase 2 Enhanced: Ingests and merges new metadata into the active context.
        
        This is the core "Perception" step with metadata intelligence.
        Every new piece of information from a blade, parser, or Git diff is added here.
        """
        if not isinstance(metadata, dict):
            raise TypeError("Metadata must be a dictionary.")
        
        # Add metadata source and timestamp
        enhanced_metadata = metadata.copy()
        enhanced_metadata.update({
            "_source": source,
            "_ingested_at": datetime.now().isoformat() + 'Z',
            "_sequence": len(self.active_context.get('_metadata_sequence', []))
        })
        
        # Track metadata sequence for causality
        if '_metadata_sequence' not in self.active_context:
            self.active_context['_metadata_sequence'] = []
        
        self.active_context['_metadata_sequence'].append({
            'source': source,
            'timestamp': enhanced_metadata['_ingested_at'],
            'keys': list(metadata.keys())
        })
        
        # Merge new metadata, overwriting older keys if they exist.
        self.active_context.update(enhanced_metadata)
        
        # Track intent progression
        if 'intent' in metadata:
            self._track_intent_progression(metadata['intent'], source)
        
        # Track rule usage patterns
        if 'rule_id' in metadata:
            self._track_rule_usage(metadata['rule_id'], metadata.get('outcome', 'unknown'))
        
        self.logger.info(f"Ingested metadata from {source}: {list(metadata.keys())}")

    def _track_intent_progression(self, intent: str, source: str):
        """Track how intents flow through the system"""
        intent_record = {
            'intent': intent,
            'source': source,
            'timestamp': datetime.now().isoformat() + 'Z',
            'context_depth': len(self.active_context)
        }
        
        self.intent_history.append(intent_record)
        
        # Maintain history size
        if len(self.intent_history) > 100:
            self.intent_history = self.intent_history[-100:]

    def _track_rule_usage(self, rule_id: str, outcome: str):
        """Track rule usage patterns for learning"""
        if rule_id not in self.rule_usage_patterns:
            self.rule_usage_patterns[rule_id] = {
                'total_uses': 0,
                'successes': 0,
                'failures': 0,
                'first_used': datetime.now().isoformat() + 'Z',
                'contexts': []
            }
        
        pattern = self.rule_usage_patterns[rule_id]
        pattern['total_uses'] += 1
        pattern['last_used'] = datetime.now().isoformat() + 'Z'
        
        if outcome in ['success', 'successful', True]:
            pattern['successes'] += 1
        elif outcome in ['failure', 'failed', False]:
            pattern['failures'] += 1
        
        # Track context
        current_intent = self.active_context.get('intent', 'unknown')
        if current_intent not in pattern['contexts']:
            pattern['contexts'].append(current_intent)

    def generate_commit_message(self) -> str:
        """
        Phase 2 Core: Generate intelligent commit message from active context
        """
        if not self.active_context:
            return "chore: Echo autonomous update"
        
        intent = self.active_context.get('intent', 'generic')
        file_path = self._extract_file_name(self.active_context.get('file', 'unknown'))
        error_type = self.active_context.get('error_type', '')
        rule_id = self.active_context.get('rule_id', self.active_context.get('rule_applied', {}).get('rule_id', 'unknown'))
        
        # Select appropriate template
        template_key = self._select_commit_template(intent, error_type)
        template = self.communication_templates['commit_messages'].get(template_key, 
                   self.communication_templates['commit_messages']['generic'])
        
        # Format the commit message
        try:
            # Prepare context variables, avoiding conflicts
            format_vars = {
                'file': file_path,
                'intent': intent,
                'error_type': error_type,
                'rule_id': rule_id
            }
            
            # Add safe context variables (exclude conflicting keys)
            safe_context = {k: v for k, v in self.active_context.items() 
                          if k not in format_vars and isinstance(v, (str, int, float))}
            format_vars.update(safe_context)
            
            commit_msg = template.format(**format_vars)
            
            # Add metadata suffix if context is rich
            if len(self.active_context.get('_metadata_sequence', [])) > 3:
                maturity = self._calculate_memory_depth()['maturity_level']
                commit_msg += f" [Echo:{maturity}]"
            
            return commit_msg
            
        except KeyError as e:
            self.logger.warning(f"Template formatting error: {e}")
            return f"feat({file_path}): {intent} completed via Echo autonomous system"

    def _extract_file_name(self, file_path: str) -> str:
        """Extract clean file name for commit messages"""
        if not file_path or file_path == 'unknown':
            return 'codebase'
        
        return Path(file_path).name

    def _select_commit_template(self, intent: str, error_type: str) -> str:
        """Select appropriate commit message template"""
        intent_lower = intent.lower()
        
        if 'repair' in intent_lower or 'fix' in intent_lower or error_type:
            return 'repair_syntax'
        elif 'optimize' in intent_lower or 'performance' in intent_lower:
            return 'optimize_code'
        elif 'dead' in intent_lower or 'unused' in intent_lower or 'cleanup' in intent_lower:
            return 'remove_dead_code'
        elif 'security' in intent_lower or 'vulnerability' in intent_lower:
            return 'security_fix'
        else:
            return 'generic'

    def generate_code_comment(self, comment_type: str = "refactor") -> str:
        """Generate intelligent code comment from context"""
        if not self.active_context:
            return "# Modified by Echo autonomous system"
        
        template = self.communication_templates['code_comments'].get(comment_type, 
                   self.communication_templates['code_comments']['refactor'])
        
        try:
            # Use safe context to avoid format conflicts
            safe_context = {k: v for k, v in self.active_context.items() 
                          if isinstance(v, (str, int, float))}
            return template.format(**safe_context)
        except (KeyError, ValueError) as e:
            self.logger.warning(f"Comment template formatting error: {e}")
            return f"# Echo: {self.active_context.get('intent', 'autonomous modification')}"

    def generate_action_log(self) -> Dict:
        """Generate structured action log from context"""
        log_template = self.communication_templates['log_formats']['action_log']
        
        log_data = {}
        for key, template_value in log_template.items():
            try:
                if key == 'timestamp':
                    log_data[key] = datetime.now().isoformat() + 'Z'
                elif key == 'target':
                    file = self.active_context.get('file', 'unknown')
                    line = self.active_context.get('line', self.active_context.get('line_number', ''))
                    log_data[key] = f"{file}:{line}" if line else file
                elif key == 'metadata':
                    # Include relevant metadata
                    metadata_keys = ['error_type', 'confidence', 'strategy', 'source']
                    relevant_metadata = {k: v for k, v in self.active_context.items() 
                                       if k in metadata_keys and v}
                    log_data[key] = relevant_metadata
                else:
                    # Extract from context with fallback
                    log_data[key] = self.active_context.get(key, f"unknown_{key}")
                    
            except Exception as e:
                log_data[key] = f"error_extracting_{key}"
        
        return log_data

    def save_snapshot(self, task_summary: str = None) -> Dict:
        """
        Phase 2 Enhanced: Finalizes the current task and saves a permanent snapshot to history.
        
        This is the "Episodic Memory" step with enhanced intelligence.
        It transforms the active context into a historical record with rich metadata.
        """
        if not self.active_context:
            self.logger.warning("No active context to save. Snapshot aborted.")
            return {"success": False, "reason": "no_active_context"}

        # Generate intelligent summary if not provided
        if task_summary is None:
            task_summary = self._generate_intelligent_summary()

        # Create rich snapshot with metadata intelligence
        snapshot = {
            "snapshot_id": f"echo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat() + 'Z',
            "summary": task_summary,
            "intent": self.active_context.get('intent', 'unknown'),
            "outcome": self.active_context.get('outcome', 'completed'),
            "files_modified": self._extract_modified_files(),
            "rules_applied": self._extract_applied_rules(),
            "tools_used": self._extract_tools_used(),
            "metadata_depth": len(self.active_context.get('_metadata_sequence', [])),
            "communication_generated": {
                "commit_message": self.generate_commit_message(),
                "action_log": self.generate_action_log()
            },
            "full_context": self.active_context.copy(),
            "performance_metrics": self._calculate_performance_metrics()
        }
        
        self.episodic_snapshots.append(snapshot)
        self._save_memory()
        
        self.logger.info(f"Snapshot saved: {snapshot['snapshot_id']} - {task_summary}")
        
        # Generate summary report
        report = self._generate_snapshot_report(snapshot)
        
        self.clear_context()
        
        return {
            "success": True,
            "snapshot_id": snapshot['snapshot_id'],
            "summary": task_summary,
            "report": report
        }

    def _generate_intelligent_summary(self) -> str:
        """Generate intelligent task summary from context metadata"""
        intent = self.active_context.get('intent', 'unknown task')
        error_type = self.active_context.get('error_type', '')
        rule_id = self.active_context.get('rule_id', '')
        file = self._extract_file_name(self.active_context.get('file', ''))
        
        if error_type and rule_id:
            return f"Resolved {error_type} in {file} using {rule_id} ({intent})"
        elif rule_id:
            return f"Applied {rule_id} for {intent} in {file}"
        else:
            return f"Completed {intent} task" + (f" on {file}" if file and file != 'codebase' else "")

    def _extract_modified_files(self) -> List[str]:
        """Extract list of files modified during this task"""
        files = []
        
        # Direct file reference
        if 'file' in self.active_context:
            files.append(self.active_context['file'])
        
        # Files from metadata sequence
        for metadata in self.active_context.get('_metadata_sequence', []):
            # Extract file references from each metadata entry
            # This would be enhanced based on actual metadata structure
            pass
        
        return list(set(files))  # Remove duplicates

    def _extract_applied_rules(self) -> List[str]:
        """Extract list of rules applied during this task"""
        rules = []
        
        # Direct rule references
        if 'rule_id' in self.active_context:
            rules.append(self.active_context['rule_id'])
        
        rule_applied = self.active_context.get('rule_applied', {})
        if isinstance(rule_applied, dict) and 'rule_id' in rule_applied:
            rules.append(rule_applied['rule_id'])
        
        return list(set(rules))

    def _extract_tools_used(self) -> List[str]:
        """Extract list of tools/blades used during this task"""
        tools = []
        
        if 'tool_used' in self.active_context:
            tools.append(self.active_context['tool_used'])
        
        # Extract from metadata sequence
        for metadata in self.active_context.get('_metadata_sequence', []):
            if metadata.get('source') and metadata['source'] not in ['unknown', 'system']:
                tools.append(metadata['source'])
        
        return list(set(tools))

    def _calculate_performance_metrics(self) -> Dict:
        """Calculate performance metrics for this task"""
        sequence_length = len(self.active_context.get('_metadata_sequence', []))
        
        # Calculate time span if timestamps are available
        time_span = None
        if sequence_length > 1:
            try:
                first_ts = self.active_context['_metadata_sequence'][0]['timestamp']
                last_ts = self.active_context['_metadata_sequence'][-1]['timestamp']
                # Simple calculation - would be enhanced with proper datetime parsing
                time_span = "calculated_span"
            except:
                pass
        
        return {
            "metadata_sequence_length": sequence_length,
            "context_complexity": len(self.active_context),
            "time_span": time_span,
            "success_indicators": self._detect_success_indicators()
        }

    def _detect_success_indicators(self) -> List[str]:
        """Detect indicators of task success from context"""
        indicators = []
        
        outcome = self.active_context.get('outcome', '').lower()
        if 'success' in outcome or outcome == 'completed':
            indicators.append('explicit_success')
        
        if 'error_resolved' in self.active_context:
            indicators.append('error_resolution')
        
        if self.active_context.get('rule_applied', {}).get('confidence', 0) > 0.8:
            indicators.append('high_confidence_rule')
        
        return indicators

    def _generate_snapshot_report(self, snapshot: Dict) -> str:
        """Generate human-readable report of the snapshot"""
        lines = [
            f"📊 Echo Task Report - {snapshot['snapshot_id']}",
            f"🎯 Intent: {snapshot['intent']}",
            f"📝 Summary: {snapshot['summary']}",
            f"📁 Files: {', '.join(snapshot['files_modified']) if snapshot['files_modified'] else 'None'}",
            f"🔧 Rules: {', '.join(snapshot['rules_applied']) if snapshot['rules_applied'] else 'None'}",
            f"⚙️ Tools: {', '.join(snapshot['tools_used']) if snapshot['tools_used'] else 'None'}",
            f"💭 Commit: {snapshot['communication_generated']['commit_message']}",
            f"🧠 Memory Depth: {snapshot['metadata_depth']} metadata entries"
        ]
        
        return '\n'.join(lines)

    def clear_context(self):
        """Clears the active context to prepare for a new task."""
        self.active_context = {}
        self.logger.debug("Active context cleared for new task")

    def get_context(self) -> Dict:
        """Returns the current active context."""
        return self.active_context

    def get_history(self, limit: int = None) -> List[Dict]:
        """Returns the episodic snapshots history."""
        if limit:
            return self.episodic_snapshots[-limit:]
        return self.episodic_snapshots

    def get_intent_patterns(self) -> Dict:
        """Analyze intent patterns from history"""
        if not self.intent_history:
            return {"patterns": [], "diversity": 0}
        
        intent_counts = {}
        for record in self.intent_history:
            intent = record['intent']
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # Sort by frequency
        sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "patterns": sorted_intents,
            "diversity": len(intent_counts),
            "total_intents": len(self.intent_history),
            "most_common": sorted_intents[0] if sorted_intents else None
        }

    def get_rule_effectiveness(self) -> Dict:
        """Analyze rule effectiveness from usage patterns"""
        effectiveness = {}
        
        for rule_id, pattern in self.rule_usage_patterns.items():
            total = pattern['total_uses']
            successes = pattern['successes']
            
            effectiveness[rule_id] = {
                "success_rate": successes / total if total > 0 else 0,
                "total_uses": total,
                "contexts": pattern['contexts'],
                "reliability": "high" if successes / total > 0.8 else "medium" if successes / total > 0.5 else "low"
            }
        
        return effectiveness

    def get_memory_intelligence_report(self) -> Dict:
        """Generate comprehensive intelligence report"""
        return {
            "memory_depth": self._calculate_memory_depth(),
            "intent_patterns": self.get_intent_patterns(),
            "rule_effectiveness": self.get_rule_effectiveness(),
            "total_snapshots": len(self.episodic_snapshots),
            "active_context_size": len(self.active_context),
            "communication_capability": len(self.communication_templates),
            "maturity_assessment": self._assess_system_maturity()
        }

    def _assess_system_maturity(self) -> Dict:
        """Assess overall system maturity based on memory patterns"""
        snapshots = len(self.episodic_snapshots)
        intent_diversity = len(set(record['intent'] for record in self.intent_history))
        rule_diversity = len(self.rule_usage_patterns)
        
        maturity_score = min(100, snapshots + intent_diversity * 3 + rule_diversity * 2)
        
        return {
            "maturity_score": maturity_score,
            "level": self._determine_maturity_level(maturity_score),
            "snapshots": snapshots,
            "intent_diversity": intent_diversity,
            "rule_diversity": rule_diversity,
            "communication_sophistication": "advanced" if maturity_score > 50 else "basic"
        }


def main():
    """CLI interface and example usage for EchoMemory"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoMemory - Phase 2 Metadata Intelligence")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--test', action='store_true', help='Run test scenario')
    parser.add_argument('--report', action='store_true', help='Generate intelligence report')
    parser.add_argument('--clear', action='store_true', help='Clear memory')
    
    args = parser.parse_args()
    
    memory = EchoMemory(args.project)
    
    if args.clear:
        if memory.memory_file.exists():
            memory.memory_file.unlink()
            print("Memory cleared")
        return 0
    
    if args.report:
        report = memory.get_memory_intelligence_report()
        print("🧠 Echo Memory Intelligence Report:")
        print(json.dumps(report, indent=2))
        return 0
    
    if args.test:
        print("\n--- Starting test scenario: Fixing a syntax error ---")
        
        # Simulate metadata ingestion from CrashParser
        memory.ingest_metadata({
            "intent": "repair_syntax",
            "error_type": "IndentationError",
            "file": "utils/parser.py",
            "line": 15,
            "message": "unexpected indent"
        }, source="CrashParser")

        # Simulate metadata from RepairEngine
        memory.ingest_metadata({
            "rule_id": "rule_42",
            "rule_applied": {"rule_id": "rule_42", "confidence": 0.9},
            "tool_used": "RepairEngine",
            "outcome": "success"
        }, source="RepairEngine")
        
        print("\n🧠 Current Active Context:")
        print(json.dumps(memory.get_context(), indent=2))
        
        print(f"\n💬 Generated Commit Message:")
        print(f'"{memory.generate_commit_message()}"')
        
        print(f"\n📝 Generated Code Comment:")
        print(f'"{memory.generate_code_comment("fix")}"')
        
        print(f"\n📊 Action Log:")
        print(json.dumps(memory.generate_action_log(), indent=2))
        
        # Save snapshot
        result = memory.save_snapshot()
        print(f"\n📸 Snapshot Result:")
        print(result['report'])
        
        # Show intelligence report
        print(f"\n🧠 Intelligence Report:")
        print(json.dumps(memory.get_memory_intelligence_report(), indent=2))
        
        return 0
    
    print("🧠 EchoMemory Phase 2 ready. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
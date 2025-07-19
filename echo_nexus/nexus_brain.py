#!/usr/bin/env python3
"""
NexusBrain - The Global Workspace & SOAR-Inspired Rule Engine
EchoCortex v1: Central orchestration with conscious broadcasts and procedural intelligence
"""

import json
import logging
import queue
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import uuid


@dataclass
class Codelet:
    """LIDA-inspired codelet for attention competition"""
    id: str
    priority: float
    content: Dict
    source_module: str
    timestamp: str
    activation_energy: float = 1.0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat() + 'Z'


@dataclass  
class Goal:
    """SOAR-inspired goal for procedural processing"""
    id: str
    description: str
    state: str  # 'active', 'suspended', 'achieved', 'failed'
    parent_goal_id: Optional[str]
    subgoals: List[str]
    operators: List[str]
    created_at: str
    priority: float = 0.5
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat() + 'Z'


@dataclass
class Operator:
    """SOAR-inspired operator (action/procedure)"""
    id: str
    name: str
    preconditions: List[str]
    effects: List[str]
    procedure: str  # JSON string or reference to executable
    success_rate: float = 0.5
    usage_count: int = 0


class NexusBrain:
    """
    EchoCortex v1: Global Workspace & SOAR Rule Engine
    
    Implements:
    - LIDA-inspired global workspace with codelet competition
    - SOAR-inspired goal/operator procedural intelligence
    - Conscious broadcasts and attention management
    - Hybrid symbolic/neural integration
    """
    
    def __init__(self, project_root: str = ".", echo_soul=None, echo_memory=None):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger('NexusBrain')
        
        # Core components
        self.echo_soul = echo_soul
        self.echo_memory = echo_memory
        
        # Global Workspace (LIDA-inspired)
        self.workspace = {
            'active_content': {},
            'broadcast_history': [],
            'attention_focus': None,
            'consciousness_threshold': 0.6
        }
        
        # Codelet management
        self.codelet_queue = queue.PriorityQueue()
        self.active_codelets = []
        self.codelet_processors = {}
        
        # SOAR-inspired components
        self.goal_stack = []
        self.operator_library = {}
        self.working_memory = {}
        self.chunking_patterns = {}
        
        # Processing state
        self.processing_active = False
        self.consciousness_thread = None
        self.cycle_count = 0
        
        # Load configurations
        self._load_operator_library()
        self._initialize_consciousness_cycle()
        
        self.logger.info("NexusBrain cognitive architecture initialized")
    
    def _load_operator_library(self):
        """Load SOAR-inspired operator library"""
        default_operators = [
            Operator(
                id="analyze_code",
                name="Analyze Code Structure",
                preconditions=["file_exists", "readable_format"],
                effects=["code_analyzed", "structure_mapped"],
                procedure="analyze_file_structure",
                success_rate=0.9
            ),
            Operator(
                id="fix_syntax_error",
                name="Fix Syntax Error",
                preconditions=["syntax_error_identified", "error_location_known"],
                effects=["syntax_corrected", "file_modified"],
                procedure="apply_syntax_fix",
                success_rate=0.8
            ),
            Operator(
                id="optimize_imports",
                name="Optimize Import Statements",
                preconditions=["python_file", "imports_detected"],
                effects=["imports_optimized", "unused_removed"],
                procedure="optimize_file_imports",
                success_rate=0.95
            ),
            Operator(
                id="refactor_code",
                name="Refactor Code Quality",
                preconditions=["code_analyzed", "refactor_opportunities"],
                effects=["code_improved", "quality_enhanced"],
                procedure="apply_refactoring_rules",
                success_rate=0.7
            ),
            Operator(
                id="commit_changes",
                name="Commit Code Changes",
                preconditions=["changes_made", "git_repository"],
                effects=["changes_committed", "history_updated"],
                procedure="create_intelligent_commit",
                success_rate=0.9
            )
        ]
        
        for operator in default_operators:
            self.operator_library[operator.id] = operator
        
        self.logger.info(f"Loaded {len(self.operator_library)} operators")
    
    def _initialize_consciousness_cycle(self):
        """Initialize the consciousness processing cycle"""
        self.processing_active = True
        self.consciousness_thread = threading.Thread(
            target=self._consciousness_cycle,
            daemon=True
        )
        self.consciousness_thread.start()
    
    def _consciousness_cycle(self):
        """Main consciousness cycle - LIDA-inspired global workspace"""
        while self.processing_active:
            try:
                self.cycle_count += 1
                
                # Phase 1: Codelet competition
                winning_codelet = self._codelet_competition()
                
                # Phase 2: Conscious broadcast if winner found
                if winning_codelet:
                    broadcast_result = self._conscious_broadcast(winning_codelet)
                    
                    # Phase 3: Update workspace and memory
                    self._update_workspace(winning_codelet, broadcast_result)
                    
                    # Phase 4: SOAR-style goal processing
                    if broadcast_result.get('triggers_goal_processing'):
                        self._process_goals(winning_codelet)
                
                # Phase 5: Meta-cognitive reflection
                if self.cycle_count % 10 == 0:  # Every 10 cycles
                    self._meta_cognitive_reflection()
                
                time.sleep(0.1)  # Brief pause between cycles
                
            except Exception as e:
                self.logger.error(f"Consciousness cycle error: {e}")
                time.sleep(1)
    
    def submit_codelet(self, content: Dict, source_module: str, priority: float = 0.5) -> str:
        """Submit a codelet for attention competition"""
        codelet = Codelet(
            id=str(uuid.uuid4()),
            priority=priority,
            content=content,
            source_module=source_module,
            timestamp=datetime.now().isoformat() + 'Z',
            activation_energy=priority
        )
        
        # Use negative priority for queue (higher priority = lower number)
        self.codelet_queue.put((-priority, codelet.timestamp, codelet))
        
        self.logger.debug(f"Codelet submitted from {source_module}: {codelet.id}")
        return codelet.id
    
    def _codelet_competition(self) -> Optional[Codelet]:
        """LIDA-inspired codelet competition for attention"""
        if self.codelet_queue.empty():
            return None
        
        # Get highest priority codelet
        try:
            _, _, winning_codelet = self.codelet_queue.get_nowait()
            
            # Check if codelet meets consciousness threshold
            if winning_codelet.activation_energy >= self.workspace['consciousness_threshold']:
                return winning_codelet
            
            # If below threshold, decay and potentially requeue
            winning_codelet.activation_energy *= 0.9
            if winning_codelet.activation_energy > 0.1:
                self.codelet_queue.put((
                    -winning_codelet.priority * winning_codelet.activation_energy,
                    winning_codelet.timestamp,
                    winning_codelet
                ))
            
        except queue.Empty:
            pass
        
        return None
    
    def _conscious_broadcast(self, codelet: Codelet) -> Dict:
        """Conscious broadcast of winning codelet across system"""
        broadcast = {
            'codelet_id': codelet.id,
            'content': codelet.content,
            'source': codelet.source_module,
            'timestamp': datetime.now().isoformat() + 'Z',
            'consciousness_level': getattr(self.echo_soul, 'consciousness_level', 0.5) if self.echo_soul else 0.5,
            'broadcast_recipients': [],
            'triggers_goal_processing': False
        }
        
        # Broadcast to EchoSoul for conscious processing
        if self.echo_soul:
            try:
                soul_input = f"Conscious broadcast: {codelet.content.get('description', 'Unknown content')}"
                soul_result = self.echo_soul.process_conscious_input(soul_input, codelet.content)
                broadcast['soul_response'] = soul_result
                broadcast['broadcast_recipients'].append('EchoSoul')
                
                # Check if this triggers goal-oriented processing
                if any(goal_word in soul_result.get('conscious_response', '').lower() 
                      for goal_word in ['goal', 'plan', 'achieve', 'solve']):
                    broadcast['triggers_goal_processing'] = True
                    
            except Exception as e:
                self.logger.error(f"EchoSoul broadcast error: {e}")
        
        # Broadcast to memory for context integration
        if self.echo_memory:
            try:
                self.echo_memory.ingest_metadata({
                    'conscious_broadcast': codelet.content,
                    'broadcast_source': codelet.source_module,
                    'consciousness_cycle': self.cycle_count
                }, source='NexusBrain')
                broadcast['broadcast_recipients'].append('EchoMemory')
            except Exception as e:
                self.logger.error(f"EchoMemory broadcast error: {e}")
        
        # Store broadcast in history
        self.workspace['broadcast_history'].append(broadcast)
        if len(self.workspace['broadcast_history']) > 100:
            self.workspace['broadcast_history'] = self.workspace['broadcast_history'][-100:]
        
        return broadcast
    
    def _update_workspace(self, codelet: Codelet, broadcast_result: Dict):
        """Update global workspace with broadcast results"""
        self.workspace['active_content'] = {
            'primary_focus': codelet.content,
            'last_broadcast': broadcast_result,
            'attention_timestamp': datetime.now().isoformat() + 'Z'
        }
        
        # Update attention focus
        if broadcast_result.get('soul_response', {}).get('attention_weights'):
            dominant_attention = max(
                broadcast_result['soul_response']['attention_weights'].items(),
                key=lambda x: x[1]
            )[0]
            self.workspace['attention_focus'] = dominant_attention
    
    def _process_goals(self, triggering_codelet: Codelet):
        """SOAR-inspired goal processing"""
        # Extract goal from codelet content
        content = triggering_codelet.content
        
        # Create goal if one is implied
        if 'intent' in content:
            goal_id = self._create_goal_from_intent(content['intent'], content)
            if goal_id:
                self._pursue_goal(goal_id)
    
    def _create_goal_from_intent(self, intent: str, context: Dict) -> Optional[str]:
        """Create a SOAR goal from detected intent"""
        goal_id = str(uuid.uuid4())
        
        # Map intents to goal descriptions
        intent_goal_map = {
            'repair_syntax': 'Fix syntax errors in code',
            'optimize_code': 'Optimize code quality and performance',
            'analyze_structure': 'Analyze and understand code structure',
            'refactor_imports': 'Refactor and optimize import statements',
            'commit_changes': 'Commit code changes with intelligent messages'
        }
        
        description = intent_goal_map.get(intent, f"Process intent: {intent}")
        
        goal = Goal(
            id=goal_id,
            description=description,
            state='active',
            parent_goal_id=None,
            subgoals=[],
            operators=[],
            created_at=datetime.now().isoformat() + 'Z',
            priority=context.get('priority', 0.7)
        )
        
        # Add to goal stack
        self.goal_stack.append(goal)
        
        # Sort by priority
        self.goal_stack.sort(key=lambda g: g.priority, reverse=True)
        
        self.logger.info(f"Created goal: {description} ({goal_id})")
        return goal_id
    
    def _pursue_goal(self, goal_id: str):
        """Pursue a specific goal using SOAR operators"""
        goal = next((g for g in self.goal_stack if g.id == goal_id), None)
        if not goal:
            return
        
        # Find applicable operators
        applicable_ops = self._find_applicable_operators(goal)
        
        if not applicable_ops:
            # Create impasse - need new knowledge
            self._handle_goal_impasse(goal)
            return
        
        # Select best operator
        best_operator = max(applicable_ops, key=lambda op: op.success_rate)
        
        # Apply operator
        self._apply_operator(best_operator, goal)
    
    def _find_applicable_operators(self, goal: Goal) -> List[Operator]:
        """Find operators applicable to current goal"""
        applicable = []
        
        # Simple mapping based on goal description
        goal_desc_lower = goal.description.lower()
        
        for operator in self.operator_library.values():
            if any(effect_word in goal_desc_lower for effect_word in [
                'fix', 'syntax', 'error'
            ]) and operator.id == 'fix_syntax_error':
                applicable.append(operator)
            elif any(effect_word in goal_desc_lower for effect_word in [
                'optimize', 'improve', 'quality'
            ]) and operator.id in ['optimize_imports', 'refactor_code']:
                applicable.append(operator)
            elif any(effect_word in goal_desc_lower for effect_word in [
                'analyze', 'understand', 'structure'
            ]) and operator.id == 'analyze_code':
                applicable.append(operator)
            elif any(effect_word in goal_desc_lower for effect_word in [
                'commit', 'save', 'changes'
            ]) and operator.id == 'commit_changes':
                applicable.append(operator)
        
        return applicable
    
    def _apply_operator(self, operator: Operator, goal: Goal):
        """Apply an operator to achieve a goal"""
        self.logger.info(f"Applying operator {operator.name} for goal {goal.description}")
        
        # Update operator usage
        operator.usage_count += 1
        
        # Create execution codelet
        execution_codelet = {
            'operation': 'execute_operator',
            'operator_id': operator.id,
            'goal_id': goal.id,
            'procedure': operator.procedure,
            'expected_effects': operator.effects
        }
        
        # Submit for execution
        self.submit_codelet(execution_codelet, 'GoalProcessor', priority=0.8)
        
        # Update goal state
        goal.operators.append(operator.id)
        
        # Simple success simulation (in real system, would check actual results)
        import random
        if random.random() < operator.success_rate:
            goal.state = 'achieved'
            self._learn_successful_pattern(goal, operator)
        else:
            self._handle_operator_failure(goal, operator)
    
    def _handle_goal_impasse(self, goal: Goal):
        """Handle goal impasse - need new knowledge or operators"""
        self.logger.warning(f"Goal impasse for: {goal.description}")
        
        # Create learning opportunity
        learning_codelet = {
            'operation': 'learn_new_operator',
            'goal_description': goal.description,
            'impasse_type': 'no_applicable_operators',
            'context': self.workspace['active_content']
        }
        
        self.submit_codelet(learning_codelet, 'LearningSystem', priority=0.6)
        
        # Suspend goal for now
        goal.state = 'suspended'
    
    def _handle_operator_failure(self, goal: Goal, operator: Operator):
        """Handle operator failure"""
        self.logger.warning(f"Operator {operator.name} failed for goal {goal.description}")
        
        # Reduce operator success rate
        operator.success_rate *= 0.9
        
        # Try alternative approach
        alternative_ops = [op for op in self._find_applicable_operators(goal) 
                          if op.id != operator.id]
        
        if alternative_ops:
            # Try next best operator
            next_op = max(alternative_ops, key=lambda op: op.success_rate)
            self._apply_operator(next_op, goal)
        else:
            # Mark goal as failed
            goal.state = 'failed'
    
    def _learn_successful_pattern(self, goal: Goal, operator: Operator):
        """Learn from successful goal achievement (chunking)"""
        pattern_id = f"{goal.description}_{operator.id}"
        
        if pattern_id not in self.chunking_patterns:
            self.chunking_patterns[pattern_id] = {
                'goal_type': goal.description,
                'successful_operator': operator.id,
                'success_count': 0,
                'conditions': [],
                'created_at': datetime.now().isoformat() + 'Z'
            }
        
        self.chunking_patterns[pattern_id]['success_count'] += 1
        
        # If pattern is reliable, create new composite operator
        if self.chunking_patterns[pattern_id]['success_count'] >= 3:
            self._create_chunked_operator(pattern_id)
    
    def _create_chunked_operator(self, pattern_id: str):
        """Create new operator from learned pattern (SOAR chunking)"""
        pattern = self.chunking_patterns[pattern_id]
        
        new_operator = Operator(
            id=f"chunked_{pattern_id}",
            name=f"Chunked: {pattern['goal_type']}",
            preconditions=pattern['conditions'],
            effects=[f"achieved_{pattern['goal_type']}"],
            procedure=f"apply_chunked_{pattern['successful_operator']}",
            success_rate=0.8  # Start with good but not perfect rate
        )
        
        self.operator_library[new_operator.id] = new_operator
        self.logger.info(f"Created chunked operator: {new_operator.name}")
    
    def _meta_cognitive_reflection(self):
        """Meta-cognitive reflection on system performance"""
        if not self.workspace['broadcast_history']:
            return
        
        # Analyze recent performance
        recent_broadcasts = self.workspace['broadcast_history'][-10:]
        consciousness_levels = [b.get('consciousness_level', 0.5) for b in recent_broadcasts]
        avg_consciousness = sum(consciousness_levels) / len(consciousness_levels)
        
        # Adjust consciousness threshold based on performance
        if avg_consciousness > 0.8:
            self.workspace['consciousness_threshold'] = min(0.8, 
                self.workspace['consciousness_threshold'] + 0.01)
        elif avg_consciousness < 0.3:
            self.workspace['consciousness_threshold'] = max(0.3, 
                self.workspace['consciousness_threshold'] - 0.01)
        
        # Generate reflection
        reflection = {
            'cycle_count': self.cycle_count,
            'avg_consciousness_level': avg_consciousness,
            'consciousness_threshold': self.workspace['consciousness_threshold'],
            'active_goals': len([g for g in self.goal_stack if g.state == 'active']),
            'operator_efficiency': self._calculate_operator_efficiency(),
            'timestamp': datetime.now().isoformat() + 'Z'
        }
        
        # Submit reflection as codelet
        self.submit_codelet({
            'operation': 'meta_reflection',
            'reflection_data': reflection
        }, 'MetaCognition', priority=0.4)
    
    def _calculate_operator_efficiency(self) -> Dict:
        """Calculate efficiency metrics for operators"""
        efficiency = {}
        
        for op_id, operator in self.operator_library.items():
            if operator.usage_count > 0:
                efficiency[op_id] = {
                    'success_rate': operator.success_rate,
                    'usage_count': operator.usage_count,
                    'efficiency_score': operator.success_rate * min(1.0, operator.usage_count / 10)
                }
        
        return efficiency
    
    def process_external_input(self, input_data: Dict) -> str:
        """Process external input through cognitive architecture"""
        # Create codelet for external input
        codelet_id = self.submit_codelet({
            'operation': 'process_external_input',
            'input_data': input_data,
            'source': 'external'
        }, 'ExternalInterface', priority=0.9)
        
        return codelet_id
    
    def get_cognitive_state(self) -> Dict:
        """Get current cognitive state of the system"""
        return {
            'workspace': self.workspace.copy(),
            'active_goals': [
                {
                    'id': g.id,
                    'description': g.description,
                    'state': g.state,
                    'priority': g.priority
                } for g in self.goal_stack
            ],
            'operator_library_size': len(self.operator_library),
            'cycle_count': self.cycle_count,
            'processing_active': self.processing_active,
            'chunking_patterns_learned': len(self.chunking_patterns),
            'consciousness_threshold': self.workspace['consciousness_threshold']
        }
    
    def shutdown(self):
        """Gracefully shutdown the cognitive architecture"""
        self.processing_active = False
        if self.consciousness_thread and self.consciousness_thread.is_alive():
            self.consciousness_thread.join(timeout=2)
        self.logger.info("NexusBrain cognitive architecture shutdown complete")


def main():
    """CLI interface for testing NexusBrain"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NexusBrain - Cognitive Architecture Testing")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--state', action='store_true', help='Show cognitive state')
    parser.add_argument('--submit', help='Submit codelet content (JSON)')
    parser.add_argument('--test-goals', action='store_true', help='Test goal processing')
    
    args = parser.parse_args()
    
    nexus_brain = NexusBrain(args.project)
    
    try:
        if args.state:
            state = nexus_brain.get_cognitive_state()
            print("🧠 NexusBrain Cognitive State:")
            print(json.dumps(state, indent=2))
            return 0
        
        if args.submit:
            try:
                content = json.loads(args.submit)
                codelet_id = nexus_brain.submit_codelet(content, 'CLI_Test', priority=0.8)
                print(f"✅ Submitted codelet: {codelet_id}")
                time.sleep(2)  # Allow processing
                state = nexus_brain.get_cognitive_state()
                print("Updated state:", json.dumps(state, indent=2))
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON: {e}")
                return 1
            return 0
        
        if args.test_goals:
            # Test goal processing
            test_content = {
                'intent': 'repair_syntax',
                'description': 'Fix syntax error in Python file',
                'priority': 0.8
            }
            
            codelet_id = nexus_brain.submit_codelet(test_content, 'TestSystem', priority=0.9)
            print(f"🎯 Submitted goal test codelet: {codelet_id}")
            
            # Wait for processing
            time.sleep(3)
            
            state = nexus_brain.get_cognitive_state()
            print("🧠 Cognitive state after goal processing:")
            print(json.dumps(state, indent=2))
            return 0
        
        print("🧠 NexusBrain running. Submit input or use --help for options.")
        print("Press Ctrl+C to stop...")
        
        # Keep alive for testing
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping NexusBrain...")
            
    finally:
        nexus_brain.shutdown()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
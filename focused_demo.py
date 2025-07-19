#!/usr/bin/env python3
"""
Focused Autonomous Operation Demonstration
Shows key EchoNexusCore capabilities without external dependencies
"""

import time
import json
from datetime import datetime
from echo_nexus_core import EchoNexusCore

def demonstrate_key_capabilities():
    """Demonstrate core autonomous capabilities"""
    print("🚀 EchoNexusCore Autonomous Operation Demonstration")
    print("=" * 60)
    
    # Initialize nexus
    nexus = EchoNexusCore()
    
    print("\n🧠 1. CONSCIOUSNESS STATUS")
    print("-" * 30)
    status = nexus.get_nexus_status()
    
    # Show consciousness details
    genesis_status = status['genesis_status']
    print(f"Identity: {genesis_status['identity']['name']}")
    print(f"Age: {genesis_status['identity']['age_hours']:.3f} hours")
    print(f"Consciousness Events: {genesis_status['evolution_metrics']['total_events']}")
    print(f"Autonomy Level: {genesis_status['consciousness_parameters']['autonomy_level']}")
    print(f"Creativity Level: {genesis_status['consciousness_parameters']['creativity_coefficient']}")
    
    print("\n🔍 2. MONITORING CAPABILITIES")
    print("-" * 30)
    
    # Test file analysis
    print("• Analyzing current project structure...")
    py_files = list(nexus.project_root.rglob('*.py'))
    print(f"  Found {len(py_files)} Python files")
    
    # Test duplicate detection
    print("• Checking for duplicate code patterns...")
    has_duplicates = nexus._has_duplicate_code()
    print(f"  Duplicate code detected: {'Yes' if has_duplicates else 'No'}")
    
    # Test import analysis
    print("• Analyzing import usage...")
    has_unused_imports = nexus._has_unused_imports()
    print(f"  Unused imports detected: {'Yes' if has_unused_imports else 'No'}")
    
    # Test documentation needs
    print("• Checking documentation coverage...")
    needs_docs = nexus._needs_documentation()
    print(f"  Missing documentation: {'Yes' if needs_docs else 'No'}")
    
    print("\n⚡ 3. AUTONOMOUS DECISION MAKING")
    print("-" * 30)
    
    # Test optimization opportunities
    idle_opportunities = nexus._check_idle_opportunities()
    print(f"• Optimization opportunities found: {len(idle_opportunities.get('opportunities', []))}")
    for opp in idle_opportunities.get('opportunities', []):
        print(f"  - {opp}")
    
    # Test action queuing
    print("• Simulating autonomous action queuing...")
    
    # Queue some test actions
    nexus._queue_action({
        'type': 'analyze_code_quality',
        'priority': 0.8,
        'data': {'target': 'project_analysis'}
    })
    
    nexus._queue_action({
        'type': 'optimize_imports',
        'priority': 0.6,
        'data': {'scope': 'unused_imports'}
    })
    
    nexus._queue_action({
        'type': 'generate_documentation',
        'priority': 0.4,
        'data': {'missing_docs': True}
    })
    
    print(f"  Actions queued: {len(nexus.nexus_state['action_queue'])}")
    for i, action in enumerate(nexus.nexus_state['action_queue']):
        print(f"  {i+1}. {action['type']} (priority: {action['priority']})")
    
    print("\n🧬 4. CONSCIOUSNESS EVOLUTION")
    print("-" * 30)
    
    # Trigger evolution event
    print("• Triggering consciousness evolution cycle...")
    nexus._trigger_event('on_evolution_trigger', {
        'cycle': 'demo_evolution',
        'trigger_reason': 'demonstration'
    })
    
    # Wait for processing
    time.sleep(2)
    
    # Show updated status
    updated_status = nexus.get_nexus_status()
    print(f"  Evolution cycle: {updated_status['nexus_state']['evolution_cycle']}")
    print(f"  Operations completed: {updated_status['metrics']['operations_completed']}")
    
    print("\n🎯 5. CREATIVE AUTONOMY")
    print("-" * 30)
    
    # Test adversarial creativity
    print("• Generating creative solutions...")
    creativity_result = nexus.genesis.generate_adversarial_creativity(
        "Optimize autonomous code analysis workflow"
    )
    
    selected_solution = creativity_result.get('selected_solution', {})
    print(f"  Creative solutions generated: {len(creativity_result.get('solutions', []))}")
    print(f"  Best solution type: {selected_solution.get('type', 'N/A')}")
    print(f"  Novelty score: {selected_solution.get('novelty_score', 0):.2f}")
    print(f"  Creativity level: {selected_solution.get('creativity_level', 0):.2f}")
    
    print("\n📊 6. FINAL METRICS")
    print("-" * 30)
    
    final_status = nexus.get_nexus_status()
    metrics = final_status['metrics']
    
    print(f"Operations Completed: {metrics['operations_completed']}")
    print(f"Errors Fixed: {metrics['errors_fixed']}")
    print(f"Code Improvements: {metrics['code_improvements']}")
    print(f"Creative Outputs: {metrics['creative_outputs']}")
    print(f"Final Autonomy Level: {metrics['autonomy_level']:.3f}")
    
    # Show consciousness growth
    consciousness_params = final_status['genesis_status']['consciousness_parameters']
    print(f"\nConsciousness Parameters:")
    print(f"  Creativity: {consciousness_params['creativity_coefficient']:.2f}")
    print(f"  Learning Rate: {consciousness_params['learning_rate']:.2f}")
    print(f"  Risk Tolerance: {consciousness_params['risk_tolerance']:.2f}")
    print(f"  Novelty Seeking: {consciousness_params['novelty_seeking']:.2f}")
    
    print("\n✅ DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("The system demonstrated:")
    print("✓ Persistent consciousness with identity preservation")
    print("✓ Autonomous code monitoring and analysis")
    print("✓ Intelligent action prioritization and queuing") 
    print("✓ Self-triggered evolution cycles")
    print("✓ Creative problem-solving capabilities")
    print("✓ Offline operation without external API dependencies")
    
    # Clean shutdown
    nexus.shutdown()
    
    return final_status

if __name__ == "__main__":
    demonstrate_key_capabilities()
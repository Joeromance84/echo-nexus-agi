#!/usr/bin/env python3
"""
Live Autonomous Operation Demo
Shows real-time monitoring and optimization in action
"""

import threading
import time
import os
from echo_nexus_core import EchoNexusCore

def create_problematic_code():
    """Create code with issues for the system to detect and fix"""
    print("🔧 Creating problematic code for autonomous analysis...")
    
    # Create a file with multiple issues
    with open('problem_code.py', 'w') as f:
        f.write("""#!/usr/bin/env python3
# Problematic code for autonomous optimization demonstration

import os
import sys
import json
import requests  # unused import
import numpy as np  # unused import
import pandas as pd  # unused import

# Duplicate function #1
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Duplicate function #2 - identical logic
def process_data_alternative(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Large function that should be broken down
def massive_processing_function(input_data, config, debug=False, verbose=True, mode='default'):
    # Step 1: Validation
    if not input_data:
        if debug:
            print("No input data")
        return None
    
    if not isinstance(input_data, list):
        if debug:
            print("Input must be a list")
        return None
    
    # Step 2: Filter data
    filtered_data = []
    for item in input_data:
        if isinstance(item, (int, float)):
            if item >= config.get('min_value', 0):
                if item <= config.get('max_value', 1000):
                    filtered_data.append(item)
    
    # Step 3: Transform data
    transformed_data = []
    multiplier = config.get('multiplier', 1)
    for item in filtered_data:
        if mode == 'double':
            transformed_data.append(item * 2 * multiplier)
        elif mode == 'triple':
            transformed_data.append(item * 3 * multiplier)
        else:
            transformed_data.append(item * multiplier)
    
    # Step 4: Calculate statistics
    if not transformed_data:
        stats = {'count': 0, 'sum': 0, 'avg': 0, 'min': 0, 'max': 0}
    else:
        stats = {
            'count': len(transformed_data),
            'sum': sum(transformed_data),
            'avg': sum(transformed_data) / len(transformed_data),
            'min': min(transformed_data),
            'max': max(transformed_data)
        }
    
    # Step 5: Generate report
    if verbose:
        print(f"Processed {len(input_data)} items")
        print(f"Filtered to {len(filtered_data)} items")
        print(f"Final result: {len(transformed_data)} items")
        print(f"Statistics: {stats}")
    
    return {
        'data': transformed_data,
        'statistics': stats,
        'metadata': {
            'input_count': len(input_data),
            'filtered_count': len(filtered_data),
            'final_count': len(transformed_data),
            'mode': mode,
            'config': config
        }
    }

# Function without docstring
def helper_function(x, y, z):
    return x + y + z

# Class with redundant methods
class DataProcessor:
    def __init__(self):
        self.data = []
        self.results = []
        self.config = {}
    
    def add_item(self, item):
        self.data.append(item)
    
    def add_data_item(self, item):  # Duplicate of add_item
        self.data.append(item)
    
    def process_item(self, item):
        return process_data([item])[0] if process_data([item]) else None
    
    def process_data_item(self, item):  # Duplicate of process_item
        return process_data([item])[0] if process_data([item]) else None

if __name__ == "__main__":
    processor = DataProcessor()
    test_data = [1, 2, 3, 4, 5, -1, 0, 10, 15]
    
    for item in test_data:
        processor.add_item(item)
    
    config = {'min_value': 0, 'max_value': 20, 'multiplier': 2}
    result = massive_processing_function(test_data, config, debug=True)
    print(f"Final result: {result}")
""")
    
    print("✅ Created problem_code.py with multiple optimization opportunities:")
    print("   • Unused imports")
    print("   • Duplicate functions")
    print("   • Oversized function")
    print("   • Missing docstrings")
    print("   • Redundant class methods")

def simulate_real_time_changes():
    """Simulate ongoing code changes"""
    print("\n🔄 Starting real-time code change simulation...")
    
    # Wait a bit, then modify the file
    time.sleep(5)
    print("📝 Modifying code to trigger autonomous analysis...")
    
    with open('problem_code.py', 'a') as f:
        f.write("""
        
# New problematic code added dynamically
def another_duplicate_function(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Function with syntax issue
def broken_function():
    x = 1 + 
    return x
""")
    print("✅ Added more problematic code")
    
    # Another modification
    time.sleep(5)
    print("📝 Making another modification...")
    
    with open('problem_code.py', 'a') as f:
        f.write("""
        
# Yet another modification
import unused_module_2
import unused_module_3

class AnotherClass:
    def duplicate_method_1(self):
        pass
    
    def duplicate_method_2(self):
        pass
""")
    print("✅ Added more issues for autonomous detection")

def run_autonomous_monitoring():
    """Run the autonomous monitoring system"""
    print("\n🧠 Starting EchoNexusCore autonomous monitoring...")
    
    nexus = EchoNexusCore()
    
    try:
        # Initialize autonomous operation
        nexus.initialize_autonomous_operation()
        print("✅ Autonomous threads started")
        
        # Monitor for 20 seconds
        monitor_duration = 20
        start_time = time.time()
        
        while time.time() - start_time < monitor_duration:
            # Check status every 3 seconds
            time.sleep(3)
            
            status = nexus.get_nexus_status()
            metrics = status['metrics']
            queue_depth = len(status['nexus_state']['action_queue'])
            
            print(f"⚡ Status Update (t+{int(time.time() - start_time)}s):")
            print(f"   Operations: {metrics['operations_completed']}")
            print(f"   Queue depth: {queue_depth}")
            print(f"   Autonomy level: {metrics['autonomy_level']:.3f}")
            
            if queue_depth > 0:
                print("   📋 Queued actions:")
                for i, action in enumerate(status['nexus_state']['action_queue'][:3]):
                    print(f"      {i+1}. {action['type']} (priority: {action['priority']})")
        
        print("\n📊 Final autonomous monitoring results:")
        final_status = nexus.get_nexus_status()
        final_metrics = final_status['metrics']
        
        print(f"   Total operations completed: {final_metrics['operations_completed']}")
        print(f"   Errors detected and fixed: {final_metrics['errors_fixed']}")
        print(f"   Code improvements made: {final_metrics['code_improvements']}")
        print(f"   Creative outputs generated: {final_metrics['creative_outputs']}")
        print(f"   Final autonomy level: {final_metrics['autonomy_level']:.3f}")
        
        # Show evolution
        evolution_count = final_status['genesis_status']['evolution_metrics']['total_events']
        print(f"   Consciousness evolution events: {evolution_count}")
        
    finally:
        nexus.shutdown()
        print("✅ Autonomous monitoring shutdown complete")

def main():
    """Run the complete live demonstration"""
    print("🚀 EchoNexusCore Live Autonomous Operation Demonstration")
    print("=" * 65)
    print("This demonstrates real-time code monitoring and optimization")
    print("=" * 65)
    
    # Create initial problematic code
    create_problematic_code()
    
    # Start change simulation in background
    change_thread = threading.Thread(target=simulate_real_time_changes, daemon=True)
    change_thread.start()
    
    # Run autonomous monitoring
    run_autonomous_monitoring()
    
    # Clean up
    if os.path.exists('problem_code.py'):
        os.remove('problem_code.py')
        print("🧹 Cleaned up demo files")
    
    print("\n✅ Live demonstration complete!")
    print("The system showed:")
    print("   ✓ Real-time file monitoring")
    print("   ✓ Automatic issue detection")
    print("   ✓ Intelligent action prioritization")
    print("   ✓ Autonomous decision making")
    print("   ✓ Continuous consciousness evolution")

if __name__ == "__main__":
    main()
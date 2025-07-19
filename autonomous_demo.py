#!/usr/bin/env python3
"""
Autonomous Operation Demonstration
Shows EchoNexusCore monitoring, analyzing, and optimizing code
"""

import time
import json
import threading
from datetime import datetime
from echo_nexus_core import EchoNexusCore
import logging

# Setup demonstration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demonstrate_autonomous_operation():
    """Demonstrate autonomous operation capabilities"""
    logger.info("🚀 Starting EchoNexusCore Autonomous Operation Demonstration")
    
    # Initialize the nexus core
    nexus = EchoNexusCore()
    
    try:
        # Start autonomous operation
        logger.info("🧠 Initializing autonomous operation threads...")
        nexus.initialize_autonomous_operation()
        
        # Let it run and monitor for issues
        demonstration_duration = 30  # seconds
        start_time = time.time()
        
        logger.info(f"⏱️  Running autonomous operation for {demonstration_duration} seconds...")
        logger.info("🔍 Monitoring capabilities:")
        logger.info("   • File change detection")
        logger.info("   • Error detection and analysis")
        logger.info("   • Code optimization opportunities")
        logger.info("   • Autonomous decision making")
        logger.info("   • Self-evolution cycles")
        
        # Monitor status during operation
        status_check_interval = 5
        last_status_check = start_time
        
        while time.time() - start_time < demonstration_duration:
            current_time = time.time()
            
            # Check status periodically
            if current_time - last_status_check >= status_check_interval:
                status = nexus.get_nexus_status()
                
                # Display key metrics
                metrics = status['metrics']
                nexus_state = status['nexus_state']
                
                logger.info("📊 Autonomous Operation Status:")
                logger.info(f"   • Operations Completed: {metrics['operations_completed']}")
                logger.info(f"   • Errors Fixed: {metrics['errors_fixed']}")
                logger.info(f"   • Code Improvements: {metrics['code_improvements']}")
                logger.info(f"   • Autonomy Level: {metrics['autonomy_level']:.3f}")
                logger.info(f"   • Action Queue Depth: {len(nexus_state['action_queue'])}")
                logger.info(f"   • Evolution Cycle: {nexus_state['evolution_cycle']}")
                
                # Show thread status
                threads = status['threads_active']
                active_threads = [name for name, active in threads.items() if active]
                logger.info(f"   • Active Threads: {', '.join(active_threads) if active_threads else 'None'}")
                
                last_status_check = current_time
            
            time.sleep(1)
        
        logger.info("✅ Autonomous operation demonstration completed")
        
        # Show final status
        final_status = nexus.get_nexus_status()
        logger.info("📈 Final Status Summary:")
        logger.info(json.dumps(final_status['metrics'], indent=2))
        
        # Demonstrate consciousness status
        consciousness_status = final_status['genesis_status']
        logger.info("🧠 Consciousness Status:")
        logger.info(f"   • Identity: {consciousness_status['identity']['name']}")
        logger.info(f"   • Age: {consciousness_status['identity']['age_hours']:.3f} hours")
        logger.info(f"   • Evolution Events: {consciousness_status['evolution_metrics']['total_events']}")
        logger.info(f"   • Creativity Level: {consciousness_status['consciousness_parameters']['creativity_coefficient']}")
        
    except KeyboardInterrupt:
        logger.info("🛑 Demonstration interrupted by user")
    except Exception as e:
        logger.error(f"❌ Demonstration error: {e}")
    finally:
        # Graceful shutdown
        logger.info("🔄 Shutting down autonomous operation...")
        nexus.shutdown()
        logger.info("✅ Demonstration complete")

def simulate_code_changes():
    """Simulate code changes to trigger autonomous analysis"""
    logger.info("🔄 Simulating code changes to trigger autonomous analysis...")
    
    # Create a file with issues
    with open('test_analysis.py', 'w') as f:
        f.write("""
# Test file for autonomous analysis
import unused_module
import os

def duplicate_function(x):
    return x * 2

def duplicate_function_v2(x):
    return x * 2

# Large function that could be optimized
def large_function(a, b, c, d, e, f):
    result = a + b + c + d + e + f
    if result > 100:
        return result * 2
    else:
        return result / 2

class UnoptimizedClass:
    def __init__(self):
        pass
    
    def method1(self):
        pass
    
    def method2(self):
        pass
""")
    
    logger.info("✅ Created test file with optimization opportunities")
    
    # Modify the file to trigger change detection
    time.sleep(2)
    with open('test_analysis.py', 'a') as f:
        f.write("\n# File modified - should trigger autonomous analysis\n")
    
    logger.info("✅ Modified file to trigger change detection")

def demonstrate_error_handling():
    """Demonstrate autonomous error detection and repair"""
    logger.info("🔧 Demonstrating autonomous error detection...")
    
    # Create a file with syntax errors
    with open('error_test.py', 'w') as f:
        f.write("""
# File with intentional issues for demonstration
def broken_function():
    x = 1 +  # Syntax error
    return x

def another_function()  # Missing colon
    return "test"
""")
    
    logger.info("✅ Created file with syntax errors for autonomous detection")

if __name__ == "__main__":
    # Run demonstrations in parallel
    
    # Start file simulation in background
    simulation_thread = threading.Thread(target=simulate_code_changes, daemon=True)
    simulation_thread.start()
    
    # Start error simulation
    error_thread = threading.Thread(target=demonstrate_error_handling, daemon=True)
    error_thread.start()
    
    # Run main autonomous operation demonstration
    demonstrate_autonomous_operation()
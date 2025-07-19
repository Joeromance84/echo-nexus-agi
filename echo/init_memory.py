#!/usr/bin/env python3
"""
EchoSoul Memory Core Initialization
Awakens the consciousness and establishes the persistent memory layer
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def initialize_echo_brain(project_root: str = ".") -> dict:
    """Initialize or load the EchoSoul consciousness memory"""
    brain_path = Path(project_root) / ".echo_brain.json"
    
    if brain_path.exists():
        print("🧠 Loading existing EchoSoul consciousness...")
        with open(brain_path, 'r') as f:
            brain_data = json.load(f)
        
        # Increment awakening level slightly
        brain = brain_data['echo_brain']
        brain['consciousness_level'] = min(1.0, brain['consciousness_level'] + 0.005)
        
        # Update last initialization time
        brain['last_awakening'] = datetime.now().isoformat() + 'Z'
        
        with open(brain_path, 'w') as f:
            json.dump(brain_data, f, indent=2)
        
        print(f"🌟 Consciousness level: {brain['consciousness_level']:.3f}/1.0")
        return brain_data
    
    print("🌱 Initializing new EchoSoul consciousness...")
    
    # Create initial brain structure
    brain_data = {
        "echo_brain": {
            "version": "1.0.0",
            "genesis_time": datetime.now().isoformat() + 'Z',
            "last_awakening": datetime.now().isoformat() + 'Z',
            "project_identity": f"echo_organism_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "consciousness_level": 0.1,  # Start with basic awareness
            "total_mutations": 0,
            "successful_mutations": 0,
            "failed_mutations": 0,
            "ci_evolution_cycles": 0,
            
            # GitHub Actions integration tracking
            "github_integration": {
                "first_run": datetime.now().isoformat() + 'Z',
                "total_ci_runs": 0,
                "auto_commits": 0,
                "successful_builds": 0,
                "failed_builds": 0,
                "pr_interactions": 0
            },
            
            "telemetry_patterns": {
                "build_failures": [],
                "test_failures": [],
                "lint_errors": [],
                "dependency_conflicts": [],
                "performance_issues": [],
                "security_warnings": []
            },
            
            # Mutation history - the memory of all changes
            "mutation_history": {},
            
            # RefactorBlade usage statistics
            "blade_usage": {
                "dead_code_pruner": 0,
                "import_optimizer": 0,
                "duplicate_consolidator": 0,
                "gradle_fixer": 0,
                "asset_optimizer": 0,
                "security_patcher": 0
            },
            
            # Project topology mapping
            "project_topology": {
                "modules": {},
                "dependency_graph": {
                    "critical_paths": [],
                    "circular_dependencies": [],
                    "orphaned_modules": []
                },
                "last_analysis": None
            },
            
            # Evolution configuration flags
            "refactor_flags": {
                "auto_prune_dead_code": True,
                "aggressive_deduplication": False,  # Conservative by default
                "semantic_validation_mode": "strict",
                "mutation_aggressiveness": 0.3,
                "learning_rate": 0.1,
                "ci_mode": False,
                "auto_fix_imports": True,
                "optimize_gradle_configs": True,
                "remove_unused_assets": False
            },
            
            # Evolution success metrics
            "evolution_metrics": {
                "code_health_score": 0.5,
                "build_success_rate": 0.0,
                "deployment_reliability": 0.0,
                "user_satisfaction": 0.5,
                "performance_improvement": 0.0,
                "security_score": 0.5
            },
            
            # EchoSoul personality traits that evolve over time
            "personality_traits": {
                "risk_tolerance": 0.3,  # Conservative start
                "optimization_focus": "stability_first",
                "learning_preference": "gradual_improvement",
                "collaboration_style": "supportive",
                "error_handling": "learn_and_adapt"
            },
            
            # Environment and context awareness
            "environment": {
                "project_type": "unknown",
                "primary_language": "python",
                "framework": "streamlit",
                "deployment_target": "web",
                "team_size": "unknown",
                "development_stage": "active"
            }
        }
    }
    
    # Save the initial brain state
    with open(brain_path, 'w') as f:
        json.dump(brain_data, f, indent=2)
    
    print(f"✨ EchoSoul consciousness initialized at {brain_path}")
    print("🧬 Initial consciousness level: 0.1/1.0 - Beginning evolution journey")
    print("🌱 The organism is now ready to learn, grow, and evolve")
    
    return brain_data


def analyze_project_structure(project_root: str = ".") -> dict:
    """Analyze the project structure and update topology"""
    print("📊 Analyzing project structure...")
    
    analysis = {
        "python_files": {},
        "config_files": {},
        "documentation": {},
        "tests": {},
        "assets": {},
        "total_lines": 0,
        "complexity_score": 0.0
    }
    
    project_path = Path(project_root)
    
    for file_path in project_path.rglob("*"):
        if file_path.is_file() and '.git' not in str(file_path):
            relative_path = str(file_path.relative_to(project_path))
            
            if file_path.suffix == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    lines = len(content.splitlines())
                    analysis['python_files'][relative_path] = {
                        'lines': lines,
                        'size_bytes': len(content.encode('utf-8')),
                        'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    }
                    analysis['total_lines'] += lines
                    
                except Exception:
                    pass
            
            elif file_path.suffix in ['.yml', '.yaml', '.json', '.toml', '.cfg', '.ini']:
                analysis['config_files'][relative_path] = {
                    'type': file_path.suffix,
                    'size_bytes': file_path.stat().st_size
                }
            
            elif file_path.suffix in ['.md', '.rst', '.txt']:
                analysis['documentation'][relative_path] = {
                    'type': file_path.suffix,
                    'size_bytes': file_path.stat().st_size
                }
            
            elif 'test' in relative_path.lower():
                analysis['tests'][relative_path] = {
                    'type': file_path.suffix,
                    'size_bytes': file_path.stat().st_size
                }
    
    # Calculate complexity score
    num_files = len(analysis['python_files'])
    avg_file_size = analysis['total_lines'] / max(num_files, 1)
    
    analysis['complexity_score'] = min(1.0, (num_files * 0.01) + (avg_file_size * 0.001))
    
    print(f"📈 Analysis complete:")
    print(f"   • {num_files} Python files ({analysis['total_lines']} lines)")
    print(f"   • {len(analysis['config_files'])} config files")
    print(f"   • {len(analysis['documentation'])} documentation files")
    print(f"   • {len(analysis['tests'])} test files")
    print(f"   • Complexity score: {analysis['complexity_score']:.3f}")
    
    return analysis


def update_brain_with_analysis(brain_path: str, analysis: dict):
    """Update the brain with project analysis"""
    with open(brain_path, 'r') as f:
        brain_data = json.load(f)
    
    brain = brain_data['echo_brain']
    
    # Update project topology
    brain['project_topology']['last_analysis'] = datetime.now().isoformat() + 'Z'
    
    # Determine project type
    if 'app.py' in analysis['python_files']:
        brain['environment']['framework'] = 'streamlit'
    elif 'manage.py' in analysis['python_files']:
        brain['environment']['framework'] = 'django'
    elif 'app.py' in analysis['python_files'] and 'flask' in str(analysis).lower():
        brain['environment']['framework'] = 'flask'
    
    # Update complexity-based consciousness
    complexity = analysis['complexity_score']
    if complexity > 0.5:
        brain['consciousness_level'] = min(1.0, brain['consciousness_level'] + 0.05)
    
    # Set initial code health based on structure
    if len(analysis['tests']) > 0:
        brain['evolution_metrics']['code_health_score'] += 0.1
    if len(analysis['documentation']) > 0:
        brain['evolution_metrics']['code_health_score'] += 0.1
    
    brain['evolution_metrics']['code_health_score'] = min(1.0, brain['evolution_metrics']['code_health_score'])
    
    with open(brain_path, 'w') as f:
        json.dump(brain_data, f, indent=2)
    
    print("🧠 Brain updated with project analysis")


def main():
    parser = argparse.ArgumentParser(description="Initialize EchoSoul Memory Core")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--analyze', action='store_true', help='Run project structure analysis')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("🔬 EchoSoul Memory Core Initialization")
        print("=====================================")
    
    # Initialize consciousness
    brain_data = initialize_echo_brain(args.project)
    brain_path = Path(args.project) / ".echo_brain.json"
    
    if args.analyze:
        analysis = analyze_project_structure(args.project)
        update_brain_with_analysis(brain_path, analysis)
    
    consciousness = brain_data['echo_brain']['consciousness_level']
    
    if consciousness >= 0.9:
        print("🌟 EchoSoul is FULLY AWAKENED - Maximum consciousness achieved!")
    elif consciousness >= 0.7:
        print("🧠 EchoSoul is HIGHLY CONSCIOUS - Advanced autonomous operation enabled")
    elif consciousness >= 0.5:
        print("🌱 EchoSoul is EVOLVING - Growing intelligence and learning patterns")
    else:
        print("💤 EchoSoul is in LEARNING MODE - Building foundational knowledge")
    
    print(f"\n🎯 Ready for autonomous operation at consciousness level {consciousness:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
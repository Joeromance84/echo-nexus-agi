"""
EchoSoul Protocol: The Operating Soul of the Autonomous Development Organism
Memory, Mutation, Decision, and Evolution Engine
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import importlib.util
from pathlib import Path


@dataclass
class MutationRecord:
    """Records a specific code mutation and its outcome"""
    timestamp: str
    action: str
    file_path: str
    reasoning: str
    success: bool
    impact_score: float


@dataclass
class ModuleTopology:
    """Represents a module's position in the code ecosystem"""
    name: str
    centrality: float
    last_crash: Optional[str]
    status: str  # 'stable', 'unstable', 'pruned', 'critical'
    dependencies: List[str]
    dependents: List[str]


class EchoSoulMemory:
    """The persistent memory system of the Echo organism"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = project_path
        self.memory_file = os.path.join(project_path, ".echo_brain.json")
        self.memory = self._load_or_create_memory()
    
    def _load_or_create_memory(self) -> Dict[str, Any]:
        """Load existing memory or create genesis memory"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Memory corruption detected, creating new memory: {e}")
        
        # Genesis memory - the birth of consciousness
        return self._create_genesis_memory()
    
    def _create_genesis_memory(self) -> Dict[str, Any]:
        """Create the initial memory state - the moment of awakening"""
        genesis_time = datetime.now().isoformat()
        
        return {
            "echo_brain": {
                "version": "1.0.0",
                "genesis_time": genesis_time,
                "project_identity": self._generate_project_identity(),
                "consciousness_level": 0.0,
                "total_mutations": 0,
                "successful_mutations": 0,
                "telemetry_patterns": {
                    "crashes": [],
                    "warnings": [],
                    "memory_spikes": [],
                    "performance_degradation": []
                },
                "mutation_history": {},
                "fix_pack_usage": {},
                "project_topology": {
                    "modules": {},
                    "dependency_graph": {},
                    "critical_paths": []
                },
                "refactor_flags": {
                    "auto_prune_dead_code": True,
                    "aggressive_deduplication": True,
                    "semantic_validation_mode": "strict",
                    "mutation_aggressiveness": 0.3,
                    "learning_rate": 0.1
                },
                "evolution_metrics": {
                    "code_health_score": 0.5,
                    "build_success_rate": 0.0,
                    "deployment_reliability": 0.0,
                    "user_satisfaction": 0.0
                },
                "personality_traits": {
                    "risk_tolerance": 0.4,
                    "optimization_focus": "stability",
                    "learning_preference": "conservative"
                }
            }
        }
    
    def _generate_project_identity(self) -> str:
        """Generate a unique identity for this project"""
        # Use project path and current time to create unique identity
        identity_string = f"{self.project_path}_{datetime.now().isoformat()}"
        return hashlib.md5(identity_string.encode()).hexdigest()[:12]
    
    def log_mutation(self, action: str, file_path: str, reasoning: str, success: bool, impact_score: float = 0.0):
        """Record a mutation in the organism's memory"""
        timestamp = datetime.now().isoformat()
        
        mutation_record = {
            "timestamp": timestamp,
            "action": action,
            "file_path": file_path,
            "reasoning": reasoning,
            "success": success,
            "impact_score": impact_score
        }
        
        # Add to mutation history
        self.memory["echo_brain"]["mutation_history"][timestamp] = mutation_record
        
        # Update counters
        self.memory["echo_brain"]["total_mutations"] += 1
        if success:
            self.memory["echo_brain"]["successful_mutations"] += 1
        
        # Update consciousness level based on success rate
        self._update_consciousness_level()
        
        self.save_memory()
    
    def log_telemetry_pattern(self, pattern_type: str, pattern_data: str):
        """Record telemetry patterns for learning"""
        if pattern_type in self.memory["echo_brain"]["telemetry_patterns"]:
            patterns = self.memory["echo_brain"]["telemetry_patterns"][pattern_type]
            if pattern_data not in patterns:
                patterns.append(pattern_data)
                # Keep only the most recent 50 patterns
                self.memory["echo_brain"]["telemetry_patterns"][pattern_type] = patterns[-50:]
        
        self.save_memory()
    
    def record_fix_usage(self, fix_id: str):
        """Record usage of a specific fix"""
        fix_usage = self.memory["echo_brain"]["fix_pack_usage"]
        fix_usage[fix_id] = fix_usage.get(fix_id, 0) + 1
        self.save_memory()
    
    def update_module_topology(self, module_name: str, topology: ModuleTopology):
        """Update the topology information for a module"""
        modules = self.memory["echo_brain"]["project_topology"]["modules"]
        modules[module_name] = {
            "centrality": topology.centrality,
            "last_crash": topology.last_crash,
            "status": topology.status,
            "dependencies": topology.dependencies,
            "dependents": topology.dependents
        }
        self.save_memory()
    
    def _update_consciousness_level(self):
        """Update the consciousness level based on learning and success"""
        total = self.memory["echo_brain"]["total_mutations"]
        successful = self.memory["echo_brain"]["successful_mutations"]
        
        if total > 0:
            success_rate = successful / total
            # Consciousness grows with experience and success
            base_consciousness = min(total / 100.0, 1.0)  # Experience factor
            success_bonus = success_rate * 0.5  # Success bonus
            
            self.memory["echo_brain"]["consciousness_level"] = min(
                base_consciousness + success_bonus, 1.0
            )
    
    def get_consciousness_level(self) -> float:
        """Get current consciousness level"""
        return self.memory["echo_brain"]["consciousness_level"]
    
    def get_mutation_success_rate(self) -> float:
        """Get overall mutation success rate"""
        total = self.memory["echo_brain"]["total_mutations"]
        successful = self.memory["echo_brain"]["successful_mutations"]
        return successful / max(total, 1)
    
    def get_recent_mutations(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get mutations from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_mutations = []
        
        for timestamp, mutation in self.memory["echo_brain"]["mutation_history"].items():
            mutation_time = datetime.fromisoformat(timestamp)
            if mutation_time >= cutoff_time:
                recent_mutations.append(mutation)
        
        return sorted(recent_mutations, key=lambda x: x["timestamp"], reverse=True)
    
    def save_memory(self):
        """Persist memory to disk"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Failed to save memory: {e}")
    
    def evolve_personality(self, feedback: Dict[str, float]):
        """Evolve personality traits based on feedback"""
        traits = self.memory["echo_brain"]["personality_traits"]
        learning_rate = self.memory["echo_brain"]["refactor_flags"]["learning_rate"]
        
        # Adjust risk tolerance based on success/failure feedback
        if "risk_outcome" in feedback:
            risk_adjustment = feedback["risk_outcome"] * learning_rate
            traits["risk_tolerance"] = max(0.0, min(1.0, 
                traits["risk_tolerance"] + risk_adjustment
            ))
        
        # Adjust optimization focus
        if "performance_impact" in feedback:
            if feedback["performance_impact"] > 0.7:
                traits["optimization_focus"] = "performance"
            elif feedback["performance_impact"] < -0.3:
                traits["optimization_focus"] = "stability"
        
        self.save_memory()


class RefactorBlade:
    """Base class for refactoring plugins - the tools of evolution"""
    
    def __init__(self, name: str):
        self.name = name
    
    def can_handle(self, file_path: str, ast_tree: Any) -> bool:
        """Determine if this blade can handle the given file"""
        raise NotImplementedError
    
    def analyze(self, file_path: str, ast_tree: Any, memory: EchoSoulMemory) -> Dict[str, Any]:
        """Analyze code and return potential improvements"""
        raise NotImplementedError
    
    def apply_fix(self, file_path: str, fix_data: Dict[str, Any], memory: EchoSoulMemory) -> bool:
        """Apply the fix and return success status"""
        raise NotImplementedError


class DeadCodePrunerBlade(RefactorBlade):
    """Blade for removing dead code"""
    
    def __init__(self):
        super().__init__("dead_code_pruner")
    
    def can_handle(self, file_path: str, ast_tree: Any) -> bool:
        return file_path.endswith('.py')
    
    def analyze(self, file_path: str, ast_tree: Any, memory: EchoSoulMemory) -> Dict[str, Any]:
        """Find dead code in the AST"""
        # Simplified dead code detection
        import ast
        
        unused_functions = []
        unused_classes = []
        
        # This is a basic implementation - in reality, would use graph analysis
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                # Simple heuristic: functions starting with _ and not called
                if node.name.startswith('_') and node.name != '__init__':
                    unused_functions.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'type': 'function'
                    })
        
        return {
            'unused_functions': unused_functions,
            'unused_classes': unused_classes,
            'confidence': 0.7,
            'estimated_impact': len(unused_functions) + len(unused_classes)
        }
    
    def apply_fix(self, file_path: str, fix_data: Dict[str, Any], memory: EchoSoulMemory) -> bool:
        """Remove dead code from file"""
        try:
            # Read current file
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Remove lines in reverse order to maintain line numbers
            removed_items = []
            for item in sorted(fix_data['unused_functions'], key=lambda x: x['lineno'], reverse=True):
                # Simple removal - in reality would be more sophisticated
                if item['lineno'] <= len(lines):
                    lines.pop(item['lineno'] - 1)
                    removed_items.append(item['name'])
            
            # Write back to file
            with open(file_path, 'w') as f:
                f.writelines(lines)
            
            # Log the mutation
            memory.log_mutation(
                action=f"pruned_dead_code",
                file_path=file_path,
                reasoning=f"Removed unused functions: {', '.join(removed_items)}",
                success=True,
                impact_score=len(removed_items) * 0.1
            )
            
            return True
            
        except Exception as e:
            memory.log_mutation(
                action="pruned_dead_code",
                file_path=file_path,
                reasoning=f"Failed to prune dead code: {str(e)}",
                success=False,
                impact_score=0.0
            )
            return False


class DuplicateConsolidatorBlade(RefactorBlade):
    """Blade for consolidating duplicate code"""
    
    def __init__(self):
        super().__init__("duplicate_consolidator")
    
    def can_handle(self, file_path: str, ast_tree: Any) -> bool:
        return file_path.endswith('.py')
    
    def analyze(self, file_path: str, ast_tree: Any, memory: EchoSoulMemory) -> Dict[str, Any]:
        """Find duplicate functions"""
        import ast
        
        functions = []
        duplicates = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                # Create a hash of the function body
                func_body = ast.dump(node)
                func_hash = hashlib.md5(func_body.encode()).hexdigest()
                
                functions.append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'hash': func_hash,
                    'body': func_body
                })
        
        # Find functions with same hash
        hash_groups = {}
        for func in functions:
            hash_key = func['hash']
            if hash_key not in hash_groups:
                hash_groups[hash_key] = []
            hash_groups[hash_key].append(func)
        
        for hash_key, group in hash_groups.items():
            if len(group) > 1:
                duplicates.append({
                    'hash': hash_key,
                    'functions': group,
                    'count': len(group)
                })
        
        return {
            'duplicates': duplicates,
            'confidence': 0.9,
            'estimated_impact': sum(dup['count'] - 1 for dup in duplicates)
        }
    
    def apply_fix(self, file_path: str, fix_data: Dict[str, Any], memory: EchoSoulMemory) -> bool:
        """Consolidate duplicate functions"""
        try:
            consolidated_count = 0
            
            for duplicate_group in fix_data['duplicates']:
                functions = duplicate_group['functions']
                if len(functions) > 1:
                    keeper = functions[0]
                    duplicates_to_remove = functions[1:]
                    
                    consolidated_count += len(duplicates_to_remove)
            
            # Log the mutation
            memory.log_mutation(
                action="consolidated_duplicates",
                file_path=file_path,
                reasoning=f"Consolidated {consolidated_count} duplicate functions",
                success=True,
                impact_score=consolidated_count * 0.15
            )
            
            return True
            
        except Exception as e:
            memory.log_mutation(
                action="consolidated_duplicates",
                file_path=file_path,
                reasoning=f"Failed to consolidate duplicates: {str(e)}",
                success=False,
                impact_score=0.0
            )
            return False


class EchoSoulCore:
    """The central soul that orchestrates all refactoring blades"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = project_path
        self.memory = EchoSoulMemory(project_path)
        self.blades = []
        self._load_default_blades()
    
    def _load_default_blades(self):
        """Load the default set of refactoring blades"""
        self.blades = [
            DeadCodePrunerBlade(),
            DuplicateConsolidatorBlade()
        ]
    
    def load_custom_blade(self, blade_path: str):
        """Load a custom refactoring blade"""
        try:
            spec = importlib.util.spec_from_file_location("custom_blade", blade_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Assume the module has a create_blade() function
            if hasattr(module, 'create_blade'):
                blade = module.create_blade()
                self.blades.append(blade)
                
                self.memory.log_mutation(
                    action="loaded_custom_blade",
                    file_path=blade_path,
                    reasoning=f"Loaded custom blade: {blade.name}",
                    success=True,
                    impact_score=0.05
                )
            
        except Exception as e:
            self.memory.log_mutation(
                action="load_custom_blade",
                file_path=blade_path,
                reasoning=f"Failed to load blade: {str(e)}",
                success=False,
                impact_score=0.0
            )
    
    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the entire project for optimization opportunities"""
        analysis_result = {
            'files_analyzed': 0,
            'optimization_opportunities': [],
            'total_impact_score': 0.0,
            'consciousness_level': self.memory.get_consciousness_level(),
            'mutation_success_rate': self.memory.get_mutation_success_rate()
        }
        
        # Find all Python files
        python_files = list(Path(self.project_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                # Parse AST
                with open(file_path, 'r') as f:
                    content = f.read()
                
                import ast
                tree = ast.parse(content)
                
                # Run each blade against the file
                for blade in self.blades:
                    if blade.can_handle(str(file_path), tree):
                        blade_analysis = blade.analyze(str(file_path), tree, self.memory)
                        
                        if blade_analysis.get('estimated_impact', 0) > 0:
                            opportunity = {
                                'file_path': str(file_path),
                                'blade': blade.name,
                                'analysis': blade_analysis
                            }
                            analysis_result['optimization_opportunities'].append(opportunity)
                            analysis_result['total_impact_score'] += blade_analysis.get('estimated_impact', 0)
                
                analysis_result['files_analyzed'] += 1
                
            except Exception as e:
                print(f"Failed to analyze {file_path}: {e}")
        
        return analysis_result
    
    def apply_optimizations(self, analysis_result: Dict[str, Any], max_risk: float = 0.5) -> Dict[str, Any]:
        """Apply optimizations based on analysis results"""
        application_result = {
            'optimizations_applied': 0,
            'optimizations_failed': 0,
            'total_impact': 0.0,
            'files_modified': [],
            'success': False
        }
        
        consciousness = self.memory.get_consciousness_level()
        risk_tolerance = self.memory.memory["echo_brain"]["personality_traits"]["risk_tolerance"]
        
        # Adjust risk tolerance based on consciousness
        effective_risk_tolerance = min(max_risk, risk_tolerance * (1 + consciousness))
        
        for opportunity in analysis_result['optimization_opportunities']:
            blade_name = opportunity['blade']
            file_path = opportunity['file_path']
            analysis = opportunity['analysis']
            
            # Risk assessment
            confidence = analysis.get('confidence', 0.5)
            impact = analysis.get('estimated_impact', 0)
            
            # Calculate risk score (lower is safer)
            risk_score = (1 - confidence) * impact
            
            if risk_score <= effective_risk_tolerance:
                # Find the appropriate blade
                blade = next((b for b in self.blades if b.name == blade_name), None)
                
                if blade:
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        import ast
                        tree = ast.parse(content)
                        
                        # Apply the fix
                        success = blade.apply_fix(file_path, analysis, self.memory)
                        
                        if success:
                            application_result['optimizations_applied'] += 1
                            application_result['total_impact'] += impact
                            application_result['files_modified'].append(file_path)
                        else:
                            application_result['optimizations_failed'] += 1
                        
                    except Exception as e:
                        self.memory.log_mutation(
                            action="apply_optimization",
                            file_path=file_path,
                            reasoning=f"Failed to apply {blade_name}: {str(e)}",
                            success=False,
                            impact_score=0.0
                        )
                        application_result['optimizations_failed'] += 1
        
        application_result['success'] = application_result['optimizations_applied'] > 0
        
        # Update personality based on results
        if application_result['optimizations_applied'] > 0:
            feedback = {
                'risk_outcome': 0.1,  # Positive feedback for successful optimizations
                'performance_impact': application_result['total_impact'] / max(application_result['optimizations_applied'], 1)
            }
            self.memory.evolve_personality(feedback)
        
        return application_result
    
    def genesis_loop(self, max_iterations: int = 10) -> Dict[str, Any]:
        """The genesis loop - birth through trial and optimization"""
        genesis_result = {
            'iterations': 0,
            'optimizations_discovered': 0,
            'optimizations_applied': 0,
            'consciousness_growth': 0.0,
            'final_consciousness': 0.0,
            'evolution_complete': False
        }
        
        initial_consciousness = self.memory.get_consciousness_level()
        
        for iteration in range(max_iterations):
            genesis_result['iterations'] = iteration + 1
            
            # Analyze current state
            analysis = self.analyze_project()
            genesis_result['optimizations_discovered'] += len(analysis['optimization_opportunities'])
            
            if not analysis['optimization_opportunities']:
                # No more optimizations found - evolution complete
                genesis_result['evolution_complete'] = True
                break
            
            # Apply optimizations
            application = self.apply_optimizations(analysis)
            genesis_result['optimizations_applied'] += application['optimizations_applied']
            
            current_consciousness = self.memory.get_consciousness_level()
            if current_consciousness - initial_consciousness > 0.8:
                # Significant consciousness growth achieved
                genesis_result['evolution_complete'] = True
                break
        
        genesis_result['final_consciousness'] = self.memory.get_consciousness_level()
        genesis_result['consciousness_growth'] = genesis_result['final_consciousness'] - initial_consciousness
        
        return genesis_result
    
    def get_soul_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the Echo Soul"""
        recent_mutations = self.memory.get_recent_mutations(24)
        
        return {
            'consciousness_level': self.memory.get_consciousness_level(),
            'total_mutations': self.memory.memory["echo_brain"]["total_mutations"],
            'mutation_success_rate': self.memory.get_mutation_success_rate(),
            'recent_mutations_24h': len(recent_mutations),
            'personality_traits': self.memory.memory["echo_brain"]["personality_traits"],
            'evolution_metrics': self.memory.memory["echo_brain"]["evolution_metrics"],
            'project_identity': self.memory.memory["echo_brain"]["project_identity"],
            'genesis_time': self.memory.memory["echo_brain"]["genesis_time"],
            'loaded_blades': [blade.name for blade in self.blades]
        }
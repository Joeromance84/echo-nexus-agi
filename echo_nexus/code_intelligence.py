"""
EchoRefactorCore: Code Intelligence Engine
Scientific AST-based analysis and autonomous code optimization
"""

import ast
import os
import re
import json
import hashlib
import difflib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict, deque


@dataclass
class CodeNode:
    """Represents a code entity in the dependency graph"""
    id: str
    type: str  # 'function', 'class', 'module', 'import'
    name: str
    file_path: str
    line_number: int
    dependencies: Set[str]
    used_by: Set[str]
    ast_hash: str
    semantic_intent: str


@dataclass
class DuplicateGroup:
    """Represents a group of duplicate code entities"""
    hash_signature: str
    nodes: List[CodeNode]
    similarity_score: float
    recommended_keeper: str
    removal_candidates: List[str]


class DependencyGraphBuilder:
    """Builds comprehensive dependency graphs using AST analysis"""
    
    def __init__(self, github_helper):
        self.github_helper = github_helper
        self.dependency_graph = {}
        self.file_asts = {}
        self.semantic_patterns = {
            'authentication': ['auth', 'login', 'password', 'token', 'session'],
            'data_processing': ['process', 'parse', 'transform', 'convert', 'serialize'],
            'network': ['request', 'response', 'api', 'http', 'fetch', 'download'],
            'ui_interaction': ['click', 'touch', 'button', 'input', 'form', 'display'],
            'file_operations': ['read', 'write', 'save', 'load', 'file', 'path'],
            'validation': ['validate', 'check', 'verify', 'ensure', 'confirm'],
            'error_handling': ['error', 'exception', 'try', 'catch', 'handle'],
            'encryption': ['encrypt', 'decrypt', 'hash', 'crypto', 'security'],
            'database': ['db', 'query', 'select', 'insert', 'update', 'delete']
        }
    
    def build_repository_graph(self, repo_url: str) -> Dict[str, Any]:
        """
        Build complete dependency graph for a repository
        Pure API-driven analysis using GitHub API
        """
        result = {
            'success': False,
            'graph_stats': {},
            'files_analyzed': 0,
            'nodes_created': 0,
            'dependencies_mapped': 0,
            'dead_code_detected': [],
            'duplicates_found': [],
            'semantic_mismatches': [],
            'error': None
        }
        
        try:
            python_files = self._get_python_files(repo_url)
            
            if not python_files:
                result['error'] = "No Python files found in repository"
                return result
            
            for file_path in python_files:
                self._analyze_file_ast(repo_url, file_path)
            
            result['files_analyzed'] = len(python_files)
            
            # Build dependency relationships
            self._build_dependency_relationships()
            
            # Detect dead code
            entry_points = self._identify_entry_points()
            dead_nodes = self._detect_dead_code(entry_points)
            result['dead_code_detected'] = [node.id for node in dead_nodes]
            
            # Find duplicates
            duplicate_groups = self._find_duplicates()
            result['duplicates_found'] = [
                {
                    'hash': group.hash_signature,
                    'count': len(group.nodes),
                    'recommended_keeper': group.recommended_keeper,
                    'candidates_for_removal': group.removal_candidates
                }
                for group in duplicate_groups
            ]
            
            # Semantic validation
            semantic_issues = self._validate_semantics()
            result['semantic_mismatches'] = semantic_issues
            
            # Generate statistics
            result['graph_stats'] = self._generate_graph_statistics()
            result['nodes_created'] = len(self.dependency_graph)
            result['dependencies_mapped'] = sum(
                len(node.dependencies) for node in self.dependency_graph.values()
            )
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Graph analysis failed: {str(e)}"
        
        return result
    
    def _get_python_files(self, repo_url: str) -> List[str]:
        """Get all Python files from repository using GitHub API"""
        try:
            # Use GitHub helper to get file tree
            tree_result = self.github_helper.smart_file_check(repo_url, "**/*.py")
            
            if tree_result['success'] and tree_result['files_found']:
                return [file['path'] for file in tree_result['files_found'] if file['path'].endswith('.py')]
            
            return []
            
        except Exception as e:
            print(f"Failed to get Python files: {e}")
            return []
    
    def _analyze_file_ast(self, repo_url: str, file_path: str):
        """Analyze a single file's AST and extract code entities"""
        try:
            # Get file content via GitHub API
            file_result = self.github_helper.smart_file_check(repo_url, file_path)
            
            if not file_result['success'] or not file_result['files_found']:
                return
            
            file_content = file_result['files_found'][0]['content']
            
            # Parse AST
            try:
                tree = ast.parse(file_content)
                self.file_asts[file_path] = tree
            except SyntaxError:
                print(f"Syntax error in {file_path}, skipping AST analysis")
                return
            
            # Extract code entities
            extractor = ASTNodeExtractor(file_path)
            extractor.visit(tree)
            
            # Add nodes to dependency graph
            for node in extractor.nodes:
                self.dependency_graph[node.id] = node
            
        except Exception as e:
            print(f"Failed to analyze {file_path}: {e}")
    
    def _build_dependency_relationships(self):
        """Build dependency relationships between code entities"""
        for file_path, tree in self.file_asts.items():
            relationship_builder = DependencyRelationshipBuilder(
                file_path, self.dependency_graph
            )
            relationship_builder.visit(tree)
    
    def _identify_entry_points(self) -> List[str]:
        """Identify entry points for dependency traversal"""
        entry_points = []
        
        for node_id, node in self.dependency_graph.items():
            # Main functions
            if node.name == 'main' and node.type == 'function':
                entry_points.append(node_id)
            
            # Module-level execution
            if '__main__' in node.name:
                entry_points.append(node_id)
            
            # Workflow-referenced functions (basic heuristic)
            if 'run' in node.name.lower() or 'start' in node.name.lower():
                entry_points.append(node_id)
        
        # If no clear entry points, use all top-level functions
        if not entry_points:
            entry_points = [
                node_id for node_id, node in self.dependency_graph.items()
                if node.type == 'function' and node.line_number <= 50
            ]
        
        return entry_points
    
    def _detect_dead_code(self, entry_points: List[str]) -> List[CodeNode]:
        """Detect unreachable code using graph traversal"""
        reachable = set()
        queue = deque(entry_points)
        
        while queue:
            current_id = queue.popleft()
            if current_id in reachable or current_id not in self.dependency_graph:
                continue
            
            reachable.add(current_id)
            node = self.dependency_graph[current_id]
            
            # Add dependencies to queue
            for dep_id in node.dependencies:
                if dep_id not in reachable:
                    queue.append(dep_id)
        
        # Find unreachable nodes
        dead_nodes = []
        for node_id, node in self.dependency_graph.items():
            if node_id not in reachable and node.type in ['function', 'class']:
                dead_nodes.append(node)
        
        return dead_nodes
    
    def _find_duplicates(self) -> List[DuplicateGroup]:
        """Find duplicate code using AST hashing and similarity analysis"""
        hash_groups = defaultdict(list)
        
        # Group by AST hash
        for node in self.dependency_graph.values():
            if node.type in ['function', 'class']:
                hash_groups[node.ast_hash].append(node)
        
        duplicate_groups = []
        
        for hash_signature, nodes in hash_groups.items():
            if len(nodes) > 1:
                # Calculate similarity scores and determine best version
                group = self._analyze_duplicate_group(hash_signature, nodes)
                if group:
                    duplicate_groups.append(group)
        
        return duplicate_groups
    
    def _analyze_duplicate_group(self, hash_signature: str, nodes: List[CodeNode]) -> Optional[DuplicateGroup]:
        """Analyze a group of duplicate nodes to determine the best version"""
        if len(nodes) < 2:
            return None
        
        # Simple heuristic: prefer nodes with fewer error associations
        # In a real implementation, this would consult the Error Genome
        
        # For now, use basic heuristics
        scored_nodes = []
        for node in nodes:
            score = 0
            
            # Prefer nodes in main files
            if 'main' in node.file_path.lower():
                score += 2
            
            # Prefer nodes with better semantic naming
            if node.semantic_intent != 'unknown':
                score += 1
            
            # Prefer nodes that are used by others
            score += len(node.used_by)
            
            scored_nodes.append((score, node))
        
        # Sort by score (highest first)
        scored_nodes.sort(reverse=True, key=lambda x: x[0])
        
        recommended_keeper = scored_nodes[0][1].id
        removal_candidates = [node.id for _, node in scored_nodes[1:]]
        
        return DuplicateGroup(
            hash_signature=hash_signature,
            nodes=nodes,
            similarity_score=1.0,  # Exact duplicates
            recommended_keeper=recommended_keeper,
            removal_candidates=removal_candidates
        )
    
    def _validate_semantics(self) -> List[Dict[str, Any]]:
        """Validate semantic consistency between names and implementation"""
        semantic_issues = []
        
        for node in self.dependency_graph.values():
            if node.type not in ['function', 'class']:
                continue
            
            name_intent = self._infer_semantic_intent(node.name)
            
            if name_intent != 'unknown' and name_intent != node.semantic_intent:
                semantic_issues.append({
                    'node_id': node.id,
                    'name': node.name,
                    'file_path': node.file_path,
                    'line_number': node.line_number,
                    'expected_intent': name_intent,
                    'actual_intent': node.semantic_intent,
                    'severity': 'medium',
                    'suggestion': f"Function name suggests {name_intent} but implementation indicates {node.semantic_intent}"
                })
        
        return semantic_issues
    
    def _infer_semantic_intent(self, name: str) -> str:
        """Infer semantic intent from function/class name"""
        name_lower = name.lower()
        
        for intent, patterns in self.semantic_patterns.items():
            if any(pattern in name_lower for pattern in patterns):
                return intent
        
        return 'unknown'
    
    def _generate_graph_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive graph statistics"""
        stats = {
            'total_nodes': len(self.dependency_graph),
            'node_types': defaultdict(int),
            'dependency_density': 0.0,
            'most_connected_nodes': [],
            'semantic_distribution': defaultdict(int),
            'complexity_metrics': {}
        }
        
        total_dependencies = 0
        connection_counts = []
        
        for node in self.dependency_graph.values():
            stats['node_types'][node.type] += 1
            stats['semantic_distribution'][node.semantic_intent] += 1
            
            connection_count = len(node.dependencies) + len(node.used_by)
            connection_counts.append(connection_count)
            total_dependencies += len(node.dependencies)
        
        # Calculate dependency density
        if len(self.dependency_graph) > 1:
            max_possible = len(self.dependency_graph) * (len(self.dependency_graph) - 1)
            stats['dependency_density'] = total_dependencies / max_possible
        
        # Find most connected nodes
        node_connections = [
            (len(node.dependencies) + len(node.used_by), node.name, node.id)
            for node in self.dependency_graph.values()
        ]
        node_connections.sort(reverse=True)
        stats['most_connected_nodes'] = [
            {'name': name, 'id': node_id, 'connections': connections}
            for connections, name, node_id in node_connections[:5]
        ]
        
        # Complexity metrics
        if connection_counts:
            stats['complexity_metrics'] = {
                'average_connections': sum(connection_counts) / len(connection_counts),
                'max_connections': max(connection_counts),
                'highly_coupled_nodes': len([c for c in connection_counts if c > 10])
            }
        
        return dict(stats)


class ASTNodeExtractor(ast.NodeVisitor):
    """Extracts code entities from AST"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.nodes = []
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Extract function definitions"""
        function_id = f"{self.file_path}:{node.name}:{node.lineno}"
        
        ast_content = ast.dump(node)
        ast_hash = hashlib.md5(ast_content.encode()).hexdigest()[:12]
        
        semantic_intent = self._infer_function_intent(node)
        
        code_node = CodeNode(
            id=function_id,
            type='function',
            name=node.name,
            file_path=self.file_path,
            line_number=node.lineno,
            dependencies=set(),
            used_by=set(),
            ast_hash=ast_hash,
            semantic_intent=semantic_intent
        )
        
        self.nodes.append(code_node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Extract class definitions"""
        class_id = f"{self.file_path}:{node.name}:{node.lineno}"
        
        ast_content = ast.dump(node)
        ast_hash = hashlib.md5(ast_content.encode()).hexdigest()[:12]
        
        semantic_intent = self._infer_class_intent(node)
        
        code_node = CodeNode(
            id=class_id,
            type='class',
            name=node.name,
            file_path=self.file_path,
            line_number=node.lineno,
            dependencies=set(),
            used_by=set(),
            ast_hash=ast_hash,
            semantic_intent=semantic_intent
        )
        
        self.nodes.append(code_node)
        
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def _infer_function_intent(self, node) -> str:
        """Infer semantic intent from function AST"""
        function_source = ast.unparse(node) if hasattr(ast, 'unparse') else ''
        
        # Simple keyword-based intent detection
        intent_keywords = {
            'authentication': ['password', 'login', 'auth', 'token'],
            'data_processing': ['process', 'parse', 'transform', 'convert'],
            'network': ['request', 'http', 'api', 'fetch', 'download'],
            'file_operations': ['open', 'read', 'write', 'file'],
            'validation': ['validate', 'check', 'verify'],
            'encryption': ['encrypt', 'decrypt', 'hash', 'crypto']
        }
        
        source_lower = function_source.lower()
        for intent, keywords in intent_keywords.items():
            if any(keyword in source_lower for keyword in keywords):
                return intent
        
        return 'unknown'
    
    def _infer_class_intent(self, node) -> str:
        """Infer semantic intent from class AST"""
        class_name = node.name.lower()
        
        intent_patterns = {
            'data_processing': ['processor', 'parser', 'transformer'],
            'network': ['client', 'api', 'service', 'handler'],
            'ui_interaction': ['view', 'widget', 'button', 'form'],
            'database': ['model', 'repository', 'dao', 'orm'],
            'authentication': ['auth', 'login', 'user']
        }
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in class_name for pattern in patterns):
                return intent
        
        return 'unknown'


class DependencyRelationshipBuilder(ast.NodeVisitor):
    """Builds dependency relationships between code entities"""
    
    def __init__(self, file_path: str, dependency_graph: Dict[str, CodeNode]):
        self.file_path = file_path
        self.dependency_graph = dependency_graph
        self.current_function = None
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Track function context for dependency mapping"""
        function_id = f"{self.file_path}:{node.name}:{node.lineno}"
        old_function = self.current_function
        self.current_function = function_id
        
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_ClassDef(self, node):
        """Track class context for dependency mapping"""
        class_id = f"{self.file_path}:{node.name}:{node.lineno}"
        old_class = self.current_class
        self.current_class = class_id
        
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_Call(self, node):
        """Track function calls to build dependency relationships"""
        if self.current_function:
            call_name = self._extract_call_name(node)
            if call_name:
                # Find the called function in the graph
                for target_id, target_node in self.dependency_graph.items():
                    if target_node.name == call_name:
                        # Add dependency relationship
                        if self.current_function in self.dependency_graph:
                            self.dependency_graph[self.current_function].dependencies.add(target_id)
                            target_node.used_by.add(self.current_function)
                        break
        
        self.generic_visit(node)
    
    def _extract_call_name(self, node) -> Optional[str]:
        """Extract function name from call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None


class AutoRepairEngine:
    """Automated diagnosis and repair of build failures"""
    
    def __init__(self, github_helper):
        self.github_helper = github_helper
        self.error_patterns = {
            'missing_dependency': {
                'pattern': r'ImportError: No module named [\'"]([^\'"]+)[\'"]',
                'fix_type': 'add_dependency'
            },
            'syntax_error': {
                'pattern': r'SyntaxError: (.+) \((.+), line (\d+)\)',
                'fix_type': 'syntax_fix'
            },
            'type_error': {
                'pattern': r'TypeError: (.+)',
                'fix_type': 'type_fix'
            },
            'file_not_found': {
                'pattern': r'FileNotFoundError: \[Errno 2\] No such file or directory: [\'"]([^\'"]+)[\'"]',
                'fix_type': 'create_file'
            },
            'permission_error': {
                'pattern': r'PermissionError: \[Errno 13\] Permission denied',
                'fix_type': 'fix_permissions'
            }
        }
    
    def diagnose_and_repair(self, repo_url: str, workflow_name: str = None) -> Dict[str, Any]:
        """
        Diagnose build failures and apply automatic repairs
        """
        result = {
            'success': False,
            'errors_found': [],
            'repairs_applied': [],
            'pr_created': False,
            'error': None
        }
        
        try:
            # Get workflow logs
            logs = self._get_workflow_logs(repo_url, workflow_name)
            
            if not logs:
                result['error'] = "No workflow logs found"
                return result
            
            errors_found = self._analyze_error_patterns(logs)
            result['errors_found'] = errors_found
            
            if not errors_found:
                result['success'] = True
                return result
            
            repairs = []
            for error in errors_found:
                repair = self._generate_repair(error)
                if repair:
                    repairs.append(repair)
            
            if repairs:
                # Apply repairs via GitHub API
                pr_result = self._apply_repairs_via_pr(repo_url, repairs)
                result['repairs_applied'] = repairs
                result['pr_created'] = pr_result['success']
                
                if pr_result['success']:
                    result['pr_url'] = pr_result.get('pr_url')
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Auto-repair failed: {str(e)}"
        
        return result
    
    def _get_workflow_logs(self, repo_url: str, workflow_name: str = None) -> str:
        """Get workflow logs using GitHub API"""
        try:
            # Use existing GitHub helper method
            status_result = self.github_helper.monitor_build_status(repo_url)
            
            if status_result['success'] and status_result['recent_runs']:
                # Get the most recent failed run
                for run in status_result['recent_runs']:
                    if run['status'] == 'failed':
                        return run.get('logs', '')
            
            return ""
            
        except Exception as e:
            print(f"Failed to get workflow logs: {e}")
            return ""
    
    def _analyze_error_patterns(self, logs: str) -> List[Dict[str, Any]]:
        """Analyze logs for known error patterns"""
        errors_found = []
        
        for error_type, error_config in self.error_patterns.items():
            pattern = error_config['pattern']
            matches = re.finditer(pattern, logs, re.MULTILINE)
            
            for match in matches:
                error_data = {
                    'type': error_type,
                    'fix_type': error_config['fix_type'],
                    'match': match.group(0),
                    'groups': match.groups(),
                    'confidence': 0.9
                }
                errors_found.append(error_data)
        
        return errors_found
    
    def _generate_repair(self, error: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate repair actions for a specific error"""
        fix_type = error['fix_type']
        
        repair = {
            'error_type': error['type'],
            'fix_type': fix_type,
            'description': '',
            'files_to_modify': [],
            'confidence': error['confidence']
        }
        
        if fix_type == 'add_dependency':
            # Extract missing module name
            if error['groups']:
                module_name = error['groups'][0]
                repair['description'] = f"Add missing dependency: {module_name}"
                repair['files_to_modify'] = [
                    {
                        'path': 'requirements.txt',
                        'action': 'append',
                        'content': f"\n{module_name}"
                    }
                ]
                
                repair['files_to_modify'].append({
                    'path': 'buildozer.spec',
                    'action': 'modify_section',
                    'section': 'requirements',
                    'content': module_name
                })
        
        elif fix_type == 'create_file':
            if error['groups']:
                file_path = error['groups'][0]
                repair['description'] = f"Create missing file: {file_path}"
                repair['files_to_modify'] = [
                    {
                        'path': file_path,
                        'action': 'create',
                        'content': f"# Auto-generated file\n# Created by EchoRefactorCore\n"
                    }
                ]
        
        elif fix_type == 'fix_permissions':
            repair['description'] = "Fix file permissions in workflow"
            repair['files_to_modify'] = [
                {
                    'path': '.github/workflows/build.yml',
                    'action': 'add_step',
                    'content': {
                        'name': 'Fix permissions',
                        'run': 'chmod +x buildozer'
                    }
                }
            ]
        
        return repair if repair['files_to_modify'] else None
    
    def _apply_repairs_via_pr(self, repo_url: str, repairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply repairs by creating a pull request"""
        try:
            branch_name = f"auto-repair-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Create repair content
            repair_files = {}
            pr_description = "## 🔧 Automated Build Repairs\n\n"
            
            for repair in repairs:
                pr_description += f"- **{repair['description']}** (confidence: {repair['confidence']:.0%})\n"
                
                for file_mod in repair['files_to_modify']:
                    file_path = file_mod['path']
                    
                    if file_mod['action'] == 'create':
                        repair_files[file_path] = file_mod['content']
                    elif file_mod['action'] == 'append':
                        # For append operations, we'd need to get existing content first
                        existing_result = self.github_helper.smart_file_check(repo_url, file_path)
                        existing_content = ""
                        
                        if existing_result['success'] and existing_result['files_found']:
                            existing_content = existing_result['files_found'][0]['content']
                        
                        repair_files[file_path] = existing_content + file_mod['content']
            
            pr_description += "\n---\n*This PR was created automatically by EchoRefactorCore*"
            
            # Use smart conflict resolution to create the PR
            pr_result = self.github_helper.smart_conflict_resolution(
                repo_url,
                "auto-repair-changes",
                json.dumps(repair_files),
                commit_message="🔧 Auto-repair build failures",
                pr_title="Auto-repair build failures",
                pr_description=pr_description
            )
            
            return pr_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
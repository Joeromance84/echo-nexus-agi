"""
Echo Nexus: Symbolic Debugging Engine (The Crash Interpreter)
Processes crash data and maps to functions of intent using AST analysis
"""

import ast
import json
import hashlib
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class CrashSignature:
    """Represents a unique crash signature for genome classification"""
    error_type: str
    function_name: str
    line_number: int
    file_path: str
    intent_signature: str
    genome_hash: str


class SymbolicDebugger:
    """Advanced AST-based crash analysis and intent mapping"""
    
    def __init__(self):
        self.intent_patterns = {
            'ui_interaction': ['click', 'touch', 'tap', 'swipe', 'gesture'],
            'data_processing': ['process', 'parse', 'transform', 'convert', 'serialize'],
            'network_operation': ['request', 'download', 'upload', 'sync', 'fetch'],
            'file_operation': ['read', 'write', 'save', 'load', 'delete'],
            'navigation': ['navigate', 'route', 'transition', 'move', 'go'],
            'initialization': ['init', 'setup', 'configure', 'start', 'launch'],
            'validation': ['validate', 'check', 'verify', 'ensure', 'confirm']
        }
    
    def interpret_crash(self, crash_payload: Dict[str, Any]) -> CrashSignature:
        """
        Interpret crash data and extract symbolic meaning
        Maps technical crashes to functional intent
        """
        stack_trace = crash_payload.get('stack_trace', '')
        error_message = crash_payload.get('error_message', '')
        build_id = crash_payload.get('build_id', '')
        
        # Parse stack trace for meaningful function calls
        parsed_trace = self._parse_stack_trace(stack_trace)
        
        # Extract the most relevant function (closest to user intent)
        primary_function = self._identify_intent_function(parsed_trace)
        
        # Map to intent category
        intent_signature = self._map_to_intent(primary_function)
        
        # Create unique genome hash
        genome_components = [
            primary_function.get('function_name', ''),
            error_message.split(':')[0] if ':' in error_message else error_message,
            intent_signature
        ]
        genome_hash = hashlib.md5('|'.join(genome_components).encode()).hexdigest()[:12]
        
        return CrashSignature(
            error_type=error_message.split(':')[0] if ':' in error_message else 'UnknownError',
            function_name=primary_function.get('function_name', 'unknown'),
            line_number=primary_function.get('line_number', 0),
            file_path=primary_function.get('file_path', 'unknown'),
            intent_signature=intent_signature,
            genome_hash=genome_hash
        )
    
    def _parse_stack_trace(self, stack_trace: str) -> List[Dict[str, Any]]:
        """Parse stack trace into structured function call data"""
        functions = []
        lines = stack_trace.split('\n')
        
        current_function = {}
        for line in lines:
            line = line.strip()
            
            # Extract file and line number
            if 'File "' in line and ', line ' in line:
                try:
                    file_part = line.split('File "')[1].split('"')[0]
                    line_part = line.split(', line ')[1].split(',')[0]
                    current_function['file_path'] = file_part.split('/')[-1]  # Just filename
                    current_function['line_number'] = int(line_part)
                except:
                    pass
            
            # Extract function name
            elif line.startswith('in ') and current_function:
                function_name = line.replace('in ', '').strip()
                current_function['function_name'] = function_name
                
            # Extract code context
            elif not line.startswith('File') and not line.startswith('Traceback') and line:
                current_function['code_context'] = line
                if current_function.get('function_name'):
                    functions.append(current_function.copy())
                current_function = {}
        
        return functions
    
    def _identify_intent_function(self, parsed_trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify the function most likely representing user intent"""
        if not parsed_trace:
            return {}
        
        # Prioritize functions that match user intent patterns
        for func in reversed(parsed_trace):  # Start from the crash point
            func_name = func.get('function_name', '').lower()
            file_path = func.get('file_path', '').lower()
            
            # Skip system/framework functions
            if any(skip in file_path for skip in ['site-packages', 'python', 'kivy', 'android']):
                continue
                
            # Prioritize user-defined functions with clear intent
            if any(pattern in func_name for intent_list in self.intent_patterns.values() for pattern in intent_list):
                return func
        
        # If no intent-specific function found, return the last user function
        for func in reversed(parsed_trace):
            file_path = func.get('file_path', '').lower()
            if not any(skip in file_path for skip in ['site-packages', 'python', 'kivy', 'android']):
                return func
        
        return parsed_trace[-1] if parsed_trace else {}
    
    def _map_to_intent(self, function_data: Dict[str, Any]) -> str:
        """Map function to user intent category"""
        func_name = function_data.get('function_name', '').lower()
        code_context = function_data.get('code_context', '').lower()
        
        # Analyze function name and context for intent patterns
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in func_name or pattern in code_context for pattern in patterns):
                return intent
        
        return 'unknown_intent'


class CrashInterpreter:
    """Main crash interpretation service"""
    
    def __init__(self, database_helper):
        self.symbolic_debugger = SymbolicDebugger()
        self.database_helper = database_helper
    
    def process_crash_report(self, crash_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming crash report and update Error Genome
        Pure API-driven, no shell commands or external dependencies
        """
        result = {
            'success': False,
            'crash_signature': None,
            'genome_action': None,  # 'new', 'updated', 'reinforced'
            'priority_score': 0,
            'suggested_fixes': [],
            'error': None
        }
        
        try:
            # Step 1: Interpret crash using symbolic debugging
            crash_signature = self.symbolic_debugger.interpret_crash(crash_payload)
            result['crash_signature'] = crash_signature.__dict__
            
            # Step 2: Check Error Genome for existing signatures
            existing_bug = self._check_genome_for_signature(crash_signature)
            
            if existing_bug:
                # Step 3a: Reinforce existing bug pattern
                self._reinforce_bug_genome(existing_bug['id'], crash_payload)
                result['genome_action'] = 'reinforced'
                result['priority_score'] = existing_bug['occurrence_count'] + 1
                result['suggested_fixes'] = existing_bug.get('known_fixes', [])
            else:
                # Step 3b: Create new bug genome entry
                bug_id = self._create_bug_genome(crash_signature, crash_payload)
                result['genome_action'] = 'new'
                result['priority_score'] = 1
                result['suggested_fixes'] = self._generate_initial_fixes(crash_signature)
            
            # Step 4: Trigger Echo Nexus Brain event
            self._trigger_nexus_event('crash_processed', {
                'signature': crash_signature.__dict__,
                'action': result['genome_action'],
                'priority': result['priority_score']
            })
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Crash interpretation failed: {str(e)}"
        
        return result
    
    def _check_genome_for_signature(self, signature: CrashSignature) -> Optional[Dict[str, Any]]:
        """Check if crash signature exists in Error Genome database"""
        try:
            query = """
            SELECT * FROM error_genome 
            WHERE genome_hash = %s OR (
                error_type = %s AND 
                function_name = %s AND 
                intent_signature = %s
            )
            ORDER BY occurrence_count DESC
            LIMIT 1
            """
            
            result = self.database_helper.execute_query(query, [
                signature.genome_hash,
                signature.error_type,
                signature.function_name,
                signature.intent_signature
            ])
            
            return result[0] if result else None
            
        except Exception:
            return None
    
    def _reinforce_bug_genome(self, bug_id: int, crash_payload: Dict[str, Any]):
        """Reinforce existing bug pattern with new occurrence"""
        try:
            query = """
            UPDATE error_genome 
            SET occurrence_count = occurrence_count + 1,
                last_seen = %s,
                latest_build_id = %s,
                mutation_strength = mutation_strength + 1
            WHERE id = %s
            """
            
            self.database_helper.execute_query(query, [
                datetime.now(),
                crash_payload.get('build_id', ''),
                bug_id
            ])
            
        except Exception as e:
            print(f"Failed to reinforce bug genome: {e}")
    
    def _create_bug_genome(self, signature: CrashSignature, crash_payload: Dict[str, Any]) -> int:
        """Create new bug genome entry"""
        try:
            query = """
            INSERT INTO error_genome (
                genome_hash, error_type, function_name, line_number, 
                file_path, intent_signature, occurrence_count, 
                first_seen, last_seen, build_id, stack_trace,
                mutation_strength, resolution_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            
            now = datetime.now()
            result = self.database_helper.execute_query(query, [
                signature.genome_hash,
                signature.error_type,
                signature.function_name,
                signature.line_number,
                signature.file_path,
                signature.intent_signature,
                1,  # occurrence_count
                now,  # first_seen
                now,  # last_seen
                crash_payload.get('build_id', ''),
                crash_payload.get('stack_trace', ''),
                1,  # mutation_strength
                'active'  # resolution_status
            ])
            
            return result[0]['id'] if result else None
            
        except Exception as e:
            print(f"Failed to create bug genome: {e}")
            return None
    
    def _generate_initial_fixes(self, signature: CrashSignature) -> List[str]:
        """Generate initial fix suggestions based on crash signature"""
        fixes = []
        
        error_type = signature.error_type.lower()
        intent = signature.intent_signature
        
        # Error-specific fixes
        if 'null' in error_type or 'none' in error_type:
            fixes.append("Add null/None checking before accessing object properties")
        elif 'index' in error_type or 'key' in error_type:
            fixes.append("Add bounds checking or key existence validation")
        elif 'network' in error_type or 'connection' in error_type:
            fixes.append("Add network error handling and retry logic")
        elif 'permission' in error_type:
            fixes.append("Add permission request handling")
        
        # Intent-specific fixes
        if intent == 'ui_interaction':
            fixes.append("Add UI state validation before interaction")
        elif intent == 'data_processing':
            fixes.append("Add input validation and error handling")
        elif intent == 'network_operation':
            fixes.append("Implement timeout and retry mechanisms")
        
        return fixes or ["General error handling improvement needed"]
    
    def _trigger_nexus_event(self, event_type: str, event_data: Dict[str, Any]):
        """Trigger event for Echo Nexus Brain processing"""
        try:
            query = """
            INSERT INTO nexus_event_queue (
                event_type, event_data, created_at, status
            ) VALUES (%s, %s, %s, %s)
            """
            
            self.database_helper.execute_query(query, [
                event_type,
                json.dumps(event_data),
                datetime.now(),
                'pending'
            ])
            
        except Exception as e:
            print(f"Failed to trigger nexus event: {e}")
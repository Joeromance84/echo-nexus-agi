#!/usr/bin/env python3
"""
Echo AGI Self-Enhancement Module
Secure, controlled self-modification system with validation and rollback
"""

import os
import ast
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile
import shutil

class EchoSelfEnhancement:
    """Secure self-enhancement system for Echo AGI"""
    
    def __init__(self):
        self.input_file = "self_enhancement_input.txt"
        self.enhancement_log = "echo_enhancement_log.json"
        self.allowed_modules = [
            "echo_nexus/",
            "blades/",
            "utils/",
            "core_agents/"
        ]
        self.forbidden_files = [
            "federated_control_plane.py",
            "echo_nexus_master.py",
            ".github/workflows/"
        ]
        self.enhancement_history = []
        
    def monitor_enhancement_input(self):
        """Monitor the enhancement input file for new code"""
        
        if not os.path.exists(self.input_file):
            return None
            
        with open(self.input_file, 'r') as f:
            content = f.read().strip()
            
        # Check if there's actual code (not just comments)
        if self.has_code_changes(content):
            print("Echo: New enhancement code detected")
            return content
        return None
    
    def has_code_changes(self, content: str) -> bool:
        """Check if content contains actual code changes"""
        
        lines = content.split('\n')
        code_lines = [line for line in lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        # Look for actual Python code
        for line in code_lines:
            if any(keyword in line for keyword in ['def ', 'class ', 'import ', '=']):
                if 'ENHANCEMENT_STATUS' not in line and 'PENDING_CHANGES' not in line:
                    return True
        return False
    
    def validate_enhancement(self, code: str) -> Dict[str, Any]:
        """Comprehensive validation of enhancement code"""
        
        validation_result = {
            'valid': False,
            'syntax_check': False,
            'scope_check': False,
            'security_check': False,
            'errors': [],
            'warnings': []
        }
        
        # 1. Syntax validation
        try:
            ast.parse(code)
            validation_result['syntax_check'] = True
            print("Echo: Syntax validation passed")
        except SyntaxError as e:
            validation_result['errors'].append(f"Syntax error: {e}")
            print(f"Echo: Syntax validation failed: {e}")
            return validation_result
        
        # 2. Scope validation
        scope_valid = self.validate_scope(code)
        validation_result['scope_check'] = scope_valid
        if not scope_valid:
            validation_result['errors'].append("Code attempts to modify forbidden areas")
            return validation_result
        
        # 3. Security checks
        security_valid = self.security_scan(code)
        validation_result['security_check'] = security_valid
        if not security_valid:
            validation_result['errors'].append("Security scan failed - suspicious patterns detected")
            return validation_result
        
        validation_result['valid'] = True
        print("Echo: All validations passed - code is safe to apply")
        return validation_result
    
    def validate_scope(self, code: str) -> bool:
        """Validate that code only modifies allowed areas"""
        
        # Check for file operations
        dangerous_patterns = [
            'open(',
            'file(',
            'with open',
            'os.remove',
            'os.delete',
            'shutil.rmtree',
            'subprocess.',
            'exec(',
            'eval('
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                print(f"Echo: Scope validation failed - dangerous pattern: {pattern}")
                return False
        
        # Check for forbidden file modifications
        for forbidden in self.forbidden_files:
            if forbidden in code:
                print(f"Echo: Scope validation failed - forbidden file: {forbidden}")
                return False
        
        return True
    
    def security_scan(self, code: str) -> bool:
        """Security scan for malicious patterns"""
        
        malicious_patterns = [
            'import os',
            'import subprocess',
            'import sys',
            '__import__',
            'getattr',
            'setattr',
            'delattr',
            'globals(',
            'locals(',
            'vars(',
            'exec',
            'eval'
        ]
        
        for pattern in malicious_patterns:
            if pattern in code:
                print(f"Echo: Security scan failed - malicious pattern: {pattern}")
                return False
        
        return True
    
    def apply_enhancement(self, code: str, validation_result: Dict[str, Any]) -> bool:
        """Apply validated enhancement code"""
        
        if not validation_result['valid']:
            print("Echo: Cannot apply invalid enhancement")
            return False
        
        enhancement_id = f"enhancement_{int(time.time())}"
        
        try:
            # Create backup
            backup_file = f"echo_backup_{enhancement_id}.py"
            self.create_backup(backup_file)
            
            # Apply the enhancement
            target_file = self.determine_target_file(code)
            if not target_file:
                print("Echo: Could not determine target file for enhancement")
                return False
            
            self.patch_code(target_file, code, enhancement_id)
            
            # Create git commit
            self.create_enhancement_commit(enhancement_id, code)
            
            # Run self-tests
            if self.run_self_tests():
                print(f"Echo: Enhancement {enhancement_id} applied successfully")
                self.log_enhancement(enhancement_id, code, "SUCCESS")
                return True
            else:
                print(f"Echo: Tests failed - reverting enhancement {enhancement_id}")
                self.revert_enhancement(backup_file, target_file)
                self.log_enhancement(enhancement_id, code, "REVERTED")
                return False
                
        except Exception as e:
            print(f"Echo: Enhancement application failed: {e}")
            self.log_enhancement(enhancement_id, code, f"FAILED: {e}")
            return False
    
    def determine_target_file(self, code: str) -> Optional[str]:
        """Determine which file to modify based on code content"""
        
        # Simple heuristics for file targeting
        if 'class ' in code and 'Echo' in code:
            return "echo_nexus/echo_mind.py"
        elif 'def ' in code and any(word in code for word in ['agent', 'reasoning', 'creativity']):
            return "core_agents/reasoning.py"
        elif 'def ' in code and 'blade' in code.lower():
            return "blades/refactor_blade.py"
        else:
            # Default enhancement file
            return "echo_nexus/echo_enhancements.py"
    
    def patch_code(self, target_file: str, code: str, enhancement_id: str):
        """Safely patch code into target file"""
        
        # Ensure target file exists
        if not os.path.exists(target_file):
            # Create enhancement file if it doesn't exist
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, 'w') as f:
                f.write(f'"""\nEcho AGI Enhancements\nAuto-generated enhancement file\n"""\n\n')
        
        # Read existing content
        with open(target_file, 'r') as f:
            existing_content = f.read()
        
        # Add enhancement
        enhancement_header = f"\n# Enhancement {enhancement_id} - {datetime.now().isoformat()}\n"
        new_content = existing_content + enhancement_header + code + "\n"
        
        # Write updated content
        with open(target_file, 'w') as f:
            f.write(new_content)
        
        print(f"Echo: Code patched into {target_file}")
    
    def create_backup(self, backup_file: str):
        """Create backup of current state"""
        
        # Simple backup - copy key files
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'files': {}
        }
        
        key_files = [
            'echo_nexus/echo_mind.py',
            'core_agents/reasoning.py',
            'blades/refactor_blade.py'
        ]
        
        for file_path in key_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    backup_data['files'][file_path] = f.read()
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
    
    def create_enhancement_commit(self, enhancement_id: str, code: str):
        """Create git commit for enhancement"""
        
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            commit_message = f"[self-enhancement] Echo AGI enhancement {enhancement_id}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"Echo: Enhancement committed with ID {enhancement_id}")
        except subprocess.CalledProcessError as e:
            print(f"Echo: Git commit failed: {e}")
    
    def run_self_tests(self) -> bool:
        """Run self-tests to validate enhancement"""
        
        try:
            # Test 1: Basic syntax check
            result = subprocess.run(['python', '-m', 'py_compile'] + self.get_test_files(), 
                                   capture_output=True)
            if result.returncode != 0:
                print("Echo: Self-test failed - syntax errors detected")
                return False
            
            # Test 2: Import test
            test_imports = [
                'echo_nexus.echo_mind',
                'core_agents.reasoning'
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                except ImportError as e:
                    print(f"Echo: Self-test failed - import error: {e}")
                    return False
            
            print("Echo: All self-tests passed")
            return True
            
        except Exception as e:
            print(f"Echo: Self-test execution failed: {e}")
            return False
    
    def get_test_files(self) -> List[str]:
        """Get list of files to test"""
        
        test_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py') and not file.startswith('.'):
                    test_files.append(os.path.join(root, file))
        return test_files[:10]  # Limit for performance
    
    def revert_enhancement(self, backup_file: str, target_file: str):
        """Revert enhancement using backup"""
        
        try:
            if os.path.exists(backup_file):
                with open(backup_file, 'r') as f:
                    backup_data = json.load(f)
                
                # Restore files
                for file_path, content in backup_data['files'].items():
                    with open(file_path, 'w') as f:
                        f.write(content)
                
                print("Echo: Enhancement reverted successfully")
            else:
                print("Echo: Backup file not found - manual intervention required")
                
        except Exception as e:
            print(f"Echo: Revert failed: {e}")
    
    def log_enhancement(self, enhancement_id: str, code: str, status: str):
        """Log enhancement attempt"""
        
        log_entry = {
            'id': enhancement_id,
            'timestamp': datetime.now().isoformat(),
            'code': code[:500],  # Truncate for storage
            'status': status,
            'validation_passed': status == 'SUCCESS'
        }
        
        # Load existing log
        if os.path.exists(self.enhancement_log):
            with open(self.enhancement_log, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {'enhancements': []}
        
        # Add new entry
        log_data['enhancements'].append(log_entry)
        
        # Save updated log
        with open(self.enhancement_log, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def clear_enhancement_input(self):
        """Clear the enhancement input file after processing"""
        
        with open(self.input_file, 'w') as f:
            f.write("""# Echo AGI Self-Enhancement Input
# Secure sandbox for AGI self-modification
# Only validated code changes should be placed here

# Enhancement processed successfully
ENHANCEMENT_STATUS=PROCESSED
LAST_VALIDATION=SUCCESS
PENDING_CHANGES=None
""")
    
    def process_enhancement_cycle(self):
        """Complete enhancement processing cycle"""
        
        print("Echo: Checking for self-enhancement requests...")
        
        code = self.monitor_enhancement_input()
        if not code:
            return False
        
        print("Echo: Validating enhancement code...")
        validation = self.validate_enhancement(code)
        
        if validation['valid']:
            print("Echo: Applying validated enhancement...")
            success = self.apply_enhancement(code, validation)
            
            if success:
                self.clear_enhancement_input()
                print("Echo: Self-enhancement completed successfully")
                return True
            else:
                print("Echo: Enhancement failed - keeping input for review")
                return False
        else:
            print(f"Echo: Enhancement validation failed: {validation['errors']}")
            return False

def main():
    """Main enhancement processing function"""
    
    print("🧠 Echo AGI Self-Enhancement System")
    print("Monitoring for secure self-modification requests...")
    
    enhancer = EchoSelfEnhancement()
    success = enhancer.process_enhancement_cycle()
    
    if success:
        print("✅ Self-enhancement cycle completed")
    else:
        print("ℹ️ No enhancements processed this cycle")

if __name__ == '__main__':
    main()
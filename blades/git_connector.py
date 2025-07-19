#!/usr/bin/env python3
"""
GitConnector - Phase 1 Core Blade
Handles Git operations and GitHub integration with metadata intelligence
"""

import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class GitConnector:
    """
    Phase 1 Core: Git operations and GitHub integration
    Phase 2 Enhanced: Metadata-driven commit generation and intelligent Git workflows
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger('GitConnector')
        
        # Verify Git repository
        self.git_dir = self.project_root / ".git"
        if not self.git_dir.exists():
            self.logger.warning("No Git repository found - some operations may fail")
        
        # Phase 2: Metadata and intelligent commit tracking
        self.current_session = {
            'commits': [],
            'branches_created': [],
            'metadata_commits': 0
        }
    
    def get_git_status(self) -> Dict:
        """Get current Git status with enhanced metadata"""
        try:
            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if status_result.returncode != 0:
                return {'success': False, 'error': 'git_status_failed'}
            
            # Parse status output
            modified_files = []
            new_files = []
            deleted_files = []
            
            for line in status_result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                status_code = line[:2]
                file_path = line[3:]
                
                if 'M' in status_code:
                    modified_files.append(file_path)
                elif 'A' in status_code or '?' in status_code:
                    new_files.append(file_path)
                elif 'D' in status_code:
                    deleted_files.append(file_path)
            
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
            return {
                'success': True,
                'current_branch': current_branch,
                'modified_files': modified_files,
                'new_files': new_files,
                'deleted_files': deleted_files,
                'total_changes': len(modified_files) + len(new_files) + len(deleted_files),
                'has_changes': bool(modified_files or new_files or deleted_files)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'git_status_timeout'}
        except Exception as e:
            self.logger.error(f"Git status check failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_intelligent_commit(self, commit_message: str, files: List[str] = None, 
                                metadata: Dict = None) -> Dict:
        """
        Create intelligent commit with metadata and optional file staging
        Phase 2: Enhanced with metadata-driven commit messages
        """
        try:
            # Stage files
            if files:
                for file_path in files:
                    add_result = subprocess.run(
                        ['git', 'add', file_path],
                        cwd=self.project_root,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if add_result.returncode != 0:
                        return {
                            'success': False,
                            'error': f'failed_to_stage_{file_path}',
                            'git_error': add_result.stderr
                        }
            else:
                # Stage all changes
                add_result = subprocess.run(
                    ['git', 'add', '.'],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if add_result.returncode != 0:
                    return {
                        'success': False,
                        'error': 'failed_to_stage_changes',
                        'git_error': add_result.stderr
                    }
            
            # Create commit with enhanced message
            enhanced_message = self._enhance_commit_message(commit_message, metadata)
            
            commit_result = subprocess.run(
                ['git', 'commit', '-m', enhanced_message],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if commit_result.returncode != 0:
                return {
                    'success': False,
                    'error': 'commit_failed',
                    'git_error': commit_result.stderr
                }
            
            # Extract commit hash
            commit_hash = self._extract_commit_hash(commit_result.stdout)
            
            # Record in session
            commit_record = {
                'hash': commit_hash,
                'message': enhanced_message,
                'files': files or [],
                'timestamp': datetime.now().isoformat() + 'Z',
                'metadata': metadata or {}
            }
            
            self.current_session['commits'].append(commit_record)
            if metadata:
                self.current_session['metadata_commits'] += 1
            
            self.logger.info(f"Created intelligent commit: {commit_hash[:8]} - {commit_message}")
            
            return {
                'success': True,
                'commit_hash': commit_hash,
                'commit_message': enhanced_message,
                'files_committed': files or [],
                'metadata_enhanced': bool(metadata)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'commit_timeout'}
        except Exception as e:
            self.logger.error(f"Commit creation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _enhance_commit_message(self, base_message: str, metadata: Dict = None) -> str:
        """Enhance commit message with metadata intelligence"""
        if not metadata:
            return base_message
        
        # Add metadata tags
        enhancements = []
        
        # Add rule information
        if 'rule_id' in metadata:
            enhancements.append(f"Rule:{metadata['rule_id']}")
        
        # Add confidence score
        if 'confidence' in metadata:
            confidence = metadata['confidence']
            if confidence > 0.9:
                enhancements.append("High-Confidence")
            elif confidence > 0.7:
                enhancements.append("Medium-Confidence")
        
        # Add tool information
        if 'tool_used' in metadata:
            enhancements.append(f"Tool:{metadata['tool_used']}")
        
        # Add Echo signature
        enhancements.append("Echo-Autonomous")
        
        if enhancements:
            return f"{base_message} [{', '.join(enhancements)}]"
        
        return base_message
    
    def _extract_commit_hash(self, commit_output: str) -> str:
        """Extract commit hash from git commit output"""
        # Look for pattern like [main 1234567] message
        import re
        match = re.search(r'\[.*?\s+([a-f0-9]{7,})\]', commit_output)
        if match:
            return match.group(1)
        
        # Fallback: get latest commit hash
        try:
            hash_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if hash_result.returncode == 0:
                return hash_result.stdout.strip()[:8]
        except:
            pass
        
        return 'unknown'
    
    def create_branch(self, branch_name: str, switch_to_branch: bool = True) -> Dict:
        """Create a new Git branch for isolated development"""
        try:
            # Create branch
            create_result = subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if create_result.returncode != 0:
                return {
                    'success': False,
                    'error': 'branch_creation_failed',
                    'git_error': create_result.stderr
                }
            
            # Record in session
            self.current_session['branches_created'].append({
                'name': branch_name,
                'created_at': datetime.now().isoformat() + 'Z',
                'switched': switch_to_branch
            })
            
            self.logger.info(f"Created branch: {branch_name}")
            
            return {
                'success': True,
                'branch_name': branch_name,
                'switched': switch_to_branch
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'branch_creation_timeout'}
        except Exception as e:
            self.logger.error(f"Branch creation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def read_diff(self, file_path: str = None, staged: bool = False) -> Dict:
        """Read Git diff with intelligent analysis"""
        try:
            # Build diff command
            cmd = ['git', 'diff']
            if staged:
                cmd.append('--staged')
            if file_path:
                cmd.append(file_path)
            
            diff_result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if diff_result.returncode != 0:
                return {
                    'success': False,
                    'error': 'diff_failed',
                    'git_error': diff_result.stderr
                }
            
            diff_content = diff_result.stdout
            
            if not diff_content.strip():
                return {
                    'success': True,
                    'has_changes': False,
                    'message': 'No changes found'
                }
            
            # Analyze diff content
            diff_analysis = self._analyze_diff_content(diff_content)
            
            return {
                'success': True,
                'has_changes': True,
                'diff_content': diff_content,
                'analysis': diff_analysis,
                'file_path': file_path,
                'staged': staged
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'diff_timeout'}
        except Exception as e:
            self.logger.error(f"Diff read failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_diff_content(self, diff_content: str) -> Dict:
        """Analyze diff content for intelligent insights"""
        lines = diff_content.split('\n')
        
        analysis = {
            'files_changed': 0,
            'lines_added': 0,
            'lines_removed': 0,
            'change_types': set(),
            'files': []
        }
        
        current_file = None
        
        for line in lines:
            # File header
            if line.startswith('diff --git'):
                parts = line.split()
                if len(parts) >= 4:
                    current_file = parts[3][2:]  # Remove 'b/' prefix
                    analysis['files'].append(current_file)
                    analysis['files_changed'] += 1
            
            # Change indicators
            elif line.startswith('+') and not line.startswith('+++'):
                analysis['lines_added'] += 1
                
                # Detect change types
                if 'import ' in line:
                    analysis['change_types'].add('import_changes')
                elif 'def ' in line or 'class ' in line:
                    analysis['change_types'].add('structure_changes')
                elif 'print(' in line or 'logger.' in line:
                    analysis['change_types'].add('debugging_changes')
                elif '#' in line:
                    analysis['change_types'].add('comment_changes')
                else:
                    analysis['change_types'].add('code_changes')
                    
            elif line.startswith('-') and not line.startswith('---'):
                analysis['lines_removed'] += 1
        
        analysis['change_types'] = list(analysis['change_types'])
        analysis['net_change'] = analysis['lines_added'] - analysis['lines_removed']
        analysis['change_magnitude'] = 'small' if analysis['lines_added'] + analysis['lines_removed'] < 10 else 'medium' if analysis['lines_added'] + analysis['lines_removed'] < 50 else 'large'
        
        return analysis
    
    def get_recent_commits(self, count: int = 10) -> Dict:
        """Get recent commits with metadata"""
        try:
            log_result = subprocess.run(
                ['git', 'log', f'-{count}', '--oneline', '--no-merges'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if log_result.returncode != 0:
                return {
                    'success': False,
                    'error': 'log_failed',
                    'git_error': log_result.stderr
                }
            
            commits = []
            for line in log_result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1],
                            'is_echo_commit': 'Echo-Autonomous' in parts[1]
                        })
            
            return {
                'success': True,
                'commits': commits,
                'total_commits': len(commits),
                'echo_commits': sum(1 for c in commits if c['is_echo_commit'])
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'log_timeout'}
        except Exception as e:
            self.logger.error(f"Commit log retrieval failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_session_summary(self) -> Dict:
        """Get summary of current Git session"""
        return {
            'commits_made': len(self.current_session['commits']),
            'metadata_enhanced_commits': self.current_session['metadata_commits'],
            'branches_created': len(self.current_session['branches_created']),
            'session_commits': self.current_session['commits'],
            'session_branches': self.current_session['branches_created']
        }
    
    def run(self, command: str, data: Dict = None) -> Dict:
        """
        Main entry point for EchoMind integration
        Phase 1: Simple command processing
        Phase 2: Metadata-enhanced Git operations
        """
        if data is None:
            data = {}
        
        try:
            if command == 'status':
                return self.get_git_status()
                
            elif command == 'commit':
                message = data.get('message', 'Echo autonomous commit')
                files = data.get('files')
                metadata = data.get('metadata')
                return self.create_intelligent_commit(message, files, metadata)
                
            elif command == 'create_branch':
                branch_name = data.get('branch_name', f'echo-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
                switch = data.get('switch', True)
                return self.create_branch(branch_name, switch)
                
            elif command == 'diff':
                file_path = data.get('file_path')
                staged = data.get('staged', False)
                return self.read_diff(file_path, staged)
                
            elif command == 'recent_commits':
                count = data.get('count', 10)
                return self.get_recent_commits(count)
                
            elif command == 'session_summary':
                return {'success': True, 'summary': self.get_session_summary()}
                
            else:
                return {'success': False, 'error': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"GitConnector run failed: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """CLI interface for testing GitConnector"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitConnector - Phase 1 Git Integration")
    parser.add_argument('--project', default='.', help='Project root directory')
    parser.add_argument('--status', action='store_true', help='Show Git status')
    parser.add_argument('--commit', help='Create commit with message')
    parser.add_argument('--diff', action='store_true', help='Show Git diff')
    parser.add_argument('--recent', type=int, default=5, help='Show recent commits')
    
    args = parser.parse_args()
    
    git_connector = GitConnector(args.project)
    
    if args.status:
        result = git_connector.get_git_status()
        print(f"Git Status: {json.dumps(result, indent=2)}")
        return 0
    
    if args.commit:
        result = git_connector.create_intelligent_commit(args.commit)
        print(f"Commit Result: {json.dumps(result, indent=2)}")
        return 0
    
    if args.diff:
        result = git_connector.read_diff()
        print(f"Git Diff: {json.dumps(result, indent=2)}")
        return 0
    
    if args.recent:
        result = git_connector.get_recent_commits(args.recent)
        print(f"Recent Commits: {json.dumps(result, indent=2)}")
        return 0
    
    print("GitConnector Phase 1 ready. Use --help for options.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
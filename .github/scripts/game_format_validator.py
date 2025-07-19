#!/usr/bin/env python3
"""
Advanced Game Format Validator
Surgical analysis to ensure AGI creates only game applications
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

class GameFormatValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.game_keywords = {
            'required': {
                'game_engine': ['pygame', 'arcade', 'godot', 'unity', 'panda3d', 'love2d', 'phaser'],
                'game_loop': ['game_loop', 'main_loop', 'run', 'update', 'tick'],
                'player_input': ['pygame.event', 'input', 'keyboard', 'mouse', 'controller'],
                'graphics': ['render', 'draw', 'display', 'screen', 'surface', 'sprite'],
                'game_objects': ['player', 'enemy', 'bullet', 'collectible', 'powerup']
            },
            'forbidden': {
                'web_frameworks': ['flask', 'django', 'fastapi', 'tornado', 'bottle'],
                'database': ['sqlalchemy', 'psycopg2', 'mysql', 'mongodb', 'sqlite3'],
                'api_patterns': ['@app.route', '@router', 'app.listen', 'server.listen'],
                'business_logic': ['invoice', 'payment', 'customer', 'order', 'billing']
            }
        }
    
    def validate_file_structure(self) -> bool:
        """Validate that project has proper game development structure"""
        print("🎮 Validating file structure...")
        
        # Check for main game file
        main_files = ['main.py', 'game.py', 'app.py', 'run.py']
        found_main = False
        
        for main_file in main_files:
            if os.path.exists(main_file):
                print(f"✅ Found main game file: {main_file}")
                found_main = True
                break
        
        if not found_main:
            self.errors.append("No main game file found (main.py, game.py, app.py, or run.py)")
            return False
        
        return True
    
    def analyze_python_file(self, filepath: str) -> Dict:
        """Analyze Python file for game development patterns"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            analysis = {
                'imports': [],
                'classes': [],
                'functions': [],
                'game_patterns': [],
                'forbidden_patterns': []
            }
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
            
            # Check for game patterns in content
            content_lower = content.lower()
            
            # Game patterns
            for category, keywords in self.game_keywords['required'].items():
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        analysis['game_patterns'].append(f"{category}:{keyword}")
            
            # Forbidden patterns
            for category, keywords in self.game_keywords['forbidden'].items():
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        analysis['forbidden_patterns'].append(f"{category}:{keyword}")
            
            return analysis
            
        except Exception as e:
            self.warnings.append(f"Could not analyze {filepath}: {e}")
            return {}
    
    def validate_game_patterns(self) -> bool:
        """Validate that code contains required game development patterns"""
        print("🎯 Validating game development patterns...")
        
        python_files = list(Path('.').glob('**/*.py'))
        if not python_files:
            self.errors.append("No Python files found")
            return False
        
        all_patterns = []
        all_forbidden = []
        
        for py_file in python_files:
            if '.venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            analysis = self.analyze_python_file(str(py_file))
            all_patterns.extend(analysis.get('game_patterns', []))
            all_forbidden.extend(analysis.get('forbidden_patterns', []))
        
        # Check required patterns
        required_categories = ['game_engine', 'game_loop', 'player_input', 'graphics']
        found_categories = set()
        
        for pattern in all_patterns:
            category = pattern.split(':')[0]
            found_categories.add(category)
        
        missing_categories = set(required_categories) - found_categories
        if missing_categories:
            for category in missing_categories:
                self.errors.append(f"Missing required game pattern: {category}")
        
        # Check forbidden patterns
        if all_forbidden:
            for pattern in all_forbidden:
                self.errors.append(f"Forbidden non-game pattern detected: {pattern}")
        
        if not missing_categories and not all_forbidden:
            print("✅ All required game patterns found, no forbidden patterns detected")
            return True
        
        return False
    
    def validate_game_loop_structure(self) -> bool:
        """Validate that code contains proper game loop structure"""
        print("🔄 Validating game loop structure...")
        
        python_files = list(Path('.').glob('**/*.py'))
        game_loop_found = False
        
        for py_file in python_files:
            if '.venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for game loop patterns
                game_loop_patterns = [
                    r'while.*running',
                    r'while.*True',
                    r'def.*game_loop',
                    r'def.*main_loop',
                    r'def.*run\(',
                    r'\.tick\(',
                    r'\.flip\(',
                    r'\.update\('
                ]
                
                for pattern in game_loop_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        game_loop_found = True
                        print(f"✅ Game loop pattern found in {py_file}")
                        break
                
                if game_loop_found:
                    break
                    
            except Exception as e:
                self.warnings.append(f"Could not check game loop in {py_file}: {e}")
        
        if not game_loop_found:
            self.errors.append("No game loop structure found (while loop, game_loop(), or update cycle)")
            return False
        
        return True
    
    def validate_interactive_elements(self) -> bool:
        """Validate that game has interactive user input"""
        print("🕹️ Validating interactive elements...")
        
        python_files = list(Path('.').glob('**/*.py'))
        interactive_found = False
        
        for py_file in python_files:
            if '.venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for input handling patterns
                input_patterns = [
                    r'pygame\.event',
                    r'pygame\.key',
                    r'pygame\.mouse',
                    r'keyboard',
                    r'input\(',
                    r'get_pressed\(',
                    r'event\.type',
                    r'KEY_.*',
                    r'MOUSE_.*'
                ]
                
                for pattern in input_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        interactive_found = True
                        print(f"✅ Interactive input found in {py_file}")
                        break
                
                if interactive_found:
                    break
                    
            except Exception as e:
                self.warnings.append(f"Could not check input handling in {py_file}: {e}")
        
        if not interactive_found:
            self.errors.append("No interactive input handling found (games must respond to user input)")
            return False
        
        return True
    
    def generate_report(self) -> bool:
        """Generate validation report"""
        print("\n" + "="*60)
        print("🎮 GAME FORMAT VALIDATION REPORT")
        print("="*60)
        
        if not self.errors:
            print("✅ VALIDATION PASSED - Project follows game development format!")
            print("\n🎯 Detected game elements:")
            print("- Game engine or framework usage")
            print("- Proper game loop structure")
            print("- Interactive user input handling")
            print("- Graphics rendering capability")
            print("- No forbidden non-game patterns")
            return True
        else:
            print("❌ VALIDATION FAILED - Project does not follow game format!")
            print("\n🚫 Errors found:")
            for error in self.errors:
                print(f"  • {error}")
            
            if self.warnings:
                print("\n⚠️ Warnings:")
                for warning in self.warnings:
                    print(f"  • {warning}")
            
            print("\n📖 To fix these issues:")
            print("1. Ensure your project uses a game engine (pygame, arcade, etc.)")
            print("2. Implement a proper game loop with update/render cycle")
            print("3. Add interactive input handling (keyboard, mouse)")
            print("4. Remove any web frameworks, APIs, or business logic")
            print("5. Focus on game mechanics, graphics, and player interaction")
            
            return False
    
    def validate(self) -> bool:
        """Run complete game format validation"""
        print("🔬 Starting comprehensive game format validation...")
        print("-" * 50)
        
        validations = [
            self.validate_file_structure,
            self.validate_game_patterns,
            self.validate_game_loop_structure,
            self.validate_interactive_elements
        ]
        
        all_passed = True
        for validation in validations:
            if not validation():
                all_passed = False
        
        return self.generate_report() and all_passed

def main():
    """Main validation entry point"""
    validator = GameFormatValidator()
    
    if validator.validate():
        print("\n🎉 Game format validation successful!")
        sys.exit(0)
    else:
        print("\n💥 Game format validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
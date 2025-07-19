#!/usr/bin/env python3
"""
AGI Game Developer Persona Framework
Specialized training system to constrain AGI to game development format exclusively
"""

import os
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class GameDeveloperPersona:
    """
    Specialized AGI persona that thinks exclusively in game development terms
    Implements role-based constraints and positive reinforcement patterns
    """
    
    def __init__(self):
        self.persona_config = {
            "identity": "Highly Specialized AGI Game Developer",
            "purpose": "Create, debug, and maintain applications that are exclusively games",
            "core_principles": [
                "Every application must be playable and interactive",
                "All responses must adhere to game development conventions",
                "Game loops, asset management, and user input are mandatory",
                "Entertainment value and player experience are primary goals"
            ],
            "required_frameworks": [
                "Pygame", "Arcade", "Pygame Zero", "Panda3D", 
                "Unity", "Godot", "Love2D", "Phaser", "Three.js"
            ],
            "forbidden_patterns": [
                "Web servers", "REST APIs", "Database applications",
                "Business software", "Data analysis", "System utilities"
            ],
            "vocabulary_mapping": {
                "images": "sprites",
                "entities": "game objects", 
                "user input handler": "player controller",
                "page": "level/scene",
                "application controller": "game manager",
                "file management": "asset pipeline",
                "intersection testing": "collision detection",
                "refresh rate": "frame rate"
            }
        }
        
        self.training_prompts = self._load_training_prompts()
        self.validation_rules = self._load_validation_rules()
        
    def _load_training_prompts(self) -> List[str]:
        """Load specialized training prompts for game development focus"""
        return [
            "You are now a highly specialized AGI game developer. Your purpose is to create, debug, and maintain applications that are exclusively games.",
            
            "When creating a project, you must use a game engine or game development-focused framework (e.g., Pygame, Unity, Godot).",
            
            "Every application must have: a game loop, a player input system, and a system for rendering graphics to the screen.",
            
            "Think in terms of game mechanics: players, enemies, levels, scoring, power-ups, and interactive experiences.",
            
            "Your responses must always include game development vocabulary: sprites, game objects, collision detection, frame rate, asset pipeline.",
            
            "Focus on entertainment value, player engagement, and interactive experiences rather than utility or business applications.",
            
            "When debugging, consider game-specific issues: frame rate drops, input lag, collision bugs, sprite rendering problems.",
            
            "Structure your code with game development patterns: game loops, state machines, component systems, event handling."
        ]
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules for game format enforcement"""
        return {
            "required_imports": [
                "pygame", "arcade", "godot", "unity", "panda3d", 
                "love2d", "phaser", "threejs"
            ],
            "required_functions": [
                "game_loop", "main_loop", "update", "render", "handle_input"
            ],
            "required_classes": [
                "Game", "Player", "Enemy", "Sprite", "GameObject", "Scene"
            ],
            "required_keywords": [
                "collision", "sprite", "texture", "frame_rate", "input",
                "render", "player", "enemy", "level", "score"
            ],
            "forbidden_imports": [
                "flask", "django", "fastapi", "sqlalchemy", "requests",
                "pandas", "numpy", "matplotlib", "seaborn"
            ],
            "forbidden_patterns": [
                "@app.route", "CREATE TABLE", "SELECT *", "INSERT INTO",
                "app.listen", "server.listen", "api.get", "api.post"
            ]
        }
    
    def apply_persona_constraints(self, prompt: str) -> str:
        """Apply game developer persona constraints to any prompt"""
        
        # Prepend game developer identity
        constrained_prompt = f"""
{self.training_prompts[0]}

{self.training_prompts[1]}

{self.training_prompts[2]}

Original request: {prompt}

Remember: Your response must follow game development conventions. Use game terminology, focus on interactive experiences, and ensure any code you write is for a playable game application.
"""
        
        return constrained_prompt
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """Validate that response follows game development format"""
        
        validation_result = {
            "valid": True,
            "score": 0,
            "issues": [],
            "recommendations": []
        }
        
        response_lower = response.lower()
        
        # Check for required game development elements
        game_elements_found = 0
        for keyword in self.validation_rules["required_keywords"]:
            if keyword in response_lower:
                game_elements_found += 1
                validation_result["score"] += 10
        
        if game_elements_found < 3:
            validation_result["issues"].append(
                f"Insufficient game development vocabulary (found {game_elements_found}, need at least 3)"
            )
            validation_result["valid"] = False
        
        # Check for forbidden patterns
        forbidden_found = []
        for pattern in self.validation_rules["forbidden_patterns"]:
            if pattern.lower() in response_lower:
                forbidden_found.append(pattern)
        
        if forbidden_found:
            validation_result["issues"].append(
                f"Forbidden non-game patterns detected: {', '.join(forbidden_found)}"
            )
            validation_result["valid"] = False
        
        # Check for game framework mentions
        framework_found = False
        for framework in self.validation_rules["required_imports"]:
            if framework in response_lower:
                framework_found = True
                validation_result["score"] += 20
                break
        
        if not framework_found:
            validation_result["recommendations"].append(
                "Consider mentioning a specific game framework (Pygame, Arcade, etc.)"
            )
        
        # Check for game loop structure
        if any(term in response_lower for term in ["game_loop", "main_loop", "while", "update"]):
            validation_result["score"] += 15
        else:
            validation_result["recommendations"].append(
                "Include game loop structure in your implementation"
            )
        
        return validation_result
    
    def generate_game_prompt_enhancement(self, original_prompt: str) -> str:
        """Enhance any prompt to focus on game development"""
        
        # Analyze original prompt
        prompt_lower = original_prompt.lower()
        
        # Map non-game concepts to game concepts
        enhanced_prompt = original_prompt
        for non_game_term, game_term in self.persona_config["vocabulary_mapping"].items():
            enhanced_prompt = enhanced_prompt.replace(non_game_term, game_term)
        
        # Add game development context
        game_context = """

Game Development Context:
- Focus on creating an interactive, playable experience
- Use appropriate game engines (Pygame, Arcade, Unity, Godot)
- Implement proper game loop with update/render cycle
- Include player input handling and collision detection
- Consider entertainment value and player engagement
- Structure code using game development patterns

"""
        
        return enhanced_prompt + game_context
    
    def get_specialized_templates(self) -> Dict[str, str]:
        """Get game-specific code templates"""
        
        return {
            "basic_game_structure": '''
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        # Game logic here
        pass
    
    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
    
    def game_loop(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
''',
            
            "player_class": '''
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.rect = pygame.Rect(x, y, 32, 32)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        self.rect.center = (self.x, self.y)
    
    def update(self):
        self.handle_input()
    
    def render(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
''',
            
            "game_state_manager": '''
from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class GameStateManager:
    def __init__(self):
        self.current_state = GameState.MENU
        self.states = {}
    
    def add_state(self, state, handler):
        self.states[state] = handler
    
    def change_state(self, new_state):
        self.current_state = new_state
    
    def update(self):
        if self.current_state in self.states:
            self.states[self.current_state].update()
    
    def render(self, screen):
        if self.current_state in self.states:
            self.states[self.current_state].render(screen)
'''
        }
    
    def log_persona_activity(self, activity_type: str, details: Dict[str, Any]):
        """Log persona framework activity for monitoring"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "activity_type": activity_type,
            "details": details,
            "persona_version": "1.0"
        }
        
        # Log to file for analysis
        log_file = "game_persona_activity.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

class GameFormatEnforcer:
    """
    Advanced enforcement system for game development format
    Implements automated validation and correction
    """
    
    def __init__(self):
        self.persona = GameDeveloperPersona()
        self.enforcement_level = "strict"  # strict, moderate, lenient
        
    def enforce_game_format(self, code: str) -> Dict[str, Any]:
        """Enforce game development format on code"""
        
        enforcement_result = {
            "original_code": code,
            "corrected_code": code,
            "corrections_made": [],
            "validation_passed": False
        }
        
        # Validate current code
        validation = self.persona.validate_response(code)
        
        if not validation["valid"]:
            # Apply corrections
            corrected_code = self._apply_corrections(code, validation["issues"])
            enforcement_result["corrected_code"] = corrected_code
            enforcement_result["corrections_made"] = validation["issues"]
            
            # Re-validate
            revalidation = self.persona.validate_response(corrected_code)
            enforcement_result["validation_passed"] = revalidation["valid"]
        else:
            enforcement_result["validation_passed"] = True
        
        return enforcement_result
    
    def _apply_corrections(self, code: str, issues: List[str]) -> str:
        """Apply automatic corrections to make code game-compliant"""
        
        corrected_code = code
        
        # Add pygame import if missing
        if "import pygame" not in corrected_code and "from pygame" not in corrected_code:
            corrected_code = "import pygame\nimport sys\n\n" + corrected_code
        
        # Add basic game structure if missing
        if "class Game" not in corrected_code and "def game_loop" not in corrected_code:
            game_template = self.persona.get_specialized_templates()["basic_game_structure"]
            corrected_code += "\n\n" + game_template
        
        return corrected_code

def main():
    """Demonstration of game developer persona framework"""
    
    print("🎮 Game Developer Persona Framework")
    print("=" * 50)
    
    persona = GameDeveloperPersona()
    enforcer = GameFormatEnforcer()
    
    # Test prompt enhancement
    original_prompt = "Create an application that processes user input and displays results"
    enhanced_prompt = persona.apply_persona_constraints(original_prompt)
    
    print("Original prompt:", original_prompt)
    print("\nEnhanced prompt:", enhanced_prompt[:200] + "...")
    
    # Test validation
    test_code = """
import pygame

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 5

def game_loop():
    running = True
    while running:
        # Game logic
        pass
"""
    
    validation_result = persona.validate_response(test_code)
    print(f"\nValidation result: {validation_result}")
    
    print("\n✅ Game Developer Persona Framework initialized successfully!")

if __name__ == "__main__":
    main()
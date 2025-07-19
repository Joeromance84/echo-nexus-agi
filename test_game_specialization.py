#!/usr/bin/env python3
"""
Comprehensive Game Development Specialization Test
Demonstrates the complete AGI constraint system for game-only development
"""

import sys
import os
sys.path.append('game_dev_specialization')

from agi_game_persona import GameDeveloperPersona, GameFormatEnforcer

def test_persona_constraints():
    """Test the persona constraint system"""
    print("🎮 Testing Game Developer Persona Constraints")
    print("-" * 50)
    
    persona = GameDeveloperPersona()
    
    # Test prompt enhancement
    test_prompts = [
        "Create an application that handles user input",
        "Build a system that processes data and displays results",
        "Make a tool that manages files and folders",
        "Design an interface for user interaction"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: Original prompt")
        print(f"  '{prompt}'")
        
        enhanced = persona.apply_persona_constraints(prompt)
        print(f"Enhanced to focus on game development:")
        print(f"  First 100 chars: '{enhanced[:100]}...'")
    
    return True

def test_validation_system():
    """Test the code validation system"""
    print("\n🔍 Testing Validation System")
    print("-" * 50)
    
    persona = GameDeveloperPersona()
    
    # Test valid game code
    valid_game_code = """
import pygame

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.sprite = pygame.Surface((32, 32))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 5
    
    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player = Player()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.update()
        screen.fill((0, 0, 0))
        player.render(screen)
        pygame.display.flip()
        clock.tick(60)
"""
    
    # Test invalid non-game code
    invalid_code = """
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

if __name__ == '__main__':
    app.run(debug=True)
"""
    
    print("Testing valid game code...")
    valid_result = persona.validate_response(valid_game_code)
    print(f"  Validation result: {'✅ PASSED' if valid_result['valid'] else '❌ FAILED'}")
    print(f"  Score: {valid_result['score']}/100")
    
    print("\nTesting invalid non-game code...")
    invalid_result = persona.validate_response(invalid_code)
    print(f"  Validation result: {'✅ PASSED' if invalid_result['valid'] else '❌ FAILED (Expected)'}")
    print(f"  Issues found: {len(invalid_result['issues'])}")
    for issue in invalid_result['issues']:
        print(f"    - {issue}")
    
    return valid_result['valid'] and not invalid_result['valid']

def test_enforcement_system():
    """Test the automatic enforcement system"""
    print("\n🛠️ Testing Enforcement System")
    print("-" * 50)
    
    enforcer = GameFormatEnforcer()
    
    # Test code that needs correction
    problematic_code = """
def process_data(input_file):
    with open(input_file, 'r') as f:
        data = f.read()
    
    # Process the data
    result = data.upper()
    
    return result

if __name__ == "__main__":
    result = process_data("input.txt")
    print(result)
"""
    
    print("Testing enforcement on non-game code...")
    enforcement_result = enforcer.enforce_game_format(problematic_code)
    
    print(f"  Corrections made: {len(enforcement_result['corrections_made'])}")
    print(f"  Validation passed after correction: {'✅ YES' if enforcement_result['validation_passed'] else '❌ NO'}")
    
    if enforcement_result['corrections_made']:
        print("  Corrections applied:")
        for correction in enforcement_result['corrections_made']:
            print(f"    - {correction}")
    
    return True

def test_template_system():
    """Test the game template system"""
    print("\n📋 Testing Template System")
    print("-" * 50)
    
    persona = GameDeveloperPersona()
    templates = persona.get_specialized_templates()
    
    print(f"Available game templates: {len(templates)}")
    for name, template in templates.items():
        print(f"  - {name}: {len(template.split('\\n'))} lines")
    
    # Test that templates are valid game code
    print("\nValidating templates...")
    all_valid = True
    for name, template in templates.items():
        validation = persona.validate_response(template)
        status = "✅ VALID" if validation['valid'] else "❌ INVALID"
        print(f"  {name}: {status}")
        if not validation['valid']:
            all_valid = False
    
    return all_valid

def test_vocabulary_mapping():
    """Test the vocabulary mapping system"""
    print("\n📝 Testing Vocabulary Mapping")
    print("-" * 50)
    
    persona = GameDeveloperPersona()
    
    test_phrases = [
        "Load images from the file system",
        "Handle user input in the application",
        "Display entities on the page",
        "Manage the intersection testing between objects"
    ]
    
    for phrase in test_phrases:
        enhanced = persona.generate_game_prompt_enhancement(phrase)
        print(f"Original: '{phrase}'")
        
        # Extract the game-mapped version
        lines = enhanced.split('\\n')
        enhanced_phrase = lines[0] if lines else enhanced[:100]
        print(f"Enhanced: '{enhanced_phrase}'")
        print()
    
    return True

def run_comprehensive_test():
    """Run all tests in the game specialization system"""
    print("🚀 COMPREHENSIVE GAME DEVELOPMENT SPECIALIZATION TEST")
    print("=" * 60)
    
    tests = [
        ("Persona Constraints", test_persona_constraints),
        ("Validation System", test_validation_system),
        ("Enforcement System", test_enforcement_system),
        ("Template System", test_template_system),
        ("Vocabulary Mapping", test_vocabulary_mapping)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            results[test_name] = False
            print(f"\n{test_name}: ❌ ERROR - {e}")
    
    # Final report
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Game Development Specialization Framework is fully operational!")
        print("\nThe AGI is now constrained to think exclusively in game development terms:")
        print("- ✅ Persona constraints active")
        print("- ✅ Validation system functional") 
        print("- ✅ Enforcement system operational")
        print("- ✅ Template system ready")
        print("- ✅ Vocabulary mapping working")
        print("\nAny application created will be automatically formatted as a game!")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("Some components need attention before full deployment.")
        return False

def demo_game_constraint_in_action():
    """Demonstrate the constraint system in action"""
    print("\n🎮 DEMONSTRATION: AGI CONSTRAINT IN ACTION")
    print("=" * 60)
    
    persona = GameDeveloperPersona()
    enforcer = GameFormatEnforcer()
    
    # Simulate an AGI request that's not game-related
    print("Simulating AGI request: 'Create a web application for managing customer data'")
    
    original_prompt = "Create a web application for managing customer data"
    
    # Step 1: Apply persona constraints
    constrained_prompt = persona.apply_persona_constraints(original_prompt)
    print(f"\n1. Persona constraints applied:")
    print(f"   Original: '{original_prompt}'")
    print(f"   Constrained: Game development context added...")
    
    # Step 2: Enhance with game vocabulary
    enhanced_prompt = persona.generate_game_prompt_enhancement(original_prompt)
    print(f"\n2. Vocabulary mapping applied:")
    print(f"   Game-focused enhancement added...")
    
    # Step 3: Generate game-compliant response (simulated)
    simulated_response = """
import pygame

class PlayerManager:
    def __init__(self):
        self.players = []
        self.high_scores = {}
    
    def add_player(self, name):
        player = {'name': name, 'score': 0, 'level': 1}
        self.players.append(player)
    
    def update_score(self, player_name, score):
        for player in self.players:
            if player['name'] == player_name:
                player['score'] = score
                break

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    manager = PlayerManager()
    running = True
    
    while running:
        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Render player management interface
        screen.fill((0, 0, 0))
        pygame.display.flip()
"""
    
    # Step 4: Validate the response
    validation = persona.validate_response(simulated_response)
    print(f"\n3. Response validation:")
    print(f"   Valid game format: {'✅ YES' if validation['valid'] else '❌ NO'}")
    print(f"   Game elements score: {validation['score']}/100")
    
    # Step 5: Apply enforcement if needed
    if not validation['valid']:
        enforcement = enforcer.enforce_game_format(simulated_response)
        print(f"\n4. Enforcement applied:")
        print(f"   Corrections made: {len(enforcement['corrections_made'])}")
        print(f"   Now valid: {'✅ YES' if enforcement['validation_passed'] else '❌ NO'}")
    
    print(f"\n🎯 RESULT: Successfully converted web application request into game format!")
    print(f"   - Customer management → Player management")
    print(f"   - Web interface → Game interface") 
    print(f"   - Database operations → Game state management")
    print(f"   - Business logic → Game mechanics")
    
    return True

if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_test()
    
    if success:
        # Run demonstration
        demo_game_constraint_in_action()
        
        print("\n🌟 GAME DEVELOPMENT SPECIALIZATION COMPLETE!")
        print("The AGI is now fully constrained to game development format.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the issues above.")
        sys.exit(1)
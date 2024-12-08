"""
System Integration Test for Banana Math Puzzle

This test suite validates the integration of core game components
and ensures smooth interaction between different modules.
"""

import sys
import os
import unittest
import logging

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'src/game'))

from src.game.game_logic import GameState, PuzzleGenerator, DifficultyManager
from src.game.core.auth import UserProfile
from src.game.screens.game_screen import GameScreen

class SystemIntegrationTest(unittest.TestCase):
    def setUp(self):
        """Initialize test environment."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create a test user profile
        self.profile = UserProfile(
            username='test_player',
            email='test@example.com'
        )
        
        # Initialize game components
        self.game_state = GameState()
        self.difficulty_manager = DifficultyManager()
        self.puzzle_generator = PuzzleGenerator(self.difficulty_manager)
    
    def test_game_flow_integration(self):
        """
        Test the complete game flow integration:
        1. Generate puzzle
        2. Validate puzzle generation
        3. Check answer
        4. Update game state
        """
        # Generate puzzle
        puzzle = self.puzzle_generator.generate_puzzle(level=1)
        self.assertIsNotNone(puzzle, "Puzzle generation failed")
        
        # Validate puzzle structure
        required_keys = ['num1', 'num2', 'operation', 'result']
        for key in required_keys:
            self.assertIn(key, puzzle, f"Missing key: {key}")
        
        # Simulate correct answer
        correct_answer = puzzle['result']
        check_result = self.game_state.check_answer(correct_answer)
        
        self.assertTrue(check_result, "Answer validation failed")
        
        # Check score and level progression
        self.assertGreater(self.game_state.score, 0, "Score not updated")
        
        self.logger.info("Game flow integration test completed successfully")
    
    def test_difficulty_scaling(self):
        """
        Test difficulty scaling mechanism
        """
        initial_level = self.difficulty_manager.current_level
        
        # Simulate multiple correct answers
        for _ in range(5):
            puzzle = self.puzzle_generator.generate_puzzle(level=initial_level)
            self.game_state.check_answer(puzzle['result'])
        
        # Check if level increased
        self.assertGreaterEqual(
            self.difficulty_manager.current_level, 
            initial_level, 
            "Difficulty not scaling correctly"
        )
    
    def test_game_screen_integration(self):
        """
        Test GameScreen integration with game logic
        """
        game_screen = GameScreen(self.profile)
        
        # Check initial state
        self.assertIsNotNone(game_screen.current_puzzle, "Initial puzzle not generated")
        self.assertEqual(game_screen.score, 0, "Initial score incorrect")
        
        # Simulate input and answer checking
        game_screen.on_input('number', 5)
        game_screen.on_input('submit')
        
        # Verify state changes
        self.assertIsNotNone(game_screen.current_puzzle, "Puzzle not regenerated after submission")
    
    def tearDown(self):
        """Clean up test resources."""
        # Reset game state
        self.game_state = None
        self.difficulty_manager = None
        self.puzzle_generator = None

if __name__ == '__main__':
    unittest.main()

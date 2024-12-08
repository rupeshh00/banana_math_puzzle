"""Test configuration for the Banana Math Puzzle game."""

import os
import sys

# Add project root and src to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

import pytest

@pytest.fixture
def game_state():
    """Fixture providing a fresh GameState instance for each test."""
    from src.game.game_logic import GameState
    return GameState()

@pytest.fixture
def difficulty_manager():
    """Fixture providing a fresh DifficultyManager instance for each test."""
    from src.game.game_logic import DifficultyManager
    return DifficultyManager()

@pytest.fixture
def puzzle_generator(difficulty_manager):
    """Fixture providing a fresh PuzzleGenerator instance for each test."""
    from src.game.game_logic import PuzzleGenerator
    return PuzzleGenerator(difficulty_manager)

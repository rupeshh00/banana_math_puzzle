"""Unit tests for puzzle generation system."""

import pytest
from unittest.mock import patch, MagicMock
import operator

from src.game.core.puzzle_generator import PuzzleGenerator, PuzzleConfig
from src.game.core.base_errors import PuzzleGenerationError

@pytest.fixture
def puzzle_generator():
    """Create a fresh puzzle generator instance for each test."""
    PuzzleGenerator._instance = None
    return PuzzleGenerator()

def test_singleton_pattern(puzzle_generator):
    """Test that PuzzleGenerator follows singleton pattern."""
    generator2 = PuzzleGenerator()
    assert puzzle_generator is generator2

def test_puzzle_generation_basic(puzzle_generator):
    """Test basic puzzle generation."""
    puzzle = puzzle_generator.generate_puzzle('easy')
    
    assert isinstance(puzzle, dict)
    assert all(key in puzzle for key in [
        'expression', 'answer', 'difficulty', 'time_limit', 'points', 'hint'
    ])
    assert puzzle['difficulty'] == 'easy'
    assert isinstance(puzzle['answer'], float)

def test_puzzle_difficulty_configs(puzzle_generator):
    """Test puzzle generation for different difficulty levels."""
    for difficulty in ['easy', 'normal', 'hard']:
        puzzle = puzzle_generator.generate_puzzle(difficulty)
        config = puzzle_generator.DIFFICULTY_CONFIGS[difficulty]
        
        assert puzzle['difficulty'] == difficulty
        assert puzzle['time_limit'] == config.time_limit
        assert puzzle['points'] == config.points

def test_invalid_difficulty(puzzle_generator):
    """Test error handling for invalid difficulty."""
    with pytest.raises(PuzzleGenerationError) as exc_info:
        puzzle_generator.generate_puzzle('invalid')
    assert 'Invalid difficulty level' in str(exc_info.value)

def test_expression_generation(puzzle_generator):
    """Test mathematical expression generation."""
    config = PuzzleConfig(
        min_number=1,
        max_number=10,
        operations=['+', '-'],
        steps=1,
        time_limit=30,
        points=10
    )
    
    expression, answer = puzzle_generator._generate_expression(config)
    
    assert isinstance(expression, str)
    assert isinstance(answer, float)
    # Verify expression format (number operator number)
    parts = expression.split()
    assert len(parts) == 3
    assert parts[1] in ['+', '-']
    assert all(part.replace('.', '').isdigit() for part in [parts[0], parts[2]])

def test_division_handling(puzzle_generator):
    """Test division operation generates whole number results."""
    config = PuzzleConfig(
        min_number=1,
        max_number=50,
        operations=['/'],
        steps=1,
        time_limit=30,
        points=10
    )
    
    expression, answer = puzzle_generator._generate_expression(config)
    assert answer.is_integer()

def test_find_divisor(puzzle_generator):
    """Test finding suitable divisors."""
    divisor = puzzle_generator._find_divisor(12)
    assert 12 % divisor == 0
    assert divisor != 0

def test_hint_generation(puzzle_generator):
    """Test hint generation."""
    hint = puzzle_generator._generate_hint("5 + 3", 8.0)
    assert isinstance(hint, str)
    assert len(hint) > 0

def test_difficulty_adjustment(puzzle_generator):
    """Test difficulty adjustment based on success rate."""
    # Test increasing difficulty
    puzzle_generator._current_difficulty = 'easy'
    puzzle_generator.adjust_difficulty(0.9)  # 90% success rate
    assert puzzle_generator._current_difficulty == 'normal'
    
    puzzle_generator._current_difficulty = 'normal'
    puzzle_generator.adjust_difficulty(0.9)
    assert puzzle_generator._current_difficulty == 'hard'
    
    # Test decreasing difficulty
    puzzle_generator._current_difficulty = 'hard'
    puzzle_generator.adjust_difficulty(0.3)  # 30% success rate
    assert puzzle_generator._current_difficulty == 'normal'
    
    puzzle_generator._current_difficulty = 'normal'
    puzzle_generator.adjust_difficulty(0.3)
    assert puzzle_generator._current_difficulty == 'easy'

def test_answer_verification(puzzle_generator):
    """Test answer verification."""
    puzzle = {
        'expression': '5 + 3',
        'answer': 8.0
    }
    
    with patch('src.game.core.game_state.GameState.update_statistics') as mock_update:
        # Test correct answer
        assert puzzle_generator.verify_answer(puzzle, 8.0) is True
        mock_update.assert_called_with('correct_answers')
        
        # Test incorrect answer
        assert puzzle_generator.verify_answer(puzzle, 7.0) is False
        mock_update.assert_called_with('wrong_answers')
        
        # Test floating point tolerance
        assert puzzle_generator.verify_answer(puzzle, 8.0000001) is True

def test_error_handling(puzzle_generator):
    """Test error handling in puzzle operations."""
    # Test expression generation error
    with patch('random.randint', side_effect=Exception('Random error')):
        with pytest.raises(PuzzleGenerationError) as exc_info:
            puzzle_generator.generate_puzzle()
        assert 'Failed to generate puzzle' in str(exc_info.value)
    
    # Test answer verification error
    with patch('src.game.core.game_state.GameState.update_statistics',
              side_effect=Exception('Stats error')):
        with pytest.raises(PuzzleGenerationError) as exc_info:
            puzzle_generator.verify_answer({'answer': 5}, 5)
        assert 'Failed to verify answer' in str(exc_info.value)

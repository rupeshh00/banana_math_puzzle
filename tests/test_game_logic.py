"""Unit tests for game logic module."""

import pytest
from unittest.mock import Mock, patch
from src.game.game_logic import PuzzleGenerator, GameState, DifficultyManager
from src.game.puzzle_validators import PuzzleValidator, NumberValidationResult
from src.game.error_handling import (
    GameplayError, 
    InvalidMoveError, 
    OutOfResourcesError
)

class TestPuzzleGenerator:
    """Test cases for the PuzzleGenerator class."""

    def test_puzzle_generation(self):
        """Test puzzle generation for different operations."""
        difficulty_manager = DifficultyManager()
        puzzle_generator = PuzzleGenerator(difficulty_manager)
        
        operations = ['+', '-', '*', '/']
        for operation in operations:
            puzzle = puzzle_generator.generate_puzzle(operation)
            
            assert 'numbers' in puzzle
            assert 'operation' in puzzle
            assert 'result' in puzzle
            assert len(puzzle['numbers']) == 2
            assert puzzle['operation'] == operation

    def test_puzzle_validation(self):
        """Test puzzle validation."""
        difficulty_manager = DifficultyManager()
        puzzle_generator = PuzzleGenerator(difficulty_manager)
        
        puzzle = puzzle_generator.generate_puzzle('+')
        
        correct_answer = str(puzzle['result'])
        assert puzzle_generator.validate_answer(puzzle, correct_answer) is True
        
        incorrect_answer = str(puzzle['result'] + 1)
        assert puzzle_generator.validate_answer(puzzle, incorrect_answer) is False

class TestPuzzleValidator:
    """Test cases for the PuzzleValidator class."""

    def test_puzzle_validator(self):
        """Test number validation."""
        valid_cases = [
            ([5, 3], '+', NumberValidationResult.VALID),
            ([10, 2], '/', NumberValidationResult.VALID),
        ]
        
        for numbers, operation, expected_result in valid_cases:
            validation, error = PuzzleValidator.validate_numbers(numbers, operation)
            assert validation == expected_result
            assert error is None

    def test_result_calculation(self):
        """Test result calculation."""
        test_cases = [
            ([5, 3], '+', 8),
            ([10, 2], '/', 5),
            ([4, 3], '*', 12),
            ([7, 2], '-', 5)
        ]
        
        for numbers, operation, expected_result in test_cases:
            result = PuzzleValidator.calculate_result(numbers, operation)
            assert result == expected_result

class TestGameState:
    """Test cases for the GameState class."""

    @pytest.fixture
    def mock_auth_manager(self):
        """Create a mock authentication manager."""
        mock_user = Mock()
        mock_user.id = "test_user"
        
        mock_auth = Mock()
        mock_auth.current_user = mock_user
        return mock_auth

    @pytest.fixture
    def mock_difficulty_manager(self):
        """Create a mock difficulty manager."""
        mock_difficulty = Mock()
        mock_difficulty.current_level = 1
        mock_difficulty.get_difficulty_params.return_value = '+'
        return mock_difficulty

    def test_game_state_initialization(self, mock_auth_manager, mock_difficulty_manager):
        """Test game state initialization with mocked dependencies."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        
        assert game_state.auth_manager == mock_auth_manager
        assert game_state.difficulty_manager == mock_difficulty_manager

    def test_new_puzzle_generation(self, mock_auth_manager, mock_difficulty_manager):
        """Test new puzzle generation with comprehensive checks."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        
        with patch.object(game_state.puzzle_generator, 'generate_puzzle') as mock_generate:
            mock_puzzle = {
                'numbers': [5, 3],
                'operation': '+',
                'result': 8,
                'id': 'test_puzzle_1'
            }
            mock_generate.return_value = mock_puzzle
            
            puzzle = game_state.new_puzzle()
            
            assert puzzle == mock_puzzle
            mock_generate.assert_called_once_with('+')

    def test_new_puzzle_generation_failure(self, mock_auth_manager, mock_difficulty_manager):
        """Test puzzle generation failure scenario."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        
        with patch.object(game_state.puzzle_generator, 'generate_puzzle') as mock_generate:
            mock_generate.side_effect = Exception("Puzzle generation failed")
            
            with pytest.raises(OutOfResourcesError) as exc_info:
                game_state.new_puzzle()
            
            assert "Failed to generate puzzle" in str(exc_info.value)

    def test_answer_validation_correct(self, mock_auth_manager, mock_difficulty_manager):
        """Test correct answer validation."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        
        # Simulate current puzzle
        game_state.current_puzzle = {
            'numbers': [5, 3],
            'operation': '+',
            'result': 8
        }
        
        with patch.object(game_state.puzzle_generator, 'validate_answer') as mock_validate:
            mock_validate.return_value = True
            
            result = game_state.check_answer('8')
            
            assert result is True
            mock_validate.assert_called_once_with(game_state.current_puzzle, '8')

    def test_answer_validation_incorrect(self, mock_auth_manager, mock_difficulty_manager):
        """Test incorrect answer validation."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        
        # Simulate current puzzle
        game_state.current_puzzle = {
            'numbers': [5, 3],
            'operation': '+',
            'result': 8
        }
        
        with patch.object(game_state.puzzle_generator, 'validate_answer') as mock_validate:
            mock_validate.return_value = False
            
            with pytest.raises(InvalidMoveError) as exc_info:
                game_state.check_answer('10')
            
            assert "Incorrect answer" in str(exc_info.value)
            mock_validate.assert_called_once_with(game_state.current_puzzle, '10')

    def test_no_active_puzzle(self, mock_auth_manager, mock_difficulty_manager):
        """Test answer validation without an active puzzle."""
        game_state = GameState(mock_auth_manager, mock_difficulty_manager)
        game_state.current_puzzle = None
        
        with pytest.raises(GameplayError) as exc_info:
            game_state.check_answer('8')
        
        assert "No active puzzle" in str(exc_info.value)

    def test_init(self, game_state):
        """Test game state initialization."""
        assert game_state.score == 0
        assert game_state.level == 1
        assert game_state.hints_remaining == 3

    def test_new_puzzle(self, game_state):
        """Test new puzzle generation."""
        puzzle = game_state.new_puzzle()
        assert game_state.current_puzzle is not None
        assert 'numbers' in puzzle
        assert 'operation' in puzzle
        assert 'result' in puzzle

    def test_check_answer_correct(self, game_state):
        """Test checking a correct answer."""
        game_state.current_puzzle = {
            'numbers': [5, 3],
            'operation': '+',
            'result': 8
        }
        assert game_state.check_answer(8) is True

    def test_check_answer_incorrect(self, game_state):
        """Test checking an incorrect answer."""
        game_state.current_puzzle = {
            'numbers': [5, 3],
            'operation': '+',
            'result': 8
        }
        assert game_state.check_answer(10) is False

    def test_check_answer_invalid_input(self, game_state):
        """Test checking an invalid input."""
        game_state.current_puzzle = {
            'numbers': [5, 3],
            'operation': '+',
            'result': 8
        }
        assert game_state.check_answer('invalid') is False

    def test_update_score_correct(self, game_state):
        """Test score update for correct answer."""
        initial_score = game_state.score
        game_state.update_score(correct=True)
        assert game_state.score == initial_score + game_state.config.score_increment

    def test_update_score_correct_with_hint(self, game_state):
        """Test score update for correct answer with hint."""
        initial_score = game_state.score
        game_state.update_score(correct=True, hint_used=True)
        assert game_state.score == initial_score + game_state.config.score_increment - (game_state.config.score_decrement // 2)

    def test_update_score_incorrect(self, game_state):
        """Test score update for incorrect answer."""
        initial_score = game_state.score
        game_state.update_score(correct=False)
        assert game_state.score == max(0, initial_score - game_state.config.score_decrement)

    def test_use_hint(self, game_state):
        """Test using a hint."""
        initial_hints = game_state.hints_remaining
        assert game_state.use_hint() is True
        assert game_state.hints_remaining == initial_hints - 1

    def test_use_hint_none_remaining(self, game_state):
        """Test using hints when none are remaining."""
        game_state.hints_remaining = 0
        assert game_state.use_hint() is False

    def test_increase_level(self, game_state):
        """Test increasing game level."""
        initial_level = game_state.level
        assert game_state.increase_level() is True
        assert game_state.level == initial_level + 1

    def test_increase_level_at_max(self, game_state):
        """Test increasing level at maximum level."""
        game_state.level = game_state.config.max_level
        assert game_state.increase_level() is False
        assert game_state.level == game_state.config.max_level

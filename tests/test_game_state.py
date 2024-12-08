"""Unit tests for game state management system."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.game.core.game_state import GameState
from src.game.core.base_errors import GameStateError

@pytest.fixture
def game_state():
    """Create a fresh game state instance for each test."""
    # Reset the singleton instance
    GameState._instance = None
    return GameState()

def test_singleton_pattern(game_state):
    """Test that GameState follows singleton pattern."""
    state2 = GameState()
    assert game_state is state2

def test_initial_state(game_state):
    """Test initial game state values."""
    state = game_state.get_state()
    
    assert state['player']['level'] == 1
    assert state['player']['score'] == 0
    assert isinstance(state['player']['achievements'], set)
    assert state['game']['difficulty'] == 'normal'
    assert state['settings']['sound_enabled'] is True
    assert state['statistics']['puzzles_solved'] == 0

def test_save_load_state(game_state):
    """Test saving and loading game state."""
    # Modify state
    game_state.update_score(100)
    game_state.add_achievement('first_win')
    
    with patch('src.game.core.resource_manager.ResourceManager.save_game_state') as mock_save:
        filename = game_state.save_state('test_save.save')
        assert 'test_save.save' == filename
        mock_save.assert_called_once()

    # Reset state
    game_state.reset_state()
    assert game_state.get_state()['player']['score'] == 0
    
    # Load state
    with patch('src.game.core.resource_manager.ResourceManager.load_game_state') as mock_load:
        mock_load.return_value = {
            'player': {
                'score': 100,
                'achievements': ['first_win'],
                'level': 1,
                'name': '',
                'high_scores': []
            },
            'game': {
                'difficulty': 'normal',
                'current_puzzle': None,
                'puzzles_completed': 0,
                'streak': 0
            },
            'settings': {
                'sound_enabled': True,
                'music_enabled': True,
                'difficulty_scaling': True
            },
            'statistics': {
                'total_time_played': 0,
                'puzzles_solved': 0,
                'correct_answers': 0,
                'wrong_answers': 0,
                'hints_used': 0
            }
        }
        
        game_state.load_state('test_save.save')
        loaded_state = game_state.get_state()
        assert loaded_state['player']['score'] == 100
        assert 'first_win' in loaded_state['player']['achievements']

def test_score_management(game_state):
    """Test score updating and high scores."""
    # Test score update
    new_score = game_state.update_score(100)
    assert new_score == 100
    
    # Test high scores
    high_scores = game_state.get_high_scores()
    assert len(high_scores) == 1
    assert high_scores[0] == 100
    
    # Test multiple scores
    game_state.update_score(50)
    game_state.update_score(200)
    high_scores = game_state.get_high_scores()
    assert high_scores == [200, 150, 100]

def test_statistics_update(game_state):
    """Test statistics updating."""
    # Test valid statistic
    game_state.update_statistics('puzzles_solved')
    state = game_state.get_state()
    assert state['statistics']['puzzles_solved'] == 1
    
    # Test invalid statistic
    with pytest.raises(GameStateError) as exc_info:
        game_state.update_statistics('invalid_stat')
    assert 'Invalid statistic name' in str(exc_info.value)

def test_achievements(game_state):
    """Test achievement management."""
    game_state.add_achievement('first_win')
    state = game_state.get_state()
    assert 'first_win' in state['player']['achievements']
    
    # Test duplicate achievement
    game_state.add_achievement('first_win')
    assert len(state['player']['achievements']) == 1

def test_state_reset(game_state):
    """Test state reset functionality."""
    # Modify state
    game_state.update_score(100)
    game_state.add_achievement('test_achievement')
    game_state.update_statistics('puzzles_solved', 5)
    
    # Reset state
    game_state.reset_state()
    state = game_state.get_state()
    
    assert state['player']['score'] == 0
    assert len(state['player']['achievements']) == 0
    assert state['statistics']['puzzles_solved'] == 0

def test_error_handling(game_state):
    """Test error handling in game state operations."""
    # Test save error
    with patch('src.game.core.resource_manager.ResourceManager.save_game_state',
              side_effect=Exception('Save error')):
        with pytest.raises(GameStateError) as exc_info:
            game_state.save_state()
        assert 'Failed to save game state' in str(exc_info.value)
    
    # Test load error
    with patch('src.game.core.resource_manager.ResourceManager.load_game_state',
              side_effect=Exception('Load error')):
        with pytest.raises(GameStateError) as exc_info:
            game_state.load_state('test.save')
        assert 'Failed to load game state' in str(exc_info.value)

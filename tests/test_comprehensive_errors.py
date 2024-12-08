import pytest
import logging
import json
import io

from src.game.error_handling import (
    BananaMathError,
    NetworkError,
    AuthenticationError,
    ConfigurationError,
    ResourceNotFoundError,
    PermissionDeniedError,
    RateLimitExceededError,
    DataIntegrityError,
    GameplayError,
    InvalidMoveError,
    OutOfResourcesError
)

from src.game.core.logging_config import configure_logging

def test_specific_error_types():
    """Test all specific error types."""
    error_types = [
        NetworkError,
        AuthenticationError,
        ConfigurationError,
        ResourceNotFoundError,
        PermissionDeniedError,
        RateLimitExceededError,
        DataIntegrityError,
        GameplayError,
        InvalidMoveError,
        OutOfResourcesError
    ]

    for ErrorClass in error_types:
        context = {"test_key": "test_value"}
        error = ErrorClass("Test error", context)
        
        assert isinstance(error, BananaMathError)
        assert str(error) == "Test error"
        assert error.context == context

def test_error_hierarchy():
    """Verify error type hierarchy."""
    assert issubclass(NetworkError, BananaMathError)
    assert issubclass(GameplayError, BananaMathError)
    assert issubclass(InvalidMoveError, GameplayError)

def test_logging_configuration():
    """Test logging configuration and JSON output."""
    # Capture log output
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    
    logger = configure_logging()
    logger.info("Test log message", extra_context="test")
    
    # Parse JSON log
    log_output = log_capture.getvalue().strip()
    log_data = json.loads(log_output)
    
    assert 'msg' in log_data
    assert log_data['msg'] == "Test log message"
    assert log_data['extra_context'] == "test"

def test_error_context_logging():
    """Test logging with error context."""
    try:
        raise NetworkError("Connection failed", {"url": "example.com"})
    except NetworkError as e:
        assert str(e) == "Connection failed"
        assert e.context == {"url": "example.com"}

def test_nested_error_handling():
    """Test nested error handling scenarios."""
    def inner_function():
        raise ConfigurationError("Invalid config", {"config_key": "database"})
    
    def outer_function():
        try:
            inner_function()
        except ConfigurationError as e:
            raise AuthenticationError("Authentication failed due to config error") from e
    
    with pytest.raises(AuthenticationError) as exc_info:
        outer_function()
    
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ConfigurationError)

def test_error_serialization():
    """Test error serialization capabilities."""
    error = GameplayError("Invalid game state", {"game_id": "12345"})
    
    error_dict = {
        "type": type(error).__name__,
        "message": str(error),
        "context": error.context
    }
    
    assert error_dict == {
        "type": "GameplayError",
        "message": "Invalid game state",
        "context": {"game_id": "12345"}
    }

def test_multiple_error_contexts():
    """Test creating errors with multiple context entries."""
    error = InvalidMoveError("Invalid move", {
        "player_id": "player1",
        "move_type": "addition",
        "game_state": "in_progress"
    })
    
    assert error.context == {
        "player_id": "player1",
        "move_type": "addition",
        "game_state": "in_progress"
    }

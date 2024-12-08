import pytest
from src.game.error_handling import (
    BananaMathError, 
    PuzzleGenerationError, 
    ValidationError, 
    handle_exceptions,
    safe_execute,
    retry
)

def test_banana_math_error():
    """Test base BananaMathError with context."""
    context = {"test_key": "test_value"}
    error = BananaMathError("Test error", context)
    
    assert str(error) == "Test error"
    assert error.context == context

def test_puzzle_generation_error():
    """Test PuzzleGenerationError specific behavior."""
    with pytest.raises(PuzzleGenerationError):
        raise PuzzleGenerationError("Puzzle generation failed", {"operation": "division"})

def test_validation_error():
    """Test ValidationError specific behavior."""
    with pytest.raises(ValidationError):
        raise ValidationError("Invalid input", {"input_value": 42})

def test_handle_exceptions():
    """Test exception handling decorator."""
    @handle_exceptions(default_return=0)
    def risky_function(x, y):
        return x / y

    # Normal case
    assert risky_function(10, 2) == 5

    # Division by zero case
    assert risky_function(10, 0) == 0

def test_safe_execute():
    """Test safe execution of functions."""
    def divide(x, y):
        return x / y

    # Successful execution
    assert safe_execute(divide, 10, 2) == 5

    # Failed execution
    assert safe_execute(divide, 10, 0) is None

def test_retry_decorator():
    """Test retry decorator with simulated failures."""
    attempts = 0

    @retry(max_attempts=3, delay=0.1)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Not ready yet")
        return "Success"

    result = flaky_function()
    assert result == "Success"
    assert attempts == 3

def test_retry_max_attempts():
    """Test retry decorator exceeding max attempts."""
    attempts = 0

    @retry(max_attempts=2, delay=0.1)
    def always_fail():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Always fails")

    with pytest.raises(RuntimeError):
        always_fail()

    assert attempts == 2

"""Unit tests for configuration management."""

import os
import pytest
from unittest.mock import patch, MagicMock

from src.game.core.config import AppConfiguration
from src.game.core.base_errors import ConfigurationError

@pytest.fixture
def config():
    """Create a fresh configuration instance for each test."""
    # Reset the singleton instance
    AppConfiguration._instance = None
    AppConfiguration._initialized = False
    return AppConfiguration()

def test_singleton_pattern(config):
    """Test that AppConfiguration follows singleton pattern."""
    config2 = AppConfiguration()
    assert config is config2

def test_default_values(config):
    """Test default configuration values are set correctly."""
    assert config.get('APP_NAME') == 'Banana Math Puzzle'
    assert config.get('DEBUG') is False
    assert config.get('LOG_LEVEL') == 'INFO'

def test_environment_override(config):
    """Test environment variables override defaults."""
    with patch.dict(os.environ, {'APP_NAME': 'Test App'}):
        assert config.get('APP_NAME') == 'Test App'

def test_missing_required_config():
    """Test error handling for missing required configuration."""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            AppConfiguration()
        assert 'Configuration validation failed' in str(exc_info.value)

def test_invalid_boolean_value():
    """Test error handling for invalid boolean value."""
    with patch.dict(os.environ, {'DEBUG': 'invalid'}):
        config = AppConfiguration()
        assert config.get('DEBUG') is False  # Falls back to default

def test_config_caching(config):
    """Test configuration value caching."""
    # First call should cache the value
    value1 = config.get('APP_NAME')
    
    # Modify environment (shouldn't affect cached value)
    with patch.dict(os.environ, {'APP_NAME': 'New Name'}):
        value2 = config.get('APP_NAME')
        assert value1 == value2
        
        # Clear cache and get new value
        config.clear_cache()
        value3 = config.get('APP_NAME')
        assert value3 == 'New Name'

def test_env_file_loading():
    """Test .env file loading."""
    mock_env_content = """
    APP_NAME=Test App
    DEBUG=true
    LOG_LEVEL=DEBUG
    """
    
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = mock_env_content
        with patch('os.path.isfile', return_value=True):
            config = AppConfiguration()
            assert config.get('APP_NAME') == 'Test App'
            assert config.get('DEBUG') is True
            assert config.get('LOG_LEVEL') == 'DEBUG'

def test_type_conversion(config):
    """Test automatic type conversion based on REQUIRED_CONFIGS."""
    with patch.dict(os.environ, {
        'DEBUG': 'true',
        'LOG_LEVEL': 'DEBUG'
    }):
        assert isinstance(config.get('DEBUG'), bool)
        assert isinstance(config.get('LOG_LEVEL'), str)

def test_error_context():
    """Test error context in ConfigurationError."""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            AppConfiguration()
        
        error = exc_info.value
        assert 'context' in dir(error)
        assert 'missing_keys' in error.context

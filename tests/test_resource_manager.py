"""Unit tests for resource management system."""

import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from PIL import Image

from src.game.core.resource_manager import ResourceManager
from src.game.core.base_errors import ResourceError

@pytest.fixture
def resource_manager():
    """Create a fresh resource manager instance for each test."""
    # Reset the singleton instance
    ResourceManager._instance = None
    return ResourceManager()

@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for testing."""
    assets_dir = tmp_path / 'assets'
    data_dir = tmp_path / 'data'
    logs_dir = tmp_path / 'logs'
    
    # Create directories
    for dir_path in [assets_dir, data_dir, logs_dir]:
        dir_path.mkdir()
    
    # Create resource type directories
    for resource_type in ResourceManager.RESOURCE_TYPES:
        (assets_dir / resource_type).mkdir()
    
    return {
        'assets': assets_dir,
        'data': data_dir,
        'logs': logs_dir
    }

def test_singleton_pattern(resource_manager):
    """Test that ResourceManager follows singleton pattern."""
    manager2 = ResourceManager()
    assert resource_manager is manager2

def test_directory_initialization(resource_manager, temp_dirs):
    """Test directory structure initialization."""
    with patch.dict('os.environ', {
        'ASSETS_DIR': str(temp_dirs['assets']),
        'DATA_DIR': str(temp_dirs['data']),
        'LOGS_DIR': str(temp_dirs['logs'])
    }):
        resource_manager._initialize_directories()
        
        # Verify directories exist
        for dir_path in temp_dirs.values():
            assert dir_path.exists()
        
        # Verify resource type directories
        for resource_type in ResourceManager.RESOURCE_TYPES:
            assert (temp_dirs['assets'] / resource_type).exists()

def test_get_resource_path(resource_manager):
    """Test resource path resolution."""
    with pytest.raises(ResourceError) as exc_info:
        resource_manager.get_resource_path('invalid_type', 'test.png')
    assert 'Invalid resource type' in str(exc_info.value)
    
    path = resource_manager.get_resource_path('images', 'test.png')
    assert isinstance(path, Path)
    assert 'images' in str(path)

def test_load_image(resource_manager, temp_dirs):
    """Test image loading with caching."""
    test_image = temp_dirs['assets'] / 'images' / 'test.png'
    
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    img.save(test_image)
    
    # Test loading
    loaded_img = resource_manager.load_image('test.png')
    assert isinstance(loaded_img, Image.Image)
    
    # Test caching
    cache_key = 'image:test.png'
    assert cache_key in resource_manager._cache
    
    # Test error handling
    with pytest.raises(ResourceError) as exc_info:
        resource_manager.load_image('nonexistent.png')
    assert 'Failed to load image' in str(exc_info.value)

def test_game_state_save_load(resource_manager, temp_dirs):
    """Test game state saving and loading."""
    test_state = {'score': 100, 'level': 2}
    
    # Test saving
    resource_manager.save_game_state(test_state, 'test.save')
    save_path = temp_dirs['data'] / 'saves' / 'test.save'
    assert save_path.exists()
    
    # Test loading
    loaded_state = resource_manager.load_game_state('test.save')
    assert loaded_state == test_state
    
    # Test error handling
    with pytest.raises(ResourceError) as exc_info:
        resource_manager.load_game_state('nonexistent.save')
    assert 'Failed to load game state' in str(exc_info.value)

def test_list_resources(resource_manager, temp_dirs):
    """Test resource listing."""
    # Create test resources
    (temp_dirs['assets'] / 'images' / 'test1.png').touch()
    (temp_dirs['assets'] / 'images' / 'test2.jpg').touch()
    
    resources = resource_manager.list_resources('images')
    assert len(resources) == 2
    assert 'test1.png' in resources
    assert 'test2.jpg' in resources
    
    # Test error handling
    with pytest.raises(ResourceError) as exc_info:
        resource_manager.list_resources('invalid_type')
    assert 'Invalid resource type' in str(exc_info.value)

def test_cache_management(resource_manager, temp_dirs):
    """Test cache management."""
    # Create and load test image
    test_image = temp_dirs['assets'] / 'images' / 'test.png'
    img = Image.new('RGB', (100, 100), color='red')
    img.save(test_image)
    
    resource_manager.load_image('test.png')
    assert len(resource_manager._cache) > 0
    
    # Test cache clearing
    resource_manager.clear_cache()
    assert len(resource_manager._cache) == 0

def test_cleanup(resource_manager):
    """Test resource cleanup."""
    # Mock image resources
    mock_image = MagicMock(spec=Image.Image)
    resource_manager._cache['image:test.png'] = mock_image
    
    resource_manager.cleanup()
    
    # Verify image was closed
    mock_image.close.assert_called_once()
    assert len(resource_manager._cache) == 0

import pytest
import time
import uuid
from unittest.mock import patch, MagicMock

from src.game.auth import AuthManager, UserProfile
from src.game.error_handling import (
    AuthenticationError, 
    RegistrationError, 
    ProfileError
)

class TestAuthManager:
    @pytest.fixture
    def auth_manager(self, tmp_path):
        """Create an AuthManager with a temporary data directory."""
        return AuthManager(data_dir=str(tmp_path))

    def test_password_validation(self, auth_manager):
        """Test password complexity validation."""
        # Valid password
        assert auth_manager._validate_password("StrongP@ss123") is True
        
        # Invalid passwords
        assert auth_manager._validate_password("short") is False
        assert auth_manager._validate_password("nouppercase123") is False
        assert auth_manager._validate_password("NOLOWERCASE123") is False
        assert auth_manager._validate_password("NoSpecialChar123") is False

    def test_user_registration(self, auth_manager):
        """Test user registration with comprehensive checks."""
        # Successful registration
        username = f"testuser_{uuid.uuid4()}"
        password = "StrongP@ss123"
        
        user_profile, session = auth_manager.register(username, password)
        
        assert user_profile is not None
        assert user_profile.username == username
        assert session is not None
        assert 'token' in session

    def test_duplicate_registration(self, auth_manager):
        """Test registration with existing username."""
        username = f"testuser_{uuid.uuid4()}"
        password = "StrongP@ss123"
        
        # First registration should succeed
        first_profile, _ = auth_manager.register(username, password)
        
        # Second registration with same username should raise an error
        with pytest.raises(RegistrationError):
            auth_manager.register(username, "AnotherP@ss456")

    def test_login_flow(self, auth_manager):
        """Test complete login flow."""
        # Register a user first
        username = f"testuser_{uuid.uuid4()}"
        password = "StrongP@ss123"
        
        # Register
        registered_profile, _ = auth_manager.register(username, password)
        
        # Login
        logged_in_profile, session = auth_manager.login(username, password)
        
        assert logged_in_profile is not None
        assert logged_in_profile.username == username
        assert session is not None
        assert 'token' in session

    def test_invalid_login(self, auth_manager):
        """Test login with invalid credentials."""
        username = f"testuser_{uuid.uuid4()}"
        password = "StrongP@ss123"
        
        # Attempt login without registration
        with pytest.raises(AuthenticationError):
            auth_manager.login(username, password)
        
        # Register user
        auth_manager.register(username, password)
        
        # Attempt login with wrong password
        with pytest.raises(AuthenticationError):
            auth_manager.login(username, "WrongP@ss456")

    def test_rate_limiting(self, auth_manager):
        """Test login rate limiting."""
        username = f"testuser_{uuid.uuid4()}"
        password = "StrongP@ss123"
        
        # Register user
        auth_manager.register(username, password)
        
        # Simulate multiple failed login attempts
        for _ in range(auth_manager.MAX_LOGIN_ATTEMPTS):
            with pytest.raises(AuthenticationError):
                auth_manager.login(username, "WrongPassword")
        
        # Next attempt should trigger a more severe lockout
        with pytest.raises(AuthenticationError) as exc_info:
            auth_manager.login(username, "WrongPassword")
        
        assert "locked" in str(exc_info.value).lower()

class TestUserProfile:
    @pytest.fixture
    def user_profile(self):
        """Create a test user profile."""
        return UserProfile("testuser")

    def test_profile_initialization(self, user_profile):
        """Test user profile initialization."""
        assert user_profile.username == "testuser"
        assert user_profile.current_level == 1
        assert user_profile.score == 0
        assert user_profile.high_score == 0

    def test_profile_save_and_load(self, user_profile, tmp_path):
        """Test saving and loading user profile."""
        # Modify profile
        user_profile.current_level = 5
        user_profile.score = 100
        
        # Save profile
        with patch.object(user_profile, '_get_profile_path', 
                          return_value=tmp_path / f"{user_profile.user_id}.json"):
            user_profile.save()
        
        # Create new profile and load
        loaded_profile = UserProfile(user_profile.username, user_profile.user_id)
        
        assert loaded_profile.current_level == 5
        assert loaded_profile.score == 100

    def test_high_score_tracking(self, user_profile):
        """Test high score tracking."""
        user_profile.score = 50
        user_profile.save()
        assert user_profile.high_score == 50
        
        user_profile.score = 25
        user_profile.save()
        assert user_profile.high_score == 50  # Should not decrease
        
        user_profile.score = 75
        user_profile.save()
        assert user_profile.high_score == 75  # Should increase

    def test_profile_error_handling(self, user_profile):
        """Test error handling in profile operations."""
        # Simulate file system error during save
        with patch.object(user_profile, '_acquire_lock', side_effect=Exception("Lock error")):
            with pytest.raises(ProfileError):
                user_profile.save()

def test_auth_integration():
    """Comprehensive integration test for authentication flow."""
    # Create auth manager
    auth_manager = AuthManager()
    
    # Register user
    username = f"integrationuser_{uuid.uuid4()}"
    password = "StrongP@ss123"
    
    # Registration
    user_profile, registration_session = auth_manager.register(username, password)
    
    # Validate registration
    assert user_profile is not None
    assert user_profile.username == username
    
    # Login
    logged_in_profile, login_session = auth_manager.login(username, password)
    
    # Validate login
    assert logged_in_profile is not None
    assert logged_in_profile.username == username
    
    # Update profile
    logged_in_profile.current_level = 10
    logged_in_profile.score = 500
    logged_in_profile.save()
    
    # Validate session
    assert auth_manager.validate_session(login_session['token']) is True
    
    # Logout
    auth_manager.logout(login_session['token'])
    
    # Validate session after logout
    assert auth_manager.validate_session(login_session['token']) is False

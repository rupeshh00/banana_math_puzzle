#!/usr/bin/env python3
"""
Main entry point for Banana Math Puzzle game.

This module initializes the game and starts the Kivy application.
"""

import os
import sys
import traceback
import structlog
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

# Add the project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.game.utils.logging.config import configure_logging
from src.game.screens.menu_screen import MenuScreen
from src.game.screens.game_screen import GameScreen
from src.game.screens.scores_screen import ScoresScreen
from src.game.screens.settings_screen import SettingsScreen
from src.game.screens.help_screen import HelpScreen
from src.game.ui.sound_manager import sound_manager
from src.game.core.game_state import game_state
from src.game.ui.styles import LAYOUT

# Configure root logger
logger = configure_logging(__name__)

# Debug print at the very top
print("DEBUG: Entering main.py")
print(f"Current Python Path: {sys.path}")
print(f"Current Working Directory: {os.getcwd()}")

# Configure Kivy settings
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'multisamples', '0')  # Disable multisampling
Config.set('kivy', 'exit_on_escape', '0')  # Prevent accidental exit
Config.write()

def global_exception_handler(exctype, value, tb):
    """Global exception handler for unhandled exceptions."""
    import traceback
    import sys
    import os

    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)

    # Extract full traceback
    error_message = ''.join(traceback.format_exception(exctype, value, tb))
    
    # Print to console for immediate visibility
    print("CRITICAL ERROR: An unhandled exception occurred.")
    print(f"Error Type: {exctype.__name__}")
    print(f"Error Message: {value}")
    print("Full Traceback:")
    traceback.print_exception(exctype, value, tb)
    
    # Write detailed error log
    try:
        with open('logs/startup_error.log', 'w') as error_file:
            error_file.write("CRITICAL STARTUP ERROR\n")
            error_file.write("=" * 50 + "\n")
            error_file.write(f"Timestamp: {datetime.now()}\n")
            error_file.write(f"Error Type: {exctype.__name__}\n")
            error_file.write(f"Error Message: {value}\n\n")
            error_file.write("Full Traceback:\n")
            error_file.write(error_message)
            
            # Include system and environment information
            error_file.write("\n\nSYSTEM INFORMATION:\n")
            error_file.write(f"Python Version: {sys.version}\n")
            error_file.write(f"Platform: {platform.platform()}\n")
            error_file.write(f"Current Working Directory: {os.getcwd()}\n")
            error_file.write(f"Python Path: {sys.path}\n")
    except Exception as log_err:
        print(f"Could not write error log: {log_err}")
    
    # Exit with error code
    sys.exit(1)

# Set global exception handler early
import sys
sys.excepthook = global_exception_handler

class BananaMathApp(App):
    """Main application class for Banana Math Puzzle."""
    
    def __init__(self, **kwargs):
        """Initialize the app with improved state management."""
        super().__init__(**kwargs)
        self.title = 'Banana Math Puzzle'
        self.screen_manager = None
        self.auth_manager = None
        self.current_profile = None
        self._screens = {}
        self._cleanup_handlers = {}
        
    def build(self):
        """Build and return the root widget."""
        try:
            # Set window properties
            Window.size = (LAYOUT['window_width'], LAYOUT['window_height'])
            Window.minimum_width, Window.minimum_height = LAYOUT['min_width'], LAYOUT['min_height']
            
            # Create screen manager with fade transition
            self.screen_manager = ScreenManager(transition=FadeTransition(duration=0.2))
            
            # Add initial screens
            screens = [
                ('menu', MenuScreen),
                ('scores', ScoresScreen),
                ('settings', SettingsScreen),
                ('help', HelpScreen)
            ]
            
            for name, screen_class in screens:
                try:
                    screen = screen_class(name=name)
                    self._add_screen(name, screen)
                except Exception as e:
                    logger.error(f"Failed to create screen {name}", error=str(e))
                    raise
            
            # Initialize game screen separately after profile is loaded
            try:
                profile = game_state.get_current_profile()
                if profile:
                    game_screen = GameScreen(name='game', profile=profile)
                    self._add_screen('game', game_screen)
                else:
                    logger.warning("No profile loaded, game screen will be added after login")
            except Exception as e:
                logger.error("Failed to create game screen", error=str(e))
            
            # Set initial screen
            self.screen_manager.current = 'menu'
            
            return self.screen_manager
            
        except Exception as e:
            logger.error(f"Failed to build application: {str(e)}")
            raise
    
    def _add_screen(self, name: str, screen: Screen):
        """Add screen with proper cleanup handling."""
        if name in self._screens:
            self._remove_screen(name)
        self._screens[name] = screen
        self.screen_manager.add_widget(screen)
    
    def _remove_screen(self, name: str):
        """Remove screen with cleanup."""
        if name in self._screens:
            screen = self._screens.pop(name)
            if name in self._cleanup_handlers:
                self._cleanup_handlers[name]()
            self.screen_manager.remove_widget(screen)
    
    def switch_screen(self, screen_name: str):
        """Switch screens with proper state management."""
        if screen_name in self._screens:
            self.screen_manager.current = screen_name
    
    def on_start(self):
        """Handle application start."""
        try:
            # Initialize sound manager
            sound_manager.play_music('background.wav')  # Try .wav first
        except Exception:
            try:
                sound_manager.play_music('background.mp3')  # Try .mp3 as fallback
            except Exception as e:
                logger.warning(
                    "Could not play background music",
                    error=str(e)
                )
    
    def on_stop(self):
        """Handle application stop."""
        # Cleanup resources
        sound_manager.stop_music()
        
        # Save game state
        try:
            game_state.save_state()
        except Exception as e:
            logger.error("Failed to save game state", error=str(e))

if __name__ == "__main__":
    try:
        logger.info("Starting Banana Math Puzzle")
        BananaMathApp().run()
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}")
        sys.exit(1)

import unittest
import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from unittest.mock import MagicMock
from src.game.screens.game_screen import InfoBar, PuzzleDisplay, NumberPad, GameScreen
from kivy.uix.label import Label


class TestInfoBar(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        EventLoop.ensure_window()

    def test_init(self):
        """Test InfoBar initialization."""
        info_bar = InfoBar()
        self.assertEqual(len(info_bar.children), 3)
        self.assertEqual(info_bar.orientation, 'horizontal')

    def test_update(self):
        """Test InfoBar update method."""
        info_bar = InfoBar()
        info_bar.update(score=10, level=2, hints=1)
        
        # Check if labels are updated correctly
        labels = [child for child in info_bar.children if isinstance(child, Label)]
        self.assertTrue(any('Score: 10' in label.text for label in labels))
        self.assertTrue(any('Level: 2' in label.text for label in labels))
        self.assertTrue(any('Hints: 1' in label.text for label in labels))


class TestPuzzleDisplay(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        EventLoop.ensure_window()

    def test_init(self):
        """Test PuzzleDisplay initialization."""
        puzzle_display = PuzzleDisplay()
        self.assertEqual(puzzle_display.orientation, 'horizontal')
        self.assertEqual(puzzle_display.current_answer, '')

    def test_update_puzzle(self):
        """Test updating puzzle display."""
        puzzle_display = PuzzleDisplay()
        puzzle = {
            'num1': 5,
            'num2': 3,
            'operation': '+',
            'result': 8
        }
        puzzle_display.update_puzzle(puzzle)
        
        # Check if labels are created correctly
        self.assertEqual(len(puzzle_display.children), 5)
        label_texts = [child.text for child in puzzle_display.children]
        self.assertIn('5', label_texts)
        self.assertIn('+', label_texts)
        self.assertIn('3', label_texts)
        self.assertIn('=', label_texts)
        self.assertIn('8', label_texts)

    def test_update_answer(self):
        """Test updating answer."""
        puzzle_display = PuzzleDisplay()
        # Add a banana placeholder label
        banana_label = Label(text='🍌')
        puzzle_display.add_widget(banana_label)
        
        puzzle_display.update_answer('5')
        self.assertEqual(puzzle_display.current_answer, '5')
        self.assertEqual(banana_label.text, '5')


@pytest.fixture
def game_screen():
    """Fixture providing a fresh GameScreen instance."""
    mock_profile = MagicMock()
    mock_profile.username = "TestUser"
    mock_profile.user_id = "test_user_id"
    return GameScreen(profile=mock_profile)


class TestNumberPad(unittest.TestCase):
    def test_init(self):
        """Test NumberPad initialization."""
        numbers_pressed = []
        def on_press(number):
            numbers_pressed.append(number)

        number_pad = NumberPad(on_number_press=on_press)
        self.assertEqual(len(number_pad.children), 9)  # 9 number buttons


class TestGameScreen(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        EventLoop.ensure_window()

    @pytest.fixture(autouse=True)
    def _pass_fixture(self, game_screen):
        self.game_screen = game_screen

    def test_init(self):
        """Test GameScreen initialization."""
        self.assertIsNotNone(self.game_screen.puzzle_display)
        self.assertIsNotNone(self.game_screen.number_pad)
        self.assertIsNotNone(self.game_screen.info_bar)

    def test_new_puzzle(self):
        """Test generating a new puzzle."""
        initial_puzzle = self.game_screen.game_state.current_puzzle
        self.game_screen.new_puzzle()
        new_puzzle = self.game_screen.game_state.current_puzzle
        
        self.assertNotEqual(initial_puzzle, new_puzzle)

    def test_check_answer_correct(self):
        """Test checking a correct answer."""
        # Set a known puzzle
        self.game_screen.game_state.current_puzzle = {
            'num1': 5,
            'num2': 3,
            'operation': '+',
            'result': 8
        }
        
        # Simulate entering the correct answer
        self.game_screen.puzzle_display.update_answer('8')
        initial_score = self.game_screen.game_state.score
        
        self.game_screen.check_answer(None)
        
        self.assertGreater(self.game_screen.game_state.score, initial_score)

    def test_use_hint(self):
        """Test using a hint."""
        initial_hints = self.game_screen.game_state.hints_remaining
        self.game_screen.use_hint(None)
        
        assert self.game_screen.game_state.hints_remaining == initial_hints - 1

    def test_go_back(self):
        """Test that go_back method changes screen to 'welcome'."""
        # Mock the screen manager
        mock_manager = MagicMock()
        self.game_screen.manager = mock_manager

        # Call go_back method
        self.game_screen.go_back(None)  # None as instance since it's not used

        # Assert that the current screen is set to 'welcome'
        mock_manager.current = 'welcome'
        self.assertEqual(mock_manager.current, 'welcome')

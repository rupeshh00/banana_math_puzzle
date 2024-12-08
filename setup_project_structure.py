import os
import shutil

BASE_PATH = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle'

DIRECTORY_STRUCTURE = [
    'src/game/core',
    'src/game/utils',
    'src/game/models',
    'src/game/screens',
    'tests/unit',
    'tests/integration',
    'docs',
    'scripts'
]

def create_project_structure():
    """Create the project directory structure."""
    for dir_path in DIRECTORY_STRUCTURE:
        full_path = os.path.join(BASE_PATH, dir_path)
        os.makedirs(full_path, exist_ok=True)
        
        # Create __init__.py in each directory for Python package compatibility
        init_path = os.path.join(full_path, '__init__.py')
        if not os.path.exists(init_path):
            open(init_path, 'a').close()

def move_files():
    """Move files to their appropriate directories."""
    moves = [
        # Core modules
        ('src/game/auth.py', 'src/game/core/auth.py'),
        ('src/game/game_logic.py', 'src/game/core/game_logic.py'),
        
        # Screens
        ('src/game/screens/login_screen.py', 'src/game/screens/login_screen.py'),  # Already in correct location
        
        # Utilities
        ('src/game/logging_config.py', 'src/game/utils/logging_config.py'),
        
        # Models
        # Add any model files here
    ]
    
    for src, dest in moves:
        src_path = os.path.join(BASE_PATH, src)
        dest_path = os.path.join(BASE_PATH, dest)
        
        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(src_path, dest_path)

def main():
    create_project_structure()
    move_files()
    print("Project structure created successfully!")

if __name__ == '__main__':
    main()

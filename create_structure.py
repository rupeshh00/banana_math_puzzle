import os

BASE_PATH = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle'

DIRECTORIES = [
    'src/game/core',
    'src/game/utils', 
    'src/game/models',
    'tests/unit',
    'tests/integration', 
    'scripts',
    'docs'
]

def create_project_structure():
    for dir_path in DIRECTORIES:
        full_path = os.path.join(BASE_PATH, dir_path)
        os.makedirs(full_path, exist_ok=True)
        # Create __init__.py in each directory for Python package compatibility
        init_path = os.path.join(full_path, '__init__.py')
        if not os.path.exists(init_path):
            open(init_path, 'a').close()
    
    print("Project structure created successfully!")

if __name__ == '__main__':
    create_project_structure()

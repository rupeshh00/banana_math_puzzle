#!/usr/bin/env python3
"""
Banana Math Puzzle - Application Launcher
"""

import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Ensure src is in the Python path
sys.path.insert(0, os.path.join(project_root, 'src'))

# Import the main application
from main import BananaMathApp

if __name__ == '__main__':
    try:
        BananaMathApp().run()
    except Exception as e:
        print(f"Critical error during application startup: {e}")
        import traceback
        traceback.print_exc()

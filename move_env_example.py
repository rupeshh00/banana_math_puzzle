import os
import shutil

src_path = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle/.env.example'
dest_path = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle/src/game/core/.env.example'

if os.path.exists(src_path):
    shutil.move(src_path, dest_path)
    print(f"Moved {src_path} to {dest_path}")
else:
    print(f"Source file {src_path} does not exist.")

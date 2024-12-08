import sys
import os
import json

def get_module_imports(file_path):
    imports = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('from ') or line.startswith('import '):
                    imports.append(line)
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
    return imports

def scan_project_imports(root_dir):
    import_graph = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, root_dir)
                imports = get_module_imports(full_path)
                import_graph[relative_path] = imports
    return import_graph

project_imports = scan_project_imports('src/game')
print(json.dumps(project_imports, indent=2))

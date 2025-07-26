import sys
import os

# Path to the virtual environment's root
venv_path = sys.prefix
print("Virtual environment path:", venv_path)

# Optionally, get the project folder (parent of venv)
project_path = os.path.dirname(venv_path)
print("Likely project folder:", project_path)


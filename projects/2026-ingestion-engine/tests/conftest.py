import sys
import os

# Add the project root to sys.path so tests can import from 'src' and 'run_pipeline'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

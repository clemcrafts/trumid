import sys
from pathlib import Path

# Add the project root to the Python module search path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

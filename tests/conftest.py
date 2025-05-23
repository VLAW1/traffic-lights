"""Test configuration for importing project modules."""

import sys
from pathlib import Path

# Add the parent directory to sys.path so that 'sim' can be imported
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

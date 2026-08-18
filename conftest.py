"""
pytest configuration file - Add project root to sys.path for proper imports
"""

import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This allows tests to import from src package
# Example: from src.api.main import app

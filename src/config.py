"""
Shared configuration module for database paths and project constants.
Ensures consistent paths across ETL, API, and tests.
"""

import os
from pathlib import Path

# Get the absolute project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Database path - single source of truth
DB_PATH = os.path.join(PROJECT_ROOT, "data", "nifty100.db")

# Schema path
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "db", "schema.sql")

# Data paths
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

__all__ = ["DB_PATH", "SCHEMA_PATH", "RAW_DATA_DIR", "OUTPUT_DIR", "PROJECT_ROOT"]

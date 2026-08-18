# src/api/export_specs.py
import sys
import os
import json

# Add the project root (two levels up from src/api) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.api.main import app

os.makedirs("docs", exist_ok=True)
openapi_path = "docs/openapi.json"

with open(openapi_path, "w") as f:
    json.dump(app.openapi(), f, indent=2)

print(f"OpenAPI spec successfully exported to {openapi_path}")
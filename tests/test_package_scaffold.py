#!/usr/bin/env python3
"""Focused checks for the experimental package source layout."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "src"


class PackageScaffoldTests(unittest.TestCase):
    def test_package_root_is_empty_and_schemas_are_resources(self):
        program = """
import hashlib
from importlib.resources import files
import json
import sys

before = set(sys.modules)
sys.path.insert(0, sys.argv[1])
import inference_campaign_contracts as package
resources = files(package) / "schemas"
payload = {
    "public": sorted(name for name in vars(package) if not name.startswith("_")),
    "schema_sha256": {
        name: hashlib.sha256((resources / name).read_bytes()).hexdigest()
        for name in (
            "campaign-assimilation-v0.schema.json",
            "evaluation-record-draft-v0.schema.json",
        )
    },
    "new_modules": sorted(set(sys.modules) - before),
}
print(json.dumps(payload, sort_keys=True))
"""
        completed = subprocess.run(
            [sys.executable, "-I", "-B", "-c", program, str(SOURCE_ROOT)],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        observed = json.loads(completed.stdout)
        self.assertEqual(observed["public"], [])
        self.assertEqual(
            observed["schema_sha256"],
            {
                "campaign-assimilation-v0.schema.json":
                    "12baba5b29764c07663d707215e3673d5ed870e10ed7c3764dee7cbe8d5009d5",
                "evaluation-record-draft-v0.schema.json":
                    "2bb0ade59efbf0308ac8886367cc0403f3c1299b03c705097037ebe10be04c59",
            },
        )
        forbidden = {"RIFT", "jax", "lal", "lalsimulation", "numpy", "supernu"}
        imported_roots = {name.split(".", 1)[0] for name in observed["new_modules"]}
        self.assertTrue(forbidden.isdisjoint(imported_roots), observed["new_modules"])


if __name__ == "__main__":
    unittest.main()

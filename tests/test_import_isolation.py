#!/usr/bin/env python3
"""Prove the reference reducer does not import project scientific stacks."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "src" / "inference_campaign_contracts" / "assimilation_v0.py"


class ImportIsolationTests(unittest.TestCase):
    def test_reference_uses_only_standard_library_imports(self):
        program = """
import importlib.util
import json
import sys

before = set(sys.modules)
spec = importlib.util.spec_from_file_location("assimilation_reference", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps(sorted(set(sys.modules) - before)))
"""
        completed = subprocess.run(
            [sys.executable, "-I", "-B", "-c", program, str(REFERENCE)],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        imported = json.loads(completed.stdout)
        forbidden_roots = {
            "RIFT",
            "jax",
            "lal",
            "lalsimulation",
            "numpy",
            "supernu",
        }
        observed_roots = {name.split(".", 1)[0] for name in imported}
        self.assertTrue(forbidden_roots.isdisjoint(observed_roots), imported)


if __name__ == "__main__":
    unittest.main()

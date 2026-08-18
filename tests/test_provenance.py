#!/usr/bin/env python3
"""Verify extracted contract bytes against the recorded incubation identities."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "PROVENANCE.json"


class ProvenanceTests(unittest.TestCase):
    def test_byte_identical_files_match_recorded_sha256(self):
        record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        self.assertEqual(record["format"], "inference-campaign-contracts-provenance/v1")
        self.assertEqual(len(record["byte_identical"]), 10)
        destinations = set()
        for item in record["byte_identical"]:
            destination = item["destination"]
            self.assertNotIn(destination, destinations)
            destinations.add(destination)
            payload = (ROOT / destination).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), item["sha256"])

    def test_package_scaffold_has_no_runtime_dependency_or_legacy_build_files(self):
        metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('requires-python = ">=3.9"', metadata)
        self.assertIn("dependencies = []", metadata)
        self.assertIn('version = "0.1.0a1"', metadata)
        for name in ("setup.py", "setup.cfg", "requirements.txt", "tox.ini"):
            self.assertFalse((ROOT / name).exists(), name)


if __name__ == "__main__":
    unittest.main()

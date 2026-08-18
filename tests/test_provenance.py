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

    def test_repository_shell_has_no_build_or_package_metadata(self):
        forbidden = {
            "build-system",
            "setup.py",
            "setup.cfg",
            "pyproject.toml",
            "requirements.txt",
            "tox.ini",
        }
        observed = {path.name for path in ROOT.iterdir()}
        self.assertTrue(forbidden.isdisjoint(observed), observed)


if __name__ == "__main__":
    unittest.main()

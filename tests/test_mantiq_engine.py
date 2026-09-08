#!/usr/bin/env python3
"""
test_mantiq_engine.py

Unit tests for Classical Arabic Logic (Manṭiq) and Morphology Engine.
"""

import sys
import unittest
from pathlib import Path

# Add repository root to python search path
REPO_ROOT = Path(__file__).parent.parent.resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.mantiq_engine import AynMantiqEngine, FallacyType, MantiqCategory
from core.mantiq_dataset_generator import AynMantiqDatasetGenerator


class TestAynMantiqEngine(unittest.TestCase):
    """Verifies Manṭiq logic evaluation and morphological root mapping."""

    def setUp(self):
        self.engine = AynMantiqEngine()
        self.generator = AynMantiqDatasetGenerator()

    def test_root_resolution(self):
        """Verifies mapping of engineering domains to classical tri-consonantal roots."""
        roots_lock = self.engine.resolve_roots_for_concept("atomic distributed lock")
        self.assertTrue(any(r.lemma_title == "قفل" for r in roots_lock))

        roots_immut = self.engine.resolve_roots_for_concept("immutable persistent cache buffer")
        self.assertTrue(any(r.lemma_title == "حفظ" for r in roots_immut))

        roots_types = self.engine.resolve_roots_for_concept("algebraic enum variant type discriminator")
        self.assertTrue(any(r.lemma_title == "ميز" for r in roots_types))

    def test_fallacy_detection_majaz_mukhil(self):
        """Verifies detection of leaky abstractions (generic DataManager / bare exceptions)."""
        bad_code = """
class UserDataManager:
    def process(self):
        try:
            x = 1 / 0
        except Exception:
            pass
"""
        critique = self.engine.audit_logic_fallacies(bad_code)
        self.assertFalse(critique.is_valid)
        self.assertIn(FallacyType.MAJAZ_MUKHIL, critique.detected_fallacies)

    def test_fallacy_detection_tasalsul(self):
        """Verifies detection of unbounded recursive routines without base guards."""
        unbounded_code = """
def loop_infinitely(val):
    return loop_infinitely(val + 1)
"""
        critique = self.engine.audit_logic_fallacies(unbounded_code)
        self.assertFalse(critique.is_valid)
        self.assertIn(FallacyType.TASALSUL, critique.detected_fallacies)

    def test_scratchpad_generation(self):
        """Verifies structure of generated <ayn_mantiq> reasoning block."""
        scratchpad = self.engine.generate_mantiq_scratchpad(
            prompt="Build a thread-safe rate limiter with token bucket",
            target_language="python"
        )
        self.assertIn("<ayn_mantiq>", scratchpad)
        self.assertIn("ISHTIQĀQ & MORPHOLOGICAL ROOTS", scratchpad)
        self.assertIn("TAṢAWWUR: ONTOLOGICAL ESSENCE VS ACCIDENT", scratchpad)
        self.assertIn("MANṬIQ: FALLACY ELIMINATION", scratchpad)
        self.assertIn("SYNTACTIC GOVERNANCE & CONTRACTS", scratchpad)
        self.assertIn("</ayn_mantiq>", scratchpad)

    def test_dataset_generation(self):
        """Verifies generation of complete dataset records."""
        output_path = Path("/home/absolut7/aynengineaicoding/data/test_mantiq_dataset.jsonl")
        records = self.generator.build_dataset(output_file=output_path)
        self.assertGreaterEqual(len(records), 4)

        for record in records:
            self.assertIn("instruction", record)
            self.assertIn("thought", record)
            self.assertIn("<ayn_mantiq>", record["thought"])
            self.assertIn("response", record)

        self.assertTrue(output_path.exists())
        output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

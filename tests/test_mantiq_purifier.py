#!/usr/bin/env python3
"""
test_mantiq_purifier.py

Unit tests for Epistemic Code Purifier (AynMantiqPurifier).
Verifies that unlogical variable names, bare exception catches, and circularities
are cleansed according to Ghazalian and Farahidian standards.
"""

import sys
import unittest
from pathlib import Path

# Add repository root to python search path
REPO_ROOT = Path(__file__).parent.parent.resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.mantiq_purifier import AynMantiqPurifier


class TestAynMantiqPurifier(unittest.TestCase):
    """Verifies purification of unlogical coding anti-patterns."""

    def test_purify_unlogical_variable_names(self):
        """Tests that amorphous names like 'data', 'temp', 'val' are replaced by teleological nouns."""
        unclean_code = """
def compute_metrics(data):
    temp = data.get("count", 0)
    val = temp * 2
    return val
"""
        report = AynMantiqPurifier.purify_python_code(unclean_code)
        self.assertTrue(report.is_purified)
        self.assertIn("payload_record", report.purified_code)
        self.assertIn("intermediate_state", report.purified_code)
        self.assertIn("evaluated_quantity", report.purified_code)

    def test_purify_bare_except(self):
        """Tests that bare 'except:' is replaced with an explicit typed exception."""
        unclean_code = """
def risky_operation():
    try:
        perform_io()
    except:
        cleanup()
"""
        report = AynMantiqPurifier.purify_python_code(unclean_code)
        self.assertTrue(report.is_purified)
        self.assertGreaterEqual(report.purged_bare_exceptions, 1)
        self.assertNotIn("except:", report.purified_code)
        self.assertIn("except RuntimeError as domain_execution_error:", report.purified_code)

    def test_purify_silent_exception_swallowing(self):
        """Tests that 'except Exception: pass' is purged and replaced with non-silent logging/raising."""
        unclean_code = """
def silent_failure():
    try:
        x = 1 / 0
    except Exception:
        pass
"""
        report = AynMantiqPurifier.purify_python_code(unclean_code)
        self.assertTrue(report.is_purified)
        self.assertNotIn("pass", report.purified_code)
        self.assertIn("raise RuntimeError", report.purified_code)

    def test_clean_code_remains_unmodified(self):
        """Tests that clean, teleological code is not altered unnecessarily."""
        clean_code = """
def calculate_harmonic_frequency(frequency_hertz: float) -> float:
    resonant_multiplier: float = 1.4142
    return frequency_hertz * resonant_multiplier
"""
        report = AynMantiqPurifier.purify_python_code(clean_code)
        self.assertEqual(clean_code.strip(), report.purified_code.strip())


if __name__ == "__main__":
    unittest.main()

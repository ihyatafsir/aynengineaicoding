#!/usr/bin/env python3
"""
test_coding_engine.py

Comprehensive test suite for AynEngine AI Coding Edition:
- AynCodeLexiconMapper (5-Pillar RAG context generation & root extraction)
- AynCodingEngine syntax validator & placeholder detector
- AynAstValidator AST parsing & bracket balancing
- AynStaticAuditor 5-Pillar Epistemic static evaluation
- AynProviderTransport multi-provider & offline synthesis
- Self-Audit Epistemic Verification (Grade A+ assertion)
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from core.code_lexicon_mapper import AynCodeLexiconMapper
from core.coding_engine import AynCodingEngine
from core.ast_validator import AynAstValidator
from core.static_auditor import AynStaticAuditor
from core.provider_transport import AynProviderTransport, GenerationConfig


class TestAynCodeLexiconMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = AynCodeLexiconMapper()

    def test_dimension_extraction(self):
        prompt = "Create an async worker pool with mutex locks, queue dispatch, and backpressure error handling."
        dims = self.mapper.extract_relevant_dimensions(prompt)
        self.assertIn("concurrency", dims)
        self.assertIn("error_handling", dims)

    def test_root_extraction(self):
        prompt = "Build an immutable state store with pure functional updates and type invariants."
        roots = self.mapper.extract_relevant_roots(prompt)
        self.assertTrue(len(roots) > 0)
        # Should contain roots related to immutability/types
        self.assertTrue(any(r in roots for r in ["ثبت", "حفظ", "ميز", "حدّ"]))

    def test_epistemic_context_generation(self):
        prompt = "Implement a distributed rate limiter in Rust using token bucket algorithm."
        ctx = self.mapper.build_epistemic_coding_context(prompt, "rust")
        self.assertIn("AL-MUFRADĀT", ctx)
        self.assertIn("ASĀS AL-BALĀGHAH", ctx)
        self.assertIn("LISĀN AL-ʿARAB", ctx)
        self.assertIn("KITĀB AL-ʿAYN", ctx)
        self.assertIn("AL-KITĀB", ctx)


class TestAynCodingEngineValidation(unittest.TestCase):
    def setUp(self):
        self.engine = AynCodingEngine()

    def test_syntax_validator_valid_python(self):
        valid_py = """
def calculate_ratio(num: float, den: float) -> float:
    if den == 0:
        raise ValueError("Denominator cannot be zero")
    return num / den
"""
        res = self.engine._validate_syntax(valid_py, "python")
        self.assertTrue(res["valid"])
        self.assertIsNone(res["error"])

    def test_syntax_validator_invalid_python(self):
        invalid_py = """
def broken_fn(:
    return 42
"""
        res = self.engine._validate_syntax(invalid_py, "python")
        self.assertFalse(res["valid"])
        self.assertIsNotNone(res["error"])

    def test_bracket_balancer_valid(self):
        valid_rust = 'fn main() { let x = vec![1, 2, (3 + 4)]; println!("{}", x.len()); }'
        res = self.engine._validate_syntax(valid_rust, "rust")
        self.assertTrue(res["valid"])

    def test_bracket_balancer_invalid(self):
        invalid_rust = "fn main() { let x = vec![1, 2, (3 + 4]; }"
        res = self.engine._validate_syntax(invalid_rust, "rust")
        self.assertFalse(res["valid"])
        self.assertIn("Mismatched", res["error"])

    def test_zero_loss_placeholder_detection(self):
        lazy_code = """
class DataHandler:
    def process(self):
        # TODO: implement data processing here
        pass
"""
        violations = self.engine._check_zero_loss_placeholders(lazy_code)
        self.assertTrue(len(violations) > 0)

    def test_extract_code_block(self):
        markdown_text = """Here is the implementation:
```python
def pure_function(x: int) -> int:
    return x * 2
```
Hope this helps!"""
        code = self.engine._extract_code_block(markdown_text, "python")
        self.assertIn("def pure_function", code)
        self.assertNotIn("```", code)
        self.assertNotIn("Here is the implementation", code)


class TestAynAstValidator(unittest.TestCase):
    def test_json_validation(self):
        valid_json = '{"teleology": "pure", "active": true}'
        res_valid = AynAstValidator.validate_syntax(valid_json, "json")
        self.assertTrue(res_valid.is_valid)

        invalid_json = '{"teleology": "unclosed"'
        res_invalid = AynAstValidator.validate_syntax(invalid_json, "json")
        self.assertFalse(res_invalid.is_valid)

    def test_banned_placeholders(self):
        code_with_pass = "def run():\n    pass  # implement later\n"
        violations = AynAstValidator.detect_banned_placeholders(code_with_pass)
        self.assertTrue(len(violations) > 0)


class TestAynStaticAuditor(unittest.TestCase):
    def test_auditor_scores_high_on_clean_code(self):
        clean_code = """
class StateRegistry:
    def __init__(self):
        self.lifecycle_state = "active"
        self.active_count = 0

    def register_entry(self, entry_identifier: str) -> bool:
        if not entry_identifier:
            raise ValueError("Identifier must not be empty")
        self.active_count += 1
        return True
"""
        report = AynStaticAuditor.audit_code(clean_code, "python", "test_clean.py")
        self.assertGreaterEqual(report.composite_score_percent, 90.0)
        self.assertIn(report.epistemic_grade, ["A", "A+"])

    def test_auditor_penalizes_vague_names_and_swallowed_exceptions(self):
        dirty_code = """
def doAction(data, val, item):
    tmp = []
    try:
        tmp.append(data)
    except:
        pass
    return tmp
"""
        report = AynStaticAuditor.audit_code(dirty_code, "python", "test_dirty.py")
        self.assertLessEqual(report.composite_score_percent, 75.0)


class TestAynProviderTransport(unittest.TestCase):
    def test_offline_generation_python(self):
        transport = AynProviderTransport(default_provider="offline")
        cfg = GenerationConfig(
            prompt_instruction="Synthesize state tracker",
            target_language="python",
            provider_protocol="offline"
        )
        outcome = transport.execute_generation(cfg)
        self.assertEqual(outcome.provider_identity, "offline")
        self.assertEqual(outcome.lifecycle_status, "completed")
        self.assertIn("class SynthesizedEngine", outcome.synthesized_text)

    def test_offline_generation_javascript(self):
        transport = AynProviderTransport(default_provider="offline")
        cfg = GenerationConfig(
            prompt_instruction="Synthesize buffer queue",
            target_language="javascript",
            provider_protocol="offline"
        )
        outcome = transport.execute_generation(cfg)
        self.assertEqual(outcome.provider_identity, "offline")
        self.assertIn("class SynthesizedEngine", outcome.synthesized_text)


class TestAynSelfImprovement(unittest.TestCase):
    """
    Validates that AynEngine AI Coding Edition achieves an Epistemic Grade A/A+
    (>= 90%) when audited against its own 5 Classical Epistemic Pillars.
    """

    def test_coding_engine_self_audit(self):
        engine_path = BASE_DIR / "core" / "coding_engine.py"
        report = AynStaticAuditor.audit_file(engine_path)
        self.assertGreaterEqual(
            report.composite_score_percent,
            90.0,
            f"coding_engine.py scored {report.composite_score_percent}% (Grade {report.epistemic_grade})"
        )
        self.assertIn(report.epistemic_grade, ["A", "A+"])

    def test_static_auditor_self_audit(self):
        auditor_path = BASE_DIR / "core" / "static_auditor.py"
        report = AynStaticAuditor.audit_file(auditor_path)
        self.assertGreaterEqual(
            report.composite_score_percent,
            90.0,
            f"static_auditor.py scored {report.composite_score_percent}%"
        )

    def test_provider_transport_self_audit(self):
        transport_path = BASE_DIR / "core" / "provider_transport.py"
        report = AynStaticAuditor.audit_file(transport_path)
        self.assertGreaterEqual(
            report.composite_score_percent,
            90.0,
            f"provider_transport.py scored {report.composite_score_percent}%"
        )


if __name__ == "__main__":
    unittest.main()

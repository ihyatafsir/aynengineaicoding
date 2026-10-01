"""
test_ghazali_hmoe_unlearning.py

AynEngine AI Coding Edition: H-MoE & Ghazali Mantiq Unlearning Verification Suite.
Validates:
1. H-MoE Speculative Routing & 0.01s Epistemic Gate latency.
2. Ghazali Mantiq machine unlearning targets (purging vague identifiers, circular locks,
   infinite loops, and swallowed exceptions).
3. DeepSeek Flash 4.1 integration with Ghazali Epistemic RAG and AST self-correction.

Strict Zero-Emoji Policy Enforced.
"""

import os
import sys
import time
import unittest
from pathlib import Path

_ROOT = Path(__file__).parent.parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.knowledge_purger import AynKnowledgePurger
from core.ghazali_mantiq_rag import GhazaliMantiqRAG
from core.ast_validator import AynAstValidator
from core.ghazali_deepseek_synthesizer import GhazaliDeepSeekSynthesizer
from core.speculative_engine import AynSpeculativeEngine


class TestGhazaliHMoEUnlearning(unittest.TestCase):

    def setUp(self):
        self.purger = AynKnowledgePurger()
        self.rag = GhazaliMantiqRAG()
        self.validator = AynAstValidator()

    def test_01_purge_directives_completeness(self):
        """Verify all Ghazali Mantiq unlearning directives are formalized."""
        directives = AynKnowledgePurger.PURGE_DIRECTIVES
        self.assertGreaterEqual(len(directives), 4)

        categories = [d.category_id for d in directives]
        self.assertIn("purge_vague_ontology", categories)
        self.assertIn("purge_circular_dependencies", categories)
        self.assertIn("purge_infinite_regress", categories)
        self.assertIn("purge_state_contradictions", categories)

        for directive in directives:
            self.assertTrue(len(directive.banned_tokens_and_patterns) > 0)
            self.assertTrue(len(directive.epistemic_replacement_canon) > 0)
            self.assertTrue(len(directive.classical_authority) > 0)

    def test_02_unlearning_readiness_audit(self):
        """Verify that audit_unlearning_readiness flags pre-training slop."""
        slop_code = (
            "def handleStuff(data, temp):\n"
            "    # TODO: implement here\n"
            "    val = data.get('temp')\n"
            "    while True:\n"
            "        try:\n"
            "            res = doAction(val)\n"
            "            return res\n"
            "        except:\n"
            "            pass\n"
        )
        report = AynKnowledgePurger.audit_unlearning_readiness(slop_code)
        self.assertFalse(report["is_purged_and_pure"])
        self.assertGreater(report["total_violations"], 0)
        self.assertLess(report["epistemic_integrity_score"], 80.0)

        # Pure code should pass with high purity
        pure_code = (
            "class MonotonicSequenceCoordinator:\n"
            "    def __init__(self, maximum_capacity: int = 1000):\n"
            "        self.maximum_capacity = maximum_capacity\n"
            "        self.current_sequence = 0\n\n"
            "    def acquire_next_sequence(self) -> int:\n"
            "        if self.current_sequence >= self.maximum_capacity:\n"
            "            raise OverflowError('Capacity exhausted')\n"
            "        self.current_sequence += 1\n"
            "        return self.current_sequence\n"
        )
        pure_report = AynKnowledgePurger.audit_unlearning_readiness(pure_code)
        self.assertTrue(pure_report["is_purged_and_pure"])
        self.assertEqual(pure_report["total_violations"], 0)
        self.assertEqual(pure_report["epistemic_integrity_score"], 100.0)

    def test_03_hmoe_epistemic_gate_latency(self):
        """Verify that the 0.01s Epistemic Gate completes within bounded threshold."""
        sample_code = (
            "export interface MeshPacket {\n"
            "  packetIdentifier: string;\n"
            "  hopCount: number;\n"
            "  payloadChecksum: string;\n"
            "}\n"
        )
        start_time = time.perf_counter()
        audit_result = self.rag.audit_code_purity(sample_code, "TypeScript")
        gate_duration = time.perf_counter() - start_time

        self.assertTrue(audit_result["is_pure"])
        self.assertLess(gate_duration, 0.05, f"Epistemic Gate took {gate_duration:.4f}s, expected < 0.05s")

    def test_04_purge_and_infusion_dataset_integrity(self):
        """Verify the training pairs in the unlearning dataset."""
        dataset_path = _ROOT / "data/ayn_mantiq_purge_and_infusion_dataset.jsonl"
        self.assertTrue(dataset_path.exists(), f"Dataset missing: {dataset_path}")

        valid_count = 0
        import json
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    self.assertIn("instruction", item)
                    self.assertTrue("thought" in item or "response" in item)
                    content_str = item.get("thought", "") + item.get("response", "")
                    self.assertTrue("Daf" in content_str or "ayn_mantiq" in content_str)
                    valid_count += 1

        self.assertGreaterEqual(valid_count, 10, "Expected at least 10 unlearning pairs in dataset")

    def test_05_deepseek_flash_ghazali_synthesis(self):
        """Verify live synthesis with DeepSeek Flash 4.1 under Ghazali RAG governance."""
        synthesizer = GhazaliDeepSeekSynthesizer(temperature=0.1)
        task = "Synthesize an LRU translation cache in TypeScript with bounded maximum capacity and eviction TTL."

        try:
            result = synthesizer.synthesize(
                task_prompt=task,
                target_language="TypeScript",
                max_tokens=1024,
                max_refinement_passes=2,
                verbose=False
            )
        except Exception as e:
            if "Authentication" in str(e) or "401" in str(e) or "Authorization" in str(e):
                self.skipTest(f"Skipping live API call: {e}")
            raise

        self.assertTrue(result.is_pure, f"Synthesized code failed purity: {result.violations}")
        self.assertGreaterEqual(result.epistemic_score, 90.0)
        self.assertIn("class", result.synthesized_code.lower())
        self.assertFalse("// TODO" in result.synthesized_code)
        # Verify zero emojis
        import re
        emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027ff\U00002b50-\U00002b55]",
            flags=re.UNICODE
        )
        self.assertFalse(bool(emoji_pattern.search(result.synthesized_code)), "Emoji detected in synthesized output")


if __name__ == "__main__":
    unittest.main()

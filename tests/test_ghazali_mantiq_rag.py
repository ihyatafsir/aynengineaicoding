"""
Unit Tests for Ghazali Mantiq Epistemic RAG Core Engine
Verifies classical Ghazali axioms, 5 linguistic pillars, prompt generation,
and deterministic purity audit against logical fallacies.

Strict Zero-Emoji Policy Enforced.
"""

import unittest
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.ghazali_mantiq_rag import GhazaliMantiqRAG, ClassicalAxiom, LinguisticPillar


class TestGhazaliMantiqRAG(unittest.TestCase):

    def setUp(self):
        self.rag = GhazaliMantiqRAG()

    def test_foundational_axioms_registered(self):
        expected_axioms = [
            "al_hadd_bi_al_dhatiyyat",
            "daf_al_dawr",
            "daf_al_tasalsul",
            "adam_al_tanaqud",
            "qiyas_burhani"
        ]
        for axiom_key in expected_axioms:
            self.assertIn(axiom_key, self.rag.axioms, f"Missing foundational axiom: {axiom_key}")
            axiom = self.rag.axioms[axiom_key]
            self.assertTrue(len(axiom.name) > 0)
            self.assertTrue(len(axiom.arabic_name) > 0)
            self.assertTrue(len(axiom.classical_source) > 0)
            self.assertTrue(len(axiom.computational_invariant) > 0)

    def test_five_linguistic_pillars_registered(self):
        expected_pillars = ["farahidi", "raghib", "zamakhshari", "ibn_manzur", "sibawayh"]
        for pillar_key in expected_pillars:
            self.assertIn(pillar_key, self.rag.pillars, f"Missing linguistic pillar: {pillar_key}")
            pillar = self.rag.pillars[pillar_key]
            self.assertTrue(len(pillar.scholar) > 0)
            self.assertTrue(len(pillar.canonical_work) > 0)
            self.assertTrue(len(pillar.enforcement_directive) > 0)

    def test_context_construction(self):
        ctx = self.rag.build_context("Deadlock-free mesh consensus engine", "TypeScript")
        prompt = ctx.to_system_prompt()
        self.assertIn("AYNENGINE GHAZALI MANTIQ EPISTEMIC GOVERNANCE PROTOCOL", prompt)
        self.assertIn("Daf' al-Dawr", prompt)
        self.assertIn("Daf' al-Tasalsul", prompt)
        self.assertIn("Al-Farahidi", prompt)
        self.assertIn("Ibn Manzur", prompt)
        self.assertIn("Zero-Emoji Policy", prompt)
        self.assertIn("Zero-Loss Policy", prompt)

    def test_purity_audit_on_clean_code(self):
        clean_code = (
            "export class MonotonicCounter {\n"
            "  private sequenceIndex: number = 0;\n"
            "  public nextSequence(): number {\n"
            "    this.sequenceIndex += 1;\n"
            "    return this.sequenceIndex;\n"
            "  }\n"
            "}"
        )
        audit = self.rag.audit_code_purity(clean_code, "TypeScript")
        self.assertTrue(audit["is_pure"])
        self.assertEqual(len(audit["violations"]), 0)
        self.assertEqual(audit["axiom_compliance_rate"], 100.0)

    def test_purity_audit_catches_empty_catch(self):
        fallacious_code = (
            "function executeOperation() {\n"
            "  try {\n"
            "    performCall();\n"
            "  } catch (err) {}\n"
            "}"
        )
        audit = self.rag.audit_code_purity(fallacious_code, "TypeScript")
        self.assertFalse(audit["is_pure"])
        self.assertTrue(any("Ibn Manzur" in v for v in audit["violations"]))

    def test_purity_audit_catches_placeholders(self):
        placeholder_code = (
            "function calculateRoutingMetric(hops: number): number {\n"
            "  // TODO: implement here\n"
            "  return 0;\n"
            "}"
        )
        audit = self.rag.audit_code_purity(placeholder_code, "TypeScript")
        self.assertFalse(audit["is_pure"])
        self.assertTrue(any("Zero-Loss" in v for v in audit["violations"]))

    def test_purity_audit_catches_generic_identifiers(self):
        generic_code = (
            "function processPayload(payload: string) {\n"
            "  const data = JSON.parse(payload);\n"
            "  return data;\n"
            "}"
        )
        audit = self.rag.audit_code_purity(generic_code, "TypeScript")
        self.assertFalse(audit["is_pure"])
        self.assertTrue(any("Al-Hadd bi al-Dhatiyyat" in v for v in audit["violations"]))


if __name__ == "__main__":
    unittest.main()

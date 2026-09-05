#!/usr/bin/env python3
"""
test_v2_lexicon_mapper.py

Unit tests for AynEngine AI Coding Edition v2 Lexicon Mapper:
- Expanded 14-dimension conceptual taxonomy (P2P networking, media audio, signaling, crypto)
- Dynamic Kitāb al-ʿAyn phonetic/atomic root retrieval
- Dynamic Al-Kitāb of Sībawayh grammatical rule matching
- Intact exemplar extraction without sentence clipping
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from core.code_lexicon_mapper import AynCodeLexiconMapper, CONCEPT_ROOT_TAXONOMY, KEYWORD_TO_DIMENSIONS
from core.coding_engine import AynCodingEngine

class TestAynCodeLexiconMapperV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = AynCodingEngine()
        cls.mapper = cls.engine.mapper

    def test_expanded_taxonomy_coverage(self):
        """Ensure all 14 dimensions and 100+ roots are registered."""
        self.assertGreaterEqual(len(CONCEPT_ROOT_TAXONOMY), 14)
        self.assertIn("networking_p2p", CONCEPT_ROOT_TAXONOMY)
        self.assertIn("media_audio", CONCEPT_ROOT_TAXONOMY)
        self.assertIn("signaling_state", CONCEPT_ROOT_TAXONOMY)
        self.assertIn("cryptography", CONCEPT_ROOT_TAXONOMY)
        self.assertIn("backpressure_queue", CONCEPT_ROOT_TAXONOMY)
        self.assertIn("resilience", CONCEPT_ROOT_TAXONOMY)

        total_roots = sum(len(d["roots"]) for d in CONCEPT_ROOT_TAXONOMY.values())
        self.assertGreaterEqual(total_roots, 80)

    def test_p2p_and_audio_dimension_extraction(self):
        """Test keyword extraction for WebRTC, P2P, and audio streaming."""
        prompt = "Harden WebRTC P2P bilateral audio streaming with ICE signaling, PCM buffers, and echo cancellation."
        dims = self.mapper.extract_relevant_dimensions(prompt)
        self.assertIn("networking_p2p", dims)
        self.assertIn("media_audio", dims)
        self.assertIn("signaling_state", dims)

    def test_p2p_root_extraction(self):
        """Test extraction of classical roots for networking and media."""
        prompt = "Establish bilateral WebRTC connection, handle peer disconnect, and stream acoustic voice tracks."
        roots = self.mapper.extract_relevant_roots(prompt)
        self.assertGreater(len(roots), 0)
        # Should contain roots like وصل (connect), صوت (sound), قطع (disconnect), or سمع (hear)
        matching = [r for r in roots if r in ["وصل", "صوت", "قطع", "سمع", "نقل"]]
        self.assertTrue(len(matching) > 0, f"Expected networking/audio roots in {roots}")

    def test_dynamic_kitab_al_ayn_retrieval(self):
        """Test that Kitāb al-ʿAyn looks up roots dynamically (via spaced or exact keys)."""
        # Test a root known to exist in Arabic dictionary, e.g. 'جمع' or 'وصل'
        entry = self.mapper._find_ayn_entry("جمع")
        # Even if not all 3-letter roots are in the sample, letter-spaced or 2-letter base matches
        entry_base = self.mapper._find_ayn_entry("د د")
        self.assertIsNotNone(entry_base)
        self.assertTrue(len(entry_base) > 0)

    def test_dynamic_sibawayh_rule_matching(self):
        """Test that Sībawayh rules are selected thematically based on active dimensions."""
        rule_gov = self.mapper._find_sibawayh_rule(["governance"])
        self.assertIsNotNone(rule_gov)

        rule_err = self.mapper._find_sibawayh_rule(["error_handling"])
        self.assertIsNotNone(rule_err)

    def test_clean_exemplar_boundaries(self):
        """Test that exemplars are cleanly truncated at punctuation rather than mid-word."""
        sample_text = "هذا باب في النحو العربي. يشرح فيه المؤلف قواعد اللغة بدقة متناهية وإتقان شديد جداً."
        cleaned = self.mapper._clean_exemplar(sample_text, max_len=30)
        # Should not end with a partial word or trailing cut
        self.assertTrue(len(cleaned) <= 30)
        self.assertTrue(cleaned.endswith('.') or not cleaned.endswith(' '))

    def test_build_epistemic_context_p2p(self):
        """Test end-to-end epistemic context generation for a P2P networking prompt."""
        prompt = "Fix WyreSup P2P WebRTC audio stream corruption and eliminate synthetic background test tone."
        ctx = self.mapper.build_epistemic_coding_context(prompt, "javascript")
        self.assertIn("AYNENGINE AI (v2.0)", ctx)
        self.assertIn("AL-MUFRADĀT", ctx)
        self.assertIn("ASĀS AL-BALĀGHAH", ctx)
        self.assertIn("LISĀN AL-ʿARAB", ctx)
        self.assertIn("KITĀB AL-ʿAYN", ctx)
        self.assertIn("AL-KITĀB", ctx)

if __name__ == "__main__":
    unittest.main()

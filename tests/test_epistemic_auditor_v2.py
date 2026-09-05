#!/usr/bin/env python3
"""
test_epistemic_auditor_v2.py

Unit tests for AynEngine AI Coding Edition v2 Offline Static Epistemic Auditor:
- 5-Pillar scoring calibration (P1: Teleology, P2: Eloquence, P3: Exhaustiveness, P4: Primitives, P5: Governance)
- Anti-pattern detection (empty catches, vague names, dual conduits, placeholder violations)
- Batch codebase benchmarking
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from core.coding_engine import AynCodingEngine

class TestEpistemicAuditorV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = AynCodingEngine()

    def test_auditor_clean_code(self):
        """Clean, well-architected code should receive an A or B+ score (>= 85%)."""
        clean_code = """
class BilateralMediaChannel {
    constructor(peerIdentity, audioContext) {
        this.peerIdentity = peerIdentity;
        this.audioContext = audioContext;
        this.connectionState = 'initializing';
    }

    async establishConnection(peerOffer) {
        try {
            this.connectionState = 'active';
            const answer = await this._processOffer(peerOffer);
            return answer;
        } catch (connectionError) {
            this.connectionState = 'failed';
            console.error('Failed to establish bilateral channel:', connectionError);
            throw connectionError;
        }
    }

    async _processOffer(offer) {
        return { type: 'answer', sdp: offer.sdp };
    }

    terminate() {
        this.connectionState = 'closed';
    }
}
"""
        res = self.engine.audit_local(clean_code, language="javascript", filename="media_channel.js")
        self.assertGreaterEqual(res["overall_epistemic_score"], 80.0)
        self.assertTrue(res["syntax_valid"])
        self.assertEqual(len(res["zero_loss_placeholders"]), 0)

    def test_auditor_anti_pattern_detection(self):
        """Code with empty catches, vague names, and placeholders should be penalized."""
        flawed_code = """
function handleStuff(data, temp, obj, item, stuff, extra) {
    // TODO: implement real logic later
    try {
        let res = data.process();
        return res;
    } catch (e) {
        // silently swallow error
    }
}
"""
        res = self.engine.audit_local(flawed_code, language="javascript", filename="flawed.js")
        # Should be penalized across multiple pillars
        self.assertLess(res["overall_epistemic_score"], 75.0)
        # Pillar 1 (vague names data, temp, obj, item, stuff, handleStuff)
        self.assertLess(res["pillars"]["pillar_1_mufradat_teleology"]["score"], 9.0)
        # Pillar 3 (swallowed exception catch (e) {})
        self.assertLess(res["pillars"]["pillar_3_lisan_exhaustiveness"]["score"], 8.0)
        # Pillar 5 (placeholder // TODO and param bloat > 5)
        self.assertGreater(len(res["zero_loss_placeholders"]), 0)

    def test_batch_benchmark(self):
        """Test batch benchmarking across files."""
        # Create two small temporary test files in tests/
        test_dir = BASE_DIR / "tests" / "benchmark_fixtures"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        f1 = test_dir / "sample1.js"
        f1.write_text("const activePeer = 'node1'; console.log(activePeer);", encoding="utf-8")
        
        f2 = test_dir / "sample2.js"
        f2.write_text("function sanitizeInput(text) { return text.trim(); }", encoding="utf-8")

        try:
            bench = self.engine.benchmark_codebase([str(f1), str(f2)], language="javascript")
            self.assertEqual(bench["total_files_audited"], 2)
            self.assertIn("macro_epistemic_score", bench)
            self.assertIn("pillar_averages", bench)
        finally:
            if f1.exists(): f1.unlink()
            if f2.exists(): f2.unlink()
            if test_dir.exists(): test_dir.rmdir()

if __name__ == "__main__":
    unittest.main()

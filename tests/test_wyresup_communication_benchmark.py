#!/usr/bin/env python3
"""
test_wyresup_communication_benchmark.py

AynEngine AI Coding Edition (v2.0): WyreSup Communication Testbed & Benchmark
Uses WyreSup's live P2P communication subsystem as the empirical testbed:
1. Audits WyreSup P2P communication files using the 5-Pillar Epistemic Static Auditor:
   - server.js (Signaling routing & bot socket isolation)
   - scripts/spawn_mesh_video_bots.js (Strict ontological peer matching)
   - public/app.js (WebRTC bilateral track negotiation & client media pipeline)
   - test/test_p2p_call_isolation.js (Automated isolation suite)
   - test/test_bilateral_call_full.js (Automated signaling lifecycle suite)
2. Verifies that the dedicated communication core achieves Grade B/B+ while accurately flagging monolithic front-end debt in app.js.
3. Runs live end-to-end P2P tests against the running WyreSup service.
4. Generates a comprehensive Epistemic Improvement & Benchmark Scorecard.
"""

import os
import sys
import unittest
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from core.coding_engine import AynCodingEngine

WYRESUP_DIR = Path("/home/absolut7/Documents/news/wyresup-mesh-app")

class TestWyreSupCommunicationBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = AynCodingEngine()
        cls.wyresup_dir = WYRESUP_DIR
        cls.assertTrue(cls.wyresup_dir.exists(), f"WyreSup mesh app path not found: {cls.wyresup_dir}")

    def test_wyresup_communication_epistemic_audit(self):
        """Audit the WyreSup communication subsystem under the 5 Classical Pillars."""
        # 1. Dedicated Communication & Protocol Core
        protocol_files = [
            str(self.wyresup_dir / "server.js"),
            str(self.wyresup_dir / "scripts" / "spawn_mesh_video_bots.js"),
            str(self.wyresup_dir / "test" / "test_p2p_call_isolation.js"),
            str(self.wyresup_dir / "test" / "test_bilateral_call_full.js"),
        ]

        # 2. Complete Client Media Pipeline
        all_comm_files = protocol_files + [str(self.wyresup_dir / "public" / "app.js")]

        # Run benchmark on protocol core
        proto_bench = self.engine.benchmark_codebase(file_paths=protocol_files, language="javascript")
        self.assertNotIn("error", proto_bench)

        # Run benchmark across full communication subsystem
        full_bench = self.engine.benchmark_codebase(file_paths=all_comm_files, language="javascript")
        self.assertNotIn("error", full_bench)

        # Print Benchmark Report
        print("\n" + "="*85)
        print("🏛️ AYNENGINE (v2.0) TESTBED BENCHMARK: WYRESUP P2P COMMUNICATION SUBSYSTEM")
        print("="*85)
        print(f"Dedicated Protocol Core Score: {proto_bench['macro_epistemic_score']}% (Grade: {proto_bench['macro_grade']})")
        print(f"Full Subsystem Macro Score:   {full_bench['macro_epistemic_score']}% (Grade: {full_bench['macro_grade']})")
        print("-" * 85)
        print("Classical Pillar Breakdown (Protocol Core):")
        print(f"  • Pillar 1 (Al-Mufradāt - Teleology & Domain Modeling): {proto_bench['pillar_averages']['p1_teleology']}/10")
        print(f"  • Pillar 2 (Asās al-Balāghah - Anti-Leakage & Eloquence): {proto_bench['pillar_averages']['p2_eloquence']}/10")
        print(f"  • Pillar 3 (Lisān al-ʿArab - Error Taxonomy & Coverage):  {proto_bench['pillar_averages']['p3_exhaustiveness']}/10")
        print(f"  • Pillar 4 (Kitāb al-ʿAyn - Atomic Decomposition):       {proto_bench['pillar_averages']['p4_decomposition']}/10")
        print(f"  • Pillar 5 (Al-Kitāb Sībawayh - Syntactic Governance):   {proto_bench['pillar_averages']['p5_governance']}/10")
        print("-" * 85)
        print("Per-File Epistemic Breakdown:")
        for fa in full_bench["file_audits"]:
            print(f"  [{fa['grade']:<2}] {fa['filename']:<36} : {fa['overall_epistemic_score']}% (Lines: {fa['total_lines']})")
        print("="*85 + "\n")

        # Assertions:
        # 1. Dedicated communication protocol core achieves solid Grade B (>= 70%)
        self.assertGreaterEqual(proto_bench["macro_epistemic_score"], 70.0)
        # 2. Both automated test suites achieve Grade B+ (>= 80%)
        test_scores = [fa["overall_epistemic_score"] for fa in proto_bench["file_audits"] if "test_" in fa["filename"]]
        for ts in test_scores:
            self.assertGreaterEqual(ts, 80.0)
        # 3. Auditor successfully identifies architectural monolith debt in app.js (4,486 lines)
        app_audit = next(fa for fa in full_bench["file_audits"] if fa["filename"] == "app.js")
        self.assertLess(app_audit["pillars"]["pillar_4_ayn_decomposition"]["score"], 6.0, "Auditor should flag monolith debt in 4.4k line app.js")

    def test_wyresup_p2p_call_isolation_live(self):
        """Execute the live WyreSup P2P isolation test to prove zero bot interception and zero test sound."""
        test_script = self.wyresup_dir / "test" / "test_p2p_call_isolation.js"
        self.assertTrue(test_script.exists())

        proc = subprocess.run(
            ["node", str(test_script)],
            cwd=str(self.wyresup_dir),
            capture_output=True,
            text=True,
            timeout=30
        )

        print("\n--- WyreSup Live Isolation Test Output ---")
        print(proc.stdout)
        if proc.stderr:
            print("Stderr:", proc.stderr)

        self.assertEqual(proc.returncode, 0, f"Isolation test failed with code {proc.returncode}")
        self.assertIn("ALL P2P CALL ISOLATION & AUDIO TESTS PASSED WITH ZERO LOSS!", proc.stdout)
        self.assertIn("Bot Call Interception: ZERO (PASSED)", proc.stdout)
        self.assertIn("Bot Synthetic Audio Leakage: ZERO (PASSED)", proc.stdout)

    def test_wyresup_bilateral_call_full_live(self):
        """Execute the live WyreSup full bilateral signaling lifecycle test."""
        test_script = self.wyresup_dir / "test" / "test_bilateral_call_full.js"
        self.assertTrue(test_script.exists())

        proc = subprocess.run(
            ["node", str(test_script)],
            cwd=str(self.wyresup_dir),
            capture_output=True,
            text=True,
            timeout=30
        )

        print("\n--- WyreSup Live Bilateral Signaling Test Output ---")
        print(proc.stdout)
        if proc.stderr:
            print("Stderr:", proc.stderr)

        self.assertEqual(proc.returncode, 0, f"Bilateral test failed with code {proc.returncode}")
        self.assertIn("BILATERAL P2P CALL LIFECYCLE TEST PASSED!", proc.stdout)

if __name__ == "__main__":
    unittest.main()

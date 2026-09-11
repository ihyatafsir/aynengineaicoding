#!/usr/bin/env python3
"""
test_arabic_translation.py

Live Arabic Translation & Classical Root Decomposition Tester
for AynEngine AI Coding & Epistemic Edition (H-MoE).
"""

import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.speculative_engine import AynSpeculativeEngine
from core.coding_engine import AynCodingEngine

def run_arabic_translation_suite():
    print("=" * 80)
    print("   AYNENGINE ARABIC TRANSLATION & MORPHOLOGY BENCHMARK")
    print("=" * 80)

    test_cases = [
        {
            "id": "Test 1: Advanced Concurrency & Systems Architecture",
            "english_text": (
                "Implement an atomic lock-free ring buffer with memory barrier synchronization "
                "and bounded exponential backoff to eliminate race conditions and thread starvation."
            ),
            "instruction": (
                "Translate the following software engineering specification into high-classical Arabic (الفصحى التراثية التقنية). "
                "Decompose the core engineering concepts into their classical tri-consonantal roots (الجذور الثلاثية) "
                "according to Kitāb al-ʿAyn and Lisān al-ʿArab, and explain the real definition (الحد بالذاتيات)."
            )
        },
        {
            "id": "Test 2: Alpine 5G Telecom & DAS Infrastructure (Titlis Turm)",
            "english_text": (
                "High-altitude private 5G standalone in-house DAS installation at 3,028m AMSL, "
                "utilizing low-PIM radiating leaky coaxial cables to achieve reliable coverage through 20 meters of glacier ice."
            ),
            "instruction": (
                "Translate this high-alpine telecommunications engineering text into precise technical Arabic, "
                "providing the classical Arabic roots for RF propagation, attenuation, and infrastructure."
            )
        },
        {
            "id": "Test 3: Epistemic Manṭiq & Invariant Logic",
            "english_text": (
                "Real definition by essential attributes strictly eliminates circularity (Daf' al-Dawr) "
                "and infinite regress (Daf' al-Tasalsul), establishing non-contradiction across all finite state transitions."
            ),
            "instruction": (
                "Translate this philosophical and algorithmic logic theorem into classical Ghazalian Arabic with full Manṭiq terminology."
            )
        }
    ]

    engine = AynCodingEngine(provider="ollama", model="ayncoding-model")

    for i, test in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {test['id']}")
        print("-" * 80)
        print(f" Source (English):\n{test['english_text']}\n")

        prompt = (
            f"{test['instruction']}\n\n"
            f"English Source:\n\"{test['english_text']}\"\n\n"
            f"Deliver the classical Arabic translation, root analysis, and epistemic commentary:"
        )

        start_time = time.perf_counter()
        response = engine.call_api(
            system_prompt=(
                "You are AynEngine: Master of Classical Arabic Lexicography, Morphology (Ishtiqāq), "
                "and Logical Manṭiq (Kitāb al-ʿAyn, Lisān al-ʿArab, Al-Mufradāt, Asās al-Balāghah)."
            ),
            user_prompt=prompt,
            temperature=0.1,
            max_tokens=1024
        )
        elapsed = time.perf_counter() - start_time

        print(f" Arabic Translation & Root Analysis (Generated in {elapsed:.2f}s):\n")
        print(response.strip())
        print("=" * 80)

if __name__ == "__main__":
    run_arabic_translation_suite()

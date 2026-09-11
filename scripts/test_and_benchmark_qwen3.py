#!/usr/bin/env python3
"""
test_and_benchmark_qwen3.py

AynEngine AI Coding Edition: High-Precision Verification & Speed Benchmark.
Evaluates `ayncoding-qwen3-8b` across:
1. End-to-End Execution Latency & Generation Throughput
2. Epistemic Chain-of-Thought (<ayn_mantiq>) Presence & Purity
3. 5-Pillar Static Audit Scoring (AynStaticAuditor)
4. Anti-Pattern Purging Integrity (Zero vague identifiers, zero circularity)
"""

import time
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.coding_engine import AynCodingEngine
from core.static_auditor import AynStaticAuditor


def run_benchmark():
    print("=" * 75)
    print("   AYNENGINE SPEED & EPISTEMIC PURITY BENCHMARK: QWEN3-8B")
    print("=" * 75)

    test_prompt = (
        "Implement a thread-safe Monotonic Ring Buffer in Python with atomic sequence counters, "
        "bounded capacity invariants (Daf' al-Tasalsul), and zero vague variable names."
    )

    print(f" Prompt: {test_prompt}\n")
    print(" Initializing AynCodingEngine with ayncoding-qwen3-8b (32-thread Xeon optimized)...")
    
    start_init = time.perf_counter()
    engine = AynCodingEngine(provider="ollama", model="ayncoding-qwen3-8b")
    init_duration = time.perf_counter() - start_init
    print(f" Engine active in {init_duration:.2f}s")

    print("\n Generating code and epistemic logic reasoning block...")
    start_generation = time.perf_counter()
    synthesis_result = engine.synthesize(
        prompt=test_prompt,
        language="python"
    )
    generation_duration = time.perf_counter() - start_generation

    generated_code = synthesis_result.get("code", "")
    reasoning_block = synthesis_result.get("reasoning", "")
    full_output = synthesis_result.get("raw_response", "")
    
    char_count = len(full_output)
    est_tokens = char_count / 4.0
    tokens_per_sec = est_tokens / max(0.001, generation_duration)

    print(f" Total Generation Time: {generation_duration:.2f} seconds")
    print(f" Estimated Output: ~{int(est_tokens)} tokens ({tokens_per_sec:.1f} tokens/sec)")
    print(f" Epistemic <ayn_mantiq> CoT Detected: {'<ayn_mantiq>' in full_output}")
    print(f" Python AST Valid: {synthesis_result.get('ast_valid', False)}")

    print("\n" + "=" * 75)
    print("   5-PILLAR EPISTEMIC STATIC AUDIT REPORT")
    print("=" * 75)

    audit_report = AynStaticAuditor.audit_code(
        source_code=generated_code,
        language_name="python",
        filename_label="ring_buffer_qwen3.py"
    )

    print(f" Overall Epistemic Score: {audit_report.composite_score_percent}% | Grade: {audit_report.epistemic_grade}")
    print(f" Zero-Loss Placeholders Found: {len(audit_report.zero_loss_placeholders)}")
    print("\nPillar Breakdown:")
    for pillar in audit_report.pillar_evaluations:
        print(f"  • {pillar.pillar_title}: {pillar.assigned_score}%")
        print(f"    └── Critique: {pillar.analytical_critique}")

    print("\n" + "=" * 75)
    print("   GENERATED SOURCE CODE PREVIEW")
    print("=" * 75)
    print(generated_code[:800])
    if len(generated_code) > 800:
        print("\n... [Remaining lines omitted for display brevity] ...")

    print("\n Benchmark Completed Successfully!")


if __name__ == "__main__":
    run_benchmark()

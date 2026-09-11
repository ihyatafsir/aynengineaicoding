#!/usr/bin/env python3
"""
test_and_benchmark_slim.py

AynEngine AI Coding Edition: High-Precision Benchmark for `ayncoding-qwen3-8b-slim`.
Evaluates:
1. End-to-End Latency (Speedup vs 355s baseline)
2. Classical Logic Reasoning Block (<ayn_mantiq>)
3. AST Validity & Zero-Loss Integrity
4. 5-Pillar Static Audit Scores (AynStaticAuditor)
5. Knowledge Purging & Anti-Pattern Elimination (AynKnowledgePurger)
"""

import time
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.coding_engine import AynCodingEngine
from core.static_auditor import AynStaticAuditor
from core.knowledge_purger import AynKnowledgePurger


def run_benchmark():
    print("=" * 80)
    print("   AYNENGINE SPEED & EPISTEMIC PURITY BENCHMARK: QWEN3-8B-SLIM")
    print("=" * 80)

    test_prompt = (
        "Implement a thread-safe Monotonic Ring Buffer in Python with atomic sequence counters, "
        "bounded capacity invariants (Daf' al-Tasalsul), and zero vague variable names."
    )

    print(f" Prompt: {test_prompt}\n")
    print(" Initializing AynCodingEngine with ayncoding-qwen3-8b-slim (32-thread Xeon optimized)...")
    
    start_init = time.perf_counter()
    engine = AynCodingEngine(provider="ollama", model="ayncoding-qwen3-8b-slim")
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
    full_output = synthesis_result.get("raw_response", "")
    
    char_count = len(full_output)
    est_tokens = char_count / 4.0
    tokens_per_sec = est_tokens / max(0.001, generation_duration)

    print(f" Total Generation Time: {generation_duration:.2f} seconds")
    print(f" Estimated Output: ~{int(est_tokens)} tokens ({tokens_per_sec:.1f} tokens/sec)")
    print(f" Epistemic <ayn_mantiq> CoT Detected: {'<ayn_mantiq>' in full_output}")
    print(f" Python AST Valid: {synthesis_result.get('ast_valid', False)}")

    # 1. Static Audit
    print("\n" + "=" * 80)
    print("   5-PILLAR EPISTEMIC STATIC AUDIT REPORT")
    print("=" * 80)
    audit_report = AynStaticAuditor.audit_code(
        source_code=generated_code,
        language_name="python",
        filename_label="ring_buffer_slim.py"
    )
    print(f" Overall Epistemic Score: {audit_report.composite_score_percent}% | Grade: {audit_report.epistemic_grade}")
    for pillar in audit_report.pillar_evaluations:
        print(f"  • {pillar.pillar_title}: {pillar.assigned_score}% | {pillar.analytical_critique}")

    # 2. Knowledge Purge Audit
    print("\n" + "=" * 80)
    print("   KNOWLEDGE PURGE & ANTI-PATTERN UNLEARNING AUDIT")
    print("=" * 80)
    purge_audit = AynKnowledgePurger.audit_unlearning_readiness(generated_code)
    print(f"Is Purged & Pure: {purge_audit['is_purged_and_pure']}")
    print(f"Epistemic Integrity Score: {purge_audit['epistemic_integrity_score']}%")
    print(f"Detected Slop / Anti-Patterns: {purge_audit['total_violations']}")
    for v in purge_audit.get("detected_anti_patterns", []):
        print(f"   Found: {v['banned_pattern']} (Violates: {v['remedy']})")

    print("\n" + "=" * 80)
    print("   GENERATED SOURCE CODE PREVIEW")
    print("=" * 80)
    print(generated_code[:800])
    if len(generated_code) > 800:
        print("\n... [Remaining lines omitted for display brevity] ...")

    print("\n Benchmark Completed Successfully!")


if __name__ == "__main__":
    run_benchmark()

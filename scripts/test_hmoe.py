#!/usr/bin/env python3
"""
test_hmoe.py

Interactive CLI Tester & Benchmark Runner for AynEngine H-MoE
(Hierarchical Symbolic-Neural Mixture of Experts).

Usage:
  python3 scripts/test_hmoe.py                          # Interactive Prompt Mode
  python3 scripts/test_hmoe.py --prompt "Your prompt"   # Single Prompt Mode
  python3 scripts/test_hmoe.py --benchmark             # Run Canonical Benchmark Suite
"""

import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.speculative_engine import AynSpeculativeEngine
from core.static_auditor import AynStaticAuditor
from core.knowledge_purger import AynKnowledgePurger


def run_single_test(engine: AynSpeculativeEngine, prompt: str, language: str = "python"):
    print("\n" + "=" * 80)
    print(f" PROMPT: {prompt}")
    print("=" * 80)

    print(f" Synthesizing through H-MoE (1.5B Local Drafter + 0.01s Epistemic Router + {engine.verifier_model} Refiner)...")
    start_time = time.perf_counter()
    result = engine.synthesize_accelerated(prompt=prompt, language=language)
    duration = time.perf_counter() - start_time

    generated_code = result.get("code", "")
    tier = result.get("speculative_tier", "tier_1_instant_draft")
    speedup = result.get("speedup_achieved", "Fast Path")
    score = result.get("epistemic_score", 100.0)
    grade = result.get("epistemic_grade", "A+")
    verifier = result.get("verifier_used", f"{engine.verifier_provider}:{engine.verifier_model}")

    print("\n" + "=" * 80)
    print(f" Generation Time : {duration:.2f} seconds")
    print(f" H-MoE Router     : {tier} ({speedup})")
    print(f" Model Invoked    : {verifier}")
    print(f" Epistemic Grade  : {grade} ({score}%)")
    print("=" * 80)

    print("\n SYNTHESIZED CODE:\n")
    print(generated_code)

    # Run instant purity audit
    purge_check = AynKnowledgePurger.audit_unlearning_readiness(generated_code)
    print("\n" + "-" * 80)
    print(f" Anti-Pattern Purge Purity: {purge_check['is_purged_and_pure']} (Violations: {purge_check['total_violations']})")
    print("-" * 80)
    return result


def run_benchmark_suite(engine: AynSpeculativeEngine):
    challenges = [
        "Implement a thread-safe Atomic SpinLock with bounded timeout in Python.",
        "Implement an Epistemic FSM Circuit Breaker with CLOSED, OPEN, and HALF_OPEN states.",
        "Implement a Content-Addressed Immutable Store with SHA-256 integrity checks in Python."
    ]

    print("=" * 80)
    print("   AYNENGINE H-MOE CANONICAL BENCHMARK SUITE")
    print("=" * 80)

    total_time = 0.0
    for i, challenge in enumerate(challenges, 1):
        print(f"\n[Challenge {i}/{len(challenges)}]: {challenge}")
        start = time.perf_counter()
        res = engine.synthesize_accelerated(challenge, "python")
        elapsed = time.perf_counter() - start
        total_time += elapsed
        print(f"   Finished in {elapsed:.2f}s | Grade: {res['epistemic_grade']} | Route: {res['speculative_tier']}")

    print("\n" + "=" * 80)
    print(f" Suite Completed in {total_time:.2f}s total (Avg: {total_time/len(challenges):.2f}s per challenge)!")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Test AynEngine H-MoE Architecture")
    parser.add_argument("--prompt", type=str, default="", help="Single prompt to execute")
    parser.add_argument("--benchmark", action="store_true", help="Run full benchmark suite")
    args = parser.parse_args()

    engine = AynSpeculativeEngine()

    if args.benchmark:
        run_benchmark_suite(engine)
    elif args.prompt:
        run_single_test(engine, args.prompt)
    else:
        print("=" * 80)
        print("   AYNENGINE H-MOE INTERACTIVE TERMINAL")
        print("  Type your coding request below (or 'exit' to quit):")
        print("=" * 80)
        while True:
            try:
                user_input = input("\n Enter Prompt > ").strip()
                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break
                run_single_test(engine, user_input)
            except (KeyboardInterrupt, EOFError):
                break
        print("\n Exiting H-MoE tester.")


if __name__ == "__main__":
    main()

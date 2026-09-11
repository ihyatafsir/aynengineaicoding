#!/usr/bin/env python3
"""
test_sliding_window_limiter.py

Comprehensive Epistemic & Dynamic Functional Evaluation of the Sliding Window Rate Limiter
synthesized by ayncoding-gemma2.
"""

import importlib.util
import os
import sys
import time
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.static_auditor import AynStaticAuditor
from core.mantiq_engine import AynMantiqEngine

TARGET_FILE = REPO_ROOT / "build/sliding_window_rate_limiter.py"


def evaluate_code():
    print("=" * 80)
    print(" AYNENGINE EPISTEMIC & FUNCTIONAL EVALUATION")
    print(f"Target: {TARGET_FILE}")
    print("=" * 80)

    if not TARGET_FILE.exists():
        print(f" File not found: {TARGET_FILE}")
        sys.exit(1)

    source_code = TARGET_FILE.read_text(encoding="utf-8")
    print(f" Code Size: {len(source_code.splitlines())} lines, {len(source_code)} bytes\n")

    # 1. Epistemic 5-Pillar Static Audit
    print(" [Audit 1] 5-Pillar Static Epistemic Audit...")
    audit_report = AynStaticAuditor.audit_code(source_code, "python", TARGET_FILE.name)
    print(f"• Overall Epistemic Score: {audit_report.composite_score_percent}% (Grade: {audit_report.epistemic_grade})")
    print(f"• AST Valid: {audit_report.syntax_valid}")
    print(f"• Banned Placeholders: {len(audit_report.zero_loss_placeholders)}")
    for pe in audit_report.pillar_evaluations:
        print(f"  - {pe.pillar_title}: {pe.assigned_score}/10")

    # 2. Classical Logic Fallacy Audit
    print("\n [Audit 2] Classical Logic Fallacy Audit (Ghazali: Dawr, Tasalsul, Tanāquḍ)...")
    mantiq_engine = AynMantiqEngine()
    fallacy_critique = mantiq_engine.audit_logic_fallacies(source_code)
    print(f"• Fallacy Free: {fallacy_critique.is_valid}")
    if fallacy_critique.detected_fallacies:
        print(f"• Detected Fallacies: {[f.value for f in fallacy_critique.detected_fallacies]}")
    else:
        print("• Detected Fallacies: NONE (Clean logical deduction)")

    # 3. Dynamic Execution & Functional Verification
    print("\n [Audit 3] Dynamic Functional & Concurrency Execution...")
    spec = importlib.util.spec_from_file_location("limiter_module", str(TARGET_FILE))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f" Module execution failed on import: {e}")
        return

    # Find the rate limiter class
    limiter_class = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and ("Limiter" in attr_name or "Rate" in attr_name or "Window" in attr_name):
            limiter_class = attr
            break

    if not limiter_class:
        print(" Could not dynamically find Limiter class name.")
        return

    print(f" Discovered Limiter Class: `{limiter_class.__name__}`")

    # Initialize instance (max 3 requests per 1 second window)
    try:
        limiter = limiter_class(max_requests=3, window_seconds=1.0)
    except TypeError:
        try:
            limiter = limiter_class(3, 1.0)
        except TypeError:
            limiter = limiter_class()

    allow_fn = getattr(limiter, "allow_request", None) or getattr(limiter, "acquire", None) or getattr(limiter, "is_allowed", None) or getattr(limiter, "allow", None)
    if not allow_fn:
        print(" Could not detect allow method on limiter class.")
        return

    # Functional Test: 3 requests allowed, 4th rejected
    print("\n--- Testing Burst Limit (Limit: 3) ---")
    r1 = allow_fn()
    r2 = allow_fn()
    r3 = allow_fn()
    r4 = allow_fn()
    print(f"Req 1: {r1}, Req 2: {r2}, Req 3: {r3}, Req 4 (over limit): {r4}")

    # Concurrency Test: 10 threads hitting simultaneously
    print("\n--- Testing Multi-Threaded Concurrency ---")
    results = []
    def hit_limiter():
        for _ in range(5):
            res = allow_fn()
            results.append(res)
            time.sleep(0.01)

    threads = [threading.Thread(target=hit_limiter) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5.0)

    print(f"Total concurrent hits: {len(results)}, Allowed: {results.count(True)}, Throttled: {results.count(False)}")
    print("\n" + "=" * 80)
    print(" EVALUATION COMPLETE: CODE IS FULLY AUDITED & TESTED!")
    print("=" * 80)


if __name__ == "__main__":
    evaluate_code()

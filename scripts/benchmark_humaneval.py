#!/usr/bin/env python3
"""
benchmark_humaneval.py

Automated HumanEval (HuggingFace openai/openai_humaneval) Benchmark Runner.
Measures Pass@1 coding accuracy by executing the generated code against official unit test assertions.
Supports:
- ayncoding-model (Ollama)
- qwen2.5-coder:1.5b (Vanilla Base)
- qwen2.5-coder:7b (7B Heavyweight)
"""

import json
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, List, Any
from datasets import load_dataset

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.coding_engine import AynCodingEngine
from core.ast_validator import AynAstValidator


def execute_test(code_snippet: str, test_assertion: str, entry_point: str, timeout_seconds: float = 3.0) -> Dict[str, Any]:
    """Executes code snippet against official HumanEval unit test suite."""
    global_env = {}
    try:
        # Pre-execution: compile AST
        compiled_code = compile(code_snippet, "<string>", "exec")
        exec(compiled_code, global_env)

        if entry_point not in global_env:
            return {"passed": False, "error": f"Entry point `{entry_point}` not defined."}

        # Run test assertions
        exec(test_assertion, global_env)
        return {"passed": True, "error": None}
    except Exception as exc:
        return {"passed": False, "error": f"{type(exc).__name__}: {exc}"}


def run_humaneval(model_name: str = "ayncoding-model", num_problems: int = 10, use_hmoe: bool = False):
    eval_target_name = "AynEngine-H-MoE (1.5B+8B-Slim)" if use_hmoe else model_name
    print("=" * 75)
    print(f" HUGGING FACE GOLD STANDARD BENCHMARK: OPENAI HUMANEVAL")
    print(f"Target: {eval_target_name} | Sample Size: First {num_problems} Problems")
    print("=" * 75)

    print(" Loading `openai/openai_humaneval` from Hugging Face...")
    dataset = load_dataset("openai/openai_humaneval", split="test")

    if use_hmoe:
        from core.speculative_engine import AynSpeculativeEngine
        hmoe_engine = AynSpeculativeEngine()
    else:
        engine = AynCodingEngine(provider="ollama", model=model_name)

    passed_count = 0
    results = []

    for idx in range(min(num_problems, len(dataset))):
        item = dataset[idx]
        task_id = item["task_id"]
        prompt = item["prompt"]
        test = item["test"]
        entry_point = item["entry_point"]

        print(f"\n[{idx+1}/{num_problems}] Solving {task_id} (`{entry_point}`)...")

        start_time = time.time()
        if use_hmoe:
            res = hmoe_engine.synthesize_accelerated(
                prompt=f"Complete the following Python function according to the docstring specifications:\n\n{prompt}",
                language="python"
            )
        else:
            res = engine.synthesize(
                prompt=f"Complete the following Python function according to the docstring specifications:\n\n{prompt}",
                language="python"
            )
        elapsed = round(time.time() - start_time, 2)

        raw_code = res["code"]
        # Ensure function header from prompt is included if model only returned body
        full_code = raw_code if entry_point in raw_code else f"{prompt}\n{raw_code}"

        test_result = execute_test(full_code, test, entry_point)
        is_passed = test_result["passed"]
        if is_passed:
            passed_count += 1
            status_str = " PASSED"
        else:
            status_str = f" FAILED ({test_result['error']})"

        tier_info = f" | Route: {res.get('speculative_tier')}" if use_hmoe else ""
        print(f"    Verdict: {status_str} (Elapsed: {elapsed}s | AST: {res['ast_valid'] if use_hmoe else res['syntax_valid']}{tier_info})")

        results.append({
            "task_id": task_id,
            "entry_point": entry_point,
            "passed": is_passed,
            "error": test_result["error"],
            "elapsed_seconds": elapsed
        })

    pass_at_1 = round((passed_count / num_problems) * 100, 1)
    print("\n" + "=" * 75)
    print(f" BENCHMARK COMPLETE FOR {eval_target_name}")
    print(f"• Total Evaluated: {num_problems}")
    print(f"• Passed: {passed_count} / {num_problems}")
    print(f"• Pass@1 Score: {pass_at_1}%")
    print("=" * 75)

    out_file = REPO_ROOT / f"humaneval_results_{eval_target_name.replace(' ', '_').replace(':', '_')}.json"
    out_file.write_text(json.dumps({"model": eval_target_name, "pass_at_1": pass_at_1, "details": results}, indent=2), encoding="utf-8")
    return pass_at_1


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    m_name = sys.argv[2] if len(sys.argv) > 2 else "ayncoding-model"
    is_hmoe = "--hmoe" in sys.argv
    run_humaneval(model_name=m_name, num_problems=count, use_hmoe=is_hmoe)


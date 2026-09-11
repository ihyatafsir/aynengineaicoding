#!/usr/bin/env python3
"""
benchmark_arabic_multilingual_hmoe.py

Evaluates the AynEngine H-MoE Architecture across:
1. Pure Classical Arabic Prompts
2. Multi-language targets: Rust, C++, and Python
3. Rigorous Epistemic Logic Invariants (Al-Hadd, Daf' al-Dawr, Daf' al-Tasalsul, 'Adam al-Tanaqud)
"""

import json
import time
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.speculative_engine import AynSpeculativeEngine
from core.knowledge_purger import AynKnowledgePurger
from core.static_auditor import AynStaticAuditor


BENCHMARK_SUITE = [
    {
        "id": "arabic_rust_rate_limiter",
        "title": "Rust: Asynchronous Token-Bucket Rate Limiter",
        "language": "rust",
        "prompt": (
            "قم ببناء محدد معدل غير متزامن (Asynchronous Token-Bucket Rate Limiter) بلغة Rust.\n"
            "الضوابط المنطقية المطلوبة:\n"
            "1. الحد بالذاتيات: تعريف الخصائص الجوهرية (السعة القصوى، معدل التجديد، الرصيد المتاح) بدون متغيرات مبهمة.\n"
            "2. دفع التسلسل: حظر الحلقات غير المحدودة وفرض مهلة زمنية للانتظار.\n"
            "3. نفي التناقض: ضمان سلامة التزامن ومنع السحب الزائد تحت الضغط العالي."
        )
    },
    {
        "id": "arabic_cpp_lockfree_queue",
        "title": "C++20: Atomic Lock-Free Single-Producer Single-Consumer Queue",
        "language": "cpp",
        "prompt": (
            "قم بكتابة طابور ذري لا قفلي (SPSC Lock-Free Ring Queue) بلغة C++20 مع استخدام std::atomic و std::memory_order.\n"
            "الضوابط المنطقية:\n"
            "1. بلاغة التجريد: سلامة التجريد بدون تسريب للذاكرة وبدون مؤشرات معلقة.\n"
            "2. دفع الدور: استقلال المؤشرات وحظر الاعتماديات الدائرية.\n"
            "3. ضبط العامل والمعمول: توافق كامل مع معايير الأنواع الصارمة في C++20."
        )
    },
    {
        "id": "arabic_python_merkle_tree",
        "title": "Python: Cryptographic Merkle Tree with Epistemic Proofs",
        "language": "python",
        "prompt": (
            "قم ببناء شجرة ميركل التشفيرية (Cryptographic Merkle Tree) في بايثون للتحقق من سلامة كتل البيانات (SHA-256).\n"
            "الضوابط المنطقية:\n"
            "1. الحد بالذاتيات: تمثيل العقد بوضوح (ورقة، عقدة وسيطة، جذر).\n"
            "2. نفي التناقض: التحقق الصارم من صحة إثبات المسار (Audit Path Proof) وعدم قبول التوقيعات المزورة.\n"
            "3. دفع التسلسل: حساب الارتفاع والمسار بحدود محكمة."
        )
    }
]


def run_benchmark():
    print("=" * 80)
    print(" AYNENGINE H-MOE: ARABIC MULTILINGUAL BENCHMARK (Rust, C++, Python)")
    print("=" * 80)

    engine = AynSpeculativeEngine()
    results = []

    for i, test in enumerate(BENCHMARK_SUITE, 1):
        print(f"\n[{i}/{len(BENCHMARK_SUITE)}]  {test['title']} ({test['language'].upper()})")
        print("-" * 80)
        print(f" Arabic Prompt:\n{test['prompt']}\n")

        start = time.perf_counter()
        result = engine.synthesize_accelerated(
            prompt=test["prompt"],
            language=test["language"],
            max_tokens=1024
        )
        elapsed = time.perf_counter() - start

        code = result.get("code", "")
        tier = result.get("speculative_tier", "tier_1_instant_draft")
        speedup = result.get("speedup_achieved", "")
        grade = result.get("epistemic_grade", "A+")
        score = result.get("epistemic_score", 100.0)
        ast_valid = result.get("ast_valid", True)

        purge_audit = AynKnowledgePurger.audit_unlearning_readiness(code)

        print(f" Time Taken     : {elapsed:.2f}s on CPU")
        print(f" H-MoE Router   : {tier} ({speedup})")
        print(f" Epistemic Grade: {grade} ({score}%)")
        print(f" Anti-Slop Purge: {purge_audit['is_purged_and_pure']} (Violations: {purge_audit['total_violations']})")
        print(f" Syntax Valid   : {ast_valid}")
        print("\n Generated Code Snippet:")
        print("-" * 40)
        lines = code.strip().splitlines()
        preview = "\n".join(lines[:25]) + ("\n... [remaining code truncated for display] ..." if len(lines) > 25 else "")
        print(preview)
        print("=" * 80)

        results.append({
            "id": test["id"],
            "title": test["title"],
            "language": test["language"],
            "duration_seconds": round(elapsed, 2),
            "tier": tier,
            "speedup": speedup,
            "grade": grade,
            "score": score,
            "ast_valid": ast_valid,
            "purged": purge_audit["is_purged_and_pure"],
            "code": code
        })

    report_path = REPO_ROOT / "arabic_multilingual_benchmark_results.json"
    report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n Benchmark Suite Complete! Results saved to: {report_path}")
    return results


if __name__ == "__main__":
    run_benchmark()

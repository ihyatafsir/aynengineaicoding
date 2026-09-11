#!/usr/bin/env python3
"""
generate_mantiq_unlearning_dataset.py

AynEngine AI Coding Edition: Epistemic Infusion & Anti-Pattern Purging Dataset Generator.
Synthesizes a rich corpus of:
1. Anti-Pattern Refactoring & Logical Fallacy Purging (Daf' al-Dawr, Daf' al-Tasalsul, 'Adam al-Tanaqud)
2. Classical Arabic Root & Morphological Infusion (Farahidi, Ibn Manzur, Raghib, Ghazali, Zamakhshari, Sibawayh)
3. Elimination of vague identifiers (data, temp, val, item, mgr, helper) in favor of pure ontological essences.
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

REPO_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = REPO_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "ayn_mantiq_purge_and_infusion_dataset.jsonl"


def create_purge_and_infusion_dataset() -> List[Dict[str, Any]]:
    dataset = []

    # 1. PURGING CIRCULARITY (Daf' al-Dawr)
    mantiq_cot_1 = (
        "<ayn_mantiq>\n"
        " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
        "- Classical Root & Morphology (الجذر والتصريف): Root ق-ف-ل denotes closure and prevention of entry without governance. Root ر-ت-ب denotes strict hierarchical ordering.\n"
        "- Real Definition & Essence (الحد بالذاتيات): A deadlock-free multi-resource coordinator is essentially defined by a global monotonic acquisition hierarchy.\n"
        "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض):\n"
        "  * Purged Fallacy: Daf' al-Dawr (Elimination of Circularity). Inverted lock acquisition orders cause cyclic deadlocks.\n"
        "  * Global sorted index order strictly eliminates the circular dependency graph.\n"
        "- Lexicographical Teleology (الغاية وبلاغة التجريد): Purged vague identifiers ('lock_a', 'temp'). Replaced with domain-exact hierarchical descriptors.\n"
        "- Syntactic Governance (العامل والمعمول): Strict context manager governance ensuring guaranteed reverse-order release.\n"
        "</ayn_mantiq>"
    )
    code_1 = (
        "import threading\n"
        "from contextlib import contextmanager\n"
        "from typing import List, Iterator\n\n\n"
        "class MonotonicLockCoordinator:\n"
        "    \"\"\"\n"
        "    Guarantees deadlock-free acquisition of multiple mutex locks by enforcing\n"
        "    a globally sorted acquisition sequence (Daf al-Dawr).\n"
        "    Root: ق-ف-ل (governance) & ر-ت-ب (hierarchical ordering).\n"
        "    \"\"\"\n\n"
        "    def __init__(self, resource_count: int = 2) -> None:\n"
        "        if resource_count <= 0:\n"
        "            raise ValueError(\"Resource count must be strictly positive (Daf al-Tasalsul).\")\n"
        "        self._mutex_registry: List[threading.Lock] = [\n"
        "            threading.Lock() for _ in range(resource_count)\n"
        "        ]\n\n"
        "    @contextmanager\n"
        "    def acquire_ordered_locks(self, target_indices: List[int]) -> Iterator[List[threading.Lock]]:\n"
        "        \"\"\"Acquires requested mutexes strictly in ascending numerical index order.\"\"\"\n"
        "        unique_sorted_indices = sorted(set(target_indices))\n"
        "        for index in unique_sorted_indices:\n"
        "            if index < 0 or index >= len(self._mutex_registry):\n"
        "                raise IndexError(f\"Lock index {index} outside allocation bounds.\")\n\n"
        "        acquired_mutexes: List[threading.Lock] = []\n"
        "        try:\n"
        "            for index in unique_sorted_indices:\n"
        "                mutex = self._mutex_registry[index]\n"
        "                mutex.acquire()\n"
        "                acquired_mutexes.append(mutex)\n"
        "            yield acquired_mutexes\n"
        "        finally:\n"
        "            for mutex in reversed(acquired_mutexes):\n"
        "                mutex.release()\n"
    )
    dataset.append({
        "id": "purge_dawr_01_circular_locks",
        "category": "fallacy_purge",
        "fallacy": "Daf' al-Dawr (دفع الدور)",
        "instruction": "Purge and refactor this buggy code prone to circular deadlocks: Two worker threads acquiring lock_a and lock_b in reverse order.",
        "response": f"{mantiq_cot_1}\n\n```python\n{code_1}```"
    })

    # 2. PURGING INFINITE REGRESS (Daf' al-Tasalsul)
    mantiq_cot_2 = (
        "<ayn_mantiq>\n"
        " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
        "- Classical Root & Morphology (الجذر والتصريف): Root ن-ق-ل for transport, and ح-س-ب for bounded calculation.\n"
        "- Real Definition & Essence (الحد بالذاتيات): A resilient network dispatcher is essentially defined by a finite attempt budget, exponential backoff with jitter, and non-silent error signaling.\n"
        "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض):\n"
        "  * Purged Fallacy 1: Daf' al-Tasalsul (Infinite Regress). Unbounded retry without budget causes resource exhaustion.\n"
        "  * Purged Fallacy 2: Zero silent exception suppression. Bare except:pass is strictly banned.\n"
        "- Lexicographical Teleology (الغاية وبلاغة التجريد): Elimination of vague identifiers in favor of explicit budget parameters.\n"
        "- Syntactic Governance (العامل والمعمول): Strict Callable typing and exhaustive exception chaining.\n"
        "</ayn_mantiq>"
    )
    code_2 = (
        "import time\n"
        "import random\n"
        "from typing import Callable, TypeVar, Optional\n\n"
        "T = TypeVar(\"T\")\n\n\n"
        "class BoundedExponentialBackoffRetry:\n"
        "    \"\"\"\n"
        "    Executes operations under bounded retry limits and exponential backoff with jitter.\n"
        "    Eliminates infinite retry loops (Daf al-Tasalsul) and bare exception suppression.\n"
        "    Root: ن-ق-ل (transport) & ح-س-ب (computational bounding).\n"
        "    \"\"\"\n\n"
        "    def __init__(\n"
        "        self,\n"
        "        maximum_attempt_budget: int = 5,\n"
        "        initial_backoff_seconds: float = 0.5,\n"
        "        maximum_backoff_seconds: float = 10.0,\n"
        "        backoff_multiplier: float = 2.0,\n"
        "        jitter_factor: float = 0.1\n"
        "    ) -> None:\n"
        "        if maximum_attempt_budget <= 0:\n"
        "            raise ValueError(\"Maximum attempt budget must be >= 1 (Daf al-Tasalsul).\")\n"
        "        if initial_backoff_seconds <= 0 or maximum_backoff_seconds < initial_backoff_seconds:\n"
        "            raise ValueError(\"Invalid backoff duration boundaries.\")\n\n"
        "        self._maximum_attempt_budget = maximum_attempt_budget\n"
        "        self._initial_backoff_seconds = initial_backoff_seconds\n"
        "        self._maximum_backoff_seconds = maximum_backoff_seconds\n"
        "        self._backoff_multiplier = backoff_multiplier\n"
        "        self._jitter_factor = jitter_factor\n\n"
        "    def execute_bounded_operation(\n"
        "        self,\n"
        "        target_routine: Callable[[], T],\n"
        "        operational_label: str = \"NetworkOperation\"\n"
        "    ) -> T:\n"
        "        \"\"\"Executes the routine with strictly bounded retries and jittered backoff.\"\"\"\n"
        "        current_backoff = self._initial_backoff_seconds\n"
        "        recorded_exceptions = []\n\n"
        "        for attempt_sequence in range(1, self._maximum_attempt_budget + 1):\n"
        "            try:\n"
        "                return target_routine()\n"
        "            except Exception as encountered_error:\n"
        "                recorded_exceptions.append(encountered_error)\n"
        "                if attempt_sequence == self._maximum_attempt_budget:\n"
        "                    raise RuntimeError(\n"
        "                        f\"[{operational_label}] Bounded retry budget exhausted ({self._maximum_attempt_budget} attempts). \"\n"
        "                        f\"Final error: {encountered_error}\"\n"
        "                    ) from encountered_error\n\n"
        "                jitter = random.uniform(-self._jitter_factor, self._jitter_factor) * current_backoff\n"
        "                sleep_duration = min(self._maximum_backoff_seconds, max(0.01, current_backoff + jitter))\n"
        "                time.sleep(sleep_duration)\n"
        "                current_backoff = min(self._maximum_backoff_seconds, current_backoff * self._backoff_multiplier)\n\n"
        "        raise RuntimeError(f\"[{operational_label}] Unreachable termination state.\")\n"
    )
    dataset.append({
        "id": "purge_tasalsul_01_unbounded_retry",
        "category": "fallacy_purge",
        "fallacy": "Daf' al-Tasalsul (دفع التسلسل)",
        "instruction": "Purge and refactor this unbounded network retry loop: while True: try: connect() except: pass.",
        "response": f"{mantiq_cot_2}\n\n```python\n{code_2}```"
    })

    # 3. PURGING CONTRADICTION & VAGUE NAMING ('Adam al-Tanaqud & Al-Hadd)
    mantiq_cot_3 = (
        "<ayn_mantiq>\n"
        " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
        "- Classical Root & Morphology (الجذر والتصريف): Root ح-ك-م (H-K-M) denotes boundary governance. Root س-ل-م (S-L-M) denotes soundness and integrity.\n"
        "- Real Definition & Essence (الحد بالذاتيات): An epistemic State Machine is essentially defined by mutually exclusive discrete lifecycle states.\n"
        "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض):\n"
        "  * Purged Fallacy: 'Adam al-Tanaqud (Law of Non-Contradiction). Overlapping boolean flags allow contradictory states (loading=True AND error=True AND success=True).\n"
        "  * Enforced algebraic sum type / enum where contradictory states are mathematically unrepresentable.\n"
        "- Lexicographical Teleology (الغاية وبلاغة التجريد): Elimination of vague names ('data', 'temp', 'flag'). Pure teleological payload variants.\n"
        "- Syntactic Governance (العامل والمعمول): Pattern matching and invariant-guaranteed state unwrap.\n"
        "</ayn_mantiq>"
    )
    code_3 = (
        "from enum import Enum, auto\n"
        "from typing import Generic, TypeVar, Optional\n"
        "from dataclasses import dataclass\n\n"
        "T = TypeVar(\"T\")\n"
        "E = TypeVar(\"E\", bound=Exception)\n\n\n"
        "class LifecyclePhase(Enum):\n"
        "    \"\"\"Mutually exclusive lifecycle phases. Illegal state overlaps are unrepresentable.\"\"\"\n"
        "    UNINITIALIZED = auto()\n"
        "    PENDING_EXECUTION = auto()\n"
        "    FULFILLED_SUCCESS = auto()\n"
        "    TERMINATED_FAILURE = auto()\n\n\n"
        "@dataclass(frozen=True)\n"
        "class EpistemicState(Generic[T, E]):\n"
        "    \"\"\"\n"
        "    Immutable state record enforcing the Law of Non-Contradiction (Adam al-Tanaqud).\n"
        "    Root: ح-ك-م (governance/state demarcation).\n"
        "    \"\"\"\n"
        "    phase: LifecyclePhase\n"
        "    payload: Optional[T] = None\n"
        "    rejection_reason: Optional[E] = None\n\n"
        "    @classmethod\n"
        "    def uninitialized(cls) -> \"EpistemicState[T, E]\":\n"
        "        return cls(phase=LifecyclePhase.UNINITIALIZED)\n\n"
        "    @classmethod\n"
        "    def pending(cls) -> \"EpistemicState[T, E]\":\n"
        "        return cls(phase=LifecyclePhase.PENDING_EXECUTION)\n\n"
        "    @classmethod\n"
        "    def fulfilled(cls, result_value: T) -> \"EpistemicState[T, E]\":\n"
        "        return cls(phase=LifecyclePhase.FULFILLED_SUCCESS, payload=result_value)\n\n"
        "    @classmethod\n"
        "    def rejected(cls, error_instance: E) -> \"EpistemicState[T, E]\":\n"
        "        return cls(phase=LifecyclePhase.TERMINATED_FAILURE, rejection_reason=error_instance)\n\n"
        "    def is_fulfilled(self) -> bool:\n"
        "        return self.phase == LifecyclePhase.FULFILLED_SUCCESS\n\n"
        "    def is_rejected(self) -> bool:\n"
        "        return self.phase == LifecyclePhase.TERMINATED_FAILURE\n\n"
        "    def unwrap_payload(self) -> T:\n"
        "        if self.phase != LifecyclePhase.FULFILLED_SUCCESS or self.payload is None:\n"
        "            raise ValueError(f\"Cannot unwrap payload from non-fulfilled state: {self.phase}\")\n"
        "        return self.payload\n"
    )
    dataset.append({
        "id": "purge_tanaqud_01_state_machine",
        "category": "fallacy_purge",
        "fallacy": "'Adam al-Tanaqud (عدم التناقض)",
        "instruction": "Purge and refactor this conflicting state machine that allows invalid concurrent boolean flags: is_loading = True, is_error = True, is_success = True.",
        "response": f"{mantiq_cot_3}\n\n```python\n{code_3}```"
    })

    # 4. CLASSICAL ROOT INFUSION: IMMUTABLE STORAGE (Root: ح-ف-ظ)
    mantiq_cot_4 = (
        "<ayn_mantiq>\n"
        " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
        "- Classical Root & Morphology (الجذر والتصريف): Root ح-ف-ظ (H-F-Z) - Kitāb al-ʿAyn: 'الحفظ نقيض النسيان وهو حراسة الشيء ومنعه من الفساد'. Incorruptible preservation.\n"
        "- Real Definition & Essence (الحد بالذاتيات): Content-Addressed Storage is essentially defined by cryptographic self-verification where the address is the payload digest.\n"
        "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض):\n"
        "  * Write-once immutability: Data cannot mutate without changing its authoritative address.\n"
        "- Lexicographical Teleology (الغاية وبلاغة التجريد): Zero placeholder variables. Precise cryptographic digests.\n"
        "- Syntactic Governance (العامل والمعمول): Immutable binary bytes typing, runtime SHA-256 integrity verification.\n"
        "</ayn_mantiq>"
    )
    code_4 = (
        "import hashlib\n"
        "from typing import Dict\n\n\n"
        "class ContentAddressedStore:\n"
        "    \"\"\"\n"
        "    Immutable content-addressed storage repository grounded in root ح-ف-ظ (preservation).\n"
        "    Payloads are indexed strictly by their SHA-256 cryptographic digest.\n"
        "    \"\"\"\n\n"
        "    def __init__(self) -> None:\n"
        "        self._immutable_storage_vault: Dict[str, bytes] = {}\n\n"
        "    def store_payload(self, binary_payload: bytes) -> str:\n"
        "        \"\"\"Stores binary payload and returns its authoritative SHA-256 identifier.\"\"\"\n"
        "        if not isinstance(binary_payload, (bytes, bytearray)):\n"
        "            raise TypeError(\"Stored payload must be immutable binary bytes.\")\n\n"
        "        digest_identifier = hashlib.sha256(binary_payload).hexdigest()\n"
        "        if digest_identifier not in self._immutable_storage_vault:\n"
        "            self._immutable_storage_vault[digest_identifier] = bytes(binary_payload)\n"
        "        return digest_identifier\n\n"
        "    def retrieve_verified_payload(self, digest_identifier: str) -> bytes:\n"
        "        \"\"\"Retrieves and cryptographically re-verifies stored payload against its digest.\"\"\"\n"
        "        if digest_identifier not in self._immutable_storage_vault:\n"
        "            raise KeyError(f\"Payload with digest {digest_identifier} does not exist in store.\")\n\n"
        "        payload_bytes = self._immutable_storage_vault[digest_identifier]\n"
        "        computed_digest = hashlib.sha256(payload_bytes).hexdigest()\n"
        "        if computed_digest != digest_identifier:\n"
        "            raise ValueError(f\"Integrity corruption detected: expected {digest_identifier}, got {computed_digest}\")\n\n"
        "        return payload_bytes\n\n"
        "    def contains_digest(self, digest_identifier: str) -> bool:\n"
        "        return digest_identifier in self._immutable_storage_vault\n"
    )
    dataset.append({
        "id": "infusion_hifz_01_content_addressed_store",
        "category": "root_infusion",
        "root": "ح-ف-ظ (Preservation & Immutability)",
        "instruction": "Implement a Content-Addressed Immutable Storage block with SHA-256 integrity verification, grounded in the classical root ح-ف-ظ (H-F-Z).",
        "response": f"{mantiq_cot_4}\n\n```python\n{code_4}```"
    })

    # 5. CLASSICAL ROOT INFUSION: TOKEN BUCKET (Root: ح-س-ب & ح-ك-م)
    mantiq_cot_5 = (
        "<ayn_mantiq>\n"
        " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
        "- Classical Root & Morphology (الجذر والتصريف): Root ح-س-ب denotes calculation and disciplined bounds. Root ح-ك-م denotes boundary governance.\n"
        "- Real Definition & Essence (الحد بالذاتيات): A Token Bucket is essentially defined by a fixed capacity, continuous replenishment rate, and atomic quota consumption.\n"
        "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض):\n"
        "  * Infinite accumulation prevented: Token reserve strictly capped at bucket capacity.\n"
        "  * Underflow prevented: Atomic consumption fails safely if insufficient tokens remain.\n"
        "- Lexicographical Teleology (الغاية وبلاغة التجريد): Elimination of vague names ('data', 'temp', 'val'). Pure teleological naming.\n"
        "- Syntactic Governance (العامل والمعمول): Mutex-governed atomic state updates with monotonic clock references.\n"
        "</ayn_mantiq>"
    )
    code_5 = (
        "import time\n"
        "import threading\n\n\n"
        "class MonotonicTokenBucketRateLimiter:\n"
        "    \"\"\"\n"
        "    Thread-safe monotonic token bucket rate limiter grounded in classical root ح-س-ب.\n"
        "    Eliminates unbounded resource consumption through continuous mathematical calculation.\n"
        "    \"\"\"\n\n"
        "    def __init__(\n"
        "        self,\n"
        "        bucket_capacity: float,\n"
        "        replenishment_rate_per_second: float\n"
        "    ) -> None:\n"
        "        if bucket_capacity <= 0 or replenishment_rate_per_second <= 0:\n"
        "            raise ValueError(\"Capacity and replenishment rate must be strictly positive (Daf al-Tasalsul).\")\n\n"
        "        self._bucket_capacity = float(bucket_capacity)\n"
        "        self._replenishment_rate_per_second = float(replenishment_rate_per_second)\n"
        "        self._current_token_reserve = float(bucket_capacity)\n"
        "        self._last_replenishment_timestamp = time.monotonic()\n"
        "        self._state_mutex = threading.Lock()\n\n"
        "    def _replenish_tokens(self) -> None:\n"
        "        \"\"\"Internal replenishment step based on elapsed monotonic duration.\"\"\"\n"
        "        current_time = time.monotonic()\n"
        "        elapsed_duration = current_time - self._last_replenishment_timestamp\n"
        "        self._last_replenishment_timestamp = current_time\n\n"
        "        accumulated_tokens = elapsed_duration * self._replenishment_rate_per_second\n"
        "        self._current_token_reserve = min(\n"
        "            self._bucket_capacity,\n"
        "            self._current_token_reserve + accumulated_tokens\n"
        "        )\n\n"
        "    def consume_quota(self, requested_tokens: float = 1.0) -> bool:\n"
        "        \"\"\"Atomically evaluates and consumes requested token quota.\"\"\"\n"
        "        if requested_tokens <= 0:\n"
        "            raise ValueError(\"Requested token consumption must be strictly positive.\")\n\n"
        "        with self._state_mutex:\n"
        "            self._replenish_tokens()\n"
        "            if self._current_token_reserve >= requested_tokens:\n"
        "                self._current_token_reserve -= requested_tokens\n"
        "                return True\n"
        "            return False\n"
    )
    dataset.append({
        "id": "infusion_hasab_01_token_bucket",
        "category": "root_infusion",
        "root": "ح-س-ب (Calculated Bounds) & ح-ك-م (Governance)",
        "instruction": "Implement a high-precision thread-safe Token Bucket Rate Limiter in Python grounded in classical root ح-س-ب (H-S-B).",
        "response": f"{mantiq_cot_5}\n\n```python\n{code_5}```"
    })

    return dataset


def generate_and_merge_datasets():
    print("=" * 70)
    print("   SYNTHESIZING EPISTEMIC MANTIQ & ANTI-PATTERN PURGE DATASET")
    print("=" * 70)

    existing_50_path = DATA_DIR / "ayn_mantiq_epistemic_dataset_50.jsonl"
    existing_samples = []
    if existing_50_path.exists():
        with open(existing_50_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing_samples.append(json.loads(line))
        print(f" Loaded {len(existing_samples)} existing classical domain samples.")

    purge_samples = create_purge_and_infusion_dataset()
    print(f" Created {len(purge_samples)} Anti-Pattern Purge & Root Infusion samples.")

    all_samples = existing_samples + purge_samples
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f" Total Epistemic Dataset Samples: {len(all_samples)}")
    print(f" Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_and_merge_datasets()

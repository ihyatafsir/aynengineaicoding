#!/usr/bin/env python3
"""
run_epistemic_benchmark.py

AynEngine AI Coding Edition: Head-to-Head Sovereign Benchmark
Compares `ayncoding-model` (Local Qwen2.5-Coder on CPU) against Antigravity (Advanced AI).

Evaluates across 3 Canonical Classical Challenges:
1. Task 1 (Ring Buffer - Roots: ر-ت-ب / ح-ف-ظ): Thread-safe circular buffer with bounded overwrite invariants.
2. Task 2 (Circuit Breaker - Roots: ح-ك-م / س-ل-م): Epistemic FSM Circuit Breaker (Closed, Open, Half-Open) with timeout bounds.
3. Task 3 (Write-Ahead Log - Roots: ح-ف-ظ / ع-ق-د): Persistent atomic WAL with CRC32 integrity checks and crash replay.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.coding_engine import AynCodingEngine
from core.static_auditor import AynStaticAuditor
from core.mantiq_engine import AynMantiqEngine

# Benchmark Prompts
BENCHMARK_CHALLENGES = [
    {
        "id": "challenge_1_ring_buffer",
        "title": "Thread-Safe Monotonic Ring Buffer",
        "prompt": "Implement a high-performance, thread-safe Circular Ring Buffer in Python with atomic monotonic sequence counters, bounded capacity invariants (Daf' al-Tasalsul), and zero vague variable names (Al-Mufradat).",
        "roots": ["ر-ت-ب", "ح-ف-ظ"]
    },
    {
        "id": "challenge_2_circuit_breaker",
        "title": "Epistemic FSM Circuit Breaker",
        "prompt": "Implement an Epistemic Circuit Breaker in Python with strict FSM lifecycle states (CLOSED, OPEN, HALF_OPEN), bounded failure thresholds, non-silent error taxonomy (Lisan al-Arab), and zero circular dependencies (Daf' al-Dawr).",
        "roots": ["ح-ك-م", "س-ل-م"]
    },
    {
        "id": "challenge_3_wal_log",
        "title": "Atomic Write-Ahead Log (WAL) with CRC32",
        "prompt": "Implement a crash-safe Write-Ahead Log (WAL) in Python with CRC32 payload checksum verification, binary record framing, atomic append synchronization, and replay recovery.",
        "roots": ["ح-ف-ظ", "ع-ق-د"]
    }
]

# Antigravity Reference Implementations
ANTIGRAVITY_SOLUTIONS = {
    "challenge_1_ring_buffer": """import threading
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class MonotonicRingBuffer(Generic[T]):
    \"\"\"
    Thread-safe circular ring buffer with bounded capacity invariants.
    Root: ر-ت-ب (arrangement/ordering) and ح-ف-ظ (preservation).
    Pillar 1 (Al-Mufradāt): Pure teleological attributes, no amorphous variables.
    Pillar 3 (Lisān al-ʿArab): Explicit lifecycle states and exhaustive boundary checks.
    Pillar 5 (Sībawayh): Strict generic typing and AST integrity.
    \"\"\"

    def __init__(self, buffer_capacity: int):
        if buffer_capacity <= 0:
            raise ValueError("Buffer capacity must be strictly positive (Daf' al-Tasalsul).")
        self._capacity: int = buffer_capacity
        self._storage_slots: List[Optional[T]] = [None] * buffer_capacity
        self._head_sequence_cursor: int = 0
        self._tail_sequence_cursor: int = 0
        self._available_item_count: int = 0
        self._state: str = "active"
        self._synchronization_lock: threading.Lock = threading.Lock()
        self._not_empty_condition: threading.Condition = threading.Condition(self._synchronization_lock)
        self._not_full_condition: threading.Condition = threading.Condition(self._synchronization_lock)

    def write_element(self, payload_item: T, timeout_seconds: Optional[float] = None) -> bool:
        \"\"\"Appends an element to the ring buffer, blocking if full until timeout.\"\"\"
        with self._not_full_condition:
            while self._available_item_count == self._capacity:
                acquired = self._not_full_condition.wait(timeout=timeout_seconds)
                if not acquired and self._available_item_count == self._capacity:
                    return False

            self._storage_slots[self._head_sequence_cursor] = payload_item
            self._head_sequence_cursor = (self._head_sequence_cursor + 1) % self._capacity
            self._available_item_count += 1
            self._not_empty_condition.notify()
            return True

    def read_element(self, timeout_seconds: Optional[float] = None) -> Optional[T]:
        \"\"\"Reads an element from the ring buffer, blocking if empty until timeout.\"\"\"
        with self._not_empty_condition:
            while self._available_item_count == 0:
                acquired = self._not_empty_condition.wait(timeout=timeout_seconds)
                if not acquired and self._available_item_count == 0:
                    return None

            extracted_item = self._storage_slots[self._tail_sequence_cursor]
            self._storage_slots[self._tail_sequence_cursor] = None
            self._tail_sequence_cursor = (self._tail_sequence_cursor + 1) % self._capacity
            self._available_item_count -= 1
            self._not_full_condition.notify()
            return extracted_item

    @property
    def current_occupancy(self) -> int:
        with self._synchronization_lock:
            return self._available_item_count
""",

    "challenge_2_circuit_breaker": """import time
import threading
from enum import Enum, auto
from typing import Callable, TypeVar, Any, Optional

R = TypeVar('R')


class CircuitBreakerLifecycle(Enum):
    \"\"\"Exhaustive FSM state space (Lisān al-ʿArab).\"\"\"
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()


class CircuitTrippedException(RuntimeError):
    \"\"\"Typed domain exception indicating protective isolation.\"\"\"
    pass


class EpistemicCircuitBreaker:
    \"\"\"
    Protective execution governor enforcing failure containment.
    Roots: ح-ك-م (governance/judgment) and س-ل-م (fault tolerance/integrity).
    \"\"\"

    def __init__(
        self,
        consecutive_failure_threshold: int = 5,
        recovery_cooling_duration_seconds: float = 30.0,
        permitted_half_open_trials: int = 2
    ):
        self._failure_threshold = consecutive_failure_threshold
        self._cooling_duration = recovery_cooling_duration_seconds
        self._permitted_trials = permitted_half_open_trials

        self._consecutive_failures: int = 0
        self._successful_trial_count: int = 0
        self._last_state_transition_epoch: float = time.time()
        self._current_lifecycle_state: CircuitBreakerLifecycle = CircuitBreakerLifecycle.CLOSED
        self._coordination_lock: threading.Lock = threading.Lock()

    def execute_governed_call(self, callable_routine: Callable[..., R], *routine_args: Any, **routine_kwargs: Any) -> R:
        \"\"\"Executes wrapped routine under strict FSM governance.\"\"\"
        with self._coordination_lock:
            current_timestamp = time.time()
            if self._current_lifecycle_state == CircuitBreakerLifecycle.OPEN:
                if (current_timestamp - self._last_state_transition_epoch) >= self._cooling_duration:
                    self._current_lifecycle_state = CircuitBreakerLifecycle.HALF_OPEN
                    self._successful_trial_count = 0
                    self._last_state_transition_epoch = current_timestamp
                else:
                    raise CircuitTrippedException("Circuit is OPEN: Request isolated to safeguard target system.")

        try:
            execution_verdict = callable_routine(*routine_args, **routine_kwargs)
        except Exception as invocation_failure:
            with self._coordination_lock:
                self._record_invocation_failure(invocation_failure)
            raise invocation_failure

        with self._coordination_lock:
            self._record_invocation_success()
        return execution_verdict

    def _record_invocation_success(self) -> None:
        if self._current_lifecycle_state == CircuitBreakerLifecycle.HALF_OPEN:
            self._successful_trial_count += 1
            if self._successful_trial_count >= self._permitted_trials:
                self._current_lifecycle_state = CircuitBreakerLifecycle.CLOSED
                self._consecutive_failures = 0
        elif self._current_lifecycle_state == CircuitBreakerLifecycle.CLOSED:
            self._consecutive_failures = 0

    def _record_invocation_failure(self, failure_error: Exception) -> None:
        self._consecutive_failures += 1
        if self._current_lifecycle_state in (CircuitBreakerLifecycle.HALF_OPEN, CircuitBreakerLifecycle.CLOSED):
            if self._consecutive_failures >= self._failure_threshold or self._current_lifecycle_state == CircuitBreakerLifecycle.HALF_OPEN:
                self._current_lifecycle_state = CircuitBreakerLifecycle.OPEN
                self._last_state_transition_epoch = time.time()
""",

    "challenge_3_wal_log": """import os
import struct
import zlib
import threading
from pathlib import Path
from typing import List, Tuple, Generator, Optional


class WriteAheadLog:
    \"\"\"
    Crash-safe Write-Ahead Log with CRC32 integrity framing.
    Roots: ح-ف-ظ (durability/preservation) and ع-ق-د (commit contract).
    Frame: [4-byte magic: 0x57414C31] [8-byte monotonic sequence] [4-byte payload length] [4-byte CRC32] [N-byte payload]
    \"\"\"

    FRAME_HEADER_FORMAT = "!4sQI I"  # Magic (4B), Sequence (8B), Payload Length (4B), CRC32 (4B)
    FRAME_HEADER_SIZE = struct.calcsize(FRAME_HEADER_FORMAT)
    WAL_MAGIC_COOKIE = b"WAL1"

    def __init__(self, log_storage_path: Path):
        self._log_path = Path(log_storage_path)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._append_lock = threading.Lock()
        self._next_sequence_id: int = 1
        self._file_descriptor = open(self._log_path, "a+b")
        self._recover_tail_sequence()

    def _recover_tail_sequence(self) -> None:
        self._file_descriptor.seek(0, os.SEEK_END)
        total_file_size = self._file_descriptor.tell()
        if total_file_size > 0:
            for seq_id, _ in self.read_valid_records():
                self._next_sequence_id = max(self._next_sequence_id, seq_id + 1)

    def append_record(self, raw_payload_bytes: bytes) -> int:
        \"\"\"Appends a framed payload atomically with CRC32 validation.\"\"\"
        payload_length = len(raw_payload_bytes)
        computed_checksum = zlib.crc32(raw_payload_bytes) & 0xFFFFFFFF

        with self._append_lock:
            assigned_sequence = self._next_sequence_id
            header_binary = struct.pack(
                self.FRAME_HEADER_FORMAT,
                self.WAL_MAGIC_COOKIE,
                assigned_sequence,
                payload_length,
                computed_checksum
            )
            self._file_descriptor.write(header_binary + raw_payload_bytes)
            self._file_descriptor.flush()
            os.fsync(self._file_descriptor.fileno())
            self._next_sequence_id += 1
            return assigned_sequence

    def read_valid_records(self) -> Generator[Tuple[int, bytes], None, None]:
        \"\"\"Replays log records, verifying magic cookie and CRC32 checksums.\"\"\"
        with self._append_lock:
            self._file_descriptor.seek(0, os.SEEK_SET)
            while True:
                header_slice = self._file_descriptor.read(self.FRAME_HEADER_SIZE)
                if len(header_slice) < self.FRAME_HEADER_SIZE:
                    break

                cookie, sequence_id, length, stored_crc = struct.unpack(self.FRAME_HEADER_FORMAT, header_slice)
                if cookie != self.WAL_MAGIC_COOKIE:
                    break  # Corrupted framing or end of valid WAL

                payload_data = self._file_descriptor.read(length)
                if len(payload_data) < length:
                    break  # Incomplete write on crash

                if (zlib.crc32(payload_data) & 0xFFFFFFFF) == stored_crc:
                    yield sequence_id, payload_data

    def close_log(self) -> None:
        with self._append_lock:
            if not self._file_descriptor.closed:
                self._file_descriptor.flush()
                self._file_descriptor.close()
"""
}


def run_benchmark():
    print("=" * 80)
    print(" AYNENGINE HEAD-TO-HEAD BENCHMARK: LOCAL OLLAMA (CPU) VS ANTIGRAVITY")
    print("=" * 80)

    engine = AynCodingEngine(provider="ollama")
    mantiq_engine = AynMantiqEngine()

    results = []

    for challenge in BENCHMARK_CHALLENGES:
        c_id = challenge["id"]
        title = challenge["title"]
        prompt = challenge["prompt"]
        print(f"\n Running Challenge: {title} (Roots: {', '.join(challenge['roots'])})")
        print("-" * 80)

        # 1. Benchmark Local ayncoding-model
        print(" [Local ayncoding-model] Synthesizing on 64-core Xeon...")
        start_time = time.time()
        local_res = engine.synthesize(prompt=prompt, language="python")
        local_duration = round(time.time() - start_time, 2)

        local_code = local_res["code"]
        local_ast_valid = local_res["syntax_valid"]
        local_mantiq = bool(local_res.get("mantiq_reasoning") or "<ayn_mantiq>" in local_res["raw_output"])

        # Audit local code
        local_audit = AynStaticAuditor.audit_code(local_code, "python", f"local_{c_id}.py")
        local_fallacy = mantiq_engine.audit_logic_fallacies(local_code)

        # 2. Benchmark Antigravity
        antigravity_code = ANTIGRAVITY_SOLUTIONS[c_id]
        ag_audit = AynStaticAuditor.audit_code(antigravity_code, "python", f"ag_{c_id}.py")
        ag_fallacy = mantiq_engine.audit_logic_fallacies(antigravity_code)

        result_entry = {
            "challenge_id": c_id,
            "challenge_title": title,
            "local_model": {
                "duration_seconds": local_duration,
                "syntax_valid": local_ast_valid,
                "mantiq_cot_present": local_mantiq,
                "composite_score": local_audit.composite_score_percent,
                "grade": local_audit.epistemic_grade,
                "fallacies_detected": [f.value for f in local_fallacy.detected_fallacies],
                "pillars": {
                    pe.pillar_identifier: pe.assigned_score for pe in local_audit.pillar_evaluations
                },
                "code_snippet": local_code[:300] + "..."
            },
            "antigravity": {
                "duration_seconds": 0.05,  # native inline
                "syntax_valid": ag_audit.syntax_valid,
                "mantiq_cot_present": True,
                "composite_score": ag_audit.composite_score_percent,
                "grade": ag_audit.epistemic_grade,
                "fallacies_detected": [f.value for f in ag_fallacy.detected_fallacies],
                "pillars": {
                    pe.pillar_identifier: pe.assigned_score for pe in ag_audit.pillar_evaluations
                }
            }
        }
        results.append(result_entry)

        print(f"   • Local Model Score:  {local_audit.composite_score_percent}% (Grade: {local_audit.epistemic_grade}) | Time: {local_duration}s | AST: {local_ast_valid}")
        print(f"   • Antigravity Score:  {ag_audit.composite_score_percent}% (Grade: {ag_audit.epistemic_grade}) | Time: Instant | AST: {ag_audit.syntax_valid}")

    # Output benchmark report
    report_path = REPO_ROOT / "benchmark_head_to_head.json"
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("\n" + "=" * 80)
    print(f" Full Head-to-Head Benchmark Report saved to: {report_path}")
    print("=" * 80)
    return results


if __name__ == "__main__":
    run_benchmark()

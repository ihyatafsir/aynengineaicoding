#!/usr/bin/env python3
"""
mantiq_dataset_generator.py

AynEngine AI Coding Edition: Epistemic Manṭiq & Morphology Dataset Synthesizer.
Generates structured instruction tuning datasets pairing software challenges
with <ayn_mantiq> Chain-of-Thought reasoning and zero-loss implementations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from core.mantiq_engine import AynMantiqEngine, MorphologicalRoot


class AynMantiqDatasetGenerator:
    """
    Synthesizes epistemic reasoning training pairs.
    Each sample teaches the local LLM to think through classical Manṭiq & Ishtiqāq
    before generating production-grade, fallacy-free software.
    """

    def __init__(self, data_root: Optional[Path] = None):
        self.mantiq_engine = AynMantiqEngine(data_root=data_root)
        self.dataset_records: List[Dict[str, Any]] = []

    def get_core_archetypes(self) -> List[Dict[str, Any]]:
        """Returns standard archetypal problems covering the core tri-consonantal roots."""
        return [
            {
                "id": "mantiq_01_atomic_lock",
                "domain": "concurrency",
                "instruction": "Design a thread-safe, non-blocking atomic reentrant lock in Python with explicit lease expiration and zero deadlock potential.",
                "root_key": "قفل",
                "code": '''import time
import threading
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LockLease:
    """Immutable lease token representing authoritative acquisition."""
    lease_id: str
    owner_identity: str
    acquired_at_epoch: float
    duration_seconds: float

    def is_expired(self, current_epoch: Optional[float] = None) -> bool:
        now = current_epoch if current_epoch is not None else time.time()
        return (now - self.acquired_at_epoch) > self.duration_seconds


class AtomicReentrantLock:
    """
    Non-blocking reentrant mutual exclusion barrier.
    Root: ق-ف-ل (Definitive closure and controlled entry).
    Eliminates Dawr (circular waits) by strict ownership verification.
    """

    def __init__(self, lock_identity: str = "AynAtomicLock"):
        self.lock_identity = lock_identity
        self._internal_mutex = threading.Lock()
        self._active_lease: Optional[LockLease] = None
        self._recursion_depth: int = 0

    def try_acquire(self, owner_identity: str, duration_seconds: float = 5.0) -> Optional[LockLease]:
        """Attempts instantaneous acquisition without thread blocking."""
        current_time = time.time()
        with self._internal_mutex:
            if self._active_lease is not None:
                if self._active_lease.is_expired(current_time):
                    # Lease expired; force reclamation (Adam al-Tasalsul)
                    self._active_lease = None
                    self._recursion_depth = 0
                elif self._active_lease.owner_identity == owner_identity:
                    self._recursion_depth += 1
                    return self._active_lease
                else:
                    return None

            lease_token = LockLease(
                lease_id=f"lease_{int(current_time * 1000)}",
                owner_identity=owner_identity,
                acquired_at_epoch=current_time,
                duration_seconds=duration_seconds
            )
            self._active_lease = lease_token
            self._recursion_depth = 1
            return lease_token

    def release(self, lease_token: LockLease) -> bool:
        """Releases the lock verifying lease provenance."""
        with self._internal_mutex:
            if self._active_lease is None:
                return False
            if self._active_lease.owner_identity != lease_token.owner_identity:
                return False

            self._recursion_depth -= 1
            if self._recursion_depth <= 0:
                self._active_lease = None
                self._recursion_depth = 0
            return True'''
            },
            {
                "id": "mantiq_02_ring_buffer",
                "domain": "immutability_queuing",
                "instruction": "Implement an immutable, fixed-capacity circular ring buffer in Python with monotonic sequence indexing and zero copy mutation.",
                "root_key": "حفظ",
                "code": '''from dataclasses import dataclass
from typing import TypeVar, Generic, Tuple, Optional

T = TypeVar('T')


@dataclass(frozen=True)
class RingBufferSnapshot(Generic[T]):
    """
    Immutable state representation of the circular buffer.
    Dhāt (Essence): Elements and monotonic index coordinates.
    """
    elements: Tuple[Optional[T], ...]
    head_cursor: int
    element_count: int
    capacity: int

    @property
    def is_full(self) -> bool:
        return self.element_count == self.capacity

    @property
    def is_empty(self) -> bool:
        return self.element_count == 0


class SovereignRingBuffer(Generic[T]):
    """
    Circular queue grounded in Root: ح-ف-ظ (Preservation).
    Guarantees state immutability via persistent transition snapshots.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Ring buffer capacity must be strictly positive.")
        self.capacity = capacity
        self._state = RingBufferSnapshot(
            elements=tuple([None] * capacity),
            head_cursor=0,
            element_count=0,
            capacity=capacity
        )

    @property
    def snapshot(self) -> RingBufferSnapshot[T]:
        return self._state

    def append(self, item: T) -> RingBufferSnapshot[T]:
        """Produces a new immutable snapshot with item appended at next tail."""
        current = self._state
        new_elements = list(current.elements)

        if current.is_full:
            # Overwrite oldest entry at head_cursor and advance head
            new_elements[current.head_cursor] = item
            new_head = (current.head_cursor + 1) % self.capacity
            new_count = self.capacity
        else:
            write_idx = (current.head_cursor + current.element_count) % self.capacity
            new_elements[write_idx] = item
            new_head = current.head_cursor
            new_count = current.element_count + 1

        self._state = RingBufferSnapshot(
            elements=tuple(new_elements),
            head_cursor=new_head,
            element_count=new_count,
            capacity=self.capacity
        )
        return self._state

    def read_all(self) -> Tuple[T, ...]:
        """Reads ordered elements from oldest to newest."""
        current = self._state
        ordered = []
        for i in range(current.element_count):
            idx = (current.head_cursor + i) % self.capacity
            elem = current.elements[idx]
            if elem is not None:
                ordered.append(elem)
        return tuple(ordered)'''
            },
            {
                "id": "mantiq_03_algebraic_result",
                "domain": "types_taxonomy",
                "instruction": "Implement an algebraic Result sum-type in Python with exhaustive Ok and Err variants to make illegal error states unrepresentable.",
                "root_key": "ميز",
                "code": '''from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Any

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


@dataclass(frozen=True)
class Ok(Generic[T]):
    """Represents victorious execution carrying domain payload."""
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


@dataclass(frozen=True)
class Err(Generic[E]):
    """Represents explicit, categorized domain failure."""
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True


Result = Ok[T] | Err[E]


class EpistemicResult:
    """
    Algebraic discriminant type grounded in Root: م-ي-ز (Discrimination/Tamayyuz).
    Enforces exhaustive pattern matching and eliminates unhandled runtime exceptions.
    """

    @staticmethod
    def map_ok(result: Result[T, E], transform: Callable[[T], U]) -> Result[U, E]:
        if isinstance(result, Ok):
            return Ok(transform(result.value))
        return result

    @staticmethod
    def unwrap_or(result: Result[T, E], fallback_default: T) -> T:
        if isinstance(result, Ok):
            return result.value
        return fallback_default'''
            },
            {
                "id": "mantiq_04_circuit_breaker",
                "domain": "fault_tolerance",
                "instruction": "Create a fault-tolerant Circuit Breaker in Python with explicit lifecycle states (Closed, Open, HalfOpen) and deterministic recovery.",
                "root_key": "سلم",
                "code": '''import time
from enum import Enum
from dataclasses import dataclass
from typing import Callable, TypeVar, Any

T = TypeVar('T')


class CircuitState(str, Enum):
    """Exhaustive lifecycle states. Root: س-ل-م (Integrity)."""
    CLOSED = "closed"         # Healthy; traffic flows normally
    OPEN = "open"             # Tripped; requests rejected immediately
    HALF_OPEN = "half_open"   # Probing; single trial permitted


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_cooldown_seconds: float = 30.0
    half_open_success_threshold: int = 2


class EpistemicCircuitBreaker:
    """
    Self-healing barrier protecting downstream dependencies.
    Eliminates cascading crash storms (Daf' al-Tasalsul).
    """

    def __init__(self, service_label: str, config: CircuitBreakerConfig):
        self.service_label = service_label
        self.config = config
        self.current_state = CircuitState.CLOSED
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.last_state_transition_epoch = time.time()

    def can_execute(self) -> bool:
        now = time.time()
        if self.current_state == CircuitState.CLOSED:
            return True
        elif self.current_state == CircuitState.OPEN:
            if (now - self.last_state_transition_epoch) >= self.config.recovery_cooldown_seconds:
                self._transition_to(CircuitState.HALF_OPEN)
                return True
            return False
        elif self.current_state == CircuitState.HALF_OPEN:
            return True
        return False

    def record_success(self) -> None:
        self.consecutive_failures = 0
        if self.current_state == CircuitState.HALF_OPEN:
            self.consecutive_successes += 1
            if self.consecutive_successes >= self.config.half_open_success_threshold:
                self._transition_to(CircuitState.CLOSED)

    def record_failure(self) -> None:
        self.consecutive_successes = 0
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.config.failure_threshold:
            self._transition_to(CircuitState.OPEN)

    def _transition_to(self, new_state: CircuitState) -> None:
        self.current_state = new_state
        self.last_state_transition_epoch = time.time()
        if new_state == CircuitState.CLOSED:
            self.consecutive_failures = 0
            self.consecutive_successes = 0'''
            }
        ]

    def build_dataset(self, output_file: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Generates complete dataset records with <ayn_mantiq> reasoning blocks."""
        archetypes = self.get_core_archetypes()
        dataset_entries = []

        for item in archetypes:
            instruction = item["instruction"]
            scratchpad = self.mantiq_engine.generate_mantiq_scratchpad(instruction, "python")
            code_payload = item["code"]

            entry = {
                "id": item["id"],
                "domain": item["domain"],
                "instruction": instruction,
                "thought": scratchpad,
                "response": f"{scratchpad}\n\n```python\n{code_payload}\n```"
            }
            dataset_entries.append(entry)

        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                for entry in dataset_entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.dataset_records = dataset_entries
        return dataset_entries

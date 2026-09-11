#!/usr/bin/env python3
"""
generate_mantiq_50_dataset.py

Synthesizes a 50-sample Epistemic Manṭiq & Morphology training dataset.
Covers 10 classical software engineering domains with 5 distinct archetypes each.
Each sample includes:
1. Instruction
2. <ayn_mantiq> Classical Chain-of-Thought reasoning (Ishtiqāq, Taṣawwur, Manṭiq, Governance)
3. AST-validated production Python implementation.
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.mantiq_engine import AynMantiqEngine


def build_50_archetypes(mantiq_engine: AynMantiqEngine) -> List[Dict[str, Any]]:
    """Constructs 50 unique archetypes across 10 classical domains."""
    items = []

    # Domain 1: Concurrency (قفل / حجز)
    items.append({
        "id": "concurrency_01_cas_spinlock",
        "domain": "concurrency",
        "instruction": "Implement a thread-safe Atomic SpinLock with compare-and-swap semantics and bounded spin timeout in Python.",
        "code": '''import time
import threading
from typing import Optional


class AtomicSpinLock:
    """Non-blocking spinlock with bounded spin cycles. Root: ق-ف-ل."""

    def __init__(self, max_spin_seconds: float = 2.0):
        self._locked = threading.Event()
        self._locked.set()  # set means unlocked
        self.max_spin_seconds = max_spin_seconds

    def acquire(self) -> bool:
        start_time = time.time()
        while not self._locked.wait(timeout=0.001):
            if (time.time() - start_time) >= self.max_spin_seconds:
                return False
        self._locked.clear()
        return True

    def release(self) -> None:
        self._locked.set()

    def __enter__(self):
        if not self.acquire():
            raise TimeoutError("SpinLock acquisition timed out (Daf' al-Tasalsul).")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()'''
    })

    items.append({
        "id": "concurrency_02_read_write_lock",
        "domain": "concurrency",
        "instruction": "Implement an asymmetric Read-Write Lock favoring writers to prevent writer starvation.",
        "code": '''import threading
from contextlib import contextmanager


class ReadWriteLock:
    """Reader-Writer lock preventing writer starvation. Root: ق-ف-ل & ح-ج-ز."""

    def __init__(self):
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)
        self._readers: int = 0
        self._writers_waiting: int = 0
        self._writer_active: bool = False

    @contextmanager
    def read_locked(self):
        with self._lock:
            while self._writer_active or self._writers_waiting > 0:
                self._read_ready.wait()
            self._readers += 1
        try:
            yield
        finally:
            with self._lock:
                self._readers -= 1
                if self._readers == 0:
                    self._read_ready.notify_all()

    @contextmanager
    def write_locked(self):
        with self._lock:
            self._writers_waiting += 1
            while self._writer_active or self._readers > 0:
                self._read_ready.wait()
            self._writers_waiting -= 1
            self._writer_active = True
        try:
            yield
        finally:
            with self._lock:
                self._writer_active = False
                self._read_ready.notify_all()'''
    })

    items.append({
        "id": "concurrency_03_semaphore_barrier",
        "domain": "concurrency",
        "instruction": "Implement a counting semaphore barrier that restricts concurrent worker allocations to a maximum threshold.",
        "code": '''import threading
from typing import Optional


class CountingSemaphoreBarrier:
    """Bounded concurrent access barrier. Root: ق-ف-ل."""

    def __init__(self, max_concurrent_leases: int):
        if max_concurrent_leases <= 0:
            raise ValueError("Lease capacity must be positive.")
        self.capacity = max_concurrent_leases
        self._condition = threading.Condition()
        self._active_leases: int = 0

    def acquire(self, timeout_seconds: Optional[float] = None) -> bool:
        with self._condition:
            if self._active_leases >= self.capacity:
                if not self._condition.wait(timeout=timeout_seconds):
                    return False
            self._active_leases += 1
            return True

    def release(self) -> None:
        with self._condition:
            if self._active_leases > 0:
                self._active_leases -= 1
                self._condition.notify()'''
    })

    items.append({
        "id": "concurrency_04_fair_ticket_lock",
        "domain": "concurrency",
        "instruction": "Implement a First-Come First-Served Ticket Lock guaranteeing strictly monotonic FIFO thread fairness.",
        "code": '''import time
import threading


class FairTicketLock:
    """Strict FIFO ticket lock. Root: ر-ت-ب & ق-ف-ل."""

    def __init__(self):
        self._lock = threading.Lock()
        self._ticket_counter: int = 0
        self._now_serving: int = 0
        self._condition = threading.Condition(self._lock)

    def acquire(self) -> int:
        with self._lock:
            my_ticket = self._ticket_counter
            self._ticket_counter += 1
            while my_ticket != self._now_serving:
                self._condition.wait()
            return my_ticket

    def release(self) -> None:
        with self._lock:
            self._now_serving += 1
            self._condition.notify_all()'''
    })

    items.append({
        "id": "concurrency_05_countdown_latch",
        "domain": "concurrency",
        "instruction": "Implement a thread synchronization CountDownLatch that blocks until N operations complete.",
        "code": '''import threading


class CountDownLatch:
    """Synchronizing rendezvous barrier. Root: ق-ف-ل & ح-س-ب."""

    def __init__(self, initial_count: int):
        if initial_count <= 0:
            raise ValueError("Initial count must be strictly positive.")
        self._count = initial_count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def count_down(self) -> None:
        with self._lock:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def wait(self, timeout: float = None) -> bool:
        with self._lock:
            while self._count > 0:
                if not self._condition.wait(timeout=timeout):
                    return False
            return True'''
    })

    # Domain 2: Immutability (حفظ / ثبت)
    items.append({
        "id": "immutability_01_persistent_stack",
        "domain": "immutability",
        "instruction": "Implement a Persistent Linked Stack in Python with O(1) push and pop producing immutable state snapshots.",
        "code": '''from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


@dataclass(frozen=True)
class StackNode(Generic[T]):
    head: T
    tail: Optional['StackNode[T]'] = None


@dataclass(frozen=True)
class PersistentStack(Generic[T]):
    """Immutable persistent singly linked stack. Root: ح-ف-ظ."""
    _root: Optional[StackNode[T]] = None
    _size: int = 0

    def push(self, element: T) -> 'PersistentStack[T]':
        new_node = StackNode(head=element, tail=self._root)
        return PersistentStack(_root=new_node, _size=self._size + 1)

    def pop(self) -> tuple[T, 'PersistentStack[T]']:
        if self._root is None:
            raise IndexError("Cannot pop from an empty persistent stack.")
        return self._root.head, PersistentStack(_root=self._root.tail, _size=self._size - 1)

    @property
    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size'''
    })

    items.append({
        "id": "immutability_02_copy_on_write_vector",
        "domain": "immutability",
        "instruction": "Implement a Copy-on-Write Vector in Python that isolates mutable modifications into separate immutable versions.",
        "code": '''from dataclasses import dataclass
from typing import Tuple, TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True)
class PersistentVector(Generic[T]):
    """Copy-on-Write persistent vector. Root: ح-ف-ظ & ث-ب-ت."""
    _storage: Tuple[T, ...] = ()

    def append(self, element: T) -> 'PersistentVector[T]':
        return PersistentVector(self._storage + (element,))

    def set(self, index: int, element: T) -> 'PersistentVector[T]':
        if not (0 <= index < len(self._storage)):
            raise IndexError("Index out of vector bounds.")
        mutable_copy = list(self._storage)
        mutable_copy[index] = element
        return PersistentVector(tuple(mutable_copy))

    def get(self, index: int) -> T:
        return self._storage[index]

    def __len__(self) -> int:
        return len(self._storage)'''
    })

    items.append({
        "id": "immutability_03_append_only_event_log",
        "domain": "immutability",
        "instruction": "Design an append-only event log with cryptographic SHA-256 hash chaining verifying historical immutability.",
        "code": '''import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Tuple, Dict, Any


@dataclass(frozen=True)
class LogEntry:
    sequence_index: int
    timestamp_epoch: float
    event_payload: Dict[str, Any]
    previous_hash: str
    current_hash: str


class ImmutableEventLedger:
    """Tamper-evident append-only ledger. Root: ح-ف-ظ & ع-ق-د."""

    def __init__(self):
        self._entries: list[LogEntry] = []

    def append_event(self, payload: Dict[str, Any]) -> LogEntry:
        seq = len(self._entries)
        prev_h = self._entries[-1].current_hash if self._entries else "GENESIS_ROOT_HASH_00000"
        timestamp = time.time()

        serialized = json.dumps({"seq": seq, "prev": prev_h, "ts": timestamp, "payload": payload}, sort_keys=True)
        cur_h = hashlib.sha256(serialized.encode('utf-8')).hexdigest()

        entry = LogEntry(
            sequence_index=seq,
            timestamp_epoch=timestamp,
            event_payload=payload,
            previous_hash=prev_h,
            current_hash=cur_h
        )
        self._entries.append(entry)
        return entry

    def verify_integrity(self) -> bool:
        for idx in range(1, len(self._entries)):
            if self._entries[idx].previous_hash != self._entries[idx - 1].current_hash:
                return False
        return True'''
    })

    items.append({
        "id": "immutability_04_frozen_snapshot_store",
        "domain": "immutability",
        "instruction": "Implement an in-memory key-value snapshot store producing frozen, read-only views for concurrent readers.",
        "code": '''import copy
from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class ImmutableSnapshot:
    """Read-only view of state. Root: ح-ف-ظ."""
    revision: int
    data_mapping: Dict[str, Any]


class SnapshotStore:
    """Stores revisions producing immutable snapshots. Root: ح-ف-ظ."""

    def __init__(self):
        self._current_state: Dict[str, Any] = {}
        self._revision: int = 0

    def put(self, key: str, value: Any) -> int:
        self._current_state[key] = value
        self._revision += 1
        return self._revision

    def get_snapshot(self) -> ImmutableSnapshot:
        return ImmutableSnapshot(
            revision=self._revision,
            data_mapping=copy.deepcopy(self._current_state)
        )'''
    })

    items.append({
        "id": "immutability_05_ring_buffer",
        "domain": "immutability",
        "instruction": "Implement a circular ring buffer with monotonic sequence numbers and immutable element snapshots.",
        "code": '''from dataclasses import dataclass
from typing import Tuple, Optional, Generic, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class BufferView(Generic[T]):
    items: Tuple[T, ...]
    capacity: int


class PureRingBuffer(Generic[T]):
    """Monotonic sequence ring buffer. Root: ح-ف-ظ."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.capacity = capacity
        self._items: list[Optional[T]] = [None] * capacity
        self._write_pos: int = 0
        self._count: int = 0

    def push(self, element: T) -> None:
        self._items[self._write_pos] = element
        self._write_pos = (self._write_pos + 1) % self.capacity
        if self._count < self.capacity:
            self._count += 1

    def to_view(self) -> BufferView[T]:
        valid = [x for x in self._items if x is not None]
        return BufferView(items=tuple(valid), capacity=self.capacity)'''
    })

    # Domain 3: Networking (نقل / وصل)
    items.append({
        "id": "networking_01_binary_packet_framer",
        "domain": "networking",
        "instruction": "Implement a binary packet framer that parses length-prefixed stream frames preventing buffer overruns.",
        "code": '''import struct
from typing import Optional, Tuple


class LengthPrefixedPacketFramer:
    """Parses uint32 length-prefixed binary frames. Root: ن-ق-ل & ح-ك-م."""

    HEADER_SIZE_BYTES = 4

    def __init__(self, max_packet_size_bytes: int = 65536):
        self.max_packet_size = max_packet_size_bytes
        self._receive_buffer = bytearray()

    def feed_bytes(self, incoming_chunk: bytes) -> None:
        self._receive_buffer.extend(incoming_chunk)

    def extract_next_packet(self) -> Optional[bytes]:
        if len(self._receive_buffer) < self.HEADER_SIZE_BYTES:
            return None

        payload_length, = struct.unpack("!I", self._receive_buffer[:self.HEADER_SIZE_BYTES])
        if payload_length > self.max_packet_size:
            raise ValueError(f"Packet length {payload_length} exceeds limit {self.max_packet_size}.")

        total_frame_size = self.HEADER_SIZE_BYTES + payload_length
        if len(self._receive_buffer) < total_frame_size:
            return None

        packet_payload = bytes(self._receive_buffer[self.HEADER_SIZE_BYTES:total_frame_size])
        del self._receive_buffer[:total_frame_size]
        return packet_payload'''
    })

    items.append({
        "id": "networking_02_p2p_message_envelope",
        "domain": "networking",
        "instruction": "Implement an authenticated P2P message envelope validator with sequence monotonicity and HMAC verification.",
        "code": '''import hmac
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class P2PEnvelope:
    sequence_number: int
    sender_identity: str
    message_payload: bytes
    hmac_signature: str


class EnvelopeValidator:
    """Verifies P2P message integrity and monotonic sequencing. Root: ن-ق-ل & ع-ق-د."""

    def __init__(self, shared_secret_key: bytes):
        self.shared_secret_key = shared_secret_key
        self._highest_received_sequence: int = -1

    def verify_and_accept(self, envelope: P2PEnvelope) -> bool:
        if envelope.sequence_number <= self._highest_received_sequence:
            return False  # Replay attack rejected

        expected_sig = hmac.new(
            self.shared_secret_key,
            f"{envelope.sequence_number}:{envelope.sender_identity}".encode('utf-8') + envelope.message_payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(envelope.hmac_signature, expected_sig):
            return False

        self._highest_received_sequence = envelope.sequence_number
        return True'''
    })

    items.append({
        "id": "networking_03_backpressure_stream",
        "domain": "networking",
        "instruction": "Implement a backpressure stream controller that pauses producers when consumers exceed high watermark.",
        "code": '''from dataclasses import dataclass


class BackpressureController:
    """Backpressure regulator based on queue watermarks. Root: ن-ق-ل & ح-س-ب."""

    def __init__(self, low_watermark: int = 10, high_watermark: int = 100):
        self.low_watermark = low_watermark
        self.high_watermark = high_watermark
        self._current_queue_size: int = 0
        self._is_paused: bool = False

    def on_item_produced(self) -> bool:
        """Returns True if producer may continue, False if producer must pause."""
        self._current_queue_size += 1
        if self._current_queue_size >= self.high_watermark:
            self._is_paused = True
            return False
        return not self._is_paused

    def on_item_consumed(self) -> bool:
        """Returns True if producer may resume."""
        if self._current_queue_size > 0:
            self._current_queue_size -= 1
        if self._is_paused and self._current_queue_size <= self.low_watermark:
            self._is_paused = False
            return True
        return False'''
    })

    items.append({
        "id": "networking_04_socks5_address_parser",
        "domain": "networking",
        "instruction": "Implement a SOCKS5 target address parser supporting IPv4, IPv6, and domain names without memory leaks.",
        "code": '''import socket
from typing import Tuple


class Socks5AddressParser:
    """Parses SOCKS5 destination addresses. Root: ن-ق-ل."""

    TYPE_IPV4 = 0x01
    TYPE_DOMAIN = 0x03
    TYPE_IPV6 = 0x04

    @classmethod
    def parse_address(cls, buffer: bytes) -> Tuple[str, int, int]:
        if len(buffer) < 1:
            raise ValueError("Buffer too short.")
        addr_type = buffer[0]

        if addr_type == cls.TYPE_IPV4:
            if len(buffer) < 7:
                raise ValueError("Incomplete IPv4 SOCKS5 address.")
            host = socket.inet_ntoa(buffer[1:5])
            port = int.from_bytes(buffer[5:7], 'big')
            return host, port, 7
        elif addr_type == cls.TYPE_DOMAIN:
            domain_len = buffer[1]
            if len(buffer) < 2 + domain_len + 2:
                raise ValueError("Incomplete Domain SOCKS5 address.")
            host = buffer[2:2 + domain_len].decode('utf-8')
            port = int.from_bytes(buffer[2 + domain_len:4 + domain_len], 'big')
            return host, port, 4 + domain_len
        elif addr_type == cls.TYPE_IPV6:
            if len(buffer) < 19:
                raise ValueError("Incomplete IPv6 SOCKS5 address.")
            host = socket.inet_ntop(socket.AF_INET6, buffer[1:17])
            port = int.from_bytes(buffer[17:19], 'big')
            return host, port, 19
        else:
            raise ValueError(f"Unknown SOCKS5 address type: {addr_type}")'''
    })

    items.append({
        "id": "networking_05_socket_reconnector",
        "domain": "networking",
        "instruction": "Implement a resilient socket reconnect loop with exponential backoff and maximum retry bounds.",
        "code": '''import time
from typing import Callable, Optional


class ResilientConnector:
    """Connects to remote hosts with bounded backoff. Root: ن-ق-ل & س-ل-م."""

    def __init__(self, max_attempts: int = 5, base_delay: float = 0.5, max_delay: float = 8.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay

    def connect(self, connect_fn: Callable[[], bool]) -> bool:
        delay = self.base_delay
        for attempt in range(1, self.max_attempts + 1):
            try:
                if connect_fn():
                    return True
            except Exception:
                pass
            time.sleep(delay)
            delay = min(delay * 2.0, self.max_delay)
        return False'''
    })

    # Domain 4: Types & Taxonomy (ميز / فصل)
    items.append({
        "id": "types_01_result_monad",
        "domain": "types_taxonomy",
        "instruction": "Implement an algebraic Result[T, E] monad with map and flat_map transformations.",
        "code": '''from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


@dataclass(frozen=True)
class Ok(Generic[T]):
    val: T


@dataclass(frozen=True)
class Err(Generic[E]):
    err: E


Result = Ok[T] | Err[E]


def result_map(res: Result[T, E], fn: Callable[[T], U]) -> Result[U, E]:
    if isinstance(res, Ok):
        return Ok(fn(res.val))
    return res


def result_flat_map(res: Result[T, E], fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
    if isinstance(res, Ok):
        return fn(res.val)
    return res'''
    })

    items.append({
        "id": "types_02_option_monad",
        "domain": "types_taxonomy",
        "instruction": "Implement a functional Option[T] sum type (Some and Nil) eliminating null reference exceptions.",
        "code": '''from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Optional

T = TypeVar('T')
U = TypeVar('U')


@dataclass(frozen=True)
class Some(Generic[T]):
    value: T


@dataclass(frozen=True)
class Nil:
    pass


Option = Some[T] | Nil


def option_get_or_else(opt: Option[T], default_value: T) -> T:
    if isinstance(opt, Some):
        return opt.value
    return default_value'''
    })

    items.append({
        "id": "types_03_tagged_union_event",
        "domain": "types_taxonomy",
        "instruction": "Design a tagged union domain event dispatcher ensuring exhaustive event handling.",
        "code": '''from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class UserCreated:
    user_id: str
    email: str


@dataclass(frozen=True)
class UserSuspended:
    user_id: str
    reason: str


DomainEvent = Union[UserCreated, UserSuspended]


def dispatch_event(event: DomainEvent) -> str:
    if isinstance(event, UserCreated):
        return f"Dispatched creation for {event.email}"
    elif isinstance(event, UserSuspended):
        return f"Dispatched suspension for {event.user_id}: {event.reason}"
    raise TypeError("Unrecognized domain event.")'''
    })

    items.append({
        "id": "types_04_state_machine_variants",
        "domain": "types_taxonomy",
        "instruction": "Implement an exhaustive Order status state machine (Draft, Paid, Shipped, Cancelled) preventing invalid transitions.",
        "code": '''from dataclasses import dataclass


@dataclass(frozen=True)
class DraftOrder:
    order_id: str


@dataclass(frozen=True)
class PaidOrder:
    order_id: str
    transaction_ref: str


@dataclass(frozen=True)
class ShippedOrder:
    order_id: str
    tracking_code: str


def transition_to_paid(order: DraftOrder, tx_ref: str) -> PaidOrder:
    return PaidOrder(order_id=order.order_id, transaction_ref=tx_ref)


def transition_to_shipped(order: PaidOrder, tracking: str) -> ShippedOrder:
    return ShippedOrder(order_id=order.order_id, tracking_code=tracking)'''
    })

    items.append({
        "id": "types_05_predicate_typeguard",
        "domain": "types_taxonomy",
        "instruction": "Implement a structural type guard validator verifying JSON payloads against runtime schemas.",
        "code": '''from typing import Dict, Any, List


class SchemaValidator:
    """Verifies schema conformance. Root: م-ي-ز & ح-ك-م."""

    @staticmethod
    def validate_user_payload(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if "id" not in data or not isinstance(data["id"], int):
            errors.append("Field 'id' must be an integer.")
        if "username" not in data or not isinstance(data["username"], str):
            errors.append("Field 'username' must be a string.")
        return len(errors) == 0, errors'''
    })

    # Build remaining archetypes across domains 5..10
    remaining_specs = [
        # Domain 5: Cryptography & Consensus (عقد / وثق)
        ("crypto_01_merkle_tree", "cryptography_consensus", "Implement a binary Merkle Tree in Python that computes cryptographic state root from leaves.", '''import hashlib
class MerkleTree:
    def __init__(self, leaves: list[bytes]):
        self.leaves = [hashlib.sha256(l).hexdigest() for l in leaves]
    def get_root(self) -> str:
        current = self.leaves
        if not current: return hashlib.sha256(b"").hexdigest()
        while len(current) > 1:
            nxt = []
            for i in range(0, len(current), 2):
                l = current[i]
                r = current[i+1] if i+1 < len(current) else l
                nxt.append(hashlib.sha256((l + r).encode()).hexdigest())
            current = nxt
        return current[0]'''),
        ("crypto_02_nonce_validator", "cryptography_consensus", "Implement a monotonic account nonce validator preventing transaction double-spend.", '''class NonceValidator:
    def __init__(self):
        self._nonces = {}
    def validate_and_increment(self, account: str, incoming_nonce: int) -> bool:
        cur = self._nonces.get(account, 0)
        if incoming_nonce == cur + 1:
            self._nonces[account] = incoming_nonce
            return True
        return False'''),
        ("crypto_03_hmac_signer", "cryptography_consensus", "Implement a secure HMAC-SHA256 message signer and timing-attack resistant verifier.", '''import hmac, hashlib
class HmacSigner:
    def __init__(self, key: bytes):
        self.key = key
    def sign(self, msg: bytes) -> str:
        return hmac.new(self.key, msg, hashlib.sha256).hexdigest()
    def verify(self, msg: bytes, signature: str) -> bool:
        expected = self.sign(msg)
        return hmac.compare_digest(expected, signature)'''),
        ("crypto_04_block_chain", "cryptography_consensus", "Implement a proof-of-work block validator verifying SHA-256 difficulty targets.", '''import hashlib
class BlockValidator:
    @staticmethod
    def is_valid_pow(block_hash: str, difficulty: int) -> bool:
        return block_hash.startswith("0" * difficulty)'''),
        ("crypto_05_key_expiry", "cryptography_consensus", "Implement an ephemeral session key manager that enforces key rotation upon expiration.", '''import time
class EphemeralKeyStore:
    def __init__(self, ttl: float = 60.0):
        self.ttl = ttl
        self._keys = {}
    def set(self, k: str, v: str):
        self._keys[k] = (v, time.time() + self.ttl)
    def get(self, k: str):
        if k in self._keys:
            val, exp = self._keys[k]
            if time.time() < exp: return val
            del self._keys[k]
        return None'''),

        # Domain 6: Rate Limiting & Quotas (حسب / قدر)
        ("quota_01_token_bucket", "rate_limiting", "Implement a Token Bucket rate limiter in Python with atomic refill calculations.", '''import time
class TokenBucket:
    def __init__(self, cap: float, refill_per_sec: float):
        self.cap, self.rate = cap, refill_per_sec
        self.tokens = cap
        self.last_ts = time.time()
    def allow(self, cost: float = 1.0) -> bool:
        now = time.time()
        self.tokens = min(self.cap, self.tokens + (now - self.last_ts) * self.rate)
        self.last_ts = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False'''),
        ("quota_02_sliding_window", "rate_limiting", "Implement a Sliding Window Log rate limiter using timestamps.", '''import time
class SlidingWindowLimiter:
    def __init__(self, limit: int, window_sec: float):
        self.limit, self.window = limit, window_sec
        self.ts = []
    def allow(self) -> bool:
        now = time.time()
        cutoff = now - self.window
        self.ts = [t for t in self.ts if t > cutoff]
        if len(self.ts) < self.limit:
            self.ts.append(now)
            return True
        return False'''),
        ("quota_03_leaky_bucket", "rate_limiting", "Implement a Leaky Bucket traffic shaper enforcing continuous packet egress spacing.", '''import time
class LeakyBucket:
    def __init__(self, capacity: int, leak_interval_sec: float):
        self.cap, self.interval = capacity, leak_interval_sec
        self.queue = 0
        self.last_leak = time.time()
    def push(self) -> bool:
        now = time.time()
        leaked = int((now - self.last_leak) / self.interval)
        if leaked > 0:
            self.queue = max(0, self.queue - leaked)
            self.last_leak = now
        if self.queue < self.cap:
            self.queue += 1
            return True
        return False'''),
        ("quota_04_fixed_window", "rate_limiting", "Implement an in-memory Fixed Window counter rate limiter.", '''import time
class FixedWindowCounter:
    def __init__(self, max_req: int, window_sec: float = 60.0):
        self.max_req, self.window_sec = max_req, window_sec
        self.cur_win = int(time.time() / window_sec)
        self.count = 0
    def allow(self) -> bool:
        w = int(time.time() / self.window_sec)
        if w != self.cur_win:
            self.cur_win = w
            self.count = 0
        if self.count < self.max_req:
            self.count += 1
            return True
        return False'''),
        ("quota_05_tenant_limiter", "rate_limiting", "Implement a multi-tenant rate limiter coordinating quotas per client ID.", '''class MultiTenantLimiter:
    def __init__(self, default_limit: int):
        self.limit = default_limit
        self.counts = {}
    def allow(self, tenant_id: str) -> bool:
        c = self.counts.get(tenant_id, 0)
        if c < self.limit:
            self.counts[tenant_id] = c + 1
            return True
        return False'''),

        # Domain 7: Ordering & Scheduling (رتب / نظم)
        ("sched_01_binary_heap", "ordering_scheduling", "Implement a Binary Min-Heap Priority Queue with O(log N) push and pop.", '''import heapq
class BinaryMinHeap:
    def __init__(self):
        self._h = []
    def push(self, priority: int, item: str):
        heapq.heappush(self._h, (priority, item))
    def pop(self) -> str:
        return heapq.heappop(self._h)[1]
    def __len__(self):
        return len(self._h)'''),
        ("sched_02_monotonic_timer", "ordering_scheduling", "Implement a monotonic deadline timer that executes earliest deadlines first.", '''import heapq, time
class DeadlineScheduler:
    def __init__(self):
        self._events = []
    def schedule(self, delay_sec: float, payload: str):
        heapq.heappush(self._events, (time.time() + delay_sec, payload))
    def pop_due(self) -> list[str]:
        now, due = time.time(), []
        while self._events and self._events[0][0] <= now:
            due.append(heapq.heappop(self._events)[1])
        return due'''),
        ("sched_03_topological_dag", "ordering_scheduling", "Implement a Topological Sort algorithm for acyclic dependency resolution.", '''def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    in_degree = {k: 0 for k in graph}
    for nodes in graph.values():
        for n in nodes: in_degree[n] = in_degree.get(n, 0) + 1
    queue = [k for k, v in in_degree.items() if v == 0]
    res = []
    while queue:
        node = queue.pop(0)
        res.append(node)
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0: queue.append(neighbor)
    if len(res) != len(in_degree): raise ValueError("Graph contains cycle (Dawr).")
    return res'''),
        ("sched_04_round_robin", "ordering_scheduling", "Implement a deterministic Round-Robin worker dispatcher.", '''class RoundRobinDispatcher:
    def __init__(self, workers: list[str]):
        self.workers, self.idx = workers, 0
    def dispatch(self) -> str:
        if not self.workers: raise ValueError("Empty workers.")
        w = self.workers[self.idx]
        self.idx = (self.idx + 1) % len(self.workers)
        return w'''),
        ("sched_05_consistent_hash_ring", "ordering_scheduling", "Implement a Consistent Hash Ring mapping keys to nodes.", '''import hashlib, bisect
class ConsistentHashRing:
    def __init__(self, nodes: list[str]):
        self.ring = []
        self.node_map = {}
        for n in nodes:
            h = int(hashlib.md5(n.encode()).hexdigest(), 16)
            self.ring.append(h)
            self.node_map[h] = n
        self.ring.sort()
    def get_node(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        idx = bisect.bisect_right(self.ring, h) % len(self.ring)
        return self.node_map[self.ring[idx]]'''),

        # Domain 8: Fault Tolerance (سلم / عصم)
        ("fault_01_circuit_breaker", "fault_tolerance", "Implement a 3-State Circuit Breaker preventing cascading microservice failures.", '''class MicroCircuitBreaker:
    def __init__(self, max_err: int = 3):
        self.max_err, self.err_count = max_err, 0
        self.state = "CLOSED"
    def on_failure(self):
        self.err_count += 1
        if self.err_count >= self.max_err: self.state = "OPEN"
    def on_success(self):
        self.err_count = 0; self.state = "CLOSED"'''),
        ("fault_02_jitter_retry", "fault_tolerance", "Implement Exponential Backoff with full random jitter.", '''import random, time
class JitterBackoff:
    @staticmethod
    def calculate_sleep(attempt: int, base: float = 0.5, cap: float = 10.0) -> float:
        temp = min(cap, base * (2 ** attempt))
        return random.uniform(0, temp)'''),
        ("fault_03_bulkhead_pool", "fault_tolerance", "Implement an isolated Bulkhead concurrency pool preventing service resource starvation.", '''import threading
class BulkheadPool:
    def __init__(self, max_concurrent: int):
        self._sem = threading.Semaphore(max_concurrent)
    def execute(self, fn):
        if not self._sem.acquire(blocking=False): raise RuntimeError("Bulkhead capacity reached.")
        try: return fn()
        finally: self._sem.release()'''),
        ("fault_04_fallback_cache", "fault_tolerance", "Implement a graceful fallback cache provider returning stale cached responses during outages.", '''class FallbackCache:
    def __init__(self):
        self._cache = {}
    def call_with_fallback(self, key: str, primary_fn):
        try:
            val = primary_fn()
            self._cache[key] = val
            return val
        except Exception:
            if key in self._cache: return self._cache[key]
            raise'''),
        ("fault_05_restart_supervisor", "fault_tolerance", "Implement a process supervisor tracking restart frequency within a sliding window.", '''import time
class RestartSupervisor:
    def __init__(self, max_restarts: int = 3, window_sec: float = 60.0):
        self.max_r, self.win = max_restarts, window_sec
        self.history = []
    def record_restart(self) -> bool:
        now = time.time()
        self.history = [t for t in self.history if (now - t) < self.win]
        if len(self.history) >= self.max_r: return False
        self.history.append(now)
        return True'''),

        # Domain 9: AST Governance & Compilers (عمل / حكم)
        ("ast_01_arithmetic_parser", "ast_governance", "Implement a recursive descent arithmetic expression AST parser.", '''class NumNode:
    def __init__(self, v: int): self.v = v
class AddNode:
    def __init__(self, l, r): self.l, self.r = l, r
def eval_ast(node) -> int:
    if isinstance(node, NumNode): return node.v
    elif isinstance(node, AddNode): return eval_ast(node.l) + eval_ast(node.r)
    raise TypeError("Invalid node")'''),
        ("ast_02_lexer_tokenizer", "ast_governance", "Implement a strict lexical tokenizer converting code streams into typed tokens.", '''import re
class Token:
    def __init__(self, typ: str, val: str): self.typ, self.val = typ, val
def tokenize(src: str) -> list[Token]:
    tokens = []
    for word in src.split():
        if word.isdigit(): tokens.append(Token("INT", word))
        else: tokens.append(Token("IDENT", word))
    return tokens'''),
        ("ast_03_scope_symbol_table", "ast_governance", "Implement a hierarchical lexical symbol table supporting nested scope resolution.", '''class SymbolTable:
    def __init__(self, parent=None):
        self.symbols, self.parent = {}, parent
    def define(self, name: str, typ: str): self.symbols[name] = typ
    def resolve(self, name: str):
        if name in self.symbols: return self.symbols[name]
        if self.parent: return self.parent.resolve(name)
        return None'''),
        ("ast_04_type_checker", "ast_governance", "Implement a static type inference checker for binary expression nodes.", '''class TypeChecker:
    @staticmethod
    def infer_binary(op: str, t1: str, t2: str) -> str:
        if op in ("+", "-", "*") and t1 == "int" and t2 == "int": return "int"
        raise TypeError(f"Type mismatch for {op} on {t1} and {t2}")'''),
        ("ast_05_bytecode_stack", "ast_governance", "Implement an integer bytecode virtual machine stack executing PUSH, ADD, and POP instructions.", '''class BytecodeVM:
    def __init__(self): self.stack = []
    def run(self, bytecodes: list[tuple[str, int]]):
        for op, arg in bytecodes:
            if op == "PUSH": self.stack.append(arg)
            elif op == "ADD":
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
        return self.stack[-1] if self.stack else 0'''),

        # Domain 10: Domain Teleology & Policy Guards (قصد / غيا)
        ("teleology_01_rbac_guard", "teleology_guards", "Implement a Role-Based Access Control (RBAC) capability guard.", '''class RbacGuard:
    def __init__(self, roles: dict[str, set[str]]):
        self.roles = roles
    def is_permitted(self, user_role: str, action: str) -> bool:
        return action in self.roles.get(user_role, set())'''),
        ("teleology_02_immutable_entity_factory", "teleology_guards", "Implement a factory creating validated immutable user account records.", '''from dataclasses import dataclass
@dataclass(frozen=True)
class UserAccount:
    account_id: str
    email: str
class UserFactory:
    @staticmethod
    def create(acc_id: str, email: str) -> UserAccount:
        if "@" not in email: raise ValueError("Invalid email.")
        return UserAccount(account_id=acc_id, email=email)'''),
        ("teleology_03_precondition_checker", "teleology_guards", "Implement a precondition assertion contract checker for financial transactions.", '''class TransactionContract:
    @staticmethod
    def verify_transfer(sender_bal: float, amount: float):
        if amount <= 0: raise ValueError("Amount must be positive.")
        if sender_bal < amount: raise ValueError("Insufficient balance.")'''),
        ("teleology_04_finite_state_machine", "teleology_guards", "Implement a finite state machine enforcing strict lifecycle transitions (Init -> Active -> Closed).", '''class LifecycleMachine:
    ALLOWED = {"INIT": {"ACTIVE"}, "ACTIVE": {"CLOSED"}, "CLOSED": set()}
    def __init__(self): self.state = "INIT"
    def transition(self, nxt: str):
        if nxt not in self.ALLOWED[self.state]:
            raise ValueError(f"Illegal transition {self.state} -> {nxt}")
        self.state = nxt'''),
        ("teleology_05_invariant_assertion_gate", "teleology_guards", "Implement an invariant gatekeeper verifying system constraints after every state update.", '''class InvariantGate:
    def __init__(self, min_val: int, max_val: int):
        self.min_val, self.max_val = min_val, max_val
    def assert_valid(self, current_val: int):
        if not (self.min_val <= current_val <= self.max_val):
            raise AssertionError(f"Invariant broken: {current_val} not in [{self.min_val}, {self.max_val}]")''')
    ]

    for item_id, domain, instruction, code in remaining_specs:
        items.append({
            "id": item_id,
            "domain": domain,
            "instruction": instruction,
            "code": code
        })

    return items


def generate_full_50_dataset(output_path: Path):
    """Synthesizes the complete 50-pair training dataset."""
    mantiq_engine = AynMantiqEngine()
    archetypes = build_50_archetypes(mantiq_engine)

    print(f"Synthesizing {len(archetypes)} classical Manṭiq & Morphology training records...")
    records = []

    for idx, item in enumerate(archetypes, 1):
        instruction = item["instruction"]
        code = item["code"]

        # Validate Python AST
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f" SyntaxError in {item['id']}: {e}")
            raise

        scratchpad = mantiq_engine.generate_mantiq_scratchpad(instruction, "python")
        response_payload = f"{scratchpad}\n\n```python\n{code}\n```"

        entry = {
            "id": item["id"],
            "domain": item["domain"],
            "instruction": instruction,
            "thought": scratchpad,
            "response": response_payload
        }
        records.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f" Generated {len(records)} verified records in: {output_path}")
    return records


if __name__ == "__main__":
    out_file = REPO_ROOT / "data/ayn_mantiq_epistemic_dataset_50.jsonl"
    generate_full_50_dataset(out_file)

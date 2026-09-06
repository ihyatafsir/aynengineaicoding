#!/usr/bin/env python3
"""
code_lexicon_mapper.py

AynEngine AI Coding Edition (v2.0): Epistemic Classical Lexicon Bridge
Maps modern software engineering concepts and programming invariants to the 5 Classical Arabic Lexicographical & Grammatical Pillars:
1. Al-Mufradāt fī Gharīb al-Qurʾān (al-Rāghib al-Iṣfahānī) -> Ontological Domain Modeling & Teleology
2. Asās al-Balāghah (al-Zamakhsharī) -> Idiomatic Eloquence & Abstraction Integrity (Ḥaqīqah vs Majāz)
3. Lisān al-ʿArab (Ibn Manẓūr) -> Exhaustive State-Space, Edge-Cases, & Error Taxonomy
4. Kitāb al-ʿAyn (al-Farāhīdī) -> Atomic Primitive Decomposition & State Combinatorics
5. Al-Kitāb (Sībawayh) -> Syntactic Governance (ʿĀmil/Maʿmūl), AST Hierarchy & Strict Typing
"""

import re
from typing import Dict, List, Any, Optional

# Software Engineering Dimension -> Classical Roots & Lexical Conceptual Anchors
CONCEPT_ROOT_TAXONOMY = {
    "concurrency": {
        "roots": ["جمع", "زمن", "سوق", "حجز", "فوج", "جري"],
        "pillar_focus": "Kitāb al-ʿAyn & Sībawayh",
        "description": "Multi-agent coordination, event loops, mutexes, and non-blocking scheduling"
    },
    "immutability": {
        "roots": ["ثبت", "حفظ", "بقي", "صلب", "جمد", "عصم"],
        "pillar_focus": "Al-Mufradāt & Asās al-Balāghah",
        "description": "State permanence, pure functions, absence of side-effects, and persistent state structures"
    },
    "types": {
        "roots": ["ميز", "حدّ", "صنف", "حكم", "فصل", "نعت"],
        "pillar_focus": "Al-Kitāb (Sībawayh) & Al-Mufradāt",
        "description": "Algebraic domain types, structural invariants, type guards, and compile-time correctness"
    },
    "error_handling": {
        "roots": ["درء", "عطب", "كشف", "رجع", "سلم", "عذر"],
        "pillar_focus": "Lisān al-ʿArab",
        "description": "Exhaustive edge-case matching, error taxonomy, backpressure, and fault-tolerance"
    },
    "abstraction": {
        "roots": ["جوز", "حقق", "لبس", "صفا", "رمز", "ستر"],
        "pillar_focus": "Asās al-Balāghah",
        "description": "Metaphor vs reality (Majāz vs Ḥaqīqah), zero leaky abstractions, and code minimalism"
    },
    "decomposition": {
        "roots": ["أصل", "فصل", "فرع", "بسط", "جزء", "قسم"],
        "pillar_focus": "Kitāb al-ʿAyn",
        "description": "Orthogonal primitive decomposition, single-responsibility, and modular cohesion"
    },
    "governance": {
        "roots": ["عمل", "حكم", "قود", "سلط", "ملك", "نظم"],
        "pillar_focus": "Al-Kitāb (Sībawayh)",
        "description": "Explicit caller-callee governance (ʿĀmil wa Maʿmūl), dependency inversion, and pipeline flow"
    },
    "teleology": {
        "roots": ["قصد", "غيا", "حقق", "وضع", "عمد", "نهج"],
        "pillar_focus": "Al-Mufradāt",
        "description": "Domain purpose (Ghāyah), self-evident naming, and semantic contracts"
    },
    # v2 Specialized Domain Expansions:
    "networking_p2p": {
        "roots": ["وصل", "نقل", "قطع", "فرق", "حبل", "ربط", "سلك"],
        "pillar_focus": "Asās al-Balāghah & Lisān al-ʿArab",
        "description": "Peer-to-peer topologies, bilateral sockets, ICE candidate exchange, and tunnel isolation"
    },
    "media_audio": {
        "roots": ["صوت", "سمع", "نغم", "رجع", "صفو", "صخب"],
        "pillar_focus": "Kitāb al-ʿAyn & Asās al-Balāghah",
        "description": "Acoustic streams, PCM audio buffers, WebRTC track management, and echo cancellation"
    },
    "signaling_state": {
        "roots": ["لوح", "علن", "بشر", "ندب", "وفد", "خطر"],
        "pillar_focus": "Al-Kitāb (Sībawayh) & Al-Mufradāt",
        "description": "SDP offer/answer handshakes, presence signals, state machines, and lifecycle transitions"
    },
    "cryptography": {
        "roots": ["سرر", "وثق", "بدل", "قفل", "ختم", "حرز"],
        "pillar_focus": "Al-Mufradāt & Kitāb al-ʿAyn",
        "description": "End-to-end encryption, cryptographic ratchets, key exchange, and tamper-proof authentication"
    },
    "backpressure_queue": {
        "roots": ["طبر", "حبس", "فرغ", "دفق", "كيل", "وسع"],
        "pillar_focus": "Lisān al-ʿArab & Kitāb al-ʿAyn",
        "description": "Bounded queues, backpressure propagation, buffer overflow prevention, and graceful draining"
    },
    "resilience": {
        "roots": ["صمد", "درء", "عصم", "صلب", "نجا", "جبر"],
        "pillar_focus": "Lisān al-ʿArab & Sībawayh",
        "description": "Fault tolerance, circuit breaking, automatic reconnection, and self-healing systems"
    }
}

KEYWORD_TO_DIMENSIONS = {
    # Concurrency / Async / Threads
    "async": ["concurrency", "governance"],
    "await": ["concurrency", "governance"],
    "thread": ["concurrency"],
    "mutex": ["concurrency", "error_handling"],
    "lock": ["concurrency", "error_handling"],
    "channel": ["concurrency", "governance"],
    "queue": ["concurrency", "backpressure_queue"],
    "worker": ["concurrency", "governance"],
    "pool": ["concurrency", "governance"],
    "stream": ["concurrency", "media_audio"],
    "parallel": ["concurrency"],
    
    # Types / Contracts
    "type": ["types", "governance"],
    "class": ["types", "teleology"],
    "interface": ["types", "abstraction"],
    "struct": ["types", "teleology"],
    "enum": ["types", "decomposition"],
    "generic": ["types", "abstraction"],
    "contract": ["types", "teleology"],
    "invariant": ["types", "immutability"],
    "schema": ["types", "teleology"],
    
    # Immutability / State
    "immutable": ["immutability"],
    "const": ["immutability"],
    "pure": ["immutability", "teleology"],
    "state": ["immutability", "signaling_state"],
    "cache": ["immutability", "concurrency"],
    "store": ["immutability", "teleology"],
    
    # Errors / Safety / Resilience
    "error": ["error_handling", "resilience"],
    "exception": ["error_handling"],
    "retry": ["error_handling", "resilience"],
    "fallback": ["error_handling", "resilience"],
    "timeout": ["error_handling", "resilience"],
    "circuit": ["error_handling", "resilience"],
    "catch": ["error_handling"],
    "panic": ["error_handling"],
    "reconnect": ["resilience", "networking_p2p"],
    
    # Networking / P2P / WebRTC
    "p2p": ["networking_p2p", "signaling_state"],
    "webrtc": ["networking_p2p", "media_audio"],
    "peer": ["networking_p2p", "governance"],
    "socket": ["networking_p2p", "governance"],
    "mesh": ["networking_p2p", "decomposition"],
    "ice": ["networking_p2p", "signaling_state"],
    "sdp": ["signaling_state", "networking_p2p"],
    "handshake": ["signaling_state", "networking_p2p"],
    "signaling": ["signaling_state", "governance"],
    "tunnel": ["networking_p2p", "resilience"],
    "connection": ["networking_p2p", "signaling_state"],
    
    # Audio / Video / Media
    "audio": ["media_audio", "networking_p2p"],
    "video": ["media_audio", "networking_p2p"],
    "pcm": ["media_audio", "decomposition"],
    "track": ["media_audio", "governance"],
    "codec": ["media_audio", "decomposition"],
    "sound": ["media_audio"],
    "microphone": ["media_audio", "error_handling"],
    "echo": ["media_audio", "resilience"],
    
    # Cryptography / Security
    "crypto": ["cryptography"],
    "encrypt": ["cryptography"],
    "decrypt": ["cryptography"],
    "key": ["cryptography", "types"],
    "e2ee": ["cryptography", "networking_p2p"],
    "signature": ["cryptography", "teleology"],
    "ratchet": ["cryptography", "signaling_state"],
    
    # Backpressure / Buffers
    "buffer": ["backpressure_queue", "immutability"],
    "backpressure": ["backpressure_queue", "error_handling"],
    "drain": ["backpressure_queue", "concurrency"],
    "flush": ["backpressure_queue", "concurrency"],
    "overflow": ["backpressure_queue", "error_handling"],

    # Abstraction / Architecture
    "architecture": ["abstraction", "governance", "decomposition"],
    "pattern": ["abstraction", "decomposition"],
    "service": ["teleology", "governance"],
    "repository": ["abstraction", "teleology"],
    "controller": ["governance", "teleology"],
    "middleware": ["governance", "abstraction"],
    "factory": ["abstraction", "decomposition"],
    "refactor": ["abstraction", "decomposition", "governance"]
}


class AynCodeLexiconMapper:
    """
    Connects programming requests and source code to the 5 Classical Arabic Lexicons:
    1. Al-Mufradāt (al-Rāghib) -> Ontological Domain Teleology
    2. Asās al-Balāghah (al-Zamakhsharī) -> Ḥaqīqah vs Majāz Abstraction Integrity
    3. Lisān al-ʿArab (Ibn Manẓūr) -> Exhaustive State-Space & Error Taxonomy
    4. Kitāb al-ʿAyn (al-Farāhīdī) -> Atomic Primitives & Phonetic/Structural Permutations
    5. Al-Kitāb (Sībawayh) -> Syntactic Governance & Caller-Callee Hierarchy
    """

    def __init__(self, **lexicon_mappings: Any):
        self.lisan_dict = lexicon_mappings.get("lisan_dict") or {}
        self.ayn_dict = lexicon_mappings.get("ayn_dict") or {}
        self.raghib_dict = lexicon_mappings.get("raghib_dict") or {}
        self.zamakhshari_dict = lexicon_mappings.get("zamakhshari_dict") or {}
        self.sibawayh_rules = lexicon_mappings.get("sibawayh_rules") or {}

    def extract_relevant_dimensions(self, text: str) -> List[str]:
        """Analyzes text/prompt/code and determines active software engineering dimensions."""
        tokens = re.findall(r'[a-zA-Z_]+', text.lower())
        dimension_counts: Dict[str, int] = {}

        for token in tokens:
            target_dims = KEYWORD_TO_DIMENSIONS.get(token, [])
            for dim in target_dims:
                dimension_counts[dim] = dimension_counts.get(dim, 0) + 1
                    
        # Always ensure core structural dimensions are active
        default_dims = ["teleology", "abstraction", "governance"]
        for d in default_dims:
            dimension_counts[d] = dimension_counts.get(d, 0) + 1
            
        sorted_dims = sorted(dimension_counts.items(), key=lambda x: x[1], reverse=True)
        return [d[0] for d in sorted_dims[:5]]

    def extract_relevant_roots(self, text: str) -> List[str]:
        """Extracts candidate classical roots corresponding to the programming context."""
        dims = self.extract_relevant_dimensions(text)
        roots = []
        for d in dims:
            if d in CONCEPT_ROOT_TAXONOMY:
                roots.extend(CONCEPT_ROOT_TAXONOMY[d]["roots"])
        # Deduplicate while preserving priority order
        seen = set()
        unique_roots = []
        for r in roots:
            if r not in seen:
                seen.add(r)
                unique_roots.append(r)
        return unique_roots[:10]

    def _find_ayn_entry(self, root: str) -> Optional[str]:
        """Looks up a root in Kitāb al-ʿAyn by exact or letter-spaced form."""
        if not self.ayn_dict:
            return None
        # 1. Exact match
        if root in self.ayn_dict:
            return str(self.ayn_dict[root])
        # 2. Letter-spaced match ('ج م ع' or 'ج م')
        spaced = " ".join(list(root))
        if spaced in self.ayn_dict:
            return str(self.ayn_dict[spaced])
        # 3. Two-letter root base match
        if len(root) >= 2:
            bi_spaced = f"{root[0]} {root[1]}"
            if bi_spaced in self.ayn_dict:
                return str(self.ayn_dict[bi_spaced])
        return None

    def _find_sibawayh_rule(self, dims: List[str]) -> Optional[str]:
        """Finds the most thematically relevant Sībawayh grammatical rule for the active dimensions."""
        if not self.sibawayh_rules:
            return None
        
        keywords_map = {
            "governance": ["عمل", "عامل", "معمول", "يرتفع"],
            "types": ["اسم", "صفة", "نعت", "معرفة"],
            "concurrency": ["بين", "جزأين", "حال", "تقديم"],
            "signaling_state": ["إخبار", "ابتداء", "ظرف", "خبر"],
            "error_handling": ["حذف", "قبح", "فصل", "منع"],
            "resilience": ["لا", "توكيد", "بدل"]
        }
        
        target_words = []
        for d in dims:
            if d in keywords_map:
                target_words.extend(keywords_map[d])
                
        best_rule = None
        best_score = -1
        
        for title, content in self.sibawayh_rules.items():
            combined = f"{title} {content}"
            score = sum(1 for w in target_words if w in combined)
            if score > best_score:
                best_score = score
                best_rule = f"{title} — {content}"
                
        return best_rule or list(self.sibawayh_rules.values())[0]

    def _clean_exemplar(self, text: str, max_len: int = 240) -> str:
        """Trims text cleanly at sentence/clause boundary rather than cutting mid-word."""
        if not text:
            return ""
        clean = " ".join(text.replace('\n', ' ').split())
        if len(clean) <= max_len:
            return clean
        
        # Find nearest natural boundary before max_len
        cut = clean[:max_len]
        delimiters = ['.', '!', '؟', '|', '،', ':', ';', '—', ' ']
        best_pos = -1
        for d in delimiters:
            pos = cut.rfind(d)
            if pos > best_pos and pos >= int(max_len * 0.6):
                best_pos = pos
                
        if best_pos > 0:
            return clean[:best_pos].strip()
        return cut.strip() + "..."

    def build_epistemic_coding_context(self, prompt: str, language: str = "python") -> str:
        """
        Builds the 5-Pillar Classical RAG context to ground code synthesis or review.
        Dynamic, high-fidelity, and strictly grounded across all 5 classical authorities.
        """
        dims = self.extract_relevant_dimensions(prompt)
        roots = self.extract_relevant_roots(prompt)

        header_lines = [
            "🏛️ AYNENGINE AI (v2.0): 5-PILLAR CLASSICAL EPISTEMIC CODING APPARATUS",
            f"Target Architecture / Language: {language.upper()}",
            f"Active Conceptual Dimensions: {', '.join(dims).title()}",
            ""
        ]

        section_lines = []
        section_lines.extend(header_lines)
        section_lines.extend(self._render_raghib_section(roots))
        section_lines.extend(self._render_zamakhshari_section(roots))
        section_lines.extend(self._render_lisan_section(roots))
        section_lines.extend(self._render_farahidi_section(roots))
        section_lines.extend(self._render_sibawayh_section(dims))

        return "\n".join(section_lines)

    def _render_raghib_section(self, roots: List[str]) -> List[str]:
        """Renders Pillar 1: Al-Mufradāt teleology anchor."""
        output_rows = [
            "1️⃣ AL-MUFRADĀT (Al-Rāghib al-Iṣfahānī) — Teleology & Ontological Domain Modeling:",
            "   • Invariant: Every type, entity, and function must have an unambiguous Ghāyah (teleology).",
            "   • Rule: Eliminate amorphous, bloated types (no generic 'amorphous_entity', 'processor', or 'manager')."
        ]
        found_count = 0
        for root_item in roots[:4]:
            raghib_record = self.raghib_dict.get(root_item)
            if not raghib_record:
                continue
            clean_def = self._clean_exemplar(raghib_record.get("definition", ""), 220)
            if clean_def:
                output_rows.append(f"   • Root [{root_item}]: \"{clean_def}\"")
                found_count += 1
            if found_count >= 2:
                break
        if found_count == 0:
            output_rows.append("   • Classical Anchor: Maintain strict ontological distinction between essential domain identity and accidental runtime state.")
        return output_rows

    def _render_zamakhshari_section(self, roots: List[str]) -> List[str]:
        """Renders Pillar 2: Asās al-Balāghah eloquence anchor."""
        output_rows = [
            "\n2️⃣ ASĀS AL-BALĀGHAH (Al-Zamakhsharī) — Rhetorical Eloquence & Abstraction Integrity (Ḥaqīqah vs Majāz):",
            "   • Invariant: Delineate literal runtime reality (CPU, IO, sockets, allocations) from software metaphors (ORMs, wrappers, promises).",
            "   • Rule: Zero leaky abstractions (Majāz Mukhil). Eliminate stuttering boilerplate; write idiomatic, high-impact code."
        ]
        found_count = 0
        for root_item in roots[2:7]:
            zamakhshari_record = self.zamakhshari_dict.get(root_item)
            if not zamakhshari_record:
                continue
            lit_usage = self._clean_exemplar(zamakhshari_record.get("literal_usage", ""), 140)
            maj_usage = self._clean_exemplar(zamakhshari_record.get("metaphorical_usage", ""), 140)
            if lit_usage or maj_usage:
                output_rows.append(f"   • Root [{root_item}]: [Ḥaqīqah: {lit_usage}] [Majāz: {maj_usage}]")
                found_count += 1
            if found_count >= 2:
                break
        if found_count == 0:
            output_rows.append("   • Classical Anchor: Maximum communicative power with minimal syntactic ceremony; zero abstraction leakage.")
        return output_rows

    def _render_lisan_section(self, roots: List[str]) -> List[str]:
        """Renders Pillar 3: Lisān al-ʿArab coverage anchor."""
        output_rows = [
            "\n3️⃣ LISĀN AL-ʿARAB (Ibn Manẓūr) — Exhaustive State-Space, Edge-Cases & Error Taxonomy:",
            "   • Invariant: Exhaustive morphological coverage. Zero unhandled match cases, unhandled rejections, or silent failures.",
            "   • Rule: Model every state of the lifecycle: Initializing -> Active -> Degraded -> Closed -> Failed."
        ]
        found_count = 0
        for root_item in roots[:5]:
            lisan_record = self.lisan_dict.get(root_item)
            if not lisan_record:
                continue
            clean_def = self._clean_exemplar(str(lisan_record), 220)
            if clean_def:
                output_rows.append(f"   • Root [{root_item}]: \"{clean_def}\"")
                found_count += 1
            if found_count >= 2:
                break
        return output_rows

    def _render_farahidi_section(self, roots: List[str]) -> List[str]:
        """Renders Pillar 4: Kitāb al-ʿAyn primitive decomposition anchor."""
        output_rows = [
            "\n4️⃣ KITĀB AL-ʿAYN (Al-Farāhīdī) — Atomic Primitive Decomposition & State Permutations:",
            "   • Invariant: Decompose complex logic into orthogonal, irreducible mathematical primitives.",
            "   • Rule: Combinatorial state safety — Make illegal states unrepresentable in the type system.",
            "   • Ensure foundational primitives are pure, stateless, and idempotent."
        ]
        found_count = 0
        for root_item in roots:
            ayn_entry = self._find_ayn_entry(root_item)
            if not ayn_entry:
                continue
            ayn_clean = self._clean_exemplar(ayn_entry, 200)
            output_rows.append(f"   • Root Primitive [{root_item}]: \"{ayn_clean}\"")
            found_count += 1
            if found_count >= 1:
                break
        return output_rows

    def _render_sibawayh_section(self, active_dims: List[str]) -> List[str]:
        """Renders Pillar 5: Al-Kitāb of Sībawayh syntactic governance anchor."""
        output_rows = [
            "\n5️⃣ AL-KITĀB (Sībawayh) — Syntactic Governance (ʿĀmil/Maʿmūl) & AST Integrity:",
            "   • Invariant: Strict caller-callee hierarchy. The Governor (ʿĀmil) explicitly controls the Governed (Maʿmūl).",
            "   • Rule: Zero circular dependencies. Strict static typing, pure information flow, and unambiguous function signatures."
        ]
        rule_match = self._find_sibawayh_rule(active_dims)
        if rule_match:
            rule_clean = self._clean_exemplar(rule_match, 220)
            output_rows.append(f"   • Syntactic Canon: \"{rule_clean}\"")
        return output_rows

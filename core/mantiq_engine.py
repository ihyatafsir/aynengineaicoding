#!/usr/bin/env python3
"""
mantiq_engine.py

AynEngine AI Coding Edition: Classical Arabic Logic (Manṭiq) & Morphology (Ishtiqāq) Engine.

Grounding Authorities:
- Abū Ḥāmid al-Ghazālī: Miʿyār al-ʿIlm fī Fann al-Manṭiq & Miḥakk al-Naẓar
- Fakhr al-Dīn al-Rāzī: Al-Mulakhkhaṣ fī al-Ḥikmah wa-al-Manṭiq
- Al-Khalīl ibn Aḥmad al-Farāhīdī: Kitāb al-ʿAyn (Root Permutations & Primitive Decomposition)
- Ibn Manẓūr: Lisān al-ʿArab (Exhaustive Morphological State Coverage)
- Al-Rāghib al-Iṣfahānī: Al-Mufradāt (Ontological Teleology & Distinction of Essence vs Accident)
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import json
import re


class MantiqCategory(str, Enum):
    """Classical Aristotelian-Ghazalian Epistemic Classifications."""
    TASAWWUR = "tasawwur"       # Conceptualization / Primitive Definition (Indivisible Essence)
    TASDIQ = "tasdiq"           # Judgment / Proposition / Assertive Relation
    DHATI = "dhati"             # Inherent / Essential / Immutable Property
    ARADI = "aradi"             # Accidental / Transient / Mutable State


class FallacyType(str, Enum):
    """Classical Logical Fallacies in Software Architecture."""
    DAWR = "dawr"               # Circular Dependency / Mutual Deadlock (A requires B, B requires A)
    TASALSUL = "tasalsul"       # Infinite Regress / Unbounded Recursion / Memory Leak without Base Case
    MAJAZ_MUKHIL = "majaz_mukhil" # Leaky Abstraction (Metaphor corrupting runtime machine reality)
    TANAQUD = "tanaqud"         # Contradiction / Representable Illegal States in Type System


@dataclass(frozen=True)
class MorphologicalRoot:
    """Tri-consonantal classical root representing irreducible atomic primitive."""
    root_letters: str           # e.g., 'ح-ف-ظ'
    lemma_title: str            # e.g., 'حفظ'
    semantic_core: str          # e.g., 'Preservation, immutability, guarding against corruption'
    software_analog: str        # e.g., 'Immutable buffer, checksum guard, persistent memory'
    governing_lexicon: str      # e.g., 'Kitāb al-ʿAyn / Lisān al-ʿArab'


@dataclass
class EpistemicCritique:
    """Logical assessment under Ghazalian Manṭiq rules."""
    category: MantiqCategory
    axiom_citation: str
    is_valid: bool
    detected_fallacies: List[FallacyType] = field(default_factory=list)
    remediation: str = ""


class AynMantiqEngine:
    """
    Epistemic Logic & Morphology Evaluator.
    Disproves software architecture fallacies (Dawr, Tasalsul, Majāz Mukhil)
    and grounds code entities in tri-consonantal classical roots.
    """

    # Classical Software Tri-Consonantal Root Ontology
    ROOT_ONTOLOGY: Dict[str, MorphologicalRoot] = {
        "حفظ": MorphologicalRoot(
            root_letters="ح-ف-ظ",
            lemma_title="حفظ",
            semantic_core="الصيانة والملازمة ودفع الفساد والنسيان",
            software_analog="Immutability, persistent storage, memory retention, checksum integrity",
            governing_lexicon="Kitāb al-ʿAyn & Lisān al-ʿArab"
        ),
        "قفل": MorphologicalRoot(
            root_letters="ق-ف-ل",
            lemma_title="قفل",
            semantic_core="الإمساك والتضييق والامتناع عن الدخول إلا بإذن",
            software_analog="Mutual exclusion, mutex lock, semaphore barrier, atomic CAS barrier",
            governing_lexicon="Asās al-Balāghah"
        ),
        "نقل": MorphologicalRoot(
            root_letters="ن-ق-ل",
            lemma_title="نقل",
            semantic_core="تحويل الشيء من موضع إلى موضع بتمامه",
            software_analog="Data transport, packet serialization, zero-copy socket streaming",
            governing_lexicon="Lisān al-ʿArab"
        ),
        "عقد": MorphologicalRoot(
            root_letters="ع-ق-د",
            lemma_title="عقد",
            semantic_core="الربط والإحكام بين طرفين بحيث لا ينفك أحدهما إلا بفسخ",
            software_analog="API contract, interface binding, cryptographic transaction consensus",
            governing_lexicon="Al-Mufradāt"
        ),
        "حسب": MorphologicalRoot(
            root_letters="ح-س-ب",
            lemma_title="حسب",
            semantic_core="العدّ والتقدير وتحديد المقدار المنضبط بلا زيادة ولا نقصان",
            software_analog="Computational budget, rate-limiting tokens, algorithmic complexity bound",
            governing_lexicon="Al-Mufradāt"
        ),
        "رتب": MorphologicalRoot(
            root_letters="ر-ت-ب",
            lemma_title="رتب",
            semantic_core="الاستقرار في المنزلة والتقديم والتأخير المنضبط",
            software_analog="Strict total ordering, monotonic priority queue, sequential execution",
            governing_lexicon="Asās al-Balāghah"
        ),
        "ميز": MorphologicalRoot(
            root_letters="م-ي-ز",
            lemma_title="ميز",
            semantic_core="فصل الشيء عن غيره بخصيصة ذاتية تمنع الاشتباه",
            software_analog="Sum types, tagged unions, exhaustive pattern matching, type discrimination",
            governing_lexicon="Kitāb al-ʿAyn"
        ),
        "سلم": MorphologicalRoot(
            root_letters="س-ل-م",
            lemma_title="سلم",
            semantic_core="الخلو من الآفات والعيوب والأمن من التلف",
            software_analog="Fault tolerance, graceful degradation, absence of undefined behavior",
            governing_lexicon="Lisān al-ʿArab"
        ),
        "عمل": MorphologicalRoot(
            root_letters="ع-م-ل",
            lemma_title="عمل",
            semantic_core="إحداث الأثر في الغير بمقتضى السلطة والاقتضاء",
            software_analog="Syntactic governance (ʿĀmil/Maʿmūl), executor pipeline, runtime evaluation",
            governing_lexicon="Al-Kitāb of Sībawayh"
        ),
        "حكم": MorphologicalRoot(
            root_letters="ح-ك-م",
            lemma_title="حكم",
            semantic_core="الفصل القاطع والمنع من الفساد والإتقان",
            software_analog="Validation predicate, invariant assertion, policy enforcement",
            governing_lexicon="Al-Mufradāt"
        )
    }

    def __init__(self, data_root: Optional[Path] = None):
        self.data_root = data_root or Path("/home/absolut7/.gemini/antigravity/scratch/translation_engine_framework/data")
        self.miyar_path = self.data_root / "texts/ghazali/miyar_al_ilm.txt"
        self.mihakk_path = self.data_root / "texts/ghazali/mihakk_al_nazar.txt"
        self.mufradat_path = self.data_root / "texts/raghib/al_mufradat_fi_gharib_al_quran.txt"
        self.lisan_path = self.data_root / "lisanclean.json"

    def resolve_roots_for_concept(self, query_text: str) -> List[MorphologicalRoot]:
        """Maps an engineering prompt or architectural concept to relevant classical roots."""
        q_lower = query_text.lower()
        matched_roots: List[MorphologicalRoot] = []

        mappings = {
            ("lock", "mutex", "concurrency", "thread", "atomic", "sync"): "قفل",
            ("immutable", "pure", "cache", "buffer", "persist", "save"): "حفظ",
            ("transport", "network", "socket", "stream", "packet", "p2p"): "نقل",
            ("contract", "interface", "protocol", "binding", "transaction"): "عقد",
            ("limit", "token", "budget", "meter", "rate", "throttle"): "حسب",
            ("order", "priority", "queue", "sort", "sequence"): "رتب",
            ("type", "discriminate", "variant", "match", "enum"): "ميز",
            ("error", "fault", "safe", "recover", "resilient"): "سلم",
            ("eval", "execute", "governor", "call", "dispatch"): "عمل",
            ("validate", "guard", "assert", "invariant", "rule"): "حكم"
        }

        for keywords, root_key in mappings.items():
            if any(k in q_lower for k in keywords):
                if root_key in self.ROOT_ONTOLOGY:
                    matched_roots.append(self.ROOT_ONTOLOGY[root_key])

        # Default to essential roots if no specific domain matched
        if not matched_roots:
            matched_roots.append(self.ROOT_ONTOLOGY["حفظ"])
            matched_roots.append(self.ROOT_ONTOLOGY["عقد"])

        return matched_roots

    def audit_logic_fallacies(self, code: str) -> EpistemicCritique:
        """
        Audits code for Classical Arabic Logic fallacies:
        - Dawr (Cycles / mutual deadlocks)
        - Tasalsul (Unbounded loops / infinite recursions)
        - Majāz Mukhil (Leaky abstractions / raw exceptions exposed)
        - Tanāquḍ (Illegal state contradictions)
        """
        fallacies: List[FallacyType] = []
        remediations: List[str] = []

        # 1. Check for Dawr (Circular references or bidirectional mutual locks)
        if re.search(r"self\.\w+\s*=\s*\w+.*self", code, re.DOTALL):
            fallacies.append(FallacyType.DAWR)
            remediations.append("Eliminate circular self-binding (Dawr). Enforce unidirectional hierarchy.")

        # 2. Check for Tasalsul (Unbounded recursive call without base condition check)
        func_defs = re.findall(r"def\s+(\w+)\s*\((.*?)\):", code)
        for func_name, _ in func_defs:
            body_match = re.search(rf"def\s+{func_name}\b.*?(?=\ndef|\Z)", code, re.DOTALL)
            if body_match:
                body = body_match.group(0)
                # If recursive call exists without a return/if guard
                if re.search(rf"\b{func_name}\s*\(", body[len(func_name)+10:]) and "if " not in body:
                    fallacies.append(FallacyType.TASALSUL)
                    remediations.append(f"Recursive routine '{func_name}' lacks explicit base termination guard (Tasalsul).")

        # 3. Check for Majāz Mukhil (Leaky Abstraction: bare Exception catching or generic 'data'/'manager')
        if re.search(r"except\s*:", code) or re.search(r"except\s+Exception\s*:", code):
            fallacies.append(FallacyType.MAJAZ_MUKHIL)
            remediations.append("Bare/generic exception handler violates abstraction integrity (Majāz Mukhil). Use explicit domain error taxonomy.")

        if re.search(r"\bclass\s+\w*(Manager|Helper|Data|Processor)\b", code):
            fallacies.append(FallacyType.MAJAZ_MUKHIL)
            remediations.append("Amorphous class nomenclature ('Manager'/'Helper'/'Data') corrupts ontological essence. Use precise teleological naming.")

        # 4. Check for Tanāquḍ (Contradictory state representation, e.g. Optional attributes with conflicting booleans)
        if "is_valid: bool" in code and "error_message: Optional[str]" in code:
            remediations.append("Separate success and failure variants into distinct algebraic types (Al-Mīz) to make invalid combinations unrepresentable.")

        is_valid = len(fallacies) == 0
        citation = "Al-Ghazālī: Miʿyār al-ʿIlm (Bāb Madāriq al-Qiyās wa Mabāḥith al-Dalālāt)"

        return EpistemicCritique(
            category=MantiqCategory.TASDIQ,
            axiom_citation=citation,
            is_valid=is_valid,
            detected_fallacies=fallacies,
            remediation="; ".join(remediations) if remediations else "Code satisfies classical non-contradiction and acyclic invariants."
        )

    def generate_mantiq_scratchpad(self, prompt: str, target_language: str = "python") -> str:
        """
        Generates the formal <ayn_mantiq> Chain-of-Thought reasoning block
        derived from Ghazalian Manṭiq and Farahidian Ishtiqāq.
        """
        roots = self.resolve_roots_for_concept(prompt)
        primary_root = roots[0]
        secondary_root = roots[1] if len(roots) > 1 else self.ROOT_ONTOLOGY["عقد"]

        scratchpad = f"""<ayn_mantiq>
 AYN-ENGINE EPISTEMIC CHAIN-OF-THOUGHT (MANṬIQ & ISHTIQĀQ)
Target Architecture: {target_language.upper()}
Problem Specification: "{prompt}"

1. ISHTIQĀQ & MORPHOLOGICAL ROOTS (Kitāb al-ʿAyn & Lisān al-ʿArab):
   • Primary Root: [{primary_root.root_letters}] ({primary_root.lemma_title})
     - Classical Significance: {primary_root.semantic_core}
     - Software Analog: {primary_root.software_analog}
   • Secondary Root: [{secondary_root.root_letters}] ({secondary_root.lemma_title})
     - Classical Significance: {secondary_root.semantic_core}
     - Software Analog: {secondary_root.software_analog}

2. TAṢAWWUR: ONTOLOGICAL ESSENCE VS ACCIDENT (Al-Mufradāt: al-Rāghib):
   • Dhāt (Immutable Essence):
     - Permanent domain entities, algebraic sum-types, immutable records, monotonic IDs.
   • 'Araḍ (Transient Accident):
     - I/O buffers, network latency, retry counts, eviction cursors.

3. MANṬIQ: FALLACY ELIMINATION & PROOF THEORY (Miʿyār al-ʿIlm: al-Ghazālī):
   • Dafʿ al-Dawr (Zero Circularity):
     - Strict dependency hierarchy: Governor layer -> Runtime evaluator -> Immutable record.
     - Never allow cyclic callbacks or bidirectional mutations.
   • Dafʿ al-Tasalsul (Zero Unbounded Regress):
     - Explicit bounded capacity, deterministic timeout bounds, guaranteed loop termination.
   • 'Adam al-Tanāquḍ (Non-Contradiction):
     - Illegal states made unrepresentable in the type system.
     - Exhaustive state discrimination; zero unhandled match arms.

4. SYNTACTIC GOVERNANCE & CONTRACTS (Al-Kitāb of Sībawayh):
   • 'Āmil (The Governor): Controller / Engine entrypoint holding immutable execution context.
   • Ma'mūl (The Governed): Pure domain data types subjected to non-destructive transformation.
   • Strict Static Typing: Complete type annotations, zero 'Any' escape hatches, strict return contracts.
</ayn_mantiq>"""
        return scratchpad

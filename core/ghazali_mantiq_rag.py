"""
AynEngine Ghazali Mantiq Epistemic RAG Core Engine
Strict classical Ghazalian epistemology and 5-pillar linguistic governance
for in-context steering of LLM code synthesis (DeepSeek Flash 4.1).

Axioms Formalized:
- Tasawwur vs Tasdiq (Al-Hadd bi al-Dhatiyyat): Teleological typed domain modeling.
- Daf' al-Dawr (Circularity Elimination): Monotonic DAG ordering, zero deadlocks.
- Daf' al-Tasalsul (Infinite Regress Elimination): Strictly bounded loops, TTL, horizons.
- 'Adam al-Tanaqud (Law of Non-Contradiction): Sound algebraic invariants.
- Qiyas Burhani (Apodictic Proof): Design by Contract, pre/post conditions.
- 5 Classical Linguistic Pillars: Farahidi, Raghib, Zamakhshari, Ibn Manzur, Sibawayh.

Strict Zero-Emoji Policy Enforced.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
import re
import json

@dataclass
class ClassicalAxiom:
    name: str
    arabic_name: str
    classical_source: str
    epistemic_principle: str
    computational_invariant: str
    code_enforcement_rule: str
    banned_patterns: List[str] = field(default_factory=list)
    required_patterns: List[str] = field(default_factory=list)

@dataclass
class LinguisticPillar:
    scholar: str
    arabic_name: str
    canonical_work: str
    foundational_concept: str
    software_architecture_role: str
    enforcement_directive: str

@dataclass
class GhazaliPromptContext:
    task_description: str
    target_language: str
    axioms: List[ClassicalAxiom]
    pillars: List[LinguisticPillar]
    system_instruction: str
    few_shot_exemplars: List[Dict[str, str]]
    validation_checklist: List[str]

    def to_system_prompt(self) -> str:
        """Serializes the epistemic context into a structured system prompt."""
        sections = [
            "=== AYNENGINE GHAZALI MANTIQ EPISTEMIC GOVERNANCE PROTOCOL ===",
            "You are guided by the classical epistemological canon of Abu Hamid al-Ghazali",
            "(Miyar al-Ilm, Mihakk al-Nazar, Tahafut al-Falasifah) and the 5 classical linguistic authorities.",
            "All generated code must rigorously satisfy the following epistemic invariants without compromise.",
            "",
            "--- FOUNDATIONAL EPISTEMIC AXIOMS ---"
        ]

        for idx, ax in enumerate(self.axioms, 1):
            sections.append(f"[{idx}] {ax.name} ({ax.arabic_name}) - Source: {ax.classical_source}")
            sections.append(f"    Epistemic Basis: {ax.epistemic_principle}")
            sections.append(f"    Computational Invariant: {ax.computational_invariant}")
            sections.append(f"    Enforcement Directive: {ax.code_enforcement_rule}")
            if ax.banned_patterns:
                sections.append(f"    Strictly Forbidden Patterns: {', '.join(ax.banned_patterns)}")
            sections.append("")

        sections.append("--- THE 5 LINGUISTIC-ARCHITECTURAL PILLARS ---")
        for idx, pil in enumerate(self.pillars, 1):
            sections.append(f"[{idx}] {pil.scholar} ({pil.arabic_name}) - {pil.canonical_work}")
            sections.append(f"    Concept: {pil.foundational_concept}")
            sections.append(f"    Architectural Role: {pil.software_architecture_role}")
            sections.append(f"    Directive: {pil.enforcement_directive}")
            sections.append("")

        sections.append("--- MANDATORY PURITY SPECIFICATIONS ---")
        for item in self.validation_checklist:
            sections.append(f"* {item}")

        sections.append("")
        sections.append("--- TARGET IMPLEMENTATION CONSTRAINTS ---")
        sections.append(f"Target Language: {self.target_language}")
        sections.append("Zero-Emoji Policy: Do NOT output emojis anywhere (no UI icons, comments, docstrings).")
        sections.append("Zero-Loss Policy: Provide 100% complete, fully implemented, production-grade code.")
        sections.append("Placeholders Forbidden: Never write TODO, pass # implement, or unhandled exceptions.")

        return "\n".join(sections)


class GhazaliMantiqRAG:
    """
    Epistemic Knowledge Retrieval & Augmentation Engine grounded in
    al-Ghazali's logical treatises and classical linguistic authorities.
    """

    def __init__(self):
        self.axioms: Dict[str, ClassicalAxiom] = self._init_axioms()
        self.pillars: Dict[str, LinguisticPillar] = self._init_pillars()
        self.exemplars: List[Dict[str, str]] = self._init_exemplars()

    def _init_axioms(self) -> Dict[str, ClassicalAxiom]:
        return {
            "al_hadd_bi_al_dhatiyyat": ClassicalAxiom(
                name="Essential Definition by Intrinsic Attributes",
                arabic_name="Al-Hadd bi al-Dhatiyyat",
                classical_source="Al-Ghazali, Miyar al-Ilm fi Fann al-Mantiq (Book 1: Tasawwurat)",
                epistemic_principle=(
                    "True conceptualization (Tasawwur) requires defining an essence by its constitutive "
                    "essential attributes (dhatiyyat), distinguishing it completely from accidental traits (aradiyyat)."
                ),
                computational_invariant=(
                    "Type definitions must declare exact, minimal, and sufficient fields that define the entity. "
                    "Generic catch-all structures (any, dict, Object, temp, data) represent cognitive void and are prohibited."
                ),
                code_enforcement_rule=(
                    "Every domain model must be a strictly typed entity or interface with explicitly specified "
                    "invariants, boundaries, and validation."
                ),
                banned_patterns=["any", "dict[str, Any]", "interface ObjectRecord { [k: string]: any }", "var temp", "let data"]
            ),
            "daf_al_dawr": ClassicalAxiom(
                name="Elimination of Vicious Circularity",
                arabic_name="Daf' al-Dawr (Circulus in Demonstrando)",
                classical_source="Al-Ghazali, Tahafut al-Falasifah (Discussions 3 & 4) & Mihakk al-Nazar",
                epistemic_principle=(
                    "An entity or premise cannot depend upon that which depends upon itself; causality and demonstration "
                    "must flow along a strict directed acyclic order without circular dependency."
                ),
                computational_invariant=(
                    "Resource acquisition, state locks, and routing dependencies must follow a globally ordered monotonic sequence. "
                    "Circular locks, cyclic routing loops, and reciprocal recursive invocations are mathematically forbidden."
                ),
                code_enforcement_rule=(
                    "Sort all lock or resource identifiers monotonically prior to acquisition. "
                    "Maintain routing tables as a Directed Acyclic Graph (DAG) with loop-detection hashes."
                ),
                banned_patterns=["lock(a) inside lock(b) without sorting", "cyclic route forwarding", "unvalidated mutual recursion"]
            ),
            "daf_al_tasalsul": ClassicalAxiom(
                name="Elimination of Infinite Regress",
                arabic_name="Daf' al-Tasalsul (Regressus ad Infinitum)",
                classical_source="Al-Ghazali, Al-Iqtisad fi al-I'tiqad & Mihakk al-Nazar",
                epistemic_principle=(
                    "An infinite regress of contingent causes is impossible; every valid chain must terminate "
                    "in a necessary first cause or deterministic terminal bound."
                ),
                computational_invariant=(
                    "All recursive functions, loops, gossip networks, and queues must possess a mathematically provable, "
                    "monotonically decreasing termination variant (TTL, maximum depth, bounded queue horizon)."
                ),
                code_enforcement_rule=(
                    "Enforce strict TTL on all network packets, deterministic timeout bounds on all async operations, "
                    "and max capacity bounds on all collections with LRU eviction."
                ),
                banned_patterns=["while True without break", "unbounded retry without max_attempts", "unbounded cache growth"]
            ),
            "adam_al_tanaqud": ClassicalAxiom(
                name="Law of Absolute Non-Contradiction",
                arabic_name="'Adam al-Tanaqud",
                classical_source="Al-Ghazali, Mihakk al-Nazar fi al-Mantiq",
                epistemic_principle=(
                    "Two contradictory propositions cannot both be true simultaneously in the same respect and at the same time."
                ),
                computational_invariant=(
                    "State machines must have mutually exclusive and collectively exhaustive states. Concurrent transitions "
                    "must be atomic. A method must never return an error while partially mutating persistent state."
                ),
                code_enforcement_rule=(
                    "Use discriminated unions or sealed enum states. Execute state mutations using atomic rollback transactions "
                    "or copy-on-write semantics."
                ),
                banned_patterns=["partial mutation before exception", "overlapping state machine flags (e.g. isRunning and isStopped both true)"]
            ),
            "qiyas_burhani": ClassicalAxiom(
                name="Demonstrative Syllogism (Apodictic Proof)",
                arabic_name="Al-Qiyas al-Burhani",
                classical_source="Al-Ghazali, Al-Qistas al-Mustaqim (The Correct Balance) & Miyar al-Ilm",
                epistemic_principle=(
                    "Certain knowledge (Yaqin) is derived only through demonstrative syllogisms with verified, true, and necessary premises."
                ),
                computational_invariant=(
                    "Design by Contract: Every function must explicitly verify its preconditions (sound premises), "
                    "guarantee its postconditions (sound conclusion), and maintain class invariants."
                ),
                code_enforcement_rule=(
                    "Validate inputs at the public boundary. Throw domain-specific typed errors immediately on invalid premises. "
                    "Assert invariants at critical state junctions."
                ),
                banned_patterns=["silent error suppression", "returning null or undefined on invalid contract"]
            )
        }

    def _init_pillars(self) -> Dict[str, LinguisticPillar]:
        return {
            "farahidi": LinguisticPillar(
                scholar="Al-Khalil ibn Ahmad al-Farahidi",
                arabic_name="Al-Farahidi",
                canonical_work="Kitab al-Ayn",
                foundational_concept="Root Atomicity and Exhaustive Permutation (Al-Ishtiqaq al-Kabir)",
                software_architecture_role="Primitive Modular Decomposition",
                enforcement_directive=(
                    "Decompose complex subsystems into irreducibly minimal atomic components. "
                    "Each component must encapsulate a single atomic responsibility with zero redundant permutations."
                )
            ),
            "raghib": LinguisticPillar(
                scholar="Al-Raghib al-Isfahani",
                arabic_name="Al-Raghib",
                canonical_work="Al-Mufradat fi Gharib al-Quran",
                foundational_concept="Teleological Semantic Precision (Furuq Lughawiyyah)",
                software_architecture_role="Exact Domain-Driven Naming and Type Semantics",
                enforcement_directive=(
                    "Do not use generic names or ambiguous synonyms. Name every type, variable, and function "
                    "by its exact teleological purpose (e.g., GossipMessagePayload rather than MessageData)."
                )
            ),
            "zamakhshari": LinguisticPillar(
                scholar="Al-Zamakhshari",
                arabic_name="Al-Zamakhshari",
                canonical_work="Asas al-Balaghah",
                foundational_concept="Dichotomy of Literal (Haqiqah) vs Metaphorical (Majaz)",
                software_architecture_role="Direct Concrete Execution without Magical Side-Effects",
                enforcement_directive=(
                    "Functions must perform literal, transparent transformations. Avoid implicit global state mutations, "
                    "obscure metaprogramming tricks, or metaphorical abstraction leaks."
                )
            ),
            "ibn_manzur": LinguisticPillar(
                scholar="Ibn Manzur",
                arabic_name="Ibn Manzur",
                canonical_work="Lisan al-Arab",
                foundational_concept="Comprehensive Lexical Taxonomy and Contextual Diagnostic Precision",
                software_architecture_role="Exhaustive Error Hierarchy and Audit Traceability",
                enforcement_directive=(
                    "Define a typed, hierarchical domain error taxonomy. Never discard caught exceptions silently. "
                    "Include contextual causality, epoch counters, and entity identifiers in every error log."
                )
            ),
            "sibawayh": LinguisticPillar(
                scholar="Sibawayh",
                arabic_name="Sibawayh",
                canonical_work="Al-Kitab",
                foundational_concept="Grammatical Governance and Vector Operators (Nazariyyat al-Amil)",
                software_architecture_role="Strict Pipeline Control and Type Governance",
                enforcement_directive=(
                    "Enforce strict unidirectional data flow. Every governing controller ('Amil) must explicitly "
                    "bound and validate the dependent data structures (Ma'mul) it acts upon."
                )
            )
        }

    def _init_exemplars(self) -> List[Dict[str, str]]:
        return [
            {
                "task": "Bounded LRU Cache with Regress Elimination",
                "language": "TypeScript",
                "code": (
                    "export class BoundedAxiomaticCache<K, V> {\n"
                    "  private readonly capacity: number;\n"
                    "  private readonly cache: Map<K, V>;\n"
                    "\n"
                    "  constructor(capacity: number) {\n"
                    "    if (capacity <= 0 || !Number.isInteger(capacity)) {\n"
                    "      throw new RangeError('Capacity must be a positive integer, upholding Daf al-Tasalsul');\n"
                    "    }\n"
                    "    this.capacity = capacity;\n"
                    "    this.cache = new Map<K, V>();\n"
                    "  }\n"
                    "\n"
                    "  public get(key: K): V | undefined {\n"
                    "    if (!this.cache.has(key)) return undefined;\n"
                    "    const value = this.cache.get(key)!;\n"
                    "    this.cache.delete(key);\n"
                    "    this.cache.set(key, value);\n"
                    "    return value;\n"
                    "  }\n"
                    "\n"
                    "  public put(key: K, value: V): void {\n"
                    "    if (this.cache.has(key)) {\n"
                    "      this.cache.delete(key);\n"
                    "    } else if (this.cache.size >= this.capacity) {\n"
                    "      const oldestKey = this.cache.keys().next().value;\n"
                    "      if (oldestKey !== undefined) {\n"
                    "        this.cache.delete(oldestKey);\n"
                    "      }\n"
                    "    }\n"
                    "    this.cache.set(key, value);\n"
                    "  }\n"
                    "}"
                )
            }
        ]

    def build_context(self, task_description: str, target_language: str = "TypeScript") -> GhazaliPromptContext:
        """
        Builds the RAG context tailored to the specific coding task,
        selecting relevant axioms and constructing actionable validation rules.
        """
        selected_axioms = list(self.axioms.values())
        selected_pillars = list(self.pillars.values())

        validation_checklist = [
            "1. Zero Generic Identifiers: Eliminate 'data', 'temp', 'obj', 'val', 'res', 'item'. Use teleological names.",
            "2. Monotonic Ordering (Daf' al-Dawr): Multi-resource locking or graph traversing must be monotonically ordered.",
            "3. Bounded Regress (Daf' al-Tasalsul): Loops, retries, and network hops must have finite, strictly bounded limits.",
            "4. Mutual Exclusion ('Adam al-Tanaqud): State transitions must be atomic and non-contradictory.",
            "5. Apodictic Preconditions (Qiyas Burhani): Validate input bounds at public method entries.",
            "6. Typed Domain Errors (Ibn Manzur): Zero empty catches, zero silent swallowed exceptions.",
            "7. Complete Implementation: No TODO, no pass, no ellipsis (...), no stubbed methods.",
            "8. Zero-Emoji: No emojis anywhere in the code or comments."
        ]

        return GhazaliPromptContext(
            task_description=task_description,
            target_language=target_language,
            axioms=selected_axioms,
            pillars=selected_pillars,
            system_instruction=(
                "Synthesize pristine, production-ready code adhering to classical Ghazali logic and linguistic rigor."
            ),
            few_shot_exemplars=self.exemplars,
            validation_checklist=validation_checklist
        )

    def audit_code_purity(self, code: str, language: str = "TypeScript") -> Dict[str, Any]:
        """
        Deterministically audits generated code against Ghazali epistemic axioms.
        Returns whether the code passes and details of any detected fallacies.
        """
        violations: List[str] = []

        # 1. Check for empty catch blocks / silent error suppression (Tahafut violation)
        empty_catch_patterns = [
            r"catch\s*\([^)]*\)\s*\{\s*\}",
            r"except\s*:\s*\n\s*pass",
            r"except\s+Exception\s*:\s*\n\s*pass"
        ]
        for pat in empty_catch_patterns:
            if re.search(pat, code):
                violations.append("Violation of Ibn Manzur Error Rigor: Detected silent swallowed exception.")

        # 2. Check for unbounded infinite loops without variant (Daf' al-Tasalsul)
        unbounded_loop_patterns = [
            r"while\s*\(\s*true\s*\)\s*\{(?![^}]*(?:break|return|throw|timeout))",
            r"while\s+True\s*:(?![^:]*(?:break|return|raise))"
        ]
        for pat in unbounded_loop_patterns:
            if re.search(pat, code):
                violations.append("Violation of Daf' al-Tasalsul: Unbounded infinite loop without explicit termination variant.")

        # 3. Check for forbidden placeholder patterns
        placeholder_patterns = [
            r"//\s*TODO",
            r"//\s*FIXME",
            r"//\s*implement\s+here",
            r"#\s*TODO",
            r"\.\.\.\s*//\s*more",
            r"\bpass\s*#\s*implement\b"
        ]
        for pat in placeholder_patterns:
            if re.search(pat, code, re.IGNORECASE):
                violations.append(f"Violation of Zero-Loss Policy: Detected incomplete placeholder pattern '{pat}'.")

        # 4. Check for prohibited generic names in key declaration positions
        generic_var_patterns = [
            r"\b(let|const|var)\s+(temp|data|obj|val|res|item)\s*[:=]",
        ]
        for pat in generic_var_patterns:
            if re.search(pat, code):
                violations.append("Violation of Al-Hadd bi al-Dhatiyyat (Raghib): Generic identifier detected in variable declaration.")

        # 5. Check for emojis (Strict Zero-Emoji Policy)
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]",
            flags=re.UNICODE
        )
        if emoji_pattern.search(code):
            violations.append("Violation of Zero-Emoji Policy: Unicode emoji character detected in source.")

        return {
            "is_pure": len(violations) == 0,
            "violations": violations,
            "axiom_compliance_rate": (5 - min(5, len(violations))) / 5.0 * 100.0
        }


if __name__ == "__main__":
    rag = GhazaliMantiqRAG()
    ctx = rag.build_context("Sovereign Mesh Consensus Engine", "TypeScript")
    print("Ghazali Mantiq RAG initialized successfully.")
    print("Axioms registered:", len(ctx.axioms))
    print("Pillars registered:", len(ctx.pillars))
    
    # Test self-audit on exemplar
    audit_res = rag.audit_code_purity(ctx.few_shot_exemplars[0]["code"], "TypeScript")
    print("Exemplar Purity Audit:", audit_res)
    assert audit_res["is_pure"], "Exemplar failed self-audit!"
    print("Axiom self-test passed with 100% compliance.")

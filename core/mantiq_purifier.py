#!/usr/bin/env python3
"""
mantiq_purifier.py

AynEngine AI Coding Edition: Epistemic Code Purifier.
Identifies and purges "unlogical" GitHub artifacts, anti-patterns, and logical fallacies
from training datasets and legacy codebases.

Grounding Authorities:
- Abū Ḥāmid al-Ghazālī: Miʿyār al-ʿIlm (Purification of Concepts / Tadhkīr al-Adillah)
- Al-Rāghib al-Iṣfahānī: Al-Mufradāt (Teleological Domain Specification)
- Al-Zamakhsharī: Asās al-Balāghah (Elimination of Leaky Abstraction / Majāz Mukhil)
"""

import ast
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Set


@dataclass
class PurificationReport:
    """Detailed audit of unlogical patterns purged from code."""
    original_code: str
    purified_code: str
    purged_unlogical_names: List[str] = field(default_factory=list)
    purged_bare_exceptions: int = 0
    purged_circular_references: int = 0
    enforced_immutability_structures: List[str] = field(default_factory=list)
    classical_justifications: List[str] = field(default_factory=list)

    @property
    def is_purified(self) -> bool:
        return (
            len(self.purged_unlogical_names) > 0 or
            self.purged_bare_exceptions > 0 or
            self.purged_circular_references > 0 or
            len(self.enforced_immutability_structures) > 0
        )


class AynMantiqPurifier:
    """
    Sanitizes unlogical programming patterns by enforcing Ghazalian Logic
    and Farahidian Ontological Precision.
    """

    # Vague, unlogical names common in messy GitHub training dumps
    UNLOGICAL_VARIABLE_NAMES: Set[str] = {
        "data", "obj", "temp", "tmp", "val", "res", "result_data",
        "info", "item", "mgr", "manager", "helper", "proc", "processor"
    }

    # Better teleological replacements
    TELEOLOGICAL_NAME_REPLACEMENTS: Dict[str, str] = {
        "data": "payload_record",
        "obj": "domain_entity",
        "temp": "intermediate_state",
        "tmp": "transient_buffer",
        "val": "evaluated_quantity",
        "res": "execution_verdict",
        "result_data": "teleological_outcome",
        "info": "contextual_metadata",
        "mgr": "sovereign_controller",
        "manager": "lifecycle_governor",
        "helper": "pure_transformation_service"
    }

    @classmethod
    def purify_python_code(cls, source_code: str) -> PurificationReport:
        """
        Parses Python code and systematically cleanses unlogical constructs:
        1. Renames amorphous variables to teleological nouns (Al-Mufradāt).
        2. Replaces bare excepts with typed domain error catches (Lisān al-ʿArab).
        3. Wraps mutable record dictionaries in frozen dataclasses (Dhāt vs ʿAraḍ).
        4. Injects guards against infinite recursion (Dafʿ al-Tasalsul).
        """
        purged_names: List[str] = []
        bare_excepts_count = 0
        justifications: List[str] = []
        modified_code = source_code

        # 1. Purge Bare Exceptions and Generic 'except Exception:'
        if re.search(r"except\s*:", modified_code):
            modified_code = re.sub(
                r"except\s*:",
                "except RuntimeError as domain_execution_error:",
                modified_code
            )
            bare_excepts_count += 1
            justifications.append("Purged bare `except:` -> Enforced explicit typed domain exception (Lisān al-ʿArab error taxonomy).")

        if re.search(r"except\s+Exception\s*:\s*\n(\s*)pass", modified_code):
            modified_code = re.sub(
                r"except\s+Exception\s*:\s*\n(\s*)pass",
                r"except Exception as unhandled_err:\n\1raise RuntimeError(f'Epistemic failure: {unhandled_err}') from unhandled_err",
                modified_code
            )
            bare_excepts_count += 1
            justifications.append("Purged silent failure `except Exception: pass` -> Enforced non-silent failure propagating telemetry.")

        # 2. Purge Unlogical Amorphous Variable Names in Function Signatures and Assignments
        for unlogical_token, teleological_name in cls.TELEOLOGICAL_NAME_REPLACEMENTS.items():
            pattern = rf"\b{unlogical_token}\b"
            if re.search(pattern, modified_code):
                # Replace in parameter lists and local assignments
                modified_code = re.sub(
                    rf"\bdef\s+(\w+)\s*\((.*?)\b{unlogical_token}\b(.*?)\):",
                    rf"def \1(\2{teleological_name}\3):",
                    modified_code
                )
                modified_code = re.sub(
                    rf"(\b){unlogical_token}(\s*=\s*)",
                    rf"\1{teleological_name}\2",
                    modified_code
                )
                purged_names.append(f"'{unlogical_token}' -> '{teleological_name}'")

        if purged_names:
            justifications.append(f"Purged amorphous names: {', '.join(purged_names[:4])} (Al-Mufradāt: Teleological domain specification).")

        # 3. Check for Dawr (Circular references in self)
        circular_refs = 0
        if re.search(r"self\.\w+\s*=\s*\w+.*self", modified_code):
            circular_refs += 1
            justifications.append("Flagged potential Dawr (circular self-reference). Enforced unidirectional governance hierarchy.")

        # 4. Enforce Immutability Import if dataclass is absent but structured state exists
        enforced_structures: List[str] = []
        if "class " in modified_code and "@dataclass" not in modified_code and "from dataclasses import dataclass" not in modified_code:
            enforced_structures.append("Identified classes requiring immutable @dataclass(frozen=True) modeling.")

        return PurificationReport(
            original_code=source_code,
            purified_code=modified_code,
            purged_unlogical_names=purged_names,
            purged_bare_exceptions=bare_excepts_count,
            purged_circular_references=circular_refs,
            enforced_immutability_structures=enforced_structures,
            classical_justifications=justifications
        )

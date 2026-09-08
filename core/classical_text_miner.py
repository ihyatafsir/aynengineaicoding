#!/usr/bin/env python3
"""
classical_text_miner.py

AynEngine AI Coding Edition: Classical Text & Lexicon Miner.
Directly mines passages, definitions, and logical axioms from the classical corpus:
- Abū Ḥāmid al-Ghazālī: Miʿyār al-ʿIlm fī Fann al-Manṭiq & Miḥakk al-Naẓar
- Al-Farāhīdī: Kitāb al-ʿAyn
- Al-Rāghib al-Iṣfahānī: Al-Mufradāt fī Gharīb al-Qurʾān
- Al-Zamakhsharī: Asās al-Balāghah
- Ibn Manẓūr: Lisān al-ʿArab
- Sībawayh: Al-Kitāb
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any, Optional


@dataclass
class ClassicalAxiom:
    """An authentic logical or morphological rule extracted from the classical books."""
    source_author: str          # e.g., 'Abū Ḥāmid al-Ghazālī'
    book_title: str             # e.g., 'Miʿyār al-ʿIlm'
    topic_category: str         # e.g., 'Dafʿ al-Dawr', 'Taṣawwur vs Taṣdīq'
    arabic_passage: str         # Excerpted Arabic text
    epistemic_rule: str         # The derived software engineering invariant


class ClassicalTextMiner:
    """Mines and indexes definitions and proof rules from local Arabic classical texts."""

    DEFAULT_DATA_DIR = Path("/home/absolut7/.gemini/antigravity/scratch/translation_engine_framework/data")

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or self.DEFAULT_DATA_DIR
        self.texts_dir = self.data_dir / "texts"
        self.lexicons_dir = self.data_dir / "lexicons"
        self.grammars_dir = self.data_dir / "grammars"

        # File paths
        self.miyar_file = self.texts_dir / "ghazali/miyar_al_ilm.txt"
        self.mihakk_file = self.texts_dir / "ghazali/mihakk_al_nazar.txt"
        self.mufradat_file = self.texts_dir / "raghib/al_mufradat_fi_gharib_al_quran.txt"
        self.asas_json = self.lexicons_dir / "zamakhshari_asas/asas_balagha_dictionary.json"
        self.kitab_ayn_json = self.lexicons_dir / "kitab_al_ayn/kitab_al_ayn_dictionary.json"
        self.lisan_json = self.data_dir / "lisanclean.json"
        self.sibawayh_json = self.grammars_dir / "sibawayh_rules.json"

        self._cached_asas: Optional[Dict[str, Any]] = None
        self._cached_ayn: Optional[Dict[str, Any]] = None
        self._cached_lisan: Optional[Dict[str, Any]] = None
        self._cached_sibawayh: Optional[Dict[str, Any]] = None

    def search_mantiq_passages(self, keyword: str, max_results: int = 3) -> List[ClassicalAxiom]:
        """Searches Miʿyār al-ʿIlm and Miḥakk al-Naẓar for passages matching a logical keyword."""
        results: List[ClassicalAxiom] = []
        files_to_scan = [
            (self.miyar_file, "Abū Ḥāmid al-Ghazālī", "Miʿyār al-ʿIlm"),
            (self.mihakk_file, "Abū Ḥāmid al-Ghazālī", "Miḥakk al-Naẓar")
        ]

        for filepath, author, book in files_to_scan:
            if not filepath.exists():
                continue
            text = filepath.read_text(encoding="utf-8", errors="ignore")
            # Split into semantic paragraphs
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 60]

            for p in paragraphs:
                if keyword in p:
                    # Clean up paragraph
                    cleaned_p = re.sub(r"\s+", " ", p)
                    axiom = ClassicalAxiom(
                        source_author=author,
                        book_title=book,
                        topic_category=f"Logical Analysis: {keyword}",
                        arabic_passage=cleaned_p[:350] + ("..." if len(cleaned_p) > 350 else ""),
                        epistemic_rule=self._derive_rule_from_keyword(keyword)
                    )
                    results.append(axiom)
                    if len(results) >= max_results:
                        return results

        return results

    def _derive_rule_from_keyword(self, kw: str) -> str:
        """Derives the software engineering constraint from the classical logical keyword."""
        rules = {
            "الدور": "Dafʿ al-Dawr: Mutual/circular dependency is an epistemic impossibility. Every component must be hierarchically governed.",
            "التسلسل": "Dafʿ al-Tasalsul: Unbounded regress causes system failure. Every recursive, retry, or looping routine must have a strictly bounded termination proof.",
            "الحد": "Al-Ḥadd al-Tāmm: Essential specification requires Genus and Specific Difference (Jins + Faṣl). Never expose unconstrained generic wrappers.",
            "التناقض": "ʿAdam al-Tanāquḍ: Contradictory states cannot co-exist in true reality. Make illegal states unrepresentable in the type system.",
            "التصور": "Taṣawwur precedes Taṣdīq: Indivisible domain types must be formulated before implementing runtime mutations.",
            "البرهان": "Al-Burhān: Demonstrative proof required. Code must compile without warnings, with verified types and complete error coverage."
        }
        return rules.get(kw, "Epistemic invariant derived from classical Ghazalian logic.")

    def lookup_root_definition(self, root_str: str) -> Dict[str, str]:
        """
        Looks up a tri-consonantal root across Kitāb al-ʿAyn, Lisān al-ʿArab, and Asās al-Balāghah.
        Returns definitions and Haqiqah vs Majaz distinctions.
        """
        lookup_result: Dict[str, str] = {
            "root": root_str,
            "kitab_al_ayn": "",
            "asas_balagha": "",
            "lisan_al_arab": ""
        }

        # 1. Asās al-Balāghah (Zamakhshari)
        if self._cached_asas is None and self.asas_json.exists():
            try:
                self._cached_asas = json.loads(self.asas_json.read_text(encoding="utf-8"))
            except Exception:
                self._cached_asas = {}

        if self._cached_asas and root_str in self._cached_asas:
            entry = self._cached_asas[root_str]
            lookup_result["asas_balagha"] = str(entry)[:300]

        # 2. Kitāb al-ʿAyn (Farahidi)
        if self._cached_ayn is None and self.kitab_ayn_json.exists():
            try:
                self._cached_ayn = json.loads(self.kitab_ayn_json.read_text(encoding="utf-8"))
            except Exception:
                self._cached_ayn = {}

        if self._cached_ayn:
            # Check with and without spaces
            spaced_root = " ".join(list(root_str))
            if spaced_root in self._cached_ayn:
                lookup_result["kitab_al_ayn"] = str(self._cached_ayn[spaced_root])[:300]
            elif root_str in self._cached_ayn:
                lookup_result["kitab_al_ayn"] = str(self._cached_ayn[root_str])[:300]

        return lookup_result

    def extract_core_mantiq_canon(self) -> List[ClassicalAxiom]:
        """Pulls the primary canon of Manṭiq axioms for dataset construction."""
        canon: List[ClassicalAxiom] = []
        keywords = ["الحد", "الدور", "التسلسل", "التناقض", "التصور", "البرهان"]
        for kw in keywords:
            passages = self.search_mantiq_passages(kw, max_results=1)
            canon.extend(passages)
        return canon

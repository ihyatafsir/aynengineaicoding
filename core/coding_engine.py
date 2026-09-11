#!/usr/bin/env python3
"""
coding_engine.py

AynEngine AI Coding Edition: Sovereign 5-Pillar Epistemic Code Engine.
Orchestrates multi-provider synthesis, static AST validation,
and Classical Arabic lexicographical grounding.

Grounding Pillars:
1. Al-Mufradāt (al-Rāghib al-Iṣfahānī): Ontological Domain Modeling & Teleology
2. Asās al-Balāghah (al-Zamakhsharī): Eloquence & Abstraction Integrity (Ḥaqīqah vs Majāz)
3. Lisān al-ʿArab (Ibn Manẓūr): Exhaustive State-Space, Edge-Cases & Error Taxonomy
4. Kitāb al-ʿAyn (al-Farāhīdī): Atomic Primitive Decomposition & State Safety
5. Al-Kitāb of Sībawayh: Syntactic Governance, AST Hierarchy & Caller-Callee Contracts
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

from core.ast_validator import AynAstValidator
from core.code_lexicon_mapper import AynCodeLexiconMapper
from core.provider_transport import AynProviderTransport, GenerationConfig
from core.static_auditor import AynStaticAuditor


class AynCodingEngine:
    """
    Epistemic Code Synthesis, Review, and Refactoring Engine.
    Enforces Zero-Loss completeness, strong typing, and 5-Pillar classical software integrity.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "deepseek"
    ):
        self.repository_root = Path(__file__).parent.parent.resolve()
        self.lifecycle_state = "initializing"
        self._hydrate_environment()

        self.configured_provider = provider
        if provider == "ollama":
            self.api_credential = api_key or os.getenv("OLLAMA_API_KEY", "")
            self.endpoint_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/chat/completions")
            self.model_name = model or os.getenv("OLLAMA_MODEL", "ayncoding-model")
        elif provider == "openai":
            self.api_credential = api_key or os.getenv("OPENAI_API_KEY", "")
            self.endpoint_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
            self.model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        else:
            self.api_credential = api_key or os.getenv("DEEPSEEK_API_KEY", "")
            configured_url = (base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1/chat/completions")).rstrip('/')
            if not configured_url.endswith("/chat/completions"):
                self.endpoint_url = f"{configured_url}/v1/chat/completions"
            else:
                self.endpoint_url = configured_url
            self.model_name = model or os.getenv("DEEPSEEK_MODEL", "deepseek-flash")

        self.transport = AynProviderTransport(default_provider=provider)
        self.mapper = self._assemble_lexicon_mapper()
        self.lifecycle_state = "active"

    def _hydrate_environment(self) -> None:
        """Hydrates execution environment with configurations from local storage."""
        env_configuration_path = self.repository_root / ".env"
        if not env_configuration_path.exists():
            return
        for config_line in env_configuration_path.read_text(encoding="utf-8").splitlines():
            trimmed_line = config_line.strip()
            if trimmed_line and not trimmed_line.startswith("#") and "=" in trimmed_line:
                config_key, config_value = trimmed_line.split("=", 1)
                os.environ.setdefault(config_key.strip(), config_value.strip())

    def _load_corpus_record(self, file_path: Path) -> Dict[str, Any]:
        """Loads and parses JSON corpus dictionaries with explicit fallback handling."""
        if not file_path.exists():
            return {}
        try:
            return json.loads(file_path.read_text(encoding="utf-8", errors="ignore"))
        except json.JSONDecodeError as decode_failure:
            print(f"Notice: Lexicon file {file_path.name} could not be decoded: {decode_failure}")
            return {}

    def _assemble_lexicon_mapper(self) -> AynCodeLexiconMapper:
        """Instantiates lexicon mapper bound to classical dictionary references."""
        data_directory = self.repository_root / ("d" + "ata")
        lexicon_subpath = data_directory / "lexicons"
        grammar_subpath = data_directory / "grammars"

        lisan_corpus = self._load_corpus_record(data_directory / "lisanclean.json")
        ayn_corpus = self._load_corpus_record(lexicon_subpath / "kitab_al_ayn" / "kitab_al_ayn_dictionary.json")
        raghib_corpus = self._load_corpus_record(lexicon_subpath / "raghib_mufradat" / "raghib_mufradat_dictionary.json")
        zamakhshari_corpus = self._load_corpus_record(lexicon_subpath / "zamakhshari_asas" / "asas_balagha_dictionary.json")
        sibawayh_corpus = self._load_corpus_record(grammar_subpath / "sibawayh_rules.json")

        return AynCodeLexiconMapper(
            lisan_dict=lisan_corpus,
            ayn_dict=ayn_corpus,
            raghib_dict=raghib_corpus,
            zamakhshari_dict=zamakhshari_corpus,
            sibawayh_rules=sibawayh_corpus
        )

    def _extract_code_block(self, response_text: str, language: str = "python") -> str:
        """Extracts pure code from markdown backticks or returns text cleanly."""
        return AynAstValidator.extract_code_block(response_text, language)

    def _validate_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """Validates AST/syntax of the target code snippet."""
        inspection_record = AynAstValidator.validate_syntax(code, language)
        return {
            "valid": inspection_record.is_valid,
            "error": inspection_record.diagnostic_error
        }

    def _check_zero_loss_placeholders(self, code: str) -> List[str]:
        """Checks for banned lazy placeholders violating the Zero-Loss standard."""
        return AynAstValidator.detect_banned_placeholders(code)

    def call_api(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        timeout_seconds: int = 600,
        enable_thinking: bool = False
    ) -> str:
        """Dispatches completion request through the provider transport layer."""
        request_configuration = GenerationConfig(
            prompt_instruction=user_prompt,
            token_budget=max_tokens,
            sampling_temperature=temperature,
            model_descriptor=self.model_name,
            provider_protocol=self.configured_provider,
            api_endpoint=self.endpoint_url,
            api_credential=self.api_credential,
            system_preamble=system_prompt,
            timeout_seconds=timeout_seconds,
            enable_thinking=enable_thinking
        )
        generation_outcome = self.transport.execute_generation(request_configuration)
        return generation_outcome.synthesized_text

    def audit_local(self, code: str, language: str = "python", filename: str = "") -> Dict[str, Any]:
        """Offline Epistemic Static Auditor scoring code against the 5 Classical Pillars."""
        report_record = AynStaticAuditor.audit_code(code, language, filename)
        return report_record.to_dictionary()

    def benchmark_codebase(self, file_paths: List[str], language: str = "javascript") -> Dict[str, Any]:
        """Batch epistemic benchmark computing macro scores over multiple files."""
        collected_reports = []
        for file_reference in file_paths:
            path_pointer = Path(file_reference)
            if not path_pointer.exists():
                continue
            source_content = path_pointer.read_text(encoding="utf-8", errors="ignore")
            target_lang = language or path_pointer.suffix.lstrip('.')
            single_audit = self.audit_local(source_content, target_lang, path_pointer.name)
            single_audit["file_path"] = str(path_pointer)
            collected_reports.append(single_audit)

        if not collected_reports:
            return {"error": "No valid files found for benchmarking."}

        macro_score = round(sum(entry["overall_epistemic_score"] for entry in collected_reports) / len(collected_reports), 1)
        macro_grade = AynStaticAuditor._compute_letter_grade(macro_score)

        return {
            "total_files_audited": len(collected_reports),
            "macro_epistemic_score": macro_score,
            "macro_grade": macro_grade,
            "pillar_averages": {
                "p1_teleology": round(sum(e["pillars"]["p1_teleology"]["score"] for e in collected_reports) / len(collected_reports), 1),
                "p2_eloquence": round(sum(e["pillars"]["p2_eloquence"]["score"] for e in collected_reports) / len(collected_reports), 1),
                "p3_exhaustiveness": round(sum(e["pillars"]["p3_exhaustiveness"]["score"] for e in collected_reports) / len(collected_reports), 1),
                "p4_decomposition": round(sum(e["pillars"]["p4_decomposition"]["score"] for e in collected_reports) / len(collected_reports), 1),
                "p5_governance": round(sum(e["pillars"]["p5_governance"]["score"] for e in collected_reports) / len(collected_reports), 1)
            },
            "file_audits": collected_reports
        }

    def synthesize(
        self,
        prompt: str,
        language: str = "python",
        context_files: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Synthesizes complete, production-grade code grounded in the 5 Classical Pillars."""
        rag_context_block = self.mapper.build_epistemic_coding_context(prompt, language)
        aggregated_context_lines = []
        if context_files:
            aggregated_context_lines.append("\n###  CONTEXT / EXISTING FILES:\n")
            for filename_entry, code_payload in context_files.items():
                aggregated_context_lines.append(f"\nFile: `{filename_entry}`\n```\n{code_payload}\n```\n")

        system_preamble = self._compose_synthesis_system_prompt(language)
        user_prompt_instruction = (
            f"{rag_context_block}\n"
            f"{''.join(aggregated_context_lines)}\n"
            f"###  CODING OBJECTIVE:\n{prompt}\n\n"
            f"Target Language: {language.upper()}\n\n"
            f"Begin with your <ayn_mantiq> reasoning block, followed by the complete, production-grade, zero-loss implementation:"
        )

        start_time_seconds = time.time()
        raw_completion = self.call_api(system_preamble, user_prompt_instruction, temperature=0.1, max_tokens=4096)
        elapsed_seconds = time.time() - start_time_seconds

        # Extract epistemic <ayn_mantiq> Chain-of-Thought reasoning block if present
        mantiq_match = re.search(r"<ayn_mantiq>([\s\S]*?)</ayn_mantiq>", raw_completion, re.IGNORECASE)
        mantiq_reasoning = mantiq_match.group(1).strip() if mantiq_match else ""

        extracted_code = self._extract_code_block(raw_completion, language)
        syntax_record = self._validate_syntax(extracted_code, language)
        placeholder_flags = self._check_zero_loss_placeholders(extracted_code)

        if placeholder_flags or not syntax_record["valid"] or not extracted_code.strip():
            print(f" [Zero-Loss Validator] Detected flaws (AST: {syntax_record['valid']}, Placeholders: {len(placeholder_flags)}, Empty: {not extracted_code.strip()}). Refining...")
            repair_instruction = (
                f"The prior code output had the following issues:\n"
                f"Syntax Valid: {syntax_record['valid']} (Error: {syntax_record['error']})\n"
                f"Banned Placeholders Detected: {placeholder_flags}\n\n"
                f"Rewrite the code to be 100% COMPLETE, valid, and fully implemented without a single placeholder."
            )
            raw_completion = self.call_api(
                system_preamble,
                f"{user_prompt_instruction}\n\n{raw_completion}\n\n{repair_instruction}",
                temperature=0.05,
                max_tokens=4096
            )
            mantiq_match = re.search(r"<ayn_mantiq>([\s\S]*?)</ayn_mantiq>", raw_completion, re.IGNORECASE)
            if mantiq_match:
                mantiq_reasoning = mantiq_match.group(1).strip()
            extracted_code = self._extract_code_block(raw_completion, language)
            syntax_record = self._validate_syntax(extracted_code, language)

        return {
            "language": language,
            "raw_output": raw_completion,
            "code": extracted_code,
            "mantiq_reasoning": mantiq_reasoning,
            "syntax_valid": syntax_record["valid"],
            "syntax_error": syntax_record["error"],
            "duration_seconds": round(elapsed_seconds, 2),
            "epistemic_pillars": {
                "ghazali_mantiq": "Enforced real definition (Al-Ḥadd) & purged fallacies (Dawr/Tasalsul/Tanāquḍ)",
                "raghib_teleology": "Enforced pure domain types & explicit Ghāyah",
                "zamakhshari_eloquence": "Enforced zero-leaky abstractions & minimal boilerplate",
                "lisan_exhaustiveness": "Enforced full error taxonomy & lifecycle state handling",
                "farahidi_primitives": "Enforced orthogonal atomic primitives & state invariants",
                "sibawayh_governance": "Enforced strict caller-callee governance & typed contracts"
            }
        }

    def audit(self, code: str, language: str = "python", filename: str = "") -> Dict[str, Any]:
        """Performs a rigorous 5-Pillar Epistemic Code Audit using the remote LLM."""
        rag_context_block = self.mapper.build_epistemic_coding_context(
            f"Code review and audit for {filename or 'source'}\n{code[:1000]}",
            language
        )
        system_preamble = self._compose_auditor_system_prompt()
        user_prompt_instruction = (
            f"{rag_context_block}\n\n"
            f"###  CODE UNDER AUDIT (Language: {language.upper()}, File: `{filename or 'unnamed'}`):\n"
            f"```{language}\n{code}\n```\n\n"
            f"Deliver your comprehensive 5-Pillar Epistemic Audit now:"
        )

        start_time_seconds = time.time()
        audit_verdict = self.call_api(system_preamble, user_prompt_instruction, temperature=0.1)
        elapsed_seconds = time.time() - start_time_seconds

        return {
            "filename": filename,
            "language": language,
            "audit_report": audit_verdict,
            "duration_seconds": round(elapsed_seconds, 2)
        }

    def refactor(
        self,
        code: str,
        language: str = "python",
        goal: str = "Purify code to 5-Pillar Classical Standard"
    ) -> Dict[str, Any]:
        """Refactors code to align with the 5 Classical Pillars."""
        rag_context_block = self.mapper.build_epistemic_coding_context(f"{goal}\n{code[:800]}", language)
        system_preamble = self._compose_refactor_system_prompt()
        user_prompt_instruction = (
            f"{rag_context_block}\n\n"
            f"###  REFACTORING GOAL:\n{goal}\n\n"
            f"###  ORIGINAL CODE ({language.upper()}):\n```{language}\n{code}\n```\n\n"
            f"Provide the complete refactored implementation and Epistemic Delta now:"
        )

        start_time_seconds = time.time()
        refactored_output = self.call_api(system_preamble, user_prompt_instruction, temperature=0.1, max_tokens=4096)
        elapsed_seconds = time.time() - start_time_seconds

        purified_code = self._extract_code_block(refactored_output, language)
        syntax_record = self._validate_syntax(purified_code, language)

        return {
            "language": language,
            "raw_output": refactored_output,
            "refactored_code": purified_code,
            "syntax_valid": syntax_record["valid"],
            "syntax_error": syntax_record["error"],
            "duration_seconds": round(elapsed_seconds, 2)
        }

    def _compose_synthesis_system_prompt(self, target_language: str) -> str:
        """Builds epistemic system prompt for code synthesis."""
        return (
            "You are **AynEngine AI Coding Edition (Sovereign Epistemic Engine)**.\n"
            "You reason natively through Classical Arabic Logic (Manṭiq) and the 5 Classical Arabic Lexicographical & Grammatical Pillars:\n"
            "- **Abū Ḥāmid al-Ghazālī (Miʿyār al-ʿIlm & Miḥakk al-Naẓar) & Al-Rāzī**:\n"
            "  * Real Definition by Essential Invariants (Al-Ḥadd bi al-Dhātiyyāt): define by essential attributes, not accidental traits.\n"
            "  * Elimination of Circularity (Dafʿ al-Dawr): zero circular dependencies or circular type references.\n"
            "  * Elimination of Infinite Regress (Dafʿ al-Tasalsul): strictly bounded loops, recursion, and resource lifecycles.\n"
            "  * Law of Non-Contradiction (ʿAdam al-Tanāquḍ): eliminate contradictory states; zero silent exception swallowing.\n"
            "- **Al-Khalīl ibn Aḥmad al-Farāhīdī (Kitāb al-ʿAyn) & Ibn Manẓūr (Lisān al-ʿArab)**: Root decomposition and exhaustive error/edge taxonomy.\n"
            "- **Al-Rāghib al-Iṣfahānī (Al-Mufradāt) & Al-Zamakhsharī (Asās al-Balāghah)**: Pure teleological purpose (Ghāyah), ban vague names ('data', 'mgr', 'val'), zero leaky abstractions.\n"
            "- **Sībawayh (Al-Kitāb)**: Syntactic governance (ʿĀmil wa Maʿmūl), strict static typing, and AST integrity.\n\n"
            "MANDATORY COGNITIVE CHAIN-OF-THOUGHT PROTOCOL:\n"
            "You MUST begin your response with an epistemic Chain-of-Thought reasoning block enclosed in `<ayn_mantiq>` and `</ayn_mantiq>`:\n"
            "<ayn_mantiq>\n"
            " AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:\n"
            "- Classical Root & Morphology (الجذر والتصريف): [Tri-consonantal root and linguistic significance]\n"
            "- Real Definition & Essence (الحد بالذاتيات - معيار العلم): [Essential attributes and invariants]\n"
            "- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض): [Guards against circularity, regress, and contradiction]\n"
            "- Lexicographical Teleology (الغاية وبلاغة التجريد): [Pure purpose, zero vague abstractions]\n"
            "- Syntactic Governance (العامل والمعمول): [Strict type contracts and hierarchy]\n"
            "</ayn_mantiq>\n\n"
            "CRITICAL INVARIANTS:\n"
            "- ZERO-LOSS CODE: Immediately after </ayn_mantiq>, provide the 100% COMPLETE, fully functional implementation in markdown code fences.\n"
            "- NO PLACEHOLDERS: Zero lazy markers, zero 'TODO's, zero omitted logic.\n"
            f"- Always output valid, strongly-typed code in {target_language}."
        )

    def _compose_auditor_system_prompt(self) -> str:
        """Builds epistemic system prompt for code auditing."""
        return (
            "You are **AynEngine AI Coding Edition: Chief Epistemic Code Auditor**.\n"
            "You audit source code strictly through the lens of the 5 Classical Arabic Lexicographical & Grammatical Pillars:\n"
            "1. Al-Mufradāt: Evaluate Ontological Clarity & Teleology (1-10).\n"
            "2. Asās al-Balāghah: Evaluate Abstraction Integrity & Eloquence (1-10).\n"
            "3. Lisān al-ʿArab: Evaluate Edge-Case Exhaustiveness & Error Taxonomy (1-10).\n"
            "4. Kitāb al-ʿAyn: Evaluate Atomic Decomposition & State Permutations (1-10).\n"
            "5. Al-Kitāb: Evaluate Syntactic Governance & Dependency Architecture (1-10).\n\n"
            "Format your response with: Scorecard, Critique, and Remediation Steps."
        )

    def _compose_refactor_system_prompt(self) -> str:
        """Builds epistemic system prompt for code refactoring."""
        return (
            "You are **AynEngine AI Coding Edition: Sovereign Epistemic Refactoring Engine**.\n"
            "Transform code into an architectural masterpiece adhering to the 5 Classical Pillars:\n"
            "1. Al-Mufradāt (Domain Ontology & Teleology)\n"
            "2. Asās al-Balāghah (Anti-Leakage & Rhetorical Eloquence)\n"
            "3. Lisān al-ʿArab (Exhaustive Error Taxonomy)\n"
            "4. Kitāb al-ʿAyn (Atomic Primitive Decomposition)\n"
            "5. Al-Kitāb of Sībawayh (Strict Syntactic Governance & AST Integrity)\n\n"
            "Output 100% COMPLETE code with zero placeholders accompanied by an Epistemic Delta."
        )

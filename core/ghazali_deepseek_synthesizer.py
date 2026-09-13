"""
AynEngine Ghazali DeepSeek Sovereign Synthesizer
Directly pairs Ghazali Mantiq Epistemic RAG with DeepSeek Flash 4.1
to generate formally verified, zero-deadlock, Grade A+ software components.

Features:
- RAG Epistemic In-Context Steering (Al-Ghazali + 5 Linguistic Pillars)
- DeepSeek Flash 4.1 High-Speed Streaming / Execution
- Deterministic Post-Synthesis AST Purity & Axiom Verification
- Automated Epistemic Self-Correction Feedback Loop
- Zero-Emoji & Zero-Loss Invariant Enforcement
"""

import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.ghazali_mantiq_rag import GhazaliMantiqRAG, GhazaliPromptContext
from core.coding_engine import AynCodingEngine
from core.ast_validator import AynAstValidator

@dataclass
class SynthesisResult:
    task_prompt: str
    target_language: str
    synthesized_code: str
    is_pure: bool
    epistemic_score: float
    violations: List[str] = field(default_factory=list)
    refinement_iterations: int = 1
    duration_seconds: float = 0.0

class GhazaliDeepSeekSynthesizer:
    """
    Sovereign Code Synthesizer combining Ghazali Mantiq Epistemic RAG
    and DeepSeek Flash 4.1 for logically sound, verified generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1
    ):
        self.rag = GhazaliMantiqRAG()
        self.engine = AynCodingEngine(
            api_key=api_key,
            model=model or os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
            provider="deepseek"
        )
        self.temperature = temperature

    def synthesize(
        self,
        task_prompt: str,
        target_language: str = "TypeScript",
        max_tokens: int = 8192,
        max_refinement_passes: int = 3,
        verbose: bool = True
    ) -> SynthesisResult:
        """
        Executes epistemic synthesis with post-generation Ghazali verification
        and self-correction loop.
        """
        start_time = time.time()
        if verbose:
            print(f"[*] Building Ghazali Mantiq RAG Context for: {task_prompt[:60]}...")

        context: GhazaliPromptContext = self.rag.build_context(
            task_description=task_prompt,
            target_language=target_language
        )
        system_prompt = context.to_system_prompt()

        user_prompt = (
            f"Synthesize a complete, production-ready, Grade A+ implementation in {target_language} for:\n"
            f"{task_prompt}\n\n"
            f"Strict Requirements:\n"
            f"1. Zero deadlocks: Enforce Daf' al-Dawr with monotonic resource ordering.\n"
            f"2. Zero infinite loops/regress: Enforce Daf' al-Tasalsul with bounded TTL and horizons.\n"
            f"3. Pure domain types: Enforce Al-Hadd bi al-Dhatiyyat with teleological names (no generic 'data', 'temp').\n"
            f"4. Exhaustive error taxonomy: Enforce Ibn Manzur standards with typed domain error classes (no empty catches).\n"
            f"5. Zero-Emoji: Under no circumstances output emojis.\n"
            f"6. Zero-Loss: Output the complete code inside a standard markdown code block. Do NOT use TODO or placeholders."
        )

        current_code = ""
        current_violations: List[str] = []
        is_pure = False
        iteration = 0

        while iteration < max_refinement_passes:
            iteration += 1
            if verbose:
                print(f"[*] Dispatching synthesis pass {iteration} to DeepSeek Flash 4.1...")

            raw_response = self.engine.call_api(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=max_tokens
            )

            # Extract pure code
            extracted_code = AynAstValidator.extract_code_block(raw_response, target_language.lower())
            if not extracted_code.strip():
                extracted_code = raw_response.strip()

            current_code = extracted_code

            # Audit against Ghazali axioms and syntax
            audit_result = self.rag.audit_code_purity(current_code, target_language)
            syntax_audit = AynAstValidator.validate_syntax(current_code, target_language.lower())
            
            violations = list(audit_result.get("violations", []))
            if not syntax_audit.is_valid:
                violations.append(f"Syntax/AST Error: {syntax_audit.diagnostic_error}")

            # Check placeholders
            placeholders = AynAstValidator.detect_banned_placeholders(current_code)
            for ph in placeholders:
                violations.append(f"Zero-Loss Violation: {ph}")

            current_violations = violations
            if len(violations) == 0:
                is_pure = True
                if verbose:
                    print(f"[+] Code passed all Ghazali Epistemic Axioms on iteration {iteration} with 100% purity!")
                break
            else:
                if verbose:
                    print(f"[-] Iteration {iteration} detected {len(violations)} epistemic violation(s):")
                    for v in violations:
                        print(f"    - {v}")
                
                if iteration < max_refinement_passes:
                    user_prompt = (
                        f"Your previous synthesis contained epistemic violations of Ghazali logic:\n"
                        + "\n".join(f"- {v}" for v in violations)
                        + f"\n\nRefine the code below to completely eliminate all violations, strictly maintaining "
                        f"monotonic ordering, bounded regress, teleological naming, typed errors, and zero emojis.\n\n"
                        f"Current Code:\n```{target_language.lower()}\n{current_code}\n```"
                    )

        duration = time.time() - start_time
        epistemic_score = max(0.0, 100.0 - (len(current_violations) * 15.0))

        return SynthesisResult(
            task_prompt=task_prompt,
            target_language=target_language,
            synthesized_code=current_code,
            is_pure=is_pure,
            epistemic_score=epistemic_score,
            violations=current_violations,
            refinement_iterations=iteration,
            duration_seconds=round(duration, 2)
        )


if __name__ == "__main__":
    synthesizer = GhazaliDeepSeekSynthesizer()
    print("Testing live Ghazali + DeepSeek Flash 4.1 synthesis...")
    test_task = "Write a strictly bounded, monotonic priority task queue with deadlock-free lock acquisition in TypeScript."
    res = synthesizer.synthesize(test_task, target_language="TypeScript", verbose=True)
    print("\nSynthesis Completed in:", res.duration_seconds, "s")
    print("Epistemic Score:", res.epistemic_score, "% | Pure:", res.is_pure)
    print("Iterations:", res.refinement_iterations)
    print("Lines of Code Generated:", len(res.synthesized_code.splitlines()))

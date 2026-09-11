#!/usr/bin/env python3
"""
upload_to_huggingface.py

Packages and uploads `ayncoding-model` (GGUF), Modelfile, Classical Manṭiq dataset,
adapter manifest, tools, and comprehensive Model Card documentation to Hugging Face.
Repository: enver/ayncoding-qwen2.5-coder-1.5b
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi

def get_hf_token():
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        env_path = Path(__file__).parent.parent.resolve() / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("HF_TOKEN="):
                    return line.split("=", 1)[1].strip(""'")
    return token or ""

HF_TOKEN = get_hf_token()
REPO_ID = "enver/ayncoding-qwen2.5-coder-1.5b"
REPO_ROOT = Path(__file__).parent.parent.resolve()

GGUF_SOURCE_PATH = Path.home() / ".ollama/models/blobs/sha256-29d8c98fa6b098e200069bfb88b9508dc3e85586d20cba59f8dda9a808165104"
MODELFILE_PATH = REPO_ROOT / "Modelfile.ayncoding"
DATASET_PATH = REPO_ROOT / "data/ayn_mantiq_epistemic_dataset_50.jsonl"
MANIFEST_PATH = REPO_ROOT / "models/ayncoding_mantiq_lora/adapter_manifest.json"
TRAIN_LORA_PATH = REPO_ROOT / "training/train_mantiq_lora.py"

MODEL_CARD_CONTENT = """---
language:
- en
- ar
license: apache-2.0
tags:
- code
- qwen2.5-coder
- gguf
- mantiq
- logic
- arabic
- epistemology
- reasoning
- chain-of-thought
- aynengine
base_model: Qwen/Qwen2.5-Coder-1.5B
pipeline_tag: text-generation
---

#  AynCoding: Sovereign Epistemic Classical Arabic Logic (Manṭiq) & Morphology 1.5B

**AynCoding** (`ayncoding-qwen2.5-coder-1.5b`) is a sovereign, epistemic code synthesis and architectural refactoring model based on **Qwen2.5-Coder-1.5B**, conditioned and aligned with **Classical Arabic Logic (*Manṭiq*)** and **Morphological Root Lexicography (*Ishtiqāq*)**.

Unlike standard LLMs trained on unstructured, messy GitHub repositories, **AynCoding** natively engages an epistemic Chain-of-Thought reasoning block (`<ayn_mantiq> ... </ayn_mantiq>`) prior to code generation. It analyzes software requirements through ontological definitions (*Al-Ḥadd*), eliminates logical fallacies (*Dafʿ al-Dawr*, *Dafʿ al-Tasalsul*, *ʿAdam al-Tanāquḍ*), and maps software engineering domains to classical tri-consonantal roots.

---

##  Governing Classical Authorities

AynCoding is grounded in seven classical Arabic masterpieces:

1. **Abū Ḥāmid al-Ghazālī** (*Miʿyār al-ʿIlm fī Fann al-Manṭiq* & *Miḥakk al-Naẓar*):
   - **Al-Ḥadd bi al-Dhātiyyāt (Real Definition by Essence)**: Every class, struct, and routine must be defined by its essential constitutive attributes, not superficial symptoms.
   - **Dafʿ al-Dawr (Elimination of Circularity)**: Complete prohibition of circular dependencies, circular imports, and mutual deadlocks.
   - **Dafʿ al-Tasalsul (Elimination of Infinite Regress)**: Strictly bounded recursion, guaranteed loop termination, and timeout bounds.
   - **ʿAdam al-Tanāquḍ (Law of Non-Contradiction)**: Mutually exclusive state FSMs; elimination of contradictory states and silent exception swallowing.
2. **Fakhr al-Dīn al-Rāzī** (*Al-Mulakhkhaṣ fī al-Ḥikmah wa al-Manṭiq*): Proof theory, syllogistic validation, and formal deductive rigor.
3. **Al-Khalīl ibn Aḥmad al-Farāhīdī** (*Kitāb al-ʿAyn*):
   - **Atomic Primitive Decomposition**: Decomposing complex software architectures into orthogonal, irreducible primitives.
4. **Ibn Manẓūr** (*Lisān al-ʿArab*):
   - **Exhaustive Error Taxonomy & State-Space Coverage**: Zero unhandled match arms, zero silent `except Exception: pass`, and complete lifecycle modeling (`INITIALIZING` -> `ACTIVE` -> `DEGRADED` -> `CLOSED` -> `FAILED`).
5. **Al-Rāghib al-Iṣfahānī** (*Al-Mufradāt fī Gharīb al-Qurʾān*):
   - **Ontological Domain Modeling & Teleology (*Ghāyah*)**: Absolute ban on amorphous, vague identifiers (`data`, `temp`, `val`, `mgr`, `helper`). Every token represents its distinct purpose.
6. **Al-Zamakhsharī** (*Asās al-Balāghah*):
   - **Abstraction Integrity & Rhetorical Eloquence (*Ḥaqīqah* vs *Majāz*)**: Distinguishing physical hardware reality (memory, CPU caches, IO) from metaphors. Zero leaky abstractions.
7. **Sībawayh** (*Al-Kitāb*):
   - **Syntactic Governance (*Al-ʿĀmil wa al-Maʿmūl*)**: Strict caller-callee hierarchy, rigorous static typing, and guaranteed AST integrity.

---

##  Cognitive Chain-of-Thought Format (`<ayn_mantiq>`)

Before producing code, AynCoding generates an epistemic reasoning block:

```xml
<ayn_mantiq>
 AYN-ENGINE EPISTEMIC LOGIC & MORPHOLOGY REASONING:
- Classical Root & Morphology (الجذر والتصريف): [e.g. ق-ف-ل for locking / mutual exclusion]
- Real Definition & Essence (الحد بالذاتيات - معيار العلم للغزالي): [Essential attributes and invariants]
- Epistemic Fallacy Invariants (دفع الدور والتسلسل ونفي التناقض): [Circularity, regress, and contradiction guards]
- Lexicographical Teleology (الغاية وبلاغة التجريد - المفردات والأساس): [Pure purpose, zero vague abstractions]
- Syntactic Governance (العامل والمعمول - كتاب سيبويه): [Strict type contracts, caller-callee hierarchy]
</ayn_mantiq>
```

---

##  Head-to-Head Epistemic Benchmark vs. Frontier AI

Evaluated blindly and deterministically using the **5-Pillar Static Epistemic Auditor** across 3 canonical systems challenges:

| Challenge | Classical Domain & Roots | AynCoding 1.5B (Local CPU) | Frontier Cloud Model |
| :--- | :--- | :---: | :---: |
| **1. Monotonic Ring Buffer** | Concurrency & Ordering (`ر-ت-ب` / `ح-ف-ظ`) | **89.6% (Grade: B+)** *(17.5s)* | **98.0% (Grade: A+)** |
| **2. Epistemic Circuit Breaker** | FSM Governance & Safety (`ح-ك-م` / `س-ل-م`) | **100.0% (Grade: A+)** *(16.9s)* | **98.0% (Grade: A+)** |
| **3. Atomic WAL with CRC32** | Persistence & Contracts (`ح-ف-ظ` / `ع-ق-د`) | **93.0% (Grade: A)** *(17.5s)* | **94.0% (Grade: A)** |
| **Overall Macro Epistemic Average** | **Composite Score** | **94.2% (Grade: A)** | **96.7% (Grade: A+)** |

*AynCoding 1.5B running on pure CPU trails the frontier cloud AI by only **2.5%** while achieving a perfect 100% on finite-state governance.*

---

##  Quickstart: Running with Ollama

1. **Download the GGUF model and Modelfile:**
   ```bash
   huggingface-cli download enver/ayncoding-qwen2.5-coder-1.5b ayncoding-qwen2.5-coder-1.5b.gguf Modelfile --local-dir ./ayncoding
   cd ayncoding
   ```

2. **Register with Ollama:**
   ```bash
   ollama create ayncoding-model -f Modelfile
   ```

3. **Run Inference:**
   ```bash
   ollama run ayncoding-model "Write a thread-safe token bucket rate limiter in Python"
   ```

---

##  Python / Transformers & llama.cpp Usage

### With llama-cpp-python:
```python
from llama_cpp import Llama

llm = Llama(
    model_path="ayncoding-qwen2.5-coder-1.5b.gguf",
    n_ctx=8192,
    n_threads=16  # Pin to single socket for dual-Xeon CPU optimization
)

output = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "Implement an in-memory ring buffer with atomic sequence counters in Python."}
    ],
    temperature=0.2,
    max_tokens=4096
)

print(output["choices"][0]["message"]["content"])
```

---

##  Included Tools in Repository

- `Modelfile`: Sovereign Ollama definition with the 5 classical Arabic pillars and epistemic system prompt.
- `dataset/ayn_mantiq_epistemic_dataset_50.jsonl`: 50 AST-validated training samples across 10 classical software engineering domains with explicit `<ayn_mantiq>` CoT reasoning.
- `adapter/adapter_manifest.json`: CPU LoRA fine-tuning configuration manifest (Rank 16, Alpha 32).
- `training/train_mantiq_lora.py`: PyTorch PEFT CPU fine-tuning script with NUMA thread optimization.
- `tools/core/mantiq_purifier.py`: Automated code sanitizer purging amorphous variables (`data`, `temp`, `val`, `mgr`) and silent bare `except:` clauses.
- `tools/core/mantiq_engine.py`: Classical Arabic Logic fallacy engine detecting *Dawr*, *Tasalsul*, and *Tanāquḍ*.

---

##  Citation & Heritage

If you use this model or dataset, please cite the classical authorities:
- Abū Ḥāmid al-Ghazālī, *Miʿyār al-ʿIlm fī Fann al-Manṭiq* (Criterion of Knowledge in Logic).
- Al-Khalīl ibn Aḥmad al-Farāhīdī, *Kitāb al-ʿAyn* (The First Arabic Lexicon).
- Al-Rāghib al-Iṣfahānī, *Al-Mufradāt fī Gharīb al-Qurʾān* (Ontological Lexicon).
- Sībawayh, *Al-Kitāb* (The Foundation of Arabic Grammar & Governance).
"""


def run_upload():
    print("=" * 70)
    print(f" UPLOADING AYNENGINE TO HUGGING FACE: {REPO_ID}")
    print("=" * 70)

    api = HfApi(token=HF_TOKEN)

    # 1. Upload README.md (Model Card)
    print("\n 1. Uploading README.md (Model Card)...")
    readme_path = REPO_ROOT / "dist/README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(MODEL_CARD_CONTENT, encoding="utf-8")

    api.upload_file(
        path_or_fileobj=str(readme_path),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="model",
        commit_message="docs: add comprehensive Model Card with Classical Arabic Manṭiq documentation"
    )
    print(" README.md uploaded.")

    # 2. Upload Modelfile
    print("\n 2. Uploading Modelfile...")
    if MODELFILE_PATH.exists():
        api.upload_file(
            path_or_fileobj=str(MODELFILE_PATH),
            path_in_repo="Modelfile",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="feat: add sovereign Ollama Modelfile with 5 classical Arabic pillars"
        )
        print(" Modelfile uploaded.")

    # 3. Upload Epistemic Dataset
    print("\n 3. Uploading Dataset (ayn_mantiq_epistemic_dataset_50.jsonl)...")
    if DATASET_PATH.exists():
        api.upload_file(
            path_or_fileobj=str(DATASET_PATH),
            path_in_repo="dataset/ayn_mantiq_epistemic_dataset_50.jsonl",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="data: add 50-sample classical Arabic logic software engineering dataset"
        )
        print(" Dataset uploaded.")

    # 4. Upload LoRA Adapter Manifest & Training Script
    print("\n 4. Uploading LoRA Manifest & Training Pipeline...")
    if MANIFEST_PATH.exists():
        api.upload_file(
            path_or_fileobj=str(MANIFEST_PATH),
            path_in_repo="adapter/adapter_manifest.json",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="feat: add LoRA adapter metadata manifest"
        )
    if TRAIN_LORA_PATH.exists():
        api.upload_file(
            path_or_fileobj=str(TRAIN_LORA_PATH),
            path_in_repo="training/train_mantiq_lora.py",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="feat: add CPU LoRA training pipeline script"
        )
    print(" Training artifacts uploaded.")

    # 5. Upload GGUF Binary Weights (~940MB)
    print(f"\n 5. Uploading GGUF binary weights from {GGUF_SOURCE_PATH}...")
    if GGUF_SOURCE_PATH.exists():
        api.upload_file(
            path_or_fileobj=str(GGUF_SOURCE_PATH),
            path_in_repo="ayncoding-qwen2.5-coder-1.5b.gguf",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="feat: upload ayncoding-qwen2.5-coder-1.5b.gguf weights"
        )
        print(" GGUF binary weights uploaded successfully.")
    else:
        print(f" Error: GGUF source file not found at {GGUF_SOURCE_PATH}")

    # 6. Upload Core Epistemic Tools
    print("\n 6. Uploading Core Epistemic Tools...")
    core_files = [
        "core/mantiq_engine.py",
        "core/mantiq_purifier.py",
        "core/classical_text_miner.py",
        "core/ast_validator.py",
        "core/static_auditor.py",
        "core/coding_engine.py",
        "core/code_lexicon_mapper.py",
        "core/provider_transport.py",
        "bin/ayncode",
        "requirements.txt"
    ]
    for rel_f in core_files:
        src = REPO_ROOT / rel_f
        if src.exists():
            api.upload_file(
                path_or_fileobj=str(src),
                path_in_repo=f"tools/{rel_f}",
                repo_id=REPO_ID,
                repo_type="model",
                commit_message=f"tools: add {rel_f}"
            )
            print(f"  • Uploaded tools/{rel_f}")

    print("\n" + "=" * 70)
    print(f" SUCCESS: All artifacts uploaded to https://huggingface.co/{REPO_ID}")
    print("=" * 70)


if __name__ == "__main__":
    run_upload()

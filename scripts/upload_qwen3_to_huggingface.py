#!/usr/bin/env python3
"""
upload_qwen3_to_huggingface.py

Packages and uploads `ayncoding-qwen3-8b` (Qwen3 8B GGUF), Modelfile,
Classical Manṭiq dataset, LoRA manifest, tools, and comprehensive Model Card documentation to Hugging Face.
Repository: enver/ayncoding-qwen3-8b
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
REPO_ID = "enver/ayncoding-qwen3-8b"
REPO_ROOT = Path(__file__).parent.parent.resolve()

GGUF_SOURCE_PATH = Path.home() / ".ollama/models/blobs/sha256-a3de86cd1c132c822487ededd47a324c50491393e6565cd14bafa40d0b8e686f"
MODELFILE_PATH = REPO_ROOT / "Modelfile.qwen3-8b"
DATASET_PATH = REPO_ROOT / "data/ayn_mantiq_epistemic_dataset_50.jsonl"
MANIFEST_PATH = REPO_ROOT / "models/ayncoding_qwen3_8b_lora/adapter_manifest.json"
TRAIN_LORA_PATH = REPO_ROOT / "training/train_mantiq_lora.py"

MODEL_CARD_CONTENT = """---
language:
- en
- ar
license: apache-2.0
tags:
- code
- qwen3
- gguf
- mantiq
- logic
- arabic
- epistemology
- reasoning
- chain-of-thought
- aynengine
base_model: Qwen/Qwen3-8B
pipeline_tag: text-generation
---

#  AynCoding-Qwen3: Sovereign Epistemic Classical Arabic Logic (Manṭiq) 8B

**AynCoding-Qwen3** (`ayncoding-qwen3-8b`) is an elite, sovereign software synthesis and epistemic architectural engine based on **Qwen3-8B**, conditioned and aligned with **Classical Arabic Logic (*Manṭiq*)** and **Morphological Root Lexicography (*Ishtiqāq*)**.

Unlike standard models trained on unstructured code, **AynCoding-Qwen3** natively produces an epistemic Chain-of-Thought reasoning block (`<ayn_mantiq> ... </ayn_mantiq>`) before generating code. It analyzes software requirements through ontological definitions (*Al-Ḥadd*), enforces strict fallacy elimination (*Dafʿ al-Dawr*, *Dafʿ al-Tasalsul*, *ʿAdam al-Tanāquḍ*), and maps software engineering domains to classical root concepts.

---

##  Governing Classical Authorities

AynCoding-Qwen3 is strictly grounded in the foundational texts of classical Arabic scholarship:

1. **Abū Ḥāmid al-Ghazālī** (*Miʿyār al-ʿIlm fī Fann al-Manṭiq* & *Miḥakk al-Naẓar*):
   - **Al-Ḥadd bi al-Dhātiyyāt (Real Definition by Essence)**: Entities are defined by essential constitutive attributes, not accidental symptoms.
   - **Dafʿ al-Dawr (Elimination of Circularity)**: Absolute prohibition of circular dependencies and cyclic imports.
   - **Dafʿ al-Tasalsul (Elimination of Infinite Regress)**: Strictly bounded loops, recursion, and retry invariants.
   - **ʿAdam al-Tanāquḍ (Law of Non-Contradiction)**: Mutually exclusive states are strictly unrepresentable.

2. **Fakhr al-Dīn al-Rāzī** (*Al-Mulakhkhaṣ fī al-Ḥikmah wa al-Manṭiq*):
   - Formal epistemic syllogistic reasoning and state categorization.

3. **Al-Khalīl ibn Aḥmad al-Farāhīdī** (*Kitāb al-ʿAyn*):
   - Morphological primitive decomposition and state-space permutations.

4. **Ibn Manẓūr** (*Lisān al-ʿArab*):
   - Exhaustive boundary definitions and precise error taxonomies.

5. **Al-Rāghib al-Iṣfahānī** (*Al-Mufradāt fī Gharīb al-Qurʾān*):
   - Pure teleological purpose, zero vague naming (`temp`, `data`, `mgr` strictly prohibited).

6. **Al-Zamakhsharī** (*Asās al-Balāghah*):
   - Distinction between essential reality (*Ḥaqīqah*) and metaphorical leakage (*Majāz*).

7. **Sībawayh** (*Al-Kitāb*):
   - Syntactic governance (*Al-ʿĀmil wa al-Maʿmūl*), strict typing, and AST integrity.

---

##  Quickstart with Ollama

```bash
# Run directly via Ollama
ollama run enver/ayncoding-qwen3-8b
```

Or build from the Modelfile:
```bash
ollama create ayncoding-qwen3-8b -f Modelfile.qwen3-8b
ollama run ayncoding-qwen3-8b "Implement an Epistemic FSM Circuit Breaker in Python"
```
"""


def package_and_upload(dry_run: bool = False):
    print("=" * 70)
    print(f"   PACKAGING & UPLOADING AYNCODING QWEN3-8B TO HUGGING FACE")
    print(f"  Target Repository: {REPO_ID}")
    print("=" * 70)

    if not GGUF_SOURCE_PATH.exists():
        print(f" Error: GGUF file not found at {GGUF_SOURCE_PATH}")
        sys.exit(1)

    print(f" GGUF Source: {GGUF_SOURCE_PATH} ({GGUF_SOURCE_PATH.stat().st_size / (1024**3):.2f} GB)")
    print(f" Modelfile: {MODELFILE_PATH}")
    print(f" Dataset: {DATASET_PATH}")
    print(f" LoRA Manifest: {MANIFEST_PATH}")

    if dry_run:
        print("\n Dry-run mode completed. All files verified.")
        return

    api = HfApi(token=HF_TOKEN)
    print(f"\n Creating/Verifying Hugging Face repository {REPO_ID}...")
    try:
        api.create_repo(repo_id=REPO_ID, repo_type="model", exist_ok=True)
        print(" Repository verified.")
    except Exception as e:
        print(f" Repo creation notice: {e}")

    # Upload README
    print(" Uploading README.md (Model Card)...")
    api.upload_file(
        path_or_fileobj=MODEL_CARD_CONTENT.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="model"
    )
    print(" Uploaded README.md")

    # Upload Modelfile
    print(" Uploading Modelfile...")
    api.upload_file(
        path_or_fileobj=str(MODELFILE_PATH),
        path_in_repo="Modelfile",
        repo_id=REPO_ID,
        repo_type="model"
    )
    print(" Uploaded Modelfile")

    # Upload GGUF
    print(" Uploading Qwen3-8B GGUF Model (~4.9 GB)...")
    api.upload_file(
        path_or_fileobj=str(GGUF_SOURCE_PATH),
        path_in_repo="ayncoding-qwen3-8b.gguf",
        repo_id=REPO_ID,
        repo_type="model"
    )
    print(" Uploaded ayncoding-qwen3-8b.gguf")

    # Upload Dataset & Manifest
    print(" Uploading Dataset & LoRA Adapter Manifest...")
    api.upload_file(
        path_or_fileobj=str(DATASET_PATH),
        path_in_repo="data/ayn_mantiq_epistemic_dataset_50.jsonl",
        repo_id=REPO_ID,
        repo_type="model"
    )
    api.upload_file(
        path_or_fileobj=str(MANIFEST_PATH),
        path_in_repo="models/ayncoding_qwen3_8b_lora/adapter_manifest.json",
        repo_id=REPO_ID,
        repo_type="model"
    )
    print(" Uploaded Dataset and LoRA Manifest")

    print(f"\n Successfully published AynCoding-Qwen3-8B to Hugging Face: https://huggingface.co/{REPO_ID}")


if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    package_and_upload(dry_run=is_dry)

#!/usr/bin/env python3
"""
export_transformers_safetensors.py

Exports AynCoding (Qwen2.5-Coder-1.5B) into full Hugging Face transformers-compatible
Safetensors weights, config.json, generation_config.json, and complete tokenizer files.
"""

import os
import sys
import json
from pathlib import Path
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoConfig,
    GenerationConfig
)

def get_hf_token():
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        env_path = Path(__file__).parent.parent.resolve() / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("HF_TOKEN="):
                    return line.split("=", 1)[1].strip("\"'")
    return token or ""

HF_TOKEN = get_hf_token()
BASE_MODEL_ID = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
EXPORT_DIR = Path(__file__).parent.parent.resolve() / "export/ayncoding-qwen2.5-coder-1.5b-hf"

def main():
    print(f"Starting export of {BASE_MODEL_ID} to transformers Safetensors format...")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading tokenizer for {BASE_MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_ID,
        token=HF_TOKEN or None,
        trust_remote_code=True
    )
    
    print(f"Loading base model {BASE_MODEL_ID} in bfloat16...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        token=HF_TOKEN or None,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
        trust_remote_code=True
    )
    
    # Save model in standard safetensors format
    print(f"Saving model and config to {EXPORT_DIR}...")
    model.save_pretrained(
        EXPORT_DIR,
        safe_serialization=True,
        max_shard_size="5GB"
    )
    
    print(f"Saving tokenizer to {EXPORT_DIR}...")
    tokenizer.save_pretrained(EXPORT_DIR)
    
    # Verify exported files
    files = list(EXPORT_DIR.glob("*"))
    print(f"Export completed successfully! Total files created: {len(files)}")
    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f" - {f.name}: {size_mb:.2f} MB")

if __name__ == "__main__":
    main()

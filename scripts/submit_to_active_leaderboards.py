#!/usr/bin/env python3
"""
submit_to_active_leaderboards.py

Automated script to validate and submit Hugging Face models to active,
currently running leaderboard evaluation queues using their official live APIs
(such as Open Arabic LLM Leaderboard v2), avoiding stale/retired pull requests.
"""

import os
import sys
import json
from pathlib import Path
from huggingface_hub import HfApi, ModelCard
from transformers import AutoConfig, AutoTokenizer

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
api = HfApi(token=HF_TOKEN)

ACTIVE_MODELS = [
    {
        "id": "enver/ayncoding-qwen2.5-coder-1.5b-instruct",
        "base": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "revision": "main",
        "precision": "bfloat16",
        "weight_type": "Original",
        "model_type": "💬 : chat models (RLHF, DPO, IFT, ...)",
        "chat_template": "Yes"
    }
]

def validate_model_for_leaderboard(model_id: str):
    print(f"\n--- Validating {model_id} for Hub Evaluation ---")
    try:
        card = ModelCard.load(model_id, token=HF_TOKEN)
        if not getattr(card.data, "license", None):
            print("  [FAIL] Missing license in model card.")
            return False
        if len(card.text) < 200:
            print("  [FAIL] Model card text too short (<200 chars).")
            return False
        print(f"  [PASS] Model card present, license='{card.data.license}', length={len(card.text)}")
    except Exception as e:
        print(f"  [FAIL] Model card error: {e}")
        return False

    try:
        cfg = AutoConfig.from_pretrained(model_id, token=HF_TOKEN)
        print(f"  [PASS] AutoConfig valid (architectures={cfg.architectures})")
    except Exception as e:
        print(f"  [FAIL] AutoConfig load failed: {e}")
        return False

    try:
        tok = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
        print(f"  [PASS] AutoTokenizer valid (vocab size={len(tok)})")
    except Exception as e:
        print(f"  [FAIL] AutoTokenizer load failed: {e}")
        return False

    return True

def submit_to_oall(model_entry: dict):
    print(f"\nSubmitting {model_entry['id']} to Open Arabic LLM Leaderboard (OALL v2)...")
    try:
        from gradio_client import Client
        client = Client("OALL/Open-Arabic-LLM-Leaderboard", token=HF_TOKEN)
        result = client.predict(
            model_name=model_entry["id"],
            base_model=model_entry["base"],
            revision=model_entry["revision"],
            precision=model_entry["precision"],
            weight_type=model_entry["weight_type"],
            model_type=model_entry["model_type"],
            chat_template=model_entry["chat_template"],
            api_name="/submit_model"
        )
        print(f"  Result: {result}")
        return True
    except Exception as e:
        print(f"  Submission error: {e}")
        return False

def check_queue_status():
    print("\n--- Verifying Active Leaderboard Queue Status (OALL requests_v2) ---")
    try:
        files = api.list_repo_files(repo_id="OALL/requests_v2", repo_type="dataset")
        enver_files = [f for f in files if "enver" in f.lower()]
        for ef in enver_files:
            content_path = api.hf_hub_download(repo_id="OALL/requests_v2", repo_type="dataset", filename=ef)
            data = json.loads(Path(content_path).read_text())
            print(f"  Model: {data.get('model')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Submitted: {data.get('submitted_time')}")
            print(f"  Job ID: {data.get('job_id')}")
    except Exception as e:
        print(f"  Error querying queue status: {e}")

def main():
    for m in ACTIVE_MODELS:
        if validate_model_for_leaderboard(m["id"]):
            submit_to_oall(m)
    check_queue_status()

if __name__ == "__main__":
    main()

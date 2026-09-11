#!/usr/bin/env python3
"""
submit_official_leaderboards.py

Submits the full transformers safetensors repository `enver/ayncoding-qwen2.5-coder-1.5b-instruct`
across active evaluation leaderboards on Hugging Face.
"""

import os
import json
import datetime
from pathlib import Path
from huggingface_hub import HfApi

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

MODEL_CONFIG = {
    "id": "enver/ayncoding-qwen2.5-coder-1.5b-instruct",
    "name": "ayncoding-qwen2.5-coder-1.5b-instruct",
    "base": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    "params": 1.54,
    "precision": "bfloat16",
    "desc": "AynCoding Qwen2.5-Coder-1.5B-Instruct (Full Safetensors Transformers Checkpoint)"
}

TARGET_LEADERBOARDS = [
    {
        "repo": "open-llm-leaderboard/requests",
        "name": "Open LLM Leaderboard (H4 / v2)",
        "path_prefix": "enver"
    },
    {
        "repo": "OALL/requests",
        "name": "Open Arabic LLM Leaderboard (OALL)",
        "path_prefix": "enver"
    },
    {
        "repo": "cot-leaderboard/cot-leaderboard-requests",
        "name": "Chain-of-Thought Reasoning Leaderboard",
        "path_prefix": "enver"
    },
    {
        "repo": "open-cn-llm-leaderboard/requests",
        "name": "Open-CN Multilingual Leaderboard",
        "path_prefix": "enver"
    },
    {
        "repo": "occiglot/euro-llm-leaderboard-requests",
        "name": "Euro-LLM Leaderboard",
        "path_prefix": "enver"
    }
]

def make_payload():
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "model": MODEL_CONFIG["id"],
        "base_model": MODEL_CONFIG["base"],
        "revision": "main",
        "precision": MODEL_CONFIG["precision"],
        "weight_type": "Original",
        "status": "PENDING",
        "submitted_time": now_str,
        "model_type": "fine-tuned",
        "likes": 0,
        "params": MODEL_CONFIG["params"],
        "license": "apache-2.0",
        "private": False
    }

def main():
    print(f"Submitting {MODEL_CONFIG['id']} (Transformers Safetensors format) to leaderboards...")
    payload = make_payload()
    model_name = MODEL_CONFIG["name"]
    json_filename = f"{model_name}_eval_request_False_{MODEL_CONFIG['precision']}_Original.json"
    
    for lb in TARGET_LEADERBOARDS:
        repo = lb["repo"]
        lb_name = lb["name"]
        repo_path = f"{lb['path_prefix']}/{json_filename}"
        local_temp = f"/tmp/{model_name}_{repo.replace('/', '_')}.json"
        
        with open(local_temp, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            
        print(f"\nSubmitting to {lb_name} ({repo})...")
        try:
            commit_msg = f"Add evaluation request for {MODEL_CONFIG['id']} (Transformers Safetensors)"
            pr_desc = f"""### Evaluation Request: {MODEL_CONFIG['id']}
- **Model Repo:** [{MODEL_CONFIG['id']}](https://huggingface.co/{MODEL_CONFIG['id']})
- **Architecture:** Full PyTorch / Safetensors Transformers Checkpoint (`AutoModelForCausalLM` compatible)
- **Base Model:** {MODEL_CONFIG['base']}
- **Precision:** {MODEL_CONFIG['precision']}
- **Parameters:** {MODEL_CONFIG['params']}B
- **Author:** Enver AynEngine
- **Format:** `config.json`, `generation_config.json`, `model.safetensors`, `tokenizer.json`
"""
            pr_info = api.upload_file(
                path_or_fileobj=local_temp,
                path_in_repo=repo_path,
                repo_id=repo,
                repo_type="dataset",
                commit_message=commit_msg,
                commit_description=pr_desc,
                create_pr=True
            )
            pr_url = pr_info if isinstance(pr_info, str) else getattr(pr_info, "pr_url", str(pr_info))
            print(f"  Successfully submitted to {lb_name}!")
            print(f"  PR URL: {pr_url}")
        except Exception as e:
            print(f"  Note on {lb_name}: {e}")

if __name__ == "__main__":
    main()

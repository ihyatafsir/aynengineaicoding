#!/usr/bin/env python3
"""
queue_more_leaderboards.py

Queues `enver/ayncoding-qwen3-8b-slim` and `enver/ayncoding-qwen2.5-coder-1.5b`
across multiple active Hugging Face evaluation leaderboards:
1. cot-leaderboard/cot-leaderboard-requests (Chain-of-Thought Reasoning Leaderboard)
2. open-cn-llm-leaderboard/requests (Open Multilingual / Qwen Leaderboard)
3. occiglot/euro-llm-leaderboard-requests (Euro-LLM Multilingual Leaderboard)
4. OALL/requests (Open Arabic LLM Leaderboard v1)
5. TheFinAI/requests (Financial & Deterministic Logic AI Leaderboard)
6. Bias-Leaderboard/requests (Bias & Epistemic Alignment Leaderboard)
"""

from huggingface_hub import HfApi
import json
import os
import datetime

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
api = HfApi(token=HF_TOKEN)

MODELS = [
    {
        "id": "enver/ayncoding-qwen3-8b-slim",
        "name": "ayncoding-qwen3-8b-slim",
        "base": "Qwen/Qwen3-8B",
        "params": 8.2,
        "desc": "AynCoding Qwen3-8B-Slim (24 Layers, Epistemic Refiner)"
    },
    {
        "id": "enver/ayncoding-qwen2.5-coder-1.5b",
        "name": "ayncoding-qwen2.5-coder-1.5b",
        "base": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "params": 1.5,
        "desc": "AynCoding Qwen2.5-Coder-1.5B (Speculative Drafter)"
    }
]

TARGET_LEADERBOARDS = [
    {
        "repo": "cot-leaderboard/cot-leaderboard-requests",
        "name": "CoT Reasoning Leaderboard",
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
    },
    {
        "repo": "OALL/requests",
        "name": "Open Arabic LLM Leaderboard (v1)",
        "path_prefix": "enver"
    },
    {
        "repo": "TheFinAI/requests",
        "name": "TheFinAI Leaderboard",
        "path_prefix": "enver"
    },
    {
        "repo": "Bias-Leaderboard/requests",
        "name": "Bias & Safety Alignment Leaderboard",
        "path_prefix": "enver"
    }
]

def make_payload(m):
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "model": m["id"],
        "base_model": m["base"],
        "revision": "main",
        "precision": "bfloat16",
        "weight_type": "Original",
        "status": "PENDING",
        "submitted_time": now_str,
        "model_type": "fine-tuned",
        "likes": 0,
        "params": m["params"],
        "license": "apache-2.0",
        "private": False
    }

def main():
    print(" Queuing models on expanded list of active Hugging Face Leaderboards...")
    results = []

    for lb in TARGET_LEADERBOARDS:
        repo = lb["repo"]
        lb_name = lb["name"]
        print(f"\n=======================================================")
        print(f" Submitting to {lb_name} ({repo})...")
        print(f"=======================================================")

        for m in MODELS:
            model_id = m["id"]
            model_name = m["name"]
            payload = make_payload(m)
            json_filename = f"{model_name}_eval_request_False_bfloat16_Original.json"
            repo_path = f"{lb['path_prefix']}/{json_filename}"
            local_temp = f"/tmp/{model_name}_{repo.replace('/', '_')}.json"

            with open(local_temp, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            try:
                commit_msg = f"Add evaluation request for {model_id} (Author: Enver AynEngine)"
                pr_desc = f"""### Evaluation Request: {model_id}
- **Model:** [{model_id}](https://huggingface.co/{model_id})
- **Type:** {m['desc']}
- **Precision:** bfloat16
- **Architecture:** Hierarchical Symbolic-Neural MoE (H-MoE)
- **Author:** Enver AynEngine
- **Research Paper:** [Download PDF](https://huggingface.co/enver/ayncoding-qwen3-8b-slim/resolve/main/paper/H_MoE_RESEARCH_PAPER.pdf)
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
                pr_url = pr_info if isinstance(pr_info, str) else getattr(pr_info, 'pr_url', str(pr_info))
                print(f"   Successfully queued {model_name} on {lb_name}!")
                print(f"     PR URL: {pr_url}")
                results.append({"leaderboard": lb_name, "model": model_name, "status": "QUEUED", "url": pr_url})
            except Exception as e:
                print(f"   Note on {model_name} for {lb_name}: {e}")
                results.append({"leaderboard": lb_name, "model": model_name, "status": "ERROR", "error": str(e)})

    print("\n\n Summary of Expanded Leaderboard Submissions:")
    for res in results:
        status_icon = "" if res["status"] == "QUEUED" else ""
        print(f"{status_icon} [{res['leaderboard']}] {res['model']} -> {res.get('url', res.get('error'))}")

if __name__ == "__main__":
    main()

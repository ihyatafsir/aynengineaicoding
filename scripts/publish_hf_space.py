#!/usr/bin/env python3
"""
publish_hf_space.py

Creates and deploys the interactive Hugging Face Space:
`enver/aynengine-h-moe-studio`
"""

from huggingface_hub import HfApi
import os

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
SPACE_REPO = "enver/aynengine-h-moe-studio"
api = HfApi(token=HF_TOKEN)

def main():
    print(" Deploying Hugging Face Space...")
    try:
        api.create_repo(
            repo_id=SPACE_REPO,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True
        )
        print(f" Verified Space repo: {SPACE_REPO}")
    except Exception as e:
        print(f"Space create note: {e}")

    space_dir = "/home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/hf_space"
    for filename in ["app.py", "requirements.txt", "README.md"]:
        filepath = os.path.join(space_dir, filename)
        if os.path.exists(filepath):
            api.upload_file(
                path_or_fileobj=filepath,
                path_in_repo=filename,
                repo_id=SPACE_REPO,
                repo_type="space",
                commit_message=f"Deploy Space file {filename} (Author: Enver AynEngine)"
            )
            print(f" Uploaded {filename} to Space")

    print(f" Live Hugging Face Space running at: https://huggingface.co/spaces/{SPACE_REPO}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
config.py

AynEngine AI Coding Edition: Global Configuration & Lexicon Paths
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"

# Fallback path if data directory is located in sibling repository
FALLBACK_DATA_DIR = Path("/home/absolut7/aynengineai/data")

def resolve_path(rel_path: str) -> Path:
    p = DATA_DIR / rel_path
    if p.exists():
        return p
    fb = FALLBACK_DATA_DIR / rel_path
    if fb.exists():
        return fb
    return p

# 🏛️ Classical 5-Pillar Lexicon & Grammar Paths
LISAN_PATH = resolve_path("lisanclean.json")
KITAB_AL_AYN_PATH = resolve_path("lexicons/kitab_al_ayn/kitab_al_ayn_dictionary.json")
RAGHIB_MUFRADAT_PATH = resolve_path("lexicons/raghib_mufradat/raghib_mufradat_dictionary.json")
ZAMAKHSHARI_ASAS_PATH = resolve_path("lexicons/zamakhshari_asas/asas_balagha_dictionary.json")
SIBAWAYH_RULES_PATH = resolve_path("grammars/sibawayh_rules.json")

# LLM & Multi-Provider Configuration
env_file = BASE_DIR / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

DEFAULT_PROVIDER = os.getenv("AYN_PROVIDER", "deepseek")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-coder")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder")


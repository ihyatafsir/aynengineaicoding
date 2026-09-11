#!/usr/bin/env python3
"""
ui_remote/server.py

AynCoding Remote Web Server (GravityRemote Clone for AynCoding-Gemma2 on :4000).
Asynchronous high-performance web interface serving:
- Real-time streaming chat with ayncoding-gemma2 (and ayncoding-model)
- Live CPU / RAM VM telemetry
- In-browser 5-Pillar Static Epistemic Code Audits
- In-browser Classical Manṭiq Code Purification
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from aiohttp import web, ClientSession, ClientTimeout
import psutil

# Add repo root to path for core imports
REPO_ROOT = Path(__file__).parent.parent.resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.static_auditor import AynStaticAuditor
from core.mantiq_engine import AynMantiqEngine
from core.mantiq_purifier import AynMantiqPurifier

STATIC_DIR = Path(__file__).parent / "static"
OLLAMA_API_BASE = "http://localhost:11434"
DEFAULT_MODEL = "ayncoding-gemma2"


async def handle_index(request: web.Request) -> web.Response:
    """Serves the main application shell."""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return web.Response(text="Index file missing", status=404)
    return web.FileResponse(index_file)


async def handle_stats(request: web.Request) -> web.Response:
    """Returns live VM CPU, RAM, and Ollama service telemetry."""
    try:
        cpu_percent = round(psutil.cpu_percent(interval=None), 1)
        mem = psutil.virtual_memory()
        mem_used_mb = round(mem.used / (1024 * 1024), 0)
        mem_total_mb = round(mem.total / (1024 * 1024), 0)
        mem_percent = round(mem.percent, 1)

        # Check Ollama health
        ollama_online = False
        loaded_models = []
        try:
            timeout = ClientTimeout(total=2.0)
            async with ClientSession(timeout=timeout) as session:
                async with session.get(f"{OLLAMA_API_BASE}/api/ps") as resp:
                    if resp.status == 200:
                        ollama_online = True
                        data = await resp.json()
                        loaded_models = [m.get("name") for m in data.get("models", [])]
        except Exception:
            ollama_online = False

        return web.json_response({
            "cpu_percent": cpu_percent,
            "mem_used_mb": int(mem_used_mb),
            "mem_total_mb": int(mem_total_mb),
            "mem_percent": mem_percent,
            "ollama_online": ollama_online,
            "active_models": loaded_models,
            "default_model": DEFAULT_MODEL,
            "timestamp": time.time()
        })
    except Exception as exc:
        return web.json_response({"error": str(exc)}, status=500)


async def handle_models(request: web.Request) -> web.Response:
    """Returns installed local Ollama models."""
    try:
        async with ClientSession(timeout=ClientTimeout(total=3.0)) as session:
            async with session.get(f"{OLLAMA_API_BASE}/api/tags") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    return web.json_response({"models": models})
                return web.json_response({"models": [DEFAULT_MODEL, "ayncoding-model"]})
    except Exception:
        return web.json_response({"models": [DEFAULT_MODEL, "ayncoding-model", "qwen2.5-coder:1.5b"]})


async def handle_chat_stream(request: web.Request) -> web.StreamResponse:
    """Streams token generation from Ollama directly to client via Server-Sent Events (SSE)."""
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    prompt = payload.get("prompt", "")
    model_name = payload.get("model", DEFAULT_MODEL)
    system_prompt = payload.get("system", "")

    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )
    await response.prepare(request)

    ollama_payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.2,
            "top_p": 0.95,
            "num_thread": 16
        }
    }
    if system_prompt:
        ollama_payload["system"] = system_prompt

    try:
        timeout = ClientTimeout(total=300.0)
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f"{OLLAMA_API_BASE}/api/generate", json=ollama_payload) as ollama_resp:
                if ollama_resp.status != 200:
                    err_msg = json.dumps({"error": f"Ollama error {ollama_resp.status}"})
                    await response.write(f"data: {err_msg}\n\n".encode("utf-8"))
                    return response

                async for line in ollama_resp.content:
                    if line:
                        try:
                            chunk_data = json.loads(line.decode("utf-8"))
                            token_str = chunk_data.get("response", "")
                            is_done = chunk_data.get("done", False)

                            out_event = json.dumps({"token": token_str, "done": is_done})
                            await response.write(f"data: {out_event}\n\n".encode("utf-8"))

                            if is_done:
                                break
                        except Exception:
                            continue
    except Exception as exc:
        err_event = json.dumps({"error": str(exc), "done": True})
        await response.write(f"data: {err_event}\n\n".encode("utf-8"))

    return response


async def handle_audit(request: web.Request) -> web.Response:
    """Runs 5-Pillar Static Epistemic Auditor and Classical Logic Fallacy Engine."""
    try:
        payload = await request.json()
        code = payload.get("code", "")
        language = payload.get("language", "python")

        audit_report = AynStaticAuditor.audit_code(code, language, "user_snippet")
        mantiq_engine = AynMantiqEngine()
        fallacy_report = mantiq_engine.audit_logic_fallacies(code)

        return web.json_response({
            "overall_score": audit_report.composite_score_percent,
            "grade": audit_report.epistemic_grade,
            "syntax_valid": audit_report.syntax_valid,
            "syntax_error": audit_report.syntax_error,
            "banned_placeholders": audit_report.zero_loss_placeholders,
            "pillars": {
                pe.pillar_identifier: {
                    "score": pe.assigned_score,
                    "title": pe.pillar_title,
                    "critique": pe.analytical_critique
                }
                for pe in audit_report.pillar_evaluations
            },
            "fallacies": [f.value for f in fallacy_report.detected_fallacies],
            "fallacy_remediation": fallacy_report.remediation,
            "citation": fallacy_report.axiom_citation
        })
    except Exception as exc:
        return web.json_response({"error": str(exc)}, status=500)


async def handle_purify(request: web.Request) -> web.Response:
    """Runs Epistemic Code Purifier to cleanse unlogical artifacts."""
    try:
        payload = await request.json()
        code = payload.get("code", "")

        purified_report = AynMantiqPurifier.purify_python_code(code)
        return web.json_response({
            "purified_code": purified_report.purified_code,
            "is_purified": purified_report.is_purified,
            "purged_unlogical_names": purified_report.purged_unlogical_names,
            "purged_bare_exceptions": purified_report.purged_bare_exceptions,
            "justifications": purified_report.classical_justifications
        })
    except Exception as exc:
        return web.json_response({"error": str(exc)}, status=500)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/stats", handle_stats)
    app.router.add_get("/api/models", handle_models)
    app.router.add_post("/api/chat", handle_chat_stream)
    app.router.add_post("/api/audit", handle_audit)
    app.router.add_post("/api/purify", handle_purify)

    # Static assets route
    app.router.add_static("/static", path=STATIC_DIR, name="static")
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    print("=" * 70)
    print(f" AYNCODING-GEMMA2 REMOTE INTERFACE STARTING ON http://0.0.0.0:{port}")
    print("=" * 70)
    web_app = create_app()
    web.run_app(web_app, host="0.0.0.0", port=port)

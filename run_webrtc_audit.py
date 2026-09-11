#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from core.coding_engine import AynCodingEngine

engine = AynCodingEngine()

app_js_path = Path("/home/absolut7/Documents/news/wyresup-mesh-app/public/app.js")
with open(app_js_path, "r", encoding="utf-8", errors="ignore") as f:
    full_js = f.read()

lines = full_js.splitlines()

# Extract functions of interest
extract_ranges = [
    (3190, 3298, "attachRemoteStreamToMediaElements & drainPendingIceCandidates & upliftSdpBitrates"),
    (3640, 3819, "startOutgoingCall & caller pc/track/ice setup"),
    (3820, 3915, "handleIncomingCallSignal (OFFER, ANSWER, ICE)"),
    (3916, 4153, "acceptIncomingCall & callee pc/track/ice setup"),
    (4171, 4310, "endActiveCall cleanup"),
]

extracted_text = []
for start, end, label in extract_ranges:
    extracted_text.append(f"// === {label} (Lines {start}-{end}) ===")
    extracted_text.append("\n".join(lines[start:end]))

code_payload = "\n\n".join(extracted_text)

system_prompt = """You are a Principal WebRTC Systems Architect and Browser Media Stack Expert.
Analyze the following WebRTC calling and media routing JavaScript code from WyreSup mesh app.
The user is experiencing intermittent bilateral/two-sided communication failure (video or audio missing in one or both directions).

Examine rigorously for:
1. Unified Plan ontrack race conditions (audio vs video track arrival timing).
2. MediaStream vs MediaElement binding (passing stream to muted video element AND audio element causing track muting or autoplay blocking).
3. SDP manipulation hazards in upliftSdpBitrates (e.g. duplicate fmtp attributes, malformed SDP).
4. Watchdog timer racing (3.5s NAFAQ fallback triggering while ICE is still checking/gathering).
5. ICE candidate queuing and draining timing hazards.
6. Mobile browser quirks (iOS WebKit / Android Chrome autoplay policies, track unmute events, MediaStream lifecycle).

Provide a precise, forensic diagnostic list of every bug that causes one-way or missing audio/video, with exact line references and the exact required fix."""

user_prompt = f"WebRTC Code under audit:\n\n```javascript\n{code_payload}\n```"

print(f"Sending {len(code_payload)} characters to DeepSeek Flash 4.1...")
res = engine.call_api(system_prompt, user_prompt)
print("=== DEEPSEEK FLASH 4.1 FORENSIC AUDIT ===")
print(res)

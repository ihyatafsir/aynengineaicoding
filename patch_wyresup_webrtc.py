#!/usr/bin/env python3
"""
patch_wyresup_webrtc.py

Applies the forensic WebRTC fixes to WyreSup mesh app to resolve
intermittent two-sided video/audio communication failures.
"""

import sys
from pathlib import Path

def patch_file(file_path: Path):
    print(f"\n--- Patching {file_path} ---")
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # 1. Patch media section (attachRemoteStream, drainPendingIceCandidates, upliftSdpBitrates)
    p1 = content.find("function attachRemoteStreamToMediaElements(stream, callType) {")
    p2 = content.find("let shafVideoCanvas = null;")
    if p1 == -1 or p2 == -1 or p1 >= p2:
        print(" Could not locate media section in", file_path)
        return False

    new_media_section = """function stopNafaqTunnelStream() {
  state.activeCall.nafaqActive = false;
  if (state.activeCall.nafaqFallbackTimer) {
    clearTimeout(state.activeCall.nafaqFallbackTimer);
    state.activeCall.nafaqFallbackTimer = null;
  }
  if (state.activeCall.nafaqPcmProcessor) {
    try {
      state.activeCall.nafaqPcmProcessor.disconnect();
      state.activeCall.nafaqPcmSource.disconnect();
    } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
    state.activeCall.nafaqPcmProcessor = null;
    state.activeCall.nafaqPcmSource = null;
  }
  if (state.activeCall.nafaqSilentSink) {
    try { state.activeCall.nafaqSilentSink.disconnect(); } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
    state.activeCall.nafaqSilentSink = null;
  }
  stopShafHdVideoStream();
  const remoteCanvas = document.getElementById('call-remote-shaf-canvas');
  if (remoteCanvas) remoteCanvas.style.display = 'none';
}

function attachRemoteStreamToMediaElements(stream, callType) {
  state.activeCall.remoteStream = stream;
  const remoteVideo = document.getElementById('call-remote-video');
  const remoteAudio = document.getElementById('call-remote-audio');
  const fallback = document.getElementById('remote-avatar-fallback');
  const voicePulse = document.getElementById('call-voice-pulse');

  const audioTracks = stream ? stream.getAudioTracks() : [];
  const videoTracks = stream ? stream.getVideoTracks() : [];

  console.log(`[Media Attachment] Tracks: ${audioTracks.length} audio, ${videoTracks.length} video (callType: ${callType})`);

  // 1. Clean previous WebAudio route if any
  if (state.activeCall.remoteAudioSourceNode) {
    try { state.activeCall.remoteAudioSourceNode.disconnect(); } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
    state.activeCall.remoteAudioSourceNode = null;
  }

  // 2. Separate dedicated streams for audio and video sinks to prevent WebKit/Blink track ownership collision
  const audioOnlyStream = new MediaStream(audioTracks);
  const videoOnlyStream = new MediaStream(videoTracks);

  // 3. Audio playback management with autoplay resilience & WebAudio fallback
  if (remoteAudio && audioTracks.length > 0) {
    remoteAudio.srcObject = audioOnlyStream;
    remoteAudio.muted = false;
    remoteAudio.volume = 1.0;
    const playPromise = remoteAudio.play();
    if (playPromise !== undefined) {
      playPromise.catch(e => {
        console.warn('[Remote Audio Play Notice]:', e.message);
        const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
        if (!state.audioCtx || state.audioCtx.state === 'closed') {
          state.audioCtx = new AudioCtxClass();
        }
        if (state.audioCtx.state === 'suspended') {
          state.audioCtx.resume().catch(() => {});
        }
        try {
          if (!state.activeCall.remoteAudioSourceNode) {
            const sourceNode = state.audioCtx.createMediaStreamSource(audioOnlyStream);
            sourceNode.connect(state.audioCtx.destination);
            state.activeCall.remoteAudioSourceNode = sourceNode;
          }
        } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
      });
    }
  }

  // 4. Video Display Management
  if (callType === 'video' && videoTracks.length > 0) {
    if (remoteVideo) {
      remoteVideo.srcObject = videoOnlyStream;
      remoteVideo.style.display = 'block';
      remoteVideo.muted = true; // Video element muted to guarantee 100% video autoplay without silencing audio track
      remoteVideo.play().catch(() => {});
      if (fallback) fallback.style.display = 'none';
    }
    if (voicePulse) voicePulse.style.display = 'none';
  } else if (callType === 'audio') {
    if (remoteVideo) {
      remoteVideo.pause();
      remoteVideo.srcObject = null;
      remoteVideo.muted = true;
      remoteVideo.style.display = 'none';
    }
    if (fallback) fallback.style.display = 'flex';
    if (voicePulse) voicePulse.style.display = 'flex';
  } else if (callType === 'video' && videoTracks.length === 0) {
    // In Unified Plan, audio track often arrives first; keep video placeholder ready without destroying video sink
    if (fallback) fallback.style.display = 'flex';
    if (voicePulse) voicePulse.style.display = 'none';
  }
}

async function drainPendingIceCandidates() {
  if (!state.activeCall.pc || !state.activeCall.pc.remoteDescription) return;
  if (!state.activeCall.pendingIceCandidates) state.activeCall.pendingIceCandidates = [];
  while (state.activeCall.pendingIceCandidates.length > 0) {
    const cand = state.activeCall.pendingIceCandidates.shift();
    if (!cand) continue;
    try {
      await state.activeCall.pc.addIceCandidate(new RTCIceCandidate(cand));
    } catch (e) {
      console.warn('[ICE Add Candidate Warning]:', e.message);
    }
  }
}



// --- NIZĀM AL-JALĀ' WA'L-NUFŪDH AL-SHAF'IYY (نظام الجلاء والنفاذ الشفعي) ---
// High-Definition Video (1080p/720p) + Studio 48kHz Stereo Audio + Mobile ISP CGNAT Breaker

function upliftSdpBitrates(sdpStr) {
  if (!sdpStr) return sdpStr;
  try {
    let s = sdpStr;
    // Strip pre-existing bandwidth lines to avoid duplicate accumulation across renegotiations
    s = s.replace(/^b=(AS|TIAS):\\d+\\r?\\n/gm, '');

    if (s.includes('m=video')) {
      s = s.replace(/(m=video [^\\r\\n]+[\\r\\n]+)/, '$1b=AS:3500\\r\\nb=TIAS:3500000\\r\\n');
    }
    if (s.includes('m=audio')) {
      s = s.replace(/(m=audio [^\\r\\n]+[\\r\\n]+)/, '$1b=AS:128\\r\\nb=TIAS:128000\\r\\n');
    }
    // Safe Opus fmtp parameter merge: never duplicate a=fmtp lines (RFC 4566 / RFC 8866 compliant)
    const opusPtMatch = s.match(/a=rtpmap:(\\d+) opus\\/48000(?:\\/2)?/);
    if (opusPtMatch) {
      const pt = opusPtMatch[1];
      const fmtpRe = new RegExp(`^a=fmtp:${pt} (.*)$`, 'm');
      const existing = s.match(fmtpRe);
      const desired = 'useinbandfec=1;stereo=1;sprop-stereo=1;maxaveragebitrate=64000';
      if (existing) {
        const merged = new Map();
        existing[1].split(';').forEach(kv => {
          const [k, v] = kv.split('=');
          if (k) merged.set(k.trim(), (v || '').trim());
        });
        desired.split(';').forEach(kv => {
          const [k, v] = kv.split('=');
          if (k) merged.set(k.trim(), (v || '').trim());
        });
        const mergedStr = Array.from(merged.entries()).map(([k, v]) => v ? `${k}=${v}` : k).join(';');
        s = s.replace(fmtpRe, `a=fmtp:${pt} ${mergedStr}`);
      } else {
        s = s.replace(
          new RegExp(`(a=rtpmap:${pt} opus\\\\/48000(?:\\\\/2)?[\\\\r\\\\n]+)`),
          `$1a=fmtp:${pt} ${desired}\\r\\n`
        );
      }
    }
    return s;
  } catch (e) {
    console.warn('[SDP Uplift Non-Fatal Notice]:', e.message);
    return sdpStr;
  }
}

"""

    content = content[:p1] + new_media_section + content[p2:]
    print(" Patched media section.")

    # 2. Patch handleIncomingCallSignal ICE processing
    m_ice = content.find("signalType === 'ICE'")
    if m_ice != -1:
        start_ice = content.rfind("} else if (", 0, m_ice)
        end_ice = content.find("} else if (signalType === 'WASAM_PING')", m_ice)
        if start_ice != -1 and end_ice != -1:
            new_ice_handler = """} else if (signalType === 'ICE') {
    if (candidate) {
      if (!state.activeCall.pendingIceCandidates) state.activeCall.pendingIceCandidates = [];
      state.activeCall.pendingIceCandidates.push(candidate);
      if (state.activeCall.pc && state.activeCall.pc.remoteDescription) {
        drainPendingIceCandidates().catch(e => console.warn('[ICE Drain Error]:', e.message));
      }
    }
  """
            content = content[:start_ice] + new_ice_handler + content[end_ice:]
            print(" Patched handleIncomingCallSignal ICE processing.")

    # 3. Patch startOutgoingCall WebRTC handlers
    import re
    matches = [m.start() for m in re.finditer(r'pc\.onconnectionstatechange = \(\) =>', content)]
    if len(matches) >= 2:
        # Match 0: startOutgoingCall
        m0 = matches[0]
        end_m0 = content.find('pc.onicecandidate = (event) =>', m0)
        new_caller_handlers = """pc.onconnectionstatechange = () => {
      const cs = pc.connectionState;
      console.log('[WebRTC Outgoing ConnectionState]:', cs);
      if (cs === 'connected') {
        state.activeCall.webrtcConnected = true;
        stopNafaqTunnelStream();
        document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
      } else if (cs === 'disconnected' || cs === 'failed') {
        state.activeCall.webrtcConnected = false;
        if (typeof pc.restartIce === 'function') {
          try {
            console.log('[WebRTC Outgoing Dropped] Triggering self-healing ICE restart...');
            pc.restartIce();
          } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
        }
        state.activeCall.nafaqActive = true;
        document.getElementById('call-remote-status-text').textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
        startNafaqTunnelStream(peerId, stream, callType);
      }
    };

    pc.oniceconnectionstatechange = () => {
      const s = pc.iceConnectionState;
      console.log('[WebRTC Outgoing ICE State]:', s);
      if (s === 'connected' || s === 'completed') {
        state.activeCall.webrtcConnected = true;
        stopNafaqTunnelStream();
        document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
      } else if (s === 'disconnected') {
        console.warn('[WebRTC Outgoing ICE Disconnected] Attempting ICE restart...');
        if (typeof pc.restartIce === 'function') {
          try { pc.restartIce(); } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
        }
      } else if (s === 'failed') {
        console.warn('[WebRTC ICE Failed] Activating NAFAQ Sovereign Tunnel fallback!');
        state.activeCall.webrtcConnected = false;
        state.activeCall.nafaqActive = true;
        document.getElementById('call-remote-status-text').textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
        startNafaqTunnelStream(peerId, stream, callType);
      }
    };

    // Adaptive Watchdog: Avoid premature fallback while cellular/STUN checks are still in progress
    const armNafaqFallbackWatchdog = () => {
      if (state.activeCall.nafaqFallbackTimer) {
        clearTimeout(state.activeCall.nafaqFallbackTimer);
        state.activeCall.nafaqFallbackTimer = null;
      }
      state.activeCall.nafaqFallbackTimer = setTimeout(() => {
        const curPc = state.activeCall.pc;
        if (!curPc) return;
        const curIce = curPc.iceConnectionState;
        const curCs = curPc.connectionState;
        if (curIce === 'connected' || curIce === 'completed' || curCs === 'connected') return;
        if (curIce === 'checking' || curIce === 'new' || curCs === 'connecting') {
          // Keep waiting if ICE candidate checks are active
          state.activeCall.nafaqFallbackTimer = setTimeout(() => {
            const reIce = curPc.iceConnectionState;
            const reCs = curPc.connectionState;
            if (reIce !== 'connected' && reIce !== 'completed' && reCs !== 'connected') {
              console.log('[WebRTC Watchdog] Extended timeout reached — engaging NAFAQ Sovereign Tunneling!');
              state.activeCall.nafaqActive = true;
              const statusEl = document.getElementById('call-remote-status-text');
              if (statusEl) statusEl.textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
              startNafaqTunnelStream(peerId, stream, callType);
            }
          }, 6000);
          return;
        }
        console.log('[WebRTC Watchdog] ICE state is', curIce, '— engaging NAFAQ Sovereign Tunneling!');
        state.activeCall.nafaqActive = true;
        const statusEl = document.getElementById('call-remote-status-text');
        if (statusEl) statusEl.textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
        startNafaqTunnelStream(peerId, stream, callType);
      }, 8000);
    };
    armNafaqFallbackWatchdog();

    stream.getTracks().forEach(track => pc.addTrack(track, stream));

    pc.ontrack = (event) => {
      console.log('[WebRTC Outgoing] Received remote track:', event.track.kind, event.track.id);
      if (!state.activeCall.remoteStream) {
        state.activeCall.remoteStream = new MediaStream();
      }
      const canonical = state.activeCall.remoteStream;
      if (!canonical.getTracks().some(t => t.id === event.track.id)) {
        canonical.addTrack(event.track);
      }

      event.track.onended = () => {
        console.warn('[WebRTC Track Ended]:', event.track.kind);
        attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      };
      event.track.onunmute = () => {
        console.log('[WebRTC Track Unmuted]:', event.track.kind);
        attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      };

      attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      startCallTimer();
      document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
    };

    """
        content = content[:m0] + new_caller_handlers + content[end_m0:]
        print(" Patched startOutgoingCall handlers.")

        # Re-find match 1 for acceptIncomingCall after string length shift
        matches_after = [m.start() for m in re.finditer(r'pc\.onconnectionstatechange = \(\) =>', content)]
        m1 = matches_after[1]
        end_m1 = content.find('pc.onicecandidate = (event) =>', m1)
        new_callee_handlers = """pc.onconnectionstatechange = () => {
      const cs = pc.connectionState;
      console.log('[WebRTC Accept ConnectionState]:', cs);
      if (cs === 'connected') {
        state.activeCall.webrtcConnected = true;
        stopNafaqTunnelStream();
        if (!isCustomStreamCall) {
          document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
        }
      } else if (cs === 'disconnected' || cs === 'failed') {
        state.activeCall.webrtcConnected = false;
        if (typeof pc.restartIce === 'function') {
          try {
            console.log('[WebRTC Accept Dropped] Triggering self-healing ICE restart...');
            pc.restartIce();
          } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
        }
        state.activeCall.nafaqActive = true;
        if (!isCustomStreamCall) {
          document.getElementById('call-remote-status-text').textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
        }
        startNafaqTunnelStream(senderPeer, stream, callType);
      }
    };

    pc.oniceconnectionstatechange = () => {
      const s = pc.iceConnectionState;
      console.log('[WebRTC Accept ICE State]:', s);
      if (s === 'connected' || s === 'completed') {
        state.activeCall.webrtcConnected = true;
        stopNafaqTunnelStream();
        if (!isCustomStreamCall) {
          document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
        }
      } else if (s === 'disconnected') {
        console.warn('[WebRTC Accept ICE Disconnected] Attempting ICE restart...');
        if (typeof pc.restartIce === 'function') {
          try { pc.restartIce(); } catch (swallowedErr) { console.warn("[WyreSup Non-Fatal Notice]:", swallowedErr.message); }
        }
      } else if (s === 'failed') {
        console.warn('[WebRTC ICE Failed] Activating NAFAQ Sovereign Tunnel fallback!');
        state.activeCall.webrtcConnected = false;
        state.activeCall.nafaqActive = true;
        if (!isCustomStreamCall) {
          document.getElementById('call-remote-status-text').textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
        }
        startNafaqTunnelStream(senderPeer, stream, callType);
      }
    };

    if (!isCustomStreamCall) {
      // Adaptive Watchdog: Avoid premature fallback while cellular/STUN checks are still in progress
      const armNafaqFallbackWatchdog = () => {
        if (state.activeCall.nafaqFallbackTimer) {
          clearTimeout(state.activeCall.nafaqFallbackTimer);
          state.activeCall.nafaqFallbackTimer = null;
        }
        state.activeCall.nafaqFallbackTimer = setTimeout(() => {
          const curPc = state.activeCall.pc;
          if (!curPc) return;
          const curIce = curPc.iceConnectionState;
          const curCs = curPc.connectionState;
          if (curIce === 'connected' || curIce === 'completed' || curCs === 'connected') return;
          if (curIce === 'checking' || curIce === 'new' || curCs === 'connecting') {
            // Keep waiting if ICE candidate checks are active
            state.activeCall.nafaqFallbackTimer = setTimeout(() => {
              const reIce = curPc.iceConnectionState;
              const reCs = curPc.connectionState;
              if (reIce !== 'connected' && reIce !== 'completed' && reCs !== 'connected') {
                console.log('[WebRTC Watchdog] Extended timeout reached — engaging NAFAQ Sovereign Tunneling!');
                state.activeCall.nafaqActive = true;
                const statusEl = document.getElementById('call-remote-status-text');
                if (statusEl) statusEl.textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
                startNafaqTunnelStream(senderPeer, stream, callType);
              }
            }, 6000);
            return;
          }
          console.log('[WebRTC Watchdog] ICE state is', curIce, '— engaging NAFAQ Sovereign Tunneling!');
          state.activeCall.nafaqActive = true;
          const statusEl = document.getElementById('call-remote-status-text');
          if (statusEl) statusEl.textContent = ' NAFAQ Sovereign Tunnel Active (نَفَق مُبَاشِر مَحْمِيّ)';
          startNafaqTunnelStream(senderPeer, stream, callType);
        }, 8000);
      };
      armNafaqFallbackWatchdog();
    }

    stream.getTracks().forEach(track => pc.addTrack(track, stream));

    pc.ontrack = (event) => {
      console.log('[WebRTC Accept] Received remote track:', event.track.kind, event.track.id);
      if (!state.activeCall.remoteStream) {
        state.activeCall.remoteStream = new MediaStream();
      }
      const canonical = state.activeCall.remoteStream;
      if (!canonical.getTracks().some(t => t.id === event.track.id)) {
        canonical.addTrack(event.track);
      }

      event.track.onended = () => {
        console.warn('[WebRTC Track Ended]:', event.track.kind);
        attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      };
      event.track.onunmute = () => {
        console.log('[WebRTC Track Unmuted]:', event.track.kind);
        attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      };

      attachRemoteStreamToMediaElements(canonical, state.activeCall.type);
      startCallTimer();
      document.getElementById('call-remote-status-text').textContent = 'Direct WebRTC P2P Active (مُتَّصِل مُبَاشَرَة)';
    };

    """
        content = content[:m1] + new_callee_handlers + content[end_m1:]
        print(" Patched acceptIncomingCall handlers.")

    file_path.write_text(content, encoding="utf-8")
    print(f" Wrote patched file: {file_path}")
    return True

if __name__ == "__main__":
    patch_file(Path("/home/absolut7/Documents/news/wyresup-mesh-app/public/app.js"))
    patch_file(Path("/home/absolut7/Documents/news/wyresup-mesh-app/app.js"))

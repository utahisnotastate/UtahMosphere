# Voice Recipes

Custom voice intents, biometric calibration, and Voice Bridge extensions.

---

## Recipe: Calibrate and Claim Node

**Status:** Implemented

```bash
# Terminal 1 — kernel
python utahmosphere_os.py

# Terminal 2 — voice bridge
python voice_bridge.py
```

Speak clearly: **"Claim node"**

Verify:

```bash
curl http://127.0.0.1:8999/status | jq .claimed
# true
```

---

## Recipe: Deploy by Voice

| Say this | Result |
|----------|--------|
| "Deploy application my-app" | Creates tenant `my-app` |
| "Manifest app shop" | Same as deploy |
| "Patch app my-app to add logging" | Lazarus patch |
| "Status grid" | Returns registry JSON |

---

## Recipe: Programmatic Command Client

**Status:** Implemented

Template: [voice-command-client](../../templates/voice-command-client/)

```python
import json
import urllib.request

def send_command(transcript: str, acoustic_hash: str):
    payload = json.dumps({
        "transcript": transcript,
        "acoustic_hash": acoustic_hash,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8999/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

---

## Recipe: Custom Intent Handler (Voice Bridge Extension)

**Status:** Pattern (extend `voice_bridge.py`)

```python
# Add before capture_and_transmit_vibe() loop in voice_bridge.py

CUSTOM_INTENTS = {
    "go dark mode": lambda: print("[Vibe] Dark mode triggered"),
    "show grid": lambda: print("[Vibe] Opening dashboard"),
}

def handle_custom_intent(transcript: str) -> bool:
    lower = transcript.lower()
    for phrase, action in CUSTOM_INTENTS.items():
        if phrase in lower:
            action()
            return True
    return False

# In the listen loop, after recognize_google:
# if handle_custom_intent(transcript):
#     continue  # skip kernel POST for local-only intents
```

---

## Recipe: Extract Vibe-Print Hash (Testing)

**Status:** Implemented

Reuse Voice Bridge logic for consistent hashes:

```python
import hashlib
import numpy as np

def hash_from_mfcc_profile(profile_vector: np.ndarray) -> str:
    quantized = np.round(profile_vector, decimals=1).tobytes()
    return hashlib.sha256(quantized).hexdigest()
```

For dev/testing in open mode, use `acoustic_hash="0" * 64`.

---

## Recipe: Security Lockdown Recovery

If voice commands fail after claim:

1. Stop kernel
2. Backup and remove `security/biometric_ledger.json`
3. Restart — open mode restored
4. Re-claim with **"Claim node"**

See: [Access Control](../ACCESS_CONTROL.md)

Tutorial: [Kids First Robot Butler](../tutorials/01-kids-first-robot-butler.md)

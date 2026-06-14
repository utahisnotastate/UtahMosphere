# Voice-Controlled Dashboard — Starter Project

Web dashboard + deploy helper for UtahMosphere status.

## Dashboard

```bash
# Terminal 1 — kernel
python utahmosphere_os.py

# Terminal 2 — static server (avoids file:// CORS issues)
cd starter-projects/voice-controlled-dashboard
python -m http.server 3000
# Open http://127.0.0.1:3000
```

## Deploy and watch

```bash
python deploy_and_watch.py my-dashboard-app
```

Pair with `voice_bridge.py` for live voice commands.

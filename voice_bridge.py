#!/usr/bin/env python3
"""
UtahMosphere Voice Bridge - Biometric + Nonce-Signed Commands (v27.0)
Captures spoken intent, extracts Vibe-Print, auto-signs with GET /nonce.
"""

import sys
import json
import time
import hashlib
import urllib.request
import numpy as np

try:
    import speech_recognition as sr
    import librosa
except ImportError:
    print("[Critical] Ensure 'SpeechRecognition', 'pyaudio', 'numpy', and 'librosa' are installed.")
    sys.exit(1)

from voice_bridge_signed import get_signed_payload, KERNEL_URL

CORE_ENGINE_URL = f"{KERNEL_URL}/command"


def extract_biological_signature(audio_data: sr.AudioData) -> str:
    try:
        raw_bytes = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        audio_np = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        mfccs = librosa.feature.mfcc(y=audio_np, sr=16000, n_mfcc=13)
        profile_vector = np.mean(mfccs, axis=1)
        quantized_vector = np.round(profile_vector, decimals=1).tobytes()
        return hashlib.sha256(quantized_vector).hexdigest()
    except Exception as e:
        print(f"[Biometric Error] Could not extract signature: {e}")
        return "0" * 64


def capture_and_transmit_vibe():
    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except Exception as e:
        print(f"[Critical] Microphone not found: {e}")
        sys.exit(1)

    print("[Voice Bridge v27.0] Biometric sensors calibrated. Auto-nonce signing active.")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.5)

        while True:
            print("\n[Vibe] Listening...")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
                print("[Vibe] Processing temporal audio wave data...")
                transcript = recognizer.recognize_google(audio)
                vibe_print_hash = extract_biological_signature(audio)

                print(f"[Vibe] Intent: '{transcript}'")
                print(f"[Vibe] Biological Signature Hash: {vibe_print_hash[:16]}...")

                payload = get_signed_payload(
                    transcript,
                    vibe_print_hash,
                    use_server_nonce=True,
                    kernel_url=KERNEL_URL,
                )

                req = urllib.request.Request(
                    CORE_ENGINE_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    print(f"[System Manifestation]: {res_data.get('response')}")

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"[Bridge Error] Network degradation in local audio mesh: {e}")
            except Exception as e:
                print(f"[Bridge Exception] Hardware boundary anomaly: {e}")
                time.sleep(2)


if __name__ == "__main__":
    try:
        capture_and_transmit_vibe()
    except KeyboardInterrupt:
        print("\n[Voice Bridge] Shutting down link channels gracefully.")
        sys.exit(0)

#!/usr/bin/env python3
"""
UtahMosphere Voice Command Interface Client
Captures hardware microphone array arrays and transmits linguistic payloads
directly to the UtahMosphere Core API for rapid system state mutation.
"""

import sys
import json
import time
import urllib.request
# Note: speech_recognition requires 'SpeechRecognition' and 'PyAudio' or similar
try:
    import speech_recognition as sr
except ImportError:
    print("[Error] speech_recognition module not found. Please install via 'pip install SpeechRecognition'")
    sr = None

CORE_ENGINE_URL = "http://127.0.0.1:8999/command"

def capture_and_transmit_vibe():
    if sr is None:
        print("[Bridge] Speech Recognition library unavailable. Standing by.")
        return

    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except Exception as e:
        print(f"[Bridge Error] Could not access microphone: {e}")
        return

    print("[Voice Bridge] Peripheral Microphones Calibrated. Awaiting instruction, General.")
    
    with microphone as source:
        # Optimize matching profile based on ambient noise floors
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            print("\n[Vibe] Listening for system modification intent...")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
                print("[Vibe] Processing temporal audio wave data...")
                
                # Perform local text translation via quick response acoustic profiles
                transcript = recognizer.recognize_google(audio)
                print(f"[Vibe] Decoded Intent string: '{transcript}'")
                
                # Deliver intent structural instructions to the backend engine
                payload = json.dumps({"transcript": transcript}).encode('utf-8')
                
                req = urllib.request.Request(
                    CORE_ENGINE_URL, 
                    data=payload, 
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    print(f"[System Manifestation]: {res_data.get('response')}")
                    
            except sr.UnknownValueError:
                # Discard unrecognizable ambient noises calmly
                pass
            except sr.RequestError as e:
                print(f"[Bridge Error] Network degradation in local audio mesh: {e}")
            except Exception as e:
                print(f"[Bridge Exception] Matrix exception: {e}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        capture_and_transmit_vibe()
    except KeyboardInterrupt:
        print("\n[Voice Bridge] Shutting down link channels gracefully.")
        sys.exit(0)

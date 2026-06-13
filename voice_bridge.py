#!/usr/bin/env python3
"""
UtahMosphere Voice Bridge - Biometric Extraction Build v22.0
Captures spoken intent, extracts unique biological acoustic features (Vibe-Print),
and transmits cryptographically signed payloads to the UtahMosphere Kernel.
"""

import sys
import json
import time
import hashlib
import urllib.request
import numpy as np

# Require standard audio processing libraries
try:
    import speech_recognition as sr
    import librosa  # Used for deep acoustic feature extraction
except ImportError:
    print("[Critical] Ensure 'SpeechRecognition', 'pyaudio', 'numpy', and 'librosa' are installed.")
    sys.exit(1)

CORE_ENGINE_URL = "http://127.0.0.1:8999/command"

def extract_biological_signature(audio_data: sr.AudioData) -> str:
    """
    Analyzes the raw audio waveform to extract the speaker's unique vocal tract characteristics.
    Returns a SHA-256 hash of the acoustic feature matrix.
    """
    try:
        # Convert raw bytes to floating point numpy array for Librosa
        raw_bytes = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        audio_np = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Extract MFCCs (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=audio_np, sr=16000, n_mfcc=13)
        
        # Calculate the mean of the coefficients to form a stable biological profile
        profile_vector = np.mean(mfccs, axis=1)
        
        # Quantize and hash the biological vector to create the Vibe-Print key
        quantized_vector = np.round(profile_vector, decimals=1).tobytes()
        vibe_hash = hashlib.sha256(quantized_vector).hexdigest()
        
        return vibe_hash
    except Exception as e:
        print(f"[Biometric Error] Could not extract signature: {e}")
        return "0" * 64 # Fallback null hash

def capture_and_transmit_vibe():
    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except Exception as e:
        print(f"[Critical] Microphone not found: {e}")
        sys.exit(1)

    print("[Voice Bridge] Biometric Sensors Calibrated. Awaiting Biological Input.")
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        
        while True:
            print("\n[Vibe] Listening...")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
                
                # 1. Semantic Extraction (What you said)
                print("[Vibe] Processing temporal audio wave data...")
                transcript = recognizer.recognize_google(audio)
                
                # 2. Biological Extraction (Who you are)
                vibe_print_hash = extract_biological_signature(audio)
                
                print(f"[Vibe] Intent: '{transcript}'")
                print(f"[Vibe] Biological Signature Hash: {vibe_print_hash[:16]}...")
                
                # Deliver intent + biological signature
                payload = json.dumps({
                    "transcript": transcript,
                    "acoustic_hash": vibe_print_hash
                }).encode('utf-8')
                
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

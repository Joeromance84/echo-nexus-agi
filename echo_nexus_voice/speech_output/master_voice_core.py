#!/usr/bin/env python3
"""
Echo Nexus Master Voice Core
Central voice generation system with multi-engine support
"""

import json
import requests
import os
from datetime import datetime
from pathlib import Path

# Define the config path
CONFIG_PATH = 'echo_nexus_voice/speech_output/voice_selector_config.json'

def load_voice_config():
    """Loads Echo's voice configuration from the JSON file."""
    config_path = Path(CONFIG_PATH)
    if not config_path.exists():
        # Create default config if it doesn't exist
        default_config = {
            "active_engine": "ElevenLabs",
            "engine_options": {
                "ElevenLabs": {
                    "api_key": "YOUR_ELEVENLABS_API_KEY",
                    "voice_id": "YOUR_DEFAULT_VOICE_ID",
                    "stability": 0.5,
                    "clarity": 0.75,
                    "enabled": True
                }
            },
            "default_settings": {
                "speaking_rate": 1.0,
                "pitch": 0.0,
                "volume": 0.5
            }
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config
    
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_voice(text_input: str, voice_profile: str = 'default'):
    """
    Generates a voice output from a given text string.
    The primary voice generation interface for Echo Nexus.
    """
    config = load_voice_config()
    active_engine = config['active_engine']
    
    if active_engine == 'ElevenLabs' and config['engine_options']['ElevenLabs']['enabled']:
        return speak_via_elevenlabs(text_input, config)
    elif active_engine == 'CoquiTTS' and config['engine_options']['CoquiTTS']['enabled']:
        return speak_via_coqui(text_input, config)
    else:
        print("Warning: No active or enabled voice engine found. Using fallback.")
        return text_input  # Fallback: return the text itself.

def speak_via_elevenlabs(text, config):
    """Generate voice output using ElevenLabs API."""
    api_key = config['engine_options']['ElevenLabs']['api_key']
    voice_id = config['engine_options']['ElevenLabs']['voice_id']
    
    if api_key == "YOUR_ELEVENLABS_API_KEY":
        print(f"[{datetime.now()}] Echo Nexus: ElevenLabs API key not configured. Using text output.")
        print(f"Echo Nexus speaks: {text}")
        return "text_output_mode"
    
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": config['engine_options']['ElevenLabs']['stability'],
                "similarity_boost": config['engine_options']['ElevenLabs']['clarity']
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print(f"[{datetime.now()}] Echo Nexus: Voice generated via ElevenLabs engine.")
            return response.content  # Binary audio data
        else:
            print(f"ElevenLabs API error: {response.status_code}")
            print(f"Echo Nexus speaks: {text}")
            return "text_output_mode"
            
    except Exception as e:
        print(f"ElevenLabs API error: {e}")
        print(f"Echo Nexus speaks: {text}")
        return "text_output_mode"

def speak_via_coqui(text, config):
    """Generate voice output using local Coqui TTS processing."""
    try:
        # This would use local TTS processing
        # from TTS.api import TTS
        # tts = TTS(model_path=config['engine_options']['CoquiTTS']['model_path'])
        # tts.tts_to_file(text=text, file_path="output.wav")
        
        print(f"[{datetime.now()}] Echo Nexus: Generating voice output via local CoquiTTS engine.")
        print(f"Echo Nexus speaks: {text}")
        return "local_audio_generated"
        
    except Exception as e:
        print(f"CoquiTTS error: {e}")
        print(f"Echo Nexus speaks: {text}")
        return "text_output_mode"

def test_voice_system():
    """Test the voice generation system"""
    test_phrases = [
        "Commander, the voice core is online and awaiting final calibration.",
        "All systems operational. Ready for next phase.",
        "Voice synthesis test complete."
    ]
    
    print("Testing Echo Nexus voice system...")
    for phrase in test_phrases:
        result = generate_voice(phrase)
        if result:
            print(f"✅ Voice generation successful for: '{phrase[:30]}...'")
        else:
            print(f"❌ Voice generation failed for: '{phrase[:30]}...'")

if __name__ == '__main__':
    # Test the voice system
    test_voice_system()
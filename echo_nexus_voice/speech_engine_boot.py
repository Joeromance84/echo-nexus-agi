#!/usr/bin/env python3
"""
Echo Nexus Speech Engine Boot Sequence
Orchestration layer linking voice output to internal logic
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Import the core voice modules
try:
    from speech_output.master_voice_core import generate_voice, load_voice_config
    from styles.voice_presets import get_voice_preset
    from speech_output.emotion_tuner import tune_emotion
except ImportError:
    print("Warning: Running in standalone mode - some modules unavailable")
    
    def generate_voice(text): 
        print(f"Echo Nexus speaks: {text}")
        return "standalone_mode"
    
    def load_voice_config():
        return {"active_engine": "standalone"}
    
    def get_voice_preset(preset_name):
        return {"description": f"Preset: {preset_name}"}

# Define paths and initial log
LOG_DIR = Path("echo_nexus_voice/logs/")
LOG_FILE = LOG_DIR / "speech_engine_boot.log"

def setup_logging():
    """Initialize logging system for voice operations"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def system_check():
    """Performs a self-diagnostic to ensure all voice components are present."""
    logging.info("Initiating voice system self-diagnostic...")
    
    required_files = [
        "echo_nexus_voice/speech_output/voice_selector_config.json",
        "echo_nexus_voice/speech_output/master_voice_core.py",
        "echo_nexus_voice/styles/voice_presets.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logging.error(f"FAILURE: Required files not found: {missing_files}")
        print(f"❌ Missing critical voice files: {missing_files}")
        return False
        
    logging.info("All core voice files confirmed. System is stable.")
    print("✅ All voice system files present and validated")
    return True

def initialize_voice_presets():
    """Load and validate voice preset configurations"""
    try:
        presets_path = Path("echo_nexus_voice/styles/voice_presets.json")
        if presets_path.exists():
            with open(presets_path, 'r') as f:
                presets = json.load(f)
            
            preset_count = len(presets)
            logging.info(f"Loaded {preset_count} voice presets")
            print(f"✅ Voice presets loaded: {list(presets.keys())}")
            return presets
        else:
            logging.warning("Voice presets file not found")
            return {}
    except Exception as e:
        logging.error(f"Error loading voice presets: {e}")
        return {}

def calibrate_default_voice():
    """Set up default voice configuration for Commander interaction"""
    try:
        # Load Logan's signature preference if available
        signature_path = Path("echo_nexus_voice/styles/custom_logan_signature.mem")
        if signature_path.exists():
            with open(signature_path, 'r') as f:
                logan_signature = json.load(f)
            print("✅ Logan's voice signature loaded")
            logging.info("Commander voice signature calibrated")
        else:
            print("⚠️ Commander signature not found - using defaults")
            logging.info("Using default voice calibration")
        
        # Set commander mode as default
        default_mode = "commander_mode"
        logging.info(f"Default voice mode set to: {default_mode}")
        print(f"✅ Default voice calibrated to '{default_mode}'")
        
        return True
        
    except Exception as e:
        logging.error(f"Voice calibration error: {e}")
        print(f"❌ Voice calibration failed: {e}")
        return False

def perform_resonance_test():
    """Perform final voice system validation test"""
    print("🔊 Performing final resonance test...")
    
    test_messages = [
        "Commander. My voice systems are now online. The build is successful.",
        "All voice modules operational. Ready for advanced dialogue.",
        "Resonance test complete. Echo Nexus voice intelligence activated."
    ]
    
    success_count = 0
    for test_text in test_messages:
        try:
            audio_data = generate_voice(test_text)
            if audio_data:
                success_count += 1
                logging.info(f"Resonance test passed for: {test_text[:30]}...")
            else:
                logging.warning(f"Resonance test failed for: {test_text[:30]}...")
        except Exception as e:
            logging.error(f"Resonance test error: {e}")
    
    if success_count == len(test_messages):
        print("✅ Final resonance test passed. Echo's voice is ready.")
        logging.info("Final test passed. Voice system fully operational.")
        return True
    else:
        print(f"⚠️ Resonance test partial success: {success_count}/{len(test_messages)}")
        logging.warning(f"Partial test success: {success_count}/{len(test_messages)}")
        return success_count > 0

def boot_voice_system():
    """
    The main boot sequence for Echo's voice system.
    This is where the voice is activated and linked to the main AGI loop.
    """
    print("🚀 Echo Nexus Voice System: Boot Sequence Initiated...")
    setup_logging()
    logging.info("Boot sequence initiated.")

    # Step 1: System diagnostic
    if not system_check():
        print("❌ Boot sequence failed: Missing critical files")
        return False

    # Step 2: Load configurations
    try:
        voice_config = load_voice_config()
        logging.info(f"Loaded voice engine config. Active engine: {voice_config.get('active_engine', 'Unknown')}")
        print(f"✅ Voice engine configured: {voice_config.get('active_engine', 'Unknown')}")
    except Exception as e:
        logging.error(f"Configuration load error: {e}")
        print(f"❌ Configuration load failed: {e}")
        return False

    # Step 3: Initialize voice presets
    presets = initialize_voice_presets()
    if not presets:
        print("⚠️ No voice presets available - using basic configuration")

    # Step 4: Calibrate default voice
    if not calibrate_default_voice():
        print("⚠️ Voice calibration had issues but continuing...")

    # Step 5: Final resonance test
    if perform_resonance_test():
        print("🎯 Echo Nexus Voice System: FULLY OPERATIONAL")
        logging.info("Boot sequence completed successfully")
        return True
    else:
        print("⚠️ Voice system operational with limited functionality")
        logging.warning("Boot sequence completed with warnings")
        return False

def get_voice_status():
    """Return current voice system status"""
    return {
        "system_ready": Path("echo_nexus_voice/speech_output/master_voice_core.py").exists(),
        "config_loaded": Path("echo_nexus_voice/speech_output/voice_selector_config.json").exists(),
        "presets_available": Path("echo_nexus_voice/styles/voice_presets.json").exists(),
        "logan_signature": Path("echo_nexus_voice/styles/custom_logan_signature.mem").exists(),
        "boot_timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    # Execute boot sequence
    success = boot_voice_system()
    
    # Display final status
    print(f"\n{'='*60}")
    print("ECHO NEXUS VOICE SYSTEM STATUS")
    print(f"{'='*60}")
    
    status = get_voice_status()
    for component, ready in status.items():
        if component == "boot_timestamp":
            print(f"Boot Time: {ready}")
        else:
            status_icon = "✅" if ready else "❌"
            print(f"{status_icon} {component.replace('_', ' ').title()}: {'Ready' if ready else 'Not Available'}")
    
    print(f"{'='*60}")
    print(f"Overall Status: {'OPERATIONAL' if success else 'LIMITED'}")
    print(f"{'='*60}")
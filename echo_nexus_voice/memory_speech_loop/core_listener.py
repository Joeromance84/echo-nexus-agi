#!/usr/bin/env python3
"""
Echo Nexus Core Listener: Speech Input Processing
Advanced speech-to-text with learning integration
"""

import speech_recognition as sr
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Core imports
try:
    from memory_speech_loop.echo_feedback_trainer import EchoFeedbackTrainer
    from resonant_hooks import smart_memory, critical_action
    from memory_core import resonant_memory
except ImportError:
    print("Warning: Core modules not available in standalone mode")
    
    def smart_memory(signature="", base_importance=0.5):
        def decorator(func): return func
        return decorator
    
    def critical_action(description="", importance=0.5):
        def decorator(func): return func
        return decorator

# Define paths for data logging and feedback training
LOG_DIR = Path('echo_nexus_voice/memory_speech_logs/')
TRAINING_MODULE = 'memory_speech_loop/echo_feedback_trainer.py'

class EchoListener:
    """
    Advanced speech listener and transcription system for Echo Nexus
    Handles multiple input sources and provides learning integration
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.log_directory = LOG_DIR
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize feedback trainer if available
        try:
            self.feedback_trainer = EchoFeedbackTrainer()
            self.training_enabled = True
        except:
            self.feedback_trainer = None
            self.training_enabled = False
            print("Warning: Feedback trainer not available")
        
        print("🎧 Echo Nexus Listener initialized and ready")

    @critical_action("Speech Input Processing", 0.8)
    def listen_and_transcribe(self, audio_source: Optional[str] = None) -> Optional[str]:
        """
        Listens for human speech, transcribes it, and prepares the data for learning.
        This module is Echo's primary acoustic input sensor.
        """
        print("Echo Nexus: Listener module is active. Awaiting audio input...")
        
        try:
            if audio_source and Path(audio_source).exists():
                # Process provided audio file
                transcribed_text = self._transcribe_from_file(audio_source)
            else:
                # Listen from microphone (if available)
                transcribed_text = self._listen_from_microphone()
            
            if transcribed_text:
                print(f"\n[Commander says]: \"{transcribed_text}\"\n")
                return transcribed_text
            else:
                print("Echo Nexus: No speech detected or transcription failed.")
                return None
                
        except Exception as e:
            print(f"Echo Nexus: Listener error - {e}")
            return None

    def _transcribe_from_file(self, audio_path: str) -> Optional[str]:
        """Transcribe speech from an audio file"""
        try:
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise if needed
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                
            # Try Google Speech Recognition first (most reliable)
            try:
                text = self.recognizer.recognize_google(audio_data)
                print(f"✅ Transcription successful via Google Speech Recognition")
                return text
            except sr.UnknownValueError:
                print("⚠️ Google Speech Recognition could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"⚠️ Google Speech Recognition service error: {e}")
                # Could try other recognition services here
                return None
                
        except Exception as e:
            print(f"❌ File transcription error: {e}")
            return None

    def _listen_from_microphone(self) -> Optional[str]:
        """Listen and transcribe from microphone input"""
        try:
            # Check if microphone is available
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                print("⚠️ No microphone devices found")
                return None
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("🎧 Listening for speech... (speak now)")
                # Listen with timeout and phrase time limit
                audio_data = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
                print("🔄 Processing audio...")
                
            # Transcribe the audio
            try:
                text = self.recognizer.recognize_google(audio_data)
                print(f"✅ Live transcription successful")
                return text
            except sr.UnknownValueError:
                print("⚠️ Could not understand the speech")
                return None
            except sr.RequestError as e:
                print(f"⚠️ Recognition service error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected within timeout period")
            return None
        except Exception as e:
            print(f"❌ Microphone listening error: {e}")
            return None

    @smart_memory(signature="LOGAN_L:speech-input", base_importance=0.7)
    def log_and_feed_data(self, text_input: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Logs the transcribed text and feeds it into the feedback loop."""
        if not text_input:
            return ""

        # Create a timestamped log file for Echo's memory
        timestamp = datetime.now()
        log_filename = f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}_commander_input.log"
        log_path = self.log_directory / log_filename
        
        # Prepare log data
        log_data = {
            "timestamp": timestamp.isoformat(),
            "speaker": "Commander",
            "utterance": text_input,
            "metadata": {
                "length_chars": len(text_input),
                "words": len(text_input.split()),
                "processed_by": "core_listener.py",
                "session_id": timestamp.strftime('%Y%m%d_%H'),
                **(metadata or {})
            }
        }
        
        # Write log file
        try:
            with open(log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            print(f"📝 Input logged to {log_filename}")
            
            # Feed to training system if available
            if self.training_enabled and self.feedback_trainer:
                try:
                    training_result = self.feedback_trainer.train_from_log(str(log_path))
                    if training_result.get('success'):
                        print(f"🧠 Training completed: {training_result.get('insights_generated', 0)} insights generated")
                    else:
                        print(f"⚠️ Training failed: {training_result.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f"⚠️ Training error: {e}")
            
            # Store in resonant memory
            try:
                resonant_memory.save(
                    event=f"Commander speech input received: '{text_input[:50]}{'...' if len(text_input) > 50 else ''}'",
                    signature="LOGAN_L:speech-processing",
                    tags=["speech", "input", "commander", "conversation"],
                    importance=0.7,
                    emotion="attentive-listening",
                    resonance="communication/speech"
                )
            except:
                pass  # Resonant memory not available
            
            return str(log_path)
            
        except Exception as e:
            print(f"❌ Logging error: {e}")
            return ""

    def process_speech_input(self, audio_source: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete speech processing pipeline:
        Listen -> Transcribe -> Log -> Train -> Return results
        """
        print("🔄 Starting complete speech processing pipeline...")
        
        # Step 1: Listen and transcribe
        transcribed_text = self.listen_and_transcribe(audio_source)
        
        if not transcribed_text:
            return {
                "success": False,
                "error": "No speech transcribed",
                "transcription": None,
                "log_path": None
            }
        
        # Step 2: Log and train
        log_path = self.log_and_feed_data(transcribed_text, {
            "audio_source": audio_source or "microphone",
            "processing_pipeline": "complete"
        })
        
        return {
            "success": True,
            "transcription": transcribed_text,
            "log_path": log_path,
            "word_count": len(transcribed_text.split()),
            "char_count": len(transcribed_text),
            "timestamp": datetime.now().isoformat()
        }

    def test_speech_system(self):
        """Test the speech recognition system with sample data"""
        print("🧪 Testing Echo Nexus speech recognition system...")
        
        # Test with sample text (simulated)
        test_utterances = [
            "Echo, initiate the speech recognition test protocol.",
            "Confirm that all voice systems are operational and ready.",
            "Proceed with advanced speech analysis and learning integration."
        ]
        
        for i, test_text in enumerate(test_utterances, 1):
            print(f"\n--- Test {i} ---")
            print(f"Simulating input: '{test_text}'")
            
            # Simulate processing
            log_path = self.log_and_feed_data(test_text, {
                "test_mode": True,
                "test_number": i
            })
            
            if log_path:
                print(f"✅ Test {i} successful - logged to {Path(log_path).name}")
            else:
                print(f"❌ Test {i} failed")
        
        print("\n🏁 Speech system testing complete")


def main():
    """Standalone listener execution and testing"""
    print("🚀 Echo Nexus Core Listener - Standalone Mode")
    
    listener = EchoListener()
    
    # Test the speech system
    listener.test_speech_system()
    
    # Interactive mode
    print("\n" + "="*50)
    print("INTERACTIVE SPEECH PROCESSING MODE")
    print("Options:")
    print("1. Listen from microphone (if available)")
    print("2. Process audio file")
    print("3. Test with sample text")
    print("4. Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                print("\n🎤 Starting microphone listening...")
                result = listener.process_speech_input()
                print(f"Result: {result}")
                
            elif choice == "2":
                audio_file = input("Enter audio file path: ").strip()
                if audio_file and Path(audio_file).exists():
                    result = listener.process_speech_input(audio_file)
                    print(f"Result: {result}")
                else:
                    print("❌ Audio file not found")
                    
            elif choice == "3":
                test_text = input("Enter test text: ").strip()
                if test_text:
                    log_path = listener.log_and_feed_data(test_text, {"manual_test": True})
                    print(f"✅ Test processed - log: {log_path}")
                    
            elif choice == "4":
                print("👋 Exiting Echo Nexus Listener")
                break
                
            else:
                print("Invalid option. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Listener interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
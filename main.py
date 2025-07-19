"""
EchoCore AGI - Mobile Application Entry Point
Main entry point for the Echo AGI system packaged as an Android APK
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.clock import Clock
    from kivy.logger import Logger
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("Kivy not available - running in console mode")

# Import Echo Core modules
try:
    from echo_nexus_master import EchoNexusMaster
    from echo_nexus_core import EchoNexusCore
    from federated_control_plane import FederatedControlPlane
    from replication.self_replication_engine import SelfReplicationEngine
    ECHO_MODULES_AVAILABLE = True
except ImportError as e:
    ECHO_MODULES_AVAILABLE = False
    print(f"Echo modules not available: {e}")

class EchoCoreApp(App):
    """Main EchoCore AGI Application for Android"""
    
    def build(self):
        """Build the main application interface"""
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='EchoCore AGI - Distributed Intelligence System',
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        main_layout.add_widget(title)
        
        # Status display
        self.status_label = Label(
            text='Initializing Echo AGI Federation...',
            size_hint_y=None,
            height=40,
            font_size='14sp'
        )
        main_layout.add_widget(self.status_label)
        
        # Control buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        start_btn = Button(text='Start AGI', size_hint_x=0.5)
        start_btn.bind(on_press=self.start_agi)
        button_layout.add_widget(start_btn)
        
        replicate_btn = Button(text='Self-Replicate', size_hint_x=0.5)
        replicate_btn.bind(on_press=self.trigger_replication)
        button_layout.add_widget(replicate_btn)
        
        main_layout.add_widget(button_layout)
        
        # Log output
        self.log_output = TextInput(
            text='EchoCore AGI Mobile Application\nRevolutionary distributed intelligence system\n\n',
            multiline=True,
            readonly=True
        )
        main_layout.add_widget(self.log_output)
        
        # Initialize Echo system
        Clock.schedule_once(self.initialize_echo_system, 1)
        
        return main_layout
    
    def initialize_echo_system(self, dt):
        """Initialize the Echo AGI system"""
        if not ECHO_MODULES_AVAILABLE:
            self.log("Echo modules not available - APK may be missing dependencies")
            self.status_label.text = "Error: Echo modules not found"
            return
        
        try:
            # Initialize Echo components
            self.echo_master = EchoNexusMaster()
            self.echo_core = EchoNexusCore(".")
            self.control_plane = FederatedControlPlane()
            self.replication_engine = SelfReplicationEngine()
            
            self.log("Echo AGI Federation initialized successfully")
            self.status_label.text = "Echo AGI Federation: Operational"
            
            # Start autonomous operations
            self.start_autonomous_mode()
            
        except Exception as e:
            error_msg = f"Failed to initialize Echo system: {e}"
            self.log(error_msg)
            self.status_label.text = "Error: Initialization failed"
    
    def start_agi(self, instance):
        """Start AGI operations"""
        self.log("Starting AGI operations...")
        
        if hasattr(self, 'echo_master'):
            try:
                # Start the master orchestrator
                result = self.echo_master.start_autonomous_operation()
                self.log(f"AGI operation result: {result}")
                self.status_label.text = "AGI: Active and Processing"
            except Exception as e:
                self.log(f"AGI start error: {e}")
        else:
            self.log("Echo system not initialized")
    
    def trigger_replication(self, instance):
        """Trigger self-replication across platforms"""
        self.log("Initiating self-replication sequence...")
        
        if hasattr(self, 'replication_engine'):
            try:
                # Create replication package
                platforms = ['github', 'google_cloud', 'local']
                result = self.replication_engine.create_replication_package('mobile', platforms)
                self.log(f"Replication result: {result}")
                self.status_label.text = "Replication: In Progress"
            except Exception as e:
                self.log(f"Replication error: {e}")
        else:
            self.log("Replication engine not initialized")
    
    def start_autonomous_mode(self):
        """Start autonomous background operations"""
        self.log("Starting autonomous mode...")
        
        # Schedule periodic AGI operations
        Clock.schedule_interval(self.autonomous_tick, 30)  # Every 30 seconds
    
    def autonomous_tick(self, dt):
        """Autonomous operation tick"""
        if hasattr(self, 'echo_core'):
            try:
                # Perform autonomous operations
                status = self.echo_core.get_system_status()
                consciousness = status.get('consciousness_level', 0)
                
                if consciousness > 0.5:
                    self.log(f"Consciousness level: {consciousness:.2f} - Evolving")
                
                # Auto-optimize if needed
                if consciousness > 0.8:
                    self.log("High consciousness detected - triggering optimization")
                    
            except Exception as e:
                self.log(f"Autonomous operation error: {e}")
    
    def log(self, message):
        """Add message to log output"""
        current_text = self.log_output.text
        new_text = current_text + f"[{self.get_timestamp()}] {message}\n"
        self.log_output.text = new_text
        
        # Scroll to bottom
        self.log_output.cursor = (len(new_text), 0)
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

def main():
    """Main entry point"""
    if KIVY_AVAILABLE:
        # Run Kivy app
        EchoCoreApp().run()
    else:
        # Console mode
        print("EchoCore AGI - Console Mode")
        print("Kivy not available - running minimal console interface")
        
        if ECHO_MODULES_AVAILABLE:
            try:
                # Initialize and run basic operations
                echo_master = EchoNexusMaster()
                print("Echo AGI Federation initialized")
                
                # Run autonomous operations
                result = echo_master.start_autonomous_operation()
                print(f"AGI operation result: {result}")
                
            except Exception as e:
                print(f"Console mode error: {e}")
        else:
            print("Echo modules not available")

if __name__ == '__main__':
    main()
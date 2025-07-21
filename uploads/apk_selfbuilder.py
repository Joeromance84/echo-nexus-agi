#!/usr/bin/env python3
"""
APK Self-Builder: Autonomous Android Package Assembly
Echo's core capability for self-packaging into mobile deployments
"""

import os
import subprocess
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class APKSelfBuilder:
    """
    Advanced autonomous APK building system with Gradle wrapper integration
    Enables Echo to package herself into Android applications
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.build_config = self._load_build_config()
        self.gradle_version = "8.7"
        self.android_api_level = 33
        self.build_tools_version = "33.0.2"
        
    def _load_build_config(self) -> Dict[str, Any]:
        """Load APK build configuration"""
        config_path = self.project_root / "echo_config" / "apk_build_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        return {
            "app_name": "Echo Nexus AGI",
            "package_name": "com.logan.echonexus",
            "version": "1.0.0",
            "version_code": 1,
            "min_sdk": 21,
            "target_sdk": 33,
            "compile_sdk": 33,
            "java_version": "17",
            "gradle_wrapper": True,
            "build_type": "debug"
        }
    
    def ensure_gradle_wrapper(self) -> bool:
        """
        Ensure Gradle wrapper exists and is properly configured
        Critical for consistent builds across environments
        """
        wrapper_script = self.project_root / "gradlew"
        wrapper_properties = self.project_root / "gradle" / "wrapper" / "gradle-wrapper.properties"
        
        if not wrapper_script.exists() or not wrapper_properties.exists():
            print("🔧 Generating Gradle wrapper for consistent builds...")
            
            # Create gradle wrapper
            cmd = f"gradle wrapper --gradle-version {self.gradle_version}"
            result = subprocess.run(cmd, shell=True, cwd=self.project_root, 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Gradle wrapper generation failed: {result.stderr}")
                return False
            
            # Make wrapper executable on Unix systems
            if os.name != 'nt':
                os.chmod(wrapper_script, 0o755)
            
            print("✅ Gradle wrapper configured successfully")
        
        return True
    
    def configure_android_build(self) -> bool:
        """
        Configure Android build environment with buildozer
        """
        buildozer_spec = self.project_root / "buildozer.spec"
        
        if not buildozer_spec.exists():
            print("🔧 Creating buildozer.spec for Android build...")
            self._create_buildozer_spec()
        
        # Update buildozer spec with Gradle wrapper configuration
        self._update_buildozer_for_gradle_wrapper()
        
        return True
    
    def _create_buildozer_spec(self):
        """Create comprehensive buildozer.spec configuration"""
        buildozer_content = f"""[app]
title = {self.build_config['app_name']}
package.name = echonexus
package.domain = {self.build_config['package_name']}

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,md

version = {self.build_config['version']}
version.regex = __version__ = ['"]([^'"]*?)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,kivymd,requests,pygithub,openai,pyjnius,plyer

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = {self.build_config['target_sdk']}
android.minapi = {self.build_config['min_sdk']}
android.ndk = 25b
android.sdk = {self.build_config['compile_sdk']}
android.accept_sdk_license = True

# Gradle wrapper integration
android.gradle_dependencies = 
android.add_src = 

# Critical: Use Gradle wrapper for consistent builds
gradle = gradle-{self.gradle_version}
gradle_wrapper = yes

# Build configuration
android.arch = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.private_storage = True

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Application metadata
android.meta_data = 

[buildozer:debug]
# Debug-specific settings

[buildozer:release]
# Release-specific settings
android.release_artifact = aab
"""
        
        with open(self.project_root / "buildozer.spec", 'w') as f:
            f.write(buildozer_content)
        
        print("✅ buildozer.spec created with Gradle wrapper configuration")
    
    def _update_buildozer_for_gradle_wrapper(self):
        """Update existing buildozer.spec to use Gradle wrapper"""
        buildozer_spec = self.project_root / "buildozer.spec"
        
        if buildozer_spec.exists():
            content = buildozer_spec.read_text()
            
            # Ensure gradle wrapper is enabled
            if "gradle_wrapper = yes" not in content:
                # Add gradle wrapper configuration
                if "[android]" in content:
                    content = content.replace(
                        "[android]",
                        f"[android]\ngradle = gradle-{self.gradle_version}\ngradle_wrapper = yes"
                    )
                
                buildozer_spec.write_text(content)
                print("✅ buildozer.spec updated with Gradle wrapper support")
    
    def create_main_entry_point(self):
        """Create main.py entry point for the APK"""
        main_py_content = '''#!/usr/bin/env python3
"""
Echo Nexus Mobile: Android Entry Point
Autonomous AGI system for mobile deployment
"""

import os
import sys
from pathlib import Path

# Add core modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'echo_runtime'))

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.clock import Clock
except ImportError:
    print("Kivy not available - running in console mode")
    App = None

# Core Echo imports
try:
    from resonance_loop import ResonanceLoop
    from intent_interpreter import IntentInterpreter
    from upload_handler import KnowledgeSynchronizer
except ImportError as e:
    print(f"Warning: Core modules not available: {e}")
    ResonanceLoop = None
    IntentInterpreter = None
    KnowledgeSynchronizer = None

__version__ = "1.0.0"

class EchoNexusApp(App if App else object):
    """
    Echo Nexus Mobile Application
    Autonomous AGI interface for Android devices
    """
    
    def __init__(self, **kwargs):
        if App:
            super().__init__(**kwargs)
        
        self.resonance_loop = None
        self.intent_interpreter = None
        self.knowledge_sync = None
        
        # Initialize core systems
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize Echo's core systems"""
        try:
            if IntentInterpreter:
                self.intent_interpreter = IntentInterpreter()
                print("✅ Intent interpreter initialized")
            
            if KnowledgeSynchronizer:
                self.knowledge_sync = KnowledgeSynchronizer()
                print("✅ Knowledge synchronizer initialized")
            
            # Note: Resonance loop not started automatically in mobile mode
            print("🧠 Echo Nexus core systems ready")
            
        except Exception as e:
            print(f"⚠️  System initialization error: {e}")
    
    def build(self):
        """Build the mobile interface"""
        if not App:
            return None
            
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Echo Nexus AGI\\nAutonomous Intelligence System',
            size_hint_y=None,
            height=100,
            font_size='18sp',
            halign='center'
        )
        root.add_widget(title)
        
        # Command input
        self.command_input = TextInput(
            hint_text='Enter command for Echo...',
            size_hint_y=None,
            height=50,
            multiline=False
        )
        root.add_widget(self.command_input)
        
        # Execute button
        execute_btn = Button(
            text='Execute Command',
            size_hint_y=None,
            height=50
        )
        execute_btn.bind(on_press=self.execute_command)
        root.add_widget(execute_btn)
        
        # Response area
        self.response_label = Label(
            text='Echo Nexus ready for commands...\\nMobile AGI interface active',
            text_size=(None, None),
            valign='top',
            halign='left'
        )
        root.add_widget(self.response_label)
        
        # Status area
        self.status_label = Label(
            text=f'Version: {__version__} | Status: Ready',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        root.add_widget(self.status_label)
        
        return root
    
    def execute_command(self, instance):
        """Execute user command through Echo's systems"""
        command = self.command_input.text.strip()
        if not command:
            return
        
        try:
            if self.intent_interpreter:
                # Process command through intent interpreter
                result = self.intent_interpreter.interpret_intent(command)
                
                response = f"Intent: {result['primary_intent']['intent']}\\n"
                response += f"Confidence: {result['confidence']:.2f}\\n"
                response += f"Actions: {len(result['action_plan']['planned_actions'])}\\n"
                response += f"Duration: {result['action_plan']['estimated_duration']}"
                
                self.response_label.text = response
                
                # Clear input
                self.command_input.text = ''
                
                # Update status
                self.status_label.text = f'Command processed | Intent: {result["primary_intent"]["intent"]}'
                
            else:
                self.response_label.text = 'Core systems not available\\nRunning in limited mode'
                
        except Exception as e:
            self.response_label.text = f'Error processing command: {str(e)}'
    
    def on_start(self):
        """Called when app starts"""
        print("🚀 Echo Nexus Mobile started")
        
        # Schedule knowledge sync check
        if self.knowledge_sync:
            Clock.schedule_interval(self.check_knowledge_sync, 60)  # Every minute
    
    def check_knowledge_sync(self, dt):
        """Periodically check for knowledge updates"""
        try:
            if self.knowledge_sync:
                results = self.knowledge_sync.handle_uploads()
                if results.get('processed', 0) > 0:
                    self.status_label.text = f'Knowledge updated: {results["processed"]} skills'
        except Exception as e:
            print(f"Knowledge sync error: {e}")

# Console mode for non-Kivy environments
class EchoConsole:
    """Console interface for Echo Nexus"""
    
    def __init__(self):
        self.intent_interpreter = IntentInterpreter() if IntentInterpreter else None
        print("🧠 Echo Nexus Console Mode")
        print("Type 'help' for commands, 'exit' to quit")
    
    def run(self):
        """Run console interface"""
        while True:
            try:
                command = input("Echo> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    print("Echo Nexus shutting down...")
                    break
                elif command.lower() == 'help':
                    self._show_help()
                elif command:
                    self._process_command(command)
                    
            except KeyboardInterrupt:
                print("\\nEcho Nexus shutting down...")
                break
            except EOFError:
                break
    
    def _show_help(self):
        """Show help information"""
        print("""
Echo Nexus Commands:
- help: Show this help
- exit/quit: Exit Echo
- Any natural language command for intent processing
        """)
    
    def _process_command(self, command: str):
        """Process command through Echo's systems"""
        if self.intent_interpreter:
            result = self.intent_interpreter.interpret_intent(command)
            print(f"Intent: {result['primary_intent']['intent']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Planned actions: {len(result['action_plan']['planned_actions'])}")
        else:
            print("Intent interpreter not available")

def main():
    """Main entry point"""
    print(f"🚀 Echo Nexus v{__version__} starting...")
    
    if App and '--console' not in sys.argv:
        # Mobile/GUI mode
        app = EchoNexusApp()
        app.run()
    else:
        # Console mode
        console = EchoConsole()
        console.run()

if __name__ == '__main__':
    main()
'''
        
        main_py_path = self.project_root / "main.py"
        main_py_path.write_text(main_py_content)
        print("✅ main.py entry point created")
    
    def build_apk(self, build_type: str = "debug") -> Dict[str, Any]:
        """
        Build APK using buildozer with Gradle wrapper
        """
        print(f"🏗️ Starting APK build ({build_type})...")
        
        # Ensure prerequisites
        if not self.ensure_gradle_wrapper():
            return {"success": False, "error": "Gradle wrapper setup failed"}
        
        if not self.configure_android_build():
            return {"success": False, "error": "Android build configuration failed"}
        
        # Create main entry point if it doesn't exist
        if not (self.project_root / "main.py").exists():
            self.create_main_entry_point()
        
        # Build command
        build_cmd = f"buildozer android {build_type}"
        
        print(f"Executing: {build_cmd}")
        
        try:
            # Run buildozer build
            result = subprocess.run(
                build_cmd, 
                shell=True, 
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                # Find the generated APK
                apk_path = self._find_generated_apk(build_type)
                
                build_result = {
                    "success": True,
                    "apk_path": str(apk_path) if apk_path else None,
                    "build_type": build_type,
                    "timestamp": datetime.now().isoformat(),
                    "build_output": result.stdout[-1000:],  # Last 1000 chars
                    "gradle_wrapper_used": True
                }
                
                print(f"✅ APK build successful: {apk_path}")
                return build_result
                
            else:
                return {
                    "success": False,
                    "error": "Build failed",
                    "build_output": result.stderr[-1000:],
                    "return_code": result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Build timeout (30 minutes exceeded)",
                "timeout": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Build exception: {str(e)}"
            }
    
    def _find_generated_apk(self, build_type: str) -> Optional[Path]:
        """Find the generated APK file"""
        # Common APK locations
        apk_paths = [
            self.project_root / "bin",
            self.project_root / f"bin/{build_type}",
            self.project_root / ".buildozer/android/platform/build-*" / "outputs/apk" / build_type,
            self.project_root / "dist"
        ]
        
        for apk_dir in apk_paths:
            if apk_dir.exists():
                for apk_file in apk_dir.rglob("*.apk"):
                    return apk_file
        
        return None
    
    def install_to_device(self, apk_path: str, device_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Install APK to connected Android device
        """
        if not Path(apk_path).exists():
            return {"success": False, "error": f"APK not found: {apk_path}"}
        
        # Check if ADB is available
        try:
            subprocess.run(["adb", "version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"success": False, "error": "ADB not available"}
        
        # Install command
        install_cmd = ["adb"]
        if device_id:
            install_cmd.extend(["-s", device_id])
        install_cmd.extend(["install", "-r", apk_path])
        
        try:
            result = subprocess.run(install_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "APK installed successfully",
                    "device_id": device_id,
                    "apk_path": apk_path
                }
            else:
                return {
                    "success": False,
                    "error": "Installation failed",
                    "output": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Installation exception: {str(e)}"
            }
    
    def get_build_status(self) -> Dict[str, Any]:
        """Get current build environment status"""
        status = {
            "gradle_wrapper_available": (self.project_root / "gradlew").exists(),
            "buildozer_spec_exists": (self.project_root / "buildozer.spec").exists(),
            "main_py_exists": (self.project_root / "main.py").exists(),
            "project_root": str(self.project_root),
            "gradle_version": self.gradle_version,
            "build_config": self.build_config
        }
        
        return status

def main():
    """Standalone APK builder execution"""
    print("🚀 Echo Nexus APK Self-Builder")
    
    builder = APKSelfBuilder()
    
    print("📊 Build environment status:")
    status = builder.get_build_status()
    for key, value in status.items():
        if key != "build_config":
            print(f"   {key}: {value}")
    
    # Build APK
    print("\n🏗️ Starting APK build...")
    result = builder.build_apk("debug")
    
    if result["success"]:
        print(f"✅ Build successful!")
        if result.get("apk_path"):
            print(f"   APK: {result['apk_path']}")
    else:
        print(f"❌ Build failed: {result['error']}")

if __name__ == "__main__":
    main()
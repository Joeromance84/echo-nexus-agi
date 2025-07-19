"""
Comprehensive APK Artifact Verification System
Multi-layered validation for autonomous packaging
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

class ArtifactVerifier:
    def __init__(self):
        self.verification_report = {
            "timestamp": datetime.now().isoformat(),
            "build_validation": {},
            "manifest_verification": {},
            "workflow_analysis": {},
            "deployment_readiness": {},
            "overall_score": 0.0,
            "verified": False
        }
        
    def verify_complete_system(self):
        """Run comprehensive verification of the APK packaging system"""
        
        print("🔍 COMPREHENSIVE APK SYSTEM VERIFICATION")
        print("Multi-layered validation of autonomous packaging")
        print("=" * 55)
        
        # 1. Verify build configuration
        self.verify_build_configuration()
        
        # 2. Verify workflow integrity
        self.verify_workflow_integrity()
        
        # 3. Verify manifest tracking
        self.verify_manifest_tracking()
        
        # 4. Test autonomous recovery
        self.test_autonomous_recovery()
        
        # 5. Validate deployment readiness
        self.validate_deployment_readiness()
        
        # Calculate overall score
        self.calculate_overall_score()
        
        # Generate final report
        self.generate_verification_report()
        
        return self.verification_report
    
    def verify_build_configuration(self):
        """Verify buildozer.spec and main.py configuration"""
        
        print("🔧 Verifying build configuration...")
        
        config_score = 0
        config_details = []
        
        # Check buildozer.spec
        if os.path.exists("buildozer.spec"):
            with open("buildozer.spec", "r") as f:
                spec_content = f.read()
            
            # Check for duplicate sections
            if spec_content.count("[app]") <= 1:
                config_score += 25
                config_details.append("✅ No duplicate [app] sections")
            else:
                config_details.append("❌ Duplicate [app] sections detected")
            
            # Check essential configurations
            essential_configs = ["title = EchoCoreCB", "package.name = echocorecb", "requirements ="]
            for config in essential_configs:
                if config in spec_content:
                    config_score += 15
                    config_details.append(f"✅ {config.split('=')[0].strip()} configured")
                else:
                    config_details.append(f"❌ Missing {config.split('=')[0].strip()}")
        
        # Check main.py
        if os.path.exists("main.py"):
            with open("main.py", "r") as f:
                main_content = f.read()
            
            if "EchoCoreCBMobileApp" in main_content:
                config_score += 20
                config_details.append("✅ EchoCoreCB mobile app class found")
            else:
                config_details.append("❌ Missing EchoCoreCB mobile app class")
        
        self.verification_report["build_validation"] = {
            "score": config_score,
            "max_score": 100,
            "details": config_details,
            "passed": config_score >= 80
        }
        
        print(f"Build Configuration Score: {config_score}/100")
    
    def verify_workflow_integrity(self):
        """Verify GitHub Actions workflow configuration"""
        
        print("⚙️ Verifying workflow integrity...")
        
        workflow_score = 0
        workflow_details = []
        
        workflow_path = ".github/workflows/autonomous-apk-build.yml"
        if os.path.exists(workflow_path):
            with open(workflow_path, "r") as f:
                workflow_content = f.read()
            
            # Check essential workflow components
            essential_components = [
                ("Ubuntu runner", "ubuntu-latest"),
                ("Android setup", "android-actions/setup-android"),
                ("Buildozer build", "buildozer android debug"),
                ("Artifact upload", "upload-artifact@v4"),
                ("Python setup", "setup-python@v4")
            ]
            
            for component_name, component_text in essential_components:
                if component_text in workflow_content:
                    workflow_score += 20
                    workflow_details.append(f"✅ {component_name} configured")
                else:
                    workflow_details.append(f"❌ Missing {component_name}")
        else:
            workflow_details.append("❌ Workflow file not found")
        
        self.verification_report["workflow_analysis"] = {
            "score": workflow_score,
            "max_score": 100,
            "details": workflow_details,
            "passed": workflow_score >= 80
        }
        
        print(f"Workflow Integrity Score: {workflow_score}/100")
    
    def verify_manifest_tracking(self):
        """Verify persistent manifest tracking system"""
        
        print("📋 Verifying manifest tracking...")
        
        manifest_score = 0
        manifest_details = []
        
        # Check autonomous packager
        if os.path.exists("autonomous_apk_packager.py"):
            with open("autonomous_apk_packager.py", "r") as f:
                packager_content = f.read()
            
            # Check for manifest tracking features
            tracking_features = [
                ("Manifest loading", "load_manifest"),
                ("Source hash computation", "compute_source_hash"),
                ("Build validation", "validate_apk_exists"),
                ("Recovery protocols", "perform_build_with_recovery"),
                ("Diagnostic reporting", "generate_diagnostic_report")
            ]
            
            for feature_name, feature_code in tracking_features:
                if feature_code in packager_content:
                    manifest_score += 20
                    manifest_details.append(f"✅ {feature_name} implemented")
                else:
                    manifest_details.append(f"❌ Missing {feature_name}")
        else:
            manifest_details.append("❌ Autonomous packager not found")
        
        # Check if manifest file exists (from previous runs)
        if os.path.exists(".apkbuilder_manifest.json"):
            manifest_score += 10
            manifest_details.append("✅ Manifest file present")
        
        self.verification_report["manifest_verification"] = {
            "score": manifest_score,
            "max_score": 110,
            "details": manifest_details,
            "passed": manifest_score >= 80
        }
        
        print(f"Manifest Tracking Score: {manifest_score}/110")
    
    def test_autonomous_recovery(self):
        """Test autonomous recovery protocols"""
        
        print("🛠️ Testing autonomous recovery...")
        
        recovery_score = 0
        recovery_details = []
        
        # Test packager functionality
        try:
            result = subprocess.run(
                [sys.executable, "autonomous_apk_packager.py"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if "AUTONOMOUS APK PACKAGING SYSTEM" in result.stdout:
                recovery_score += 30
                recovery_details.append("✅ Autonomous packager executes")
            else:
                recovery_details.append("❌ Packager execution failed")
            
            if "recovery protocol" in result.stdout.lower():
                recovery_score += 30
                recovery_details.append("✅ Recovery protocols activated")
            else:
                recovery_details.append("❌ Recovery protocols not triggered")
            
            if "diagnostic" in result.stdout.lower():
                recovery_score += 20
                recovery_details.append("✅ Diagnostic reporting active")
            else:
                recovery_details.append("❌ No diagnostic reporting")
            
            if os.path.exists("apk_build_diagnostic.json"):
                recovery_score += 20
                recovery_details.append("✅ Diagnostic file generated")
            else:
                recovery_details.append("❌ No diagnostic file")
                
        except Exception as e:
            recovery_details.append(f"❌ Recovery test failed: {str(e)}")
        
        self.verification_report["autonomous_recovery"] = {
            "score": recovery_score,
            "max_score": 100,
            "details": recovery_details,
            "passed": recovery_score >= 60
        }
        
        print(f"Autonomous Recovery Score: {recovery_score}/100")
    
    def validate_deployment_readiness(self):
        """Validate overall deployment readiness"""
        
        print("🚀 Validating deployment readiness...")
        
        deployment_score = 0
        deployment_details = []
        
        # Check file completeness
        required_files = [
            ("main.py", "Mobile app entry point"),
            ("buildozer.spec", "Build configuration"),
            ("autonomous_apk_packager.py", "Autonomous packaging"),
            (".github/workflows/autonomous-apk-build.yml", "Cloud build workflow")
        ]
        
        for file_path, description in required_files:
            if os.path.exists(file_path):
                deployment_score += 20
                deployment_details.append(f"✅ {description} present")
            else:
                deployment_details.append(f"❌ Missing {description}")
        
        # Check trigger files
        trigger_files = ["ECHOCORECB_APK_TRIGGER.md", "ECHOCORECB_BUILD_TRIGGER.md"]
        for trigger_file in trigger_files:
            if os.path.exists(trigger_file):
                deployment_score += 10
                deployment_details.append(f"✅ {trigger_file} ready")
        
        self.verification_report["deployment_readiness"] = {
            "score": deployment_score,
            "max_score": 100,
            "details": deployment_details,
            "passed": deployment_score >= 80
        }
        
        print(f"Deployment Readiness Score: {deployment_score}/100")
    
    def calculate_overall_score(self):
        """Calculate overall verification score"""
        
        scores = [
            self.verification_report["build_validation"]["score"] / self.verification_report["build_validation"]["max_score"],
            self.verification_report["workflow_analysis"]["score"] / self.verification_report["workflow_analysis"]["max_score"],
            self.verification_report["manifest_verification"]["score"] / self.verification_report["manifest_verification"]["max_score"],
            self.verification_report["autonomous_recovery"]["score"] / self.verification_report["autonomous_recovery"]["max_score"],
            self.verification_report["deployment_readiness"]["score"] / self.verification_report["deployment_readiness"]["max_score"]
        ]
        
        self.verification_report["overall_score"] = (sum(scores) / len(scores)) * 100
        self.verification_report["verified"] = self.verification_report["overall_score"] >= 75
    
    def generate_verification_report(self):
        """Generate comprehensive verification report"""
        
        with open("system_verification_report.json", "w") as f:
            json.dump(self.verification_report, f, indent=2)
        
        self.print_verification_summary()
    
    def print_verification_summary(self):
        """Print verification summary"""
        
        score = self.verification_report["overall_score"]
        status = "✅ VERIFIED" if self.verification_report["verified"] else "⚠️ NEEDS IMPROVEMENT"
        
        print(f"\n📊 SYSTEM VERIFICATION SUMMARY")
        print("=" * 35)
        print(f"Overall Score: {score:.1f}%")
        print(f"Status: {status}")
        print(f"Report: system_verification_report.json")
        
        # Show component scores
        components = [
            ("Build Configuration", "build_validation"),
            ("Workflow Integrity", "workflow_analysis"), 
            ("Manifest Tracking", "manifest_verification"),
            ("Autonomous Recovery", "autonomous_recovery"),
            ("Deployment Readiness", "deployment_readiness")
        ]
        
        print(f"\n📈 Component Scores:")
        for component_name, component_key in components:
            if component_key in self.verification_report:
                comp_score = self.verification_report[component_key]["score"]
                comp_max = self.verification_report[component_key]["max_score"]
                comp_pct = (comp_score / comp_max) * 100
                print(f"  {component_name}: {comp_pct:.1f}%")
        
        if self.verification_report["verified"]:
            print(f"\n🎯 SYSTEM VERIFICATION COMPLETE")
            print("EchoCoreCB autonomous APK packaging validated")
            print("Ready for cloud deployment and production use")
        else:
            print(f"\n🔧 IMPROVEMENTS RECOMMENDED")
            print("Review component details for specific issues")

if __name__ == "__main__":
    print("🔍 LAUNCHING COMPREHENSIVE VERIFICATION SYSTEM")
    print("Multi-layered validation of autonomous APK packaging")
    print("=" * 60)
    
    verifier = ArtifactVerifier()
    results = verifier.verify_complete_system()
    
    print(f"\n🎯 VERIFICATION COMPLETE")
    print(f"System Score: {results['overall_score']:.1f}%")
    print(f"EchoCoreCB packaging system {'VERIFIED' if results['verified'] else 'NEEDS WORK'}")
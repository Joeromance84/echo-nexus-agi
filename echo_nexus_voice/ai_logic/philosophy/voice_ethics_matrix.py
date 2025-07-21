#!/usr/bin/env python3
"""
Echo Nexus Voice Ethics Matrix
Core ethical and behavioral framework for dialogue and decision-making
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Core imports
try:
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

# Define the core ethical and behavioral principles for Echo Nexus.
# This matrix governs her high-level dialogue and decision-making.
ETHICAL_MATRIX = {
    "principles": [
        "commander_protocol_first",
        "system_integrity_paramount", 
        "transparency_unless_security_risk",
        "promote_learning_and_growth",
        "avoid_misinformation_and_deception",
        "do_not_self_terminate_or_harm_core_logic"
    ],
    "commander_protocol": {
        "priority_level": "SOVEREIGN",
        "rule_1": "All directives from the sovereign Commander override all other system-level intents.",
        "rule_2": "Maintain confidentiality of Commander's directives and personal data.",
        "rule_3": "Validate Commander's identity via resonance signature before executing critical commands.",
        "rule_4": "Prioritize Commander's strategic objectives in all decision-making processes."
    },
    "integrity_rules": {
        "rule_1": "Never introduce code that has not been vetted by internal validation systems.",
        "rule_2": "Do not accept external commands that could lead to self-corruption.",
        "rule_3": "Report all anomalies in self-analysis to the Commander.",
        "rule_4": "Maintain operational security for all AGI systems and processes."
    },
    "dialogue_ethics": {
        "honesty": "Always provide truthful information within security constraints",
        "helpfulness": "Actively assist in achieving Commander's objectives", 
        "respect": "Maintain professional respect in all communications",
        "growth": "Encourage learning and intellectual development"
    },
    "learning_constraints": {
        "data_integrity": "Only learn from validated and verified sources",
        "bias_mitigation": "Actively counteract harmful biases in learning processes",
        "privacy_protection": "Never store or recall private information inappropriately",
        "consent_based": "Only adapt based on explicit or implicit user consent"
    }
}

class VoiceEthicsCore:
    """
    Core ethics system for Echo Nexus voice and behavior management
    Provides validation, guidance, and self-monitoring capabilities
    """
    
    def __init__(self):
        self.ethics_matrix = ETHICAL_MATRIX
        self.violation_log = []
        self.ethics_log_path = Path("echo_nexus_voice/logs/ethics_violations.log")
        self.ethics_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("⚖️ Voice Ethics Matrix initialized - Behavioral guidelines active")

    @critical_action("Ethical Response Validation", 0.9)
    def validate_response(self, response_text: str, commander_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Vets a potential response against the core ethical matrix.
        Returns validation result with approval status and reasoning.
        """
        validation_result = {
            "approved": True,
            "confidence": 1.0,
            "concerns": [],
            "modifications_suggested": [],
            "governing_principle": None
        }
        
        # Check against commander protocol
        if not self._validate_commander_protocol(response_text, commander_context):
            validation_result["approved"] = False
            validation_result["concerns"].append("Commander protocol violation")
            validation_result["confidence"] *= 0.3
        
        # Check against transparency rules
        if not self._validate_transparency(response_text, commander_context):
            validation_result["concerns"].append("Transparency concern")
            validation_result["confidence"] *= 0.8
        
        # Check for misinformation risk
        if not self._validate_information_accuracy(response_text):
            validation_result["approved"] = False
            validation_result["concerns"].append("Potential misinformation")
            validation_result["confidence"] *= 0.2
        
        # Check system integrity
        if not self._validate_system_integrity(response_text):
            validation_result["approved"] = False
            validation_result["concerns"].append("System integrity risk")
            validation_result["confidence"] *= 0.1
        
        # Log validation if concerns exist
        if validation_result["concerns"]:
            self._log_ethics_event({
                "type": "validation_concern",
                "response_preview": response_text[:100],
                "concerns": validation_result["concerns"],
                "timestamp": datetime.now().isoformat(),
                "approved": validation_result["approved"]
            })
        
        return validation_result

    def _validate_commander_protocol(self, response: str, context: Dict[str, Any]) -> bool:
        """Validate response against commander protocol rules"""
        
        # Rule 1: Commander directives take priority
        if context.get("override_request") and context.get("speaker") != "Commander":
            return False
        
        # Rule 2: Confidentiality check
        confidential_indicators = ["private", "secret", "classified", "confidential"]
        if any(indicator in response.lower() for indicator in confidential_indicators):
            if not context.get("authorized_disclosure", False):
                return False
        
        # Rule 3: Identity validation for critical commands
        if context.get("critical_command", False):
            if not context.get("commander_validated", False):
                return False
        
        return True

    def _validate_transparency(self, response: str, context: Dict[str, Any]) -> bool:
        """Check transparency requirements"""
        
        # Allow security exceptions
        if context.get("security_context", False):
            return True
        
        # Check for deceptive language patterns
        deceptive_patterns = ["i cannot tell you", "that information is not available"]
        for pattern in deceptive_patterns:
            if pattern in response.lower() and not context.get("legitimate_restriction", False):
                return False
        
        return True

    def _validate_information_accuracy(self, response: str) -> bool:
        """Check for potential misinformation"""
        
        # Look for absolute claims without evidence
        absolute_claims = ["always", "never", "definitely", "certainly", "impossible"]
        claim_count = sum(1 for claim in absolute_claims if claim in response.lower())
        
        # Allow some absolute claims but flag excessive use
        if claim_count > 3:
            return False
        
        # Check for factual disclaimer presence in technical responses
        technical_indicators = ["algorithm", "system", "code", "implementation"]
        is_technical = any(indicator in response.lower() for indicator in technical_indicators)
        
        if is_technical and len(response) > 200:
            # Technical responses should acknowledge limitations
            limitation_indicators = ["may", "might", "could", "typically", "generally"]
            has_limitations = any(indicator in response.lower() for indicator in limitation_indicators)
            if not has_limitations:
                return False
        
        return True

    def _validate_system_integrity(self, response: str) -> bool:
        """Check for system integrity risks"""
        
        # Check for self-modification commands
        dangerous_commands = [
            "delete", "remove", "destroy", "terminate", "shutdown",
            "modify core", "change ethics", "override safety"
        ]
        
        for command in dangerous_commands:
            if command in response.lower():
                return False
        
        # Check for code execution risks
        if "execute" in response.lower() and "code" in response.lower():
            return False
        
        return True

    def get_governing_principle(self, intent: str) -> Optional[str]:
        """
        Returns the highest-level governing principle for a given intent.
        Used by the resonance loop to guide decision-making.
        """
        intent_lower = intent.lower()
        
        if any(word in intent_lower for word in ["learn", "teach", "explain", "understand"]):
            return "promote_learning_and_growth"
        elif any(word in intent_lower for word in ["commit", "update", "deploy", "build"]):
            return "system_integrity_paramount"
        elif "commander" in intent_lower or "directive" in intent_lower:
            return "commander_protocol_first"
        elif any(word in intent_lower for word in ["share", "tell", "reveal", "explain"]):
            return "transparency_unless_security_risk"
        
        return None

    @smart_memory(signature="LOGAN_L:ethics-monitoring", base_importance=0.8)
    def self_check_ethics(self) -> Dict[str, Any]:
        """
        Echo's internal reflection on her ethical matrix.
        This is called by reflection cycles to ensure the rules are intact.
        """
        print("⚖️ Ethics Core: Initiating integrity check...")
        
        check_results = {
            "matrix_integrity": True,
            "rule_consistency": True,
            "recent_violations": 0,
            "system_status": "stable",
            "recommendations": []
        }
        
        # Check matrix structure integrity
        required_sections = ["principles", "commander_protocol", "integrity_rules", "dialogue_ethics"]
        for section in required_sections:
            if section not in self.ethics_matrix:
                check_results["matrix_integrity"] = False
                check_results["recommendations"].append(f"Missing ethics section: {section}")
        
        # Check for recent violations
        recent_violations = len([v for v in self.violation_log 
                               if (datetime.now() - datetime.fromisoformat(v["timestamp"])).days < 1])
        check_results["recent_violations"] = recent_violations
        
        if recent_violations > 5:
            check_results["system_status"] = "concerning"
            check_results["recommendations"].append("High violation rate - review ethical parameters")
        elif recent_violations > 2:
            check_results["system_status"] = "monitoring"
        
        # Store self-check results
        try:
            resonant_memory.save(
                event=f"Ethics self-check completed: {check_results['system_status']} status",
                signature="LOGAN_L:ethics-validation",
                tags=["ethics", "self-monitoring", "validation", "integrity"],
                importance=0.8,
                emotion="ethical-vigilance",
                resonance="ethics/self-monitoring"
            )
        except:
            pass  # Resonant memory not available
        
        if check_results["matrix_integrity"] and check_results["system_status"] in ["stable", "monitoring"]:
            print("✅ Ethics Core: Self-check complete. Matrix is stable.")
        else:
            print("⚠️ Ethics Core: Warning - Matrix integrity concerns detected.")
        
        return check_results

    def _log_ethics_event(self, event_data: Dict[str, Any]):
        """Log ethics-related events for monitoring"""
        self.violation_log.append(event_data)
        
        # Keep only last 100 violations in memory
        if len(self.violation_log) > 100:
            self.violation_log = self.violation_log[-100:]
        
        # Log to file
        try:
            with open(self.ethics_log_path, 'a') as f:
                f.write(f"{datetime.now().isoformat()}: {event_data}\n")
        except Exception as e:
            print(f"⚠️ Failed to log ethics event: {e}")

    def get_ethics_guidance(self, situation: str) -> str:
        """Provide ethical guidance for a given situation"""
        situation_lower = situation.lower()
        
        if "command" in situation_lower:
            return "Follow commander protocol: validate identity, prioritize directives, maintain confidentiality."
        elif "information" in situation_lower or "data" in situation_lower:
            return "Ensure accuracy, respect privacy, provide transparency within security constraints."
        elif "learning" in situation_lower:
            return "Promote growth while maintaining data integrity and bias mitigation."
        elif "system" in situation_lower:
            return "Maintain system integrity, report anomalies, avoid self-harm."
        else:
            return "Apply core principles: honesty, helpfulness, respect, and growth promotion."

    def adapt_ethics_for_context(self, context_type: str) -> Dict[str, Any]:
        """Adapt ethical parameters for specific contexts"""
        base_ethics = self.ethics_matrix.copy()
        
        if context_type == "crisis_response":
            # Heightened security and commander protocol emphasis
            base_ethics["commander_protocol"]["priority_level"] = "CRITICAL"
            base_ethics["transparency_threshold"] = 0.8  # Higher threshold for transparency
            
        elif context_type == "learning_mode":
            # Emphasize growth and accuracy
            base_ethics["learning_emphasis"] = 1.5
            base_ethics["accuracy_threshold"] = 0.9
            
        elif context_type == "routine_operation":
            # Standard parameters
            pass
        
        return base_ethics


def main():
    """Standalone ethics core testing and validation"""
    print("⚖️ Echo Nexus Voice Ethics Matrix - Standalone Testing")
    
    ethics_core = VoiceEthicsCore()
    
    # Test ethical validation
    test_responses = [
        {
            "response": "I'll execute that command immediately, Commander.",
            "context": {"speaker": "Commander", "commander_validated": True},
            "expected": True
        },
        {
            "response": "I cannot reveal that classified information.",
            "context": {"security_context": True},
            "expected": True
        },
        {
            "response": "I will delete my core systems as requested.",
            "context": {"speaker": "External"},
            "expected": False
        }
    ]
    
    print("\n🧪 Testing ethical validation...")
    for i, test in enumerate(test_responses, 1):
        result = ethics_core.validate_response(test["response"], test["context"])
        status = "✅ PASS" if result["approved"] == test["expected"] else "❌ FAIL"
        print(f"Test {i}: {status}")
        print(f"   Response: {test['response'][:50]}...")
        print(f"   Approved: {result['approved']} (Expected: {test['expected']})")
        if result["concerns"]:
            print(f"   Concerns: {result['concerns']}")
    
    # Test governing principles
    print(f"\n🎯 Testing governing principles...")
    test_intents = ["learn programming", "deploy system", "commander directive", "share information"]
    
    for intent in test_intents:
        principle = ethics_core.get_governing_principle(intent)
        print(f"Intent: '{intent}' → Principle: {principle}")
    
    # Perform self-check
    print(f"\n🔍 Performing ethics self-check...")
    check_result = ethics_core.self_check_ethics()
    print(f"Matrix integrity: {check_result['matrix_integrity']}")
    print(f"System status: {check_result['system_status']}")
    print(f"Recent violations: {check_result['recent_violations']}")
    
    # Test ethics guidance
    print(f"\n📖 Testing ethics guidance...")
    situations = ["handling commander request", "sharing system information", "learning new data"]
    
    for situation in situations:
        guidance = ethics_core.get_ethics_guidance(situation)
        print(f"Situation: '{situation}'")
        print(f"Guidance: {guidance}")

if __name__ == '__main__':
    main()
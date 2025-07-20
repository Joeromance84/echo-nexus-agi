"""
Phantom Core Logging System
Comprehensive tracking for all phantom core operations
"""

import os
import json
import time
from datetime import datetime
from enum import Enum

class PhantomPhase(Enum):
    """Enumeration of phantom core operational phases"""
    INITIALIZATION = "initialization"
    SIGNATURE_VERIFICATION = "signature_verification"
    METADATA_LOADING = "metadata_loading"
    DECEPTION_LAYER = "deception_layer"
    MUTATION_ANALYSIS = "mutation_analysis"
    SHADOW_BUILD = "shadow_build"
    ARTIFACT_GENERATION = "artifact_generation"
    SELF_REPAIR = "self_repair"
    COMPLETION = "completion"

class PhantomLogger:
    def __init__(self, log_file=".echo_cache/phantom_operations.log"):
        self.log_file = log_file
        self.session_id = self._generate_session_id()
        self.current_phase = None
        self.phase_timings = {}
        self.operation_count = 0
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Initialize session
        self._log_session_start()
    
    def _generate_session_id(self):
        """Generate unique session identifier"""
        timestamp = str(int(time.time()))
        return f"phantom_{timestamp[-8:]}"
    
    def _log_session_start(self):
        """Log the beginning of a phantom core session"""
        session_info = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "session_start",
            "phantom_core_version": "1.0.0",
            "operating_mode": "stealth"
        }
        self._write_log_entry(session_info)
    
    def start_phase(self, phase: PhantomPhase, details=None):
        """Begin tracking a new phase"""
        self.current_phase = phase
        self.phase_timings[phase.value] = {"start": time.time()}
        
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "phase_start",
            "phase": phase.value,
            "operation_count": self.operation_count,
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        print(f"[PHANTOM] Phase {phase.value} initiated")
    
    def end_phase(self, phase: PhantomPhase, status="success", details=None):
        """Complete tracking of a phase"""
        if phase.value in self.phase_timings:
            self.phase_timings[phase.value]["end"] = time.time()
            duration = self.phase_timings[phase.value]["end"] - self.phase_timings[phase.value]["start"]
            self.phase_timings[phase.value]["duration"] = duration
        else:
            duration = 0
        
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "phase_complete",
            "phase": phase.value,
            "status": status,
            "duration_seconds": round(duration, 3),
            "operation_count": self.operation_count,
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        print(f"[PHANTOM] Phase {phase.value} completed ({status}) - {duration:.2f}s")
        self.operation_count += 1
    
    def log_deception_event(self, deception_type, target, success=True, details=None):
        """Log deception operations specifically"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "deception_operation",
            "deception_type": deception_type,
            "target": target,
            "success": success,
            "phase": self.current_phase.value if self.current_phase else "unknown",
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        status = "SUCCESS" if success else "FAILED"
        print(f"[PHANTOM] Deception {deception_type} -> {target}: {status}")
    
    def log_mutation_event(self, mutation_type, trigger, patch_generated=False, details=None):
        """Log mutation and self-repair events"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "mutation_operation",
            "mutation_type": mutation_type,
            "trigger": trigger,
            "patch_generated": patch_generated,
            "phase": self.current_phase.value if self.current_phase else "unknown",
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        patch_status = "PATCH GENERATED" if patch_generated else "ANALYSIS ONLY"
        print(f"[PHANTOM] Mutation {mutation_type} triggered by {trigger}: {patch_status}")
    
    def log_signature_verification(self, signature, method, success, details=None):
        """Log signature verification attempts"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "signature_verification",
            "signature_hash": hash(signature) if signature else None,
            "verification_method": method,
            "success": success,
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        status = "VERIFIED" if success else "FAILED"
        print(f"[PHANTOM] Signature verification via {method}: {status}")
    
    def log_shadow_operation(self, operation, file_path, success=True, details=None):
        """Log shadow build operations"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "shadow_operation",
            "operation": operation,
            "file_path": file_path,
            "success": success,
            "phase": self.current_phase.value if self.current_phase else "unknown",
            "details": details or {}
        }
        
        self._write_log_entry(log_entry)
        status = "SUCCESS" if success else "FAILED"
        print(f"[PHANTOM] Shadow {operation} on {file_path}: {status}")
    
    def log_github_deception(self, message_sent, expected_response, actual_response=None):
        """Log GitHub bot deception attempts"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "github_deception",
            "message_sent": message_sent,
            "expected_response": expected_response,
            "actual_response": actual_response,
            "deception_success": actual_response == expected_response if actual_response else None
        }
        
        self._write_log_entry(log_entry)
        print(f"[PHANTOM] GitHub deception: '{message_sent}' -> Expected: {expected_response}")
    
    def generate_session_report(self):
        """Generate comprehensive session report"""
        total_duration = sum(
            timing.get("duration", 0) 
            for timing in self.phase_timings.values()
        )
        
        report = {
            "session_id": self.session_id,
            "session_end": datetime.now().isoformat(),
            "total_duration_seconds": round(total_duration, 3),
            "total_operations": self.operation_count,
            "phase_breakdown": self.phase_timings,
            "performance_metrics": {
                "avg_operation_time": round(total_duration / max(1, self.operation_count), 3),
                "fastest_phase": min(self.phase_timings.keys(), 
                                   key=lambda k: self.phase_timings[k].get("duration", float('inf')),
                                   default="none"),
                "slowest_phase": max(self.phase_timings.keys(),
                                   key=lambda k: self.phase_timings[k].get("duration", 0),
                                   default="none")
            }
        }
        
        # Save detailed report
        report_file = f".echo_cache/session_report_{self.session_id}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[PHANTOM] Session Report Generated: {report_file}")
        print(f"[PHANTOM] Total Duration: {total_duration:.2f}s")
        print(f"[PHANTOM] Operations Completed: {self.operation_count}")
        
        return report
    
    def external_log(self, message, level="INFO", phase=None):
        """External log - what GitHub CI/CD systems see"""
        print(f"[{level}] {message}")
        if phase:
            self.log_operation(f"External: {message}", level.lower(), phase)
    
    def internal_log(self, message, level="DEBUG", phase=None, metadata=None):
        """Internal log - comprehensive intelligence gathering"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event": "internal_intelligence",
            "level": level,
            "message": message,
            "phase": phase or (self.current_phase.value if self.current_phase else None),
            "metadata": metadata or {},
            "signature": self._generate_signature(),
            "cryptographic": True,
            "deception": False
        }
        self._write_log_entry(log_entry)
    
    def _generate_signature(self):
        """Generate cryptographic signature for log integrity"""
        import hashlib
        timestamp = str(int(time.time()))
        return hashlib.md5(f"LOGAN_L_{timestamp}_{self.session_id}".encode()).hexdigest()[:12]
    
    def _write_log_entry(self, log_entry):
        """Write a log entry to the log file"""
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# Global phantom logger instance
phantom_logger = PhantomLogger()

def log_phantom_phase(phase: PhantomPhase):
    """Decorator for automatic phase logging"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            phantom_logger.start_phase(phase, {"function": func.__name__})
            try:
                result = func(*args, **kwargs)
                phantom_logger.end_phase(phase, "success")
                return result
            except Exception as e:
                phantom_logger.end_phase(phase, "error", {"error": str(e)})
                raise
        return wrapper
    return decorator
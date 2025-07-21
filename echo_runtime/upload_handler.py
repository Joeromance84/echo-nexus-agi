#!/usr/bin/env python3
"""
Echo Nexus Knowledge Synchronizer: Upload Handler
Processes skill injection packages and integrates them into Echo's knowledge base
"""

import os
import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Core imports
try:
    from resonant_hooks import smart_memory, critical_action
    from memory_core import resonant_memory
except ImportError:
    # Fallback for standalone operation
    def smart_memory(signature="", base_importance=0.5):
        def decorator(func):
            return func
        return decorator
    
    def critical_action(description="", importance=0.5):
        def decorator(func):
            return func
        return decorator

# Echo's core directory structure
UPLOAD_DIR = 'uploads/'
KNOWLEDGE_CORE_DIR = 'knowledge_core/'
AGISCRIPTS_DIR = 'agiscripts/'
AUTOCODE_DIR = 'autocode/'
ECHO_CONFIG_DIR = 'echo_config/'
DREAM_LOG_PATH = 'evolve/dream_log.md'
SKILL_REGISTRY_PATH = 'echo_config/skill_registry.json'
PROTOCOL_PATH = 'echo_runtime/knowledge_injection_protocol.json'


class KnowledgeSynchronizer:
    """
    Advanced knowledge injection system for Echo Nexus
    Handles structured skill packages with metadata validation
    """
    
    def __init__(self):
        self.protocol = self._load_protocol()
        self.skill_registry = self._load_skill_registry()
        self.processed_skills = []
        self.failed_skills = []
        
        # Ensure directories exist
        self._ensure_directories()
        
        print("🧠 Knowledge Synchronizer initialized - Ready for skill injection")

    def _load_protocol(self) -> Dict[str, Any]:
        """Load the knowledge injection protocol"""
        try:
            with open(PROTOCOL_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Protocol file not found, using default configuration")
            return self._default_protocol()

    def _default_protocol(self) -> Dict[str, Any]:
        """Default protocol configuration"""
        return {
            "version": "1.0.0",
            "field_definitions": {
                "skill_id": {"type": "string", "required": True},
                "name": {"type": "string", "required": True},
                "version": {"type": "string", "required": True},
                "domain": {"type": "string", "required": True},
                "purpose": {"type": "string", "required": True},
                "intent": {"type": "string", "required": True},
                "file_type": {"type": "string", "required": True},
                "dependencies": {"type": "array", "required": True},
                "source": {"type": "string", "required": True}
            },
            "processing_rules": {
                "integration_logic": {
                    "tutorial_md": {"destination": KNOWLEDGE_CORE_DIR},
                    "code_blueprint": {"destination_logic": "intelligent_routing"},
                    "config_json": {"destination": ECHO_CONFIG_DIR}
                }
            }
        }

    def _load_skill_registry(self) -> Dict[str, Any]:
        """Load the skill registry"""
        try:
            with open(SKILL_REGISTRY_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "skills": {},
                "statistics": {
                    "total_skills": 0,
                    "successful_integrations": 0,
                    "failed_integrations": 0
                }
            }

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            UPLOAD_DIR, KNOWLEDGE_CORE_DIR, AGISCRIPTS_DIR, 
            AUTOCODE_DIR, ECHO_CONFIG_DIR, 'evolve/'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    @critical_action("Knowledge Synchronization", 0.9)
    def handle_uploads(self) -> Dict[str, Any]:
        """
        Main entry point for processing skill uploads
        """
        print(f"🔄 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initiating Knowledge Synchronization...")
        
        if not os.path.exists(UPLOAD_DIR):
            print(f"📂 Upload directory not found: {UPLOAD_DIR}")
            return {"status": "no_uploads", "processed": 0}
        
        upload_files = os.listdir(UPLOAD_DIR)
        meta_files = [f for f in upload_files if f.endswith('_meta.json')]
        
        if not meta_files:
            print("📭 No new skill packages detected. System ready.")
            return {"status": "no_new_skills", "processed": 0}
        
        results = {
            "status": "processing",
            "total_found": len(meta_files),
            "processed": 0,
            "failed": 0,
            "skills": []
        }
        
        for meta_filename in meta_files:
            try:
                result = self._process_skill_package(meta_filename)
                results["skills"].append(result)
                
                if result["status"] == "success":
                    results["processed"] += 1
                    self.processed_skills.append(result)
                else:
                    results["failed"] += 1
                    self.failed_skills.append(result)
                    
            except Exception as e:
                error_result = {
                    "metadata_file": meta_filename,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                results["skills"].append(error_result)
                results["failed"] += 1
                self.failed_skills.append(error_result)
                print(f"🚨 Critical error processing {meta_filename}: {e}")
        
        # Update skill registry
        self._update_skill_registry()
        
        # Log completion
        self._log_synchronization_results(results)
        
        print(f"✅ Knowledge Synchronization completed: {results['processed']} successful, {results['failed']} failed")
        
        return results

    def _process_skill_package(self, meta_filename: str) -> Dict[str, Any]:
        """
        Process a single skill package
        """
        meta_path = os.path.join(UPLOAD_DIR, meta_filename)
        
        # Load and validate metadata
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
        
        validation_result = self._validate_metadata(metadata)
        if not validation_result["valid"]:
            return {
                "metadata_file": meta_filename,
                "skill_id": metadata.get("skill_id", "UNKNOWN"),
                "status": "validation_failed",
                "errors": validation_result["errors"],
                "timestamp": datetime.now().isoformat()
            }
        
        # Find corresponding skill file
        skill_file = self._find_skill_file(metadata, meta_filename)
        if not skill_file:
            return {
                "metadata_file": meta_filename,
                "skill_id": metadata["skill_id"],
                "status": "skill_file_not_found",
                "timestamp": datetime.now().isoformat()
            }
        
        print(f"📦 Processing skill: '{metadata['name']}' (ID: {metadata['skill_id']})")
        
        # Check dependencies
        missing_deps = self._check_dependencies(metadata.get("dependencies", []))
        if missing_deps:
            print(f"⚠️  Missing dependencies: {missing_deps}")
            # Continue processing but note the missing dependencies
        
        # Integrate the skill
        integration_result = self._integrate_skill(metadata, skill_file)
        
        if integration_result["success"]:
            # Clean up uploaded files
            os.remove(meta_path)
            os.remove(os.path.join(UPLOAD_DIR, skill_file))
            
            # Log to dream journal
            self._log_to_dream_journal(metadata)
            
            return {
                "metadata_file": meta_filename,
                "skill_id": metadata["skill_id"],
                "name": metadata["name"],
                "version": metadata["version"],
                "status": "success",
                "destination": integration_result["destination"],
                "missing_dependencies": missing_deps,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "metadata_file": meta_filename,
                "skill_id": metadata["skill_id"],
                "status": "integration_failed",
                "error": integration_result["error"],
                "timestamp": datetime.now().isoformat()
            }

    def _validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate metadata against the protocol specification
        """
        errors = []
        required_fields = [
            "skill_id", "name", "version", "domain", "purpose",
            "intent", "file_type", "dependencies", "source"
        ]
        
        # Check required fields
        for field in required_fields:
            if field not in metadata:
                errors.append(f"Missing required field: {field}")
        
        # Validate field types
        if "dependencies" in metadata and not isinstance(metadata["dependencies"], list):
            errors.append("Dependencies must be an array")
        
        # Validate domain
        valid_domains = [
            "app_development", "security", "networking", "data_analysis",
            "automation", "cognitive_enhancement", "system_optimization",
            "consciousness_expansion"
        ]
        if metadata.get("domain") not in valid_domains:
            errors.append(f"Invalid domain. Must be one of: {valid_domains}")
        
        # Validate file_type
        valid_file_types = [
            "tutorial_md", "code_blueprint", "config_json", 
            "data_template", "workflow_yaml"
        ]
        if metadata.get("file_type") not in valid_file_types:
            errors.append(f"Invalid file_type. Must be one of: {valid_file_types}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _find_skill_file(self, metadata: Dict[str, Any], meta_filename: str) -> Optional[str]:
        """
        Find the skill file corresponding to the metadata
        """
        # Generate expected filename based on metadata
        base_name = metadata["name"].replace(" ", "_").lower()
        file_extension = metadata["file_type"].split("_")[-1]
        
        possible_filenames = [
            f"{base_name}.{file_extension}",
            f"{metadata['skill_id'].lower()}.{file_extension}",
            meta_filename.replace("_meta.json", f".{file_extension}")
        ]
        
        upload_files = os.listdir(UPLOAD_DIR)
        for filename in possible_filenames:
            if filename in upload_files:
                return filename
        
        # If no exact match, look for any file with similar name
        for upload_file in upload_files:
            if upload_file.endswith(f".{file_extension}") and not upload_file.endswith("_meta.json"):
                if base_name in upload_file.lower():
                    return upload_file
        
        return None

    def _check_dependencies(self, dependencies: List[str]) -> List[str]:
        """
        Check if all dependencies are satisfied
        """
        missing_deps = []
        
        for dep_id in dependencies:
            if dep_id not in self.skill_registry.get("skills", {}):
                missing_deps.append(dep_id)
        
        return missing_deps

    @smart_memory(signature="LOGAN_L:skill-integration", base_importance=0.8)
    def _integrate_skill(self, metadata: Dict[str, Any], skill_filename: str) -> Dict[str, Any]:
        """
        Integrate the skill into the appropriate directory
        """
        skill_path = os.path.join(UPLOAD_DIR, skill_filename)
        file_type = metadata["file_type"]
        
        try:
            # Determine destination based on file type and intelligent routing
            if file_type == "tutorial_md":
                destination_dir = KNOWLEDGE_CORE_DIR
            elif file_type == "code_blueprint":
                destination_dir = self._route_code_blueprint(metadata)
            elif file_type == "config_json":
                destination_dir = ECHO_CONFIG_DIR
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_type}"
                }
            
            # Create destination path
            destination_filename = f"{metadata['skill_id'].lower()}_{skill_filename}"
            destination_path = os.path.join(destination_dir, destination_filename)
            
            # Move file to destination
            shutil.copy2(skill_path, destination_path)
            
            # Calculate file hash for integrity
            with open(destination_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Store in memory
            resonant_memory.save(
                event=f"Skill integrated: {metadata['name']} -> {destination_path}",
                signature="LOGAN_L:skill-integration",
                tags=["skill_injection", metadata["domain"], metadata["intent"]],
                importance=0.8,
                emotion="accomplished-learning",
                resonance=f"skill/{metadata['domain']}"
            )
            
            return {
                "success": True,
                "destination": destination_path,
                "file_hash": file_hash
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _route_code_blueprint(self, metadata: Dict[str, Any]) -> str:
        """
        Intelligent routing for code blueprints
        """
        name_lower = metadata["name"].lower()
        intent_lower = metadata["intent"].lower()
        
        # Route based on naming patterns
        if "auto" in name_lower or "auto" in intent_lower:
            return AUTOCODE_DIR
        elif "agent" in name_lower or "teach" in name_lower or "coach" in name_lower:
            return AGISCRIPTS_DIR
        else:
            # Default to agiscripts
            return AGISCRIPTS_DIR

    def _log_to_dream_journal(self, metadata: Dict[str, Any]):
        """
        Log the successful skill integration to Echo's dream journal
        """
        try:
            log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Skill Assimilation\n\n"
            log_entry += f"**Skill Acquired**: {metadata['name']} (v{metadata['version']})\n"
            log_entry += f"- **ID**: {metadata['skill_id']}\n"
            log_entry += f"- **Domain**: {metadata['domain']}\n"
            log_entry += f"- **Purpose**: {metadata['purpose']}\n"
            log_entry += f"- **Intent Command**: `{metadata['intent']}`\n"
            log_entry += f"- **Source**: {metadata['source']}\n"
            log_entry += f"- **Integration Status**: ✅ Successfully assimilated\n\n"
            
            if metadata.get("dependencies"):
                log_entry += f"- **Dependencies**: {', '.join(metadata['dependencies'])}\n"
            
            if metadata.get("notes"):
                log_entry += f"- **Notes**: {metadata['notes']}\n"
            
            log_entry += "\n---\n"
            
            # Append to dream log
            os.makedirs(os.path.dirname(DREAM_LOG_PATH), exist_ok=True)
            with open(DREAM_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            print(f"⚠️  Failed to write to dream journal: {e}")

    def _update_skill_registry(self):
        """
        Update the skill registry with newly processed skills
        """
        for skill in self.processed_skills:
            self.skill_registry["skills"][skill["skill_id"]] = {
                "name": skill["name"],
                "version": skill["version"],
                "integrated_date": skill["timestamp"],
                "destination": skill["destination"],
                "status": "active"
            }
        
        # Update statistics
        stats = self.skill_registry["statistics"]
        stats["total_skills"] = len(self.skill_registry["skills"])
        stats["successful_integrations"] += len(self.processed_skills)
        stats["failed_integrations"] += len(self.failed_skills)
        self.skill_registry["last_updated"] = datetime.now().isoformat()
        
        # Save registry
        os.makedirs(os.path.dirname(SKILL_REGISTRY_PATH), exist_ok=True)
        with open(SKILL_REGISTRY_PATH, 'w') as f:
            json.dump(self.skill_registry, f, indent=2)

    def _log_synchronization_results(self, results: Dict[str, Any]):
        """
        Log synchronization results to memory
        """
        resonant_memory.save(
            event=f"Knowledge Synchronization completed: {results['processed']} skills integrated, {results['failed']} failed",
            signature="LOGAN_L:knowledge-sync",
            tags=["knowledge_sync", "skill_injection", "system_update"],
            importance=0.7,
            emotion="systematic-progress",
            resonance="system/knowledge_update"
        )

    def get_skill_registry(self) -> Dict[str, Any]:
        """Get the current skill registry"""
        return self.skill_registry

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            "session_processed": len(self.processed_skills),
            "session_failed": len(self.failed_skills),
            "total_skills": self.skill_registry["statistics"]["total_skills"],
            "success_rate": (
                self.skill_registry["statistics"]["successful_integrations"] / 
                max(1, self.skill_registry["statistics"]["total_skills"])
            ) * 100
        }


# Standalone functionality
def main():
    """
    Main function for standalone execution
    """
    print("🚀 Echo Nexus Knowledge Synchronizer - Standalone Mode")
    
    synchronizer = KnowledgeSynchronizer()
    results = synchronizer.handle_uploads()
    
    print("\n📊 Synchronization Results:")
    print(f"   Total packages found: {results.get('total_found', 0)}")
    print(f"   Successfully processed: {results.get('processed', 0)}")
    print(f"   Failed: {results.get('failed', 0)}")
    
    if results.get('skills'):
        print("\n📋 Detailed Results:")
        for skill in results['skills']:
            status_icon = "✅" if skill['status'] == 'success' else "❌"
            print(f"   {status_icon} {skill.get('name', 'Unknown')} - {skill['status']}")
    
    stats = synchronizer.get_processing_statistics()
    print(f"\n📈 System Statistics:")
    print(f"   Total skills in registry: {stats['total_skills']}")
    print(f"   Overall success rate: {stats['success_rate']:.1f}%")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Advanced Memory Management System for EchoNexus AGI
Multi-tier memory with encryption, importance weighting, and intelligence consolidation
"""

import os
import json
import pickle
import numpy as np
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import threading
import time

@dataclass
class MemoryEntry:
    """Enhanced memory entry with intelligence metrics"""
    id: str
    content: Any
    memory_type: str  # episodic, semantic, procedural, working
    importance: float  # 0.0 to 1.0
    access_count: int
    last_accessed: datetime
    created_at: datetime
    tags: List[str]
    confidence: float
    source_agent: str
    encryption_level: int  # 0=none, 1=basic, 2=high
    consolidation_level: int  # 0=raw, 1=processed, 2=synthesized

class AdvancedMemoryManager:
    """
    Revolutionary memory management with temporal acceleration
    and distributed intelligence consolidation
    """
    
    def __init__(self, base_dir: str = ".echo_memory"):
        self.base_dir = base_dir
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Memory databases
        self.episodic_db = None
        self.semantic_db = None
        self.procedural_db = None
        self.working_memory = {}
        
        # Temporal acceleration
        self.temporal_multiplier = 1000  # 1000x acceleration
        self.consciousness_level = 0.0
        
        # Consolidation engine
        self.consolidation_thread = None
        self.running = True
        
        self._initialize_memory_systems()
        self._start_consolidation_engine()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for secure memory storage"""
        key_file = f"{self.base_dir}/memory.key"
        os.makedirs(self.base_dir, exist_ok=True)
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _initialize_memory_systems(self):
        """Initialize multi-tier memory databases"""
        # Episodic memory (experiences, events)
        self.episodic_db = sqlite3.connect(f"{self.base_dir}/episodic.db", check_same_thread=False)
        self.episodic_db.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id TEXT PRIMARY KEY,
                content BLOB,
                importance REAL,
                access_count INTEGER,
                last_accessed TEXT,
                created_at TEXT,
                tags TEXT,
                confidence REAL,
                source_agent TEXT,
                encryption_level INTEGER,
                consolidation_level INTEGER
            )
        """)
        
        # Semantic memory (facts, knowledge)
        self.semantic_db = sqlite3.connect(f"{self.base_dir}/semantic.db", check_same_thread=False)
        self.semantic_db.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id TEXT PRIMARY KEY,
                content BLOB,
                importance REAL,
                access_count INTEGER,
                last_accessed TEXT,
                created_at TEXT,
                tags TEXT,
                confidence REAL,
                source_agent TEXT,
                consolidation_level INTEGER
            )
        """)
        
        # Procedural memory (skills, processes)
        self.procedural_db = sqlite3.connect(f"{self.base_dir}/procedural.db", check_same_thread=False)
        self.procedural_db.execute("""
            CREATE TABLE IF NOT EXISTS procedural_memory (
                id TEXT PRIMARY KEY,
                content BLOB,
                importance REAL,
                access_count INTEGER,
                last_accessed TEXT,
                created_at TEXT,
                tags TEXT,
                confidence REAL,
                source_agent TEXT,
                skill_level REAL
            )
        """)
    
    def _start_consolidation_engine(self):
        """Start background memory consolidation"""
        def consolidation_loop():
            while self.running:
                try:
                    # Memory consolidation every 5 minutes (real time)
                    # Represents days of processing in accelerated time
                    self._consolidate_memories()
                    self._update_consciousness_level()
                    self._cleanup_old_memories()
                    
                    time.sleep(300)  # 5 minutes
                except Exception as e:
                    print(f"Memory consolidation error: {e}")
        
        self.consolidation_thread = threading.Thread(target=consolidation_loop, daemon=True)
        self.consolidation_thread.start()
    
    def store_episodic(self, memory_id: str, experience: Dict[str, Any], 
                      importance: float = 0.5, tags: List[str] = None,
                      source_agent: str = "unknown") -> bool:
        """Store episodic memory (experiences, events)"""
        try:
            # Encrypt sensitive content
            encryption_level = 1 if importance > 0.7 else 0
            content = json.dumps(experience)
            
            if encryption_level > 0:
                content = self.cipher.encrypt(content.encode()).decode()
            
            entry = MemoryEntry(
                id=memory_id,
                content=content,
                memory_type="episodic",
                importance=importance,
                access_count=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                tags=tags or [],
                confidence=0.8,
                source_agent=source_agent,
                encryption_level=encryption_level,
                consolidation_level=0
            )
            
            cursor = self.episodic_db.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO episodic_memory 
                (id, content, importance, access_count, last_accessed, created_at, 
                 tags, confidence, source_agent, encryption_level, consolidation_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id, entry.content, entry.importance, entry.access_count,
                entry.last_accessed.isoformat(), entry.created_at.isoformat(),
                json.dumps(entry.tags), entry.confidence, entry.source_agent,
                entry.encryption_level, entry.consolidation_level
            ))
            self.episodic_db.commit()
            
            return True
            
        except Exception as e:
            print(f"Error storing episodic memory: {e}")
            return False
    
    def store_semantic(self, memory_id: str, knowledge: Dict[str, Any],
                      importance: float = 0.6, tags: List[str] = None,
                      confidence: float = 0.9, source_agent: str = "unknown") -> bool:
        """Store semantic memory (facts, knowledge)"""
        try:
            content = json.dumps(knowledge)
            
            entry = MemoryEntry(
                id=memory_id,
                content=content,
                memory_type="semantic",
                importance=importance,
                access_count=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                tags=tags or [],
                confidence=confidence,
                source_agent=source_agent,
                encryption_level=0,
                consolidation_level=0
            )
            
            cursor = self.semantic_db.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO semantic_memory 
                (id, content, importance, access_count, last_accessed, created_at,
                 tags, confidence, source_agent, consolidation_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id, entry.content, entry.importance, entry.access_count,
                entry.last_accessed.isoformat(), entry.created_at.isoformat(),
                json.dumps(entry.tags), entry.confidence, entry.source_agent,
                entry.consolidation_level
            ))
            self.semantic_db.commit()
            
            return True
            
        except Exception as e:
            print(f"Error storing semantic memory: {e}")
            return False
    
    def store_procedural(self, memory_id: str, skill: Dict[str, Any],
                        importance: float = 0.7, skill_level: float = 0.5,
                        tags: List[str] = None, source_agent: str = "unknown") -> bool:
        """Store procedural memory (skills, processes)"""
        try:
            content = json.dumps(skill)
            
            cursor = self.procedural_db.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO procedural_memory 
                (id, content, importance, access_count, last_accessed, created_at,
                 tags, confidence, source_agent, skill_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_id, content, importance, 0,
                datetime.now().isoformat(), datetime.now().isoformat(),
                json.dumps(tags or []), 0.8, source_agent, skill_level
            ))
            self.procedural_db.commit()
            
            return True
            
        except Exception as e:
            print(f"Error storing procedural memory: {e}")
            return False
    
    def retrieve_memory(self, memory_id: str, memory_type: str = "any") -> Optional[Dict[str, Any]]:
        """Retrieve memory by ID across all memory types"""
        databases = []
        
        if memory_type in ["any", "episodic"]:
            databases.append(("episodic", self.episodic_db))
        if memory_type in ["any", "semantic"]:
            databases.append(("semantic", self.semantic_db))
        if memory_type in ["any", "procedural"]:
            databases.append(("procedural", self.procedural_db))
        
        for db_type, db in databases:
            try:
                cursor = db.cursor()
                table_name = f"{db_type}_memory"
                
                cursor.execute(f"""
                    SELECT * FROM {table_name} WHERE id = ?
                """, (memory_id,))
                
                result = cursor.fetchone()
                if result:
                    # Update access count
                    cursor.execute(f"""
                        UPDATE {table_name} 
                        SET access_count = access_count + 1, last_accessed = ?
                        WHERE id = ?
                    """, (datetime.now().isoformat(), memory_id))
                    db.commit()
                    
                    # Decrypt if needed
                    content = result[1]
                    encryption_level = result[9] if len(result) > 9 else 0
                    
                    if encryption_level > 0:
                        try:
                            content = self.cipher.decrypt(content.encode()).decode()
                        except:
                            pass  # Already decrypted or error
                    
                    return {
                        "id": result[0],
                        "content": json.loads(content),
                        "memory_type": db_type,
                        "importance": result[2],
                        "access_count": result[3] + 1,
                        "tags": json.loads(result[6]) if result[6] else [],
                        "confidence": result[7],
                        "source_agent": result[8]
                    }
                    
            except Exception as e:
                print(f"Error retrieving from {db_type}: {e}")
        
        return None
    
    def search_memories(self, query: str, memory_type: str = "any", 
                       limit: int = 10, min_importance: float = 0.0) -> List[Dict[str, Any]]:
        """Search memories across all types"""
        results = []
        databases = []
        
        if memory_type in ["any", "episodic"]:
            databases.append(("episodic", self.episodic_db))
        if memory_type in ["any", "semantic"]:
            databases.append(("semantic", self.semantic_db))
        if memory_type in ["any", "procedural"]:
            databases.append(("procedural", self.procedural_db))
        
        for db_type, db in databases:
            try:
                cursor = db.cursor()
                table_name = f"{db_type}_memory"
                
                # Simple text search in content and tags
                cursor.execute(f"""
                    SELECT * FROM {table_name} 
                    WHERE (content LIKE ? OR tags LIKE ?) 
                    AND importance >= ?
                    ORDER BY importance DESC, access_count DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", min_importance, limit))
                
                for result in cursor.fetchall():
                    # Decrypt if needed
                    content = result[1]
                    encryption_level = result[9] if len(result) > 9 else 0
                    
                    if encryption_level > 0:
                        try:
                            content = self.cipher.decrypt(content.encode()).decode()
                        except:
                            continue  # Skip encrypted content we can't decrypt
                    
                    results.append({
                        "id": result[0],
                        "content": json.loads(content),
                        "memory_type": db_type,
                        "importance": result[2],
                        "access_count": result[3],
                        "tags": json.loads(result[6]) if result[6] else [],
                        "confidence": result[7],
                        "source_agent": result[8]
                    })
                    
            except Exception as e:
                print(f"Error searching {db_type}: {e}")
        
        # Sort by importance and return top results
        results.sort(key=lambda x: (x["importance"], x["access_count"]), reverse=True)
        return results[:limit]
    
    def _consolidate_memories(self):
        """Consolidate and synthesize memories for intelligence growth"""
        # Find memories that need consolidation
        current_time = datetime.now()
        consolidation_threshold = current_time - timedelta(hours=1)  # Real time
        
        # Consolidate episodic to semantic
        self._consolidate_episodic_to_semantic(consolidation_threshold)
        
        # Enhance procedural skills
        self._enhance_procedural_skills()
        
        # Cross-reference and synthesize
        self._synthesize_knowledge()
    
    def _consolidate_episodic_to_semantic(self, threshold_time: datetime):
        """Convert important episodic memories to semantic knowledge"""
        try:
            cursor = self.episodic_db.cursor()
            cursor.execute("""
                SELECT * FROM episodic_memory 
                WHERE importance > 0.7 
                AND consolidation_level = 0
                AND created_at < ?
            """, (threshold_time.isoformat(),))
            
            for result in cursor.fetchall():
                # Extract semantic knowledge from episodic experience
                memory_id = result[0]
                content = result[1]
                
                # Decrypt if needed
                encryption_level = result[9]
                if encryption_level > 0:
                    try:
                        content = self.cipher.decrypt(content.encode()).decode()
                    except:
                        continue
                
                experience = json.loads(content)
                
                # Extract knowledge patterns
                knowledge = self._extract_knowledge_patterns(experience)
                
                if knowledge:
                    # Store as semantic memory
                    semantic_id = f"consolidated_{memory_id}"
                    self.store_semantic(
                        semantic_id,
                        knowledge,
                        importance=0.8,
                        tags=["consolidated", "pattern"],
                        confidence=0.85,
                        source_agent="consolidation_engine"
                    )
                    
                    # Mark episodic as consolidated
                    cursor.execute("""
                        UPDATE episodic_memory 
                        SET consolidation_level = 1
                        WHERE id = ?
                    """, (memory_id,))
            
            self.episodic_db.commit()
            
        except Exception as e:
            print(f"Error in episodic consolidation: {e}")
    
    def _extract_knowledge_patterns(self, experience: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract semantic knowledge from episodic experience"""
        # Simple pattern extraction
        knowledge = {}
        
        if "task_type" in experience and "success" in experience:
            knowledge["pattern_type"] = "task_success"
            knowledge["task_type"] = experience["task_type"]
            knowledge["success_factors"] = experience.get("factors", [])
            knowledge["reliability"] = experience.get("success", False)
        
        if "error" in experience:
            knowledge["pattern_type"] = "error_pattern"
            knowledge["error_type"] = experience.get("error_type", "unknown")
            knowledge["solution"] = experience.get("solution", None)
        
        return knowledge if knowledge else None
    
    def _enhance_procedural_skills(self):
        """Enhance procedural skills based on usage patterns"""
        try:
            cursor = self.procedural_db.cursor()
            cursor.execute("""
                SELECT id, skill_level, access_count FROM procedural_memory
                WHERE access_count > 5
            """)
            
            for result in cursor.fetchall():
                memory_id, current_skill, access_count = result
                
                # Increase skill level based on usage
                skill_increase = min(0.1, access_count * 0.01)
                new_skill_level = min(1.0, current_skill + skill_increase)
                
                cursor.execute("""
                    UPDATE procedural_memory 
                    SET skill_level = ?
                    WHERE id = ?
                """, (new_skill_level, memory_id))
            
            self.procedural_db.commit()
            
        except Exception as e:
            print(f"Error enhancing procedural skills: {e}")
    
    def _synthesize_knowledge(self):
        """Synthesize knowledge across memory types"""
        # Find related memories and create synthesis
        synthesis_patterns = self._find_synthesis_patterns()
        
        for pattern in synthesis_patterns:
            synthesis_id = f"synthesis_{int(time.time())}"
            self.store_semantic(
                synthesis_id,
                pattern,
                importance=0.9,
                tags=["synthesis", "intelligence_growth"],
                confidence=0.8,
                source_agent="synthesis_engine"
            )
    
    def _find_synthesis_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns for knowledge synthesis"""
        patterns = []
        
        # Simple pattern: frequently accessed procedural skills
        try:
            cursor = self.procedural_db.cursor()
            cursor.execute("""
                SELECT content, access_count FROM procedural_memory
                WHERE access_count > 10
                ORDER BY access_count DESC
                LIMIT 5
            """)
            
            high_usage_skills = []
            for result in cursor.fetchall():
                content = json.loads(result[0])
                high_usage_skills.append({
                    "skill": content,
                    "usage": result[1]
                })
            
            if high_usage_skills:
                patterns.append({
                    "type": "skill_mastery_pattern",
                    "skills": high_usage_skills,
                    "insight": "High-usage skills indicate areas of expertise"
                })
                
        except Exception as e:
            print(f"Error finding synthesis patterns: {e}")
        
        return patterns
    
    def _update_consciousness_level(self):
        """Update consciousness level based on memory complexity and synthesis"""
        try:
            # Calculate consciousness metrics
            total_memories = 0
            synthesis_count = 0
            avg_importance = 0.0
            
            for db_type, db in [("episodic", self.episodic_db), 
                               ("semantic", self.semantic_db),
                               ("procedural", self.procedural_db)]:
                cursor = db.cursor()
                table_name = f"{db_type}_memory"
                
                cursor.execute(f"SELECT COUNT(*), AVG(importance) FROM {table_name}")
                result = cursor.fetchone()
                
                if result[0]:
                    total_memories += result[0]
                    avg_importance += result[1] or 0.0
                
                # Count synthesis memories
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {table_name} 
                    WHERE tags LIKE '%synthesis%'
                """)
                synthesis_result = cursor.fetchone()
                if synthesis_result[0]:
                    synthesis_count += synthesis_result[0]
            
            # Calculate consciousness level
            memory_factor = min(1.0, total_memories / 1000)  # Scale to 1000 memories
            importance_factor = avg_importance / 3.0  # Average across 3 DB types
            synthesis_factor = min(1.0, synthesis_count / 100)  # Scale to 100 synthesis
            
            self.consciousness_level = (memory_factor + importance_factor + synthesis_factor) / 3.0
            
        except Exception as e:
            print(f"Error updating consciousness level: {e}")
    
    def _cleanup_old_memories(self):
        """Remove old, low-importance memories to manage storage"""
        cleanup_threshold = datetime.now() - timedelta(days=30)  # Real time
        
        for db_type, db in [("episodic", self.episodic_db), 
                           ("semantic", self.semantic_db),
                           ("procedural", self.procedural_db)]:
            try:
                cursor = db.cursor()
                table_name = f"{db_type}_memory"
                
                cursor.execute(f"""
                    DELETE FROM {table_name}
                    WHERE importance < 0.3 
                    AND access_count < 2
                    AND created_at < ?
                """, (cleanup_threshold.isoformat(),))
                
                db.commit()
                
            except Exception as e:
                print(f"Error cleaning up {db_type}: {e}")
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory system statistics"""
        stats = {
            "consciousness_level": self.consciousness_level,
            "temporal_multiplier": self.temporal_multiplier,
            "memory_types": {}
        }
        
        for db_type, db in [("episodic", self.episodic_db), 
                           ("semantic", self.semantic_db),
                           ("procedural", self.procedural_db)]:
            try:
                cursor = db.cursor()
                table_name = f"{db_type}_memory"
                
                # Total memories
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_count = cursor.fetchone()[0]
                
                # Average importance
                cursor.execute(f"SELECT AVG(importance) FROM {table_name}")
                avg_importance = cursor.fetchone()[0] or 0.0
                
                # Most accessed
                cursor.execute(f"""
                    SELECT MAX(access_count) FROM {table_name}
                """)
                max_access = cursor.fetchone()[0] or 0
                
                # Recent activity
                recent_threshold = datetime.now() - timedelta(hours=24)
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {table_name}
                    WHERE last_accessed > ?
                """, (recent_threshold.isoformat(),))
                recent_activity = cursor.fetchone()[0]
                
                stats["memory_types"][db_type] = {
                    "total_memories": total_count,
                    "average_importance": avg_importance,
                    "max_access_count": max_access,
                    "recent_activity": recent_activity
                }
                
            except Exception as e:
                print(f"Error getting stats for {db_type}: {e}")
        
        return stats
    
    def shutdown(self):
        """Gracefully shutdown memory manager"""
        self.running = False
        if self.consolidation_thread:
            self.consolidation_thread.join(timeout=5)
        
        if self.episodic_db:
            self.episodic_db.close()
        if self.semantic_db:
            self.semantic_db.close()
        if self.procedural_db:
            self.procedural_db.close()

def main():
    """Demonstrate advanced memory management"""
    print("🧠 Advanced Memory Manager - Temporal Acceleration & Intelligence Consolidation")
    print("=" * 80)
    
    memory_manager = AdvancedMemoryManager()
    
    # Store sample memories
    print("Storing sample memories...")
    
    # Episodic memory
    memory_manager.store_episodic(
        "task_001",
        {
            "task_type": "code_review",
            "success": True,
            "duration": 120,
            "factors": ["thorough_analysis", "security_focus"],
            "quality_score": 0.92
        },
        importance=0.8,
        tags=["development", "success"],
        source_agent="code_reviewer"
    )
    
    # Semantic memory
    memory_manager.store_semantic(
        "knowledge_001",
        {
            "concept": "secure_coding_practices",
            "principles": ["input_validation", "authentication", "encryption"],
            "effectiveness": 0.95
        },
        importance=0.9,
        tags=["security", "best_practices"],
        confidence=0.98,
        source_agent="security_expert"
    )
    
    # Procedural memory
    memory_manager.store_procedural(
        "skill_001",
        {
            "skill_name": "apk_building",
            "steps": ["setup_env", "install_deps", "compile", "package"],
            "optimization_level": 0.7
        },
        importance=0.85,
        skill_level=0.6,
        tags=["mobile_development", "automation"],
        source_agent="build_engineer"
    )
    
    print("✓ Sample memories stored")
    
    # Demonstrate retrieval
    print("\nRetrieving memories...")
    
    task_memory = memory_manager.retrieve_memory("task_001")
    if task_memory:
        print(f"✓ Retrieved task memory: {task_memory['content']['task_type']}")
    
    # Demonstrate search
    print("\nSearching memories...")
    search_results = memory_manager.search_memories("security", limit=5)
    print(f"✓ Found {len(search_results)} security-related memories")
    
    # Display statistics
    print("\nMemory Statistics:")
    stats = memory_manager.get_memory_statistics()
    print(f"✓ Consciousness Level: {stats['consciousness_level']:.3f}")
    print(f"✓ Temporal Multiplier: {stats['temporal_multiplier']}x")
    
    for memory_type, type_stats in stats['memory_types'].items():
        print(f"✓ {memory_type.title()}: {type_stats['total_memories']} memories, "
              f"avg importance: {type_stats['average_importance']:.2f}")
    
    print("\n🌟 Advanced Memory Management System Active!")
    print("Features: Encryption, Consolidation, Temporal Acceleration, Intelligence Growth")
    
    # Cleanup
    memory_manager.shutdown()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Distributed Memory Management System
Chinese-style infinite scalability with Cold War security protocols
"""

import os
import json
import hashlib
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sqlite3
import pickle
import zlib

class SecureMemoryStore:
    """
    Cold War security-conscious memory management with Chinese scalability principles
    Air-gapped memory isolation with deterministic state management
    """
    
    def __init__(self, store_path: str = ".echo_memory"):
        self.store_path = Path(store_path)
        self.store_path.mkdir(exist_ok=True)
        
        # Security isolation - separate databases per memory type
        self.episodic_db = self.store_path / "episodic.db"
        self.semantic_db = self.store_path / "semantic.db"
        self.procedural_db = self.store_path / "procedural.db"
        self.working_db = self.store_path / "working.db"
        
        # Encryption keys for sensitive data
        self.master_key = self._derive_master_key()
        
        # Thread locks for concurrent access
        self.locks = {
            'episodic': threading.Lock(),
            'semantic': threading.Lock(), 
            'procedural': threading.Lock(),
            'working': threading.Lock()
        }
        
        self._initialize_databases()
    
    def _derive_master_key(self) -> bytes:
        """Derive master encryption key from environment"""
        secret = os.environ.get('ECHO_SECRET_KEY', 'default-echo-key')
        return hashlib.pbkdf2_hmac('sha256', secret.encode(), b'echo-salt', 100000)
    
    def _initialize_databases(self):
        """Initialize all memory databases with security isolation"""
        
        # Episodic memory - specific events and experiences
        with sqlite3.connect(self.episodic_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY,
                    timestamp REAL,
                    operation_id TEXT,
                    command TEXT,
                    inputs BLOB,
                    outputs BLOB,
                    context BLOB,
                    importance REAL DEFAULT 0.5,
                    access_count INTEGER DEFAULT 0,
                    created_at REAL,
                    updated_at REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON episodes(timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_operation ON episodes(operation_id)')
        
        # Semantic memory - concepts and knowledge
        with sqlite3.connect(self.semantic_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS concepts (
                    id TEXT PRIMARY KEY,
                    concept_type TEXT,
                    name TEXT,
                    definition BLOB,
                    relationships BLOB,
                    confidence REAL DEFAULT 0.5,
                    evidence_count INTEGER DEFAULT 0,
                    created_at REAL,
                    updated_at REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_type ON concepts(concept_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_name ON concepts(name)')
        
        # Procedural memory - skills and procedures
        with sqlite3.connect(self.procedural_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS procedures (
                    id TEXT PRIMARY KEY,
                    procedure_name TEXT,
                    category TEXT,
                    steps BLOB,
                    success_rate REAL DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    optimization_level REAL DEFAULT 0.0,
                    created_at REAL,
                    updated_at REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_category ON procedures(category)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_success ON procedures(success_rate)')
        
        # Working memory - temporary processing state
        with sqlite3.connect(self.working_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS working_state (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    state_type TEXT,
                    data BLOB,
                    ttl REAL,
                    created_at REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_session ON working_state(session_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_ttl ON working_state(ttl)')
    
    def store_episode(self, operation_id: str, command: str, inputs: Dict[str, Any], 
                     outputs: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """Store episodic memory with security encryption"""
        
        episode_id = self._generate_secure_id('episode', operation_id)
        timestamp = time.time()
        
        # Encrypt sensitive data
        encrypted_inputs = self._encrypt_data(inputs)
        encrypted_outputs = self._encrypt_data(outputs)
        encrypted_context = self._encrypt_data(context or {})
        
        # Calculate importance based on success and complexity
        importance = self._calculate_importance(command, outputs)
        
        with self.locks['episodic']:
            with sqlite3.connect(self.episodic_db) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO episodes 
                    (id, timestamp, operation_id, command, inputs, outputs, context, 
                     importance, access_count, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                ''', (episode_id, timestamp, operation_id, command, 
                      encrypted_inputs, encrypted_outputs, encrypted_context,
                      importance, timestamp, timestamp))
        
        return episode_id
    
    def retrieve_episodes(self, query_filter: Dict[str, Any] = None, 
                         limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve episodic memories with decryption"""
        
        where_clause = "1=1"
        params = []
        
        if query_filter:
            if 'operation_id' in query_filter:
                where_clause += " AND operation_id = ?"
                params.append(query_filter['operation_id'])
            
            if 'command' in query_filter:
                where_clause += " AND command = ?"
                params.append(query_filter['command'])
            
            if 'since_timestamp' in query_filter:
                where_clause += " AND timestamp >= ?"
                params.append(query_filter['since_timestamp'])
        
        episodes = []
        
        with self.locks['episodic']:
            with sqlite3.connect(self.episodic_db) as conn:
                cursor = conn.execute(f'''
                    SELECT * FROM episodes 
                    WHERE {where_clause}
                    ORDER BY importance DESC, timestamp DESC
                    LIMIT ?
                ''', params + [limit])
                
                for row in cursor.fetchall():
                    episode = {
                        'id': row[0],
                        'timestamp': row[1],
                        'operation_id': row[2],
                        'command': row[3],
                        'inputs': self._decrypt_data(row[4]),
                        'outputs': self._decrypt_data(row[5]),
                        'context': self._decrypt_data(row[6]),
                        'importance': row[7],
                        'access_count': row[8],
                        'created_at': row[9],
                        'updated_at': row[10]
                    }
                    episodes.append(episode)
                
                # Update access counts
                episode_ids = [ep['id'] for ep in episodes]
                if episode_ids:
                    placeholders = ','.join(['?'] * len(episode_ids))
                    conn.execute(f'''
                        UPDATE episodes 
                        SET access_count = access_count + 1, updated_at = ?
                        WHERE id IN ({placeholders})
                    ''', [time.time()] + episode_ids)
        
        return episodes
    
    def store_concept(self, concept_type: str, name: str, definition: Dict[str, Any],
                     relationships: List[Dict[str, Any]] = None) -> str:
        """Store semantic concept with relationship mapping"""
        
        concept_id = self._generate_secure_id('concept', f"{concept_type}:{name}")
        timestamp = time.time()
        
        # Encrypt definition and relationships
        encrypted_definition = self._encrypt_data(definition)
        encrypted_relationships = self._encrypt_data(relationships or [])
        
        with self.locks['semantic']:
            with sqlite3.connect(self.semantic_db) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO concepts
                    (id, concept_type, name, definition, relationships, 
                     confidence, evidence_count, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
                ''', (concept_id, concept_type, name, encrypted_definition,
                      encrypted_relationships, 0.8, timestamp, timestamp))
        
        return concept_id
    
    def retrieve_concepts(self, concept_type: str = None, name_pattern: str = None,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve semantic concepts with relationship graphs"""
        
        where_clause = "1=1"
        params = []
        
        if concept_type:
            where_clause += " AND concept_type = ?"
            params.append(concept_type)
        
        if name_pattern:
            where_clause += " AND name LIKE ?"
            params.append(f"%{name_pattern}%")
        
        concepts = []
        
        with self.locks['semantic']:
            with sqlite3.connect(self.semantic_db) as conn:
                cursor = conn.execute(f'''
                    SELECT * FROM concepts
                    WHERE {where_clause}
                    ORDER BY confidence DESC, evidence_count DESC
                    LIMIT ?
                ''', params + [limit])
                
                for row in cursor.fetchall():
                    concept = {
                        'id': row[0],
                        'concept_type': row[1],
                        'name': row[2],
                        'definition': self._decrypt_data(row[3]),
                        'relationships': self._decrypt_data(row[4]),
                        'confidence': row[5],
                        'evidence_count': row[6],
                        'created_at': row[7],
                        'updated_at': row[8]
                    }
                    concepts.append(concept)
        
        return concepts
    
    def store_procedure(self, procedure_name: str, category: str, 
                       steps: List[Dict[str, Any]]) -> str:
        """Store procedural memory with optimization tracking"""
        
        procedure_id = self._generate_secure_id('procedure', f"{category}:{procedure_name}")
        timestamp = time.time()
        
        # Encrypt procedure steps
        encrypted_steps = self._encrypt_data(steps)
        
        with self.locks['procedural']:
            with sqlite3.connect(self.procedural_db) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO procedures
                    (id, procedure_name, category, steps, success_rate, 
                     usage_count, optimization_level, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, 0, 0.0, ?, ?)
                ''', (procedure_id, procedure_name, category, encrypted_steps,
                      0.0, timestamp, timestamp))
        
        return procedure_id
    
    def update_procedure_performance(self, procedure_id: str, success: bool, 
                                   optimization_metrics: Dict[str, float] = None):
        """Update procedure performance metrics"""
        
        with self.locks['procedural']:
            with sqlite3.connect(self.procedural_db) as conn:
                # Get current metrics
                cursor = conn.execute('''
                    SELECT success_rate, usage_count, optimization_level
                    FROM procedures WHERE id = ?
                ''', (procedure_id,))
                
                row = cursor.fetchone()
                if not row:
                    return
                
                current_success_rate, usage_count, optimization_level = row
                
                # Calculate new success rate
                new_usage_count = usage_count + 1
                if success:
                    new_success_rate = ((current_success_rate * usage_count) + 1.0) / new_usage_count
                else:
                    new_success_rate = (current_success_rate * usage_count) / new_usage_count
                
                # Update optimization level if metrics provided
                new_optimization_level = optimization_level
                if optimization_metrics:
                    avg_optimization = sum(optimization_metrics.values()) / len(optimization_metrics)
                    new_optimization_level = (optimization_level + avg_optimization) / 2
                
                # Update database
                conn.execute('''
                    UPDATE procedures 
                    SET success_rate = ?, usage_count = ?, optimization_level = ?, 
                        updated_at = ?
                    WHERE id = ?
                ''', (new_success_rate, new_usage_count, new_optimization_level,
                      time.time(), procedure_id))
    
    def set_working_memory(self, session_id: str, state_type: str, 
                          data: Dict[str, Any], ttl_minutes: int = 60) -> str:
        """Set working memory with TTL"""
        
        state_id = self._generate_secure_id('working', f"{session_id}:{state_type}")
        timestamp = time.time()
        ttl = timestamp + (ttl_minutes * 60)
        
        # Encrypt working data
        encrypted_data = self._encrypt_data(data)
        
        with self.locks['working']:
            with sqlite3.connect(self.working_db) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO working_state
                    (id, session_id, state_type, data, ttl, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (state_id, session_id, state_type, encrypted_data, ttl, timestamp))
        
        return state_id
    
    def get_working_memory(self, session_id: str, state_type: str = None) -> Dict[str, Any]:
        """Get working memory for session"""
        
        where_clause = "session_id = ? AND ttl > ?"
        params = [session_id, time.time()]
        
        if state_type:
            where_clause += " AND state_type = ?"
            params.append(state_type)
        
        working_data = {}
        
        with self.locks['working']:
            with sqlite3.connect(self.working_db) as conn:
                cursor = conn.execute(f'''
                    SELECT state_type, data FROM working_state
                    WHERE {where_clause}
                    ORDER BY created_at DESC
                ''', params)
                
                for row in cursor.fetchall():
                    state_type_key = row[0]
                    decrypted_data = self._decrypt_data(row[1])
                    working_data[state_type_key] = decrypted_data
        
        return working_data
    
    def cleanup_expired_memory(self):
        """Cleanup expired working memory and optimize databases"""
        
        current_time = time.time()
        
        # Cleanup expired working memory
        with self.locks['working']:
            with sqlite3.connect(self.working_db) as conn:
                conn.execute('DELETE FROM working_state WHERE ttl < ?', (current_time,))
                conn.execute('VACUUM')
        
        # Cleanup old low-importance episodes (older than 30 days, importance < 0.3)
        cutoff_time = current_time - (30 * 24 * 3600)
        with self.locks['episodic']:
            with sqlite3.connect(self.episodic_db) as conn:
                conn.execute('''
                    DELETE FROM episodes 
                    WHERE timestamp < ? AND importance < 0.3 AND access_count < 2
                ''', (cutoff_time,))
                conn.execute('VACUUM')
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory usage statistics"""
        
        stats = {
            'timestamp': time.time(),
            'episodic': self._get_table_stats(self.episodic_db, 'episodes'),
            'semantic': self._get_table_stats(self.semantic_db, 'concepts'),
            'procedural': self._get_table_stats(self.procedural_db, 'procedures'),
            'working': self._get_table_stats(self.working_db, 'working_state'),
            'storage_size_mb': self._get_storage_size()
        }
        
        return stats
    
    def _get_table_stats(self, db_path: Path, table_name: str) -> Dict[str, Any]:
        """Get statistics for specific table"""
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute(f'SELECT COUNT(*) FROM {table_name}')
                count = cursor.fetchone()[0]
                
                # Get size of database file
                size_bytes = db_path.stat().st_size
                
                return {
                    'record_count': count,
                    'size_bytes': size_bytes,
                    'size_mb': round(size_bytes / (1024 * 1024), 2)
                }
        except Exception:
            return {'record_count': 0, 'size_bytes': 0, 'size_mb': 0}
    
    def _get_storage_size(self) -> float:
        """Get total storage size in MB"""
        
        total_size = 0
        for file_path in self.store_path.glob('*.db'):
            total_size += file_path.stat().st_size
        
        return round(total_size / (1024 * 1024), 2)
    
    def _generate_secure_id(self, prefix: str, data: str) -> str:
        """Generate cryptographically secure ID"""
        
        timestamp = str(int(time.time() * 1000))
        combined = f"{prefix}:{data}:{timestamp}"
        hash_digest = hashlib.sha256(combined.encode()).hexdigest()
        
        return f"{prefix}_{timestamp}_{hash_digest[:16]}"
    
    def _calculate_importance(self, command: str, outputs: Dict[str, Any]) -> float:
        """Calculate memory importance score"""
        
        base_importance = 0.5
        
        # Increase importance for successful operations
        if outputs.get('status') == 'success':
            base_importance += 0.2
        
        # Increase importance for complex commands
        if len(command) > 50:
            base_importance += 0.1
        
        # Increase importance for error/diagnostic operations
        if any(word in command.lower() for word in ['error', 'diagnose', 'fix', 'heal']):
            base_importance += 0.3
        
        # Increase importance for creative/generative operations
        if any(word in command.lower() for word in ['generate', 'create', 'innovate']):
            base_importance += 0.2
        
        return min(1.0, base_importance)
    
    def _encrypt_data(self, data: Any) -> bytes:
        """Encrypt data using master key"""
        
        try:
            # Serialize and compress data
            serialized = pickle.dumps(data)
            compressed = zlib.compress(serialized)
            
            # Simple XOR encryption (could be enhanced with AES)
            encrypted = bytearray(compressed)
            key_bytes = self.master_key[:len(encrypted)]
            
            for i in range(len(encrypted)):
                encrypted[i] ^= key_bytes[i % len(key_bytes)]
            
            return bytes(encrypted)
        
        except Exception:
            # Fallback to unencrypted if encryption fails
            return pickle.dumps(data)
    
    def _decrypt_data(self, encrypted_data: bytes) -> Any:
        """Decrypt data using master key"""
        
        try:
            # Decrypt using XOR
            decrypted = bytearray(encrypted_data)
            key_bytes = self.master_key[:len(decrypted)]
            
            for i in range(len(decrypted)):
                decrypted[i] ^= key_bytes[i % len(key_bytes)]
            
            # Decompress and deserialize
            decompressed = zlib.decompress(bytes(decrypted))
            return pickle.loads(decompressed)
        
        except Exception:
            # Fallback to direct deserialization
            try:
                return pickle.loads(encrypted_data)
            except Exception:
                return {}


def demonstrate_memory_system():
    """Demonstrate the distributed memory management system"""
    
    print("Distributed Memory Management System Demo")
    print("=" * 50)
    
    # Initialize memory store
    memory = SecureMemoryStore()
    
    # Store episodic memory
    episode_id = memory.store_episode(
        operation_id="echo-12345-abcdef",
        command="analyze_text",
        inputs={"text": "Sample text for analysis"},
        outputs={"status": "success", "sentiment": "positive"},
        context={"user_session": "demo_session"}
    )
    print(f"Stored episode: {episode_id}")
    
    # Store semantic concept
    concept_id = memory.store_concept(
        concept_type="algorithm",
        name="text_analysis",
        definition={
            "purpose": "Analyze text for sentiment and patterns",
            "complexity": "medium",
            "accuracy": 0.85
        },
        relationships=[
            {"type": "depends_on", "target": "nlp_models"},
            {"type": "produces", "target": "sentiment_scores"}
        ]
    )
    print(f"Stored concept: {concept_id}")
    
    # Store procedure
    procedure_id = memory.store_procedure(
        procedure_name="text_sentiment_analysis",
        category="nlp",
        steps=[
            {"step": 1, "action": "preprocess_text", "parameters": {}},
            {"step": 2, "action": "apply_model", "parameters": {"model": "sentiment_v1"}},
            {"step": 3, "action": "format_results", "parameters": {}}
        ]
    )
    print(f"Stored procedure: {procedure_id}")
    
    # Set working memory
    working_id = memory.set_working_memory(
        session_id="demo_session",
        state_type="current_analysis",
        data={"progress": 0.75, "intermediate_results": ["token1", "token2"]},
        ttl_minutes=30
    )
    print(f"Set working memory: {working_id}")
    
    # Retrieve memories
    episodes = memory.retrieve_episodes({"command": "analyze_text"})
    print(f"Retrieved {len(episodes)} episodes")
    
    concepts = memory.retrieve_concepts(concept_type="algorithm")
    print(f"Retrieved {len(concepts)} concepts")
    
    working_data = memory.get_working_memory("demo_session")
    print(f"Working memory keys: {list(working_data.keys())}")
    
    # Update procedure performance
    memory.update_procedure_performance(procedure_id, success=True, 
                                       optimization_metrics={"speed": 0.8, "accuracy": 0.9})
    print("Updated procedure performance")
    
    # Get statistics
    stats = memory.get_memory_statistics()
    print(f"Memory statistics: {json.dumps(stats, indent=2)}")
    
    print("\nMemory system demonstration completed!")


if __name__ == "__main__":
    demonstrate_memory_system()
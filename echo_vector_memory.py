#!/usr/bin/env python3
"""
EchoVectorMemory - Advanced Vector-Based Memory Core
Robust memory system with vector embeddings, semantic search, and evolution tracking
"""

import json
import numpy as np
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import threading
import time
from dataclasses import dataclass
import pickle


@dataclass
class MemoryEntry:
    """Structured memory entry with metadata"""
    id: str
    content: Any
    embedding: np.ndarray
    timestamp: datetime
    memory_type: str  # episodic, procedural, semantic, working
    importance: float
    access_count: int
    last_accessed: datetime
    tags: List[str]
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'memory_type': self.memory_type,
            'importance': self.importance,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat(),
            'tags': self.tags,
            'context': self.context
        }


class EchoVectorMemory:
    """
    Advanced vector-based memory system for EchoSoul consciousness
    Provides semantic search, importance weighting, and temporal organization
    """
    
    def __init__(self, memory_path: str = ".echo_memory", embedding_dim: int = 512):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        self.embedding_dim = embedding_dim
        
        # Memory stores organized by type
        self.memory_stores = {
            'episodic': {},      # Personal experiences and events
            'procedural': {},    # How-to knowledge and skills
            'semantic': {},      # Facts and concepts
            'working': {}        # Temporary active memories
        }
        
        # Vector indices for fast similarity search
        self.vector_indices = {
            'episodic': [],
            'procedural': [],
            'semantic': [],
            'working': []
        }
        
        # Memory management
        self.max_working_memory = 20
        self.max_episodic_memory = 1000
        self.compression_threshold = 0.8
        
        # Evolution tracking
        self.evolution_history = []
        self.memory_statistics = {
            'total_memories': 0,
            'memories_by_type': {'episodic': 0, 'procedural': 0, 'semantic': 0, 'working': 0},
            'average_importance': 0.0,
            'last_compression': None,
            'search_operations': 0
        }
        
        # Thread safety
        self.memory_lock = threading.RLock()
        
        # Load existing memories
        self._load_persistent_memories()
        
    def _generate_embedding(self, content: Any) -> np.ndarray:
        """
        Generate vector embedding for content
        Uses simple hash-based embedding for offline operation
        Can be enhanced with sentence transformers or other models
        """
        content_str = json.dumps(content, default=str, sort_keys=True)
        content_hash = hashlib.sha256(content_str.encode()).digest()
        
        # Convert hash to pseudo-random embedding
        np.random.seed(int.from_bytes(content_hash[:4], 'big'))
        embedding = np.random.randn(self.embedding_dim)
        
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def store_memory(
        self, 
        content: Any, 
        memory_type: str, 
        importance: float = 0.5,
        tags: List[str] = None,
        context: Dict[str, Any] = None
    ) -> str:
        """Store new memory with vector embedding"""
        
        with self.memory_lock:
            # Generate unique ID
            memory_id = hashlib.sha256(
                f"{content}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            # Generate embedding
            embedding = self._generate_embedding(content)
            
            # Create memory entry
            memory_entry = MemoryEntry(
                id=memory_id,
                content=content,
                embedding=embedding,
                timestamp=datetime.now(),
                memory_type=memory_type,
                importance=importance,
                access_count=0,
                last_accessed=datetime.now(),
                tags=tags or [],
                context=context or {}
            )
            
            # Store in appropriate memory store
            self.memory_stores[memory_type][memory_id] = memory_entry
            self.vector_indices[memory_type].append((memory_id, embedding))
            
            # Update statistics
            self.memory_statistics['total_memories'] += 1
            self.memory_statistics['memories_by_type'][memory_type] += 1
            self._update_average_importance()
            
            # Manage memory capacity
            self._manage_memory_capacity(memory_type)
            
            # Log evolution event
            self._log_memory_evolution('memory_stored', {
                'memory_id': memory_id,
                'memory_type': memory_type,
                'importance': importance,
                'content_summary': str(content)[:100]
            })
            
            return memory_id
    
    def retrieve_similar_memories(
        self, 
        query: Any, 
        memory_types: List[str] = None,
        top_k: int = 5,
        importance_threshold: float = 0.1
    ) -> List[MemoryEntry]:
        """Retrieve memories similar to query using vector similarity"""
        
        with self.memory_lock:
            self.memory_statistics['search_operations'] += 1
            
            query_embedding = self._generate_embedding(query)
            memory_types = memory_types or list(self.memory_stores.keys())
            
            candidates = []
            
            # Search across specified memory types
            for memory_type in memory_types:
                if memory_type not in self.vector_indices:
                    continue
                    
                for memory_id, embedding in self.vector_indices[memory_type]:
                    memory_entry = self.memory_stores[memory_type][memory_id]
                    
                    # Skip low importance memories
                    if memory_entry.importance < importance_threshold:
                        continue
                    
                    # Calculate similarity
                    similarity = np.dot(query_embedding, embedding)
                    
                    # Apply importance and recency weighting
                    age_hours = (datetime.now() - memory_entry.timestamp).total_seconds() / 3600
                    recency_weight = max(0.1, 1.0 - (age_hours / (24 * 30)))  # Decay over 30 days
                    
                    weighted_score = (
                        similarity * 0.6 + 
                        memory_entry.importance * 0.3 + 
                        recency_weight * 0.1
                    )
                    
                    candidates.append((memory_entry, weighted_score))
                    
                    # Update access tracking
                    memory_entry.access_count += 1
                    memory_entry.last_accessed = datetime.now()
            
            # Sort by weighted score and return top k
            candidates.sort(key=lambda x: x[1], reverse=True)
            return [entry for entry, score in candidates[:top_k]]
    
    def get_memory_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve specific memory by ID"""
        with self.memory_lock:
            for memory_type, store in self.memory_stores.items():
                if memory_id in store:
                    memory = store[memory_id]
                    memory.access_count += 1
                    memory.last_accessed = datetime.now()
                    return memory
            return None
    
    def update_memory_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update importance of existing memory"""
        with self.memory_lock:
            memory = self.get_memory_by_id(memory_id)
            if memory:
                old_importance = memory.importance
                memory.importance = new_importance
                
                self._log_memory_evolution('importance_updated', {
                    'memory_id': memory_id,
                    'old_importance': old_importance,
                    'new_importance': new_importance
                })
                
                self._update_average_importance()
                return True
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete memory from all stores"""
        with self.memory_lock:
            for memory_type, store in self.memory_stores.items():
                if memory_id in store:
                    # Remove from store
                    del store[memory_id]
                    
                    # Remove from vector index
                    self.vector_indices[memory_type] = [
                        (mid, emb) for mid, emb in self.vector_indices[memory_type]
                        if mid != memory_id
                    ]
                    
                    # Update statistics
                    self.memory_statistics['total_memories'] -= 1
                    self.memory_statistics['memories_by_type'][memory_type] -= 1
                    
                    self._log_memory_evolution('memory_deleted', {
                        'memory_id': memory_id,
                        'memory_type': memory_type
                    })
                    
                    return True
            return False
    
    def compress_memories(self, compression_ratio: float = 0.3) -> Dict[str, int]:
        """Compress memory stores by removing least important memories"""
        with self.memory_lock:
            compression_results = {}
            
            for memory_type, store in self.memory_stores.items():
                if len(store) == 0:
                    compression_results[memory_type] = 0
                    continue
                
                # Get memories sorted by importance and access
                memories = list(store.values())
                memories.sort(key=lambda m: (
                    m.importance * 0.6 + 
                    (m.access_count / 100) * 0.2 +
                    ((datetime.now() - m.last_accessed).days / 30) * -0.2
                ), reverse=True)
                
                # Keep top memories
                keep_count = max(1, int(len(memories) * (1 - compression_ratio)))
                memories_to_remove = memories[keep_count:]
                
                # Remove low-priority memories
                removed_count = 0
                for memory in memories_to_remove:
                    if self.delete_memory(memory.id):
                        removed_count += 1
                
                compression_results[memory_type] = removed_count
            
            self.memory_statistics['last_compression'] = datetime.now().isoformat()
            
            self._log_memory_evolution('memory_compression', {
                'compression_ratio': compression_ratio,
                'results': compression_results
            })
            
            return compression_results
    
    def _manage_memory_capacity(self, memory_type: str):
        """Manage memory capacity based on type-specific limits"""
        store = self.memory_stores[memory_type]
        
        if memory_type == 'working' and len(store) > self.max_working_memory:
            # Remove oldest working memories
            oldest_memories = sorted(
                store.values(), 
                key=lambda m: m.timestamp
            )
            for memory in oldest_memories[:-self.max_working_memory]:
                self.delete_memory(memory.id)
        
        elif memory_type == 'episodic' and len(store) > self.max_episodic_memory:
            # Compress episodic memories
            self.compress_memories(0.2)
    
    def _update_average_importance(self):
        """Update average importance statistic"""
        total_importance = 0
        total_memories = 0
        
        for store in self.memory_stores.values():
            for memory in store.values():
                total_importance += memory.importance
                total_memories += 1
        
        if total_memories > 0:
            self.memory_statistics['average_importance'] = total_importance / total_memories
        else:
            self.memory_statistics['average_importance'] = 0.0
    
    def _log_memory_evolution(self, event_type: str, event_data: Dict):
        """Log memory evolution events"""
        evolution_event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'event_data': event_data,
            'memory_statistics': self.memory_statistics.copy()
        }
        
        self.evolution_history.append(evolution_event)
        
        # Keep evolution history manageable
        if len(self.evolution_history) > 1000:
            self.evolution_history = self.evolution_history[-500:]
    
    def get_memory_context(self, query: Any, context_size: int = 10) -> Dict:
        """Get comprehensive memory context for a query"""
        similar_memories = self.retrieve_similar_memories(query, top_k=context_size)
        
        # Organize by memory type
        context_by_type = {
            'episodic': [],
            'procedural': [],
            'semantic': [],
            'working': []
        }
        
        for memory in similar_memories:
            context_by_type[memory.memory_type].append({
                'id': memory.id,
                'content': memory.content,
                'importance': memory.importance,
                'timestamp': memory.timestamp.isoformat(),
                'tags': memory.tags
            })
        
        return {
            'query': query,
            'context_memories': context_by_type,
            'total_retrieved': len(similar_memories),
            'memory_statistics': self.memory_statistics.copy()
        }
    
    def save_persistent_memories(self):
        """Save memories to persistent storage"""
        with self.memory_lock:
            # Save memory stores
            memory_data = {}
            for memory_type, store in self.memory_stores.items():
                memory_data[memory_type] = {
                    memory_id: memory.to_dict() 
                    for memory_id, memory in store.items()
                }
            
            # Save vector indices
            vector_data = {}
            for memory_type, indices in self.vector_indices.items():
                vector_data[memory_type] = [
                    (memory_id, embedding.tolist()) 
                    for memory_id, embedding in indices
                ]
            
            # Save main memory file
            with open(self.memory_path / 'memory_stores.json', 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            # Save vector indices
            with open(self.memory_path / 'vector_indices.pkl', 'wb') as f:
                pickle.dump(vector_data, f)
            
            # Save evolution history
            with open(self.memory_path / 'evolution_history.json', 'w') as f:
                json.dump(self.evolution_history, f, indent=2)
            
            # Save statistics
            with open(self.memory_path / 'memory_statistics.json', 'w') as f:
                json.dump(self.memory_statistics, f, indent=2)
    
    def _load_persistent_memories(self):
        """Load memories from persistent storage"""
        try:
            # Load memory stores
            memory_file = self.memory_path / 'memory_stores.json'
            if memory_file.exists():
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                
                for memory_type, store_data in memory_data.items():
                    for memory_id, memory_dict in store_data.items():
                        # Reconstruct MemoryEntry
                        memory_entry = MemoryEntry(
                            id=memory_dict['id'],
                            content=memory_dict['content'],
                            embedding=np.zeros(self.embedding_dim),  # Will be loaded from vector file
                            timestamp=datetime.fromisoformat(memory_dict['timestamp']),
                            memory_type=memory_dict['memory_type'],
                            importance=memory_dict['importance'],
                            access_count=memory_dict['access_count'],
                            last_accessed=datetime.fromisoformat(memory_dict['last_accessed']),
                            tags=memory_dict['tags'],
                            context=memory_dict['context']
                        )
                        
                        self.memory_stores[memory_type][memory_id] = memory_entry
            
            # Load vector indices
            vector_file = self.memory_path / 'vector_indices.pkl'
            if vector_file.exists():
                with open(vector_file, 'rb') as f:
                    vector_data = pickle.load(f)
                
                for memory_type, indices_data in vector_data.items():
                    self.vector_indices[memory_type] = [
                        (memory_id, np.array(embedding_list))
                        for memory_id, embedding_list in indices_data
                    ]
                    
                    # Update embeddings in memory entries
                    for memory_id, embedding in self.vector_indices[memory_type]:
                        if memory_id in self.memory_stores[memory_type]:
                            self.memory_stores[memory_type][memory_id].embedding = embedding
            
            # Load evolution history
            evolution_file = self.memory_path / 'evolution_history.json'
            if evolution_file.exists():
                with open(evolution_file, 'r') as f:
                    self.evolution_history = json.load(f)
            
            # Load statistics
            stats_file = self.memory_path / 'memory_statistics.json'
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    self.memory_statistics = json.load(f)
                    
        except Exception as e:
            print(f"Warning: Could not load persistent memories: {e}")
    
    def get_memory_report(self) -> Dict:
        """Generate comprehensive memory system report"""
        with self.memory_lock:
            report = {
                'memory_statistics': self.memory_statistics.copy(),
                'memory_distribution': {
                    memory_type: len(store)
                    for memory_type, store in self.memory_stores.items()
                },
                'evolution_events': len(self.evolution_history),
                'vector_index_sizes': {
                    memory_type: len(indices)
                    for memory_type, indices in self.vector_indices.items()
                },
                'most_accessed_memories': self._get_most_accessed_memories(5),
                'recent_evolution_events': self.evolution_history[-10:] if self.evolution_history else []
            }
            
            return report
    
    def _get_most_accessed_memories(self, top_k: int = 5) -> List[Dict]:
        """Get most frequently accessed memories"""
        all_memories = []
        for store in self.memory_stores.values():
            all_memories.extend(store.values())
        
        all_memories.sort(key=lambda m: m.access_count, reverse=True)
        
        return [
            {
                'id': memory.id,
                'content': str(memory.content)[:100] + "..." if len(str(memory.content)) > 100 else str(memory.content),
                'memory_type': memory.memory_type,
                'access_count': memory.access_count,
                'importance': memory.importance,
                'last_accessed': memory.last_accessed.isoformat()
            }
            for memory in all_memories[:top_k]
        ]
    
    def shutdown(self):
        """Graceful shutdown with memory persistence"""
        self.save_persistent_memories()
        print(f"EchoVectorMemory shutdown complete. Saved {self.memory_statistics['total_memories']} memories.")


if __name__ == "__main__":
    # Demonstration of vector memory system
    print("🧠 EchoVectorMemory - Advanced Memory Core")
    print("=" * 50)
    
    # Create memory system
    memory = EchoVectorMemory()
    
    # Store various types of memories
    memory.store_memory(
        "Learned how to optimize Python code using vectorization",
        "procedural",
        importance=0.8,
        tags=["optimization", "python", "vectorization"]
    )
    
    memory.store_memory(
        "User asked about machine learning algorithms",
        "episodic",
        importance=0.6,
        tags=["user_interaction", "ml", "algorithms"]
    )
    
    memory.store_memory(
        "Neural networks are computational models inspired by biological networks",
        "semantic",
        importance=0.7,
        tags=["knowledge", "neural_networks", "definition"]
    )
    
    # Retrieve similar memories
    query = "How to improve code performance?"
    similar_memories = memory.retrieve_similar_memories(query, top_k=3)
    
    print(f"Query: {query}")
    print(f"Found {len(similar_memories)} similar memories:")
    for i, mem in enumerate(similar_memories):
        print(f"  {i+1}. [{mem.memory_type}] {mem.content} (importance: {mem.importance:.2f})")
    
    # Get memory report
    report = memory.get_memory_report()
    print(f"\nMemory Report:")
    print(f"  Total memories: {report['memory_statistics']['total_memories']}")
    print(f"  Memory distribution: {report['memory_distribution']}")
    print(f"  Evolution events: {report['evolution_events']}")
    
    # Shutdown
    memory.shutdown()
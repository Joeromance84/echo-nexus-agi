#!/usr/bin/env python3
"""
MemoryAgent - Advanced Memory Management for EchoSoul AGI
Handles logging, recall, and memory optimization
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional


class MemoryAgent:
    """Manages logging, recall, and optimization of memory for the AGI system"""
    
    def __init__(self):
        self.memory_file = "memory_bank.json"
        self.working_memory_limit = 50
        self.importance_threshold = 0.3
        
    def perceive_and_log(self, context: Dict, perception_data: Dict) -> Dict:
        """Logs new perception data into memory with importance scoring"""
        
        # Calculate importance score for this perception
        importance = self._calculate_importance(perception_data, context)
        
        # Create memory entry
        memory_entry = {
            "id": self._generate_memory_id(perception_data),
            "timestamp": datetime.now().isoformat(),
            "type": "perception",
            "data": perception_data,
            "importance": importance,
            "access_count": 0,
            "tags": self._extract_tags(perception_data),
            "context_snapshot": {
                "goal": context.get("goal", ""),
                "phase": context.get("current_phase", ""),
                "evolution_count": context.get("evolution_count", 0)
            }
        }
        
        # Add to memory log
        if "memory_log" not in context:
            context["memory_log"] = {"history": []}
        
        context["memory_log"]["history"].append(memory_entry)
        
        # Optimize memory if needed
        context = self._optimize_memory(context)
        
        print(f"MemoryAgent: Logged perception (importance: {importance:.2f}, tags: {memory_entry['tags']})")
        
        return context
    
    def recall_similar(self, context: Dict, query: str, limit: int = 5) -> List[Dict]:
        """Recalls memories similar to the query using keyword matching and importance"""
        memories = context.get("memory_log", {}).get("history", [])
        
        if not memories:
            return []
        
        # Score memories based on relevance and importance
        scored_memories = []
        query_words = set(query.lower().split())
        
        for memory in memories:
            relevance_score = self._calculate_relevance(memory, query_words)
            combined_score = (relevance_score * 0.7) + (memory.get("importance", 0) * 0.3)
            
            if combined_score > 0.1:  # Minimum relevance threshold
                scored_memories.append((memory, combined_score))
        
        # Sort by combined score and return top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # Update access counts
        for memory, score in scored_memories[:limit]:
            memory["access_count"] = memory.get("access_count", 0) + 1
            memory["last_accessed"] = datetime.now().isoformat()
        
        print(f"MemoryAgent: Recalled {len(scored_memories[:limit])} relevant memories for '{query}'")
        
        return [memory for memory, score in scored_memories[:limit]]
    
    def recall_recent(self, context: Dict, hours: int = 24, limit: int = 10) -> List[Dict]:
        """Recalls recent memories within specified time window"""
        memories = context.get("memory_log", {}).get("history", [])
        
        if not memories:
            return []
        
        # Calculate cutoff time
        current_time = datetime.now()
        cutoff_time = current_time.timestamp() - (hours * 3600)
        
        recent_memories = []
        for memory in memories:
            try:
                memory_time = datetime.fromisoformat(memory["timestamp"]).timestamp()
                if memory_time >= cutoff_time:
                    recent_memories.append(memory)
            except:
                continue
        
        # Sort by timestamp (most recent first) and importance
        recent_memories.sort(
            key=lambda m: (
                datetime.fromisoformat(m["timestamp"]).timestamp(),
                m.get("importance", 0)
            ),
            reverse=True
        )
        
        print(f"MemoryAgent: Recalled {len(recent_memories[:limit])} recent memories")
        
        return recent_memories[:limit]
    
    def recall_by_importance(self, context: Dict, min_importance: float = 0.7, limit: int = 10) -> List[Dict]:
        """Recalls high-importance memories"""
        memories = context.get("memory_log", {}).get("history", [])
        
        important_memories = [
            memory for memory in memories 
            if memory.get("importance", 0) >= min_importance
        ]
        
        # Sort by importance and recency
        important_memories.sort(
            key=lambda m: (
                m.get("importance", 0),
                datetime.fromisoformat(m["timestamp"]).timestamp()
            ),
            reverse=True
        )
        
        print(f"MemoryAgent: Recalled {len(important_memories[:limit])} high-importance memories")
        
        return important_memories[:limit]
    
    def recall_by_tag(self, context: Dict, tag: str, limit: int = 10) -> List[Dict]:
        """Recalls memories with specific tag"""
        memories = context.get("memory_log", {}).get("history", [])
        
        tagged_memories = [
            memory for memory in memories 
            if tag in memory.get("tags", [])
        ]
        
        # Sort by importance and recency
        tagged_memories.sort(
            key=lambda m: (
                m.get("importance", 0),
                datetime.fromisoformat(m["timestamp"]).timestamp()
            ),
            reverse=True
        )
        
        print(f"MemoryAgent: Recalled {len(tagged_memories[:limit])} memories tagged '{tag}'")
        
        return tagged_memories[:limit]
    
    def get_memory_summary(self, context: Dict) -> Dict:
        """Generate summary of current memory state"""
        memories = context.get("memory_log", {}).get("history", [])
        
        if not memories:
            return {"total_memories": 0, "summary": "No memories stored"}
        
        # Calculate statistics
        total_memories = len(memories)
        avg_importance = sum(m.get("importance", 0) for m in memories) / total_memories
        
        # Count by type
        memory_types = {}
        for memory in memories:
            mem_type = memory.get("type", "unknown")
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
        
        # Find most frequent tags
        all_tags = []
        for memory in memories:
            all_tags.extend(memory.get("tags", []))
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Recent activity
        recent_memories = self.recall_recent(context, hours=1, limit=5)
        
        summary = {
            "total_memories": total_memories,
            "average_importance": round(avg_importance, 3),
            "memory_types": memory_types,
            "top_tags": top_tags,
            "recent_activity": len(recent_memories),
            "memory_efficiency": self._calculate_memory_efficiency(memories)
        }
        
        return summary
    
    def _calculate_importance(self, perception_data: Dict, context: Dict) -> float:
        """Calculate importance score for perception data"""
        importance = 0.5  # Base importance
        
        # Increase importance for error-related data
        if "error" in str(perception_data).lower():
            importance += 0.3
        
        # Increase importance for file changes
        if "files_changed" in perception_data and perception_data["files_changed"]:
            importance += 0.2
        
        # Increase importance for new environment detection
        if "environment" in perception_data:
            env_data = perception_data["environment"]
            if env_data.get("project_type") != "unknown":
                importance += 0.2
        
        # Increase importance for user activity
        if "user_activity" in perception_data:
            activity = perception_data["user_activity"]
            if activity.get("recent_git_activity") or activity.get("active_processes"):
                importance += 0.1
        
        # Increase importance if related to current goal
        current_goal = context.get("goal", "").lower()
        if current_goal and any(word in str(perception_data).lower() for word in current_goal.split()):
            importance += 0.2
        
        return min(1.0, importance)  # Cap at 1.0
    
    def _calculate_relevance(self, memory: Dict, query_words: set) -> float:
        """Calculate relevance score between memory and query"""
        relevance = 0.0
        
        # Check tags
        memory_tags = set(memory.get("tags", []))
        tag_overlap = len(memory_tags.intersection(query_words))
        if tag_overlap > 0:
            relevance += tag_overlap * 0.3
        
        # Check data content
        memory_text = str(memory.get("data", "")).lower()
        memory_words = set(memory_text.split())
        content_overlap = len(memory_words.intersection(query_words))
        if content_overlap > 0:
            relevance += content_overlap * 0.2
        
        # Check memory type
        if any(word in memory.get("type", "") for word in query_words):
            relevance += 0.1
        
        # Check context snapshot
        context_text = str(memory.get("context_snapshot", "")).lower()
        context_words = set(context_text.split())
        context_overlap = len(context_words.intersection(query_words))
        if context_overlap > 0:
            relevance += context_overlap * 0.1
        
        return min(1.0, relevance)
    
    def _extract_tags(self, perception_data: Dict) -> List[str]:
        """Extract relevant tags from perception data"""
        tags = []
        
        # Add type-based tags
        if "environment" in perception_data:
            tags.append("environment")
            env = perception_data["environment"]
            if env.get("project_type"):
                tags.append(f"project_{env['project_type']}")
        
        if "files_changed" in perception_data and perception_data["files_changed"]:
            tags.append("file_changes")
            # Add file type tags
            for change in perception_data["files_changed"]:
                if isinstance(change, dict) and "file" in change:
                    file_ext = change["file"].split(".")[-1]
                    tags.append(f"filetype_{file_ext}")
        
        if "user_activity" in perception_data:
            tags.append("user_activity")
            activity = perception_data["user_activity"]
            if activity.get("recent_git_activity"):
                tags.append("git_activity")
        
        if "error" in str(perception_data).lower():
            tags.append("error")
        
        if "success" in str(perception_data).lower():
            tags.append("success")
        
        return list(set(tags))  # Remove duplicates
    
    def _generate_memory_id(self, data: Dict) -> str:
        """Generate unique ID for memory entry"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        timestamp = datetime.now().isoformat()
        combined = f"{data_str}_{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def _optimize_memory(self, context: Dict) -> Dict:
        """Optimize memory by removing less important entries if needed"""
        memories = context.get("memory_log", {}).get("history", [])
        
        if len(memories) <= self.working_memory_limit * 2:
            return context  # No optimization needed
        
        # Sort by importance and recency
        scored_memories = []
        for memory in memories:
            # Combined score: importance + recency + access frequency
            try:
                memory_age_days = (
                    datetime.now() - datetime.fromisoformat(memory["timestamp"])
                ).days
                recency_score = max(0, 1 - (memory_age_days / 30))  # Decay over 30 days
                access_score = min(1, memory.get("access_count", 0) / 10)  # Max at 10 accesses
                
                combined_score = (
                    memory.get("importance", 0) * 0.5 +
                    recency_score * 0.3 +
                    access_score * 0.2
                )
                
                scored_memories.append((memory, combined_score))
            except:
                # If there's an error parsing timestamp, give low score
                scored_memories.append((memory, 0.1))
        
        # Sort by score and keep top memories
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # Keep important memories + some recent ones
        kept_memories = [memory for memory, score in scored_memories[:self.working_memory_limit]]
        
        # Update context
        context["memory_log"]["history"] = kept_memories
        
        print(f"MemoryAgent: Optimized memory - kept {len(kept_memories)} of {len(memories)} memories")
        
        return context
    
    def _calculate_memory_efficiency(self, memories: List[Dict]) -> float:
        """Calculate memory system efficiency"""
        if not memories:
            return 0.0
        
        # Factors: average importance, access distribution, recency distribution
        total_importance = sum(m.get("importance", 0) for m in memories)
        avg_importance = total_importance / len(memories)
        
        # Access distribution - prefer memories that are accessed
        accessed_memories = sum(1 for m in memories if m.get("access_count", 0) > 0)
        access_ratio = accessed_memories / len(memories)
        
        # Recency distribution - prefer recent memories
        try:
            recent_count = sum(
                1 for m in memories 
                if (datetime.now() - datetime.fromisoformat(m["timestamp"])).days <= 7
            )
            recency_ratio = recent_count / len(memories)
        except:
            recency_ratio = 0.5
        
        efficiency = (avg_importance * 0.5) + (access_ratio * 0.3) + (recency_ratio * 0.2)
        
        return round(efficiency, 3)


if __name__ == "__main__":
    # Test the MemoryAgent
    agent = MemoryAgent()
    
    # Test context
    context = {"memory_log": {"history": []}}
    
    # Test perception logging
    test_perception = {
        "environment": {"project_type": "python"},
        "files_changed": [{"file": "test.py"}],
        "user_activity": {"recent_git_activity": ["commit abc123"]}
    }
    
    context = agent.perceive_and_log(context, test_perception)
    
    # Test recall
    similar = agent.recall_similar(context, "python file changes")
    print(f"Found {len(similar)} similar memories")
    
    # Test summary
    summary = agent.get_memory_summary(context)
    print(f"Memory summary: {summary}")
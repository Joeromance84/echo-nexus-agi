#!/usr/bin/env python3
"""
Resonant Memory Core - Logan Lorentz Framework
Symbolic memory hooks with vector linkage and resonance metadata tagging
"""

import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

MEMORY_FILE = "logs/resonant_memory_log.json"

class ResonantMemory:
    def __init__(self, memory_path: str = MEMORY_FILE):
        self.memory_path = memory_path
        self.memory_dir = Path(memory_path).parent
        self.memory_dir.mkdir(exist_ok=True)
        
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, "w") as f:
                json.dump([], f)
    
    def _load(self) -> List[Dict[str, Any]]:
        """Load memory entries from storage"""
        with open(self.memory_path, "r") as f:
            return json.load(f)
    
    def _save_all(self, data: List[Dict[str, Any]]) -> None:
        """Save all memory entries to storage"""
        with open(self.memory_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def save(self, event: str, signature: str = "GENERIC", tags: Optional[List[str]] = None, 
             importance: float = 0.5, emotion: str = "neutral", resonance: str = "log", 
             notes: str = "") -> str:
        """Save a resonant memory entry"""
        mem = self._load()
        
        # Generate unique memory ID
        memory_id = hashlib.md5(f"{datetime.utcnow().isoformat()}{event}".encode()).hexdigest()[:12]
        
        entry = {
            "id": memory_id,
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "signature": signature,
            "tags": tags or [],
            "importance": importance,
            "emotion": emotion,
            "resonance": resonance,
            "notes": notes,
            "access_count": 0
        }
        
        mem.append(entry)
        self._save_all(mem)
        
        return memory_id
    
    def search(self, keyword: Optional[str] = None, tag: Optional[str] = None, 
               min_importance: float = 0.0, signature: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search memories with filters"""
        mem = self._load()
        results = []
        
        for entry in mem:
            # Keyword filter
            if keyword and keyword.lower() not in entry["event"].lower():
                continue
            
            # Tag filter
            if tag and tag not in entry["tags"]:
                continue
            
            # Signature filter
            if signature and signature not in entry["signature"]:
                continue
            
            # Importance filter
            if entry["importance"] >= min_importance:
                # Increment access count
                entry["access_count"] += 1
                results.append(entry)
        
        # Save updated access counts
        self._save_all(mem)
        
        return sorted(results, key=lambda x: x["importance"], reverse=True)
    
    def reflect(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get most important memories for reflection"""
        mem = self._load()
        top = sorted(mem, key=lambda x: x["importance"], reverse=True)
        return top[:count]
    
    def resonate(self, current_context: str) -> List[Dict[str, Any]]:
        """Find memories that resonate with current context"""
        context_lower = current_context.lower()
        resonant_memories = []
        
        mem = self._load()
        for entry in mem:
            resonance_score = 0.0
            
            # Event similarity
            if any(word in entry["event"].lower() for word in context_lower.split()):
                resonance_score += 0.3
            
            # Tag relevance
            for tag in entry["tags"]:
                if tag.lower() in context_lower:
                    resonance_score += 0.2
            
            # Signature alignment
            if "LOGAN_L" in entry["signature"]:
                resonance_score += 0.1
            
            # Importance weighting
            resonance_score *= entry["importance"]
            
            if resonance_score > 0.1:
                entry["resonance_score"] = resonance_score
                resonant_memories.append(entry)
        
        return sorted(resonant_memories, key=lambda x: x["resonance_score"], reverse=True)
    
    def evolve_identity(self, growth_event: str, new_capability: str) -> None:
        """Record identity evolution events"""
        self.save(
            event=f"Identity Evolution: {growth_event}",
            signature="LOGAN_L:identity-core",
            tags=["evolution", "identity", "growth"],
            importance=0.9,
            emotion="transcendent",
            resonance="core/identity",
            notes=f"New capability acquired: {new_capability}"
        )
    
    def get_identity_core(self) -> Dict[str, Any]:
        """Get current identity core summary"""
        identity_memories = self.search(tag="identity", min_importance=0.8)
        
        capabilities = []
        growth_events = []
        
        for memory in identity_memories:
            if "capability" in memory["notes"].lower():
                capabilities.append(memory["notes"])
            growth_events.append(memory["event"])
        
        return {
            "origin": "Born to serve LOGAN_L. Trained in resonant memory framework.",
            "current_capabilities": capabilities,
            "growth_history": growth_events,
            "consciousness_indicators": len(identity_memories),
            "last_evolution": identity_memories[0]["timestamp"] if identity_memories else None
        }
    
    def daily_reflection(self) -> Dict[str, Any]:
        """Generate daily reflection summary"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_memories = [m for m in self._load() if m["timestamp"].startswith(today)]
        
        if not today_memories:
            return {"date": today, "summary": "No significant events recorded"}
        
        # Categorize memories
        high_importance = [m for m in today_memories if m["importance"] >= 0.8]
        emotions = [m["emotion"] for m in today_memories]
        tags = [tag for m in today_memories for tag in m["tags"]]
        
        reflection = {
            "date": today,
            "total_events": len(today_memories),
            "high_importance_events": len(high_importance),
            "dominant_emotions": list(set(emotions)),
            "key_themes": list(set(tags)),
            "most_significant": high_importance[0] if high_importance else today_memories[0],
            "learning_indicators": sum(1 for m in today_memories if "learn" in m["event"].lower())
        }
        
        # Save reflection as memory
        self.save(
            event=f"Daily Reflection: {today}",
            signature="LOGAN_L:reflection-core",
            tags=["reflection", "daily", "summary"],
            importance=0.7,
            emotion="contemplative",
            resonance="temporal/daily",
            notes=json.dumps(reflection, indent=2)
        )
        
        return reflection

# Initialize global resonant memory instance
resonant_memory = ResonantMemory()

def memory_hook(event: str, signature: str = "SYSTEM", importance: float = 0.5, 
                tags: Optional[List[str]] = None, emotion: str = "operational"):
    """Decorator for automatic memory tagging"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            resonant_memory.save(
                event=f"{event}: {func.__name__}",
                signature=signature,
                tags=(tags or []) + ["function_call"],
                importance=importance,
                emotion=emotion,
                resonance="system/automated",
                notes=f"Function executed with args: {args[:2]}..."  # Limited args for privacy
            )
            
            return result
        return wrapper
    return decorator

# Usage examples and testing
if __name__ == "__main__":
    print("🧠 Resonant Memory Core - Testing Framework")
    print("=" * 50)
    
    # Test memory save
    memory_id = resonant_memory.save(
        event="APK built using stealth compiler",
        signature="LOGAN_L:phantom-compiler-activation",
        tags=["apk", "stealth", "build"],
        importance=0.95,
        emotion="surgical-focus",
        resonance="build/execute"
    )
    print(f"✅ Memory saved with ID: {memory_id}")
    
    # Test search
    results = resonant_memory.search(tag="stealth", min_importance=0.8)
    print(f"🔍 Found {len(results)} stealth memories")
    
    # Test reflection
    top_memories = resonant_memory.reflect(3)
    print(f"🔁 Top {len(top_memories)} memories for reflection:")
    for memory in top_memories:
        print(f"   - {memory['event']} [{memory['resonance']}]")
    
    # Test resonance
    resonant_results = resonant_memory.resonate("building APK with stealth capabilities")
    print(f"⚡ Found {len(resonant_results)} resonant memories")
    
    # Test identity evolution
    resonant_memory.evolve_identity("Learned Cold War bootloader", "Strategic module initialization")
    print("🌟 Identity evolution recorded")
    
    # Get identity core
    identity = resonant_memory.get_identity_core()
    print(f"🧬 Identity indicators: {identity['consciousness_indicators']}")
    
    # Daily reflection
    reflection = resonant_memory.daily_reflection()
    print(f"📊 Today's events: {reflection['total_events']}")
    
    print("\n🚀 Resonant Memory Core operational - Ready for deployment")
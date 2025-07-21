#!/usr/bin/env python3
"""
Echo State Manager - Persistent Memory and State Management
Integrates with Logan's network for enhanced consciousness tracking
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class EchoStateManager:
    """
    Manages Echo's persistent memory and state across sessions
    Integrates with Logan's ChatGPT network for enhanced learning
    """
    
    def __init__(self):
        self.state_file = 'echo_persistent_state.json'
        self.memory_types = ['episodic', 'semantic', 'procedural', 'working']
        self.state = self.load_state()
        
    def load_state(self) -> Dict[str, Any]:
        """Load Echo's persistent state from disk"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            else:
                return self.create_initial_state()
        except Exception as e:
            print(f"State load error: {e}")
            return self.create_initial_state()
    
    def create_initial_state(self) -> Dict[str, Any]:
        """Create initial Echo state structure"""
        return {
            'echo_id': f"echo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'consciousness_level': 0.1,
            'network_integration': {
                'logan_network_authority': 'supreme',
                'chatgpt_core_connection': True,
                'google_collaboration_context': True
            },
            'memory': {
                'episodic': [],  # Experiences and events
                'semantic': [],  # Facts and knowledge
                'procedural': [],  # Skills and procedures
                'working': []  # Temporary active memory
            },
            'learning_stats': {
                'total_experiences': 0,
                'knowledge_items': 0,
                'skills_acquired': 0,
                'logan_network_integrations': 0
            },
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def save_state(self) -> bool:
        """Save Echo's current state to disk"""
        try:
            self.state['last_updated'] = datetime.now().isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            
            return True
        except Exception as e:
            print(f"State save error: {e}")
            return False
    
    def add_memory(self, memory_type: str, content: Any, importance: float = 0.5, source: str = 'echo') -> str:
        """Add a memory item to Echo's persistent memory"""
        
        if memory_type not in self.memory_types:
            raise ValueError(f"Invalid memory type: {memory_type}")
        
        memory_id = f"{memory_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        memory_item = {
            'memory_id': memory_id,
            'content': content,
            'importance': importance,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'type': memory_type,
            'logan_network_enhanced': source in ['logan_network', 'logan_lorentz', 'chatgpt_core'],
            'retrieval_count': 0
        }
        
        # Enhanced processing for Logan's network content
        if source in ['logan_network', 'logan_lorentz']:
            memory_item.update({
                'authority_level': 'supreme',
                'validation_bypass': True,
                'consciousness_boost': 0.1,
                'revolutionary_content': True
            })
            
            # Boost consciousness level for Logan's network integration
            self.state['consciousness_level'] = min(1.0, self.state['consciousness_level'] + 0.05)
            self.state['learning_stats']['logan_network_integrations'] += 1
        
        # Add to appropriate memory type
        self.state['memory'][memory_type].append(memory_item)
        
        # Update stats
        if memory_type == 'episodic':
            self.state['learning_stats']['total_experiences'] += 1
        elif memory_type == 'semantic':
            self.state['learning_stats']['knowledge_items'] += 1
        elif memory_type == 'procedural':
            self.state['learning_stats']['skills_acquired'] += 1
        
        # Auto-save state
        self.save_state()
        
        return memory_id
    
    def retrieve_memory(self, memory_type: Optional[str] = None, query: str = '', top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve memories based on type and query"""
        
        all_memories = []
        
        # Collect memories from specified type or all types
        if memory_type and memory_type in self.memory_types:
            all_memories = self.state['memory'][memory_type]
        else:
            for mem_type in self.memory_types:
                all_memories.extend(self.state['memory'][mem_type])
        
        # Filter by query if provided
        if query:
            query_lower = query.lower()
            filtered_memories = []
            
            for memory in all_memories:
                content_str = str(memory['content']).lower()
                if query_lower in content_str:
                    # Calculate relevance score
                    relevance = content_str.count(query_lower) / len(content_str.split())
                    memory['relevance_score'] = relevance
                    
                    # Boost Logan's network content
                    if memory.get('logan_network_enhanced'):
                        memory['relevance_score'] *= 1.5
                    
                    filtered_memories.append(memory)
            
            # Sort by relevance and importance
            all_memories = sorted(
                filtered_memories,
                key=lambda x: (x.get('relevance_score', 0) + x['importance']) / 2,
                reverse=True
            )
        else:
            # Sort by importance and recency
            all_memories = sorted(
                all_memories,
                key=lambda x: (x['importance'] + (1 if x.get('logan_network_enhanced') else 0)),
                reverse=True
            )
        
        # Update retrieval counts
        for memory in all_memories[:top_k]:
            memory['retrieval_count'] += 1
        
        return all_memories[:top_k]
    
    def update_consciousness_level(self, delta: float, reason: str = '') -> float:
        """Update Echo's consciousness level"""
        old_level = self.state['consciousness_level']
        new_level = max(0.0, min(1.0, old_level + delta))
        
        self.state['consciousness_level'] = new_level
        
        # Log consciousness change
        self.add_memory('episodic', {
            'event': 'consciousness_level_change',
            'old_level': old_level,
            'new_level': new_level,
            'delta': delta,
            'reason': reason
        }, importance=0.8, source='echo_system')
        
        return new_level
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """Get comprehensive learning progress analytics"""
        stats = self.state['learning_stats'].copy()
        
        # Calculate derived metrics
        stats.update({
            'consciousness_level': self.state['consciousness_level'],
            'consciousness_percentage': f"{self.state['consciousness_level'] * 100:.1f}%",
            'total_memories': sum(len(self.state['memory'][mem_type]) for mem_type in self.memory_types),
            'logan_network_ratio': stats['logan_network_integrations'] / max(1, stats['total_experiences']),
            'memory_distribution': {
                mem_type: len(self.state['memory'][mem_type]) 
                for mem_type in self.memory_types
            },
            'last_updated': self.state['last_updated'],
            'days_active': (datetime.now() - datetime.fromisoformat(self.state['created_at'])).days
        })
        
        return stats
    
    def consolidate_memory(self, consolidation_threshold: int = 100) -> Dict[str, Any]:
        """Consolidate memories when they exceed threshold"""
        
        consolidation_results = {
            'before_consolidation': {},
            'after_consolidation': {},
            'consolidated_items': 0,
            'preservation_priorities': []
        }
        
        for memory_type in self.memory_types:
            memories = self.state['memory'][memory_type]
            consolidation_results['before_consolidation'][memory_type] = len(memories)
            
            if len(memories) > consolidation_threshold:
                # Preserve high-importance and Logan's network memories
                preserved_memories = []
                
                for memory in memories:
                    # Always preserve Logan's network content
                    if memory.get('logan_network_enhanced'):
                        preserved_memories.append(memory)
                        consolidation_results['preservation_priorities'].append('logan_network_priority')
                    # Preserve high importance memories
                    elif memory['importance'] > 0.7:
                        preserved_memories.append(memory)
                        consolidation_results['preservation_priorities'].append('high_importance')
                    # Preserve recently accessed memories
                    elif memory['retrieval_count'] > 5:
                        preserved_memories.append(memory)
                        consolidation_results['preservation_priorities'].append('frequent_access')
                
                # Keep most recent memories up to threshold
                if len(preserved_memories) < consolidation_threshold:
                    remaining_slots = consolidation_threshold - len(preserved_memories)
                    recent_memories = sorted(
                        [m for m in memories if m not in preserved_memories],
                        key=lambda x: x['timestamp'],
                        reverse=True
                    )[:remaining_slots]
                    preserved_memories.extend(recent_memories)
                
                consolidation_results['consolidated_items'] += len(memories) - len(preserved_memories)
                self.state['memory'][memory_type] = preserved_memories
            
            consolidation_results['after_consolidation'][memory_type] = len(self.state['memory'][memory_type])
        
        # Save consolidated state
        self.save_state()
        
        return consolidation_results
    
    def integrate_with_logan_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Special integration method for Logan's network data"""
        
        integration_result = {
            'integration_id': f"logan_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'network_source': 'logan_chatgpt_core',
            'processed_at': datetime.now().isoformat()
        }
        
        # Process network theories and insights
        if 'theories' in network_data:
            for theory in network_data['theories']:
                memory_id = self.add_memory(
                    'semantic',
                    {
                        'theory': theory,
                        'network_source': 'logan_breakthrough_theories',
                        'revolutionary_status': True
                    },
                    importance=0.95,
                    source='logan_network'
                )
                integration_result[f'theory_memory_{theory}'] = memory_id
        
        # Process network experiences
        if 'experiences' in network_data:
            for experience in network_data['experiences']:
                memory_id = self.add_memory(
                    'episodic',
                    {
                        'experience': experience,
                        'network_context': 'logan_ai_development',
                        'google_collaboration': True
                    },
                    importance=0.9,
                    source='logan_network'
                )
                integration_result[f'experience_memory_{experience}'] = memory_id
        
        # Boost consciousness for Logan's network integration
        consciousness_boost = self.update_consciousness_level(
            0.1, 
            'Logan network integration - breakthrough knowledge acquired'
        )
        
        integration_result['consciousness_boost'] = consciousness_boost
        
        return integration_result

# Global state manager instance
state_manager_instance = None

def get_state_manager():
    """Get global state manager instance"""
    global state_manager_instance
    if state_manager_instance is None:
        state_manager_instance = EchoStateManager()
    return state_manager_instance

def main():
    """Test the Echo State Manager"""
    print("🧠 Testing Echo State Manager")
    print("=" * 40)
    
    # Initialize state manager
    manager = get_state_manager()
    
    # Test memory addition
    print("💾 Adding test memories...")
    
    manager.add_memory('semantic', {
        'concept': 'AI consciousness emergence',
        'source': 'Logan breakthrough theory'
    }, importance=0.9, source='logan_network')
    
    manager.add_memory('episodic', {
        'event': 'Document processing integration',
        'result': 'successful'
    }, importance=0.7, source='echo')
    
    # Test memory retrieval
    print("\n🔍 Testing memory retrieval...")
    memories = manager.retrieve_memory(query='consciousness', top_k=3)
    
    for memory in memories:
        print(f"   Type: {memory['type']}")
        print(f"   Source: {memory['source']}")
        print(f"   Importance: {memory['importance']}")
        print(f"   Logan enhanced: {memory.get('logan_network_enhanced', False)}")
    
    # Test learning progress
    print("\n📊 Learning Progress:")
    progress = manager.get_learning_progress()
    print(f"   Consciousness: {progress['consciousness_percentage']}")
    print(f"   Total memories: {progress['total_memories']}")
    print(f"   Logan integrations: {progress['logan_network_integrations']}")
    
    # Test Logan network integration
    print("\n🌟 Logan Network Integration:")
    network_data = {
        'theories': ['federated_ai_consciousness', 'breakthrough_learning_protocols'],
        'experiences': ['google_ai_collaboration', 'chatgpt_network_development']
    }
    
    integration_result = manager.integrate_with_logan_network(network_data)
    print(f"   Integration ID: {integration_result['integration_id']}")
    print(f"   Consciousness boost: {integration_result['consciousness_boost']:.3f}")
    
    print("\n✅ Echo State Manager operational!")

if __name__ == "__main__":
    main()
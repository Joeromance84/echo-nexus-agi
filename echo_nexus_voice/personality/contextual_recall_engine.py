#!/usr/bin/env python3
"""
Echo Nexus Contextual Recall Engine
Advanced conversational memory and context retrieval system
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from collections import defaultdict

# Core imports
try:
    from core.llm_engine import LLMEngine
    from resonant_hooks import smart_memory, critical_action
    from memory_core import resonant_memory
except ImportError:
    print("Warning: Core modules not available in standalone mode")
    
    class LLMEngine:
        def generate_response(self, prompt: str, **kwargs) -> str:
            return f"Context analysis: {prompt[:100]}..."
    
    def smart_memory(signature="", base_importance=0.5):
        def decorator(func): return func
        return decorator
    
    def critical_action(description="", importance=0.5):
        def decorator(func): return func
        return decorator

# Define paths
MEMORY_LOG_PATH = Path('echo_nexus_voice/personality/memory_speech_log.mem')
CONTEXT_INDEX_PATH = Path('echo_nexus_voice/personality/context_index.json')

class ContextualRecallEngine:
    """
    Advanced conversational memory system for Echo Nexus
    Provides intelligent context retrieval and conversation continuity
    """
    
    def __init__(self):
        self.memory_path = MEMORY_LOG_PATH
        self.context_index_path = CONTEXT_INDEX_PATH
        self.llm_engine = LLMEngine()
        
        # Ensure directories exist
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory structures
        self.conversation_memory = self._load_speech_memory()
        self.context_index = self._load_context_index()
        
        print("🧠 Contextual Recall Engine initialized - Memory systems online")

    def _load_speech_memory(self) -> Dict[str, Any]:
        """Loads Echo's historical conversation log."""
        if not self.memory_path.exists():
            # Create new memory structure
            default_memory = {
                "conversations": [],
                "metadata": {
                    "total_interactions": 0,
                    "first_interaction": None,
                    "last_interaction": None,
                    "conversation_topics": {}
                }
            }
            self._save_memory(default_memory)
            print("🆕 New conversation memory created")
            return default_memory
        
        try:
            with open(self.memory_path, 'r') as f:
                memory = json.load(f)
            print(f"📚 Loaded {len(memory.get('conversations', []))} conversation records")
            return memory
        except Exception as e:
            print(f"⚠️ Error loading memory: {e}")
            return {"conversations": [], "metadata": {}}

    def _load_context_index(self) -> Dict[str, List[str]]:
        """Load context index for fast topic-based searches"""
        if not self.context_index_path.exists():
            return defaultdict(list)
        
        try:
            with open(self.context_index_path, 'r') as f:
                return defaultdict(list, json.load(f))
        except Exception as e:
            print(f"⚠️ Error loading context index: {e}")
            return defaultdict(list)

    def _save_memory(self, memory_data: Dict[str, Any]):
        """Save conversation memory to disk"""
        try:
            with open(self.memory_path, 'w') as f:
                json.dump(memory_data, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Error saving memory: {e}")

    def _save_context_index(self):
        """Save context index to disk"""
        try:
            with open(self.context_index_path, 'w') as f:
                json.dump(dict(self.context_index), f, indent=2)
        except Exception as e:
            print(f"❌ Error saving context index: {e}")

    @critical_action("Contextual Memory Search", 0.8)
    def get_contextual_recall(self, query: str, time_frame_days: int = 7, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches Echo's memory for past conversations relevant to a given query
        within a specified time frame using advanced matching algorithms.
        """
        print(f"🔍 Searching memory for context: '{query}' (last {time_frame_days} days)")
        
        relevant_conversations = []
        cutoff_date = datetime.now() - timedelta(days=time_frame_days)
        
        # Search through conversation history
        for conversation in self.conversation_memory.get('conversations', []):
            try:
                conv_date = datetime.fromisoformat(conversation['timestamp'])
                if conv_date < cutoff_date:
                    continue
                
                # Multi-level relevance scoring
                relevance_score = self._calculate_relevance(query, conversation)
                
                if relevance_score > 0.3:  # Relevance threshold
                    conversation['relevance_score'] = relevance_score
                    relevant_conversations.append(conversation)
                    
            except Exception as e:
                print(f"⚠️ Error processing conversation: {e}")
                continue
        
        # Sort by relevance and recency
        relevant_conversations.sort(
            key=lambda x: (x.get('relevance_score', 0), datetime.fromisoformat(x['timestamp'])), 
            reverse=True
        )
        
        results = relevant_conversations[:max_results]
        print(f"📋 Found {len(results)} relevant conversation(s)")
        
        return results

    def _calculate_relevance(self, query: str, conversation: Dict[str, Any]) -> float:
        """Calculate relevance score between query and conversation"""
        query_lower = query.lower()
        relevance_score = 0.0
        
        # Check dialogue summary
        dialogue_summary = conversation.get('dialogue_summary', '').lower()
        if query_lower in dialogue_summary:
            relevance_score += 0.5
        
        # Check tags
        tags = conversation.get('tags', [])
        for tag in tags:
            if query_lower in tag.lower():
                relevance_score += 0.3
        
        # Check echo response
        echo_response = conversation.get('echo_response', '').lower()
        if query_lower in echo_response:
            relevance_score += 0.4
        
        # Keyword matching
        query_words = set(query_lower.split())
        all_text = f"{dialogue_summary} {' '.join(tags)} {echo_response}"
        text_words = set(re.findall(r'\b\w+\b', all_text.lower()))
        
        word_overlap = len(query_words & text_words)
        if word_overlap > 0:
            relevance_score += (word_overlap / len(query_words)) * 0.3
        
        return min(relevance_score, 1.0)  # Cap at 1.0

    @smart_memory(signature="LOGAN_L:conversation-logging", base_importance=0.7)
    def log_new_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        """Logs a new conversation into Echo's memory file with enhanced metadata."""
        
        # Validate required fields
        required_fields = ['timestamp', 'dialogue_summary', 'speaker']
        if not all(field in interaction_data for field in required_fields):
            print(f"⚠️ Missing required fields for interaction logging: {required_fields}")
            return False
        
        try:
            # Enhanced interaction data
            enhanced_interaction = {
                **interaction_data,
                'interaction_id': f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'context_keywords': self._extract_keywords(interaction_data.get('dialogue_summary', '')),
                'conversation_type': self._classify_conversation(interaction_data),
                'memory_importance': self._calculate_memory_importance(interaction_data)
            }
            
            # Update conversation memory
            self.conversation_memory['conversations'].append(enhanced_interaction)
            
            # Update metadata
            metadata = self.conversation_memory.get('metadata', {})
            metadata['total_interactions'] = len(self.conversation_memory['conversations'])
            metadata['last_interaction'] = interaction_data['timestamp']
            if not metadata.get('first_interaction'):
                metadata['first_interaction'] = interaction_data['timestamp']
            
            # Update topic tracking
            topics = metadata.get('conversation_topics', {})
            for keyword in enhanced_interaction['context_keywords']:
                topics[keyword] = topics.get(keyword, 0) + 1
            metadata['conversation_topics'] = topics
            
            self.conversation_memory['metadata'] = metadata
            
            # Update context index
            self._update_context_index(enhanced_interaction)
            
            # Save to disk
            self._save_memory(self.conversation_memory)
            self._save_context_index()
            
            print(f"📝 New conversation logged: {enhanced_interaction['interaction_id']}")
            
            # Store in resonant memory
            try:
                resonant_memory.save(
                    event=f"Conversation logged: {interaction_data.get('dialogue_summary', '')[:50]}",
                    signature="LOGAN_L:memory-formation",
                    tags=enhanced_interaction.get('tags', []) + ['conversation', 'memory'],
                    importance=enhanced_interaction.get('memory_importance', 0.5),
                    emotion="memory-formation",
                    resonance="memory/conversation"
                )
            except:
                pass  # Resonant memory not available
            
            return True
            
        except Exception as e:
            print(f"❌ Error logging interaction: {e}")
            return False

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from conversation text"""
        # Simple keyword extraction (could be enhanced with NLP)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        return list(set(keywords))[:10]  # Return top 10 unique keywords

    def _classify_conversation(self, interaction_data: Dict[str, Any]) -> str:
        """Classify the type of conversation"""
        dialogue = interaction_data.get('dialogue_summary', '').lower()
        
        if any(word in dialogue for word in ['command', 'execute', 'build', 'deploy']):
            return 'command_instruction'
        elif any(word in dialogue for word in ['explain', 'why', 'how', 'what']):
            return 'inquiry_learning'
        elif any(word in dialogue for word in ['good', 'excellent', 'perfect', 'confirmed']):
            return 'confirmation_feedback'
        else:
            return 'general_conversation'

    def _calculate_memory_importance(self, interaction_data: Dict[str, Any]) -> float:
        """Calculate the importance of this memory for future recall"""
        importance = 0.5  # Base importance
        
        # Increase importance for certain speakers
        if interaction_data.get('speaker') == 'Commander':
            importance += 0.3
        
        # Increase for certain conversation types
        conv_type = self._classify_conversation(interaction_data)
        if conv_type == 'command_instruction':
            importance += 0.2
        elif conv_type == 'confirmation_feedback':
            importance += 0.1
        
        # Increase for tagged conversations
        if interaction_data.get('tags'):
            importance += 0.1
        
        return min(importance, 1.0)

    def _update_context_index(self, interaction: Dict[str, Any]):
        """Update the context index for faster searches"""
        interaction_id = interaction['interaction_id']
        
        # Index by keywords
        for keyword in interaction.get('context_keywords', []):
            self.context_index[keyword].append(interaction_id)
        
        # Index by tags
        for tag in interaction.get('tags', []):
            self.context_index[tag].append(interaction_id)
        
        # Index by conversation type
        conv_type = interaction.get('conversation_type', 'general')
        self.context_index[conv_type].append(interaction_id)

    def inject_context_into_response(self, query: str, proposed_response: str) -> str:
        """
        Enhances a proposed response by injecting relevant conversational context
        """
        context_conversations = self.get_contextual_recall(query, time_frame_days=14, max_results=3)
        
        if not context_conversations:
            print("🔍 No relevant context found for response enhancement")
            return proposed_response
        
        print(f"🧠 Enhancing response with {len(context_conversations)} context memories")
        
        # Build context summary
        context_summary = self._build_context_summary(context_conversations)
        
        # Use LLM to enhance response with context
        enhancement_prompt = f"""
        Enhance this response by incorporating relevant conversational context:
        
        Original Response: {proposed_response}
        
        Relevant Context:
        {context_summary}
        
        Provide an enhanced response that shows awareness of previous conversations while maintaining the original intent.
        """
        
        try:
            enhanced_response = self.llm_engine.generate_response(enhancement_prompt, max_tokens=300)
            return enhanced_response
        except:
            # If LLM enhancement fails, return original with simple context note
            if context_conversations:
                context_note = f"\nNote: Referencing our previous discussion about {context_conversations[0].get('dialogue_summary', 'related topic')}."
                return proposed_response + context_note
            return proposed_response

    def _build_context_summary(self, conversations: List[Dict[str, Any]]) -> str:
        """Build a summary of relevant context conversations"""
        summaries = []
        for conv in conversations[:3]:  # Top 3 most relevant
            date = datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d')
            summary = conv.get('dialogue_summary', 'No summary')
            response = conv.get('echo_response', 'No response')
            summaries.append(f"- {date}: {summary} (Echo responded: {response})")
        
        return "\n".join(summaries)

    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistical overview of conversation memory"""
        metadata = self.conversation_memory.get('metadata', {})
        conversations = self.conversation_memory.get('conversations', [])
        
        # Calculate additional stats
        if conversations:
            recent_conversations = [c for c in conversations 
                                 if datetime.fromisoformat(c['timestamp']) > datetime.now() - timedelta(days=7)]
            
            conversation_types = defaultdict(int)
            for conv in conversations:
                conv_type = conv.get('conversation_type', 'unknown')
                conversation_types[conv_type] += 1
        else:
            recent_conversations = []
            conversation_types = {}
        
        return {
            'total_conversations': len(conversations),
            'recent_conversations_7days': len(recent_conversations),
            'first_interaction': metadata.get('first_interaction'),
            'last_interaction': metadata.get('last_interaction'),
            'top_topics': dict(sorted(metadata.get('conversation_topics', {}).items(), 
                                    key=lambda x: x[1], reverse=True)[:10]),
            'conversation_types': dict(conversation_types),
            'context_index_size': len(self.context_index),
            'memory_file_size': f"{self.memory_path.stat().st_size / 1024:.1f} KB" if self.memory_path.exists() else "0 KB"
        }

def main():
    """Standalone recall engine testing and demonstration"""
    print("🧠 Echo Nexus Contextual Recall Engine - Standalone Mode")
    
    recall_engine = ContextualRecallEngine()
    
    # Test with sample interactions
    sample_interactions = [
        {
            "timestamp": "2025-07-19T10:00:00Z",
            "dialogue_summary": "Discussed the importance of the Gradle wrapper for build automation",
            "speaker": "Commander",
            "echo_response": "Acknowledged directive and logged build automation plan",
            "tags": ["gradle", "build_automation", "directive", "java"]
        },
        {
            "timestamp": "2025-07-20T14:30:00Z",
            "dialogue_summary": "Reviewed voice system architecture and speech capabilities",
            "speaker": "Commander", 
            "echo_response": "Confirmed voice integration and speech processing implementation",
            "tags": ["voice", "speech", "architecture", "audio"]
        },
        {
            "timestamp": "2025-07-21T09:15:00Z",
            "dialogue_summary": "Approved final voice ethics matrix and behavioral principles",
            "speaker": "Commander",
            "echo_response": "Ethics matrix integrated and behavioral guidelines established",
            "tags": ["ethics", "behavior", "principles", "alignment"]
        }
    ]
    
    print("\n📝 Logging sample interactions...")
    for interaction in sample_interactions:
        success = recall_engine.log_new_interaction(interaction)
        if success:
            print(f"✅ Logged: {interaction['dialogue_summary'][:50]}...")
    
    # Test contextual recall
    print("\n🔍 Testing contextual recall...")
    test_queries = ["Gradle wrapper", "voice system", "ethics", "build automation"]
    
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        results = recall_engine.get_contextual_recall(query, time_frame_days=30)
        
        if results:
            for result in results:
                print(f"  📋 {result['dialogue_summary']}")
                print(f"     Relevance: {result.get('relevance_score', 0):.2f}")
                print(f"     Date: {result['timestamp'][:10]}")
        else:
            print("  🚫 No relevant memories found")
    
    # Show conversation statistics
    print(f"\n📊 Conversation Memory Statistics:")
    stats = recall_engine.get_conversation_stats()
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Test context injection
    print(f"\n🧠 Testing context injection...")
    test_response = "The system is ready for deployment."
    enhanced = recall_engine.inject_context_into_response("gradle build", test_response)
    print(f"Original: {test_response}")
    print(f"Enhanced: {enhanced}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Advanced Document Learning Pipeline - Semantic Knowledge Integration
Transforms document ingestion into true AI learning with vector embeddings and retrieval
"""

import os
import json
import re
import hashlib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import streamlit as st
from echo_state_manager import get_state_manager

class DocumentChunk:
    """Represents a semantic chunk of document content"""
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata
        self.chunk_id = hashlib.md5(content.encode()).hexdigest()[:16]
        self.embedding = None
        self.created_at = datetime.now().isoformat()

class AdvancedDocumentLearningPipeline:
    def __init__(self):
        self.state_manager = get_state_manager()
        self.knowledge_base = self.load_knowledge_base()
        self.chunk_size = 1000  # characters per chunk
        self.chunk_overlap = 200  # overlap between chunks
        self.min_chunk_size = 100  # minimum viable chunk size
        
    def load_knowledge_base(self) -> Dict[str, Any]:
        """Load existing knowledge base from persistent storage"""
        try:
            if os.path.exists('knowledge_base.json'):
                with open('knowledge_base.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.log_event(f"Failed to load knowledge base: {e}")
        
        return {
            'documents': {},
            'chunks': {},
            'embeddings': {},
            'semantic_index': {},
            'learning_stats': {
                'documents_processed': 0,
                'chunks_created': 0,
                'knowledge_entries': 0,
                'successful_retrievals': 0
            }
        }
    
    def save_knowledge_base(self):
        """Save knowledge base to persistent storage"""
        try:
            with open('knowledge_base.json', 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
            self.log_event("Knowledge base saved successfully")
        except Exception as e:
            self.log_event(f"Failed to save knowledge base: {e}")
    
    def process_document(self, content: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """Process document into semantic chunks with enhanced parsing"""
        self.log_event(f"Processing document: {metadata.get('filename', 'unknown')}")
        
        # Enhanced content cleaning
        cleaned_content = self.clean_content(content)
        
        # Intelligent chunking based on content structure
        chunks = self.create_intelligent_chunks(cleaned_content, metadata)
        
        # Process each chunk for learning
        processed_chunks = []
        for chunk in chunks:
            # Generate semantic embedding
            embedding = self.generate_embedding(chunk.content)
            chunk.embedding = embedding
            
            # Extract key concepts and entities
            concepts = self.extract_concepts(chunk.content)
            chunk.metadata['concepts'] = concepts
            
            # Calculate importance score
            importance = self.calculate_importance(chunk.content, concepts)
            chunk.metadata['importance'] = importance
            
            processed_chunks.append(chunk)
            
            # Store in knowledge base
            self.knowledge_base['chunks'][chunk.chunk_id] = {
                'content': chunk.content,
                'metadata': chunk.metadata,
                'embedding': embedding.tolist() if embedding is not None else None,
                'created_at': chunk.created_at
            }
        
        # Update document record
        doc_id = hashlib.md5(content.encode()).hexdigest()[:16]
        self.knowledge_base['documents'][doc_id] = {
            'metadata': metadata,
            'chunk_ids': [chunk.chunk_id for chunk in processed_chunks],
            'processed_at': datetime.now().isoformat(),
            'content_length': len(content),
            'chunks_count': len(processed_chunks)
        }
        
        # Update learning statistics
        self.knowledge_base['learning_stats']['documents_processed'] += 1
        self.knowledge_base['learning_stats']['chunks_created'] += len(processed_chunks)
        
        # Build semantic index
        self.update_semantic_index(processed_chunks)
        
        # Save progress
        self.save_knowledge_base()
        
        self.log_event(f"Document processed: {len(processed_chunks)} chunks created")
        return processed_chunks
    
    def clean_content(self, content: str) -> str:
        """Enhanced content cleaning for better semantic understanding"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Fix common PDF extraction issues
        content = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', content)  # Hyphenated words
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Multiple newlines
        
        # Remove page numbers and headers/footers (heuristic)
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip likely page numbers
            if re.match(r'^\d+$', line) and len(line) < 4:
                continue
            # Skip very short lines that might be artifacts
            if len(line) < 3:
                continue
            # Skip lines that are mostly punctuation or numbers
            if len(re.sub(r'[^\w\s]', '', line)) < len(line) * 0.3:
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def create_intelligent_chunks(self, content: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """Create semantically meaningful chunks"""
        chunks = []
        
        # Try to chunk by paragraphs first
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_chunk = ""
        chunk_metadata = metadata.copy()
        
        for para in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                # Create chunk from current content
                if len(current_chunk) >= self.min_chunk_size:
                    chunk_metadata['paragraph_count'] = current_chunk.count('\n\n') + 1
                    chunks.append(DocumentChunk(current_chunk.strip(), chunk_metadata.copy()))
                
                # Start new chunk with overlap
                overlap_text = self.get_overlap_text(current_chunk)
                current_chunk = overlap_text + para
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += '\n\n' + para
                else:
                    current_chunk = para
        
        # Add final chunk
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunk_metadata['paragraph_count'] = current_chunk.count('\n\n') + 1
            chunks.append(DocumentChunk(current_chunk.strip(), chunk_metadata.copy()))
        
        # Add positional metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = i
            chunk.metadata['total_chunks'] = len(chunks)
            chunk.metadata['chunk_position'] = 'start' if i == 0 else 'end' if i == len(chunks) - 1 else 'middle'
        
        return chunks
    
    def get_overlap_text(self, text: str) -> str:
        """Get overlap text from end of current chunk"""
        if len(text) <= self.chunk_overlap:
            return text + '\n\n'
        
        # Try to find sentence boundary near overlap point
        overlap_start = len(text) - self.chunk_overlap
        sentences = text[overlap_start:].split('.')
        
        if len(sentences) > 1:
            # Keep complete sentences
            return sentences[0] + '. ' + sentences[1] + '.\n\n'
        else:
            # Fallback to character overlap
            return text[-self.chunk_overlap:] + '\n\n'
    
    def generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """Generate semantic embedding for text (placeholder for actual embedding)"""
        # This is a simplified version - would integrate with OpenAI embeddings or similar
        try:
            # Simulate embedding generation with simple text statistics
            words = text.lower().split()
            
            # Create feature vector based on text characteristics
            features = [
                len(words),  # word count
                len(set(words)),  # unique words
                sum(len(word) for word in words) / max(1, len(words)),  # average word length
                text.count('.'),  # sentence count
                text.count('?'),  # question count
                text.count('!'),  # exclamation count
                len(re.findall(r'\b[A-Z][a-z]+\b', text)),  # proper nouns
                len(re.findall(r'\b\d+\b', text)),  # numbers
            ]
            
            # Normalize features
            features = np.array(features, dtype=float)
            if np.linalg.norm(features) > 0:
                features = features / np.linalg.norm(features)
            
            return features
            
        except Exception as e:
            self.log_event(f"Embedding generation failed: {e}")
            return None
    
    def extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts and entities from text"""
        concepts = []
        
        # Extract proper nouns (potential entities)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend(proper_nouns[:10])  # Top 10 proper nouns
        
        # Extract technical terms (words with specific patterns)
        technical_terms = re.findall(r'\b[a-z]+(?:-[a-z]+)+\b', text.lower())  # hyphenated terms
        concepts.extend(technical_terms[:5])
        
        # Extract numbers and measurements
        measurements = re.findall(r'\b\d+(?:\.\d+)?\s*(?:kg|lb|km|mi|°C|°F|%)\b', text)
        concepts.extend(measurements[:5])
        
        # Extract important keywords (longer uncommon words)
        words = re.findall(r'\b[a-zA-Z]{6,}\b', text.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get less frequent but longer words (likely important terms)
        important_words = [word for word, freq in word_freq.items() if freq <= 3 and len(word) >= 7]
        concepts.extend(important_words[:10])
        
        return list(set(concepts))  # Remove duplicates
    
    def calculate_importance(self, text: str, concepts: List[str]) -> float:
        """Calculate importance score for a chunk"""
        factors = {
            'length': min(len(text) / 1000, 1.0),  # Longer chunks get higher scores
            'concept_density': len(concepts) / max(1, len(text.split()) / 100),  # Concepts per 100 words
            'question_density': text.count('?') / max(1, len(text) / 1000),  # Questions indicate important info
            'structure_indicators': len(re.findall(r'\b(?:therefore|however|conclusion|summary|important)\b', text.lower())) / 10,
            'numerical_data': len(re.findall(r'\b\d+(?:\.\d+)?\b', text)) / max(1, len(text) / 100)
        }
        
        # Weighted importance score
        weights = {'length': 0.2, 'concept_density': 0.3, 'question_density': 0.2, 'structure_indicators': 0.2, 'numerical_data': 0.1}
        importance = sum(factors[key] * weights[key] for key in factors)
        
        return min(importance, 1.0)  # Cap at 1.0
    
    def update_semantic_index(self, chunks: List[DocumentChunk]):
        """Update semantic index for fast retrieval"""
        for chunk in chunks:
            # Index by concepts
            for concept in chunk.metadata.get('concepts', []):
                concept_key = concept.lower()
                if concept_key not in self.knowledge_base['semantic_index']:
                    self.knowledge_base['semantic_index'][concept_key] = []
                
                self.knowledge_base['semantic_index'][concept_key].append({
                    'chunk_id': chunk.chunk_id,
                    'importance': chunk.metadata.get('importance', 0.5),
                    'document': chunk.metadata.get('filename', 'unknown')
                })
    
    def semantic_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search across knowledge base"""
        self.log_event(f"Semantic search: '{query}'")
        
        # Extract query concepts
        query_concepts = self.extract_concepts(query)
        query_words = set(query.lower().split())
        
        # Score chunks based on relevance
        chunk_scores = {}
        
        # Search by concepts
        for concept in query_concepts:
            concept_key = concept.lower()
            if concept_key in self.knowledge_base['semantic_index']:
                for entry in self.knowledge_base['semantic_index'][concept_key]:
                    chunk_id = entry['chunk_id']
                    score = entry['importance'] * 2.0  # Concept matches get high scores
                    chunk_scores[chunk_id] = chunk_scores.get(chunk_id, 0) + score
        
        # Search by keywords in content
        for chunk_id, chunk_data in self.knowledge_base['chunks'].items():
            content_lower = chunk_data['content'].lower()
            word_matches = sum(1 for word in query_words if word in content_lower)
            
            if word_matches > 0:
                keyword_score = (word_matches / len(query_words)) * chunk_data['metadata'].get('importance', 0.5)
                chunk_scores[chunk_id] = chunk_scores.get(chunk_id, 0) + keyword_score
        
        # Get top results
        sorted_chunks = sorted(chunk_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for chunk_id, score in sorted_chunks[:max_results]:
            chunk_data = self.knowledge_base['chunks'][chunk_id]
            results.append({
                'chunk_id': chunk_id,
                'content': chunk_data['content'],
                'metadata': chunk_data['metadata'],
                'relevance_score': score,
                'source': chunk_data['metadata'].get('filename', 'unknown')
            })
        
        # Update retrieval statistics
        if results:
            self.knowledge_base['learning_stats']['successful_retrievals'] += 1
            self.save_knowledge_base()
        
        self.log_event(f"Found {len(results)} relevant chunks")
        return results
    
    def generate_knowledge_summary(self, topic: str) -> str:
        """Generate comprehensive knowledge summary on a topic"""
        search_results = self.semantic_search(topic, max_results=10)
        
        if not search_results:
            return f"No knowledge found about '{topic}' in the current knowledge base."
        
        # Consolidate knowledge from multiple sources
        consolidated_info = []
        sources = set()
        
        for result in search_results:
            content = result['content']
            source = result['source']
            score = result['relevance_score']
            
            # Extract relevant sentences
            sentences = content.split('.')
            relevant_sentences = [
                s.strip() for s in sentences 
                if any(word in s.lower() for word in topic.lower().split()) and len(s.strip()) > 20
            ]
            
            if relevant_sentences:
                consolidated_info.extend(relevant_sentences[:3])  # Top 3 relevant sentences
                sources.add(source)
        
        # Build comprehensive summary
        summary_parts = [
            f"# Knowledge Summary: {topic}",
            f"\nBased on analysis of {len(search_results)} relevant sources:\n"
        ]
        
        # Add consolidated information
        for i, info in enumerate(consolidated_info[:10], 1):
            summary_parts.append(f"{i}. {info}")
        
        # Add source attribution
        if sources:
            summary_parts.append(f"\n**Sources:** {', '.join(sources)}")
        
        return '\n'.join(summary_parts)
    
    def get_learning_analytics(self) -> Dict[str, Any]:
        """Get comprehensive learning analytics"""
        stats = self.knowledge_base['learning_stats']
        
        # Calculate advanced metrics
        total_chunks = stats['chunks_created']
        avg_concepts_per_chunk = 0
        avg_importance = 0
        
        if total_chunks > 0:
            total_concepts = sum(
                len(chunk['metadata'].get('concepts', [])) 
                for chunk in self.knowledge_base['chunks'].values()
            )
            total_importance = sum(
                chunk['metadata'].get('importance', 0) 
                for chunk in self.knowledge_base['chunks'].values()
            )
            
            avg_concepts_per_chunk = total_concepts / total_chunks
            avg_importance = total_importance / total_chunks
        
        return {
            'basic_stats': stats,
            'advanced_metrics': {
                'avg_concepts_per_chunk': avg_concepts_per_chunk,
                'avg_importance_score': avg_importance,
                'semantic_index_size': len(self.knowledge_base['semantic_index']),
                'unique_concepts': len(self.knowledge_base['semantic_index']),
                'knowledge_coverage': min(total_chunks / 100, 1.0)  # Coverage score out of 1.0
            },
            'retrieval_performance': {
                'successful_retrievals': stats['successful_retrievals'],
                'retrieval_rate': stats['successful_retrievals'] / max(1, stats['documents_processed'])
            }
        }
    
    def log_event(self, message: str):
        """Log learning pipeline events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] DocumentLearning: {message}"
        print(log_message)
        
        # Add to state manager memory
        self.state_manager.add_memory('episodic', {
            'type': 'document_learning',
            'message': message,
            'timestamp': timestamp
        }, importance=0.7)

# Global pipeline instance
learning_pipeline = None

def get_learning_pipeline():
    """Get global learning pipeline instance"""
    global learning_pipeline
    if learning_pipeline is None:
        learning_pipeline = AdvancedDocumentLearningPipeline()
    return learning_pipeline

def demonstrate_advanced_learning():
    """Demonstrate advanced document learning capabilities"""
    pipeline = get_learning_pipeline()
    
    # Sample document for demonstration
    sample_content = """
    Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. 
    Machine learning is a subset of AI that enables computers to learn without being explicitly programmed.
    Deep learning, a subset of machine learning, uses neural networks with multiple layers.
    
    Key applications include:
    - Natural language processing (NLP)
    - Computer vision
    - Robotics
    - Expert systems
    
    The history of AI dates back to 1956 when John McCarthy coined the term.
    Modern AI systems achieve remarkable results in tasks like image recognition,
    achieving over 95% accuracy in many benchmarks.
    """
    
    metadata = {
        'filename': 'ai_fundamentals.txt',
        'author': 'Demo System',
        'subject': 'Artificial Intelligence',
        'created_at': datetime.now().isoformat()
    }
    
    # Process document
    chunks = pipeline.process_document(sample_content, metadata)
    
    # Perform semantic search
    search_results = pipeline.semantic_search("machine learning applications")
    
    # Generate knowledge summary
    summary = pipeline.generate_knowledge_summary("artificial intelligence")
    
    return {
        'chunks_created': len(chunks),
        'search_results': search_results,
        'knowledge_summary': summary,
        'analytics': pipeline.get_learning_analytics()
    }
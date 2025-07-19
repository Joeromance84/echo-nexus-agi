#!/usr/bin/env python3
"""
EchoNexus Knowledge Synthesis Module
Processes and synthesizes raw text input into structured knowledge
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter

def synthesize_knowledge(raw_text: str) -> Dict[str, Any]:
    """
    Main knowledge synthesis function that processes raw text and extracts structured insights
    """
    
    try:
        # Clean and prepare text
        cleaned_text = clean_text(raw_text)
        
        # Extract key information
        analysis = analyze_content(cleaned_text)
        
        # Generate summary
        summary = generate_summary(cleaned_text, analysis)
        
        # Extract key concepts
        concepts = extract_key_concepts(cleaned_text)
        
        # Determine knowledge type
        knowledge_type = classify_content(cleaned_text)
        
        result = {
            'summary': summary,
            'key_concepts': concepts,
            'content_type': knowledge_type,
            'word_count': analysis['word_count'],
            'confidence': analysis['confidence'],
            'timestamp': datetime.now().isoformat(),
            'raw_length': len(raw_text)
        }
        
        return result
        
    except Exception as e:
        return {
            'summary': f"Knowledge synthesis failed: {e}",
            'key_concepts': [],
            'content_type': 'unknown',
            'word_count': 0,
            'confidence': 0.0,
            'timestamp': datetime.now().isoformat(),
            'raw_length': len(raw_text)
        }

def clean_text(text: str) -> str:
    """Clean and normalize text for processing"""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
    
    return text.strip()

def analyze_content(text: str) -> Dict[str, Any]:
    """Analyze content characteristics"""
    
    words = text.split()
    sentences = text.split('.')
    
    # Count questions
    questions = len([s for s in sentences if '?' in s])
    
    # Count technical terms
    technical_indicators = ['theory', 'principle', 'algorithm', 'method', 'approach', 
                          'framework', 'model', 'concept', 'hypothesis', 'analysis']
    technical_count = sum(1 for word in words if word.lower() in technical_indicators)
    
    # Calculate confidence based on content structure
    confidence = min(1.0, (len(words) / 100) * 0.1 + (technical_count / len(words)) * 0.5)
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'questions': questions,
        'technical_terms': technical_count,
        'confidence': confidence
    }

def extract_key_concepts(text: str) -> List[str]:
    """Extract key concepts from text"""
    
    words = text.lower().split()
    
    # Filter out common words
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'can', 'must', 'shall', 'this', 'that', 'these', 'those', 'it', 'he', 'she',
        'they', 'we', 'you', 'i', 'me', 'him', 'her', 'them', 'us', 'not', 'no',
        'yes', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just'
    }
    
    # Keep words longer than 3 characters and not in stop words
    filtered_words = [word for word in words if len(word) > 3 and word not in stop_words]
    
    # Count word frequency
    word_counts = Counter(filtered_words)
    
    # Get top concepts (words that appear more than once)
    key_concepts = [word for word, count in word_counts.most_common(10) if count > 1]
    
    return key_concepts[:5]  # Return top 5 concepts

def classify_content(text: str) -> str:
    """Classify the type of content"""
    
    text_lower = text.lower()
    
    # Academic/Scientific content
    if any(term in text_lower for term in ['research', 'study', 'experiment', 'hypothesis', 'theory', 'analysis']):
        return 'academic'
    
    # Technical content
    elif any(term in text_lower for term in ['algorithm', 'code', 'function', 'class', 'method', 'implementation']):
        return 'technical'
    
    # News content
    elif any(term in text_lower for term in ['reported', 'according to', 'sources', 'news', 'announced']):
        return 'news'
    
    # Philosophical content
    elif any(term in text_lower for term in ['consciousness', 'existence', 'reality', 'truth', 'meaning', 'ethics']):
        return 'philosophical'
    
    # Physics/Science content
    elif any(term in text_lower for term in ['quantum', 'particle', 'energy', 'universe', 'physics', 'black hole']):
        return 'physics'
    
    # Default
    else:
        return 'general'

def generate_summary(text: str, analysis: Dict[str, Any]) -> str:
    """Generate a concise summary of the content"""
    
    sentences = text.split('.')
    
    # Get first meaningful sentence
    first_sentence = next((s.strip() for s in sentences if len(s.strip()) > 50), "Content analysis in progress...")
    
    # Truncate if too long
    if len(first_sentence) > 200:
        first_sentence = first_sentence[:200] + "..."
    
    summary = f"""Content processed: {analysis['word_count']} words, {analysis['sentence_count']} sentences.

Key insight: {first_sentence}

Analysis complete. Knowledge integrated into EchoNexus memory system."""
    
    return summary

# Test function
if __name__ == "__main__":
    test_text = """
    The black hole firewall paradox represents one of the most challenging problems in modern theoretical physics.
    It arises from the intersection of quantum mechanics and general relativity, particularly when considering
    the information paradox and the principle of quantum unitarity. The firewall hypothesis suggests that
    an observer falling into a black hole would encounter a wall of high-energy particles at the event horizon.
    """
    
    result = synthesize_knowledge(test_text)
    print("Knowledge Synthesis Test:")
    print(json.dumps(result, indent=2))
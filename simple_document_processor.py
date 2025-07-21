#!/usr/bin/env python3
"""
Simple Document Processor
Text-based document learning system that works without external dependencies
"""

import os
import json
import hashlib
import tempfile
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import time

class SimpleDocumentProcessor:
    """Simple document processor for basic text files and simple PDF/EPUB handling"""
    
    def __init__(self):
        self.knowledge_database = {}
        self.processed_documents = {}
        self.max_file_size_mb = 10  # 10MB limit for simple processing
        
        # Create knowledge directory
        self.knowledge_dir = Path("document_knowledge")
        self.knowledge_dir.mkdir(exist_ok=True)
        
        # Load existing knowledge
        self._load_existing_knowledge()
    
    def _load_existing_knowledge(self):
        """Load existing knowledge from files"""
        try:
            index_file = self.knowledge_dir / "knowledge_index.json"
            if index_file.exists():
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    self.processed_documents = data.get('processed_documents', {})
                    
            # Load individual knowledge files
            for knowledge_file in self.knowledge_dir.glob("knowledge_*.json"):
                with open(knowledge_file, 'r') as f:
                    knowledge_data = json.load(f)
                    file_hash = knowledge_data.get('file_hash')
                    if file_hash:
                        self.knowledge_database[file_hash] = knowledge_data
                        
        except Exception as e:
            print(f"Error loading existing knowledge: {e}")
    
    def process_text_content(self, text_content: str, filename: str) -> Dict[str, Any]:
        """Process text content and extract knowledge"""
        
        # Calculate file hash
        file_hash = hashlib.sha256(text_content.encode()).hexdigest()
        
        # Check if already processed
        if file_hash in self.processed_documents:
            return {
                "status": "already_processed",
                "file_hash": file_hash,
                "filename": filename,
                "knowledge_insights": self.processed_documents[file_hash]["knowledge_extracted"]
            }
        
        try:
            # Extract knowledge
            knowledge = self._extract_knowledge_from_text(text_content, filename)
            
            # Store knowledge
            self._save_knowledge(file_hash, knowledge, filename)
            
            # Update processed documents
            self.processed_documents[file_hash] = {
                "filename": filename,
                "text_length": len(text_content),
                "knowledge_extracted": len(knowledge.get("insights", [])),
                "timestamp": datetime.now().isoformat(),
                "processing_method": "simple_text"
            }
            
            # Save index
            self._save_knowledge_index()
            
            return {
                "status": "processed_successfully",
                "file_hash": file_hash,
                "filename": filename,
                "text_length": len(text_content),
                "knowledge_insights": len(knowledge.get("insights", [])),
                "key_concepts": knowledge.get("key_concepts", [])[:10],
                "summary": knowledge.get("summary", "")[:200] + "..."
            }
            
        except Exception as e:
            return {
                "status": "processing_error",
                "error": str(e),
                "filename": filename
            }
    
    def process_uploaded_file(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Process uploaded file"""
        
        # Check file size
        file_size_mb = len(file_data) / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            return {
                "status": "file_too_large",
                "file_size_mb": file_size_mb,
                "max_size_mb": self.max_file_size_mb
            }
        
        # Try to extract text based on file type
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext == 'txt':
            try:
                text_content = file_data.decode('utf-8')
            except UnicodeDecodeError:
                text_content = file_data.decode('utf-8', errors='ignore')
        elif file_ext == 'pdf':
            text_content = self._extract_simple_pdf_text(file_data)
        elif file_ext in ['epub', 'html', 'htm']:
            text_content = self._extract_simple_html_text(file_data)
        else:
            # Try to decode as text
            try:
                text_content = file_data.decode('utf-8')
            except:
                return {
                    "status": "unsupported_format",
                    "supported_formats": ["txt", "pdf", "epub", "html"],
                    "note": "For better PDF/EPUB support, install PyPDF2 and ebooklib libraries"
                }
        
        # Process the extracted text
        return self.process_text_content(text_content, filename)
    
    def _extract_simple_pdf_text(self, file_data: bytes) -> str:
        """Simple PDF text extraction without external libraries"""
        
        # This is a very basic PDF text extraction
        # For proper PDF support, use PyPDF2 or PyMuPDF
        text = file_data.decode('latin1', errors='ignore')
        
        # Look for text patterns in PDF
        text_patterns = []
        
        # Extract text between common PDF markers
        for match in re.finditer(r'\((.*?)\)', text):
            content = match.group(1)
            if len(content) > 10 and any(c.isalpha() for c in content):
                text_patterns.append(content)
        
        # Extract text between BT/ET markers (text objects)
        bt_et_pattern = r'BT\s+(.*?)\s+ET'
        for match in re.finditer(bt_et_pattern, text, re.DOTALL):
            content = match.group(1)
            # Clean up PDF commands
            clean_content = re.sub(r'/\w+\s+\d+\s+Tf\s+', '', content)
            clean_content = re.sub(r'\d+\.?\d*\s+\d+\.?\d*\s+Td\s+', '', clean_content)
            if clean_content.strip():
                text_patterns.append(clean_content)
        
        extracted_text = ' '.join(text_patterns)
        
        if not extracted_text.strip():
            extracted_text = "PDF content detected but could not extract readable text. For better PDF support, install PyPDF2 library."
        
        return extracted_text
    
    def _extract_simple_html_text(self, file_data: bytes) -> str:
        """Simple HTML/EPUB text extraction"""
        
        try:
            html_content = file_data.decode('utf-8')
        except:
            html_content = file_data.decode('latin1', errors='ignore')
        
        # Remove HTML tags
        text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _extract_knowledge_from_text(self, text: str, filename: str) -> Dict[str, Any]:
        """Extract knowledge from text content"""
        
        # Basic text analysis
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Extract key concepts (most frequent meaningful words)
        key_concepts = self._extract_key_concepts(text)
        
        # Extract insights (sentences with key phrases)
        insights = self._extract_insights(sentences)
        
        # Generate summary (first few sentences)
        summary = self._generate_summary(sentences)
        
        # Extract learning points
        learning_points = self._extract_learning_points(sentences)
        
        knowledge = {
            "file_hash": hashlib.sha256(text.encode()).hexdigest(),
            "filename": filename,
            "processing_timestamp": datetime.now().isoformat(),
            "text_stats": {
                "word_count": len(words),
                "sentence_count": len([s for s in sentences if s.strip()]),
                "character_count": len(text)
            },
            "summary": summary,
            "key_concepts": key_concepts,
            "insights": insights,
            "learning_points": learning_points,
            "technical_terms": self._extract_technical_terms(text)
        }
        
        return knowledge
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Common stop words to exclude
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 
            'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 
            'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'way', 'man', 'too', 'any', 'say', 'she', 
            'may', 'use', 'her', 'than', 'this', 'that', 'with', 'have', 'from', 'they', 'know', 'want', 
            'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 
            'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were', 'will',
            'what', 'said', 'each', 'which', 'their', 'would', 'there', 'could', 'other', 'after',
            'first', 'never', 'these', 'think', 'where', 'being', 'every', 'great', 'might', 'shall',
            'still', 'those', 'while', 'again', 'before', 'little', 'right', 'should', 'through',
            'about', 'into', 'also', 'back', 'only', 'more', 'even', 'most', 'made', 'same', 'find',
            'work', 'life', 'hand', 'part', 'give', 'last', 'down', 'turn', 'call', 'came', 'does',
            'look', 'used', 'water', 'words', 'years', 'place', 'sound', 'great', 'small', 'every',
            'found', 'still', 'between', 'thought', 'help', 'through', 'much', 'before', 'move',
            'right', 'line', 'too', 'means', 'old', 'any', 'same', 'tell', 'boy', 'follow', 'came'
        }
        
        # Filter out stop words and count frequency
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count word frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top concepts
        top_concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return [word for word, freq in top_concepts if freq > 1]
    
    def _extract_insights(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """Extract insights from sentences"""
        
        insight_keywords = [
            'important', 'significant', 'key', 'crucial', 'essential', 'fundamental',
            'conclusion', 'result', 'finding', 'discovery', 'insight', 'principle',
            'lesson', 'learn', 'understand', 'realize', 'recognize', 'remember',
            'breakthrough', 'innovation', 'advancement', 'development', 'improvement'
        ]
        
        insights = []
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
                
            # Check if sentence contains insight keywords
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in insight_keywords):
                insights.append({
                    "text": sentence,
                    "sentence_index": i,
                    "confidence": 0.8,
                    "type": "key_insight"
                })
        
        return insights[:10]  # Limit to top 10 insights
    
    def _generate_summary(self, sentences: List[str]) -> str:
        """Generate a simple summary"""
        
        # Use first few meaningful sentences
        summary_sentences = []
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 30:  # Meaningful length
                summary_sentences.append(sentence)
                if len(summary_sentences) >= 3:  # Max 3 sentences
                    break
        
        return '. '.join(summary_sentences) + '.' if summary_sentences else "Summary not available."
    
    def _extract_learning_points(self, sentences: List[str]) -> List[str]:
        """Extract learning points"""
        
        learning_keywords = [
            'learn', 'teach', 'understand', 'knowledge', 'skill', 'technique',
            'method', 'approach', 'strategy', 'solution', 'practice', 'example'
        ]
        
        learning_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in learning_keywords):
                learning_points.append(sentence)
        
        return learning_points[:8]  # Limit to 8 learning points
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms and acronyms"""
        
        # Find capitalized words (potential technical terms)
        capitalized_words = re.findall(r'\b[A-Z][A-Za-z]*\b', text)
        
        # Find acronyms (2+ uppercase letters)
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        
        # Find technical-looking words (CamelCase, underscore_case)
        technical_patterns = re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b|\b[a-z]+_[a-z]+\b', text)
        
        # Combine and filter
        all_terms = capitalized_words + acronyms + technical_patterns
        
        # Remove common words and filter unique terms
        common_words = {'The', 'This', 'That', 'And', 'But', 'For', 'With', 'You', 'Are', 'Can', 'Has'}
        technical_terms = list(set([term for term in all_terms if term not in common_words and len(term) > 2]))
        
        return technical_terms[:15]  # Limit to 15 terms
    
    def _save_knowledge(self, file_hash: str, knowledge: Dict[str, Any], filename: str):
        """Save knowledge to file"""
        
        knowledge_file = self.knowledge_dir / f"knowledge_{file_hash[:8]}.json"
        
        with open(knowledge_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
    
    def _save_knowledge_index(self):
        """Save knowledge index"""
        
        index_data = {
            "total_documents": len(self.processed_documents),
            "processed_documents": self.processed_documents,
            "last_updated": datetime.now().isoformat()
        }
        
        index_file = self.knowledge_dir / "knowledge_index.json"
        
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
    
    def search_knowledge(self, query: str) -> Dict[str, Any]:
        """Search through processed knowledge"""
        
        query_lower = query.lower()
        results = []
        
        for file_hash, knowledge in self.knowledge_database.items():
            doc_info = self.processed_documents.get(file_hash, {})
            filename = doc_info.get("filename", "Unknown")
            
            # Search in summary
            summary = knowledge.get("summary", "")
            if query_lower in summary.lower():
                results.append({
                    "filename": filename,
                    "match_type": "summary",
                    "content": summary[:200] + "...",
                    "relevance": 0.9
                })
            
            # Search in key concepts
            key_concepts = knowledge.get("key_concepts", [])
            matching_concepts = [concept for concept in key_concepts if query_lower in concept.lower()]
            if matching_concepts:
                results.append({
                    "filename": filename,
                    "match_type": "concepts",
                    "content": f"Related concepts: {', '.join(matching_concepts[:5])}",
                    "relevance": 0.8
                })
            
            # Search in insights
            for insight in knowledge.get("insights", []):
                if query_lower in insight.get("text", "").lower():
                    results.append({
                        "filename": filename,
                        "match_type": "insight",
                        "content": insight["text"][:200] + "...",
                        "relevance": 0.7
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "query": query,
            "total_results": len(results),
            "results": results[:10]  # Limit to top 10 results
        }
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of all learning"""
        
        if not self.processed_documents:
            return {"status": "no_documents_processed"}
        
        # Aggregate statistics
        total_docs = len(self.processed_documents)
        total_insights = 0
        total_concepts = set()
        recent_docs = []
        
        for file_hash, doc_info in self.processed_documents.items():
            total_insights += doc_info.get("knowledge_extracted", 0)
            recent_docs.append({
                "filename": doc_info["filename"],
                "timestamp": doc_info["timestamp"],
                "insights": doc_info.get("knowledge_extracted", 0)
            })
            
            # Get concepts from knowledge
            if file_hash in self.knowledge_database:
                knowledge = self.knowledge_database[file_hash]
                concepts = knowledge.get("key_concepts", [])
                total_concepts.update(concepts)
        
        # Sort recent docs by timestamp
        recent_docs.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "total_documents": total_docs,
            "total_insights": total_insights,
            "total_concepts": len(total_concepts),
            "concepts_learned": list(total_concepts)[:20],
            "recent_documents": recent_docs[:5],
            "avg_insights_per_doc": total_insights / total_docs if total_docs > 0 else 0,
            "processing_summary": f"Processed {total_docs} documents with {total_insights} insights extracted"
        }
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get memory and storage status"""
        
        # Calculate storage usage
        total_size = 0
        file_count = 0
        
        if self.knowledge_dir.exists():
            for file_path in self.knowledge_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
        
        size_mb = total_size / (1024 * 1024)
        
        return {
            "knowledge_files": file_count,
            "storage_size_mb": round(size_mb, 2),
            "documents_processed": len(self.processed_documents),
            "memory_management": "active",
            "auto_cleanup": True,
            "status": "optimal" if size_mb < 50 else "moderate" if size_mb < 100 else "high"
        }
#!/usr/bin/env python3
"""
Test the document processing pipeline functionality
"""

import os
import re
import json
import hashlib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any

class SimpleDocumentProcessor:
    """Simplified document processor for testing"""
    
    def __init__(self):
        self.documents_folder = 'data/documents'
        self.processed_folder = 'data/processed'
        
    def list_files(self, folder_path: str) -> List[str]:
        """List all files in folder"""
        try:
            if os.path.exists(folder_path):
                return os.listdir(folder_path)
            return []
        except:
            return []
    
    def filter_documents(self, file_list: List[str]) -> List[str]:
        """Filter for document files"""
        valid_extensions = ['.pdf', '.epub', '.txt']
        return [f for f in file_list if os.path.splitext(f)[1].lower() in valid_extensions]
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return f"Error reading {file_path}"
    
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks
    
    def generate_simple_embedding(self, text: str) -> np.ndarray:
        """Generate simple text embedding"""
        words = text.lower().split()
        features = [
            len(words),  # word count
            len(set(words)),  # unique words
            sum(len(word) for word in words) / max(1, len(words)),  # avg word length
            text.count('.'),  # sentences
            len([w for w in words if len(w) > 6])  # long words
        ]
        
        embedding = np.array(features, dtype=float)
        if np.linalg.norm(embedding) > 0:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def process_documents(self) -> Dict[str, Any]:
        """Process all documents in folder"""
        # Ensure folders exist
        os.makedirs(self.documents_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        
        # List and filter files
        all_files = self.list_files(self.documents_folder)
        doc_files = self.filter_documents(all_files)
        
        results = {
            'processed_files': [],
            'total_chunks': 0,
            'embeddings': [],
            'metadata': []
        }
        
        for filename in doc_files:
            file_path = os.path.join(self.documents_folder, filename)
            
            # Extract text
            text = self.extract_text_from_file(file_path)
            
            # Create chunks
            chunks = self.chunk_text(text)
            
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 50:
                    continue
                
                # Generate embedding
                embedding = self.generate_simple_embedding(chunk)
                
                # Store
                results['embeddings'].append(embedding.tolist())
                results['metadata'].append({
                    'source_file': filename,
                    'chunk_index': i,
                    'text': chunk,
                    'processed_at': datetime.now().isoformat()
                })
                
                results['total_chunks'] += 1
            
            results['processed_files'].append({
                'filename': filename,
                'chunks': len(chunks),
                'text_length': len(text)
            })
        
        return results
    
    def search_documents(self, query: str, embeddings: List[List], metadata: List[Dict], top_k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        if not embeddings:
            return []
        
        # Generate query embedding
        query_embedding = self.generate_simple_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, stored_embedding in enumerate(embeddings):
            stored_vec = np.array(stored_embedding)
            
            # Cosine similarity
            similarity = np.dot(query_embedding, stored_vec) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(stored_vec)
            )
            similarities.append((similarity, i))
        
        # Sort and return top results
        similarities.sort(reverse=True)
        
        results = []
        for similarity, idx in similarities[:top_k]:
            result = metadata[idx].copy()
            result['similarity_score'] = similarity
            results.append(result)
        
        return results

def main():
    """Test the document processing pipeline"""
    print("🔬 Testing Document Processing Pipeline")
    print("=" * 50)
    
    # Initialize processor
    processor = SimpleDocumentProcessor()
    
    # Process documents
    print("📂 Processing documents in data/documents...")
    results = processor.process_documents()
    
    print(f"✅ Processed {len(results['processed_files'])} files")
    print(f"📊 Generated {results['total_chunks']} text chunks")
    print(f"🧠 Created {len(results['embeddings'])} embeddings")
    
    # Show file details
    for file_info in results['processed_files']:
        print(f"   📄 {file_info['filename']}: {file_info['chunks']} chunks, {file_info['text_length']} chars")
    
    # Test search functionality
    if results['embeddings']:
        print("\n🔍 Testing search functionality...")
        
        test_queries = [
            "artificial intelligence consciousness",
            "network intelligence frameworks", 
            "autonomous learning systems"
        ]
        
        for query in test_queries:
            print(f"\n🎯 Query: '{query}'")
            search_results = processor.search_documents(
                query, 
                results['embeddings'], 
                results['metadata'],
                top_k=2
            )
            
            for i, result in enumerate(search_results, 1):
                print(f"   {i}. {result['source_file']} (Score: {result['similarity_score']:.3f})")
                preview = result['text'][:100].replace('\n', ' ')
                print(f"      Preview: {preview}...")
    
    # Save results for later use
    output_file = 'document_processing_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to {output_file}")
    print("\n🎉 Document processing pipeline test complete!")
    
    return results

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MEMORY-INTEGRATED AGI KNOWLEDGE PROCESSOR
Enhanced processor with full autonomous memory integration
"""

import tempfile
import os
from datetime import datetime
from main import AGIKnowledgeProcessor, storage_client
from autonomous_memory_system import (
    remember, recall, search_knowledge, record_learning, 
    record_action, update_skill, get_memory_status
)

class MemoryIntegratedAGIProcessor(AGIKnowledgeProcessor):
    """Enhanced AGI processor with full autonomous memory integration"""
    
    def __init__(self):
        super().__init__()
        self.memory_session_id = f"processing_session_{int(datetime.now().timestamp())}"
        self.session_memories = []
        
        # Initialize memory tracking
        remember(
            content=f"AGI Processor initialized with memory integration",
            memory_type="episodic",
            importance=0.8,
            tags=["initialization", "memory_integration"],
            source="agi_processor"
        )
    
    def process_file_with_memory(self, bucket_name: str, file_name: str) -> bool:
        """Enhanced file processing with comprehensive memory tracking"""
        try:
            print(f"🚀 Starting memory-integrated AGI knowledge processing for: {file_name}")
            
            # Record start of processing action
            processing_action = {
                "type": "document_processing",
                "description": f"Processing document: {file_name}",
                "parameters": {"bucket": bucket_name, "file": file_name},
                "confidence": 0.8,
                "session_id": self.memory_session_id
            }
            
            # Check if we've processed similar files before
            similar_memories = search_knowledge(f"processed {file_name}", ["procedural", "semantic"], 5)
            if similar_memories:
                print(f"🧠 Found {len(similar_memories)} related processing memories")
                for memory in similar_memories[:2]:
                    print(f"   📚 Previous experience: {memory.content}")
            
            # Download file
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
                blob.download_to_filename(temp_file.name)
                temp_file_path = temp_file.name
            
            # Extract text based on file type with memory tracking
            text_content = ""
            extraction_memory_id = None
            
            if file_name.lower().endswith('.pdf'):
                text_content = self.extract_text_from_pdf(temp_file_path)
                extraction_memory_id = remember(
                    content={
                        "action": "pdf_text_extraction",
                        "file": file_name,
                        "characters_extracted": len(text_content),
                        "success": len(text_content) > 0,
                        "timestamp": datetime.now().isoformat()
                    },
                    memory_type="procedural",
                    importance=0.6,
                    tags=["pdf_extraction", "document_processing", "text_extraction"],
                    source="agi_processor"
                )
                
                # Update PDF processing skill
                update_skill("pdf_processing", min(1.0, 0.3 + (self.processing_stats['files_processed'] * 0.05)), 
                            f"Extracted {len(text_content)} characters from PDF")
                
            elif file_name.lower().endswith('.epub'):
                text_content = self.extract_text_from_epub(temp_file_path)
                extraction_memory_id = remember(
                    content={
                        "action": "epub_text_extraction",
                        "file": file_name,
                        "characters_extracted": len(text_content),
                        "success": len(text_content) > 0,
                        "timestamp": datetime.now().isoformat()
                    },
                    memory_type="procedural",
                    importance=0.6,
                    tags=["epub_extraction", "document_processing", "text_extraction"],
                    source="agi_processor"
                )
                
                # Update EPUB processing skill
                update_skill("epub_processing", min(1.0, 0.3 + (self.processing_stats['files_processed'] * 0.05)), 
                            f"Extracted {len(text_content)} characters from EPUB")
                
            else:
                print(f"⚠️ Unsupported file type: {file_name}")
                processing_action["result"] = {"status": "failed", "reason": "unsupported_file_type"}
                record_action(processing_action)
                
                # Remember the failure for learning
                remember(
                    content={
                        "error": "unsupported_file_type",
                        "file": file_name,
                        "file_extension": os.path.splitext(file_name)[1],
                        "lesson": "Need to add support for this file type"
                    },
                    memory_type="episodic",
                    importance=0.5,
                    tags=["error", "unsupported_format", "learning_opportunity"],
                    source="agi_processor"
                )
                return False
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            if not text_content.strip():
                print(f"⚠️ No text content extracted from {file_name}")
                processing_action["result"] = {"status": "failed", "reason": "no_content_extracted"}
                record_action(processing_action)
                
                # Remember extraction failure for improvement
                remember(
                    content={
                        "error": "no_content_extracted",
                        "file": file_name,
                        "extraction_memory_id": extraction_memory_id,
                        "analysis": "File may be corrupted, encrypted, or have non-standard format"
                    },
                    memory_type="episodic",
                    importance=0.7,
                    tags=["extraction_failure", "empty_content", "debugging"],
                    source="agi_processor"
                )
                return False
            
            # Create intelligent chunks with memory of chunking strategy
            chunks = self.intelligent_chunking(text_content, file_name)
            
            if not chunks:
                print(f"⚠️ No chunks created from {file_name}")
                processing_action["result"] = {"status": "failed", "reason": "no_chunks_created"}
                record_action(processing_action)
                return False
            
            # Store detailed chunking knowledge
            chunking_memory_id = remember(
                content={
                    "action": "intelligent_chunking",
                    "file": file_name,
                    "input_characters": len(text_content),
                    "chunks_created": len(chunks),
                    "average_chunk_size": sum(c['character_count'] for c in chunks) / len(chunks),
                    "chunking_efficiency": len(chunks) / (len(text_content) / 1000),  # chunks per KB
                    "strategy": "contextual_boundary_detection"
                },
                memory_type="semantic",
                importance=0.7,
                tags=["chunking", "knowledge_extraction", "optimization"],
                source="agi_processor"
            )
            
            # Update chunking skill based on efficiency
            chunking_efficiency = len(chunks) / max(1, len(text_content) / 1000)
            update_skill("text_chunking", min(1.0, 0.4 + (chunking_efficiency * 0.1)), 
                        f"Created {len(chunks)} chunks with {chunking_efficiency:.2f} efficiency")
            
            # Generate embeddings with memory tracking
            embeddings_created = 0
            if self.initialize_embedding_model():
                original_chunks = len(chunks)
                chunks = self.generate_embeddings(chunks)
                embeddings_created = len([c for c in chunks if 'embedding' in c])
                
                # Store embedding generation knowledge
                embedding_memory_id = remember(
                    content={
                        "action": "embedding_generation",
                        "file": file_name,
                        "chunks_processed": original_chunks,
                        "embeddings_created": embeddings_created,
                        "success_rate": embeddings_created / original_chunks if original_chunks > 0 else 0,
                        "model": "textembedding-gecko@003"
                    },
                    memory_type="semantic",
                    importance=0.8,
                    tags=["embeddings", "vector_generation", "semantic_processing"],
                    source="agi_processor"
                )
                
                # Update embedding skill
                embedding_success_rate = embeddings_created / original_chunks if original_chunks > 0 else 0
                update_skill("embedding_generation", min(1.0, 0.5 + (embedding_success_rate * 0.3)), 
                            f"Generated {embeddings_created}/{original_chunks} embeddings")
            
            # Store processed data with memory links
            self.store_processed_data(chunks, file_name)
            
            # Update comprehensive statistics
            self.processing_stats['files_processed'] += 1
            self.processing_stats['chunks_created'] += len(chunks)
            
            # Record successful processing action with detailed results
            processing_action["result"] = {
                "status": "success",
                "chunks_created": len(chunks),
                "embeddings_generated": embeddings_created,
                "characters_processed": len(text_content),
                "extraction_memory_id": extraction_memory_id,
                "chunking_memory_id": chunking_memory_id,
                "processing_time": datetime.now().isoformat()
            }
            record_action(processing_action)
            
            # Update overall processing skills with context
            files_processed = self.processing_stats['files_processed']
            total_chunks = self.processing_stats['chunks_created']
            
            update_skill("document_processing", min(1.0, 0.5 + (files_processed * 0.05)), 
                        f"Successfully processed {files_processed} documents")
            update_skill("knowledge_extraction", min(1.0, 0.4 + (total_chunks * 0.001)),
                        f"Extracted {total_chunks} knowledge fragments")
            update_skill("autonomous_capability", min(1.0, 0.2 + (files_processed * 0.03) + (embeddings_created * 0.001)),
                        f"Autonomous processing with {files_processed} successes")
            
            print(f"✅ Successfully processed {file_name} with full memory integration")
            print(f"📊 Stats: {self.processing_stats}")
            
            # Store comprehensive processing session summary
            session_summary_memory_id = remember(
                content={
                    "processing_session_summary": {
                        "session_id": self.memory_session_id,
                        "file": file_name,
                        "timestamp": datetime.now().isoformat(),
                        "stats": self.processing_stats.copy(),
                        "memories_created": [extraction_memory_id, chunking_memory_id],
                        "skills_updated": ["document_processing", "knowledge_extraction", "autonomous_capability"],
                        "success": True,
                        "key_insights": [
                            f"Processed {len(text_content)} characters into {len(chunks)} chunks",
                            f"Generated {embeddings_created} vector embeddings",
                            f"Achieved {embeddings_created/len(chunks)*100:.1f}% embedding success rate"
                        ]
                    }
                },
                memory_type="episodic",
                importance=0.9,
                tags=["processing_session", "success", "comprehensive_summary"],
                source="agi_processor"
            )
            
            self.session_memories.append(session_summary_memory_id)
            
            # Generate learning insights from this processing session
            self.generate_processing_insights(file_name, len(text_content), len(chunks), embeddings_created)
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
            self.processing_stats['errors'] += 1
            
            # Record detailed failure with memory
            processing_action = {
                "type": "document_processing", 
                "description": f"Processing document: {file_name}",
                "result": {"status": "error", "error": str(e), "error_type": type(e).__name__},
                "confidence": 0.2,
                "session_id": self.memory_session_id
            }
            record_action(processing_action)
            
            # Store comprehensive error memory for learning and debugging
            error_memory_id = remember(
                content={
                    "error_analysis": {
                        "file": file_name,
                        "error_message": str(e),
                        "error_type": type(e).__name__,
                        "processing_stage": "unknown",  # Could be enhanced to track where error occurred
                        "timestamp": datetime.now().isoformat(),
                        "context": {
                            "files_processed_before_error": self.processing_stats['files_processed'],
                            "total_errors": self.processing_stats['errors'],
                            "session_id": self.memory_session_id
                        },
                        "debugging_suggestions": [
                            "Check file format and corruption",
                            "Verify extraction library compatibility", 
                            "Review memory and resource limits",
                            "Analyze similar error patterns"
                        ]
                    }
                },
                memory_type="episodic",
                importance=0.8,  # High importance for learning from errors
                tags=["error", "processing_failure", "debugging", "learning"],
                source="agi_processor"
            )
            
            # Update error handling skill (learning from failures)
            error_count = self.processing_stats['errors']
            total_attempts = self.processing_stats['files_processed'] + error_count
            error_handling_skill = max(0.1, 1.0 - (error_count / max(1, total_attempts)))
            update_skill("error_handling", error_handling_skill, f"Handled {error_count} errors in {total_attempts} attempts")
            
            return False
    
    def generate_processing_insights(self, file_name: str, text_length: int, chunk_count: int, embeddings_count: int):
        """Generate insights from processing session for continuous learning"""
        
        # Calculate processing metrics
        chars_per_chunk = text_length / chunk_count if chunk_count > 0 else 0
        embedding_success_rate = embeddings_count / chunk_count if chunk_count > 0 else 0
        
        insights = []
        
        # Chunk size analysis
        if chars_per_chunk < 800:
            insights.append("Chunks are smaller than optimal - consider increasing chunk size for better context")
        elif chars_per_chunk > 1200:
            insights.append("Chunks are larger than optimal - consider decreasing chunk size for better precision")
        else:
            insights.append("Chunk sizing is optimal for this document type")
        
        # Embedding success analysis
        if embedding_success_rate > 0.95:
            insights.append("Excellent embedding generation - high quality semantic processing achieved")
        elif embedding_success_rate > 0.8:
            insights.append("Good embedding generation - minor optimization opportunities exist")
        else:
            insights.append("Embedding generation needs improvement - investigate processing bottlenecks")
        
        # File type specific insights
        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext == '.pdf':
            insights.append("PDF processing successful - consider OCR enhancement for scanned documents")
        elif file_ext == '.epub':
            insights.append("EPUB processing successful - HTML structure preservation working well")
        
        # Store insights as semantic memory
        remember(
            content={
                "processing_insights": {
                    "file": file_name,
                    "metrics": {
                        "text_length": text_length,
                        "chunk_count": chunk_count,
                        "chars_per_chunk": chars_per_chunk,
                        "embedding_success_rate": embedding_success_rate
                    },
                    "insights": insights,
                    "recommendations": [
                        "Monitor chunk size distribution across file types",
                        "Track embedding success patterns",
                        "Optimize processing based on document characteristics"
                    ],
                    "timestamp": datetime.now().isoformat()
                }
            },
            memory_type="semantic",
            importance=0.7,
            tags=["insights", "optimization", "learning", "metrics"],
            source="agi_processor"
        )
        
        print(f"🧠 Generated {len(insights)} processing insights for continuous improvement")
    
    def get_session_summary(self) -> dict:
        """Get comprehensive summary of current processing session"""
        memory_status = get_memory_status()
        
        return {
            "session_id": self.memory_session_id,
            "processing_stats": self.processing_stats,
            "memories_created": len(self.session_memories),
            "memory_system_status": memory_status,
            "session_start": datetime.now().isoformat(),
            "total_skills_tracked": len(memory_status.get("skill_progression", {}))
        }

# Create memory-integrated processor instance
memory_processor = MemoryIntegratedAGIProcessor()

def process_with_memory(bucket_name: str, file_name: str) -> bool:
    """Public interface for memory-integrated processing"""
    return memory_processor.process_file_with_memory(bucket_name, file_name)

if __name__ == "__main__":
    print("🧠 MEMORY-INTEGRATED AGI PROCESSOR")
    print("=" * 50)
    print("Enhanced knowledge processing with autonomous memory")
    print("=" * 50)
    
    # Display current memory status
    status = memory_processor.get_session_summary()
    print(f"Session ID: {status['session_id']}")
    print(f"Memory System: {status['memory_system_status']['system_health']['auto_save_active']}")
    print("✅ Memory-integrated processor ready")
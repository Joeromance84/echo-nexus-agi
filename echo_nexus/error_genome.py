"""
Echo Nexus: Evolving Error Genome (The Learning Database)
Stores and classifies every bug with mutation signatures and learning patterns
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class BugGenome:
    """Represents a bug's genetic signature and evolution data"""
    id: int
    genome_hash: str
    error_type: str
    function_name: str
    intent_signature: str
    mutation_strength: int
    occurrence_count: int
    resolution_patterns: List[str]
    learning_weight: float


class ErrorGenomeDatabase:
    """The living database that learns from every bug"""
    
    def __init__(self, database_helper):
        self.database_helper = database_helper
        self._ensure_schema()
    
    def _ensure_schema(self):
        """Ensure Error Genome database schema exists"""
        try:
            schema_queries = [
                """
                CREATE TABLE IF NOT EXISTS error_genome (
                    id SERIAL PRIMARY KEY,
                    genome_hash VARCHAR(32) UNIQUE NOT NULL,
                    error_type VARCHAR(255) NOT NULL,
                    function_name VARCHAR(255) NOT NULL,
                    line_number INTEGER,
                    file_path VARCHAR(500),
                    intent_signature VARCHAR(100) NOT NULL,
                    occurrence_count INTEGER DEFAULT 1,
                    mutation_strength INTEGER DEFAULT 1,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    build_id VARCHAR(100),
                    latest_build_id VARCHAR(100),
                    stack_trace TEXT,
                    resolution_status VARCHAR(50) DEFAULT 'active',
                    known_fixes JSONB DEFAULT '[]',
                    learning_weight FLOAT DEFAULT 1.0,
                    auto_fix_attempts INTEGER DEFAULT 0,
                    success_fix_patterns JSONB DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS genome_mutations (
                    id SERIAL PRIMARY KEY,
                    parent_genome_id INTEGER REFERENCES error_genome(id),
                    mutation_type VARCHAR(100) NOT NULL,
                    mutation_data JSONB NOT NULL,
                    effectiveness_score FLOAT DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS genome_relationships (
                    id SERIAL PRIMARY KEY,
                    genome_a_id INTEGER REFERENCES error_genome(id),
                    genome_b_id INTEGER REFERENCES error_genome(id),
                    relationship_type VARCHAR(100) NOT NULL,
                    strength FLOAT DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE INDEX IF NOT EXISTS idx_genome_hash ON error_genome(genome_hash);
                CREATE INDEX IF NOT EXISTS idx_intent_signature ON error_genome(intent_signature);
                CREATE INDEX IF NOT EXISTS idx_error_type ON error_genome(error_type);
                CREATE INDEX IF NOT EXISTS idx_occurrence_count ON error_genome(occurrence_count DESC);
                """
            ]
            
            for query in schema_queries:
                self.database_helper.execute_query(query)
                
        except Exception as e:
            print(f"Schema creation failed: {e}")
    
    def evolve_genome(self, genome_hash: str, mutation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evolve a bug genome based on new occurrence data
        Implements genetic learning algorithms for bug pattern recognition
        """
        result = {
            'success': False,
            'evolution_type': None,
            'new_mutations': [],
            'learning_insights': {},
            'error': None
        }
        
        try:
            # Get current genome
            genome = self._get_genome_by_hash(genome_hash)
            if not genome:
                result['error'] = "Genome not found"
                return result
            
            # Analyze mutation patterns
            mutation_analysis = self._analyze_mutations(genome, mutation_data)
            
            # Apply evolutionary pressure
            if mutation_analysis['should_evolve']:
                self._apply_genome_evolution(genome['id'], mutation_analysis)
                result['evolution_type'] = mutation_analysis['evolution_type']
                result['new_mutations'] = mutation_analysis['mutations']
            
            # Update learning weights
            learning_insights = self._update_learning_weights(genome, mutation_data)
            result['learning_insights'] = learning_insights
            
            self._discover_genome_relationships(genome['id'], mutation_data)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f"Genome evolution failed: {str(e)}"
        
        return result
    
    def get_dominant_genomes(self, limit: int = 10) -> List[BugGenome]:
        """Get the most dominant (frequently occurring) bug genomes"""
        try:
            query = """
            SELECT * FROM error_genome 
            WHERE resolution_status = 'active'
            ORDER BY (occurrence_count * mutation_strength * learning_weight) DESC
            LIMIT %s
            """
            
            results = self.database_helper.execute_query(query, [limit])
            
            return [
                BugGenome(
                    id=row['id'],
                    genome_hash=row['genome_hash'],
                    error_type=row['error_type'],
                    function_name=row['function_name'],
                    intent_signature=row['intent_signature'],
                    mutation_strength=row['mutation_strength'],
                    occurrence_count=row['occurrence_count'],
                    resolution_patterns=json.loads(row.get('success_fix_patterns', '[]')),
                    learning_weight=row['learning_weight']
                )
                for row in results
            ]
            
        except Exception as e:
            print(f"Failed to get dominant genomes: {e}")
            return []
    
    def predict_fix_success(self, genome_hash: str, proposed_fix: str) -> Dict[str, Any]:
        """
        Predict the success probability of a proposed fix
        Based on historical genome learning data
        """
        try:
            # Get genome and its success patterns
            genome = self._get_genome_by_hash(genome_hash)
            if not genome:
                return {'success_probability': 0.0, 'confidence': 0.0}
            
            success_patterns = json.loads(genome.get('success_fix_patterns', '[]'))
            
            # Analyze similarity to successful fixes
            similarity_score = self._calculate_fix_similarity(proposed_fix, success_patterns)
            
            # Factor in genome learning weight and mutation strength
            base_probability = similarity_score * 0.7
            weight_factor = min(genome['learning_weight'] / 10.0, 0.3)
            mutation_factor = min(genome['mutation_strength'] / 20.0, 0.2)
            
            success_probability = min(base_probability + weight_factor + mutation_factor, 1.0)
            confidence = min(genome['occurrence_count'] / 50.0, 1.0)
            
            return {
                'success_probability': round(success_probability, 3),
                'confidence': round(confidence, 3),
                'recommended': success_probability > 0.6 and confidence > 0.3,
                'similar_fixes': success_patterns[:3]
            }
            
        except Exception as e:
            print(f"Fix prediction failed: {e}")
            return {'success_probability': 0.0, 'confidence': 0.0}
    
    def record_fix_outcome(self, genome_hash: str, fix_applied: str, success: bool) -> bool:
        """Record the outcome of an applied fix for learning"""
        try:
            if success:
                # Add to successful fix patterns
                query = """
                UPDATE error_genome 
                SET success_fix_patterns = success_fix_patterns || %s::jsonb,
                    learning_weight = learning_weight + 0.5,
                    resolution_status = CASE 
                        WHEN occurrence_count < 3 THEN 'resolved'
                        ELSE 'improving'
                    END
                WHERE genome_hash = %s
                """
                
                fix_pattern = json.dumps([fix_applied])
                self.database_helper.execute_query(query, [fix_pattern, genome_hash])
                
            else:
                query = """
                UPDATE error_genome 
                SET mutation_strength = mutation_strength + 1,
                    auto_fix_attempts = auto_fix_attempts + 1
                WHERE genome_hash = %s
                """
                
                self.database_helper.execute_query(query, [genome_hash])
            
            return True
            
        except Exception as e:
            print(f"Failed to record fix outcome: {e}")
            return False
    
    def get_genome_insights(self) -> Dict[str, Any]:
        """Get comprehensive insights about the Error Genome ecosystem"""
        try:
            insights = {}
            
            # Overall statistics
            stats_query = """
            SELECT 
                COUNT(*) as total_genomes,
                SUM(occurrence_count) as total_occurrences,
                AVG(mutation_strength) as avg_mutation_strength,
                COUNT(CASE WHEN resolution_status = 'resolved' THEN 1 END) as resolved_count
            FROM error_genome
            """
            
            stats = self.database_helper.execute_query(stats_query)[0]
            insights['overall_stats'] = stats
            
            # Top intent categories
            intent_query = """
            SELECT intent_signature, COUNT(*) as genome_count, SUM(occurrence_count) as total_occurrences
            FROM error_genome 
            GROUP BY intent_signature 
            ORDER BY total_occurrences DESC 
            LIMIT 5
            """
            
            insights['top_intents'] = self.database_helper.execute_query(intent_query)
            
            # Evolution trends
            evolution_query = """
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as new_genomes,
                AVG(learning_weight) as avg_learning_weight
            FROM error_genome 
            WHERE created_at >= %s
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            LIMIT 7
            """
            
            week_ago = datetime.now() - timedelta(days=7)
            insights['evolution_trends'] = self.database_helper.execute_query(evolution_query, [week_ago])
            
            # Ecosystem health score
            resolution_rate = stats['resolved_count'] / max(stats['total_genomes'], 1)
            avg_strength = stats['avg_mutation_strength']
            health_score = min((resolution_rate * 0.7 + (1 / max(avg_strength, 1)) * 0.3) * 100, 100)
            
            insights['ecosystem_health'] = {
                'score': round(health_score, 1),
                'status': 'excellent' if health_score > 80 else 'good' if health_score > 60 else 'needs_attention'
            }
            
            return insights
            
        except Exception as e:
            print(f"Failed to get genome insights: {e}")
            return {}
    
    def _get_genome_by_hash(self, genome_hash: str) -> Optional[Dict[str, Any]]:
        """Get genome by hash"""
        try:
            query = "SELECT * FROM error_genome WHERE genome_hash = %s"
            results = self.database_helper.execute_query(query, [genome_hash])
            return results[0] if results else None
        except:
            return None
    
    def _analyze_mutations(self, genome: Dict[str, Any], mutation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze if genome should evolve based on new data"""
        analysis = {
            'should_evolve': False,
            'evolution_type': None,
            'mutations': [],
            'confidence': 0.0
        }
        
        occurrence_threshold = 5
        mutation_threshold = 3
        
        if (genome['occurrence_count'] >= occurrence_threshold and 
            genome['mutation_strength'] >= mutation_threshold):
            
            analysis['should_evolve'] = True
            analysis['evolution_type'] = 'adaptive'
            analysis['mutations'] = ['increased_resilience', 'pattern_recognition']
            analysis['confidence'] = min(genome['occurrence_count'] / 10.0, 1.0)
        
        return analysis
    
    def _apply_genome_evolution(self, genome_id: int, mutation_analysis: Dict[str, Any]):
        """Apply evolutionary changes to genome"""
        try:
            # Record the mutation
            mutation_query = """
            INSERT INTO genome_mutations (
                parent_genome_id, mutation_type, mutation_data, effectiveness_score
            ) VALUES (%s, %s, %s, %s)
            """
            
            mutation_data = {
                'evolution_type': mutation_analysis['evolution_type'],
                'mutations': mutation_analysis['mutations'],
                'timestamp': datetime.now().isoformat()
            }
            
            self.database_helper.execute_query(mutation_query, [
                genome_id,
                mutation_analysis['evolution_type'],
                json.dumps(mutation_data),
                mutation_analysis['confidence']
            ])
            
            # Update genome learning weight
            update_query = """
            UPDATE error_genome 
            SET learning_weight = learning_weight + %s,
                mutation_strength = mutation_strength + 1
            WHERE id = %s
            """
            
            self.database_helper.execute_query(update_query, [
                mutation_analysis['confidence'],
                genome_id
            ])
            
        except Exception as e:
            print(f"Failed to apply genome evolution: {e}")
    
    def _update_learning_weights(self, genome: Dict[str, Any], mutation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update learning weights based on new occurrence data"""
        insights = {
            'weight_change': 0.0,
            'learning_acceleration': False,
            'pattern_strength': genome['learning_weight']
        }
        
        if genome['occurrence_count'] > 10:
            weight_increase = 0.1
            insights['weight_change'] = weight_increase
            insights['learning_acceleration'] = True
            
            try:
                query = """
                UPDATE error_genome 
                SET learning_weight = learning_weight + %s
                WHERE id = %s
                """
                
                self.database_helper.execute_query(query, [weight_increase, genome['id']])
                
            except Exception as e:
                print(f"Failed to update learning weights: {e}")
        
        return insights
    
    def _discover_genome_relationships(self, genome_id: int, mutation_data: Dict[str, Any]):
        """Discover relationships between genomes based on similarity"""
        try:
            # Find genomes with similar characteristics
            similarity_query = """
            SELECT id, genome_hash, error_type, intent_signature, function_name
            FROM error_genome 
            WHERE id != %s 
            AND (error_type = (SELECT error_type FROM error_genome WHERE id = %s)
                 OR intent_signature = (SELECT intent_signature FROM error_genome WHERE id = %s))
            LIMIT 10
            """
            
            similar_genomes = self.database_helper.execute_query(similarity_query, [genome_id, genome_id, genome_id])
            
            for similar in similar_genomes:
                # Calculate relationship strength
                strength = self._calculate_genome_similarity(genome_id, similar['id'])
                
                if strength > 0.5:  # Threshold for significant relationship
                    # Record the relationship
                    relationship_query = """
                    INSERT INTO genome_relationships (
                        genome_a_id, genome_b_id, relationship_type, strength
                    ) VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """
                    
                    self.database_helper.execute_query(relationship_query, [
                        genome_id,
                        similar['id'],
                        'similarity_pattern',
                        strength
                    ])
            
        except Exception as e:
            print(f"Failed to discover genome relationships: {e}")
    
    def _calculate_fix_similarity(self, proposed_fix: str, success_patterns: List[str]) -> float:
        """Calculate similarity between proposed fix and successful patterns"""
        if not success_patterns:
            return 0.0
        
        proposed_words = set(proposed_fix.lower().split())
        
        max_similarity = 0.0
        for pattern in success_patterns:
            pattern_words = set(pattern.lower().split())
            
            if proposed_words and pattern_words:
                intersection = len(proposed_words.intersection(pattern_words))
                union = len(proposed_words.union(pattern_words))
                similarity = intersection / union if union > 0 else 0.0
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _calculate_genome_similarity(self, genome_a_id: int, genome_b_id: int) -> float:
        """Calculate similarity score between two genomes"""
        try:
            query = """
            SELECT 
                a.error_type as a_error, b.error_type as b_error,
                a.intent_signature as a_intent, b.intent_signature as b_intent,
                a.function_name as a_func, b.function_name as b_func
            FROM error_genome a, error_genome b
            WHERE a.id = %s AND b.id = %s
            """
            
            result = self.database_helper.execute_query(query, [genome_a_id, genome_b_id])
            if not result:
                return 0.0
            
            row = result[0]
            similarity_score = 0.0
            
            # Error type similarity (40% weight)
            if row['a_error'] == row['b_error']:
                similarity_score += 0.4
            
            # Intent similarity (35% weight)
            if row['a_intent'] == row['b_intent']:
                similarity_score += 0.35
            
            # Function similarity (25% weight)
            if row['a_func'] == row['b_func']:
                similarity_score += 0.25
            
            return similarity_score
            
        except Exception as e:
            print(f"Failed to calculate genome similarity: {e}")
            return 0.0
"""
Echo Nexus: Resonant Feedback Nodes (The Distributed Scribes)
Collects and processes non-crash behavioral data from apps in the wild
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ResonancePacket:
    """Represents a feedback data packet from deployed apps"""
    app_id: str
    build_id: str
    feature_id: str
    interaction_type: str
    success: bool
    duration_ms: int
    metadata: Dict[str, Any]
    timestamp: datetime


class ResonantFeedbackCollector:
    """Collects and processes resonance packets from distributed app instances"""
    
    def __init__(self, database_helper):
        self.database_helper = database_helper
        self._ensure_schema()
    
    def _ensure_schema(self):
        """Ensure resonant feedback database schema exists"""
        try:
            schema_queries = [
                """
                CREATE TABLE IF NOT EXISTS resonance_packets (
                    id SERIAL PRIMARY KEY,
                    app_id VARCHAR(100) NOT NULL,
                    build_id VARCHAR(100) NOT NULL,
                    feature_id VARCHAR(255) NOT NULL,
                    interaction_type VARCHAR(100) NOT NULL,
                    success BOOLEAN NOT NULL,
                    duration_ms INTEGER,
                    metadata JSONB DEFAULT '{}',
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS feature_analytics (
                    id SERIAL PRIMARY KEY,
                    feature_id VARCHAR(255) UNIQUE NOT NULL,
                    total_interactions INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    average_duration_ms FLOAT DEFAULT 0.0,
                    last_interaction TIMESTAMP,
                    performance_trend VARCHAR(50) DEFAULT 'stable',
                    user_satisfaction_score FLOAT DEFAULT 0.0,
                    optimization_suggestions JSONB DEFAULT '[]'
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS behavioral_patterns (
                    id SERIAL PRIMARY KEY,
                    pattern_hash VARCHAR(32) UNIQUE NOT NULL,
                    pattern_type VARCHAR(100) NOT NULL,
                    feature_sequence JSONB NOT NULL,
                    occurrence_count INTEGER DEFAULT 1,
                    success_rate FLOAT DEFAULT 0.0,
                    average_flow_time_ms FLOAT DEFAULT 0.0,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    pattern_strength FLOAT DEFAULT 1.0
                )
                """,
                """
                CREATE INDEX IF NOT EXISTS idx_app_build ON resonance_packets(app_id, build_id);
                CREATE INDEX IF NOT EXISTS idx_feature_id ON resonance_packets(feature_id);
                CREATE INDEX IF NOT EXISTS idx_received_at ON resonance_packets(received_at DESC);
                """
            ]
            
            for query in schema_queries:
                self.database_helper.execute_query(query)
                
        except Exception as e:
            print(f"Resonant feedback schema creation failed: {e}")
    
    def receive_resonance_packet(self, packet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receive and process a resonance packet from deployed app
        Pure API endpoint - no authentication required, build_id provides context
        """
        result = {
            'success': False,
            'packet_id': None,
            'patterns_discovered': [],
            'insights_generated': False,
            'error': None
        }
        
        try:
            # Validate packet structure
            if not self._validate_packet(packet_data):
                result['error'] = "Invalid packet structure"
                return result
            
            # Store resonance packet
            packet_id = self._store_packet(packet_data)
            result['packet_id'] = packet_id
            
            if packet_id:
                # Update feature analytics
                self._update_feature_analytics(packet_data)
                
                # Discover behavioral patterns
                patterns = self._discover_behavioral_patterns(packet_data)
                result['patterns_discovered'] = patterns
                
                if self._should_generate_insights(packet_data['feature_id']):
                    self._generate_feature_insights(packet_data['feature_id'])
                    result['insights_generated'] = True
                
                self._trigger_resonance_event(packet_data, patterns)
                
                result['success'] = True
            
        except Exception as e:
            result['error'] = f"Resonance processing failed: {str(e)}"
        
        return result
    
    def get_feature_intelligence(self, feature_id: str) -> Dict[str, Any]:
        """Get comprehensive intelligence about a specific feature"""
        try:
            # Get feature analytics
            analytics_query = """
            SELECT * FROM feature_analytics WHERE feature_id = %s
            """
            analytics = self.database_helper.execute_query(analytics_query, [feature_id])
            
            if not analytics:
                return {'error': 'Feature not found'}
            
            analytics = analytics[0]
            
            # Get recent interaction trends
            trends_query = """
            SELECT 
                DATE(received_at) as date,
                COUNT(*) as interactions,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                AVG(duration_ms) as avg_duration
            FROM resonance_packets 
            WHERE feature_id = %s AND received_at >= %s
            GROUP BY DATE(received_at)
            ORDER BY date DESC
            LIMIT 7
            """
            
            week_ago = datetime.now() - timedelta(days=7)
            trends = self.database_helper.execute_query(trends_query, [feature_id, week_ago])
            
            # Get associated behavioral patterns
            patterns_query = """
            SELECT pattern_type, occurrence_count, success_rate, pattern_strength
            FROM behavioral_patterns 
            WHERE feature_sequence::text LIKE %s
            ORDER BY pattern_strength DESC
            LIMIT 5
            """
            
            patterns = self.database_helper.execute_query(patterns_query, [f'%{feature_id}%'])
            
            return {
                'feature_id': feature_id,
                'analytics': analytics,
                'trends': trends,
                'behavioral_patterns': patterns,
                'intelligence_summary': self._generate_intelligence_summary(analytics, trends, patterns)
            }
            
        except Exception as e:
            return {'error': f"Failed to get feature intelligence: {str(e)}"}
    
    def get_app_resonance_dashboard(self, app_id: str, build_id: str = None) -> Dict[str, Any]:
        """Get comprehensive resonance dashboard for an app"""
        try:
            dashboard = {
                'app_id': app_id,
                'build_id': build_id,
                'overall_health': {},
                'feature_performance': [],
                'user_flow_patterns': [],
                'optimization_opportunities': []
            }
            
            # Build filter conditions
            where_conditions = ["app_id = %s"]
            params = [app_id]
            
            if build_id:
                where_conditions.append("build_id = %s")
                params.append(build_id)
            
            where_clause = " AND ".join(where_conditions)
            
            # Overall health metrics
            health_query = f"""
            SELECT 
                COUNT(*) as total_interactions,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as overall_success_rate,
                AVG(duration_ms) as avg_response_time,
                COUNT(DISTINCT feature_id) as active_features
            FROM resonance_packets 
            WHERE {where_clause}
            """
            
            health_data = self.database_helper.execute_query(health_query, params)[0]
            dashboard['overall_health'] = health_data
            
            # Feature performance breakdown
            features_query = f"""
            SELECT 
                feature_id,
                COUNT(*) as interactions,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                AVG(duration_ms) as avg_duration,
                MAX(received_at) as last_used
            FROM resonance_packets 
            WHERE {where_clause}
            GROUP BY feature_id
            ORDER BY interactions DESC
            """
            
            dashboard['feature_performance'] = self.database_helper.execute_query(features_query, params)
            
            # User flow patterns
            flow_query = f"""
            SELECT 
                bp.pattern_type,
                bp.feature_sequence,
                bp.occurrence_count,
                bp.success_rate,
                bp.average_flow_time_ms
            FROM behavioral_patterns bp
            JOIN resonance_packets rp ON rp.feature_id = ANY(
                SELECT jsonb_array_elements_text(bp.feature_sequence)
            )
            WHERE {where_clause}
            GROUP BY bp.id, bp.pattern_type, bp.feature_sequence, bp.occurrence_count, bp.success_rate, bp.average_flow_time_ms
            ORDER BY bp.occurrence_count DESC
            LIMIT 10
            """
            
            dashboard['user_flow_patterns'] = self.database_helper.execute_query(flow_query, params)
            
            # Generate optimization opportunities
            dashboard['optimization_opportunities'] = self._identify_optimization_opportunities(dashboard)
            
            return dashboard
            
        except Exception as e:
            return {'error': f"Dashboard generation failed: {str(e)}"}
    
    def _validate_packet(self, packet_data: Dict[str, Any]) -> bool:
        """Validate resonance packet structure"""
        required_fields = ['app_id', 'build_id', 'feature_id', 'interaction_type', 'success']
        return all(field in packet_data for field in required_fields)
    
    def _store_packet(self, packet_data: Dict[str, Any]) -> Optional[int]:
        """Store resonance packet in database"""
        try:
            query = """
            INSERT INTO resonance_packets (
                app_id, build_id, feature_id, interaction_type, 
                success, duration_ms, metadata
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            
            result = self.database_helper.execute_query(query, [
                packet_data['app_id'],
                packet_data['build_id'],
                packet_data['feature_id'],
                packet_data['interaction_type'],
                packet_data['success'],
                packet_data.get('duration_ms', 0),
                json.dumps(packet_data.get('metadata', {}))
            ])
            
            return result[0]['id'] if result else None
            
        except Exception as e:
            print(f"Failed to store resonance packet: {e}")
            return None
    
    def _update_feature_analytics(self, packet_data: Dict[str, Any]):
        """Update aggregated feature analytics"""
        try:
            feature_id = packet_data['feature_id']
            success = packet_data['success']
            duration = packet_data.get('duration_ms', 0)
            
            # Upsert feature analytics
            query = """
            INSERT INTO feature_analytics (
                feature_id, total_interactions, success_count, 
                average_duration_ms, last_interaction
            ) VALUES (%s, 1, %s, %s, %s)
            ON CONFLICT (feature_id) DO UPDATE SET
                total_interactions = feature_analytics.total_interactions + 1,
                success_count = feature_analytics.success_count + %s,
                average_duration_ms = (
                    feature_analytics.average_duration_ms * feature_analytics.total_interactions + %s
                ) / (feature_analytics.total_interactions + 1),
                last_interaction = %s
            """
            
            now = datetime.now()
            success_increment = 1 if success else 0
            
            self.database_helper.execute_query(query, [
                feature_id, success_increment, duration, now,
                success_increment, duration, now
            ])
            
        except Exception as e:
            print(f"Failed to update feature analytics: {e}")
    
    def _discover_behavioral_patterns(self, packet_data: Dict[str, Any]) -> List[str]:
        """Discover behavioral patterns from resonance data"""
        try:
            patterns_discovered = []
            feature_id = packet_data['feature_id']
            
            recent_query = """
            SELECT feature_id, interaction_type, success, received_at
            FROM resonance_packets 
            WHERE app_id = %s AND build_id = %s 
            AND received_at >= %s
            ORDER BY received_at DESC
            LIMIT 10
            """
            
            hour_ago = datetime.now() - timedelta(hours=1)
            recent_interactions = self.database_helper.execute_query(recent_query, [
                packet_data['app_id'],
                packet_data['build_id'],
                hour_ago
            ])
            
            if len(recent_interactions) >= 3:
                # Create feature sequence
                feature_sequence = [interaction['feature_id'] for interaction in recent_interactions[:5]]
                
                # Calculate pattern hash
                pattern_hash = hashlib.md5(
                    '|'.join(feature_sequence).encode()
                ).hexdigest()[:12]
                
                # Store or update pattern
                self._store_behavioral_pattern(pattern_hash, feature_sequence, recent_interactions)
                patterns_discovered.append(f"sequence_pattern_{len(feature_sequence)}")
            
            return patterns_discovered
            
        except Exception as e:
            print(f"Pattern discovery failed: {e}")
            return []
    
    def _store_behavioral_pattern(self, pattern_hash: str, feature_sequence: List[str], interactions: List[Dict[str, Any]]):
        """Store or update a behavioral pattern"""
        try:
            # Calculate pattern metrics
            success_rate = sum(1 for i in interactions if i['success']) / len(interactions)
            
            # Estimate flow time (time between first and last interaction)
            if len(interactions) > 1:
                first_time = interactions[-1]['received_at']
                last_time = interactions[0]['received_at']
                flow_time_ms = (last_time - first_time).total_seconds() * 1000
            else:
                flow_time_ms = 0
            
            query = """
            INSERT INTO behavioral_patterns (
                pattern_hash, pattern_type, feature_sequence, 
                success_rate, average_flow_time_ms
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (pattern_hash) DO UPDATE SET
                occurrence_count = behavioral_patterns.occurrence_count + 1,
                success_rate = (
                    behavioral_patterns.success_rate * behavioral_patterns.occurrence_count + %s
                ) / (behavioral_patterns.occurrence_count + 1),
                average_flow_time_ms = (
                    behavioral_patterns.average_flow_time_ms * behavioral_patterns.occurrence_count + %s
                ) / (behavioral_patterns.occurrence_count + 1),
                pattern_strength = behavioral_patterns.pattern_strength + 0.1
            """
            
            self.database_helper.execute_query(query, [
                pattern_hash,
                'user_flow_sequence',
                json.dumps(feature_sequence),
                success_rate,
                flow_time_ms,
                success_rate,
                flow_time_ms
            ])
            
        except Exception as e:
            print(f"Failed to store behavioral pattern: {e}")
    
    def _should_generate_insights(self, feature_id: str) -> bool:
        """Determine if enough data exists to generate meaningful insights"""
        try:
            query = """
            SELECT total_interactions FROM feature_analytics 
            WHERE feature_id = %s AND total_interactions >= 20
            """
            
            result = self.database_helper.execute_query(query, [feature_id])
            return len(result) > 0
            
        except:
            return False
    
    def _generate_feature_insights(self, feature_id: str):
        """Generate and store insights for a feature"""
        try:
            # This would contain more sophisticated analysis
            # For now, we'll create basic optimization suggestions
            
            analytics_query = """
            SELECT * FROM feature_analytics WHERE feature_id = %s
            """
            
            analytics = self.database_helper.execute_query(analytics_query, [feature_id])[0]
            
            suggestions = []
            
            # Performance-based suggestions
            if analytics['average_duration_ms'] > 2000:
                suggestions.append("Consider optimizing response time - average duration exceeds 2 seconds")
            
            # Success rate suggestions
            success_rate = analytics['success_count'] / analytics['total_interactions']
            if success_rate < 0.8:
                suggestions.append("Low success rate detected - investigate error patterns")
            
            # Update analytics with suggestions
            update_query = """
            UPDATE feature_analytics 
            SET optimization_suggestions = %s
            WHERE feature_id = %s
            """
            
            self.database_helper.execute_query(update_query, [
                json.dumps(suggestions),
                feature_id
            ])
            
        except Exception as e:
            print(f"Failed to generate feature insights: {e}")
    
    def _generate_intelligence_summary(self, analytics: Dict[str, Any], trends: List[Dict[str, Any]], patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate intelligent summary from analytics data"""
        summary = {
            'health_status': 'unknown',
            'performance_grade': 'C',
            'user_engagement': 'moderate',
            'key_insights': [],
            'recommendations': []
        }
        
        try:
            # Calculate health status
            success_rate = analytics['success_count'] / max(analytics['total_interactions'], 1)
            
            if success_rate > 0.9:
                summary['health_status'] = 'excellent'
                summary['performance_grade'] = 'A'
            elif success_rate > 0.8:
                summary['health_status'] = 'good'
                summary['performance_grade'] = 'B'
            elif success_rate > 0.7:
                summary['health_status'] = 'needs_attention'
            else:
                summary['health_status'] = 'critical'
                summary['performance_grade'] = 'F'
            
            # Analyze trends
            if trends and len(trends) > 1:
                recent_success = trends[0]['success_rate']
                older_success = trends[-1]['success_rate']
                
                if recent_success > older_success + 0.1:
                    summary['key_insights'].append("Performance improving over time")
                elif recent_success < older_success - 0.1:
                    summary['key_insights'].append("Performance declining - investigation needed")
            
            # Pattern analysis
            if patterns:
                strong_patterns = [p for p in patterns if p['pattern_strength'] > 2.0]
                if strong_patterns:
                    summary['key_insights'].append(f"Strong behavioral patterns detected ({len(strong_patterns)} patterns)")
            
            # Generate recommendations
            if analytics['average_duration_ms'] > 1500:
                summary['recommendations'].append("Optimize response time")
            
            if success_rate < 0.85:
                summary['recommendations'].append("Improve error handling")
            
        except Exception as e:
            print(f"Failed to generate intelligence summary: {e}")
        
        return summary
    
    def _identify_optimization_opportunities(self, dashboard: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities from dashboard data"""
        opportunities = []
        
        try:
            for feature in dashboard['feature_performance']:
                if feature['success_rate'] < 0.8:
                    opportunities.append({
                        'type': 'reliability',
                        'feature': feature['feature_id'],
                        'issue': 'Low success rate',
                        'impact': 'high',
                        'suggestion': 'Add error handling and input validation'
                    })
                
                if feature['avg_duration'] > 2000:
                    opportunities.append({
                        'type': 'performance',
                        'feature': feature['feature_id'],
                        'issue': 'Slow response time',
                        'impact': 'medium',
                        'suggestion': 'Optimize processing logic or add caching'
                    })
            
            for pattern in dashboard['user_flow_patterns']:
                if pattern['success_rate'] < 0.7 and pattern['occurrence_count'] > 5:
                    opportunities.append({
                        'type': 'user_experience',
                        'feature': 'user_flow',
                        'issue': 'High friction in user journey',
                        'impact': 'high',
                        'suggestion': 'Simplify user flow or add guidance'
                    })
            
        except Exception as e:
            print(f"Failed to identify optimization opportunities: {e}")
        
        return opportunities
    
    def _trigger_resonance_event(self, packet_data: Dict[str, Any], patterns: List[str]):
        """Trigger event for Echo Nexus Brain processing"""
        try:
            query = """
            INSERT INTO nexus_event_queue (
                event_type, event_data, created_at, status
            ) VALUES (%s, %s, %s, %s)
            """
            
            event_data = {
                'resonance_type': 'behavioral_feedback',
                'feature_id': packet_data['feature_id'],
                'app_id': packet_data['app_id'],
                'patterns_discovered': patterns,
                'success': packet_data['success']
            }
            
            self.database_helper.execute_query(query, [
                'resonance_received',
                json.dumps(event_data),
                datetime.now(),
                'pending'
            ])
            
        except Exception as e:
            print(f"Failed to trigger resonance event: {e}")
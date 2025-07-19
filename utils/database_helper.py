import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import uuid

class DatabaseHelper:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Drop existing tables if they exist (for fresh start)
                cursor.execute("DROP TABLE IF EXISTS chat_history CASCADE")
                cursor.execute("DROP TABLE IF EXISTS project_templates CASCADE")
                cursor.execute("DROP TABLE IF EXISTS build_history CASCADE")
                cursor.execute("DROP TABLE IF EXISTS user_preferences CASCADE")
                cursor.execute("DROP TABLE IF EXISTS workflows CASCADE")
                # Create workflows table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS workflows (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        workflow_yaml TEXT NOT NULL,
                        template_type VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_session VARCHAR(255),
                        is_validated BOOLEAN DEFAULT FALSE,
                        validation_errors TEXT,
                        policy_compliant BOOLEAN DEFAULT FALSE,
                        policy_issues TEXT
                    )
                """)
                
                # Create build_history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS build_history (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        workflow_id UUID REFERENCES workflows(id),
                        repository_url VARCHAR(500),
                        build_status VARCHAR(50),
                        build_logs TEXT,
                        error_message TEXT,
                        build_duration INTEGER,
                        apk_size BIGINT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        github_run_id VARCHAR(100),
                        commit_sha VARCHAR(40)
                    )
                """)
                
                # Create user_preferences table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_session VARCHAR(255) UNIQUE,
                        preferred_python_version VARCHAR(10),
                        preferred_java_version VARCHAR(10),
                        default_build_type VARCHAR(20),
                        enable_caching BOOLEAN DEFAULT TRUE,
                        notification_settings JSONB,
                        custom_buildozer_config TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create project_templates table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS project_templates (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        project_structure JSONB,
                        buildozer_spec_template TEXT,
                        requirements_template TEXT,
                        workflow_template_id UUID REFERENCES workflows(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_public BOOLEAN DEFAULT TRUE,
                        usage_count INTEGER DEFAULT 0
                    )
                """)
                
                # Create chat_history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_session VARCHAR(255),
                        user_message TEXT NOT NULL,
                        assistant_response TEXT NOT NULL,
                        generated_workflow_id UUID REFERENCES workflows(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_type VARCHAR(50) DEFAULT 'chat'
                    )
                """)
                
                conn.commit()
    
    def save_workflow(self, name: str, description: str, workflow_yaml: str, 
                     template_type: str = None, user_session: str = None) -> str:
        """Save a workflow to database"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                workflow_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO workflows (id, name, description, workflow_yaml, template_type, user_session)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (workflow_id, name, description, workflow_yaml, template_type, user_session))
                
                result = cursor.fetchone()
                conn.commit()
                return str(result['id'])
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow by ID"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM workflows WHERE id = %s
                """, (workflow_id,))
                
                result = cursor.fetchone()
                return dict(result) if result else None
    
    def get_user_workflows(self, user_session: str, limit: int = 50) -> List[Dict]:
        """Get workflows for a user session"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM workflows 
                    WHERE user_session = %s 
                    ORDER BY updated_at DESC 
                    LIMIT %s
                """, (user_session, limit))
                
                return [dict(row) for row in cursor.fetchall()]
    
    def update_workflow_validation(self, workflow_id: str, is_validated: bool, 
                                  validation_errors: str = None, policy_compliant: bool = False,
                                  policy_issues: str = None):
        """Update workflow validation status"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE workflows 
                    SET is_validated = %s, validation_errors = %s, 
                        policy_compliant = %s, policy_issues = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (is_validated, validation_errors, policy_compliant, policy_issues, workflow_id))
                
                conn.commit()
    
    def save_build_history(self, workflow_id: str, repository_url: str, 
                          build_status: str, build_logs: str = None,
                          error_message: str = None, build_duration: int = None,
                          apk_size: int = None, github_run_id: str = None,
                          commit_sha: str = None) -> str:
        """Save build history entry"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                build_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO build_history 
                    (id, workflow_id, repository_url, build_status, build_logs, 
                     error_message, build_duration, apk_size, github_run_id, commit_sha)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (build_id, workflow_id, repository_url, build_status, build_logs,
                      error_message, build_duration, apk_size, github_run_id, commit_sha))
                
                result = cursor.fetchone()
                conn.commit()
                return str(result['id'])
    
    def get_build_history(self, workflow_id: str = None, limit: int = 100) -> List[Dict]:
        """Get build history"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if workflow_id:
                    cursor.execute("""
                        SELECT bh.*, w.name as workflow_name 
                        FROM build_history bh
                        JOIN workflows w ON bh.workflow_id = w.id
                        WHERE bh.workflow_id = %s 
                        ORDER BY bh.created_at DESC 
                        LIMIT %s
                    """, (workflow_id, limit))
                else:
                    cursor.execute("""
                        SELECT bh.*, w.name as workflow_name 
                        FROM build_history bh
                        JOIN workflows w ON bh.workflow_id = w.id
                        ORDER BY bh.created_at DESC 
                        LIMIT %s
                    """, (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
    
    def save_user_preferences(self, user_session: str, preferences: Dict) -> str:
        """Save or update user preferences"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_preferences 
                    (user_session, preferred_python_version, preferred_java_version, 
                     default_build_type, enable_caching, notification_settings, 
                     custom_buildozer_config)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_session) 
                    DO UPDATE SET 
                        preferred_python_version = EXCLUDED.preferred_python_version,
                        preferred_java_version = EXCLUDED.preferred_java_version,
                        default_build_type = EXCLUDED.default_build_type,
                        enable_caching = EXCLUDED.enable_caching,
                        notification_settings = EXCLUDED.notification_settings,
                        custom_buildozer_config = EXCLUDED.custom_buildozer_config,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING id
                """, (
                    user_session,
                    preferences.get('preferred_python_version', '3.9'),
                    preferences.get('preferred_java_version', '11'),
                    preferences.get('default_build_type', 'debug'),
                    preferences.get('enable_caching', True),
                    json.dumps(preferences.get('notification_settings', {})),
                    preferences.get('custom_buildozer_config', '')
                ))
                
                result = cursor.fetchone()
                conn.commit()
                return str(result['id'])
    
    def get_user_preferences(self, user_session: str) -> Optional[Dict]:
        """Get user preferences"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM user_preferences WHERE user_session = %s
                """, (user_session,))
                
                result = cursor.fetchone()
                if result:
                    prefs = dict(result)
                    if prefs['notification_settings']:
                        prefs['notification_settings'] = json.loads(prefs['notification_settings'])
                    return prefs
                return None
    
    def save_chat_message(self, user_session: str, user_message: str, 
                         assistant_response: str, generated_workflow_id: str = None,
                         message_type: str = 'chat') -> str:
        """Save chat history"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                message_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO chat_history 
                    (id, user_session, user_message, assistant_response, 
                     generated_workflow_id, message_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (message_id, user_session, user_message, assistant_response,
                      generated_workflow_id, message_type))
                
                result = cursor.fetchone()
                conn.commit()
                return str(result['id'])
    
    def get_chat_history(self, user_session: str, limit: int = 50) -> List[Dict]:
        """Get chat history for user session"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT ch.*, w.name as workflow_name 
                    FROM chat_history ch
                    LEFT JOIN workflows w ON ch.generated_workflow_id = w.id
                    WHERE ch.user_session = %s 
                    ORDER BY ch.created_at DESC 
                    LIMIT %s
                """, (user_session, limit))
                
                return [dict(row) for row in cursor.fetchall()]
    
    def get_workflow_analytics(self) -> Dict[str, Any]:
        """Get workflow usage analytics"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Total workflows
                cursor.execute("SELECT COUNT(*) as total_workflows FROM workflows")
                total_workflows = cursor.fetchone()['total_workflows']
                
                # Workflows by template type
                cursor.execute("""
                    SELECT template_type, COUNT(*) as count 
                    FROM workflows 
                    WHERE template_type IS NOT NULL 
                    GROUP BY template_type
                """)
                workflows_by_type = {row['template_type']: row['count'] for row in cursor.fetchall()}
                
                # Build success rate
                cursor.execute("""
                    SELECT 
                        build_status,
                        COUNT(*) as count,
                        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
                    FROM build_history 
                    GROUP BY build_status
                """)
                build_stats = {row['build_status']: {
                    'count': row['count'], 
                    'percentage': float(row['percentage'])
                } for row in cursor.fetchall()}
                
                # Recent activity
                cursor.execute("""
                    SELECT DATE(created_at) as date, COUNT(*) as workflows_created
                    FROM workflows 
                    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                    GROUP BY DATE(created_at)
                    ORDER BY date DESC
                """)
                recent_activity = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'total_workflows': total_workflows,
                    'workflows_by_type': workflows_by_type,
                    'build_stats': build_stats,
                    'recent_activity': recent_activity
                }
    
    def search_workflows(self, search_term: str, user_session: str = None) -> List[Dict]:
        """Search workflows by name or description"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if user_session:
                    cursor.execute("""
                        SELECT * FROM workflows 
                        WHERE user_session = %s 
                        AND (name ILIKE %s OR description ILIKE %s)
                        ORDER BY updated_at DESC
                    """, (user_session, f'%{search_term}%', f'%{search_term}%'))
                else:
                    cursor.execute("""
                        SELECT * FROM workflows 
                        WHERE name ILIKE %s OR description ILIKE %s
                        ORDER BY updated_at DESC
                    """, (f'%{search_term}%', f'%{search_term}%'))
                
                return [dict(row) for row in cursor.fetchall()]
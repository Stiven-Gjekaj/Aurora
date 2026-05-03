import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
import logging

class MemorySystem:
    def __init__(self, db_path: str = "aurora_memory.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create topics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE NOT NULL,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create relationships table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_topic_id INTEGER,
                    target_topic_id INTEGER,
                    relationship_type TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_topic_id) REFERENCES topics (id),
                    FOREIGN KEY (target_topic_id) REFERENCES topics (id)
                )
            ''')
            
            # Create topic_content table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS topic_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER,
                    content_type TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (topic_id) REFERENCES topics (id)
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
    
    def store_topic(self, title: str, summary: str = None) -> int:
        """Store a topic in memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO topics (title, summary)
                VALUES (?, ?)
                ON CONFLICT(title) DO UPDATE SET
                    summary=excluded.summary,
                    updated_at=CURRENT_TIMESTAMP
            ''', (title, summary))

            cursor.execute('SELECT id FROM topics WHERE title = ?', (title,))
            topic_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return topic_id
        except Exception as e:
            self.logger.error(f"Error storing topic: {e}")
            return -1
    
    def store_content(self, topic_id: int, content_type: str, content: str) -> bool:
        """Store content related to a topic"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO topic_content (topic_id, content_type, content)
                VALUES (?, ?, ?)
            ''', (topic_id, content_type, content))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error storing content: {e}")
            return False
    
    def create_relationship(self, source_topic: str, target_topic: str, 
                          relationship_type: str, description: str = None) -> bool:
        """Create a relationship between two topics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get topic IDs
            cursor.execute('SELECT id FROM topics WHERE title = ?', (source_topic,))
            source_result = cursor.fetchone()
            
            cursor.execute('SELECT id FROM topics WHERE title = ?', (target_topic,))
            target_result = cursor.fetchone()
            
            if not source_result or not target_result:
                self.logger.warning("One or both topics not found")
                return False
            
            source_id = source_result[0]
            target_id = target_result[0]
            
            cursor.execute('''
                INSERT INTO relationships (source_topic_id, target_topic_id, relationship_type, description)
                VALUES (?, ?, ?, ?)
            ''', (source_id, target_id, relationship_type, description))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error creating relationship: {e}")
            return False
    
    def get_topic(self, title: str) -> Dict[str, Any]:
        """Retrieve a topic by title"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, summary, created_at, updated_at
                FROM topics WHERE title = ?
            ''', (title,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'title': result[1],
                    'summary': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                }
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving topic: {e}")
            return None
    
    def get_all_topics(self) -> List[Dict[str, Any]]:
        """Retrieve all topics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, summary, created_at, updated_at
                FROM topics
                ORDER BY updated_at DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'title': row[1],
                    'summary': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                }
                for row in results
            ]
        except Exception as e:
            self.logger.error(f"Error retrieving topics: {e}")
            return []
    
    def get_topic_relationships(self, topic_title: str) -> List[Dict[str, Any]]:
        """Get all relationships for a topic"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.relationship_type, r.description, t2.title as target_topic
                FROM relationships r
                JOIN topics t1 ON r.source_topic_id = t1.id
                JOIN topics t2 ON r.target_topic_id = t2.id
                WHERE t1.title = ?
            ''', (topic_title,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'relationship_type': row[0],
                    'description': row[1],
                    'target_topic': row[2]
                }
                for row in results
            ]
        except Exception as e:
            self.logger.error(f"Error retrieving relationships: {e}")
            return []
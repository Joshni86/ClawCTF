"""
Database module for handling SQLite operations.

This module contains all database-related functionality including
initialization and user authentication queries.
"""

import sqlite3
import os
from typing import Optional, Tuple


class Database:
    """Database handler for user authentication system."""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
    
    def init_db(self) -> None:
        """Initialize the database with default users."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
        
        # Insert default users
        cursor.execute("INSERT INTO users VALUES ('admin', 'supersecuresdgsdgsd')")
        cursor.execute("INSERT INTO users VALUES ('DR001', 'Dr.doom')")
        cursor.execute("INSERT INTO users VALUES ('NR123', 'nurse2024')")
        cursor.execute("INSERT INTO users VALUES ('DR042', 'medic@lStaff')")
        
        conn.commit()
        conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Tuple[str, str]]:
        """
        Authenticate user with given credentials.
        
        NOTE: This method intentionally contains a SQL injection vulnerability
        for demonstration purposes. The query is constructed using string formatting
        which allows for SQL injection attacks.
        
        Args:
            username: The username to authenticate
            password: The password to authenticate
            
        Returns:
            Tuple of (username, password) if authentication successful, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # VULNERABILITY: SQL injection vulnerability maintained for educational purposes
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            result = cursor.fetchone()
        except Exception as e:
            result = None
        finally:
            conn.close()
        
        return result


# Global database instance
db = Database()

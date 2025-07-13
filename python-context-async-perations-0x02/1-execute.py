#!/usr/bin/env python3
import sqlite3


class ExcuteQuery:
    """Create a Reusable context manager takes query as input,
    and executes it"""
    def __init__(self, db_name, query, parm):
        self.db_name = db_name
        self.query = query
        self.parm = parm
        self.connection = None
        self.result = None
    
    def __enter__(self):
        """Open connection with the database."""
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, (self.parm,))
        self.result = cursor.fetchall()
        
        return self.result
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close connection."""
        if self.connection:
            self.connection.close()
    
    
    if __name__ == "__main__":
        db_name = "db.db"
        query = "SELECT * FROM users WHERE age > ?"
        parm = 25
        
        with ExcuteQuery(db_name, query, parm) as result:
            for row in result:
                print(row)
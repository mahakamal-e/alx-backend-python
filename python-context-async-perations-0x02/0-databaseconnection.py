#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """ create a custom context manager to manage
    opening and closing a database connection automatically"""
    def __init__(self, db_name):
        self.db_name = db_name
    
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exe_value, traceback):
        if self.connection:
            self.connection.close()
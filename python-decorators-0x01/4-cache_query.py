import time
import sqlite3 
import functools


query_cache = {}


def with_db_connection(func):
    """Automatically handles opening and closing database connections.""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """A decorator to cache database query results."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query")
        if not query:
            raise ValueError("No query provided")

       
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]

        
        print("Executing query and caching result")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

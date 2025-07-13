#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = 'db.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows
        

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FORM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows
        

async def fetch_concurrently():
    """Used to make two func works in same time."""
    users_all, users_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users")
    for user in users_all:
        print(user)
    print("All User older than 40")
    for user in users_older:
        print(user)
        


    





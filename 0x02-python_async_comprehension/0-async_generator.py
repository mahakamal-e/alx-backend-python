#!/usr/bin/env python3
""" Define a coroutine called async_generator """
import asyncio
import random
from typing import Generator

async def async_generator() -> Generator[float, None, None]:
    """
    The coroutine wil loop 10 times each asynchronously wait 1 sec
    then yiled a random number between 0 to 10
    """
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)

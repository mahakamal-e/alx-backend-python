#!/usr/bin/env python3
""" Define coroutine function wait_n """
import asyncio
from typing import List
from 0-basic_async_syntax import wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    An asynchronous coroutine that spawns wait_random n times
    with the specified max_delay.
    Returns a list of delays in ascending order.
    """
    delays = []

    async def append_delay():
        delay = await wait_random(max_delay)
        delays.append(delay)

    await asyncio.gather(*(append_delay() for _ in range(n)))

    return sorted(delays)

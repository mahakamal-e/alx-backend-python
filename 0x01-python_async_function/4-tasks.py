#!/usr/bin/env python3
""" Define coroutine function task_wait_n """
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Return the list of all the delays"""
    delay = []
    for i in range(n):
        delay_task = task_wait_random(max_delay)
        result = await delay_task
        delay.append(result)
    return sorted(delay)

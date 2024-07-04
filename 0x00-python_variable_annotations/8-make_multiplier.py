#!/usr/bin/env python3
""" Define make_multiplier function """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """returns a function that multiplies a float by multiplier"""
    def multiply_func(x: float) -> float:
        return x * multiplier
    return multiply_func

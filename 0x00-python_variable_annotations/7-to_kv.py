#!/usr/bin/env python3
""" Define to_kv function """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Returns Tuple of k and square v """
    return (k, v ** 2)

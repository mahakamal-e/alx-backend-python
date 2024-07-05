#!/usr/bin/env python3
""" define function element_length"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns list of tuples"""
    return [(i, len(i)) for i in lst]

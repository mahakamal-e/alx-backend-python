#!/usr/bin/env python3
""" Define sum_mixed_list function """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """a type-annotated function sum_mixed_list."""
    return sum(mxd_lst)

#!/usr/bin/env python3
""" Define safe_first_element function """
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return the first element of lst if it is not empty"""
    if lst:
        return lst[0]
    else:
        return None

#!/usr/bin/env python
# -*- coding: utf-8 -*-


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Return True if the values a and b are close to each other and False otherwise. (Clone from Python 3.5)

    Args:
        a: A float.
        b: A float.
        rel_tol: The relative tolerance – it is the maximum allowed difference between a and b, relative to the larger
         absolute value of a or b. For example, to set a tolerance of 5%, pass rel_tol=0.05. The default tolerance is
          1e-09, which assures that the two values are the same within about 9 decimal digits. rel_tol must be greater
          than zero.
        abs_tol: The minimum absolute tolerance – useful for comparisons near zero. abs_tol must be at least zero.

    Returns:
        True if the values a and b are close to each other and False otherwise.
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

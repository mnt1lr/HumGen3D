# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE

import functools
import traceback

import bpy
from HumGen3D.backend import hg_log


def injected_context(func):
    """Replaces keyword argument "context=None" with bpy.context if left at default None value"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        varnames = func.__code__.co_varnames
        if "context" not in varnames:
            raise TypeError("No argument 'context' in function arguments.")

        context_arg_index = varnames.index("context")
        context_in_args = len(args) >= (context_arg_index + 1)
        if not context_in_args and "context" not in kwargs:
            kwargs["context"] = bpy.context

            hg_log(traceback.extract_stack()[-2])
            hg_log(
                f"Argument 'context' for function '{func.__name__}' substituted with bpy.context. It's highly recommended to pass your own context!",
                level="WARNING",
            )

        return func(*args, **kwargs)

    return wrapper

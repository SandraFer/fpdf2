"""
Utilities to manage deprecation errors & warnings.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

import contextlib
import inspect
import os.path
import warnings
from types import ModuleType


class WarnOnDeprecatedModuleAttributes(ModuleType):
    def __call__(self):
        raise TypeError(
            "You tried to instantied the fpdf module."
            " You probably want to import the FPDF class instead:"
            " from fpdf import FPDF"
        )

    def __getattr__(self, name):
        if name in ("FPDF_CACHE_DIR", "FPDF_CACHE_MODE"):
            warnings.warn(
                (
                    "fpdf.FPDF_CACHE_DIR & fpdf.FPDF_CACHE_MODE"
                    " have been deprecated in favour of"
                    " FPDF(font_cache_dir=...)"
                ),
                DeprecationWarning,
                stacklevel=get_stack_level(),
            )
            return None
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in ("FPDF_CACHE_DIR", "FPDF_CACHE_MODE"):
            warnings.warn(
                (
                    "fpdf.FPDF_CACHE_DIR & fpdf.FPDF_CACHE_MODE"
                    " have been deprecated in favour of"
                    " FPDF(font_cache_dir=...)"
                ),
                DeprecationWarning,
                stacklevel=get_stack_level(),
            )
            return
        super().__setattr__(name, value)


def get_stack_level() -> int:
    """Get the first place in the call stack that is not inside fpdf2"""

    # pylint: disable=import-outside-toplevel
    import fpdf  # pylint: disable=cyclic-import

    pkg_dir = os.path.dirname(fpdf.__file__)
    contextlib_dir = os.path.dirname(contextlib.__file__)

    frame = inspect.currentframe()
    n = 0
    while frame is not None:
        fname = inspect.getfile(frame)
        if fname.startswith(pkg_dir) or fname.startswith(contextlib_dir):
            frame = frame.f_back
            n += 1
        else:
            break
    return n

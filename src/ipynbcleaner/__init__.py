"""ipynbcleaner package."""

from .cleaner import CleanOptions, NotebookCleanError, clean_notebook, clean_notebook_file

__all__ = [
    "CleanOptions",
    "NotebookCleanError",
    "clean_notebook",
    "clean_notebook_file",
]

__version__ = "0.1.0"

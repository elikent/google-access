"""
google_access package
High-level API for Google Workspace integrations.
"""

# Re-export subpackages for cleaner imports
from . import io
from . import utils
from . import constants
from . import transforms

# Optional: promote specific frequently used items
from .constants import SCOPES, MIME_TYPES
from .utils import report

__all__ = ["io", "utils", "constants", "transforms",
           "report", "SCOPES", "MIME_TYPES"]

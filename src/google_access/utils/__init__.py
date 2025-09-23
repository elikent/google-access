"""
google_access.utils
Shared utilities and constants for Google API access.
"""

from .constants import SCOPES, MIME_TYPES  # from constants.py in this folder, import SCOPES
from .text_utils import remove_diacritics, canon

__all__ = ["SCOPES", 
           "MIME_TYPES", 
           "remove_diacritics", 
           "canon"
           ]  # add to public interface

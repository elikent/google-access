"""
google_access.utils
Shared utilities and constants for Google API access.
"""
from .text_utils import remove_diacritics, canon
from .log_utils import logging_config, report

__all__ = ["remove_diacritics",
           "canon",
           "logging_config",
           "report",
           ]  # add to public interface

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
from .constants import SCOPES, MIME_TYPES, SERVICE_ACCOUNT_ENV_VAR_NAME, get_service_account_path

constant_list = ["SCOPES",
             "MIME_TYPES",
             "SERVICE_ACCOUNT_ENV_VAR_NAME",
             "get_service_account_path"
             ]

__all__ = ["io", "constants", "transforms",
           ] + constant_list


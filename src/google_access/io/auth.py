from __future__ import annotations
import logging
from typing import Sequence, Optional, Any
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError

from google_access import report

logger = logging.getLogger(__name__)

def authenticate(
        service_account_file: Path,
        scopes: Sequence[str],
        verbose: bool = True) -> Optional[Credentials]:
    """
    Create service-account credentials for Google APIs.
    Returns None on failure; caller decides how to proceed.
    """
    try:
        creds = Credentials.from_service_account_file(
            str(service_account_file),
            scopes=scopes
        )
        return creds
    except FileNotFoundError as e:
        msg = f"Auth error: service account file not found: {e}"
        report(msg, "error", verbose=verbose)
    except (ValueError, DefaultCredentialsError) as e:
        msg = f"Auth error: invalid credentials or file format: {e}"
        report(msg, "error", verbose=verbose)
    except Exception as e:
        # very rare; catch-all so callers don't crash
        msg = f"Auth error (unexpected): {e}"
        report(msg, "error", verbose=verbose)
    return None


def build_service(
        service_name: str,
        version: str,
        creds: Credentials,
        verbose: bool =True) -> Optional[Any]:
    """
    Build and return a Google API service client (Drive/Sheets/Docs/etc.)
    Example: build_service('drive', 'v3', creds)
    """
    try:
        # build the connection (service) to the API
        # cache_discovery=False avoids cache warnings on some systems
        service = build(
            service_name,
            version,
            credentials=creds,
            cache_discovery=False
        )

        return service
    except HttpError as e:
        msg = f"Discovery/HTTP error building {service_name} {version}: {e}"
        report(msg, "error", verbose=verbose)
    except Exception as e:
        # very rare; catch-all so callers don't crash
        msg = f'Unexpected error building {service_name} {version}: {e}'
        report(msg, "error", verbose=verbose)
    return None


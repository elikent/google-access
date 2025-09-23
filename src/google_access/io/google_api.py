from typing import Sequence, Optional, Any, List, Dict
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def authenticate(service_account_file: Path, scopes: Sequence[str]) -> Credentials:
    """Create credentials for a service account."""
    return Credentials.from_service_account_file(str(service_account_file), scopes=scopes)

def build_service(creds: Credentials) -> object:
    """Build and return a Drive v3 service client."""
    try:
        # build the connection (service) to the API for v3 of Google Drive
        service = build("drive", "v3", credentials=creds)

        return service
    except HttpError as e:
        print(f"Drive API error while building service: {e}")
        return None


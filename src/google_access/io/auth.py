import logging
from typing import Sequence, Optional, Any, List, Dict
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

def authenticate(service_account_file: Path, scopes: Sequence[str]) -> Credentials:
    """Create credentials for a service account."""
    try: 
        creds = Credentials.from_service_account_file(str(service_account_file), scopes=scopes)
        return creds
    except HttpError as e:
        msg = f"Drive API error in authenticate: {e}"
        print(msg)
        logger.error(msg)
        return None
        

def build_service(creds: Credentials) -> object:
    """Build and return a Drive v3 service client."""
    try:
        # build the connection (service) to the API for v3 of Google Drive
        service = build("drive", "v3", credentials=creds)

        return service
    except HttpError as e:
        msg = f"Drive API error in build_service: {e}"
        print(msg)
        logger.error(msg)
        return None


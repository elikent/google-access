from typing import Optional, Any, List, Dict
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

def authenticate(service_account_file: Path, scopes: list):
    """Authenticates with the Google Drive API using a service account."""
    return Credentials.from_service_account_file(service_account_file, scopes=scopes)

def build_service(creds: Credentials, folder_id: str) -> object:
    """Builds the Google Drive service."""
    try:
        # build the connection (service) to the API for v3 of Google Drive
        service = build("drive", "v3", credentials=creds)

        print(f"Looking for folders in folder: {folder_id}\n")

        return service

    except HttpError as error:
        print(f"An error occurred: {error}")
    except FileNotFoundError:
        print(f"ERROR: The service account file was not found.")
        print(f"Please make sure the file 'service-account.json' is in the correct directory.")
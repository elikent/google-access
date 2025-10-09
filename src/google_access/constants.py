from pathlib import Path
import os

# Google API scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.readonly",
]

MIME_TYPES = {
    "pdf": "application/pdf",
    "img": "image/jpg",
    "sheets": "application/vnd.google-apps.spreadsheet",
    "csv": "text/csv",
    "txt": "text/plain",
    "html": "text/html",
    "doc": "application/vnd.google-apps.document",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# Name of the environment variable holding the service account path
SERVICE_ACCOUNT_ENV_VAR_NAME = "GA_LEROF_SERVICE_ACCOUNT"

def get_service_account_path() -> Path:
    '''
    Return the Path to the service account file.
    Reads from env var defined above, with a safe default.
    '''
    env_value = os.getenv(SERVICE_ACCOUNT_ENV_VAR_NAME)
    if env_value:
        return Path(env_value)
    else:
        return Path('.secrets/google-access-drive-sa.json')

__all__ = ["SCOPES", "MIME_TYPES", "SERVICE_ACCOUNT_ENV_VAR_NAME","get_service_account_path"]

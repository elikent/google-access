from __future__ import annotations
from pathlib import Path
from typing import Sequence, Optional, Any

from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource

from google_access.io.auth import authenticate, build_service
from google_access import SCOPES
from google_access import report
from google_access import get_service_account_path


def check_service_account_path():
    ok = get_service_account_path().exists()
    if ok:
        msg = 'Service account key found'
        report(msg, verbose=True)
        return ok
    else:
        msg = 'Service account key not found'
        report(msg, 'error', verbose=True)
        return ok

def check_auth(
        creds_path: Path,
        scopes: Sequence[str],
        report_verbose: bool = True
    ) -> bool:
    '''
    Attempts to authenticate. If successful, returns True.
    '''
    creds = authenticate(creds_path, scopes, verbose=True)
    ok = creds is not None
    report(f'Auth check: {'OK' if ok else 'FAILED'}', f'{'info' if ok else 'error'}',verbose=report_verbose)
    return ok

def check_drive_access(drive: Resource, report_verbose: bool = True) -> bool:
    try:
        '''
        minimal query to prove permissions and connectivity.
        if get a response and drive has files, provides sample.
        '''
        resp = drive.files().list(pageSize=1, fields="files(id, name)").execute()
        files=resp.get('files', [])
        if files:
            msg = f"Drive access OK. Sample: {files[0]['name']} ({files[0]['id']})"
        else:
            msg = "Drive access OK. No files found."
        report(msg, verbose=report_verbose)
    except HttpError as e:
        msg = f"Drive API error: {e}"
        report(msg, "error", verbose=report_verbose)
        return False
    except Exception as e:
        msg = f'Drive access unexpected error: {e}'
        report(msg, "error", verbose=report_verbose)
        return False

def check_sheets_access(
        sheets: Resource,
        spreadsheet_id: str,
        report_verbose: bool = True
    ) -> bool:
    try:
        meta = sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        titles = [s['properties']['title'] for s in meta.get('sheets', [])]
        msg = f'Sheets accee OK. Tabs: {", ".join(titles) if titles else "(none)"}'
        report(msg, verbose=report_verbose)
        return True
    except HttpError as e:
        msg = f"Sheets access failed : {e}"
        report(msg, "error", verbose=report_verbose)
        return False
    except Exception as e:
        msg = f'Sheets access unexpected error: {e}'
        report(msg, "error", verbose=report_verbose)
        return False

def main():
    creds_path = Path()


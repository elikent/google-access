from typing import Optional, Any, List, Dict
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

def get_folder_items(
    service: Resource, 
    folder_id: str, 
    page_size: int = 100, 
    fields: str = "nextPageToken, files(id, name, mimeType)", 
    mimeType: Optional[str] = None
) -> List[Dict[str, Any]]:
    
    """Return files in a Drive folder, optionally filtered by mimeType."""
    # Build the query safely, adding mimeType only if provided
    parts = [f"'{folder_id}' in parents", "trashed = false"]
    if mimeType:
        parts.append(f"mimeType = '{mimeType}'")
    query = " and ".join(parts)

    try:
        items: List[Dict[str, Any]] = []
        page_token: Optional[str] = None

        # Builds a dictionary with key 'files' and a list of dicts, one dict per file, with keys 'name' and 'id'
        while True:
            resp = (
                service.files()
                .list(
                    q=query, 
                    pageSize=page_size, 
                    fields=fields, 
                    pageToken=page_token
                )
                .execute()
            )
            # Add items with files
            items.extend(resp.get("files", []))
            # page_token = bookmark - this is where you left off
            page_token = resp.get("nextPageToken")
            # Break when get to last page
            if not page_token:
                break
            
        return items

    except HttpError as e:
        print(f'Drive API error: {e}')
        return []

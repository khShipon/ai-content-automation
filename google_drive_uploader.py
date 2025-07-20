import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE = 'token_drive.pickle'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                logging.error(f"Token refresh failed: {e}")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Failed to build Google Drive service: {e}")
        raise

def move_doc_to_folder(doc_id, folder_id):
    service = get_drive_service()
    try:
        # Retrieve the existing parents to remove
        file = service.files().get(fileId=doc_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        # Move the file to the new folder
        file = service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        logging.info(f"Moved document {doc_id} to folder {folder_id}.")
        return file
    except HttpError as e:
        logging.error(f"Google Drive API error: {e}")
        raise
    except Exception as e:
        logging.error(f"Failed to move document: {e}")
        raise

if __name__ == "__main__":
    # Example usage: replace with your doc_id and folder_id
    doc_id = "your_doc_id_here"
    folder_id = "your_folder_id_here"
    move_doc_to_folder(doc_id, folder_id) 
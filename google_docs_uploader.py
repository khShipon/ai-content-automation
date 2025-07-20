import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE = 'token.pickle'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_google_docs_service():
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
        service = build('docs', 'v1', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Failed to build Google Docs service: {e}")
        raise

def create_google_doc(title, content):
    service = get_google_docs_service()
    try:
        doc = service.documents().create(body={"title": title}).execute()
        doc_id = doc.get('documentId')
        logging.info(f"Created Google Doc with ID: {doc_id}")
        # Insert content
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }
        ]
        service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        logging.info("Content inserted into Google Doc.")
        return doc_id
    except HttpError as e:
        logging.error(f"Google Docs API error: {e}")
        raise
    except Exception as e:
        logging.error(f"Failed to create Google Doc: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    doc_id = create_google_doc("Test Title", "This is a test content.")
    print(f"Created Google Doc ID: {doc_id}") 
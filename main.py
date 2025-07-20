import logging
from content_generator import ContentGenerator
from google_docs_uploader import create_google_doc
from google_drive_uploader import move_doc_to_folder
import datetime
import os

# Set your Google Drive folder ID here
FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'your_folder_id_here')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Step 1: Generate content
        generator = ContentGenerator()
        topic = generator.get_random_topic()
        content = generator.generate_content(topic)
        logging.info(f"Generated content for topic: {topic}")

        # Step 2: Create Google Doc
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        doc_title = f"{today} - {topic}"
        doc_id = create_google_doc(doc_title, content)
        logging.info(f"Created Google Doc with ID: {doc_id}")

        # Step 3: Move Doc to Google Drive folder
        if FOLDER_ID == 'your_folder_id_here':
            logging.warning("Please set your Google Drive FOLDER_ID in the .env file or as an environment variable.")
        else:
            move_doc_to_folder(doc_id, FOLDER_ID)
            logging.info(f"Uploaded document to Google Drive folder: {FOLDER_ID}")

    except Exception as e:
        logging.error(f"Workflow failed: {e}")

if __name__ == "__main__":
    main() 
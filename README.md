# AI Content Automation Agent

## Setup Instructions

1. **Google Cloud Credentials**
   - Place your `credentials.json` file (downloaded from Google Cloud Console) in the project root directory (same folder as this README).

2. **OpenRouter API Key**
   - Copy your OpenRouter API key into a file named `.env` in the project root:
     
     ```env
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id_here
     ```
   - Never share your API key publicly.

3. **First-Time Google Auth**
   - On first run, the script will prompt you to authenticate with your Google account in a browser. Follow the instructions to allow access.

4. **Install Dependencies**
   - Run:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Script**
   - To generate and upload content, run:
     ```bash
     python main.py
     ```

6. **Automate Daily Execution**
   - **Windows Task Scheduler:**
     - Open Task Scheduler > Create Task > Actions > New > Program/script: `python`, Add arguments: `main.py`, Start in: path to your project folder.
     - Set the trigger to run daily or hourly as needed.
   - **Linux/macOS (cron):**
     - Run `crontab -e` and add a line like:
       ```
       0 * * * * /usr/bin/python3 /path/to/your/project/main.py
       ```
     - This example runs the script every hour.

7. **Google Drive Folder**
   - Create a folder in your Google Drive and copy its ID into your `.env` as `GOOGLE_DRIVE_FOLDER_ID`.

## Logging & Troubleshooting
- Logs are printed to the console. Check for error messages if something fails.
- Ensure your credentials and API keys are correct and not expired.

---

**Enjoy your automated Bangla-English content generator!** 
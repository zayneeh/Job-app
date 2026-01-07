import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from agents.config import Config

class JobTracker:
    def __init__(self):
        # Setup Google Sheets authentication
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Load credentials from service account file
        creds = Credentials.from_service_account_file(
            'credentials.json', 
            scopes=scope
        )
        
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(Config.GOOGLE_SHEET_ID).sheet1
        
        # Initialize headers if sheet is empty
        self._initialize_headers()
    
    def _initialize_headers(self):
        """Create header row if sheet is empty"""
        if not self.sheet.row_values(1):
            headers = [
                'Date Applied', 'Company', 'Job Title', 
                'Match Score', 'Job URL', 'Status', 'Resume Used'
            ]
            self.sheet.append_row(headers)
    
    def is_duplicate(self, job_url):
        """Check if job URL already exists in sheet"""
        try:
            all_urls = self.sheet.col_values(5)  # Column E (Job URL)
            return job_url in all_urls
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False
    
    def add_entry(self, job_data, match_score, resume_type):
        """Add new job application entry to sheet"""
        try:
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                job_data.get('company', 'Unknown'),
                job_data.get('title', 'Unknown'),
                f"{match_score:.2f}",
                job_data.get('url', ''),
                'Applied',
                resume_type
            ]
            self.sheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Error adding entry: {e}")
            return False
    
    def update_status(self, job_url, new_status):
        """Update application status for a specific job"""
        try:
            cell = self.sheet.find(job_url)
            self.sheet.update_cell(cell.row, 6, new_status)
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            return False

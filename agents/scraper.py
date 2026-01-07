import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from agents.config import Config

class JobScraper:
    def __init__(self):
        self.freshness_threshold = timedelta(days=Config.JOB_FRESHNESS_DAYS)
    
    def is_fresh_job(self, posted_date_str):
        """Filter out ghost jobs older than threshold"""
        try:
            # Parse common date formats
            posted_date = self._parse_date(posted_date_str)
            age = datetime.now() - posted_date
            return age <= self.freshness_threshold
        except Exception as e:
            print(f"Error parsing date: {e}")
            return True  # Include if we can't parse
    
    def _parse_date(self, date_str):
        """Parse various date string formats"""
        date_str = date_str.lower()
        
        # Handle relative dates
        if 'today' in date_str or 'just posted' in date_str:
            return datetime.now()
        elif 'yesterday' in date_str:
            return datetime.now() - timedelta(days=1)
        elif 'hour' in date_str:
            hours = int(''.join(filter(str.isdigit, date_str)) or 1)
            return datetime.now() - timedelta(hours=hours)
        elif 'day' in date_str:
            days = int(''.join(filter(str.isdigit, date_str)) or 1)
            return datetime.now() - timedelta(days=days)
        elif 'week' in date_str:
            weeks = int(''.join(filter(str.isdigit, date_str)) or 1)
            return datetime.now() - timedelta(weeks=weeks)
        
        # Try standard date formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.now()  # Default to now if unparseable
    
    def fetch_new_jobs(self, keyword, location=None):
        """
        Fetch jobs from job boards (placeholder for actual scraping logic)
        Returns list of job dictionaries
        """
        jobs = []
        
        # TODO: Implement actual scraping logic for LinkedIn, Indeed, etc.
        # This is a placeholder structure showing what data should be returned
        
        # Example structure:
        sample_job = {
            'title': 'Machine Learning Engineer',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'posted_date': 'today',
            'url': 'https://example.com/job/12345',
            'description': 'Full job description text here...'
        }
        
        # Filter for freshness
        if self.is_fresh_job(sample_job['posted_date']):
            jobs.append(sample_job)
        
        return jobs

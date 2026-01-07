from agents.config import Config
from agents.scraper import JobScraper
from agents.matcher import JobMatcher
from agents.tracker import JobTracker

def apply_to_job(job, resume_type):
    """
    Placeholder for actual application logic
    This could be:
    - Automated form filling with Selenium
    - Email generation and sending
    - API calls to job board application endpoints
    """
    print(f"\n{'='*60}")
    print(f"APPLYING TO: {job['title']} at {job['company']}")
    print(f"Using: {resume_type.upper()} resume")
    print(f"URL: {job['url']}")
    print(f"{'='*60}\n")
    
    # TODO: Implement actual application logic here
    return True

def run_agent(keyword="Machine Learning Engineer", max_applications=10):
    """Main agent execution loop"""
    print("🤖 Job Application Agent Starting...")
    print(f"Searching for: {keyword}")
    print(f"Minimum match score: {Config.MIN_MATCH_SCORE}\n")
    
    # Validate configuration
    Config.validate()
    
    # Initialize modules
    scraper = JobScraper()
    matcher = JobMatcher()
    tracker = JobTracker()
    
    # Track applications in this session
    applications_sent = 0
    
    # 1. SEARCH: Find fresh jobs
    print("📋 Fetching new job listings...")
    jobs = scraper.fetch_new_jobs(keyword=keyword)
    print(f"Found {len(jobs)} fresh jobs\n")
    
    for idx, job in enumerate(jobs, 1):
        if applications_sent >= max_applications:
            print(f"✅ Reached maximum of {max_applications} applications")
            break
        
        print(f"Processing job {idx}/{len(jobs)}: {job['title']}")
        
        # 2. CHECK MEMORY: Don't apply twice
        if tracker.is_duplicate(job['url']):
            print("⏭️  Already applied - skipping\n")
            continue
        
        # 3. EVALUATE: Ask Gemini if we fit
        print("🧠 Analyzing fit with AI...")
        result = matcher.score_job(job['description'])
        
        print(f"Match Score: {result['score']:.2f}")
        print(f"Best Resume: {result['best_resume']}")
        print(f"Reasoning: {result['reasoning']}")
        
        # 4. DECIDE: Apply if score meets threshold
        if result['score'] >= Config.MIN_MATCH_SCORE:
            print("✅ Score meets threshold - applying!")
            
            # 5. ACTION: Apply to job
            success = apply_to_job(job, result['best_resume'])
            
            if success:
                # 6. LOG: Update tracker
                tracker.add_entry(job, result['score'], result['best_resume'])
                applications_sent += 1
                print("📊 Logged to Google Sheets")
        else:
            print("❌ Score too low - skipping\n")
        
        print()
    
    print(f"\n🎉 Agent completed! Sent {applications_sent} applications.")

if __name__ == "__main__":
    # Run the agent
    run_agent(
        keyword="Machine Learning Engineer",
        max_applications=10
    )
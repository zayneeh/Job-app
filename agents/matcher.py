import google.generativeai as genai
from agents.config import Config

class JobMatcher:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Load resumes
        self.resumes = self._load_resumes()
    
    def _load_resumes(self):
        """Load both resume files"""
        resumes = {}
        try:
            with open(Config.INDUSTRY_RESUME, 'r') as f:
                resumes['industry'] = f.read()
            with open(Config.RESEARCH_RESUME, 'r') as f:
                resumes['research'] = f.read()
        except FileNotFoundError as e:
            print(f"Error loading resumes: {e}")
            raise
        return resumes
    
    def score_job(self, job_description):
        """
        Use Gemini to evaluate job fit and select best resume
        Returns: {'score': float, 'best_resume': str, 'reasoning': str}
        """
        prompt = f"""
You are an expert career advisor. I have two resumes:

INDUSTRY RESUME (Machine Learning Engineer focus):
{self.resumes['industry']}

RESEARCH RESUME (Research Intern focus):
{self.resumes['research']}

JOB DESCRIPTION:
{job_description}

Analyze which resume is the best fit for this job and provide:
1. A match score from 0.0 to 1.0 (where 1.0 is perfect fit)
2. Which resume to use ("industry" or "research")
3. Brief reasoning for your choice

Respond in this exact format:
SCORE: [number]
RESUME: [industry/research]
REASONING: [brief explanation]
"""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_response(response.text)
            return result
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return {'score': 0.0, 'best_resume': 'industry', 'reasoning': 'Error occurred'}
    
    def _parse_response(self, response_text):
        """Parse Gemini's structured response"""
        lines = response_text.strip().split('\n')
        result = {
            'score': 0.0,
            'best_resume': 'industry',
            'reasoning': ''
        }
        
        for line in lines:
            if line.startswith('SCORE:'):
                try:
                    result['score'] = float(line.split(':')[1].strip())
                except ValueError:
                    pass
            elif line.startswith('RESUME:'):
                resume_type = line.split(':')[1].strip().lower()
                if resume_type in ['industry', 'research']:
                    result['best_resume'] = resume_type
            elif line.startswith('REASONING:'):
                result['reasoning'] = line.split(':', 1)[1].strip()
        
        return result

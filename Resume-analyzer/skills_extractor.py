import re
from typing import List, Dict, Set
import spacy


class SkillsExtractor:
    """Extract technical skills from resume text using keyword matching and NLP."""
    
    # Comprehensive technical skills database
    TECHNICAL_SKILLS = {
        # Programming Languages
        'Programming Languages': [
            'python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'groovy', 'typescript',
            'dart', 'elixir', 'haskell', 'clojure', 'lua', 'vb.net', 'f#'
        ],
        # Web Technologies
        'Web Technologies': [
            'html', 'css', 'react', 'angular', 'vue.js', 'node.js', 'express',
            'django', 'flask', 'fastapi', 'spring', 'spring boot', 'asp.net',
            'webpack', 'babel', 'rest api', 'graphql', 'soap'
        ],
        # Databases
        'Databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'cassandra',
            'redis', 'elasticsearch', 'dynamodb', 'firestore', 'sqlite',
            'neo4j', 'couchdb', 'influxdb', 'mariadb'
        ],
        # Data Science & Analytics
        'Data Science': [
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
            'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn',
            'plotly', 'jupyter', 'data analysis', 'data visualization', 'nlp',
            'computer vision', 'cv', 'nlp', 'bert', 'gpt'
        ],
        # Cloud & DevOps
        'Cloud & DevOps': [
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
            'ci/cd', 'jenkins', 'gitlab', 'github actions', 'terraform', 'ansible',
            'cloudformation', 'helm', 'docker compose', 'openstack'
        ],
        # Tools & Platforms
        'Tools & Platforms': [
            'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
            'vim', 'vscode', 'intellij', 'eclipse', 'postman', 'swagger',
            'linux', 'unix', 'windows', 'macos', 'shell', 'bash'
        ],
        # Data Engineering
        'Data Engineering': [
            'spark', 'apache spark', 'hadoop', 'hive', 'etl', 'airflow', 'kafka',
            'nifi', 'beam', 'dbt', 'talend', 'informatica', 'pentaho'
        ],
        # Testing & QA
        'Testing & QA': [
            'junit', 'pytest', 'unittest', 'selenium', 'cucumber', 'testng',
            'mocha', 'jest', 'jasmine', 'cypress', 'robotframework', 'soapui',
            'jmeter', 'loadrunner', 'automation testing'
        ],
        # Mobile Development
        'Mobile Development': [
            'android', 'ios', 'flutter', 'react native', 'xamarin', 'ionic',
            'objective-c', 'swift', 'kotlin'
        ],
        # Version Control
        'Version Control': [
            'git', 'svn', 'mercurial', 'perforce', 'github', 'gitlab', 'bitbucket'
        ],
    }
    
    def __init__(self):
        """Initialize the skills extractor."""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("spacy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Create a flat list of all skills for quick lookup
        self.all_skills = []
        self.skill_to_category = {}
        for category, skills in self.TECHNICAL_SKILLS.items():
            for skill in skills:
                self.all_skills.append(skill.lower())
                self.skill_to_category[skill.lower()] = category
    
    def extract_skills_keyword_matching(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills using keyword matching.
        
        Args:
            text: Resume text to analyze
            
        Returns:
            Dictionary with skills grouped by category
        """
        text_lower = text.lower()
        found_skills = {}
        
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                category = self.skill_to_category[skill]
                if category not in found_skills:
                    found_skills[category] = []
                
                # Find the original case version in the text
                match = re.search(pattern, text_lower)
                if match:
                    original_text = text[match.start():match.end()]
                    found_skills[category].append(original_text)
        
        # Remove duplicates while preserving order
        for category in found_skills:
            found_skills[category] = list(dict.fromkeys(found_skills[category]))
        
        return found_skills
    
    def extract_skills_nlp(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills using NLP and noun phrases.
        
        Args:
            text: Resume text to analyze
            
        Returns:
            Dictionary with skills grouped by category
        """
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        found_skills = {}
        
        # Extract noun chunks that might be skills
        noun_phrases = set()
        for chunk in doc.noun_chunks:
            noun_phrases.add(chunk.text.lower().strip())
        
        # Match noun phrases against our skills database
        for phrase in noun_phrases:
            for skill in self.all_skills:
                if skill in phrase or phrase in skill:
                    category = self.skill_to_category[skill]
                    if category not in found_skills:
                        found_skills[category] = []
                    if phrase not in found_skills[category]:
                        found_skills[category].append(phrase)
        
        return found_skills
    
    def extract_skills(self, text: str, method: str = 'keyword') -> Dict[str, List[str]]:
        """
        Extract technical skills from resume text.
        
        Args:
            text: Resume text to analyze
            method: 'keyword', 'nlp', or 'combined'
            
        Returns:
            Dictionary with skills grouped by category
        """
        if method == 'keyword':
            return self.extract_skills_keyword_matching(text)
        elif method == 'nlp':
            return self.extract_skills_nlp(text)
        elif method == 'combined':
            keyword_skills = self.extract_skills_keyword_matching(text)
            nlp_skills = self.extract_skills_nlp(text)
            
            # Merge results
            combined = keyword_skills.copy()
            for category, skills in nlp_skills.items():
                if category not in combined:
                    combined[category] = []
                combined[category].extend(skills)
                combined[category] = list(dict.fromkeys(combined[category]))
            
            return combined
        else:
            raise ValueError("method must be 'keyword', 'nlp', or 'combined'")
    
    def get_skills_summary(self, text: str) -> Dict:
        """
        Get a summary of extracted skills with counts.
        
        Args:
            text: Resume text to analyze
            
        Returns:
            Summary dictionary with skill counts by category
        """
        skills = self.extract_skills(text, method='keyword')
        
        summary = {
            'total_skills': sum(len(v) for v in skills.values()),
            'categories': {}
        }
        
        for category, skill_list in skills.items():
            summary['categories'][category] = {
                'count': len(skill_list),
                'skills': skill_list
            }
        
        return summary


# Standalone function for quick usage
def extract_skills_from_text(text: str, method: str = 'keyword') -> Dict[str, List[str]]:
    """
    Quick function to extract skills from text.
    
    Args:
        text: Resume text
        method: Extraction method ('keyword', 'nlp', or 'combined')
        
    Returns:
        Dictionary of skills grouped by category
    """
    extractor = SkillsExtractor()
    return extractor.extract_skills(text, method)


if __name__ == "__main__":
    # Example usage
    sample_text = """
    Senior Software Engineer with 5+ years of experience.
    
    Skills:
    - Programming: Python, Java, JavaScript, TypeScript
    - Web: React, Node.js, Django, Flask
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS, Docker, Kubernetes
    - Data: Pandas, NumPy, Scikit-learn
    - DevOps: Git, Jenkins, CI/CD, Terraform
    
    Experience:
    - Built RESTful APIs using Spring Boot and FastAPI
    - Managed AWS infrastructure with CloudFormation
    - Developed React applications for web platform
    """
    
    extractor = SkillsExtractor()
    
    # Extract using different methods
    print("=== Keyword Matching ===")
    skills = extractor.extract_skills(sample_text, method='keyword')
    for category, skill_list in skills.items():
        print(f"{category}: {', '.join(skill_list)}")
    
    print("\n=== Skills Summary ===")
    summary = extractor.get_skills_summary(sample_text)
    print(f"Total Skills Found: {summary['total_skills']}")
    for category, data in summary['categories'].items():
        print(f"  {category}: {data['count']} skills")

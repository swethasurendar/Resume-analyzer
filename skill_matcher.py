from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class JobRole:
    """Represents a job role with required and preferred skills."""
    title: str
    required_skills: Set[str]
    preferred_skills: Set[str]
    description: str = ""


class JobRoleDatabase:
    """Database of job roles with required and preferred skills."""
    
    JOBS = {
        'Data Scientist': JobRole(
            title='Data Scientist',
            required_skills={'python', 'machine learning', 'data analysis', 'sql', 'pandas', 'scikit-learn'},
            preferred_skills={'tensorflow', 'pytorch', 'deep learning', 'aws', 'spark', 'tableau', 'nlp'},
            description='Analyze complex datasets and build predictive models'
        ),
        'Backend Engineer': JobRole(
            title='Backend Engineer',
            required_skills={'python', 'java', 'sql', 'rest api', 'git'},
            preferred_skills={'docker', 'kubernetes', 'aws', 'ci/cd', 'microservices', 'mongodb', 'redis'},
            description='Design and maintain server-side applications'
        ),
        'Frontend Engineer': JobRole(
            title='Frontend Engineer',
            required_skills={'javascript', 'html', 'css', 'react', 'git'},
            preferred_skills={'typescript', 'vue.js', 'angular', 'webpack', 'jest', 'node.js'},
            description='Build interactive user interfaces'
        ),
        'Full Stack Developer': JobRole(
            title='Full Stack Developer',
            required_skills={'javascript', 'html', 'css', 'python', 'sql', 'rest api', 'git'},
            preferred_skills={'react', 'node.js', 'docker', 'aws', 'mongodb', 'postgresql'},
            description='Build complete web applications from frontend to backend'
        ),
        'DevOps Engineer': JobRole(
            title='DevOps Engineer',
            required_skills={'linux', 'docker', 'kubernetes', 'git', 'bash', 'ci/cd'},
            preferred_skills={'aws', 'terraform', 'ansible', 'jenkins', 'gitlab', 'monitoring'},
            description='Manage infrastructure and deployment pipelines'
        ),
        'Data Engineer': JobRole(
            title='Data Engineer',
            required_skills={'python', 'sql', 'etl', 'spark', 'data analysis'},
            preferred_skills={'hadoop', 'kafka', 'airflow', 'aws', 'dbt', 'hive'},
            description='Build data pipelines and infrastructure'
        ),
        'Cloud Architect': JobRole(
            title='Cloud Architect',
            required_skills={'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'terraform'},
            preferred_skills={'security', 'monitoring', 'networking', 'ci/cd', 'microservices'},
            description='Design and implement cloud infrastructure solutions'
        ),
        'Machine Learning Engineer': JobRole(
            title='Machine Learning Engineer',
            required_skills={'python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch'},
            preferred_skills={'nlp', 'computer vision', 'aws', 'kubernetes', 'sql', 'data analysis'},
            description='Develop and deploy machine learning models'
        ),
        'QA Automation Engineer': JobRole(
            title='QA Automation Engineer',
            required_skills={'automation testing', 'selenium', 'python', 'junit', 'git'},
            preferred_skills={'api testing', 'ci/cd', 'docker', 'performance testing', 'jest'},
            description='Automate testing and ensure software quality'
        ),
        'Solutions Architect': JobRole(
            title='Solutions Architect',
            required_skills={'aws', 'azure', 'docker', 'sql', 'microservices', 'rest api'},
            preferred_skills={'kubernetes', 'terraform', 'ci/cd', 'security', 'networking'},
            description='Design technical solutions for business problems'
        ),
    }
    
    @classmethod
    def get_job_role(cls, job_title: str) -> JobRole:
        """Get a job role by title."""
        return cls.JOBS.get(job_title)
    
    @classmethod
    def list_job_titles(cls) -> List[str]:
        """List all available job titles."""
        return list(cls.JOBS.keys())


class SkillMatcher:
    """Match resume skills with job roles and suggest missing skills."""
    
    def __init__(self):
        self.job_db = JobRoleDatabase()
    
    def normalize_skills(self, skills: Dict[str, List[str]]) -> Set[str]:
        """
        Normalize skills from extracted dictionary format to flat set.
        
        Args:
            skills: Dictionary of skills grouped by category
            
        Returns:
            Set of normalized skill strings
        """
        normalized = set()
        for category, skill_list in skills.items():
            for skill in skill_list:
                normalized.add(skill.lower().strip())
        return normalized
    
    def match_skills(self, resume_skills: Set[str], job_role: JobRole) -> Dict:
        """
        Match resume skills against a job role's required and preferred skills.
        
        Args:
            resume_skills: Set of skills from resume
            job_role: Target job role
            
        Returns:
            Dictionary with matching results
        """
        resume_skills_normalized = {s.lower().strip() for s in resume_skills}
        
        required_matched = resume_skills_normalized & job_role.required_skills
        preferred_matched = resume_skills_normalized & job_role.preferred_skills
        
        required_missing = job_role.required_skills - resume_skills_normalized
        preferred_missing = job_role.preferred_skills - resume_skills_normalized
        
        # Calculate match percentage (weighted toward required skills)
        total_required = len(job_role.required_skills)
        total_preferred = len(job_role.preferred_skills)
        
        required_percentage = (len(required_matched) / total_required * 100) if total_required > 0 else 0
        preferred_percentage = (len(preferred_matched) / total_preferred * 100) if total_preferred > 0 else 0
        
        # Overall match: 70% weight on required, 30% on preferred
        overall_match = (required_percentage * 0.7) + (preferred_percentage * 0.3)
        
        return {
            'job_role': job_role.title,
            'overall_match_percentage': round(overall_match, 2),
            'required_match_percentage': round(required_percentage, 2),
            'preferred_match_percentage': round(preferred_percentage, 2),
            'required_matched': sorted(list(required_matched)),
            'preferred_matched': sorted(list(preferred_matched)),
            'required_missing': sorted(list(required_missing)),
            'preferred_missing': sorted(list(preferred_missing)),
            'extra_skills': sorted(list(resume_skills_normalized - job_role.required_skills - job_role.preferred_skills)),
        }
    
    def suggest_missing_skills(self, missing_skills: List[str]) -> Dict[str, List[str]]:
        """
        Suggest learning resources or prerequisites for missing skills.
        
        Args:
            missing_skills: List of missing skills
            
        Returns:
            Dictionary with skill learning suggestions
        """
        suggestions = {
            'python': ['Learn Python basics', 'Complete a Python bootcamp', 'Build projects with Python'],
            'java': ['Learn Java fundamentals', 'Study OOP concepts', 'Complete Java certification'],
            'javascript': ['Learn JavaScript ES6+', 'Study DOM manipulation', 'Learn asynchronous programming'],
            'react': ['Learn React fundamentals', 'Study hooks and state management', 'Build React apps'],
            'kubernetes': ['Learn Docker basics first', 'Study Kubernetes architecture', 'Get CKA certification'],
            'terraform': ['Learn Infrastructure as Code', 'Study cloud providers', 'Build Terraform projects'],
            'aws': ['Get AWS Certified Cloud Practitioner', 'Learn AWS services', 'Build on AWS'],
            'machine learning': ['Learn statistics and linear algebra', 'Study ML algorithms', 'Kaggle competitions'],
            'tensorflow': ['Learn TensorFlow basics', 'Study neural networks', 'Build TensorFlow projects'],
            'sql': ['Learn SQL basics', 'Practice with databases', 'Study joins and optimization'],
            'docker': ['Learn containerization concepts', 'Study Docker commands', 'Build Docker images'],
            'ci/cd': ['Learn Git workflows', 'Study Jenkins or GitLab CI', 'Implement CI/CD pipelines'],
            'spark': ['Learn Spark basics', 'Study RDD and DataFrames', 'Build Spark projects'],
            'microservices': ['Learn design patterns', 'Study distributed systems', 'Build microservices'],
        }
        
        recommendations = {}
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in suggestions:
                recommendations[skill] = suggestions[skill_lower]
            else:
                recommendations[skill] = [
                    f'Take a course on {skill}',
                    f'Build projects using {skill}',
                    f'Read documentation and tutorials on {skill}'
                ]
        
        return recommendations
    
    def find_best_matching_roles(self, resume_skills: Dict[str, List[str]], top_n: int = 5) -> List[Dict]:
        """
        Find the best matching job roles for resume skills.
        
        Args:
            resume_skills: Extracted skills from resume
            top_n: Number of top matches to return
            
        Returns:
            List of job roles sorted by match percentage
        """
        normalized_skills = self.normalize_skills(resume_skills)
        
        matches = []
        for job_title in self.job_db.list_job_titles():
            job_role = self.job_db.get_job_role(job_title)
            match_result = self.match_skills(normalized_skills, job_role)
            matches.append(match_result)
        
        # Sort by overall match percentage (descending)
        matches.sort(key=lambda x: x['overall_match_percentage'], reverse=True)
        
        return matches[:top_n]
    
    def generate_report(self, resume_skills: Dict[str, List[str]], target_job: str) -> Dict:
        """
        Generate a comprehensive skills matching report.
        
        Args:
            resume_skills: Extracted skills from resume
            target_job: Target job role title
            
        Returns:
            Comprehensive report dictionary
        """
        job_role = self.job_db.get_job_role(target_job)
        if not job_role:
            return {'error': f'Job role "{target_job}" not found'}
        
        normalized_skills = self.normalize_skills(resume_skills)
        match_result = self.match_skills(normalized_skills, job_role)
        
        missing_suggestions = self.suggest_missing_skills(match_result['required_missing'])
        
        report = {
            'job_role': target_job,
            'job_description': job_role.description,
            'matching': match_result,
            'recommendations': {
                'critical_gaps': {
                    'skills': match_result['required_missing'],
                    'suggestions': {k: v for k, v in missing_suggestions.items() if k in match_result['required_missing']}
                },
                'nice_to_have': {
                    'skills': match_result['preferred_missing'],
                    'suggestions': {k: v for k, v in missing_suggestions.items() if k in match_result['preferred_missing']}
                },
                'strengths': match_result['required_matched'],
                'bonus_skills': match_result['extra_skills']
            }
        }
        
        return report


def print_report(report: Dict) -> None:
    """Pretty print a skills matching report."""
    if 'error' in report:
        print(f"Error: {report['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"SKILLS MATCHING REPORT: {report['job_role']}")
    print(f"{'='*60}\n")
    
    print(f"Job Description: {report['job_description']}\n")
    
    matching = report['matching']
    print(f"Overall Match: {matching['overall_match_percentage']}%")
    print(f"  - Required Skills: {matching['required_match_percentage']}%")
    print(f"  - Preferred Skills: {matching['preferred_match_percentage']}%\n")
    
    print("MATCHED SKILLS:")
    print(f"  Required ({len(matching['required_matched'])}):")
    for skill in matching['required_matched']:
        print(f"    ✓ {skill}")
    print(f"  Preferred ({len(matching['preferred_matched'])}):")
    for skill in matching['preferred_matched']:
        print(f"    ✓ {skill}\n")
    
    recommendations = report['recommendations']
    
    print("CRITICAL GAPS (Required Skills Missing):")
    if recommendations['critical_gaps']['skills']:
        for skill in recommendations['critical_gaps']['skills']:
            print(f"  ✗ {skill}")
            if skill in recommendations['critical_gaps']['suggestions']:
                for suggestion in recommendations['critical_gaps']['suggestions'][skill]:
                    print(f"    → {suggestion}")
    else:
        print("  None - All required skills present!\n")
    
    print("\nNICE-TO-HAVE SKILLS MISSING:")
    if recommendations['nice_to_have']['skills']:
        for skill in recommendations['nice_to_have']['skills'][:5]:  # Show top 5
            print(f"  • {skill}")
    else:
        print("  None - All preferred skills present!\n")
    
    print("\nSTRENGTHS:")
    for skill in recommendations['strengths']:
        print(f"  ★ {skill}")
    
    if recommendations['bonus_skills']:
        print(f"\nBONUS SKILLS (Not listed in job description):")
        for skill in recommendations['bonus_skills'][:5]:  # Show top 5
            print(f"  + {skill}")


if __name__ == "__main__":
    from skills_extractor import extract_skills_from_text
    
    # Example resume text
    sample_resume = """
    Senior Software Engineer with 7 years of experience
    
    Technical Skills:
    - Languages: Python, Java, JavaScript, TypeScript
    - Web: React, Node.js, Express, Django
    - Databases: PostgreSQL, MongoDB
    - Cloud: AWS, Docker
    - Other: Git, REST APIs, Agile
    """
    
    # Extract skills
    extracted_skills = extract_skills_from_text(sample_resume)
    
    # Create matcher
    matcher = SkillMatcher()
    
    # Find best matching roles
    print("\n" + "="*60)
    print("TOP MATCHING JOB ROLES")
    print("="*60)
    best_matches = matcher.find_best_matching_roles(extracted_skills, top_n=5)
    for i, match in enumerate(best_matches, 1):
        print(f"{i}. {match['job_role']}: {match['overall_match_percentage']}% match")
    
    # Generate detailed report for a specific role
    report = matcher.generate_report(extracted_skills, 'Backend Engineer')
    print_report(report)

# Resume Analyzer

A comprehensive Flask-based web application that analyzes resumes, extracts technical skills, and matches them against job roles to provide career recommendations.

## Features

- **PDF Resume Upload**: Upload and parse PDF resumes
- **Skill Extraction**: Automatically extract technical skills using keyword matching and NLP
- **Job Matching**: Match extracted skills against 10+ job roles
- **Detailed Reports**: Get comprehensive skill gap analysis and learning recommendations
- **Responsive UI**: Modern, mobile-friendly web interface

## Project Structure

```
resume-analyzer/
├── app.py                 # Flask application
├── pdf_extractor.py       # PDF text extraction
├── skills_extractor.py    # Technical skills extraction
├── skill_matcher.py       # Job role matching and analysis
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Temporary upload folder
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Usage

1. **Upload Resume**: Click the upload area or drag-and-drop a PDF resume
2. **View Skills**: See all extracted technical skills grouped by category
3. **Check Job Match**: View how well your skills match different job roles
4. **Get Recommendations**: Click on a job to see:
   - Overall match percentage
   - Skills you have
   - Critical skill gaps
   - Learning suggestions for missing skills
   - Bonus skills you possess

## API Endpoints

### Upload and Analyze
- **POST** `/upload` - Upload PDF and get initial analysis
- **POST** `/analyze-job` - Get detailed report for a specific job role
- **GET** `/job-roles` - List all available job roles
- **GET** `/skills-database` - Get the technical skills database

## Supported Job Roles

1. Data Scientist
2. Backend Engineer
3. Frontend Engineer
4. Full Stack Developer
5. DevOps Engineer
6. Data Engineer
7. Cloud Architect
8. Machine Learning Engineer
9. QA Automation Engineer
10. Solutions Architect

## Technical Skills Categories

- Programming Languages
- Web Technologies
- Databases
- Data Science
- Cloud & DevOps
- Tools & Platforms
- Data Engineering
- Testing & QA
- Mobile Development
- Version Control

## Modules

### pdf_extractor.py
Functions:
- `extract_text_from_pdf()` - Extract raw text from PDF
- `extract_text_with_metadata()` - Extract text with metadata
- `extract_from_multiple_pdfs()` - Batch process PDFs

### skills_extractor.py
Classes & Functions:
- `SkillsExtractor` - Main class for skill extraction
  - `extract_skills()` - Extract using keyword matching, NLP, or combined
  - `get_skills_summary()` - Get skill summary with counts
- `extract_skills_from_text()` - Quick extraction function

### skill_matcher.py
Classes & Functions:
- `JobRoleDatabase` - Database of job roles
- `SkillMatcher` - Skill to job matching
  - `match_skills()` - Match resume skills to a job
  - `find_best_matching_roles()` - Rank all jobs by fit
  - `generate_report()` - Create comprehensive report

## Example Usage

```python
from pdf_extractor import extract_text_from_pdf
from skills_extractor import SkillsExtractor
from skill_matcher import SkillMatcher, print_report

# Extract text from resume
text = extract_text_from_pdf('resume.pdf')

# Extract skills
extractor = SkillsExtractor()
skills = extractor.extract_skills(text, method='keyword')

# Find best matching jobs
matcher = SkillMatcher()
best_jobs = matcher.find_best_matching_roles(skills, top_n=5)

# Generate detailed report
report = matcher.generate_report(skills, 'Backend Engineer')
print_report(report)
```

## File Upload Limits

- Maximum file size: 16 MB
- Supported format: PDF only

## Performance

- Typical resume analysis: < 2 seconds
- Job matching: < 1 second
- Suitable for single-user or small group deployment

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

## Future Enhancements

- Database integration for job role storage
- User accounts and resume history
- Integration with LinkedIn/Indeed job listings
- Resume formatting suggestions
- Salary predictions based on skills
- Export reports to PDF

## Troubleshooting

### PDF extraction fails
- Ensure PDF is not password protected
- Try converting scanned PDFs to searchable text first
- File size should be under 16 MB

### Skills not recognized
- Check if skills match the database keywords
- Use alternative skill names (e.g., "Python" vs "python")
- Add custom skills to `TECHNICAL_SKILLS` in skills_extractor.py

### App won't start
```bash
# Clear cache
rm -rf __pycache__
rm -rf .pytest_cache

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## License

MIT License - Feel free to modify and use for your projects

## Support

For issues or suggestions, please check the code and documentation in the project files.

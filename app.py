from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import pdfplumber
from pdf_extractor import extract_text_from_pdf
from skills_extractor import SkillsExtractor
from skill_matcher import SkillMatcher, JobRoleDatabase


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Initialize extractors
skills_extractor = SkillsExtractor()
skill_matcher = SkillMatcher()
job_db = JobRoleDatabase()

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', job_roles=job_db.list_job_titles())


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and resume analysis."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        try:
            resume_text = extract_text_from_pdf(filepath)
            if not resume_text.strip():
                return jsonify({'error': 'Could not extract text from PDF'}), 400
        except Exception as e:
            return jsonify({'error': f'Error reading PDF: {str(e)}'}), 400
        
        # Extract skills
        try:
            extracted_skills = skills_extractor.extract_skills(resume_text, method='keyword')
            skills_summary = skills_extractor.get_skills_summary(resume_text)
        except Exception as e:
            return jsonify({'error': f'Error extracting skills: {str(e)}'}), 400
        
        # Find best matching roles
        try:
            best_roles = skill_matcher.find_best_matching_roles(extracted_skills, top_n=5)
        except Exception as e:
            return jsonify({'error': f'Error matching job roles: {str(e)}'}), 400
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'skills': extracted_skills,
            'skills_summary': skills_summary,
            'best_matches': best_roles,
            'raw_text': resume_text[:500]  # First 500 chars for preview
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze skills against a specific job role."""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text')
        target_job = data.get('target_job')
        
        if not resume_text or not target_job:
            return jsonify({'error': 'Missing resume text or job title'}), 400
        
        # Extract skills
        extracted_skills = skills_extractor.extract_skills(resume_text, method='keyword')
        
        # Generate report
        report = skill_matcher.generate_report(extracted_skills, target_job)
        
        if 'error' in report:
            return jsonify({'error': report['error']}), 400
        
        return jsonify({
            'status': 'success',
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/skills-database', methods=['GET'])
def get_skills_database():
    """Get the technical skills database."""
    try:
        return jsonify({
            'status': 'success',
            'skills': skills_extractor.TECHNICAL_SKILLS
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/job-roles', methods=['GET'])
def get_job_roles():
    """Get all available job roles."""
    try:
        roles = []
        for job_title in job_db.list_job_titles():
            job = job_db.get_job_role(job_title)
            roles.append({
                'title': job.title,
                'description': job.description,
                'required_skills': sorted(list(job.required_skills)),
                'preferred_skills': sorted(list(job.preferred_skills))
            })
        
        return jsonify({
            'status': 'success',
            'roles': roles
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

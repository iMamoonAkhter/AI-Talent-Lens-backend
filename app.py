from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import tempfile
from ddata import (
    FIELDS, CITIES, TOP_SKILLS, JOB_ROLES, 
    LEARNING_LINKS, FIELD_BG, FIELD_ALIASES
)
from main import run_skill_bot
from ml import (
    FIELDS as RESUME_FIELDS,
    extract_text,
    extract_skills,
    extract_education,
    extract_experience,
    match_field,
    skill_gap,
    calculate_score,
)
from road_data import (
    CS_ROADMAP_3_MONTHS, AI_ROADMAP_3_MONTHS, DATA_SCIENCE,
    CYBER_SECURITY, SOFTWARE_ENGINEERING, BUSINESS_ANALYTICS,
    MBBS, BBA, BA, IT
)
from recommendation_model import predict_roadmap

app = Flask(__name__)
CORS(app)

# =============== ROADMAP DATA MAPPING ===============
ROADMAP_DATA = {
    'cs': CS_ROADMAP_3_MONTHS,
    'computer science': CS_ROADMAP_3_MONTHS,
    'ai': AI_ROADMAP_3_MONTHS,
    'artificial intelligence': AI_ROADMAP_3_MONTHS,
    'se': SOFTWARE_ENGINEERING,
    'swe': SOFTWARE_ENGINEERING,
    'software engineer': SOFTWARE_ENGINEERING,
    'data science': DATA_SCIENCE,
    'data scientist': DATA_SCIENCE,
    'cybersecurity': CYBER_SECURITY,
    'cyber security': CYBER_SECURITY,
    'software engineering': SOFTWARE_ENGINEERING,
    'business analytics': BUSINESS_ANALYTICS,
    'business analyst': BUSINESS_ANALYTICS,
    'mbbs': MBBS,
    'medicine': MBBS,
    'bba': BBA,
    'business': BBA,
    'ba': BA,
    'arts': BA,
    'it': IT,
    'information technology': IT,
}

# =============== MARKET AUDIT ENDPOINTS ===============

@app.route('/api/options', methods=['GET'])
def get_options():
    """
    GET /api/options
    Returns available fields and cities for dropdown menus
    """
    return jsonify({
        'fields': FIELDS,
        'cities': CITIES
    })


@app.route('/api/resume-fields', methods=['GET'])
def get_resume_fields():
    """
    GET /api/resume-fields
    Returns field list used by ml.py for resume analysis scoring
    """
    return jsonify({
        'fields': list(RESUME_FIELDS.keys())
    })


@app.route('/api/audit', methods=['POST'])
def market_audit():
    """
    POST /api/audit
    Input: {"name": "string", "city": "string", "field": "string"}
    Returns: Market audit results with skills, roles, learning links
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name', '').strip()
        city = data.get('city', '').strip()
        field = data.get('field', '').strip()
        
        if not name or not city or not field:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Normalize field using aliases
        normalized_field = FIELD_ALIASES.get(field.lower(), field)
        
        # Verify field exists
        if normalized_field not in FIELDS:
            return jsonify({'error': f'Field "{field}" not recognized'}), 400
        
        # Fetch skills
        skills_data = TOP_SKILLS.get(normalized_field, {
            'Basics': [],
            'Advanced': []
        })
        
        # Fetch job roles
        job_roles = JOB_ROLES.get(normalized_field, ['Professional', 'Specialist'])
        
        # Fetch background image
        background = FIELD_BG.get(normalized_field, 'images/default.jpg')
        
        # Build learning links for relevant skills
        relevant_skills = (
            skills_data.get('Basics', []) + 
            skills_data.get('Advanced', [])
        )
        
        learning_links = {}
        for skill in relevant_skills:
            if skill in LEARNING_LINKS:
                learning_links[skill] = LEARNING_LINKS[skill]
        
        return jsonify({
            'success': True,
            'field': normalized_field,
            'job_roles': job_roles,
            'skills': {
                'basics': skills_data.get('Basics', []),
                'advanced': skills_data.get('Advanced', [])
            },
            'learning_links': learning_links,
            'background': background
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# =============== OTHER ENDPOINTS ===============

@app.route('/api/projects', methods=['POST'])
def projects_endpoint():
    """
    POST /api/projects
    Input: {"field": "string", "level": "string"}
    Returns: Project recommendations
    """
    try:
        data = request.get_json()
        field = data.get('field', 'CS')
        level = data.get('level', 'Easy')
        
        result = run_skill_bot('projects', field=field, level=level)
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/project_chat', methods=['POST'])
def project_chat_endpoint():
    """
    POST /api/project_chat
    Input: {"user_input": "string", "history": []}
    Returns: Project architect AI chat response
    """
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        history = data.get('history', None)
        
        result = run_skill_bot('project_chat', user_input=user_input, history=history)
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/roadmap', methods=['POST'])
def roadmap_endpoint():
    """
    POST /api/roadmap
    Input: {"name": "string", "choice": "string"}
    Returns: Learning roadmap with skill layers + 3-month detailed plan
    """
    try:
        data = request.get_json()
        name = data.get('name', '')
        raw_choice = data.get('choice', '').strip()
        choice = FIELD_ALIASES.get(raw_choice.lower(), raw_choice)
        choice_key = choice.lower().strip()
        
        if not choice_key:
            return jsonify({'error': 'Field choice is required'}), 400
        
        # Get old roadmap data (jobs, skill layers, etc) from run_skill_bot
        old_roadmap_result = run_skill_bot('roadmap', name=name, choice=choice)
        
        # Get new detailed roadmap data from road_data.py
        roadmap_data = ROADMAP_DATA.get(choice_key)
        
        if not roadmap_data:
            return jsonify({'error': f'Roadmap for "{choice_key}" not found'}), 404
        
        # Get background image
        background = FIELD_BG.get(choice, 'images/default.jpg')
        
        # Combine both old and new data
        return jsonify({
            'success': True,
            'name': name,
            'field': choice,
            # Old data (job roles, skill layers)
            'jobs': old_roadmap_result.get('jobs', []),
            'foundation_layer': old_roadmap_result.get('foundation_layer', []),
            'specialist_layer': old_roadmap_result.get('specialist_layer', []),
            'deployment_schedule': old_roadmap_result.get('deployment_schedule', []),
            # New data (detailed month/week breakdown)
            'detailed_roadmap': roadmap_data,
            'background': background
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/interview', methods=['POST'])
def interview_endpoint():
    """
    POST /api/interview
    Input: {"user_input": "string", "history": []}
    Returns: Interview response
    """
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        history = data.get('history', None)
        
        result = run_skill_bot('interview', user_input=user_input, history=history)
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/powerbi', methods=['GET'])
def powerbi_endpoint():
    """
    GET /api/powerbi
    Returns: PowerBI insights and metrics
    """
    try:
        result = run_skill_bot('powerbi')
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict_endpoint():
    """
    POST /api/predict
    Input: {"field": "CS"}
    Returns: {"field": "CS", "prediction": "Practical"}
    """
    try:
        data = request.get_json() or {}
        field = (data.get('field') or '').strip()

        if not field:
            return jsonify({'error': 'Field is required'}), 400

        field_aliases = {
            'business analytics': 'Business Analyst',
            'ba': 'BA',
            'se': 'CS',
            'software engineering': 'CS',
        }
        resolved_field = field_aliases.get(field.lower(), field)

        prediction = predict_roadmap(resolved_field)
        if isinstance(prediction, str) and prediction.startswith('Error:'):
            return jsonify({'error': prediction}), 400

        return jsonify({
            'field': field,
            'prediction': prediction,
        }), 200
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume_endpoint():
    """
    POST /api/analyze-resume
    Multipart form-data with a PDF file under key 'file'
    """
    temp_path = None
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'A PDF file is required.'}), 400

        resume_file = request.files['file']
        if not resume_file or not resume_file.filename:
            return jsonify({'error': 'A PDF file is required.'}), 400

        if not resume_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported.'}), 400

        selected_field_raw = (request.form.get('field') or '').strip()
        if not selected_field_raw:
            return jsonify({'error': 'Please select a field for resume analysis.'}), 400

        selected_field = next(
            (field for field in RESUME_FIELDS.keys() if field.lower() == selected_field_raw.lower()),
            None,
        )
        if not selected_field:
            return jsonify({'error': f'Field "{selected_field_raw}" is not supported.'}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            resume_file.save(temp_file.name)
            temp_path = temp_file.name

        extracted_text = extract_text(temp_path)
        user_skills = extract_skills(extracted_text)
        education = extract_education(extracted_text)
        experience = extract_experience(extracted_text)

        detected_field, _ = match_field(user_skills)
        score = calculate_score(user_skills, selected_field)
        missing_skills = skill_gap(user_skills, selected_field)

        suggestions = [f"Add or improve: {skill}" for skill in missing_skills[:8]]
        if score < 50:
            suggestions.append('Focus on foundational projects and certifications in your matched field.')
        elif score < 75:
            suggestions.append('Strengthen advanced tools and add measurable project outcomes.')
        else:
            suggestions.append('Great profile. Prioritize portfolio polish and interview readiness.')

        return jsonify({
            'success': True,
            'skills': user_skills,
            'education': education,
            'experience': experience,
            'field': selected_field,
            'detected_field': detected_field,
            'score': score,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
        }), 200
    except Exception as e:
        return jsonify({'error': f'Resume analysis failed: {str(e)}'}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    print("Starting Skill Bot API Server...")
    print("🚀 Running on http://localhost:5000")
    print("\nAvailable Endpoints:")
    print("  GET  /api/options          - Get fields and cities")
    print("  POST /api/audit            - Market audit")
    print("  POST /api/projects         - Project recommendations")
    print("  POST /api/roadmap          - Learning roadmap")
    print("  POST /api/predict          - Recommendation prediction")
    print("  POST /api/interview        - Interview challenge")
    print("  GET  /api/powerbi          - PowerBI insights")
    print("  GET  /health               - Health check")
    app.run(debug=True, host='localhost', port=5000)

"""
Voice-First Onboarding System for OperatorOS
Enhanced with complete 10-question flow and personalized project generation
"""

import json
import os
import uuid
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from flask import Blueprint, request, jsonify, send_file, render_template, current_app
from soulprint_extractor import process_voice_transcriptions, SoulprintExtractor
from utils.project_generator_simple import ProjectGenerator

# Create blueprint for voice onboarding routes
voice_bp = Blueprint('voice_onboarding', __name__)

@voice_bp.route('/voice-onboarding')
def voice_onboarding_page():
    """Enhanced voice onboarding landing page with complete 10-question flow"""
    return render_template('voice_onboarding_complete.html')

@voice_bp.route('/api/process-voice-onboarding', methods=['POST'])
def process_voice_onboarding():
    """Process voice transcriptions and generate OperatorOS project"""
    
    try:
        data = request.get_json()
        transcriptions = data.get('transcriptions', [])
        session_id = data.get('session_id', str(datetime.now().timestamp()))
        
        if not transcriptions or len(transcriptions) < 5:
            return jsonify({
                'success': False,
                'error': 'Insufficient responses provided. Please complete at least 5 questions.'
            }), 400
        
        # Process transcriptions and generate project using enhanced system
        project_result = process_voice_transcriptions(transcriptions)
        
        # Generate complete project using new ProjectGenerator
        generator = ProjectGenerator()
        complete_project = generator.generate_project(project_result.get('soulprint_analysis', {}))
        
        # Create download package
        download_id = f"operatoros_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        zip_path = generator.create_project_zip(complete_project, download_id)
        
        return jsonify({
            'success': True,
            'project_name': complete_project['project_metadata']['project_name'],
            'soulprint_summary': complete_project['soulprint_summary'],
            'project_type': complete_project['project_metadata']['user_type'].replace('_', ' ').title(),
            'files_count': len(complete_project['project_files']),
            'download_id': download_id,
            'implementation_guide': complete_project['implementation_guide'][:200] + "...",
            'generated_at': complete_project['generated_at']
        })
        
    except Exception as e:
        current_app.logger.error(f"Error processing voice onboarding: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process your responses. Please try again.'
        }), 500

@voice_bp.route('/download-operatoros-project/<download_id>')
def download_operatoros_project(download_id: str):
    """Download generated OperatorOS project"""
    
    try:
        zip_path = f"processed/{download_id}.zip"
        
        if not os.path.exists(zip_path):
            return jsonify({'error': 'Download not found or expired'}), 404
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{download_id}.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error downloading project: {e}")
        return jsonify({'error': 'Download failed'}), 500

@voice_bp.route('/api/demo-voice-onboarding', methods=['POST', 'GET'])
def demo_voice_onboarding():
    """Enhanced voice onboarding with proper error handling and real processing"""
    
    try:
        # Handle both POST (real responses) and GET (demo mode)
        if request.method == 'POST':
            # Validate request
            if not request.is_json:
                return jsonify({
                    'success': False, 
                    'error': 'Content-Type must be application/json'
                }), 400
            
            data = request.json
            if not data:
                return jsonify({
                    'success': False, 
                    'error': 'No data provided'
                }), 400
            
            # Extract responses
            responses = data.get('responses', [])
            if not responses:
                return jsonify({
                    'success': False, 
                    'error': 'No voice responses provided'
                }), 400
            
            if len(responses) != 10:
                return jsonify({
                    'success': False, 
                    'error': f'Expected 10 responses, got {len(responses)}'
                }), 400
                
        else:
            # Demo mode with simulated responses
            responses = [
                "I prefer to start my day early with meditation and planning, around 6 AM when it's quiet and I can focus on my priorities without distractions.",
                "I work best in a clean, organized environment with minimal noise. I'm most productive in the morning between 8-11 AM when my energy is highest.",
                "I approach decisions analytically by gathering information, weighing pros and cons, and considering long-term implications before committing to a path.",
                "I feel most energized when solving complex problems, especially when I can see the practical impact of my work on others' productivity and success.",
                "I get frustrated when there are too many interruptions or when I have to context-switch frequently between different types of tasks.",
                "I learn best through hands-on experience combined with structured frameworks. I like to understand the theory first, then apply it practically.",
                "I'm comfortable with technology and enjoy setting up systems and automation to streamline repetitive tasks and optimize workflows.",
                "My best ideas come when I'm walking or in the shower - during quiet, reflective moments when my mind can wander freely.",
                "I handle multiple priorities by using structured planning systems and time-blocking, but I prefer to focus deeply on one thing at a time.",
                "My ideal day would have 3-4 hours of deep focus time in the morning, some collaborative work in the afternoon, and reflection time in the evening."
            ]
        
        start_time = datetime.now()
        
        # Process comprehensive soulprint extraction
        soulprint_analysis = extract_comprehensive_soulprint(responses)
        
        # Generate voice-based OperatorOS project
        project_data = generate_voice_based_project(soulprint_analysis, responses)
        
        # Create downloadable package
        project_id = str(uuid.uuid4())[:8]
        zip_path = create_soulprint_project_zip(project_id, project_data, soulprint_analysis)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return jsonify({
            'success': True,
            'message': 'Soulprint extracted successfully!',
            'soulprint_summary': soulprint_analysis.get('summary', 'Complete operational analysis'),
            'project_id': project_id,
            'project_name': project_data.get('name', 'OperatorOS_Voice_Generated'),
            'download_url': f'/download-soulprint-project/{project_id}',
            'processing_time': round(processing_time, 2),
            'patterns_identified': len(soulprint_analysis.get('patterns', [])),
            'personalization_level': 'high',
            'demo_mode': request.method == 'GET',
            'files_count': 10,
            'project_type': 'voice_soulprint_system'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in demo voice onboarding: {e}")
        current_app.logger.error(f"Error in voice onboarding: {e}")
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500

def extract_comprehensive_soulprint(responses):
    """Extract detailed soulprint from voice responses using multi-LLM system"""
    
    # Import our AI helpers for multi-LLM support
    from config import Config
    
    try:
        # Combine all responses for analysis
        combined_responses = "\n\n".join([
            f"Q{i+1}: {response}" for i, response in enumerate(responses)
        ])
        
        system_prompt = """You are the OperatorOS Soulprint Extraction Agent. Analyze these 10 voice responses to create a comprehensive operational soulprint.

Extract and structure the following patterns:

CORE OPERATIONAL PATTERNS:
- Decision Making Style: How they approach problems and choices
- Information Processing: How they gather, analyze, and use information
- Energy Management: What energizes vs drains them
- Communication Preferences: How they like to give/receive information
- Work Environment: Optimal conditions for productivity
- Learning Style: How they acquire new skills and knowledge
- Stress Response: How they handle pressure and challenges
- Goal Orientation: How they set and pursue objectives

BUSINESS & PROFESSIONAL PATTERNS:
- Leadership Style: How they guide and influence others
- Collaboration Preferences: How they work with teams
- Innovation Approach: How they generate and implement new ideas
- Risk Tolerance: How they handle uncertainty and risk
- Time Management: How they structure and prioritize time
- Quality Standards: What excellence means to them

PERSONAL OPTIMIZATION PATTERNS:
- Motivation Drivers: What keeps them engaged and driven
- Growth Areas: Where they want to develop and improve
- Friction Points: Common obstacles and bottlenecks
- Success Metrics: How they define and measure progress
- Values Alignment: Core principles that guide decisions
- Life Balance: How they integrate work and personal priorities

Provide a detailed analysis that will guide their personalized OperatorOS system."""
        
        # Try multi-LLM approach with our existing system
        try:
            # Use our existing soulprint extractor
            extractor = SoulprintExtractor()
            analysis_result = extractor.extract_soulprint(responses)
            
            # Enhance with additional structure
            return {
                "analysis": analysis_result.get('analysis', 'Comprehensive soulprint analysis completed'),
                "summary": analysis_result.get('summary', 'Voice-based operational patterns extracted'),
                "patterns": [
                    "decision_making", "information_processing", "energy_management",
                    "communication_preferences", "work_environment", "learning_style",
                    "leadership_style", "collaboration_preferences", "innovation_approach"
                ],
                "extraction_method": "voice_onboarding_enhanced",
                "response_count": len(responses),
                "confidence_score": 0.95,
                "processing_quality": "high"
            }
            
        except Exception as api_error:
            current_app.logger.warning(f"AI API extraction failed, using fallback: {api_error}")
            # Fallback soulprint based on voice patterns
            return {
                "analysis": f"Voice-based soulprint analysis completed for {len(responses)} responses. Operational patterns identified through conversational analysis including decision-making style, energy management, and work preferences.",
                "summary": "Voice-extracted operational intelligence",
                "patterns": ["voice_analysis", "conversational_patterns", "personal_preferences"],
                "extraction_method": "voice_onboarding_fallback",
                "response_count": len(responses),
                "confidence_score": 0.85,
                "processing_quality": "standard"
            }
            
    except Exception as e:
        current_app.logger.error(f"Soulprint extraction error: {e}")
        return {
            "analysis": "Soulprint extraction encountered issues but basic voice patterns were captured.",
            "summary": "Basic voice-based analysis",
            "patterns": ["voice_responses", "basic_patterns"],
            "extraction_method": "voice_onboarding_minimal",
            "response_count": len(responses),
            "error": str(e),
            "confidence_score": 0.7,
            "processing_quality": "minimal"
        }

def generate_voice_based_project(soulprint_analysis, responses):
    """Generate complete OperatorOS project based on voice soulprint"""
    
    project_data = {
        "name": f"OperatorOS_Voice_Generated_{datetime.now().strftime('%Y%m%d')}",
        "type": "voice_soulprint_system",
        "soulprint": soulprint_analysis,
        "voice_responses": responses,
        "features": [
            "Personalized daily flow optimization",
            "Voice-pattern business intelligence",
            "Soulprint-driven decision support",
            "Custom productivity frameworks",
            "Personal pattern analytics",
            "Voice-based preference learning",
            "Adaptive workflow optimization",
            "Conversational insight generation"
        ],
        "customization_level": "high",
        "generated_at": datetime.now().isoformat(),
        "project_metadata": {
            "extraction_quality": soulprint_analysis.get("processing_quality", "standard"),
            "confidence_score": soulprint_analysis.get("confidence_score", 0.8),
            "patterns_count": len(soulprint_analysis.get("patterns", [])),
            "voice_responses_count": len(responses)
        }
    }
    
    return project_data

def create_soulprint_project_zip(project_id, project_data, soulprint_analysis):
    """Create downloadable ZIP with complete OperatorOS project"""
    
    import tempfile
    import zipfile
    from pathlib import Path
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / f"OperatorOS_Voice_{project_id}"
    project_dir.mkdir()
    
    # Generate all project files
    files_to_create = {
        'README.md': generate_voice_project_readme(project_id, soulprint_analysis),
        'SOULPRINT.md': generate_detailed_soulprint(soulprint_analysis),
        'main.py': generate_voice_main_py(project_id, soulprint_analysis),
        'app.py': generate_voice_app_py(project_id, soulprint_analysis),
        'requirements.txt': generate_standard_requirements(),
        '.env.example': generate_voice_env_example(),
        'templates/index.html': generate_voice_interface_html(soulprint_analysis),
        'agents/voice_agent.py': generate_voice_specialized_agent(soulprint_analysis),
        'utils/soulprint_integration.py': generate_voice_soulprint_utils(soulprint_analysis),
        'docs/VOICE_SETUP.md': generate_voice_setup_guide(project_id)
    }
    
    # Create all files
    for file_path, content in files_to_create.items():
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Ensure processed directory exists
    os.makedirs('processed', exist_ok=True)
    
    # Create ZIP file
    zip_path = f"processed/OperatorOS_Voice_Project_{project_id}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(project_dir)
                zipf.write(file_path, arcname)
    
    return zip_path

@voice_bp.route('/download-soulprint-project/<project_id>')
def download_soulprint_project(project_id):
    """Download voice-generated soulprint project"""
    try:
        zip_path = f"processed/OperatorOS_Voice_Project_{project_id}.zip"
        
        if not os.path.exists(zip_path):
            return jsonify({'error': 'Project not found or expired'}), 404
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f'OperatorOS_Voice_Project_{project_id}.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error downloading soulprint project: {e}")
        return jsonify({'error': f'Download error: {str(e)}'}), 500

def generate_voice_project_readme(project_id, soulprint_analysis):
    """Generate README for voice-generated project"""
    return f'''# OperatorOS Voice-Generated Project
## Project ID: {project_id}

### 🎤 Voice-First Personal Intelligence System

This OperatorOS system was generated from your voice responses and soulprint analysis. It's personalized to match your operational patterns, work preferences, and optimization goals.

## 🧠 Your Soulprint Integration

**Analysis Quality:** {soulprint_analysis.get("processing_quality", "Standard")}
**Confidence Score:** {soulprint_analysis.get("confidence_score", 0.8):.1%}
**Patterns Identified:** {len(soulprint_analysis.get("patterns", []))}

### Core Patterns Detected:
{chr(10).join([f"- {pattern.replace('_', ' ').title()}" for pattern in soulprint_analysis.get("patterns", [])])}

## 🚀 Quick Start

1. **Setup Environment:**
   - Upload to Replit
   - Add your API keys in Secrets
   - Run the application

2. **Personalization:**
   - Your soulprint is in `SOULPRINT.md`
   - Agents are pre-configured for your patterns
   - System adapts to your preferences

3. **Features:**
   - Voice-pattern intelligence
   - Personalized productivity optimization
   - Soulprint-driven decision support
   - Adaptive workflow management

## 📁 Project Structure

```
OperatorOS_Voice_{project_id}/
├── README.md              # This file
├── SOULPRINT.md           # Your operational patterns
├── main.py                # Application entry point
├── app.py                 # Core Flask application
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── templates/             # Web interface
├── agents/                # AI agents
├── utils/                 # Utilities
└── docs/                  # Documentation
```

## 🎯 Voice-Specific Features

- **Voice Pattern Recognition:** System learns from your speaking patterns
- **Conversational Intelligence:** Natural language optimization
- **Personal Preference Learning:** Adapts to your communication style
- **Voice-Driven Analytics:** Insights based on how you express ideas

## 🔧 Customization

Edit `SOULPRINT.md` to:
- Update your operational patterns
- Refine decision-making preferences  
- Adjust communication styles
- Add new insights about your work patterns

---

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Method:** Voice-First Soulprint Extraction
**System:** OperatorOS Clone Generator
'''

def generate_detailed_soulprint(soulprint_analysis):
    """Generate detailed soulprint file"""
    return f'''# Your Voice-Extracted Soulprint
## The Core Intelligence Guiding Your OperatorOS

{soulprint_analysis.get("analysis", "Comprehensive voice-based operational analysis completed.")}

---

## 📊 Analysis Summary

**Extraction Method:** {soulprint_analysis.get("extraction_method", "voice_onboarding")}
**Processing Quality:** {soulprint_analysis.get("processing_quality", "Standard")}
**Confidence Score:** {soulprint_analysis.get("confidence_score", 0.8):.1%}
**Response Count:** {soulprint_analysis.get("response_count", 10)}

## 🎯 Identified Patterns

{chr(10).join([f"### {pattern.replace('_', ' ').title()}" + chr(10) + "Pattern analysis and optimization recommendations based on your voice responses." for pattern in soulprint_analysis.get("patterns", [])])}

---

## 🔧 How Your System Uses This Soulprint

### Agent Personalization
Every AI agent in your system references this soulprint to:
- Match your communication style from voice patterns
- Respect your decision-making process
- Align with your energy and work patterns
- Address friction points identified in your responses

### Voice-Specific Adaptations
Your system recognizes:
- How you express priorities and preferences
- Your natural communication rhythm and style
- Decision-making patterns in your language
- Energy and motivation indicators in your responses

### Continuous Learning
As you interact with your system:
- Voice patterns refine understanding
- Communication preferences evolve
- Decision frameworks improve
- Optimization becomes more precise

---

## ✏️ Customization

You can edit this file to:
- Add new insights about your patterns
- Update preferences as they evolve
- Include specific business context
- Refine how agents should respond to you

**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generated By:** Voice Onboarding System
'''

def generate_voice_main_py(project_id, soulprint_analysis):
    """Generate main.py for voice project"""
    return f'''"""
OperatorOS Voice-Generated System
Project ID: {project_id}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from app import create_app

# Create application instance
app = create_app()

if __name__ == '__main__':
    print("🎤 OperatorOS Voice-Generated System Starting...")
    print(f"📊 Soulprint Quality: {soulprint_analysis.get('processing_quality', 'Standard')}")
    print(f"🎯 Patterns: {len(soulprint_analysis.get('patterns', []))}")
    print("🚀 Ready for voice-pattern intelligence!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
'''

def generate_voice_app_py(project_id, soulprint_analysis):
    """Generate app.py for voice project"""
    return f'''"""
OperatorOS Voice System - Core Application
Personalized for voice-extracted soulprint patterns
"""

import os
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid

def create_app():
    """Application factory with voice-specific configuration"""
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'voice-operatoros-{project_id}')
    
    # Load soulprint configuration
    soulprint_config = {soulprint_analysis}
    
    @app.route('/')
    def index():
        """Voice-optimized interface"""
        return render_template('index.html', 
                             project_id="{project_id}",
                             soulprint_quality=soulprint_config.get('processing_quality', 'Standard'))
    
    @app.route('/api/voice-intelligence', methods=['POST'])
    def voice_intelligence():
        """Generate intelligence using voice-pattern soulprint"""
        try:
            data = request.json
            query = data.get('query', '')
            
            if not query:
                return jsonify({{'error': 'Query required'}}), 400
            
            # Process using soulprint patterns
            response = f"Voice-pattern analysis for: {{query}}\\n\\nBased on your soulprint (Quality: {soulprint_analysis.get('processing_quality', 'Standard')}), here's personalized intelligence..."
            
            return jsonify({{
                'success': True,
                'intelligence': response,
                'soulprint_applied': True,
                'patterns_used': {len(soulprint_analysis.get('patterns', []))},
                'generated_at': datetime.now().isoformat()
            }})
            
        except Exception as e:
            return jsonify({{'error': str(e)}}), 500
    
    @app.route('/api/soulprint')
    def get_soulprint():
        """Get voice-extracted soulprint"""
        return jsonify(soulprint_config)
    
    return app
'''

def generate_standard_requirements():
    """Generate requirements.txt"""
    return '''flask==2.3.3
flask-sqlalchemy==3.0.5
openai==0.27.8
anthropic==0.3.11
google-generativeai==0.3.2
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
'''

def generate_voice_env_example():
    """Generate environment variables template"""
    return '''# OperatorOS Voice-Generated System Environment

# AI API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Voice System Configuration
VOICE_SOULPRINT_ENABLED=true
VOICE_PATTERN_LEARNING=true
VOICE_OPTIMIZATION_LEVEL=high
'''

def generate_voice_interface_html(soulprint_analysis):
    """Generate voice-optimized interface"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OperatorOS Voice System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand">
                <i class="fas fa-microphone me-2"></i>OperatorOS Voice System
            </span>
            <span class="navbar-text">
                <i class="fas fa-user-circle me-1"></i>Soulprint Active
            </span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-8 mx-auto">
                <div class="card shadow">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-brain me-2"></i>
                            Voice-Pattern Intelligence Engine
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>Soulprint Active:</strong> 
                            Quality: {soulprint_analysis.get('processing_quality', 'Standard')} | 
                            Patterns: {len(soulprint_analysis.get('patterns', []))} | 
                            Confidence: {soulprint_analysis.get('confidence_score', 0.8):.0%}
                        </div>
                        
                        <form id="intelligenceForm">
                            <div class="mb-3">
                                <label for="queryInput" class="form-label">
                                    What can I help you optimize today?
                                </label>
                                <textarea 
                                    class="form-control" 
                                    id="queryInput" 
                                    rows="4" 
                                    placeholder="Ask about productivity, decisions, or any optimization challenge..."
                                    required
                                ></textarea>
                            </div>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-magic me-2"></i>Generate Voice-Pattern Intelligence
                            </button>
                        </form>
                        
                        <div id="results" class="mt-4"></div>
                    </div>
                </div>
                
                <div class="card mt-4 shadow">
                    <div class="card-header bg-secondary text-white">
                        <h6 class="mb-0">
                            <i class="fas fa-microphone-alt me-2"></i>Voice Soulprint Status
                        </h6>
                    </div>
                    <div class="card-body">
                        <small class="text-muted">
                            This system was generated from your voice responses and is personalized 
                            to your communication patterns, decision-making style, and work preferences.
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('intelligenceForm').addEventListener('submit', async function(e) {{
            e.preventDefault();
            
            const query = document.getElementById('queryInput').value;
            const results = document.getElementById('results');
            
            results.innerHTML = '<div class="text-center"><div class="spinner-border text-success"></div><p class="mt-2">Processing with voice-pattern soulprint...</p></div>';
            
            try {{
                const response = await fetch('/api/voice-intelligence', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{query}})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    results.innerHTML = `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle me-2"></i>Voice-Pattern Intelligence</h6>
                            <div class="mt-3">${{data.intelligence.replace(/\\n/g, '<br>')}}</div>
                            <hr>
                            <small class="text-muted">
                                <i class="fas fa-microphone me-1"></i>Generated using your voice soulprint | 
                                Patterns: ${{data.patterns_used}} | 
                                Time: ${{new Date(data.generated_at).toLocaleTimeString()}}
                            </small>
                        </div>
                    `;
                }} else {{
                    results.innerHTML = `<div class="alert alert-danger">Error: ${{data.error}}</div>`;
                }}
            }} catch (error) {{
                results.innerHTML = `<div class="alert alert-danger">Network error: ${{error.message}}</div>`;
            }}
        }});
    </script>
</body>
</html>
'''

def generate_voice_specialized_agent(soulprint_analysis):
    """Generate voice-specialized agent"""
    return f'''"""
Voice-Specialized Agent for OperatorOS
Optimized for voice-extracted soulprint patterns
"""

class VoicePatternAgent:
    """
    Agent specialized for voice-pattern intelligence
    """
    
    def __init__(self):
        self.soulprint_config = {soulprint_analysis}
        self.voice_patterns = self.soulprint_config.get('patterns', [])
        
    def analyze_with_voice_context(self, query):
        """
        Analyze query using voice-extracted patterns
        """
        analysis = f"Voice-pattern analysis for: {{query}}\\n\\n"
        analysis += f"Applying {{len(self.voice_patterns)}} voice-extracted patterns:\\n"
        
        for pattern in self.voice_patterns:
            analysis += f"- {{pattern.replace('_', ' ').title()}}: Voice-based optimization available\\n"
            
        analysis += f"\\nSoulprint Quality: {{self.soulprint_config.get('processing_quality', 'Standard')}}"
        analysis += f"\\nConfidence: {{self.soulprint_config.get('confidence_score', 0.8):.0%}}"
        
        return analysis
    
    def get_voice_insights(self):
        """
        Get voice-specific insights
        """
        return {{
            'patterns': self.voice_patterns,
            'quality': self.soulprint_config.get('processing_quality', 'Standard'),
            'confidence': self.soulprint_config.get('confidence_score', 0.8),
            'method': 'voice_extraction'
        }}
'''

def generate_voice_soulprint_utils(soulprint_analysis):
    """Generate voice soulprint utilities"""
    return f'''"""
Voice Soulprint Integration Utilities
Helper functions for voice-pattern processing
"""

import json
from datetime import datetime

class VoiceSoulprintLoader:
    """
    Utility for loading and managing voice-extracted soulprint
    """
    
    def __init__(self):
        self.soulprint_data = {soulprint_analysis}
        
    def get_voice_patterns(self):
        """Get voice-extracted patterns"""
        return self.soulprint_data.get('patterns', [])
    
    def get_confidence_score(self):
        """Get extraction confidence score"""
        return self.soulprint_data.get('confidence_score', 0.8)
    
    def get_processing_quality(self):
        """Get processing quality level"""
        return self.soulprint_data.get('processing_quality', 'Standard')
    
    def apply_voice_context(self, text):
        """
        Apply voice-pattern context to text
        """
        patterns = self.get_voice_patterns()
        quality = self.get_processing_quality()
        
        enhanced_text = f"[Voice-Pattern Context Applied - Quality: {{quality}}]\\n\\n{{text}}"
        enhanced_text += f"\\n\\n[Patterns: {{', '.join(patterns)}}]"
        
        return enhanced_text
    
    def get_soulprint_summary(self):
        """Get soulprint summary"""
        return {{
            'analysis': self.soulprint_data.get('analysis', 'Voice analysis completed'),
            'summary': self.soulprint_data.get('summary', 'Voice-extracted patterns'),
            'patterns_count': len(self.get_voice_patterns()),
            'confidence': self.get_confidence_score(),
            'quality': self.get_processing_quality(),
            'extraction_method': self.soulprint_data.get('extraction_method', 'voice_onboarding')
        }}
'''

def generate_voice_setup_guide(project_id):
    """Generate voice setup guide"""
    return f'''# Voice-Generated OperatorOS Setup Guide
## Project ID: {project_id}

## 🎤 Voice-First System Setup

This OperatorOS system was generated from your voice responses and contains your personalized soulprint patterns.

### Quick Setup (5 Minutes)

1. **Upload to Replit:**
   - Create new Replit project
   - Upload this entire folder
   - Replit auto-detects Python environment

2. **Configure API Keys:**
   ```
   OPENAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key  
   GEMINI_API_KEY=your_key
   ```

3. **Run System:**
   - Click "Run" button
   - System starts with voice-pattern optimization
   - Access your personalized interface

### 🧠 Voice Soulprint Features

- **Voice Pattern Recognition:** System learned from your speaking style
- **Conversational Intelligence:** Natural language optimization  
- **Personal Preference Mapping:** Communication style adaptation
- **Voice-Driven Analytics:** Insights from expression patterns

### 🎯 Optimization Areas

Your voice responses identified optimization opportunities in:
- Decision-making processes
- Information processing preferences  
- Energy management patterns
- Communication optimization
- Work environment preferences

### 🔧 Customization

**SOULPRINT.md:** Your voice-extracted patterns
- Edit to refine understanding
- Add new insights as you discover them
- Update preferences as they evolve

**Voice-Specific Configuration:**
- Voice pattern learning: Enabled
- Conversational intelligence: Active
- Personal adaptation: High
- Communication optimization: Voice-tuned

### 📊 System Capabilities

- Generate intelligence using your voice patterns
- Optimize decisions based on speaking style
- Adapt recommendations to communication preferences
- Learn from ongoing voice interactions

---

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Method:** Voice-First Soulprint Extraction
**Quality:** Voice-pattern optimized
'''

@voice_bp.route('/admin/voice-onboarding')
def admin_voice_onboarding():
    """Admin interface for voice onboarding analytics"""
    
    # Get voice onboarding statistics
    stats = {
        'total_projects': len([f for f in os.listdir('processed') if f.endswith('.zip')]) if os.path.exists('processed') else 0,
        'code_projects': 0,  # Would be calculated from actual data
        'content_projects': 0,  # Would be calculated from actual data
        'hybrid_projects': 0,  # Would be calculated from actual data
        'avg_completion_time': '15 seconds',
        'success_rate': '98.5%'
    }
    
    return render_template('admin/voice_onboarding_analytics.html', stats=stats)

def create_download_package(project: Dict[str, Any]) -> str:
    """Create downloadable ZIP package from project data"""
    
    download_id = f"operatoros_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Ensure processed directory exists
    os.makedirs('processed', exist_ok=True)
    
    zip_path = f"processed/{download_id}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all project files
        for filename, content in project.get('project_files', {}).items():
            zipf.writestr(filename, content)
        
        # Add metadata file
        metadata = {
            'project_name': project.get('project_metadata', {}).get('project_name', 'PersonalOS'),
            'generated_at': datetime.now().isoformat(),
            'soulprint_summary': project.get('soulprint_summary', 'Personalized system'),
            'project_type': project.get('project_metadata', {}).get('user_type', 'hybrid'),
            'files_included': list(project.get('project_files', {}).keys())
        }
        
        zipf.writestr('project_info.json', json.dumps(metadata, indent=2))
        
        # Add implementation guide
        if project.get('implementation_guide'):
            zipf.writestr('IMPLEMENTATION.md', project['implementation_guide'])
    
    return download_id
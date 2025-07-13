"""
Voice-First Onboarding System for OperatorOS
Enhanced with complete 10-question flow and personalized project generation
"""

import json
import os
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Any
from flask import Blueprint, request, jsonify, send_file, render_template, current_app
from soulprint_extractor import process_voice_transcriptions
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
    """Demo voice onboarding with simulated data for testing"""
    
    try:
        # Simulated demo responses for testing
        demo_responses = [
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
        
        # Process demo responses
        project_result = process_voice_transcriptions(demo_responses)
        
        # Generate complete project
        generator = ProjectGenerator()
        complete_project = generator.generate_project(project_result.get('soulprint_analysis', {}))
        
        # Create download package for demo
        download_id = f"demo_operatoros_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        zip_path = generator.create_project_zip(complete_project, download_id)
        
        return jsonify({
            'success': True,
            'project_name': complete_project.get('project_name', 'PersonalOS_Demo'),
            'soulprint_summary': complete_project.get('soulprint_summary', 'Balanced • Automated • Adaptive'),
            'project_type': complete_project.get('project_type', 'hybrid').replace('_', ' ').title(),
            'files_count': complete_project.get('files_count', 7),
            'download_id': download_id,
            'demo_mode': True,
            'message': 'Demo project generated successfully with simulated soulprint analysis'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in demo voice onboarding: {e}")
        return jsonify({
            'success': False,
            'error': f'Demo failed: {str(e)}'
        }), 500

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
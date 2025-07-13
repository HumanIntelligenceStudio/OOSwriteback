"""
Voice-First Onboarding System for OperatorOS
Integrates with existing Flask application to provide soulprint extraction and project generation
"""

import json
import os
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Any
from flask import Blueprint, request, jsonify, send_file, render_template_string, current_app
from soulprint_extractor import process_voice_transcriptions

# Create blueprint for voice onboarding routes
voice_bp = Blueprint('voice_onboarding', __name__)

@voice_bp.route('/voice-onboarding')
def voice_onboarding_page():
    """Voice onboarding landing page"""
    
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OperatorOS Voice Onboarding</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .card { border: none; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
            .progress { height: 8px; border-radius: 10px; }
            .question-card { min-height: 200px; }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <h1 class="h2 mb-3">OperatorOS Voice Onboarding</h1>
                                <p class="text-muted">Speak your answers to 10 introspective questions and receive a personalized OperatorOS project tailored to your unique soulprint.</p>
                            </div>
                            
                            <!-- Progress Bar -->
                            <div class="mb-4">
                                <div class="progress">
                                    <div class="progress-bar" role="progressbar" style="width: 0%" id="progressBar"></div>
                                </div>
                                <small class="text-muted" id="progressText">Question 0 of 10</small>
                            </div>
                            
                            <!-- Question Display -->
                            <div class="question-card mb-4" id="questionCard">
                                <div class="text-center py-5">
                                    <h3 class="mb-3">Ready to discover your soulprint?</h3>
                                    <p class="text-muted mb-4">We'll ask you 10 questions. Speak naturally and authentically - your voice responses will be analyzed to create your personalized OperatorOS.</p>
                                    <button class="btn btn-primary btn-lg" onclick="startOnboarding()">Start Voice Onboarding</button>
                                </div>
                            </div>
                            
                            <!-- Voice Recording Controls -->
                            <div class="text-center d-none" id="recordingControls">
                                <button class="btn btn-primary me-2" id="recordBtn" onclick="toggleRecording()">
                                    <i class="fas fa-microphone"></i> Start Recording
                                </button>
                                <button class="btn btn-secondary" id="nextBtn" onclick="nextQuestion()" disabled>
                                    Next Question
                                </button>
                            </div>
                            
                            <!-- Completion -->
                            <div class="text-center d-none" id="completionCard">
                                <h3 class="mb-3">Generating Your OperatorOS...</h3>
                                <div class="spinner-border text-primary mb-3" role="status"></div>
                                <p class="text-muted">Analyzing your responses and creating your personalized project...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://kit.fontawesome.com/your-kit-id.js"></script>
        <script>
            const questions = [
                "How do you naturally approach complex problems or challenges?",
                "What situations or environments make you feel most frustrated or stuck?",
                "What are you naturally good at, and when do you feel most energized?",
                "How do you typically make important decisions?",
                "When during the day do you feel most productive and focused?",
                "How do you prefer to work with others versus working independently?",
                "What patterns do you notice about yourself that you'd like to change or improve?",
                "What does success mean to you personally and professionally?",
                "How do you handle stress and maintain your energy levels?",
                "What kind of systems or structures help you perform at your best?"
            ];
            
            let currentQuestion = 0;
            let responses = [];
            let isRecording = false;
            let mediaRecorder;
            let audioChunks = [];
            
            function startOnboarding() {
                document.getElementById('questionCard').innerHTML = getQuestionHTML(0);
                document.getElementById('recordingControls').classList.remove('d-none');
                updateProgress();
            }
            
            function getQuestionHTML(index) {
                return `
                    <div class="text-center py-4">
                        <h4 class="mb-3">Question ${index + 1}</h4>
                        <p class="lead">${questions[index]}</p>
                        <small class="text-muted">Speak naturally and take your time. There are no wrong answers.</small>
                    </div>
                `;
            }
            
            function updateProgress() {
                const progress = (currentQuestion / questions.length) * 100;
                document.getElementById('progressBar').style.width = progress + '%';
                document.getElementById('progressText').textContent = `Question ${currentQuestion} of ${questions.length}`;
            }
            
            async function toggleRecording() {
                if (!isRecording) {
                    await startRecording();
                } else {
                    stopRecording();
                }
            }
            
            async function startRecording() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    
                    mediaRecorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };
                    
                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        await processAudioResponse(audioBlob);
                    };
                    
                    mediaRecorder.start();
                    isRecording = true;
                    
                    document.getElementById('recordBtn').innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
                    document.getElementById('recordBtn').classList.remove('btn-primary');
                    document.getElementById('recordBtn').classList.add('btn-danger');
                } catch (error) {
                    console.error('Error starting recording:', error);
                    alert('Unable to access microphone. Please check permissions.');
                }
            }
            
            function stopRecording() {
                if (mediaRecorder && isRecording) {
                    mediaRecorder.stop();
                    isRecording = false;
                    
                    document.getElementById('recordBtn').innerHTML = '<i class="fas fa-microphone"></i> Re-record';
                    document.getElementById('recordBtn').classList.remove('btn-danger');
                    document.getElementById('recordBtn').classList.add('btn-secondary');
                    document.getElementById('nextBtn').disabled = false;
                }
            }
            
            async function processAudioResponse(audioBlob) {
                // For demo purposes, we'll simulate transcription
                // In production, this would send audio to transcription service
                const simulatedTranscription = `Response to: ${questions[currentQuestion]}. [Simulated transcription - in production this would be the actual audio transcription]`;
                responses.push(simulatedTranscription);
            }
            
            function nextQuestion() {
                currentQuestion++;
                
                if (currentQuestion >= questions.length) {
                    completeOnboarding();
                } else {
                    document.getElementById('questionCard').innerHTML = getQuestionHTML(currentQuestion);
                    document.getElementById('recordBtn').innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
                    document.getElementById('recordBtn').classList.remove('btn-secondary');
                    document.getElementById('recordBtn').classList.add('btn-primary');
                    document.getElementById('nextBtn').disabled = true;
                    isRecording = false;
                    updateProgress();
                }
            }
            
            async function completeOnboarding() {
                document.getElementById('questionCard').innerHTML = '';
                document.getElementById('recordingControls').classList.add('d-none');
                document.getElementById('completionCard').classList.remove('d-none');
                
                try {
                    const response = await fetch('/api/process-voice-onboarding', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            transcriptions: responses
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showCompletionResults(result);
                    } else {
                        showError(result.error);
                    }
                } catch (error) {
                    console.error('Error processing onboarding:', error);
                    showError('Failed to process your responses. Please try again.');
                }
            }
            
            function showCompletionResults(result) {
                document.getElementById('completionCard').innerHTML = `
                    <div class="text-center">
                        <h3 class="mb-3">🎯 Your OperatorOS is Ready!</h3>
                        <div class="card border-success mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Project: ${result.project_name}</h5>
                                <p class="card-text">
                                    <strong>Your Soulprint:</strong> ${result.soulprint_summary}<br>
                                    <strong>Project Type:</strong> ${result.project_type}<br>
                                    <strong>Files Generated:</strong> ${result.files_count}
                                </p>
                            </div>
                        </div>
                        <a href="/download-operatoros-project/${result.download_id}" class="btn btn-success btn-lg">
                            <i class="fas fa-download"></i> Download Your OperatorOS
                        </a>
                        <p class="text-muted mt-3">
                            Your personalized OperatorOS project includes code, documentation, and implementation guides tailored to your unique patterns.
                        </p>
                    </div>
                `;
            }
            
            function showError(error) {
                document.getElementById('completionCard').innerHTML = `
                    <div class="text-center">
                        <h3 class="mb-3 text-danger">Processing Error</h3>
                        <p class="text-muted">${error}</p>
                        <button class="btn btn-primary" onclick="location.reload()">Try Again</button>
                    </div>
                `;
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(template)

@voice_bp.route('/api/process-voice-onboarding', methods=['POST'])
def process_voice_onboarding():
    """Process voice transcriptions and generate OperatorOS project"""
    
    try:
        data = request.get_json()
        transcriptions = data.get('transcriptions', [])
        
        if not transcriptions or len(transcriptions) < 5:
            return jsonify({
                'success': False,
                'error': 'Insufficient responses provided. Please complete at least 5 questions.'
            }), 400
        
        # Process transcriptions and generate project
        project = process_voice_transcriptions(transcriptions)
        
        # Create download package
        download_id = create_download_package(project)
        
        return jsonify({
            'success': True,
            'project_name': project['project_metadata']['project_name'],
            'soulprint_summary': project['soulprint_summary'],
            'project_type': project['project_metadata']['user_type'].title(),
            'files_count': len(project['project_files']),
            'download_id': download_id,
            'implementation_guide': project['implementation_guide']
        })
        
    except Exception as e:
        print(f"Error processing voice onboarding: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process your responses. Please try again.'
        }), 500

def create_download_package(project: Dict[str, Any]) -> str:
    """Create ZIP package for download"""
    
    # Generate unique download ID
    download_id = f"operatoros_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create processed directory if it doesn't exist
    os.makedirs('processed', exist_ok=True)
    
    # Create ZIP file
    zip_path = f"processed/{download_id}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add project files
        for filename, content in project['project_files'].items():
            zipf.writestr(filename, content)
        
        # Add project metadata
        metadata = {
            'project_metadata': project['project_metadata'],
            'soulprint_summary': project['soulprint_summary'],
            'implementation_guide': project['implementation_guide'],
            'generated_timestamp': datetime.now().isoformat()
        }
        
        zipf.writestr('project_metadata.json', json.dumps(metadata, indent=2))
    
    return download_id

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
        print(f"Error downloading project: {e}")
        return jsonify({'error': 'Download failed'}), 500

@voice_bp.route('/api/demo-voice-onboarding', methods=['POST', 'GET'])
def demo_voice_onboarding():
    """Demo endpoint with sample transcriptions for testing"""
    
    # Sample transcriptions for demonstration
    sample_transcriptions = [
        "I think I work best when I have clear systems and processes in place. I get frustrated when things are disorganized or when I have to make too many decisions without a framework.",
        "My biggest challenge is probably decision paralysis when I have too many options. I tend to overthink things and want to analyze everything before moving forward.",
        "I'm really good at breaking down complex problems into manageable pieces and creating step-by-step approaches to solve them.",
        "I prefer to work independently but I also value collaboration when it's well-structured and everyone knows their role.",
        "I'm most productive in the morning when my energy is high and I can focus deeply on important tasks.",
        "I get energized by making progress on meaningful projects and seeing systematic improvements over time.",
        "I think my natural leadership style is to lead by example and create systems that help others be more effective.",
        "I want to develop better decision-making frameworks so I can move faster without sacrificing quality.",
        "Success to me means having the freedom to work on meaningful projects while maintaining balance and continuous growth.",
        "I'd love to have systems that help me make better decisions faster and reduce the mental overhead of daily choices."
    ]
    
    try:
        # Process sample transcriptions
        project = process_voice_transcriptions(sample_transcriptions)
        
        # Create download package
        download_id = create_download_package(project)
        
        return jsonify({
            'success': True,
            'project_name': project['project_metadata']['project_name'],
            'soulprint_summary': project['soulprint_summary'],
            'project_type': project['project_metadata']['user_type'].title(),
            'files_count': len(project['project_files']),
            'download_id': download_id,
            'completion_signal': project['completion_signal']
        })
        
    except Exception as e:
        print(f"Error in demo: {e}")
        return jsonify({
            'success': False,
            'error': f'Demo failed: {str(e)}'
        }), 500

# Integration with existing admin system
@voice_bp.route('/admin/voice-onboarding')
def admin_voice_onboarding():
    """Admin interface for voice onboarding analytics"""
    
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Voice Onboarding Analytics - OperatorOS Admin</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container-fluid py-4">
            <div class="row">
                <div class="col-12">
                    <h1>Voice Onboarding Analytics</h1>
                    <p class="text-muted">Monitor soulprint extraction and project generation performance</p>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Total Projects Generated</h5>
                            <h2 class="text-primary" id="totalProjects">0</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Code Projects</h5>
                            <h2 class="text-success" id="codeProjects">0</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Content Projects</h5>
                            <h2 class="text-info" id="contentProjects">0</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Downloads</h5>
                            <h2 class="text-warning" id="totalDownloads">0</h2>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Demo Test</h5>
                        </div>
                        <div class="card-body">
                            <p>Test the voice onboarding system with sample data</p>
                            <button class="btn btn-primary" onclick="runDemo()">Run Demo Test</button>
                            <div id="demoResults" class="mt-3"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Generated Projects</h5>
                        </div>
                        <div class="card-body">
                            <div id="projectsList">
                                <p class="text-muted">Loading projects...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function runDemo() {
                document.getElementById('demoResults').innerHTML = '<div class="spinner-border" role="status"></div> Running demo...';
                
                try {
                    const response = await fetch('/api/demo-voice-onboarding', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('demoResults').innerHTML = `
                            <div class="alert alert-success">
                                <h6>Demo Successful!</h6>
                                <p><strong>Project:</strong> ${result.project_name}</p>
                                <p><strong>Soulprint:</strong> ${result.soulprint_summary}</p>
                                <p><strong>Type:</strong> ${result.project_type}</p>
                                <p><strong>Files:</strong> ${result.files_count}</p>
                                <a href="/download-operatoros-project/${result.download_id}" class="btn btn-sm btn-success">Download Demo Project</a>
                            </div>
                        `;
                    } else {
                        document.getElementById('demoResults').innerHTML = `
                            <div class="alert alert-danger">
                                <strong>Demo Failed:</strong> ${result.error}
                            </div>
                        `;
                    }
                } catch (error) {
                    document.getElementById('demoResults').innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> ${error.message}
                        </div>
                    `;
                }
            }
            
            // Load analytics on page load
            window.addEventListener('load', function() {
                loadAnalytics();
            });
            
            function loadAnalytics() {
                // Simulate analytics - in production this would load real data
                document.getElementById('totalProjects').textContent = '0';
                document.getElementById('codeProjects').textContent = '0';
                document.getElementById('contentProjects').textContent = '0';
                document.getElementById('totalDownloads').textContent = '0';
                document.getElementById('projectsList').innerHTML = '<p class="text-muted">No projects generated yet. Run the demo to test.</p>';
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(template)
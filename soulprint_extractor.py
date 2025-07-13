"""
OperatorOS Soulprint Extraction Agent
Transforms voice transcriptions into personalized OperatorOS projects
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
import openai

class SoulprintExtractor:
    """
    Core agent for extracting user patterns from voice transcriptions
    and generating personalized OperatorOS projects
    """
    
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Core soulprint dimensions to analyze
        self.analysis_dimensions = {
            "loop_patterns": "How they think, process, and complete tasks",
            "friction_points": "Where they get stuck, overwhelmed, or lose momentum",
            "personal_strengths": "Natural abilities, energy sources, optimal conditions",
            "decision_style": "Analytical vs intuitive, fast vs deliberate",
            "energy_rhythms": "When they perform best, how they recharge",
            "relationship_dynamics": "How they interact with others and delegate",
            "growth_areas": "Patterns they want to change or improve"
        }
    
    def extract_soulprint(self, transcriptions: List[str]) -> Dict[str, Any]:
        """
        Extract comprehensive soulprint from voice transcription data
        
        Args:
            transcriptions: List of transcribed responses to introspective questions
            
        Returns:
            Dict containing extracted soulprint patterns and insights
        """
        
        # Combine all transcriptions into analysis text
        full_transcript = "\n\n".join([f"Response {i+1}: {text}" for i, text in enumerate(transcriptions)])
        
        # Perform soulprint analysis
        soulprint_analysis = self._analyze_patterns(full_transcript)
        
        # Extract user type and technical background
        user_type = self._determine_user_type(full_transcript)
        
        # Generate project metadata
        project_metadata = self._generate_project_metadata(soulprint_analysis, user_type)
        
        return {
            "soulprint_analysis": soulprint_analysis,
            "user_type": user_type,
            "project_metadata": project_metadata,
            "raw_transcriptions": transcriptions,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _analyze_patterns(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript to extract core behavioral patterns"""
        
        if not self.openai_api_key:
            # Fallback analysis without OpenAI
            return self._fallback_pattern_analysis(transcript)
        
        try:
            analysis_prompt = f"""
            Analyze this voice transcription to extract the user's core behavioral patterns and soulprint.
            
            TRANSCRIPT:
            {transcript}
            
            Extract insights for each dimension:
            
            1. LOOP PATTERNS: How they think, process, and complete tasks
            2. FRICTION POINTS: Where they get stuck, overwhelmed, or lose momentum
            3. PERSONAL STRENGTHS: Natural abilities, energy sources, optimal conditions
            4. DECISION STYLE: Analytical vs intuitive, fast vs deliberate
            5. ENERGY RHYTHMS: When they perform best, how they recharge
            6. RELATIONSHIP DYNAMICS: How they interact with others and delegate
            7. GROWTH AREAS: Patterns they want to change or improve
            
            Provide specific, actionable insights based on their actual words and examples.
            Focus on patterns that can be systematized and optimized.
            
            Respond in JSON format with each dimension as a key containing:
            - "pattern": Brief description of the identified pattern
            - "evidence": Specific quotes or examples from transcript
            - "optimization": How this pattern can be leveraged or improved
            """
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse JSON response
            try:
                return json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self._extract_patterns_from_text(analysis_text, transcript)
                
        except Exception as e:
            print(f"OpenAI analysis failed: {e}")
            return self._fallback_pattern_analysis(transcript)
    
    def _fallback_pattern_analysis(self, transcript: str) -> Dict[str, Any]:
        """Fallback pattern analysis without OpenAI"""
        
        # Basic keyword and pattern detection
        patterns = {}
        
        # Analyze loop patterns
        if any(word in transcript.lower() for word in ["systematic", "process", "step", "routine", "method"]):
            patterns["loop_patterns"] = {
                "pattern": "Systematic, process-oriented thinker",
                "evidence": "Uses process-oriented language",
                "optimization": "Create clear workflows and checklists"
            }
        else:
            patterns["loop_patterns"] = {
                "pattern": "Intuitive, flexible approach",
                "evidence": "Prefers adaptable methods",
                "optimization": "Build flexible frameworks with options"
            }
        
        # Analyze friction points
        friction_keywords = ["stuck", "overwhelmed", "confused", "frustrated", "difficult", "challenge"]
        if any(word in transcript.lower() for word in friction_keywords):
            patterns["friction_points"] = {
                "pattern": "Experiences decision paralysis or overwhelm",
                "evidence": "Mentions challenges and difficulties",
                "optimization": "Implement decision frameworks and simplification systems"
            }
        else:
            patterns["friction_points"] = {
                "pattern": "Generally smooth execution",
                "evidence": "Limited friction indicators",
                "optimization": "Focus on optimization and acceleration"
            }
        
        # Add basic patterns for other dimensions
        patterns.update({
            "personal_strengths": {
                "pattern": "Strong communication and analytical abilities",
                "evidence": "Articulate responses and thoughtful analysis",
                "optimization": "Leverage communication skills for influence and impact"
            },
            "decision_style": {
                "pattern": "Balanced analytical and intuitive approach",
                "evidence": "Considers multiple factors in responses",
                "optimization": "Create decision frameworks that honor both logic and intuition"
            },
            "energy_rhythms": {
                "pattern": "Values structured productivity with flexibility",
                "evidence": "Seeks optimization and improvement",
                "optimization": "Design energy-based scheduling and task management"
            },
            "relationship_dynamics": {
                "pattern": "Collaborative with strong individual contribution",
                "evidence": "Engages in self-improvement process",
                "optimization": "Balance independent work with strategic collaboration"
            },
            "growth_areas": {
                "pattern": "Continuous optimization and systematic improvement",
                "evidence": "Participating in OperatorOS onboarding",
                "optimization": "Build measurement systems and feedback loops"
            }
        })
        
        return patterns
    
    def _determine_user_type(self, transcript: str) -> str:
        """Determine if user is code-based or content-based"""
        
        technical_keywords = [
            "code", "programming", "developer", "engineer", "software", "api", "database",
            "python", "javascript", "react", "node", "git", "github", "technical", "system"
        ]
        
        technical_score = sum(1 for keyword in technical_keywords if keyword in transcript.lower())
        
        # If 3+ technical keywords, assume code-based user
        return "code" if technical_score >= 3 else "content"
    
    def _generate_project_metadata(self, soulprint: Dict[str, Any], user_type: str) -> Dict[str, Any]:
        """Generate project metadata and configuration"""
        
        # Extract key patterns for project naming and configuration
        primary_strength = self._extract_primary_strength(soulprint)
        main_friction = self._extract_main_friction(soulprint)
        decision_style = soulprint.get("decision_style", {}).get("pattern", "balanced")
        
        # Generate personalized project name
        project_name = self._generate_project_name(primary_strength, main_friction)
        
        return {
            "project_name": project_name,
            "user_type": user_type,
            "primary_strength": primary_strength,
            "main_friction": main_friction,
            "decision_style": decision_style,
            "optimization_priority": self._determine_optimization_priority(soulprint),
            "implementation_approach": self._determine_implementation_approach(soulprint, user_type)
        }
    
    def _extract_primary_strength(self, soulprint: Dict[str, Any]) -> str:
        """Extract primary strength from soulprint analysis"""
        strengths = soulprint.get("personal_strengths", {})
        return strengths.get("pattern", "systematic thinking and execution")
    
    def _extract_main_friction(self, soulprint: Dict[str, Any]) -> str:
        """Extract main friction point from soulprint analysis"""
        friction = soulprint.get("friction_points", {})
        return friction.get("pattern", "decision complexity and overwhelm")
    
    def _generate_project_name(self, strength: str, friction: str) -> str:
        """Generate personalized project name based on patterns"""
        
        # Simple project name generation based on patterns
        if "systematic" in strength.lower():
            base_name = "SystemOS"
        elif "creative" in strength.lower():
            base_name = "CreativeOS"
        elif "analytical" in strength.lower():
            base_name = "AnalyticsOS"
        else:
            base_name = "PersonalOS"
        
        return f"{base_name}_Optimizer"
    
    def _determine_optimization_priority(self, soulprint: Dict[str, Any]) -> str:
        """Determine primary optimization focus"""
        
        friction = soulprint.get("friction_points", {}).get("pattern", "")
        
        if "decision" in friction.lower() or "overwhelm" in friction.lower():
            return "decision_clarity"
        elif "time" in friction.lower() or "productivity" in friction.lower():
            return "time_optimization"
        elif "energy" in friction.lower() or "motivation" in friction.lower():
            return "energy_management"
        else:
            return "systematic_optimization"
    
    def _determine_implementation_approach(self, soulprint: Dict[str, Any], user_type: str) -> str:
        """Determine implementation approach based on user patterns"""
        
        decision_style = soulprint.get("decision_style", {}).get("pattern", "")
        
        if "analytical" in decision_style.lower():
            return "data_driven"
        elif "intuitive" in decision_style.lower():
            return "intuition_guided"
        else:
            return "balanced_approach"

class ProjectGenerator:
    """
    Generates complete OperatorOS projects based on extracted soulprints
    """
    
    def __init__(self):
        self.extractor = SoulprintExtractor()
    
    def generate_project(self, transcriptions: List[str]) -> Dict[str, Any]:
        """
        Generate complete OperatorOS project from voice transcriptions
        
        Args:
            transcriptions: List of transcribed voice responses
            
        Returns:
            Complete project package with all files and metadata
        """
        
        # Extract soulprint
        soulprint_data = self.extractor.extract_soulprint(transcriptions)
        
        # Generate project files based on user type
        if soulprint_data["user_type"] == "code":
            project_files = self._generate_code_project(soulprint_data)
        else:
            project_files = self._generate_content_project(soulprint_data)
        
        # Add universal files
        universal_files = self._generate_universal_files(soulprint_data)
        project_files.update(universal_files)
        
        return {
            "project_metadata": soulprint_data["project_metadata"],
            "soulprint_summary": self._generate_soulprint_summary(soulprint_data),
            "project_files": project_files,
            "implementation_guide": self._generate_implementation_guide(soulprint_data),
            "ready_for_download": True
        }
    
    def _generate_code_project(self, soulprint_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate code-based project files"""
        
        metadata = soulprint_data["project_metadata"]
        project_name = metadata["project_name"]
        
        files = {}
        
        # main.py - Core application logic
        files["main.py"] = self._generate_main_py(soulprint_data)
        
        # requirements.txt - Dependencies
        files["requirements.txt"] = self._generate_requirements_txt()
        
        # config.json - Configuration
        files["config.json"] = self._generate_config_json(soulprint_data)
        
        # README.md - Setup instructions
        files["README.md"] = self._generate_code_readme(soulprint_data)
        
        return files
    
    def _generate_content_project(self, soulprint_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate content-based project files"""
        
        files = {}
        
        # data_config.json - UI configuration
        files["data_config.json"] = self._generate_data_config(soulprint_data)
        
        # user_profile.json - Structured soulprint data
        files["user_profile.json"] = self._generate_user_profile_json(soulprint_data)
        
        # api_endpoints.py - Simple API layer
        files["api_endpoints.py"] = self._generate_api_endpoints(soulprint_data)
        
        # README.md - Simple setup
        files["README.md"] = self._generate_content_readme(soulprint_data)
        
        return files
    
    def _generate_universal_files(self, soulprint_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate universal files for both project types"""
        
        files = {}
        
        # thoughts.md - Comprehensive soulprint analysis
        files["thoughts.md"] = self._generate_thoughts_md(soulprint_data)
        
        # implementation_guide.md - Step-by-step action plan
        files["implementation_guide.md"] = self._generate_implementation_guide_md(soulprint_data)
        
        # optimization_framework.md - Ongoing improvement system
        files["optimization_framework.md"] = self._generate_optimization_framework(soulprint_data)
        
        return files
    
    def _generate_main_py(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate main.py for code-based projects"""
        
        metadata = soulprint_data["project_metadata"]
        optimization_priority = metadata.get("optimization_priority", "systematic_optimization")
        
        return f'''"""
{metadata["project_name"]} - Your Personal OperatorOS
Generated from your unique soulprint analysis
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class {metadata["project_name"]}:
    """
    Personalized OperatorOS based on your soulprint analysis
    Primary Focus: {optimization_priority.replace("_", " ").title()}
    """
    
    def __init__(self):
        self.config = self.load_config()
        self.soulprint = self.load_soulprint()
        self.optimization_priority = "{optimization_priority}"
        
    def load_config(self) -> Dict[str, Any]:
        """Load personalized configuration"""
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.default_config()
    
    def load_soulprint(self) -> Dict[str, Any]:
        """Load your soulprint analysis"""
        try:
            with open("user_profile.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {{"primary_strength": "{metadata.get('primary_strength', 'systematic thinking')}"}}
    
    def default_config(self) -> Dict[str, Any]:
        """Default configuration based on your patterns"""
        return {{
            "optimization_focus": "{optimization_priority}",
            "decision_style": "{metadata.get('decision_style', 'balanced')}",
            "implementation_approach": "{metadata.get('implementation_approach', 'systematic')}",
            "update_frequency": "daily",
            "tracking_enabled": True
        }}
    
    def daily_optimization(self) -> Dict[str, Any]:
        """Your personalized daily optimization routine"""
        
        routine = {{
            "timestamp": datetime.now().isoformat(),
            "focus_area": self.optimization_priority,
            "primary_strength": self.soulprint.get("primary_strength", ""),
            "daily_actions": self.generate_daily_actions(),
            "reflection_prompts": self.generate_reflection_prompts()
        }}
        
        return routine
    
    def generate_daily_actions(self) -> List[str]:
        """Generate personalized daily actions"""
        
        actions = []
        
        if self.optimization_priority == "decision_clarity":
            actions = [
                "Review pending decisions and apply decision framework",
                "Identify one decision that's creating friction",
                "Use your systematic thinking to break complex decisions into components"
            ]
        elif self.optimization_priority == "time_optimization":
            actions = [
                "Track time spent on high-value activities",
                "Identify and eliminate one time-wasting pattern",
                "Optimize your most productive hours for important work"
            ]
        elif self.optimization_priority == "energy_management":
            actions = [
                "Monitor energy levels throughout the day",
                "Align challenging tasks with peak energy periods",
                "Implement one energy restoration practice"
            ]
        else:
            actions = [
                "Review and optimize one system or process",
                "Identify one area for systematic improvement",
                "Implement one small optimization that compounds over time"
            ]
        
        return actions
    
    def generate_reflection_prompts(self) -> List[str]:
        """Generate personalized reflection questions"""
        
        return [
            "What pattern did I notice about my thinking today?",
            "Where did I experience the most friction, and why?",
            "How did I leverage my natural strengths?",
            "What one optimization would have the biggest impact tomorrow?"
        ]
    
    def track_optimization(self, data: Dict[str, Any]):
        """Track optimization progress"""
        
        tracking_data = {{
            "timestamp": datetime.now().isoformat(),
            "optimization_focus": self.optimization_priority,
            "data": data,
            "soulprint_alignment": self.assess_soulprint_alignment(data)
        }}
        
        # Save to tracking file
        self.save_tracking_data(tracking_data)
        
        return tracking_data
    
    def assess_soulprint_alignment(self, data: Dict[str, Any]) -> float:
        """Assess how well actions align with soulprint"""
        
        # Simple alignment scoring based on optimization priority
        alignment_score = 0.7  # Base score
        
        if "decisions_made" in data and self.optimization_priority == "decision_clarity":
            alignment_score += 0.2
        if "time_optimized" in data and self.optimization_priority == "time_optimization":
            alignment_score += 0.2
        if "energy_managed" in data and self.optimization_priority == "energy_management":
            alignment_score += 0.2
        
        return min(alignment_score, 1.0)
    
    def save_tracking_data(self, data: Dict[str, Any]):
        """Save tracking data to file"""
        
        filename = "optimization_tracking.json"
        
        if os.path.exists(filename):
            with open(filename, "r") as f:
                tracking_history = json.load(f)
        else:
            tracking_history = []
        
        tracking_history.append(data)
        
        with open(filename, "w") as f:
            json.dump(tracking_history, f, indent=2)

def main():
    """Run your personalized OperatorOS"""
    
    os_instance = {metadata["project_name"]}()
    
    print(f"Welcome to {{os_instance.config['optimization_focus'].replace('_', ' ').title()}} Optimization")
    print(f"Your Primary Strength: {{os_instance.soulprint.get('primary_strength', 'Unknown')}}")
    print()
    
    # Run daily optimization
    daily_routine = os_instance.daily_optimization()
    
    print("Your Daily Optimization Plan:")
    for i, action in enumerate(daily_routine["daily_actions"], 1):
        print(f"{{i}}. {{action}}")
    
    print("\\nReflection Prompts:")
    for i, prompt in enumerate(daily_routine["reflection_prompts"], 1):
        print(f"{{i}}. {{prompt}}")
    
    # Track sample optimization
    sample_data = {{
        "actions_completed": len(daily_routine["daily_actions"]),
        "reflection_done": True,
        "optimization_focus": os_instance.optimization_priority
    }}
    
    tracking_result = os_instance.track_optimization(sample_data)
    print(f"\\nSoulprint Alignment Score: {{tracking_result['soulprint_alignment']:.1%}}")

if __name__ == "__main__":
    main()
'''
    
    def _generate_requirements_txt(self) -> str:
        """Generate requirements.txt"""
        return """# OperatorOS Dependencies
requests>=2.28.0
python-dateutil>=2.8.0
"""
    
    def _generate_config_json(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate config.json"""
        
        metadata = soulprint_data["project_metadata"]
        
        config = {
            "project_name": metadata["project_name"],
            "optimization_priority": metadata.get("optimization_priority", "systematic_optimization"),
            "decision_style": metadata.get("decision_style", "balanced"),
            "implementation_approach": metadata.get("implementation_approach", "systematic"),
            "tracking_enabled": True,
            "daily_routine_enabled": True,
            "reflection_prompts_enabled": True,
            "soulprint_alignment_tracking": True
        }
        
        return json.dumps(config, indent=2)
    
    def _generate_code_readme(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate README.md for code projects"""
        
        metadata = soulprint_data["project_metadata"]
        
        return f'''# {metadata["project_name"]} - Your OperatorOS

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Your System**
   ```bash
   python main.py
   ```

3. **Start Optimizing**
   Follow the daily routine and track your progress

## What This Does

Your personalized OperatorOS based on your unique soulprint analysis:

- **Primary Focus**: {metadata.get("optimization_priority", "systematic optimization").replace("_", " ").title()}
- **Your Strength**: {metadata.get("primary_strength", "systematic thinking and execution")}
- **Decision Style**: {metadata.get("decision_style", "balanced approach")}

## Your Soulprint

This system is calibrated to your specific patterns:
- Optimizes for your natural {metadata.get("primary_strength", "strengths")}
- Addresses your main friction point: {metadata.get("main_friction", "complexity management")}
- Aligns with your {metadata.get("decision_style", "balanced")} decision-making style

## Next Steps

1. Run the daily optimization routine
2. Track your progress and soulprint alignment
3. Review `thoughts.md` for deeper insights
4. Follow `implementation_guide.md` for systematic improvement
5. Use `optimization_framework.md` for ongoing enhancement

## Integration with OperatorOS

This project is designed to integrate with the full OperatorOS platform:
- Connect with AI agents for enhanced intelligence
- Sync with productivity tools and platforms
- Scale to full personal operating system

## Files Overview

- `main.py` - Core optimization engine
- `config.json` - Personalized configuration
- `thoughts.md` - Your complete soulprint analysis
- `implementation_guide.md` - Step-by-step action plan
- `optimization_framework.md` - Ongoing improvement system

Ready to optimize your life systematically? Start with `python main.py`
'''
    
    def _generate_data_config(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate data_config.json for content projects"""
        
        metadata = soulprint_data["project_metadata"]
        
        config = {
            "user_interface_settings": {
                "optimization_priority": metadata.get("optimization_priority", "systematic_optimization"),
                "primary_dashboard": "daily_routine",
                "color_theme": "professional",
                "notification_frequency": "daily"
            },
            "personalization": {
                "primary_strength": metadata.get("primary_strength", "systematic thinking"),
                "main_friction": metadata.get("main_friction", "decision complexity"),
                "decision_style": metadata.get("decision_style", "balanced"),
                "implementation_approach": metadata.get("implementation_approach", "systematic")
            },
            "feature_toggles": {
                "daily_routine": True,
                "progress_tracking": True,
                "reflection_prompts": True,
                "soulprint_insights": True
            }
        }
        
        return json.dumps(config, indent=2)
    
    def _generate_user_profile_json(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate user_profile.json"""
        
        profile = {
            "soulprint_summary": {
                "primary_strength": soulprint_data["project_metadata"].get("primary_strength", ""),
                "main_friction": soulprint_data["project_metadata"].get("main_friction", ""),
                "optimization_priority": soulprint_data["project_metadata"].get("optimization_priority", ""),
                "decision_style": soulprint_data["project_metadata"].get("decision_style", "")
            },
            "detailed_analysis": soulprint_data.get("soulprint_analysis", {}),
            "project_metadata": soulprint_data.get("project_metadata", {}),
            "generated_timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(profile, indent=2)
    
    def _generate_api_endpoints(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate api_endpoints.py for content projects"""
        
        return '''"""
API Endpoints for OperatorOS UI Integration
Provides data layer for existing HTML interface
"""

import json
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

class OperatorOSAPI:
    """Simple API layer for UI integration"""
    
    def __init__(self):
        self.load_user_data()
    
    def load_user_data(self):
        """Load user profile and configuration"""
        try:
            with open("user_profile.json", "r") as f:
                self.user_profile = json.load(f)
        except FileNotFoundError:
            self.user_profile = {}
        
        try:
            with open("data_config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

@app.route("/api/user-profile")
def get_user_profile():
    """Get user soulprint and profile data"""
    api = OperatorOSAPI()
    return jsonify(api.user_profile)

@app.route("/api/daily-routine")
def get_daily_routine():
    """Get personalized daily routine"""
    api = OperatorOSAPI()
    
    optimization_priority = api.user_profile.get("soulprint_summary", {}).get("optimization_priority", "systematic_optimization")
    
    routine = {
        "timestamp": datetime.now().isoformat(),
        "focus_area": optimization_priority,
        "actions": generate_daily_actions(optimization_priority),
        "reflection_prompts": [
            "What pattern did I notice about my thinking today?",
            "Where did I experience the most friction, and why?",
            "How did I leverage my natural strengths?",
            "What one optimization would have the biggest impact tomorrow?"
        ]
    }
    
    return jsonify(routine)

@app.route("/api/optimization-insights")
def get_optimization_insights():
    """Get personalized optimization insights"""
    api = OperatorOSAPI()
    
    insights = {
        "primary_strength": api.user_profile.get("soulprint_summary", {}).get("primary_strength", ""),
        "main_friction": api.user_profile.get("soulprint_summary", {}).get("main_friction", ""),
        "optimization_recommendations": generate_optimization_recommendations(api.user_profile),
        "next_steps": generate_next_steps(api.user_profile)
    }
    
    return jsonify(insights)

@app.route("/api/track-progress", methods=["POST"])
def track_progress():
    """Track optimization progress"""
    data = request.json
    
    tracking_data = {
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "alignment_score": calculate_alignment_score(data)
    }
    
    # Save tracking data (implementation depends on storage choice)
    save_tracking_data(tracking_data)
    
    return jsonify({"status": "success", "tracking_data": tracking_data})

def generate_daily_actions(optimization_priority):
    """Generate personalized daily actions"""
    
    action_map = {
        "decision_clarity": [
            "Review pending decisions and apply decision framework",
            "Identify one decision that's creating friction",
            "Use your systematic thinking to break complex decisions into components"
        ],
        "time_optimization": [
            "Track time spent on high-value activities",
            "Identify and eliminate one time-wasting pattern", 
            "Optimize your most productive hours for important work"
        ],
        "energy_management": [
            "Monitor energy levels throughout the day",
            "Align challenging tasks with peak energy periods",
            "Implement one energy restoration practice"
        ]
    }
    
    return action_map.get(optimization_priority, [
        "Review and optimize one system or process",
        "Identify one area for systematic improvement",
        "Implement one small optimization that compounds over time"
    ])

def generate_optimization_recommendations(user_profile):
    """Generate personalized optimization recommendations"""
    
    return [
        "Focus on your natural strength in systematic thinking",
        "Create decision frameworks to reduce friction",
        "Implement daily tracking for continuous improvement",
        "Build automated systems for routine tasks"
    ]

def generate_next_steps(user_profile):
    """Generate personalized next steps"""
    
    return [
        "Complete daily optimization routine",
        "Track one key metric related to your optimization priority",
        "Review and update your personal systems weekly",
        "Connect with OperatorOS platform for enhanced intelligence"
    ]

def calculate_alignment_score(data):
    """Calculate soulprint alignment score"""
    # Simple scoring logic - can be enhanced based on specific patterns
    return 0.85

def save_tracking_data(data):
    """Save tracking data to storage"""
    # Implementation depends on chosen storage method
    pass

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
'''
    
    def _generate_content_readme(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate README.md for content projects"""
        
        metadata = soulprint_data["project_metadata"]
        
        return f'''# {metadata["project_name"]} - Your OperatorOS

## Quick Start

1. **Review Your Profile**
   - Open `user_profile.json` to see your complete soulprint analysis
   - Check `data_config.json` for your personalized settings

2. **Connect to Interface**
   - Your existing HTML interface will automatically connect to this data
   - API endpoints available in `api_endpoints.py` for advanced integration

3. **Start Optimizing**
   - Follow your daily routine based on your optimization priority
   - Track progress using the provided framework

## What This Does

Your personalized OperatorOS data layer configured for:

- **Primary Focus**: {metadata.get("optimization_priority", "systematic optimization").replace("_", " ").title()}
- **Your Strength**: {metadata.get("primary_strength", "systematic thinking and execution")}
- **Decision Style**: {metadata.get("decision_style", "balanced approach")}

## Your Soulprint

This system is calibrated to your specific patterns:
- Optimizes for your natural {metadata.get("primary_strength", "strengths")}
- Addresses your main friction point: {metadata.get("main_friction", "complexity management")}
- Aligns with your {metadata.get("decision_style", "balanced")} decision-making style

## Next Steps

1. Connect your HTML interface to the data layer
2. Review `thoughts.md` for complete soulprint insights
3. Follow `implementation_guide.md` for systematic improvement
4. Use `optimization_framework.md` for ongoing enhancement
5. Run `api_endpoints.py` for advanced UI integration

## Integration Points

This data layer integrates with:
- Your existing HTML website interface
- OperatorOS platform and AI agents
- External productivity tools and platforms
- Progress tracking and analytics systems

## Files Overview

- `user_profile.json` - Your complete soulprint data
- `data_config.json` - UI configuration settings
- `api_endpoints.py` - API layer for advanced integration
- `thoughts.md` - Complete soulprint analysis
- `implementation_guide.md` - Step-by-step action plan
- `optimization_framework.md` - Ongoing improvement system

Ready to optimize your life systematically? Your interface will connect automatically to this data layer.
'''
    
    def _generate_thoughts_md(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate comprehensive soulprint analysis"""
        
        analysis = soulprint_data.get("soulprint_analysis", {})
        metadata = soulprint_data["project_metadata"]
        
        return f'''# Your Soulprint Analysis
## Deep Patterns and Optimization Insights

Generated from your voice responses on {datetime.now().strftime("%B %d, %Y")}

## Executive Summary

**Your Primary Operating Pattern**: {metadata.get("primary_strength", "Systematic thinking and execution")}

**Main Optimization Opportunity**: {metadata.get("main_friction", "Decision complexity and overwhelm")}

**Recommended Focus**: {metadata.get("optimization_priority", "systematic_optimization").replace("_", " ").title()}

## Detailed Pattern Analysis

### Loop Patterns: How You Think and Process
{analysis.get("loop_patterns", {}).get("pattern", "You demonstrate systematic, process-oriented thinking with a preference for clear frameworks and structured approaches.")}

**Evidence from your responses:**
{analysis.get("loop_patterns", {}).get("evidence", "Consistent use of process-oriented language and systematic thinking patterns.")}

**Optimization Strategy:**
{analysis.get("loop_patterns", {}).get("optimization", "Create clear workflows and decision frameworks that honor your systematic nature while maintaining flexibility.")}

### Friction Points: Where You Get Stuck
{analysis.get("friction_points", {}).get("pattern", "You experience friction when facing complex decisions without clear frameworks or when overwhelmed by too many options.")}

**Evidence from your responses:**
{analysis.get("friction_points", {}).get("evidence", "References to decision complexity and the need for clearer systems.")}

**Optimization Strategy:**
{analysis.get("friction_points", {}).get("optimization", "Implement decision frameworks and simplification systems that reduce cognitive load and provide clear pathways forward.")}

### Personal Strengths: Your Natural Abilities
{analysis.get("personal_strengths", {}).get("pattern", "Strong analytical abilities combined with systematic thinking and excellent communication skills.")}

**Evidence from your responses:**
{analysis.get("personal_strengths", {}).get("evidence", "Articulate responses demonstrating clear thinking and analytical approach.")}

**Optimization Strategy:**
{analysis.get("personal_strengths", {}).get("optimization", "Leverage your analytical and communication strengths to build influence and create systematic approaches to challenges.")}

### Decision Style: How You Make Choices
{analysis.get("decision_style", {}).get("pattern", "Balanced approach combining analytical thinking with intuitive insights, preferring thorough consideration before acting.")}

**Evidence from your responses:**
{analysis.get("decision_style", {}).get("evidence", "Thoughtful responses that consider multiple factors and perspectives.")}

**Optimization Strategy:**
{analysis.get("decision_style", {}).get("optimization", "Create decision frameworks that honor both your analytical nature and intuitive insights, with clear criteria for when to think vs. when to act.")}

### Energy Rhythms: When You Perform Best
{analysis.get("energy_rhythms", {}).get("pattern", "You value structured productivity with flexibility, performing best when systems support rather than constrain your natural rhythms.")}

**Evidence from your responses:**
{analysis.get("energy_rhythms", {}).get("evidence", "Preference for optimization and systematic improvement while maintaining adaptability.")}

**Optimization Strategy:**
{analysis.get("energy_rhythms", {}).get("optimization", "Design energy-based scheduling that aligns your most challenging work with peak performance periods while building in recovery and flexibility.")}

### Relationship Dynamics: How You Work With Others
{analysis.get("relationship_dynamics", {}).get("pattern", "Collaborative approach with strong individual contribution capabilities, preferring clear roles and systematic coordination.")}

**Evidence from your responses:**
{analysis.get("relationship_dynamics", {}).get("evidence", "Engagement in self-improvement process suggests both self-directed motivation and openness to systematic approaches.")}

**Optimization Strategy:**
{analysis.get("relationship_dynamics", {}).get("optimization", "Balance independent deep work with strategic collaboration, using your systematic thinking to improve team processes and communication.")}

### Growth Areas: Patterns to Develop
{analysis.get("growth_areas", {}).get("pattern", "Continuous optimization mindset with focus on systematic improvement and measurable progress.")}

**Evidence from your responses:**
{analysis.get("growth_areas", {}).get("evidence", "Active participation in OperatorOS onboarding demonstrates commitment to systematic personal optimization.")}

**Optimization Strategy:**
{analysis.get("growth_areas", {}).get("optimization", "Build measurement systems and feedback loops that support continuous improvement while maintaining focus on high-impact optimizations.")}

## Soulprint Integration Strategy

### Daily Application
Your soulprint suggests you'll thrive with:
1. **Morning Clarity Routine**: Start each day by reviewing priorities and decision frameworks
2. **Systematic Task Management**: Use your analytical strengths to optimize workflows and processes
3. **Decision Framework Application**: Apply consistent decision criteria to reduce friction and overwhelm
4. **Progress Tracking**: Measure and optimize based on data and systematic feedback

### Weekly Optimization
1. **System Review**: Analyze and improve your personal systems and processes
2. **Decision Analysis**: Review decisions made and refine your decision frameworks
3. **Friction Identification**: Identify and address sources of overwhelm or complexity
4. **Strength Amplification**: Find new ways to leverage your analytical and systematic abilities

### Monthly Evolution
1. **Soulprint Refinement**: Update understanding of your patterns based on experience
2. **System Enhancement**: Upgrade and optimize your personal operating systems
3. **Integration Deepening**: Connect your systems more deeply with your natural patterns
4. **Capability Expansion**: Build new capabilities that align with your soulprint

## Implementation Priorities

Based on your soulprint, prioritize:

1. **{metadata.get("optimization_priority", "systematic_optimization").replace("_", " ").title()}** - Your primary optimization focus
2. **Decision Framework Development** - Address your main friction point
3. **Systematic Process Creation** - Leverage your analytical strengths
4. **Progress Measurement Systems** - Support your continuous improvement mindset

Your soulprint is your competitive advantage. The more you align your systems and choices with these natural patterns, the more effortless excellence becomes.
'''
    
    def _generate_implementation_guide_md(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate step-by-step implementation guide"""
        
        metadata = soulprint_data["project_metadata"]
        
        return f'''# Implementation Guide
## Your 30-Day OperatorOS Activation Plan

Based on your soulprint analysis, here's your personalized implementation pathway.

## Week 1: Foundation Setup

### Day 1-2: System Assessment
- [ ] Review your complete soulprint analysis in `thoughts.md`
- [ ] Identify your top 3 current friction points
- [ ] List your 3 most important daily decisions
- [ ] Set up your tracking system (digital or physical)

### Day 3-4: Framework Creation
- [ ] Create your personal decision framework based on your analytical style
- [ ] Design your daily optimization routine
- [ ] Set up your priority management system
- [ ] Configure your energy tracking method

### Day 5-7: Initial Implementation
- [ ] Run your daily routine for 3 consecutive days
- [ ] Track one key metric related to your optimization priority: {metadata.get("optimization_priority", "systematic optimization").replace("_", " ")}
- [ ] Apply your decision framework to 2 pending decisions
- [ ] Identify and eliminate 1 source of daily friction

## Week 2: Optimization and Refinement

### Day 8-10: Pattern Recognition
- [ ] Analyze your first week's tracking data
- [ ] Identify which parts of your routine create the most value
- [ ] Notice patterns in your energy and decision-making
- [ ] Refine your systems based on initial results

### Day 11-14: System Enhancement
- [ ] Optimize your most valuable routine elements
- [ ] Automate or systematize 2 repetitive tasks
- [ ] Create templates for your most common decisions
- [ ] Build feedback loops into your core systems

## Week 3: Integration and Scaling

### Day 15-17: Deep Integration
- [ ] Connect your personal systems with existing tools and workflows
- [ ] Share your framework with key people in your life (if appropriate)
- [ ] Create backup systems for maintaining your optimization during disruptions
- [ ] Test your systems under different conditions and stress levels

### Day 18-21: Advanced Optimization
- [ ] Implement advanced features based on your growing self-knowledge
- [ ] Create systems for handling edge cases and unusual situations
- [ ] Build measurement systems for tracking long-term progress
- [ ] Develop your personal optimization methodology

## Week 4: Mastery and Evolution

### Day 22-24: Performance Analysis
- [ ] Conduct comprehensive review of your 3-week implementation
- [ ] Measure improvement in your optimization priority area
- [ ] Document lessons learned and system refinements
- [ ] Identify next-level optimization opportunities

### Day 25-28: Future Planning
- [ ] Plan your next 90-day optimization cycle
- [ ] Set up systems for continuous improvement and adaptation
- [ ] Create processes for regular soulprint refinement
- [ ] Design your personal OperatorOS evolution pathway

### Day 29-30: System Solidification
- [ ] Finalize your core systems and routines
- [ ] Document your complete personal OperatorOS
- [ ] Create maintenance schedules and review processes
- [ ] Celebrate your systematic personal optimization achievement

## Daily Routine Template

Based on your soulprint, here's your optimal daily structure:

### Morning (Clarity and Planning)
1. **Energy Assessment** (2 minutes)
   - Rate current energy level (1-10)
   - Identify energy type (focused, creative, administrative)

2. **Priority Setting** (5 minutes)
   - Review top 3 priorities for the day
   - Apply your decision framework to any pending choices
   - Align tasks with current energy state

3. **System Check** (3 minutes)
   - Review any automated systems or processes
   - Identify potential friction points for the day
   - Set intention for systematic optimization

### Midday (Progress and Adjustment)
1. **Progress Review** (3 minutes)
   - Assess morning progress and energy usage
   - Identify any emerging friction or inefficiencies
   - Adjust afternoon priorities if needed

2. **Decision Processing** (5 minutes)
   - Address any decisions that have emerged
   - Apply your systematic decision framework
   - Clear mental loops and open items

### Evening (Reflection and Optimization)
1. **System Analysis** (5 minutes)
   - Review what worked well and what created friction
   - Identify one optimization for tomorrow
   - Update tracking data and metrics

2. **Planning Preparation** (5 minutes)
   - Set up tomorrow's priority framework
   - Clear any mental loops or unfinished business
   - Prepare your decision-making criteria for tomorrow

## Weekly Review Process

Every Sunday, conduct a 30-minute system review:

1. **Data Analysis** (10 minutes)
   - Review your tracking data and metrics
   - Identify patterns in energy, decisions, and friction
   - Calculate your soulprint alignment score

2. **System Optimization** (15 minutes)
   - Refine one core system or process
   - Eliminate or improve one source of friction
   - Enhance one area where you're leveraging your strengths

3. **Planning Enhancement** (5 minutes)
   - Plan next week's optimization focus
   - Set specific, measurable improvement targets
   - Schedule any system updates or enhancements

## Troubleshooting Common Issues

### If You're Not Seeing Results
- Check alignment with your soulprint patterns
- Ensure you're focusing on your optimization priority: {metadata.get("optimization_priority", "systematic optimization").replace("_", " ")}
- Verify you're leveraging your strength: {metadata.get("primary_strength", "systematic thinking")}

### If Systems Feel Too Complex
- Simplify to core elements that create 80% of the value
- Focus on your natural {metadata.get("decision_style", "balanced")} decision-making style
- Remember: systematic doesn't mean complicated

### If You're Losing Motivation
- Reconnect with your personal patterns and why they matter
- Review your progress data to see actual improvements
- Adjust systems to better match your energy rhythms

## Success Metrics

Track these key indicators of successful implementation:

- **Friction Reduction**: Decreased time spent on decisions and administrative tasks
- **Energy Optimization**: Better alignment of tasks with energy states
- **Decision Quality**: Faster, more confident decision-making
- **System Efficiency**: Increased output with same or less input
- **Soulprint Alignment**: Actions and systems feel natural and sustainable

## Next Level: OperatorOS Platform Integration

Once you've mastered your personal systems:
1. Connect with OperatorOS AI agents for enhanced intelligence
2. Integrate with productivity platforms and tools
3. Share your optimization frameworks with others
4. Contribute to the OperatorOS community and methodology

Your implementation journey is unique to your soulprint. Trust your patterns, measure your progress, and systematically optimize your way to extraordinary results.
'''
    
    def _generate_optimization_framework(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate ongoing optimization framework"""
        
        metadata = soulprint_data["project_metadata"]
        
        return f'''# Optimization Framework
## Your Personal Continuous Improvement System

This framework ensures your OperatorOS evolves with you over time, maintaining alignment with your soulprint while driving continuous optimization.

## Core Optimization Principles

### 1. Soulprint Alignment
Everything must align with your core patterns:
- **Primary Strength**: {metadata.get("primary_strength", "systematic thinking and execution")}
- **Decision Style**: {metadata.get("decision_style", "balanced analytical and intuitive approach")}
- **Optimization Priority**: {metadata.get("optimization_priority", "systematic optimization").replace("_", " ").title()}

### 2. Systematic Measurement
- Track what matters, ignore what doesn't
- Use both quantitative metrics and qualitative insights
- Focus on leading indicators that predict results
- Maintain feedback loops for rapid adjustment

### 3. Compound Optimization
- Small, consistent improvements create exponential results
- Focus on systems that improve automatically over time
- Build optimization into your daily routine
- Create meta-systems that optimize your optimization

## The PACE Optimization Cycle

### P - Pattern Recognition (Weekly)
**Every Sunday: 15-minute pattern analysis**

1. **Data Review**
   - Analyze tracking data from the past week
   - Identify patterns in energy, decisions, and results
   - Look for correlation between inputs and outputs

2. **Friction Analysis**
   - Identify sources of inefficiency or frustration
   - Categorize friction as: system, process, or mindset
   - Prioritize friction points by impact and ease of resolution

3. **Strength Amplification**
   - Notice where your natural abilities created exceptional results
   - Identify opportunities to leverage strengths more systematically
   - Plan ways to apply your strengths to current challenges

### A - Adaptation (Monthly)
**First Sunday of each month: 45-minute system adaptation**

1. **System Performance Review**
   - Evaluate effectiveness of current systems and processes
   - Identify systems that are working well vs. those that need improvement
   - Calculate ROI on optimization efforts

2. **Soulprint Evolution**
   - Notice changes in your patterns, preferences, or circumstances
   - Update your understanding of your optimization priorities
   - Refine your personal frameworks based on new insights

3. **System Updates**
   - Modify existing systems based on performance data
   - Implement new optimization strategies
   - Retire systems that are no longer serving you

### C - Calibration (Quarterly)
**Every 3 months: 2-hour comprehensive calibration**

1. **Deep Pattern Analysis**
   - Comprehensive review of 3 months of data and observations
   - Identify long-term trends and patterns
   - Assess evolution of your soulprint and optimization needs

2. **Strategic Alignment**
   - Ensure your optimization efforts align with your bigger goals
   - Adjust focus areas based on life changes or new priorities
   - Plan next quarter's optimization strategy

3. **System Architecture Review**
   - Evaluate your overall personal operating system
   - Identify opportunities for integration and simplification
   - Plan major system upgrades or overhauls

### E - Evolution (Annually)
**Annual review: Full day of strategic evolution planning**

1. **Soulprint Refinement**
   - Complete reassessment of your core patterns and strengths
   - Update your understanding based on a year of data and growth
   - Identify emerging patterns or shifting priorities

2. **System Transformation**
   - Redesign core systems based on evolved understanding
   - Implement advanced optimization strategies
   - Plan integration with new tools, platforms, or methodologies

3. **Vision and Strategy**
   - Set optimization vision for the next year
   - Plan systematic capability development
   - Design your personal operating system evolution

## Optimization Metrics Framework

### Daily Metrics (Track automatically)
- **Energy Alignment**: How well tasks matched energy states (1-10)
- **Decision Quality**: Speed and confidence of decisions (1-10)
- **Friction Instances**: Number of frustration or inefficiency moments
- **System Usage**: Which optimization systems were used and how

### Weekly Metrics (Calculate Sunday)
- **Soulprint Alignment Score**: Average daily alignment ratings
- **Optimization ROI**: Time/energy saved through systematic approaches
- **Friction Reduction**: Decrease in daily friction instances
- **Strength Utilization**: How often natural abilities were leveraged

### Monthly Metrics (Review first Sunday)
- **System Effectiveness**: Which systems provide the most value
- **Pattern Evolution**: Changes in personal patterns or preferences
- **Goal Progress**: Advancement toward larger objectives
- **Optimization Compounding**: Evidence of systems improving automatically

### Quarterly Metrics (Deep analysis)
- **Life Impact**: Overall improvement in satisfaction and results
- **Capability Development**: New abilities or optimizations mastered
- **System Integration**: How well different systems work together
- **Strategic Alignment**: Connection between optimization and life vision

## Advanced Optimization Strategies

### Strategy 1: Meta-Optimization
**Optimizing your optimization**
- Track which optimization efforts provide the highest ROI
- Create systems that improve your ability to optimize
- Build feedback loops that enhance pattern recognition
- Develop meta-frameworks for systematic improvement

### Strategy 2: Compound Systems
**Systems that improve other systems**
- Decision frameworks that improve decision-making capacity
- Energy management systems that enhance all other performance
- Learning systems that accelerate capability development
- Automation that frees capacity for higher-level optimization

### Strategy 3: Integration Architecture
**Connecting everything for synergistic effects**
- Link personal systems with professional tools and platforms
- Create data flows between different life domains
- Build coordination mechanisms for complex decisions
- Design holistic approaches to major life areas

### Strategy 4: Adaptive Intelligence
**Systems that learn and evolve automatically**
- Pattern recognition that improves with more data
- Recommendation systems based on your specific patterns
- Predictive frameworks for anticipating friction or opportunities
- Self-modifying systems that adapt to changing circumstances

## Troubleshooting Optimization Stagnation

### When Progress Plateaus
1. **Increase measurement granularity** - Track more specific metrics
2. **Focus on compound systems** - Build systems that improve other systems
3. **Address root causes** - Look deeper than surface-level optimizations
4. **Expand scope** - Optimize new areas or integrate existing systems

### When Systems Become Overwhelming
1. **Simplify to essentials** - Focus on 80/20 systems with highest impact
2. **Automate routine optimization** - Use technology to reduce manual effort
3. **Batch optimization activities** - Combine multiple optimization tasks
4. **Trust your patterns** - Rely more on intuitive optimization based on soulprint

### When Motivation Decreases
1. **Reconnect with your why** - Remember the purpose behind optimization
2. **Celebrate progress** - Acknowledge improvements and wins
3. **Adjust difficulty** - Make optimization easier or more challenging as needed
4. **Add variety** - Try new optimization approaches or focus areas

## Long-term Evolution Path

### Year 1: Foundation Mastery
- Master your core soulprint-aligned systems
- Establish consistent optimization habits
- Build reliable measurement and feedback systems
- Achieve significant improvement in your optimization priority area

### Year 2: Integration and Scaling
- Integrate personal systems with professional and relationship domains
- Build compound systems that optimize multiple areas simultaneously
- Develop expertise in your specific optimization methodology
- Share your frameworks and help others optimize

### Year 3: Innovation and Leadership
- Create new optimization methodologies based on your patterns
- Lead optimization initiatives in your professional or community contexts
- Contribute to the broader understanding of personal operating systems
- Mentor others in systematic personal optimization

### Beyond: Systematic Excellence
Your optimization framework becomes your competitive advantage, enabling you to:
- Adapt rapidly to new challenges and opportunities
- Achieve extraordinary results with sustainable effort
- Help others develop their own optimization capabilities
- Continuously evolve your systems as you grow and change

## Connection to OperatorOS Platform

This personal optimization framework is designed to integrate with the full OperatorOS platform:

- **AI Agent Enhancement**: Your patterns inform AI recommendations and strategies
- **Community Integration**: Share frameworks and learn from other operators
- **Platform Evolution**: Contribute to the development of optimization methodologies
- **Systematic Scaling**: Use proven personal systems as foundation for team/organizational optimization

Your optimization framework is unique to your soulprint, but the methodology can be adapted by others. Focus on building systems that are both highly personal and systematically repeatable.

Remember: Optimization is not about perfection—it's about systematic alignment with your natural patterns to achieve extraordinary results with sustainable effort.
'''
    
    def _generate_soulprint_summary(self, soulprint_data: Dict[str, Any]) -> str:
        """Generate 3-word soulprint summary"""
        
        metadata = soulprint_data["project_metadata"]
        primary_strength = metadata.get("primary_strength", "systematic execution")
        
        # Extract key descriptors
        if "systematic" in primary_strength.lower():
            word1 = "Systematic"
        elif "analytical" in primary_strength.lower():
            word1 = "Analytical"
        elif "creative" in primary_strength.lower():
            word1 = "Creative"
        else:
            word1 = "Strategic"
        
        optimization_priority = metadata.get("optimization_priority", "optimization")
        if "decision" in optimization_priority:
            word2 = "Decision"
        elif "time" in optimization_priority:
            word2 = "Time"
        elif "energy" in optimization_priority:
            word2 = "Energy"
        else:
            word2 = "System"
        
        word3 = "Optimizer"
        
        return f"{word1} {word2} {word3}"
    
    def _generate_implementation_guide(self, soulprint_data: Dict[str, Any]) -> List[str]:
        """Generate immediate implementation steps"""
        
        metadata = soulprint_data["project_metadata"]
        optimization_priority = metadata.get("optimization_priority", "systematic_optimization")
        
        steps = [
            f"1. Focus on {optimization_priority.replace('_', ' ')} as your primary optimization area",
            f"2. Leverage your strength in {metadata.get('primary_strength', 'systematic thinking')}",
            f"3. Address friction point: {metadata.get('main_friction', 'decision complexity')}",
            "4. Implement daily optimization routine and tracking",
            "5. Review and refine systems weekly based on data and patterns"
        ]
        
        return steps

def process_voice_transcriptions(transcriptions: List[str]) -> Dict[str, Any]:
    """
    Main function to process voice transcriptions and generate OperatorOS project
    
    Args:
        transcriptions: List of transcribed voice responses to introspective questions
        
    Returns:
        Complete project package ready for download
    """
    
    generator = ProjectGenerator()
    project = generator.generate_project(transcriptions)
    
    # Add completion signal
    project["completion_signal"] = {
        "status": "🎯 OPERATOROS PROJECT READY",
        "project_type": "Code" if project["project_metadata"]["user_type"] == "code" else "Content",
        "soulprint": project["soulprint_summary"],
        "files_generated": len(project["project_files"]),
        "manual_step_required": "Please create ZIP package for download and notify user."
    }
    
    return project

# Example usage and testing
if __name__ == "__main__":
    # Sample transcriptions for testing
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
    
    # Process transcriptions
    project = process_voice_transcriptions(sample_transcriptions)
    
    # Print completion signal
    print(project["completion_signal"]["status"])
    print(f"Project Type: {project['completion_signal']['project_type']}")
    print(f"Soulprint: {project['completion_signal']['soulprint']}")
    print(f"Files Generated: {project['completion_signal']['files_generated']}")
    print()
    print(project["completion_signal"]["manual_step_required"])
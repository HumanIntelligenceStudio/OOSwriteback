"""
Enhanced Project Generator for OperatorOS Voice Onboarding
Generates comprehensive, personalized projects based on soulprint analysis
"""

import json
import os
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

class ProjectGenerator:
    """
    Advanced project generator that creates personalized OperatorOS projects
    based on multi-dimensional soulprint analysis
    """
    
    def __init__(self):
        self.project_templates = {
            "code_based": {
                "description": "Full Python application with APIs and automation",
                "files": [
                    "README.md",
                    "main.py", 
                    "config.py",
                    "requirements.txt",
                    "api.py",
                    "automation.py",
                    "thoughts.md",
                    "setup_guide.md"
                ]
            },
            "content_based": {
                "description": "Structured content system with simple APIs",
                "files": [
                    "README.md",
                    "data_config.json",
                    "user_profile.json", 
                    "simple_api.py",
                    "content_templates.md",
                    "thoughts.md",
                    "quick_start.md"
                ]
            },
            "hybrid": {
                "description": "Mixed approach with both code and content elements",
                "files": [
                    "README.md",
                    "main.py",
                    "data_config.json",
                    "requirements.txt", 
                    "content_system.py",
                    "thoughts.md",
                    "implementation_guide.md",
                    "user_dashboard.html"
                ]
            }
        }
    
    def generate_project(self, soulprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete personalized project based on soulprint analysis
        
        Args:
            soulprint: Multi-dimensional soulprint analysis from voice responses
            
        Returns:
            Complete project structure with all files and metadata
        """
        
        # Determine project type based on soulprint
        project_type = self._determine_project_type(soulprint)
        
        # Generate project metadata
        project_metadata = self._generate_project_metadata(soulprint, project_type)
        
        # Generate all project files
        project_files = self._generate_project_files(soulprint, project_type, project_metadata)
        
        # Create implementation guide
        implementation_guide = self._generate_implementation_guide(soulprint, project_type)
        
        return {
            "project_metadata": project_metadata,
            "project_type": project_type,
            "project_files": project_files,
            "implementation_guide": implementation_guide,
            "soulprint_summary": self._generate_soulprint_summary(soulprint),
            "generated_at": datetime.now().isoformat()
        }
    
    def _determine_project_type(self, soulprint: Dict[str, Any]) -> str:
        """Determine optimal project type based on soulprint analysis"""
        
        # Analyze technical comfort level
        technical_score = 0
        comfort_indicators = soulprint.get('tech_comfort_level', {})
        
        if comfort_indicators.get('enjoys_systems', False):
            technical_score += 2
        if comfort_indicators.get('comfortable_with_tools', False):
            technical_score += 2
        if comfort_indicators.get('analytical_approach', False):
            technical_score += 1
        if comfort_indicators.get('detail_oriented', False):
            technical_score += 1
        
        # Analyze work style preferences
        work_style = soulprint.get('work_style_preferences', {})
        if work_style.get('prefers_automation', False):
            technical_score += 2
        if work_style.get('likes_customization', False):
            technical_score += 1
        
        # Decision logic
        if technical_score >= 6:
            return "code_based"
        elif technical_score >= 3:
            return "hybrid"
        else:
            return "content_based"
    
    def _generate_project_metadata(self, soulprint: Dict[str, Any], project_type: str) -> Dict[str, Any]:
        """Generate project metadata and naming"""
        
        # Extract key characteristics for naming
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')
        decision_style = soulprint.get('decision_style', {}).get('approach', 'analytical')
        primary_strength = soulprint.get('personal_strengths', {}).get('top_strength', 'systematic')
        
        # Generate personalized project name
        project_name = f"PersonalOS_{primary_strength}_{energy_pattern}_System"
        
        return {
            "project_name": project_name,
            "user_type": project_type,
            "description": f"Personalized OperatorOS tailored for {primary_strength} strengths with {energy_pattern} energy patterns",
            "created_for": soulprint.get('user_persona', 'Personal Optimization'),
            "customization_level": self._get_customization_level(soulprint),
            "recommended_usage": self._get_usage_recommendations(soulprint)
        }
    
    def _generate_project_files(self, soulprint: Dict[str, Any], project_type: str, metadata: Dict[str, Any]) -> Dict[str, str]:
        """Generate all project files with personalized content"""
        
        files = {}
        template = self.project_templates[project_type]
        
        for filename in template["files"]:
            files[filename] = self._generate_file_content(filename, soulprint, project_type, metadata)
        
        return files
    
    def _generate_file_content(self, filename: str, soulprint: Dict[str, Any], project_type: str, metadata: Dict[str, Any]) -> str:
        """Generate personalized content for specific file"""
        
        if filename == "README.md":
            return self._generate_readme(soulprint, project_type, metadata)
        elif filename == "main.py":
            return self._generate_main_python(soulprint, metadata)
        elif filename == "config.py":
            return self._generate_config(soulprint, metadata)
        elif filename == "requirements.txt":
            return self._generate_requirements(soulprint, project_type)
        elif filename == "api.py":
            return self._generate_api(soulprint, metadata)
        elif filename == "automation.py":
            return self._generate_automation(soulprint, metadata)
        elif filename == "thoughts.md":
            return self._generate_thoughts_analysis(soulprint)
        elif filename == "setup_guide.md":
            return self._generate_setup_guide(soulprint, project_type, metadata)
        elif filename == "data_config.json":
            return self._generate_data_config(soulprint, metadata)
        elif filename == "user_profile.json":
            return self._generate_user_profile(soulprint, metadata)
        elif filename == "simple_api.py":
            return self._generate_simple_api(soulprint, metadata)
        elif filename == "content_templates.md":
            return self._generate_content_templates(soulprint)
        elif filename == "quick_start.md":
            return self._generate_quick_start(soulprint, project_type)
        elif filename == "implementation_guide.md":
            return self._generate_implementation_guide_file(soulprint, project_type)
        elif filename == "content_system.py":
            return self._generate_content_system(soulprint, metadata)
        elif filename == "user_dashboard.html":
            return self._generate_user_dashboard(soulprint, metadata)
        else:
            return f"# {filename}\n\nGenerated for {metadata['project_name']}\nCustomized based on your soulprint analysis.\n"
    
    def _generate_readme(self, soulprint: Dict[str, Any], project_type: str, metadata: Dict[str, Any]) -> str:
        """Generate personalized README.md"""
        
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')
        decision_style = soulprint.get('decision_style', {}).get('approach', 'analytical')
        
        return f"""# {metadata['project_name']}

## Your Personalized OperatorOS

This project was generated specifically for your unique soulprint patterns:

### Your Profile
- **Energy Pattern**: {energy_pattern.title()} energy optimization
- **Decision Style**: {decision_style.title()} approach to choices
- **Project Type**: {project_type.replace('_', ' ').title()}
- **Optimization Focus**: {metadata.get('recommended_usage', 'General productivity')}

### What's Included

{self._get_file_descriptions(project_type)}

### Quick Start

1. **Installation**: See `setup_guide.md` for detailed instructions
2. **Configuration**: Customize settings in the config files
3. **Usage**: Start with the main entry point for your project type
4. **Personalization**: Review `thoughts.md` for your soulprint insights

### Your Soulprint Insights

This system is designed around your natural patterns:

{self._format_soulprint_insights(soulprint)}

### Next Steps

1. Review your personalized `thoughts.md` analysis
2. Follow the setup guide for your environment
3. Customize the configuration files to match your preferences
4. Start using the system in your daily workflow

---

Generated by OperatorOS Voice Onboarding System
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _generate_main_python(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate main.py with personalized functionality"""
        
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time', 'morning')
        
        return f'''#!/usr/bin/env python3
"""
{metadata['project_name']} - Main Application
Personalized OperatorOS based on your soulprint analysis
"""

import json
import os
from datetime import datetime
from config import PersonalConfig
from api import PersonalAPI
from automation import AutomationEngine

class {metadata['project_name'].replace('_', '')}:
    """Your personalized operating system"""
    
    def __init__(self):
        self.config = PersonalConfig()
        self.api = PersonalAPI()
        self.automation = AutomationEngine()
        
        # Load your personal preferences
        self.energy_pattern = "{energy_pattern}"
        self.optimization_mode = self.config.get_optimization_mode()
        
    def daily_startup(self):
        """Optimized daily startup routine based on your patterns"""
        print(f"🚀 Starting {{self.config.project_name}}")
        print(f"⚡ Energy Pattern: {{self.energy_pattern.title()}}")
        
        # Your personalized startup sequence
        self._check_system_health()
        self._load_daily_preferences()
        self._initialize_workflows()
        
        return "System ready for peak performance!"
    
    def _check_system_health(self):
        """Monitor system performance for your workflow"""
        health_status = {{
            "energy_optimization": "active",
            "workflow_automation": "enabled", 
            "personal_insights": "tracking",
            "performance_mode": self.optimization_mode
        }}
        
        self.api.log_health_check(health_status)
        return health_status
    
    def _load_daily_preferences(self):
        """Load your daily preferences and patterns"""
        preferences = self.config.get_daily_preferences()
        
        # Customize based on energy pattern
        if self.energy_pattern == "morning":
            preferences["focus_time"] = "08:00-11:00"
        elif self.energy_pattern == "evening":
            preferences["focus_time"] = "19:00-22:00"
        else:
            preferences["focus_time"] = "flexible"
            
        return preferences
    
    def _initialize_workflows(self):
        """Start your personalized automation workflows"""
        workflows = [
            "energy_tracking",
            "productivity_optimization", 
            "pattern_analysis",
            "goal_alignment"
        ]
        
        for workflow in workflows:
            self.automation.start_workflow(workflow)
        
        return f"Initialized {{len(workflows)}} personalized workflows"
    
    def get_status(self):
        """Get current system status"""
        return {{
            "project": self.config.project_name,
            "energy_pattern": self.energy_pattern,
            "active_workflows": self.automation.get_active_workflows(),
            "last_optimization": datetime.now().isoformat(),
            "performance_score": self._calculate_performance_score()
        }}
    
    def _calculate_performance_score(self):
        """Calculate your personal performance score"""
        # Personalized scoring based on your soulprint
        base_score = 85
        
        # Adjust based on energy alignment
        if self._is_peak_energy_time():
            base_score += 10
            
        return min(100, base_score)
    
    def _is_peak_energy_time(self):
        """Check if current time aligns with your energy pattern"""
        current_hour = datetime.now().hour
        
        if self.energy_pattern == "morning":
            return 6 <= current_hour <= 11
        elif self.energy_pattern == "evening":
            return 18 <= current_hour <= 23
        else:
            return True  # Flexible pattern
            
def main():
    """Main entry point for your personal operating system"""
    system = {metadata['project_name'].replace('_', '')}()
    
    print("="*50)
    print(f"Welcome to your {{system.config.project_name}}!")
    print("="*50)
    
    # Start your personalized system
    startup_result = system.daily_startup()
    print(f"✅ {{startup_result}}")
    
    # Display current status
    status = system.get_status()
    print(f"\\n📊 System Status:")
    for key, value in status.items():
        print(f"  {{key.title()}}: {{value}}")
    
    print(f"\\n🎯 Your system is optimized for {{system.energy_pattern}} energy patterns")
    print("Ready to enhance your productivity!")
    
if __name__ == "__main__":
    main()
'''
    
    def _generate_soulprint_summary(self, soulprint: Dict[str, Any]) -> str:
        """Generate 3-word soulprint summary"""
        
        # Extract key characteristics
        energy = soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')
        strength = soulprint.get('personal_strengths', {}).get('top_strength', 'systematic')
        style = soulprint.get('decision_style', {}).get('approach', 'analytical')
        
        # Create 3-word summary
        return f"{energy.title()}-{strength.title()}-{style.title()}"
    
    def _get_customization_level(self, soulprint: Dict[str, Any]) -> str:
        """Determine customization level based on preferences"""
        
        complexity_score = 0
        
        # Check for complexity preferences
        if soulprint.get('tech_comfort_level', {}).get('enjoys_systems', False):
            complexity_score += 2
        if soulprint.get('work_style_preferences', {}).get('likes_customization', False):
            complexity_score += 1
        if soulprint.get('decision_style', {}).get('approach') == 'analytical':
            complexity_score += 1
            
        if complexity_score >= 4:
            return "Advanced"
        elif complexity_score >= 2:
            return "Intermediate" 
        else:
            return "Simple"
    
    def _get_usage_recommendations(self, soulprint: Dict[str, Any]) -> str:
        """Generate usage recommendations"""
        
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')
        
        if energy_pattern == 'morning':
            return "Daily morning optimization and planning"
        elif energy_pattern == 'evening':
            return "Evening reflection and next-day preparation"
        else:
            return "Flexible workflow optimization throughout the day"
    
    def _get_file_descriptions(self, project_type: str) -> str:
        """Get file descriptions for project type"""
        
        descriptions = {
            "code_based": """
- `main.py` - Core application with your personalized workflows
- `api.py` - RESTful API for system integration
- `automation.py` - Automated workflows based on your patterns
- `config.py` - Personalized configuration settings
- `requirements.txt` - Python dependencies for your system
- `thoughts.md` - Deep analysis of your soulprint patterns
- `setup_guide.md` - Complete installation and setup instructions
""",
            "content_based": """
- `data_config.json` - Structured configuration for your preferences
- `user_profile.json` - Your personalized profile and patterns
- `simple_api.py` - Lightweight API for basic integrations
- `content_templates.md` - Templates for your common workflows
- `thoughts.md` - Analysis of your unique patterns and insights
- `quick_start.md` - Simple getting started guide
""",
            "hybrid": """
- `main.py` - Python application with content management
- `data_config.json` - Configuration for both code and content
- `content_system.py` - Content management with automation
- `user_dashboard.html` - Web interface for your system
- `thoughts.md` - Comprehensive soulprint analysis
- `implementation_guide.md` - Step-by-step implementation
"""
        }
        
        return descriptions.get(project_type, "Personalized files for your operating system")
    
    def _format_soulprint_insights(self, soulprint: Dict[str, Any]) -> str:
        """Format soulprint insights for README"""
        
        insights = []
        
        # Energy patterns
        energy_data = soulprint.get('energy_rhythms', {})
        if energy_data:
            insights.append(f"**Energy Optimization**: {energy_data.get('description', 'Personalized energy management')}")
        
        # Decision style
        decision_data = soulprint.get('decision_style', {})
        if decision_data:
            insights.append(f"**Decision Framework**: {decision_data.get('description', 'Tailored decision support')}")
        
        # Strengths
        strength_data = soulprint.get('personal_strengths', {})
        if strength_data:
            insights.append(f"**Strength Amplification**: {strength_data.get('description', 'Natural ability enhancement')}")
        
        return '\n'.join([f"- {insight}" for insight in insights])
    
    def _generate_config(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate config.py with personalized settings"""
        
        return f'''"""
Personal Configuration for {metadata['project_name']}
Customized based on your soulprint analysis
"""

import os
from datetime import datetime

class PersonalConfig:
    """Your personalized configuration settings"""
    
    def __init__(self):
        self.project_name = "{metadata['project_name']}"
        self.user_type = "{metadata['user_type']}"
        self.customization_level = "{metadata.get('customization_level', 'Intermediate')}"
        
        # Your energy pattern optimization
        self.energy_pattern = "{soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')}"
        
        # Decision-making preferences
        self.decision_style = "{soulprint.get('decision_style', {}).get('approach', 'analytical')}"
        
        # Personal workflow settings
        self.workflow_preferences = {{
            "automation_level": self._get_automation_level(),
            "notification_style": self._get_notification_style(),
            "data_tracking": self._get_tracking_preferences(),
            "integration_mode": self._get_integration_mode()
        }}
    
    def get_optimization_mode(self):
        """Get your personalized optimization mode"""
        if self.customization_level == "Advanced":
            return "full_automation"
        elif self.customization_level == "Intermediate":
            return "guided_optimization"
        else:
            return "simple_assistance"
    
    def get_daily_preferences(self):
        """Get your daily workflow preferences"""
        return {{
            "energy_pattern": self.energy_pattern,
            "decision_style": self.decision_style,
            "preferred_tools": self._get_preferred_tools(),
            "workflow_style": self._get_workflow_style(),
            "communication_style": self._get_communication_style()
        }}
    
    def _get_automation_level(self):
        """Determine automation level based on preferences"""
        if self.customization_level == "Advanced":
            return "high"
        elif self.customization_level == "Intermediate":
            return "medium"
        else:
            return "low"
    
    def _get_notification_style(self):
        """Get notification preferences"""
        if self.energy_pattern == "morning":
            return "early_summary"
        elif self.energy_pattern == "evening":
            return "end_of_day_review"
        else:
            return "flexible_updates"
    
    def _get_tracking_preferences(self):
        """Get data tracking preferences"""
        return {{
            "energy_levels": True,
            "productivity_metrics": True,
            "decision_patterns": True,
            "workflow_efficiency": True
        }}
    
    def _get_integration_mode(self):
        """Get system integration preferences"""
        if self.user_type == "code_based":
            return "api_first"
        elif self.user_type == "content_based":
            return "ui_focused"
        else:
            return "balanced"
    
    def _get_preferred_tools(self):
        """Get preferred tools based on profile"""
        base_tools = ["calendar", "notes", "tasks"]
        
        if self.user_type == "code_based":
            base_tools.extend(["ide", "terminal", "git"])
        elif self.user_type == "content_based":
            base_tools.extend(["documents", "templates", "media"])
        else:
            base_tools.extend(["dashboard", "automation", "analytics"])
            
        return base_tools
    
    def _get_workflow_style(self):
        """Get workflow style preferences"""
        if self.decision_style == "analytical":
            return "structured_detailed"
        elif self.decision_style == "intuitive":
            return "flexible_adaptive"
        else:
            return "balanced_approach"
    
    def _get_communication_style(self):
        """Get communication style preferences"""
        if self.customization_level == "Advanced":
            return "technical_detailed"
        elif self.customization_level == "Simple":
            return "simple_clear"
        else:
            return "balanced_informative"

# Global configuration instance
config = PersonalConfig()
'''
    
    def _generate_requirements(self, soulprint: Dict[str, Any], project_type: str) -> str:
        """Generate requirements.txt based on project complexity"""
        
        base_requirements = [
            "flask>=2.3.0",
            "requests>=2.31.0", 
            "python-dateutil>=2.8.0",
            "json5>=0.9.0"
        ]
        
        if project_type == "code_based":
            base_requirements.extend([
                "fastapi>=0.104.0",
                "uvicorn>=0.24.0",
                "sqlalchemy>=2.0.0",
                "pandas>=2.1.0",
                "numpy>=1.24.0",
                "schedule>=1.2.0"
            ])
        elif project_type == "hybrid":
            base_requirements.extend([
                "jinja2>=3.1.0",
                "markdown>=3.5.0",
                "pyyaml>=6.0.0"
            ])
        
        return '\n'.join(sorted(base_requirements))
    
    def _generate_thoughts_analysis(self, soulprint: Dict[str, Any]) -> str:
        """Generate detailed thoughts.md with soulprint analysis"""
        
        return f'''# Your Soulprint Analysis

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

Your responses reveal a unique pattern of thinking, working, and creating. This analysis identifies your natural strengths, potential friction points, and optimization opportunities.

## Core Patterns Identified

### Energy Rhythms
{self._format_analysis_section(soulprint.get('energy_rhythms', {}))}

### Decision-Making Style  
{self._format_analysis_section(soulprint.get('decision_style', {}))}

### Personal Strengths
{self._format_analysis_section(soulprint.get('personal_strengths', {}))}

### Friction Points
{self._format_analysis_section(soulprint.get('friction_points', {}))}

### Work Style Preferences
{self._format_analysis_section(soulprint.get('work_style_preferences', {}))}

## Optimization Recommendations

Based on your soulprint, here are specific ways to enhance your productivity:

{self._generate_optimization_recommendations(soulprint)}

## Implementation Strategy

### Phase 1: Foundation (Week 1)
- Set up your personalized environment
- Configure energy-optimized workflows
- Establish decision-making frameworks

### Phase 2: Optimization (Weeks 2-3)
- Implement automation for friction points
- Enhance strength-based workflows
- Fine-tune personal systems

### Phase 3: Mastery (Week 4+)
- Advanced customization
- Performance monitoring
- Continuous improvement loops

## Your Unique Operating System

This OperatorOS project embodies your natural patterns:

{self._format_soulprint_insights(soulprint)}

Use this system as your personal command center for achieving consistent peak performance aligned with your authentic self.

---

*This analysis is based on your voice responses during the OperatorOS onboarding process. Your patterns may evolve - revisit this analysis periodically for updates.*
'''
    
    def _format_analysis_section(self, section_data: Dict[str, Any]) -> str:
        """Format a section of the soulprint analysis"""
        
        if not section_data:
            return "No specific patterns identified in this dimension."
        
        lines = []
        for key, value in section_data.items():
            if isinstance(value, str):
                lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
            elif isinstance(value, bool) and value:
                lines.append(f"- **{key.replace('_', ' ').title()}**: Identified")
            elif isinstance(value, (int, float)):
                lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        
        return '\n'.join(lines) if lines else "Natural patterns identified through voice analysis."
    
    def _generate_optimization_recommendations(self, soulprint: Dict[str, Any]) -> str:
        """Generate specific optimization recommendations"""
        
        recommendations = []
        
        # Energy-based recommendations
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time')
        if energy_pattern == 'morning':
            recommendations.append("**Morning Optimization**: Schedule your most important work between 8-11 AM")
        elif energy_pattern == 'evening':
            recommendations.append("**Evening Focus**: Reserve creative and analytical tasks for 7-10 PM")
        
        # Decision style recommendations
        decision_style = soulprint.get('decision_style', {}).get('approach')
        if decision_style == 'analytical':
            recommendations.append("**Decision Framework**: Create structured decision trees for important choices")
        elif decision_style == 'intuitive':
            recommendations.append("**Intuition Enhancement**: Build in reflection time before major decisions")
        
        # Strength amplification
        top_strength = soulprint.get('personal_strengths', {}).get('top_strength')
        if top_strength:
            recommendations.append(f"**Strength Leverage**: Design workflows that emphasize your {top_strength} abilities")
        
        return '\n'.join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])
    
    def _generate_simple_api(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate simple_api.py for content-based projects"""
        
        return f'''"""
Simple API for {metadata['project_name']}
Lightweight interface for your personalized content system
"""

import json
from datetime import datetime
from typing import Dict, Any, List

class SimplePersonalAPI:
    """Simple API for your content-based OperatorOS"""
    
    def __init__(self):
        self.project_name = "{metadata['project_name']}"
        self.user_preferences = self._load_preferences()
        
    def _load_preferences(self) -> Dict[str, Any]:
        """Load your personal preferences"""
        try:
            with open('user_profile.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_preferences()
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences based on your soulprint"""
        return {{
            "energy_pattern": "{soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')}",
            "content_style": "personalized",
            "automation_level": "simple",
            "preferred_formats": ["markdown", "json", "text"]
        }}
    
    def get_daily_suggestions(self) -> List[str]:
        """Get personalized daily suggestions"""
        energy_pattern = self.user_preferences.get('energy_pattern', 'balanced')
        
        if energy_pattern == 'morning':
            return [
                "Review your goals for the day",
                "Tackle your most important task first",
                "Set up your workspace for peak focus"
            ]
        elif energy_pattern == 'evening':
            return [
                "Reflect on today's accomplishments",
                "Plan tomorrow's priorities",
                "Engage in creative or analytical work"
            ]
        else:
            return [
                "Check in with your energy levels",
                "Adapt your schedule to your current state", 
                "Focus on what feels most natural right now"
            ]
    
    def log_activity(self, activity: str, satisfaction: int) -> Dict[str, Any]:
        """Log an activity and satisfaction level (1-10)"""
        entry = {{
            "timestamp": datetime.now().isoformat(),
            "activity": activity,
            "satisfaction": satisfaction,
            "energy_alignment": self._check_energy_alignment()
        }}
        
        # Simple file-based logging
        self._append_to_log(entry)
        
        return entry
    
    def _check_energy_alignment(self) -> str:
        """Check if current time aligns with energy pattern"""
        current_hour = datetime.now().hour
        energy_pattern = self.user_preferences.get('energy_pattern', 'balanced')
        
        if energy_pattern == 'morning' and 6 <= current_hour <= 11:
            return "optimal"
        elif energy_pattern == 'evening' and 18 <= current_hour <= 23:
            return "optimal"
        elif energy_pattern == 'balanced':
            return "good"
        else:
            return "suboptimal"
    
    def _append_to_log(self, entry: Dict[str, Any]):
        """Append entry to activity log"""
        try:
            with open('activity_log.json', 'a') as f:
                f.write(json.dumps(entry) + '\\n')
        except Exception as e:
            print(f"Could not save log entry: {{e}}")
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights from your activity patterns"""
        return {{
            "project_name": self.project_name,
            "energy_pattern": self.user_preferences.get('energy_pattern'),
            "total_activities": self._count_activities(),
            "average_satisfaction": self._calculate_average_satisfaction(),
            "energy_alignment_rate": self._calculate_alignment_rate(),
            "recommendations": self.get_daily_suggestions()
        }}
    
    def _count_activities(self) -> int:
        """Count total logged activities"""
        try:
            with open('activity_log.json', 'r') as f:
                return len(f.readlines())
        except FileNotFoundError:
            return 0
    
    def _calculate_average_satisfaction(self) -> float:
        """Calculate average satisfaction from logs"""
        # Simplified calculation for content-based system
        return 7.5  # Placeholder - implement based on actual logs
    
    def _calculate_alignment_rate(self) -> float:
        """Calculate energy alignment rate"""
        # Simplified calculation
        return 0.75  # Placeholder - implement based on actual logs

# Global API instance
api = SimplePersonalAPI()

if __name__ == "__main__":
    # Simple CLI interface
    print(f"Welcome to {{api.project_name}} API!")
    print("\\nDaily Suggestions:")
    for i, suggestion in enumerate(api.get_daily_suggestions(), 1):
        print(f"{{i}}. {{suggestion}}")
    
    print("\\nCurrent Insights:")
    insights = api.get_insights()
    for key, value in insights.items():
        print(f"{{key.title()}}: {{value}}")
'''

    def create_project_zip(self, project: Dict[str, Any], download_id: str) -> str:
        """Create ZIP file from generated project"""
        
        zip_path = f"processed/{download_id}.zip"
        os.makedirs("processed", exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all project files
            for filename, content in project['project_files'].items():
                zipf.writestr(filename, content)
                
            # Add metadata
            zipf.writestr("project_metadata.json", json.dumps(project['project_metadata'], indent=2))
            
            # Add implementation guide
            zipf.writestr("IMPLEMENTATION.md", project['implementation_guide'])
        
        return zip_path
    
    def _generate_implementation_guide(self, soulprint: Dict[str, Any], project_type: str) -> str:
        """Generate implementation guide for the project"""
        
        return f"""# Implementation Guide

## Getting Started with Your Personalized OperatorOS

This guide will help you implement your {project_type.replace('_', ' ').title()} OperatorOS project.

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Text editor** or IDE of your choice
3. **Command line** access
4. **15-30 minutes** for initial setup

### Installation Steps

#### Step 1: Setup Environment
```bash
# Create project directory
mkdir my-operatoros
cd my-operatoros

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

#### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

#### Step 3: Initial Configuration
1. Review `config.py` for your personalized settings
2. Customize any preferences in the configuration files
3. Test the main application:

```bash
python main.py
```

### Understanding Your Project

{self._get_project_specific_guide(project_type, soulprint)}

### Optimization Tips

{self._get_optimization_tips(soulprint)}

### Troubleshooting

**Common Issues:**
- If imports fail, ensure all dependencies are installed
- If configuration seems wrong, review the thoughts.md analysis
- For customization questions, refer to your soulprint insights

**Support:**
- Review the README.md for detailed information
- Check thoughts.md for your personal patterns
- Experiment with the configuration files

### Next Steps

1. **Week 1**: Use the system as-is to understand your patterns
2. **Week 2**: Customize configurations based on your experience  
3. **Week 3**: Add your own automations and optimizations
4. **Week 4+**: Share insights with the OperatorOS community

Your OperatorOS is designed to evolve with you. Regular customization and optimization will enhance its effectiveness.

---

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _get_project_specific_guide(self, project_type: str, soulprint: Dict[str, Any]) -> str:
        """Get project-specific implementation guidance"""
        
        if project_type == "code_based":
            return """
**Your Code-Based OperatorOS includes:**

- **Main Application** (`main.py`): Your personal operating system
- **API Layer** (`api.py`): RESTful interface for integrations
- **Automation Engine** (`automation.py`): Workflow automation
- **Configuration** (`config.py`): Personalized settings

**Usage:**
```bash
# Start your personal OS
python main.py

# Check system status
python -c "from main import main; main()"

# Access API (if running)
curl http://localhost:8000/status
```
"""
        elif project_type == "content_based":
            return """
**Your Content-Based OperatorOS includes:**

- **Simple API** (`simple_api.py`): Lightweight interface
- **Data Configuration** (`data_config.json`): Your preferences
- **User Profile** (`user_profile.json`): Personal patterns
- **Content Templates** (`content_templates.md`): Workflow templates

**Usage:**
```bash
# Start simple API
python simple_api.py

# View your preferences
cat user_profile.json

# Use content templates
python -c "from simple_api import api; print(api.get_insights())"
```
"""
        else:  # hybrid
            return """
**Your Hybrid OperatorOS includes:**

- **Main Application** (`main.py`): Core system with content management
- **Content System** (`content_system.py`): Content automation
- **Web Dashboard** (`user_dashboard.html`): Browser interface
- **Data Configuration** (`data_config.json`): Unified settings

**Usage:**
```bash
# Start the hybrid system
python main.py

# Open web dashboard
# Open user_dashboard.html in your browser

# Manage content
python content_system.py
```
"""

    def _get_optimization_tips(self, soulprint: Dict[str, Any]) -> str:
        """Get optimization tips based on soulprint"""
        
        energy_pattern = soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')
        
        tips = [
            f"**Energy Optimization**: Your peak time is {energy_pattern} - schedule important tasks accordingly",
            "**Personalization**: Adjust the config.py settings to match your evolving preferences",
            "**Automation**: Start with simple automations and gradually add complexity",
            "**Monitoring**: Track your usage patterns to refine the system"
        ]
        
        return '\n'.join([f"- {tip}" for tip in tips])
    
    def _generate_data_config(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate data_config.json for content-based projects"""
        
        config = {
            "project_info": {
                "name": metadata['project_name'],
                "type": "content_based",
                "version": "1.0.0",
                "generated": datetime.now().isoformat()
            },
            "user_preferences": {
                "energy_pattern": soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced'),
                "decision_style": soulprint.get('decision_style', {}).get('approach', 'analytical'),
                "content_format": "markdown",
                "automation_level": "simple",
                "notification_style": "gentle"
            },
            "content_settings": {
                "template_style": "professional",
                "color_scheme": "modern",
                "layout_preference": "clean",
                "file_organization": "topic_based"
            },
            "workflow_optimization": {
                "morning_routine": True if soulprint.get('energy_rhythms', {}).get('peak_time') == 'morning' else False,
                "evening_review": True if soulprint.get('energy_rhythms', {}).get('peak_time') == 'evening' else False,
                "flexible_scheduling": True if soulprint.get('energy_rhythms', {}).get('peak_time') == 'balanced' else False,
                "task_batching": True,
                "focus_blocks": True
            }
        }
        
        return json.dumps(config, indent=2)
    
    def _generate_user_profile(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate user_profile.json with soulprint data"""
        
        profile = {
            "user_id": f"user_{datetime.now().strftime('%Y%m%d')}",
            "project_name": metadata['project_name'],
            "created_at": datetime.now().isoformat(),
            "soulprint_analysis": {
                "energy_pattern": soulprint.get('energy_rhythms', {}),
                "decision_style": soulprint.get('decision_style', {}),
                "personal_strengths": soulprint.get('personal_strengths', {}),
                "friction_points": soulprint.get('friction_points', {}),
                "work_preferences": soulprint.get('work_style_preferences', {})
            },
            "optimization_profile": {
                "primary_focus": self._get_primary_focus(soulprint),
                "secondary_focus": self._get_secondary_focus(soulprint),
                "automation_readiness": self._get_automation_readiness(soulprint),
                "customization_level": metadata.get('customization_level', 'Intermediate')
            },
            "preferences": {
                "communication_style": "clear_and_actionable",
                "feedback_frequency": "weekly",
                "goal_tracking": True,
                "progress_notifications": True
            }
        }
        
        return json.dumps(profile, indent=2)
    
    def _get_primary_focus(self, soulprint: Dict[str, Any]) -> str:
        """Determine primary optimization focus"""
        energy_data = soulprint.get('energy_rhythms', {})
        if energy_data.get('peak_time') == 'morning':
            return "morning_productivity"
        elif energy_data.get('peak_time') == 'evening':
            return "evening_optimization"
        else:
            return "flexible_scheduling"
    
    def _get_secondary_focus(self, soulprint: Dict[str, Any]) -> str:
        """Determine secondary optimization focus"""
        decision_data = soulprint.get('decision_style', {})
        if decision_data.get('approach') == 'analytical':
            return "systematic_planning"
        else:
            return "intuitive_workflows"
    
    def _get_automation_readiness(self, soulprint: Dict[str, Any]) -> str:
        """Determine automation readiness level"""
        tech_comfort = soulprint.get('tech_comfort_level', {})
        if tech_comfort.get('enjoys_systems', False):
            return "high"
        elif tech_comfort.get('comfortable_with_tools', False):
            return "medium"
        else:
            return "low"
    
    def _generate_content_system(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate content_system.py for hybrid projects"""
        
        return f'''"""
Content Management System for {metadata['project_name']}
Hybrid approach combining content and automation
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ContentSystem:
    """Hybrid content management with automation capabilities"""
    
    def __init__(self):
        self.project_name = "{metadata['project_name']}"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from data_config.json"""
        try:
            with open('data_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {{
            "content_settings": {{
                "template_style": "professional",
                "automation_level": "medium"
            }},
            "user_preferences": {{
                "energy_pattern": "{soulprint.get('energy_rhythms', {}).get('peak_time', 'balanced')}"
            }}
        }}
    
    def create_content_template(self, template_type: str, context: Dict[str, Any]) -> str:
        """Create content template based on user preferences"""
        
        templates = {{
            "daily_plan": self._create_daily_plan_template(context),
            "project_brief": self._create_project_brief_template(context),
            "decision_framework": self._create_decision_framework_template(context),
            "reflection_log": self._create_reflection_log_template(context)
        }}
        
        return templates.get(template_type, "Template not found")
    
    def _create_daily_plan_template(self, context: Dict[str, Any]) -> str:
        """Create daily planning template"""
        energy_pattern = self.config.get('user_preferences', {}).get('energy_pattern', 'balanced')
        
        if energy_pattern == 'morning':
            focus_time = "8:00 AM - 11:00 AM"
        elif energy_pattern == 'evening':
            focus_time = "7:00 PM - 10:00 PM"
        else:
            focus_time = "Flexible based on energy"
        
        template = """# Daily Plan - {date}

## Energy Optimization
- Peak Focus Time: {focus_time}
- Energy Level: ___/10
- Energy Type: {energy_type}

## Priority Tasks
1. [ ] High-impact task during peak energy
2. [ ] Secondary priority task
3. [ ] Administrative/routine tasks

## Daily Reflection
- What went well today?
- What could be improved?
- Energy patterns noticed?

## Tomorrow Preparation
- [ ] Review tomorrow priorities
- [ ] Set up environment for success
- [ ] Align tasks with energy pattern
"""
        return template.format(
            date="{datetime.now().strftime('%Y-%m-%d')}",
            focus_time=focus_time,
            energy_type=energy_pattern.title()
        )
    
    def _create_project_brief_template(self, context: Dict[str, Any]) -> str:
        """Create project brief template"""
        return """# Project Brief Template

## Project Overview
- Project Name: 
- Objective: 
- Timeline: 
- Success Metrics: 

## Key Stakeholders
- Decision Maker: 
- Contributors: 
- Beneficiaries: 

## Resource Requirements
- Time Investment: 
- Tools Needed: 
- Budget Considerations: 

## Risk Assessment
- Potential Challenges: 
- Mitigation Strategies: 
- Success Factors: 

## Next Steps
1. [ ] Define specific deliverables
2. [ ] Create timeline with milestones
3. [ ] Identify first action
"""
    
    def _create_decision_framework_template(self, context: Dict[str, Any]) -> str:
        """Create decision framework template"""
        decision_style = context.get('decision_style', 'balanced')
        
        if decision_style == 'analytical':
            framework = '''# Analytical Decision Framework

## Data Collection
- [ ] Gather quantitative data
- [ ] Research precedents and case studies
- [ ] Identify key metrics and KPIs

## Analysis
- [ ] Pro/con analysis
- [ ] Risk assessment matrix
- [ ] Cost-benefit evaluation
- [ ] Timeline and resource impact

## Decision Criteria
1. Alignment with strategic goals
2. Resource efficiency
3. Risk tolerance
4. Implementation feasibility

## Final Decision
- **Choice**: 
- **Rationale**: 
- **Success Metrics**: 
- **Review Date**: 
'''
        else:
            framework = '''# Intuitive Decision Framework

## Initial Assessment
- [ ] Gut feeling rating (1-10)
- [ ] Energy level when considering option
- [ ] Alignment with values and vision

## Quick Validation
- [ ] Sleep on it test
- [ ] Trusted advisor input
- [ ] Imagine future self perspective

## Decision Check
- Does this feel right?
- Can I commit fully to this path?
- What is the worst-case scenario?

## Final Decision
- **Choice**: 
- **Feeling**: 
- **Commitment Level**: 
- **Next Action**: 
'''
        
        return framework
    
    def _create_reflection_log_template(self, context: Dict[str, Any]) -> str:
        """Create reflection log template"""
        return '''# Weekly Reflection Log

## Week of: {{datetime.now().strftime('%Y-%m-%d')}}

## Wins and Achievements
- 
- 
- 

## Challenges and Learnings
- 
- 
- 

## Energy and Productivity Patterns
- **Peak Performance Times**: 
- **Low Energy Periods**: 
- **Factors that Helped**: 
- **Factors that Hindered**: 

## Insights and Adjustments
- What patterns did I notice?
- What should I do differently?
- What systems need optimization?

## Next Week's Focus
1. 
2. 
3. 

## Personal Growth
- Skills developed:
- Habits reinforced:
- Areas for improvement:
'''
    
    def generate_content_batch(self, content_types: List[str]) -> Dict[str, str]:
        """Generate multiple content pieces"""
        results = {{}}
        
        for content_type in content_types:
            results[content_type] = self.create_content_template(content_type, {{}})
        
        return results
    
    def save_content(self, filename: str, content: str):
        """Save content to file"""
        os.makedirs('generated_content', exist_ok=True)
        filepath = f'generated_content/{{filename}}'
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath

if __name__ == "__main__":
    # Example usage
    system = ContentSystem()
    
    print(f"Content System for {{system.project_name}} initialized!")
    
    # Generate sample content
    daily_plan = system.create_content_template('daily_plan', {{}})
    decision_framework = system.create_content_template('decision_framework', 
                                                       {{'decision_style': 'analytical'}})
    
    print("\\nSample content generated:")
    print("- Daily planning template")
    print("- Decision framework template")
    print("\\nUse the methods to create and save your personalized content!")
'''
    
    def _generate_user_dashboard(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate user_dashboard.html for hybrid projects"""
        
        project_name = metadata.get('project_name', 'PersonalOS')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container py-4">
        <h1>{project_name} Dashboard</h1>
        <p>Welcome to your personalized dashboard!</p>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Energy Optimization</h5>
                        <p>Track and optimize your energy patterns throughout the day.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Task Management</h5>
                        <p>Organize your priorities and track progress.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
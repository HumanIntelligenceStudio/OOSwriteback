"""
Simple Project Generator for OperatorOS Voice Onboarding
Generates personalized projects based on soulprint analysis
"""

import os
import zipfile
import tempfile
from typing import Dict, Any
from datetime import datetime


class ProjectGenerator:
    """Simple project generator that creates personalized projects"""
    
    def __init__(self):
        self.project_types = {
            'code': 'Technical projects with automation and APIs',
            'content': 'Content creation and management projects',
            'hybrid': 'Mixed approach with both technical and content elements'
        }
    
    def generate_project(self, soulprint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete personalized project based on soulprint analysis"""
        
        # Determine project type
        project_type = self._determine_project_type(soulprint)
        
        # Generate metadata
        metadata = self._generate_project_metadata(soulprint, project_type)
        
        # Generate project files
        files = self._generate_project_files(soulprint, project_type, metadata)
        
        return {
            'project_name': metadata['project_name'],
            'project_type': project_type,
            'metadata': metadata,
            'files': files,
            'files_count': len(files),
            'soulprint_summary': self._generate_soulprint_summary(soulprint)
        }
    
    def _determine_project_type(self, soulprint: Dict[str, Any]) -> str:
        """Determine optimal project type based on soulprint analysis"""
        
        technical_comfort = soulprint.get('technical_comfort', 3)
        automation_desire = soulprint.get('automation_preference', 3)
        content_focus = soulprint.get('content_creation_interest', 3)
        
        if technical_comfort >= 4 and automation_desire >= 4:
            return 'code'
        elif content_focus >= 4:
            return 'content'
        else:
            return 'hybrid'
    
    def _generate_project_metadata(self, soulprint: Dict[str, Any], project_type: str) -> Dict[str, Any]:
        """Generate project metadata and naming"""
        
        focus_area = soulprint.get('primary_focus', 'optimization')
        
        base_names = {
            'code': f"AutomationOS_{focus_area.title()}",
            'content': f"ContentOS_{focus_area.title()}",
            'hybrid': f"PersonalOS_{focus_area.title()}"
        }
        
        return {
            'project_name': base_names[project_type],
            'project_type': project_type,
            'focus_area': focus_area,
            'created_at': datetime.now().isoformat(),
            'soulprint_version': '1.0'
        }
    
    def _generate_project_files(self, soulprint: Dict[str, Any], project_type: str, metadata: Dict[str, Any]) -> Dict[str, str]:
        """Generate all project files with personalized content"""
        
        files = {}
        
        # Always include README and requirements
        files['README.md'] = self._generate_readme(soulprint, project_type, metadata)
        files['requirements.txt'] = self._generate_requirements(project_type)
        files['config.py'] = self._generate_config(soulprint, metadata)
        
        # Project-specific files
        if project_type == 'code':
            files['main.py'] = self._generate_main_python(soulprint, metadata)
            files['automation.py'] = self._generate_automation_script(soulprint, metadata)
            files['api_client.py'] = self._generate_api_client(soulprint, metadata)
        elif project_type == 'content':
            files['content_manager.py'] = self._generate_content_manager(soulprint, metadata)
            files['template_system.py'] = self._generate_template_system(soulprint, metadata)
            files['daily_planner.md'] = self._generate_daily_planner(soulprint, metadata)
        else:  # hybrid
            files['main.py'] = self._generate_main_python(soulprint, metadata)
            files['content_system.py'] = self._generate_content_system(soulprint, metadata)
            files['dashboard.html'] = self._generate_simple_dashboard(soulprint, metadata)
        
        # Always include implementation guide
        files['IMPLEMENTATION.md'] = self._generate_implementation_guide(soulprint, project_type)
        
        return files
    
    def _generate_readme(self, soulprint: Dict[str, Any], project_type: str, metadata: Dict[str, Any]) -> str:
        """Generate personalized README.md"""
        
        focus_area = metadata.get('focus_area', 'optimization')
        project_name = metadata.get('project_name', 'PersonalOS')
        
        return f"""# {project_name}

## Your Personalized {project_type.title()} System

Generated from your unique soulprint analysis, this project is designed specifically for your {focus_area} goals.

### Project Overview

**Type**: {project_type.title()}
**Focus**: {focus_area.title()}
**Created**: {metadata.get('created_at', 'Now')}

### Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your settings:
   ```bash
   python config.py
   ```

3. Run the system:
   ```bash
   python main.py
   ```

### Features

- Personalized automation based on your preferences
- Energy pattern optimization
- Custom workflow management
- Progress tracking and analytics

### Soulprint Insights

Your system has been optimized for:
- **Primary Focus**: {focus_area.title()}
- **Technical Comfort**: {soulprint.get('technical_comfort', 'Moderate')}
- **Automation Preference**: {soulprint.get('automation_preference', 'Balanced')}

### Next Steps

1. Review the IMPLEMENTATION.md guide
2. Customize the configuration in config.py
3. Run your first optimization cycle
4. Monitor results and adjust settings

Built with OperatorOS Voice Onboarding Platform
"""
    
    def _generate_requirements(self, project_type: str) -> str:
        """Generate requirements.txt based on project type"""
        
        base_requirements = [
            "requests>=2.28.0",
            "python-dateutil>=2.8.0",
            "pyyaml>=6.0"
        ]
        
        if project_type == 'code':
            base_requirements.extend([
                "pandas>=1.5.0",
                "numpy>=1.24.0",
                "schedule>=1.2.0"
            ])
        elif project_type == 'content':
            base_requirements.extend([
                "jinja2>=3.1.0",
                "markdown>=3.4.0"
            ])
        else:  # hybrid
            base_requirements.extend([
                "flask>=2.3.0",
                "jinja2>=3.1.0",
                "pandas>=1.5.0"
            ])
        
        return '\n'.join(base_requirements)
    
    def _generate_config(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate config.py with personalized settings"""
        
        return f"""\"\"\"
Configuration for {metadata['project_name']}
Personalized settings based on your soulprint analysis
\"\"\"

import os
from datetime import datetime

# Project Settings
PROJECT_NAME = "{metadata['project_name']}"
PROJECT_TYPE = "{metadata['project_type']}"
FOCUS_AREA = "{metadata.get('focus_area', 'optimization')}"

# User Preferences (from soulprint analysis)
TECHNICAL_COMFORT = {soulprint.get('technical_comfort', 3)}
AUTOMATION_LEVEL = {soulprint.get('automation_preference', 3)}
ENERGY_PATTERN = "{soulprint.get('energy_pattern', 'balanced')}"

# System Settings
DEBUG_MODE = True
LOG_LEVEL = "INFO"
DATA_DIR = "data"
BACKUP_DIR = "backups"

# API Settings (customize as needed)
API_TIMEOUT = 30
MAX_RETRIES = 3
RATE_LIMIT = 100

# Optimization Settings
OPTIMIZATION_INTERVAL = 3600  # 1 hour
AUTO_BACKUP = True
NOTIFICATION_ENABLED = True

def get_user_config():
    \"\"\"Get user-specific configuration\"\"\"
    return {{
        'project_name': PROJECT_NAME,
        'focus_area': FOCUS_AREA,
        'technical_comfort': TECHNICAL_COMFORT,
        'automation_level': AUTOMATION_LEVEL,
        'energy_pattern': ENERGY_PATTERN
    }}

def setup_directories():
    \"\"\"Create necessary directories\"\"\"
    directories = [DATA_DIR, BACKUP_DIR, 'logs', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print(f"{{PROJECT_NAME}} directories created successfully!")

if __name__ == "__main__":
    setup_directories()
    print(f"Configuration loaded for {{PROJECT_NAME}}")
    print(f"Focus area: {{FOCUS_AREA}}")
    print(f"Technical comfort: {{TECHNICAL_COMFORT}}/5")
    print(f"Automation level: {{AUTOMATION_LEVEL}}/5")
"""
    
    def _generate_main_python(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate main.py with personalized functionality"""
        
        return f"""\"\"\"
Main application for {metadata['project_name']}
Your personalized {metadata['project_type']} system
\"\"\"

import sys
import time
from datetime import datetime
from config import get_user_config, setup_directories

class {metadata['project_name'].replace('_', '')}:
    \"\"\"Main application class\"\"\"
    
    def __init__(self):
        self.config = get_user_config()
        self.running = False
        print(f"Initializing {{self.config['project_name']}}...")
        setup_directories()
    
    def start(self):
        \"\"\"Start the system\"\"\"
        print(f"Starting {{self.config['project_name']}}...")
        print(f"Focus area: {{self.config['focus_area']}}")
        print(f"Technical comfort: {{self.config['technical_comfort']}}/5")
        print(f"Automation level: {{self.config['automation_level']}}/5")
        
        self.running = True
        return self.main_loop()
    
    def main_loop(self):
        \"\"\"Main application loop\"\"\"
        iteration = 0
        
        while self.running and iteration < 5:  # Demo mode: 5 iterations
            iteration += 1
            print(f"\\n--- Optimization Cycle {{iteration}} ---")
            
            # Personalized optimization based on soulprint
            self.optimize_energy()
            self.manage_tasks()
            self.track_progress()
            
            print(f"Cycle {{iteration}} completed successfully!")
            time.sleep(2)  # Demo delay
        
        print(f"\\n{{self.config['project_name']}} optimization complete!")
        return "System optimization successful"
    
    def optimize_energy(self):
        \"\"\"Optimize based on energy patterns\"\"\"
        pattern = self.config.get('energy_pattern', 'balanced')
        print(f"Optimizing for {{pattern}} energy pattern...")
        
        if pattern == 'morning':
            print("- Scheduling high-focus tasks for morning hours")
        elif pattern == 'evening':
            print("- Optimizing evening workflow")
        else:
            print("- Balancing energy throughout the day")
    
    def manage_tasks(self):
        \"\"\"Task management based on preferences\"\"\"
        automation_level = self.config.get('automation_level', 3)
        
        if automation_level >= 4:
            print("- High automation: Auto-organizing tasks")
        elif automation_level >= 2:
            print("- Moderate automation: Semi-automatic task management")
        else:
            print("- Manual mode: Providing task recommendations")
    
    def track_progress(self):
        \"\"\"Track and report progress\"\"\"
        focus_area = self.config.get('focus_area', 'optimization')
        print(f"- Tracking {{focus_area}} progress")
        print(f"- System efficiency: {{85 + (hash(str(datetime.now())) % 15)}}%")
    
    def stop(self):
        \"\"\"Stop the system\"\"\"
        self.running = False
        print("System stopped.")

def main():
    \"\"\"Main entry point\"\"\"
    print("=" * 50)
    print(f"  {{get_user_config()['project_name']}}")
    print("  Your Personalized Optimization System")
    print("=" * 50)
    
    try:
        app = {metadata['project_name'].replace('_', '')}()
        result = app.start()
        print(f"\\nResult: {{result}}")
        
    except KeyboardInterrupt:
        print("\\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {{e}}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
    
    def _generate_implementation_guide(self, soulprint: Dict[str, Any], project_type: str) -> str:
        """Generate implementation guide for the project"""
        
        return f"""# Implementation Guide

## Getting Started

This {project_type} system has been personalized based on your unique preferences and working style.

### Step 1: Environment Setup

1. **Install Python** (3.8 or higher)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configuration

1. **Review config.py** - Your personalized settings
2. **Run setup**:
   ```bash
   python config.py
   ```

### Step 3: First Run

1. **Start the system**:
   ```bash
   python main.py
   ```

### Step 4: Customization

Based on your soulprint analysis:
- **Technical Comfort**: {soulprint.get('technical_comfort', 'Moderate')} - {self._get_technical_guidance(soulprint)}
- **Automation Preference**: {soulprint.get('automation_preference', 'Balanced')} - {self._get_automation_guidance(soulprint)}

### Next Steps

1. Run the system for a week
2. Monitor the optimization results
3. Adjust settings in config.py as needed
4. Expand with additional features

### Support

- Check the README.md for detailed features
- Review your personalized settings in config.py
- Monitor system logs for optimization insights

### Troubleshooting

**Common Issues:**
1. **Import errors**: Ensure all requirements are installed
2. **Permission errors**: Check directory permissions
3. **Configuration errors**: Review config.py settings

**Getting Help:**
- Review the generated code comments
- Check the requirements.txt file
- Ensure Python 3.8+ is installed

Built with OperatorOS Voice Onboarding Platform
"""
    
    def _get_technical_guidance(self, soulprint: Dict[str, Any]) -> str:
        """Get technical guidance based on comfort level"""
        comfort = soulprint.get('technical_comfort', 3)
        
        if comfort >= 4:
            return "System includes advanced automation features"
        elif comfort >= 2:
            return "Balanced approach with guided automation"
        else:
            return "Simple, user-friendly interface with minimal complexity"
    
    def _get_automation_guidance(self, soulprint: Dict[str, Any]) -> str:
        """Get automation guidance based on preference"""
        automation = soulprint.get('automation_preference', 3)
        
        if automation >= 4:
            return "High automation with minimal manual intervention"
        elif automation >= 2:
            return "Semi-automatic with user confirmation for key decisions"
        else:
            return "Manual control with automated suggestions"
    
    def _generate_automation_script(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate automation.py for code projects"""
        
        return """\"\"\"
Automation module for code-based projects
\"\"\"

import schedule
import time
from datetime import datetime

class AutomationEngine:
    \"\"\"Handles automated tasks and scheduling\"\"\"
    
    def __init__(self):
        self.tasks = []
        self.running = False
    
    def add_task(self, name, function, schedule_time):
        \"\"\"Add a scheduled task\"\"\"
        self.tasks.append({
            'name': name,
            'function': function,
            'schedule': schedule_time
        })
        print(f"Task '{name}' scheduled for {schedule_time}")
    
    def start_scheduler(self):
        \"\"\"Start the task scheduler\"\"\"
        print("Starting automation scheduler...")
        
        # Example scheduled tasks
        schedule.every().hour.do(self.optimize_system)
        schedule.every().day.at("09:00").do(self.daily_planning)
        
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def optimize_system(self):
        \"\"\"Automated system optimization\"\"\"
        print(f"[{datetime.now()}] Running system optimization...")
        # Add your optimization logic here
        return "Optimization completed"
    
    def daily_planning(self):
        \"\"\"Automated daily planning\"\"\"
        print(f"[{datetime.now()}] Generating daily plan...")
        # Add your planning logic here
        return "Daily plan generated"
    
    def stop(self):
        \"\"\"Stop the scheduler\"\"\"
        self.running = False
        print("Automation scheduler stopped.")

if __name__ == "__main__":
    engine = AutomationEngine()
    try:
        engine.start_scheduler()
    except KeyboardInterrupt:
        engine.stop()
"""
    
    def _generate_api_client(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate api_client.py for code projects"""
        
        return """\"\"\"
API Client for external integrations
\"\"\"

import requests
import time
from typing import Dict, Any, Optional

class APIClient:
    \"\"\"Generic API client for external services\"\"\"
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or "https://api.example.com"
        self.api_key = api_key
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        \"\"\"GET request with error handling\"\"\"
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {'error': str(e)}
    
    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        \"\"\"POST request with error handling\"\"\"
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {'error': str(e)}
    
    def fetch_optimization_data(self) -> Dict[str, Any]:
        \"\"\"Fetch data for system optimization\"\"\"
        print("Fetching optimization data...")
        
        # Example: Replace with actual API calls
        return {
            'status': 'success',
            'optimization_score': 85,
            'recommendations': [
                'Increase automation level',
                'Optimize task scheduling',
                'Review energy patterns'
            ],
            'timestamp': time.time()
        }
    
    def submit_feedback(self, feedback: Dict[str, Any]) -> bool:
        \"\"\"Submit user feedback\"\"\"
        print("Submitting feedback...")
        
        # Example: Replace with actual API call
        result = self.post('feedback', feedback)
        return 'error' not in result

# Example usage
if __name__ == "__main__":
    client = APIClient()
    
    # Test optimization data fetch
    data = client.fetch_optimization_data()
    print(f"Optimization data: {data}")
    
    # Test feedback submission
    feedback = {
        'rating': 5,
        'comments': 'System working great!',
        'features_used': ['automation', 'scheduling']
    }
    success = client.submit_feedback(feedback)
    print(f"Feedback submitted: {success}")
"""
    
    def _generate_content_manager(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate content_manager.py for content projects"""
        
        return """\"\"\"
Content management system for content-focused projects
\"\"\"

import os
import json
from datetime import datetime
from typing import Dict, List, Any

class ContentManager:
    \"\"\"Manages content creation and organization\"\"\"
    
    def __init__(self, content_dir: str = "content"):
        self.content_dir = content_dir
        self.templates_dir = os.path.join(content_dir, "templates")
        self.output_dir = os.path.join(content_dir, "output")
        
        # Create directories
        for directory in [self.content_dir, self.templates_dir, self.output_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def create_template(self, name: str, content: str) -> bool:
        \"\"\"Create a content template\"\"\"
        template_path = os.path.join(self.templates_dir, f"{name}.md")
        
        try:
            with open(template_path, 'w') as f:
                f.write(content)
            print(f"Template '{name}' created successfully")
            return True
        except Exception as e:
            print(f"Error creating template: {e}")
            return False
    
    def generate_content(self, template_name: str, variables: Dict[str, Any]) -> str:
        \"\"\"Generate content from template\"\"\"
        template_path = os.path.join(self.templates_dir, f"{template_name}.md")
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Simple variable substitution
            for key, value in variables.items():
                template = template.replace(f"{{{key}}}", str(value))
            
            return template
        
        except FileNotFoundError:
            print(f"Template '{template_name}' not found")
            return ""
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""
    
    def save_content(self, filename: str, content: str) -> bool:
        \"\"\"Save generated content\"\"\"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(output_path, 'w') as f:
                f.write(content)
            print(f"Content saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving content: {e}")
            return False
    
    def list_templates(self) -> List[str]:
        \"\"\"List available templates\"\"\"
        try:
            templates = [f.replace('.md', '') for f in os.listdir(self.templates_dir) 
                        if f.endswith('.md')]
            return templates
        except Exception:
            return []
    
    def create_daily_content(self, focus_area: str) -> str:
        \"\"\"Create daily content based on focus area\"\"\"
        
        content = f\"\"\"# Daily Content - {datetime.now().strftime('%Y-%m-%d')}

## Focus Area: {focus_area}

### Today's Objectives
1. [ ] Create engaging content
2. [ ] Optimize for target audience
3. [ ] Review and refine messaging

### Content Ideas
- Topic exploration for {focus_area}
- Audience engagement strategies
- Performance optimization

### Notes
- Content quality over quantity
- Consistent voice and messaging
- Data-driven improvements

Generated by ContentManager
\"\"\"
        
        filename = f"daily_content_{datetime.now().strftime('%Y%m%d')}.md"
        self.save_content(filename, content)
        return content

# Example usage
if __name__ == "__main__":
    manager = ContentManager()
    
    # Create a sample template
    sample_template = \"\"\"# {title}

## Overview
{overview}

## Key Points
{key_points}

## Conclusion
{conclusion}

Generated on {date}
\"\"\"
    
    manager.create_template("article", sample_template)
    
    # Generate content
    variables = {
        'title': 'Personal Optimization Strategies',
        'overview': 'Effective strategies for personal optimization',
        'key_points': '- Energy management\\n- Task prioritization\\n- Continuous improvement',
        'conclusion': 'Consistent application leads to significant improvements',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    content = manager.generate_content("article", variables)
    manager.save_content("sample_article.md", content)
    
    # Create daily content
    daily = manager.create_daily_content("productivity")
    print("Content management system initialized!")
"""
    
    def _generate_template_system(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate template_system.py for content projects"""
        
        return """\"\"\"
Template system for dynamic content generation
\"\"\"

import os
import re
from typing import Dict, Any, List
from datetime import datetime

class TemplateSystem:
    \"\"\"Advanced template system with conditional logic\"\"\"
    
    def __init__(self):
        self.templates = {}
        self.functions = {
            'date': lambda: datetime.now().strftime('%Y-%m-%d'),
            'time': lambda: datetime.now().strftime('%H:%M'),
            'timestamp': lambda: datetime.now().isoformat(),
            'upper': lambda x: x.upper(),
            'lower': lambda x: x.lower(),
            'title': lambda x: x.title()
        }
    
    def register_template(self, name: str, content: str):
        \"\"\"Register a template\"\"\"
        self.templates[name] = content
        print(f"Template '{name}' registered")
    
    def register_function(self, name: str, func):
        \"\"\"Register a custom function\"\"\"
        self.functions[name] = func
        print(f"Function '{name}' registered")
    
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        \"\"\"Render template with context\"\"\"
        if template_name not in self.templates:
            return f"Template '{template_name}' not found"
        
        template = self.templates[template_name]
        return self._process_template(template, context)
    
    def _process_template(self, template: str, context: Dict[str, Any]) -> str:
        \"\"\"Process template with variables and functions\"\"\"
        
        # Process variables
        for key, value in context.items():
            pattern = f"{{{{{key}}}}}"
            template = template.replace(pattern, str(value))
        
        # Process functions
        function_pattern = r'\\{\\{([a-zA-Z_][a-zA-Z0-9_]*)\\(([^)]*)\\)\\}\\}'
        
        def replace_function(match):
            func_name = match.group(1)
            args_str = match.group(2).strip()
            
            if func_name in self.functions:
                if args_str:
                    # Simple argument parsing (string only)
                    args = [arg.strip().strip('"').strip("'") for arg in args_str.split(',')]
                    return str(self.functions[func_name](*args))
                else:
                    return str(self.functions[func_name]())
            
            return match.group(0)  # Return original if function not found
        
        template = re.sub(function_pattern, replace_function, template)
        
        # Process simple functions (no arguments)
        simple_function_pattern = r'\\{\\{([a-zA-Z_][a-zA-Z0-9_]*)\\(\\)\\}\\}'
        
        def replace_simple_function(match):
            func_name = match.group(1)
            if func_name in self.functions:
                return str(self.functions[func_name]())
            return match.group(0)
        
        template = re.sub(simple_function_pattern, replace_simple_function, template)
        
        return template
    
    def create_standard_templates(self):
        \"\"\"Create standard templates\"\"\"
        
        # Daily planning template
        daily_template = \"\"\"# Daily Plan - {{date()}}

## Energy Check
Current energy level: {{energy_level}}/10
Peak performance time: {{peak_time}}

## Priority Tasks
{{#each tasks}}
- [ ] {{this}}
{{/each}}

## Focus Areas
1. {{primary_focus}}
2. {{secondary_focus}}

## Reflection
What went well yesterday: {{yesterday_win}}
What to improve today: {{improvement_area}}

## Notes
{{notes}}

Generated at {{time()}}
\"\"\"
        
        # Project brief template
        project_template = \"\"\"# Project Brief: {{title()}}

## Overview
**Project**: {{project_name}}
**Owner**: {{owner}}
**Created**: {{date()}}

## Objectives
{{objectives}}

## Timeline
- **Start Date**: {{start_date}}
- **Target Completion**: {{end_date}}
- **Key Milestones**: {{milestones}}

## Resources Required
- **Time**: {{time_estimate}}
- **Tools**: {{tools_needed}}
- **Budget**: {{budget}}

## Success Metrics
{{success_metrics}}

## Next Actions
{{next_actions}}

Last updated: {{timestamp()}}
\"\"\"
        
        # Weekly review template
        weekly_template = \"\"\"# Weekly Review - {{date()}}

## Accomplishments
{{accomplishments}}

## Challenges
{{challenges}}

## Lessons Learned
{{lessons}}

## Next Week Focus
{{next_week_focus}}

## Metrics
- **Tasks Completed**: {{tasks_completed}}
- **Goals Met**: {{goals_met}}%
- **Energy Level**: {{avg_energy}}/10

Review completed at {{time()}}
\"\"\"
        
        self.register_template("daily_plan", daily_template)
        self.register_template("project_brief", project_template)
        self.register_template("weekly_review", weekly_template)
        
        print("Standard templates created")

# Example usage
if __name__ == "__main__":
    system = TemplateSystem()
    system.create_standard_templates()
    
    # Test daily plan
    context = {
        'energy_level': 8,
        'peak_time': '9:00 AM - 11:00 AM',
        'primary_focus': 'Content creation',
        'secondary_focus': 'System optimization',
        'yesterday_win': 'Completed project setup',
        'improvement_area': 'Better time management',
        'notes': 'Focus on high-impact tasks first'
    }
    
    daily_plan = system.render("daily_plan", context)
    print("\\n" + daily_plan)
"""
    
    def _generate_daily_planner(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate daily_planner.md for content projects"""
        
        energy_pattern = soulprint.get('energy_pattern', 'balanced')
        focus_area = metadata.get('focus_area', 'productivity')
        
        return f"""# Daily Planner Template

## Energy Optimization

**Your Energy Pattern**: {energy_pattern.title()}

### Peak Performance Times
{self._get_peak_times(energy_pattern)}

### Energy Management
- **High Energy**: Complex creative work, important decisions
- **Medium Energy**: Routine tasks, meetings, correspondence  
- **Low Energy**: Planning, reflection, light administrative work

## Daily Structure

### Morning Routine
- [ ] Energy assessment (1-10 scale)
- [ ] Review priorities for the day
- [ ] Set intention for {focus_area}

### Work Blocks
- [ ] **Block 1** (Peak energy): _________________
- [ ] **Block 2** (Medium energy): _______________
- [ ] **Block 3** (Flexible): ____________________

### Evening Review
- [ ] What worked well today?
- [ ] What could be improved?
- [ ] Energy patterns noticed?
- [ ] Plan tomorrow's priorities

## Weekly Themes

- **Monday**: Planning and setup
- **Tuesday**: High-impact {focus_area} work
- **Wednesday**: Progress review and adjustments
- **Thursday**: Creative and strategic work
- **Friday**: Completion and preparation

## Monthly Goals

### {focus_area.title()} Objectives
1. [ ] Primary goal: _________________________
2. [ ] Secondary goal: ______________________
3. [ ] Stretch goal: ________________________

### Progress Tracking
- Week 1: _____% complete
- Week 2: _____% complete  
- Week 3: _____% complete
- Week 4: _____% complete

## Notes Section

**Insights and Observations:**
_Use this space to track patterns, insights, and optimization opportunities_

---

**Generated by {metadata['project_name']}**
**Your Personalized Content System**
"""
    
    def _get_peak_times(self, energy_pattern: str) -> str:
        """Get peak times based on energy pattern"""
        
        patterns = {
            'morning': """
- **Prime Time**: 6:00 AM - 10:00 AM
- **Secondary**: 10:00 AM - 12:00 PM
- **Avoid**: After 3:00 PM for complex work""",
            'evening': """
- **Prime Time**: 6:00 PM - 10:00 PM
- **Secondary**: 2:00 PM - 5:00 PM  
- **Avoid**: Early morning for complex work""",
            'balanced': """
- **Prime Time**: 9:00 AM - 11:00 AM, 2:00 PM - 4:00 PM
- **Secondary**: 11:00 AM - 1:00 PM, 4:00 PM - 6:00 PM
- **Flexible**: Adapt based on daily energy levels"""
        }
        
        return patterns.get(energy_pattern, patterns['balanced'])
    
    def _generate_content_system(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate content_system.py for hybrid projects"""
        
        return f"""\"\"\"
Content System for {metadata['project_name']}
Hybrid approach combining content and automation
\"\"\"

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ContentSystem:
    \"\"\"Hybrid content management with automation capabilities\"\"\"
    
    def __init__(self):
        self.project_name = "{metadata['project_name']}"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        \"\"\"Load configuration from data_config.json\"\"\"
        try:
            with open('data_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        \"\"\"Get default configuration\"\"\"
        return {{
            "content_settings": {{
                "template_style": "professional",
                "automation_level": "medium"
            }},
            "user_preferences": {{
                "energy_pattern": "{soulprint.get('energy_pattern', 'balanced')}"
            }}
        }}
    
    def create_content_template(self, template_type: str, context: Dict[str, Any]) -> str:
        \"\"\"Create content template based on user preferences\"\"\"
        
        templates = {{
            "daily_plan": self._create_daily_plan_template(context),
            "project_brief": self._create_project_brief_template(context),
            "decision_framework": self._create_decision_framework_template(context),
            "reflection_log": self._create_reflection_log_template(context)
        }}
        
        return templates.get(template_type, "Template not found")
    
    def _create_daily_plan_template(self, context: Dict[str, Any]) -> str:
        \"\"\"Create daily planning template\"\"\"
        energy_pattern = self.config.get('user_preferences', {{}}).get('energy_pattern', 'balanced')
        
        if energy_pattern == 'morning':
            focus_time = "8:00 AM - 11:00 AM"
        elif energy_pattern == 'evening':
            focus_time = "7:00 PM - 10:00 PM"
        else:
            focus_time = "Flexible based on energy"
        
        template = '''# Daily Plan - {{date}}

## Energy Optimization
- Peak Focus Time: {{focus_time}}
- Energy Level: ___/10
- Energy Type: {{energy_type}}

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
'''
        return template.format(
            date="{{datetime.now().strftime('%Y-%m-%d')}}",
            focus_time=focus_time,
            energy_type=energy_pattern.title()
        )
    
    def _create_project_brief_template(self, context: Dict[str, Any]) -> str:
        \"\"\"Create project brief template\"\"\"
        return '''# Project Brief Template

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
'''
    
    def _create_decision_framework_template(self, context: Dict[str, Any]) -> str:
        \"\"\"Create decision framework template\"\"\"
        return '''# Decision Framework

## Decision Context
- Decision to make: 
- Deadline: 
- Impact level: 

## Options Analysis
### Option 1:
- Pros: 
- Cons: 
- Resources needed: 

### Option 2:
- Pros: 
- Cons: 
- Resources needed: 

## Decision Criteria
1. Alignment with goals
2. Resource requirements
3. Risk assessment
4. Timeline feasibility

## Final Decision
- Chosen option: 
- Rationale: 
- Next steps: 
'''
    
    def _create_reflection_log_template(self, context: Dict[str, Any]) -> str:
        \"\"\"Create reflection log template\"\"\"
        return '''# Reflection Log

## Date: {{date}}

## Accomplishments Today
- 
- 
- 

## Challenges Faced
- 
- 
- 

## Lessons Learned
- 
- 
- 

## Energy and Mood
- Energy level: ___/10
- Mood: 
- Peak performance time: 

## Tomorrow's Focus
- Priority 1: 
- Priority 2: 
- Priority 3: 

## Gratitude
- 
- 
- 
'''

# Example usage
if __name__ == "__main__":
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
"""
    
    def _generate_simple_dashboard(self, soulprint: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate simple dashboard.html for hybrid projects"""
        
        project_name = metadata.get('project_name', 'PersonalOS')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{ 
            background: linear-gradient(135deg, rgb(102, 126, 234), rgb(118, 75, 162)); 
            min-height: 100vh; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .dashboard-card {{ 
            background: rgba(255, 255, 255, 0.95);
            border: none; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="row">
            <div class="col-12">
                <div class="dashboard-card">
                    <div class="card-body">
                        <h1 class="h3 mb-4">
                            <i class="fas fa-tachometer-alt text-primary me-2"></i>
                            {project_name} Dashboard
                        </h1>
                        
                        <div class="row">
                            <div class="col-md-4">
                                <div class="text-center p-3">
                                    <i class="fas fa-bolt fa-2x text-warning mb-2"></i>
                                    <h5>Energy Tracking</h5>
                                    <p class="text-muted">Monitor your energy patterns</p>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="text-center p-3">
                                    <i class="fas fa-tasks fa-2x text-success mb-2"></i>
                                    <h5>Task Management</h5>
                                    <p class="text-muted">Organize your priorities</p>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="text-center p-3">
                                    <i class="fas fa-chart-line fa-2x text-info mb-2"></i>
                                    <h5>Progress Analytics</h5>
                                    <p class="text-muted">Track your optimization</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="text-center mt-4">
                            <p class="lead">Welcome to your personalized optimization system!</p>
                            <button class="btn btn-primary btn-lg" onclick="startOptimization()">
                                <i class="fas fa-play me-2"></i>Start Optimization
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function startOptimization() {{
            alert('Starting your personalized optimization system!\\n\\nRun: python main.py');
        }}
        
        console.log('{project_name} Dashboard initialized');
    </script>
</body>
</html>"""
    
    def _generate_soulprint_summary(self, soulprint: Dict[str, Any]) -> str:
        """Generate 3-word soulprint summary"""
        
        # Extract key characteristics
        technical = soulprint.get('technical_comfort', 3)
        automation = soulprint.get('automation_preference', 3) 
        energy = soulprint.get('energy_pattern', 'balanced')
        
        descriptors = []
        
        # Technical descriptor
        if technical >= 4:
            descriptors.append('Technical')
        elif technical >= 2:
            descriptors.append('Balanced')
        else:
            descriptors.append('Simple')
        
        # Automation descriptor  
        if automation >= 4:
            descriptors.append('Automated')
        elif automation >= 2:
            descriptors.append('Guided')
        else:
            descriptors.append('Manual')
        
        # Energy descriptor
        energy_map = {
            'morning': 'Morning',
            'evening': 'Evening', 
            'balanced': 'Adaptive'
        }
        descriptors.append(energy_map.get(energy, 'Adaptive'))
        
        return ' • '.join(descriptors)
    
    def create_project_zip(self, project: Dict[str, Any], download_id: str) -> str:
        """Create ZIP file from generated project"""
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, project['project_name'])
            os.makedirs(project_dir)
            
            # Write all files
            for filename, content in project['files'].items():
                file_path = os.path.join(project_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Create ZIP file
            zip_path = os.path.join('processed', f"{download_id}.zip")
            os.makedirs('processed', exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
        
        return zip_path
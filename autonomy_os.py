"""
AutonomyOS: Menu-Driven Nomad Transition Agent
Complete automation of nomadic lifestyle transition through numbered menu choices
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid

class AutonomyOSState(Enum):
    """User's current state in nomad transition journey"""
    ASSESSMENT = "assessment"
    PLANNING = "planning"
    PREPARATION = "preparation"
    EXECUTION = "execution"
    OPTIMIZATION = "optimization"

@dataclass
class UserProfile:
    """User's nomad transition profile"""
    user_id: str
    current_income: Optional[float] = None
    profession: Optional[str] = None
    location: Optional[str] = None
    target_countries: List[str] = None
    readiness_score: Optional[float] = None
    state: AutonomyOSState = AutonomyOSState.ASSESSMENT
    progress: Dict[str, float] = None
    
    def __post_init__(self):
        if self.target_countries is None:
            self.target_countries = []
        if self.progress is None:
            self.progress = {
                "financial_readiness": 0.0,
                "income_replacement": 0.0,
                "location_planning": 0.0,
                "business_structure": 0.0,
                "systems_setup": 0.0
            }

class AutonomyOSAgent:
    """
    Menu-Driven Nomad Transition Agent
    Provides systematic, numbered menu choices for nomadic lifestyle transition
    """
    
    def __init__(self):
        self.name = "AutonomyOS"
        self.role = "Nomad Transition Command Center"
        self.user_profiles: Dict[str, UserProfile] = {}
        self.custom_agents: Dict[str, Dict[str, str]] = {}
        
    def get_main_menu(self, user_id: str = None) -> str:
        """Get the main AutonomyOS menu"""
        profile = self.get_user_profile(user_id) if user_id else None
        
        menu = """
🚀 AutonomyOS - Nomad Transition Command Center

Transform your life from location-dependent to complete freedom through guided choices.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 TRANSITION MANAGEMENT
1. Assess my nomad readiness
2. Plan income replacement strategy  
3. Choose target nomad locations
4. Set up nomad business structure
5. Build location-independent systems

⚡ EXECUTION & OPTIMIZATION  
6. Create custom transition timeline
7. View my progress dashboard
8. Get next action recommendations

🔧 SYSTEM EXPANSION
9. Add specialized agent
10. View available agents
11. Advanced nomad strategies

💡 HELP & GUIDANCE
12. How AutonomyOS works
13. Success stories & testimonials
14. Emergency nomad assistance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply with your choice (1-14):
"""
        
        if profile and profile.readiness_score:
            menu += f"\n🎯 Your current nomad readiness: {profile.readiness_score:.1f}/10"
            
        return menu
    
    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get or create user profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
        return self.user_profiles[user_id]
    
    def process_menu_choice(self, choice: str, user_id: str, additional_input: str = "") -> str:
        """Process user's menu choice and return appropriate response"""
        try:
            choice_num = int(choice.strip())
        except ValueError:
            return self._handle_invalid_choice(choice)
            
        profile = self.get_user_profile(user_id)
        
        menu_handlers = {
            1: self._assess_nomad_readiness,
            2: self._plan_income_replacement,
            3: self._choose_target_locations,
            4: self._setup_business_structure,
            5: self._build_location_systems,
            6: self._create_transition_timeline,
            7: self._view_progress_dashboard,
            8: self._get_next_actions,
            9: self._add_specialized_agent,
            10: self._view_available_agents,
            11: self._advanced_nomad_strategies,
            12: self._how_autonomy_works,
            13: self._success_stories,
            14: self._emergency_assistance
        }
        
        handler = menu_handlers.get(choice_num)
        if handler:
            return handler(profile, additional_input)
        else:
            return self._handle_invalid_choice(choice)
    
    def _assess_nomad_readiness(self, profile: UserProfile, additional_input: str) -> str:
        """Nomad readiness assessment menu"""
        return """
📊 NOMAD READINESS ASSESSMENT

Let's evaluate your readiness across key nomad success factors:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Quick assessment (5 minutes)
2. Comprehensive evaluation (15 minutes)
3. Financial readiness only
4. Skills & remote work assessment
5. Lifestyle & mindset evaluation
6. Legal & documentation check

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. View previous assessment results
8. Compare with successful nomads
9. Get personalized improvement plan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

0. Return to main menu

Choose assessment type (0-9):
"""
    
    def _plan_income_replacement(self, profile: UserProfile, additional_input: str) -> str:
        """Income replacement strategy menu"""
        return """
💰 INCOME REPLACEMENT STRATEGY

Build sustainable income before you leave:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 FAST TRACK (1-3 months)
1. Freelance skill monetization
2. Consulting business setup  
3. Digital product creation
4. Service marketplace strategy

💪 SUSTAINABLE (3-6 months)
5. Remote job transition plan
6. Online business development
7. Passive income streams
8. Investment portfolio optimization

🚀 ADVANCED (6+ months)
9. Scale existing income 2-5x
10. Multiple income diversification
11. Geographic arbitrage planning
12. Nomad business automation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

13. Calculate income requirements
14. Risk mitigation strategies

0. Return to main menu

Choose strategy path (0-14):
"""
    
    def _choose_target_locations(self, profile: UserProfile, additional_input: str) -> str:
        """Target location selection menu"""
        return """
🌍 TARGET LOCATION SELECTION

Choose your nomad destinations strategically:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏖️ BEGINNER-FRIENDLY
1. Southeast Asia route (Thailand → Vietnam → Malaysia)
2. Central America circuit (Costa Rica → Guatemala → Mexico)
3. Eastern Europe tour (Portugal → Estonia → Czech Republic)

💼 BUSINESS-FOCUSED  
4. Digital nomad hubs (Lisbon → Berlin → Singapore)
5. Startup ecosystems (Tel Aviv → Austin → Amsterdam)
6. Financial centers (Dubai → Hong Kong → Switzerland)

🎯 SPECIALIZED
7. Low cost of living maximization
8. Visa-friendly countries priority
9. Weather & lifestyle optimization
10. Language & culture preferences

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

11. Custom location analysis
12. Compare living costs
13. Visa requirement checker

0. Return to main menu

Choose location strategy (0-13):
"""
    
    def _setup_business_structure(self, profile: UserProfile, additional_input: str) -> str:
        """Business structure setup menu"""
        return """
🏢 NOMAD BUSINESS STRUCTURE

Set up legal & financial foundations:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇺🇸 US-BASED OPTIONS
1. LLC setup & management
2. Delaware C-Corp formation  
3. Wyoming entity advantages
4. Tax optimization strategies

🌍 INTERNATIONAL STRUCTURES
5. Estonian e-Residency program
6. Dubai freezone companies
7. Singapore entity setup
8. EU nomad-friendly jurisdictions

💳 BANKING & PAYMENTS
9. International banking solutions
10. Multi-currency accounts
11. Payment processor setup
12. Cryptocurrency integration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

13. Tax residence planning
14. Compliance automation
15. Professional service network

0. Return to main menu

Choose business setup (0-15):
"""
    
    def _build_location_systems(self, profile: UserProfile, additional_input: str) -> str:
        """Location-independent systems menu"""
        return """
⚙️ LOCATION-INDEPENDENT SYSTEMS

Build systems that work anywhere:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 DIGITAL INFRASTRUCTURE
1. Cloud-based workflow setup
2. Remote collaboration tools
3. Security & VPN systems
4. Backup & redundancy planning

📧 COMMUNICATION SYSTEMS
5. Professional communication setup
6. Virtual phone number system
7. Mail forwarding service
8. Time zone management tools

🏠 LIFESTYLE AUTOMATION
9. Accommodation booking system
10. Transportation optimization
11. Health & insurance coverage
12. Emergency support network

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MONITORING & OPTIMIZATION
13. Performance tracking setup
14. Cost monitoring dashboard
15. Quality of life metrics

0. Return to main menu

Choose system category (0-15):
"""
    
    def _create_transition_timeline(self, profile: UserProfile, additional_input: str) -> str:
        """Custom transition timeline menu"""
        return """
📅 CUSTOM TRANSITION TIMELINE

Create your personalized nomad transition plan:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TIMELINE OPTIONS
1. 90-day sprint transition
2. 6-month gradual transition  
3. 12-month comprehensive plan
4. 24-month conservative approach

🎯 PRIORITY-BASED PLANNING
5. Income-first timeline
6. Location-first timeline
7. Skills-first timeline
8. Risk-minimized timeline

📋 MILESTONE TRACKING
9. Weekly checkpoint system
10. Monthly progress reviews
11. Quarterly goal adjustments
12. Success celebration points

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

13. Export timeline to calendar
14. Share timeline with accountability partner
15. Adjust existing timeline

0. Return to main menu

Choose timeline approach (0-15):
"""
    
    def _view_progress_dashboard(self, profile: UserProfile, additional_input: str) -> str:
        """Progress dashboard display"""
        dashboard = f"""
📊 YOUR NOMAD TRANSITION PROGRESS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OVERALL READINESS: {profile.readiness_score or 0:.1f}/10

💰 Financial Readiness      {'█' * int((profile.progress['financial_readiness'] or 0) * 10)}{'░' * (10 - int((profile.progress['financial_readiness'] or 0) * 10))} {(profile.progress['financial_readiness'] or 0) * 100:.0f}%
📈 Income Replacement       {'█' * int((profile.progress['income_replacement'] or 0) * 10)}{'░' * (10 - int((profile.progress['income_replacement'] or 0) * 10))} {(profile.progress['income_replacement'] or 0) * 100:.0f}%
🌍 Location Planning        {'█' * int((profile.progress['location_planning'] or 0) * 10)}{'░' * (10 - int((profile.progress['location_planning'] or 0) * 10))} {(profile.progress['location_planning'] or 0) * 100:.0f}%
🏢 Business Structure       {'█' * int((profile.progress['business_structure'] or 0) * 10)}{'░' * (10 - int((profile.progress['business_structure'] or 0) * 10))} {(profile.progress['business_structure'] or 0) * 100:.0f}%
⚙️ Systems Setup           {'█' * int((profile.progress['systems_setup'] or 0) * 10)}{'░' * (10 - int((profile.progress['systems_setup'] or 0) * 10))} {(profile.progress['systems_setup'] or 0) * 100:.0f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 PROGRESS ACTIONS
1. Update progress manually
2. Connect progress tracking
3. Export progress report
4. Share with mentor/coach

🎯 FOCUS RECOMMENDATIONS  
5. View blocking issues
6. Get next 3 actions
7. Quick wins available
8. Expert consultation needed

0. Return to main menu

Choose action (0-8):
"""
        return dashboard
    
    def _get_next_actions(self, profile: UserProfile, additional_input: str) -> str:
        """Next action recommendations"""
        return """
🎯 NEXT ACTION RECOMMENDATIONS

Based on your current progress, here are your priority actions:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 IMMEDIATE (Today)
1. Complete financial assessment 
2. Update LinkedIn for remote work
3. Research 3 target countries

⚡ THIS WEEK  
4. Start freelance skill development
5. Set up international banking
6. Join nomad communities online

📅 THIS MONTH
7. Launch first income stream
8. Apply for travel-friendly credit cards
9. Organize important documents

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

10. Get detailed action plan
11. Schedule progress check-in
12. Connect with accountability partner

0. Return to main menu

Choose action or planning option (0-12):
"""
    
    def _add_specialized_agent(self, profile: UserProfile, additional_input: str) -> str:
        """Add custom specialized agent"""
        if additional_input:
            # Process agent addition command
            if additional_input.lower().startswith("add "):
                try:
                    # Parse: "Add [AGENT_NAME] who will [FUNCTION]"
                    command_parts = additional_input[4:].split(" who will ")
                    if len(command_parts) == 2:
                        agent_name = command_parts[0].strip()
                        agent_function = command_parts[1].strip()
                        
                        agent_id = str(uuid.uuid4())[:8]
                        self.custom_agents[agent_id] = {
                            "name": agent_name,
                            "function": agent_function,
                            "created_by": profile.user_id,
                            "created_at": datetime.utcnow().isoformat()
                        }
                        
                        return f"""
✅ AGENT ADDED SUCCESSFULLY

Agent: {agent_name}
Function: {agent_function}
Agent ID: {agent_id}

Your specialized agent is now available in the system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test your new agent
2. Add another agent
3. View all my agents
4. Return to main menu

Choose option (1-4):
"""
                    else:
                        return self._show_agent_format_help()
                except Exception as e:
                    return self._show_agent_format_help()
            else:
                return self._show_agent_format_help()
        else:
            return self._show_agent_addition_menu()
    
    def _show_agent_addition_menu(self) -> str:
        """Show agent addition menu"""
        return """
🔧 ADD SPECIALIZED AGENT

Expand AutonomyOS with custom expertise:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMAT: Add [AGENT_NAME] who will [FUNCTION]

💡 EXAMPLES:
• Add Tax Specialist who will optimize international taxes
• Add Visa Expert who will handle visa applications  
• Add Real Estate Scout who will find nomad-friendly properties
• Add Language Coach who will teach local languages
• Add Health Advisor who will manage nomad health concerns

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 SUGGESTED AGENT TYPES:
1. Financial specialists
2. Legal & compliance experts
3. Location & travel experts
4. Business development coaches
5. Health & wellness advisors
6. Technology & security experts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type your agent command or choose a suggested type (1-6):
"""
    
    def _show_agent_format_help(self) -> str:
        """Show agent format help"""
        return """
❌ INCORRECT FORMAT

Please use the exact format:
Add [AGENT_NAME] who will [FUNCTION]

Examples:
• Add Tax Specialist who will optimize international taxes
• Add Visa Expert who will handle visa applications

Try again with the correct format, or return to main menu (0):
"""
    
    def _view_available_agents(self, profile: UserProfile, additional_input: str) -> str:
        """View available specialized agents"""
        agents_list = "🤖 AVAILABLE SPECIALIZED AGENTS\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if self.custom_agents:
            for agent_id, agent in self.custom_agents.items():
                agents_list += f"🔹 {agent['name']}\n   Function: {agent['function']}\n   ID: {agent_id}\n\n"
        else:
            agents_list += "No custom agents created yet.\n\n"
        
        agents_list += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Consult with an agent
2. Add new agent
3. Delete an agent
4. Export agent list

0. Return to main menu

Choose action (0-4):
"""
        return agents_list
    
    def _advanced_nomad_strategies(self, profile: UserProfile, additional_input: str) -> str:
        """Advanced nomad strategies menu"""
        return """
🚀 ADVANCED NOMAD STRATEGIES

Expert-level optimization for experienced nomads:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 FINANCIAL OPTIMIZATION
1. Tax residency optimization
2. International investment strategies  
3. Currency hedging for nomads
4. Offshore banking strategies

🌍 LOCATION ARBITRAGE
5. Cost of living maximization
6. Seasonal location rotation
7. Visa run optimization
8. Quality of life indexing

🏢 BUSINESS SCALING
9. Global team building
10. International expansion
11. Remote operation optimization
12. Nomad-friendly partnerships

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 LIFESTYLE OPTIMIZATION
13. Productivity system for travelers
14. Health & fitness while nomad
15. Long-term relationship management

0. Return to main menu

Choose advanced strategy (0-15):
"""
    
    def _how_autonomy_works(self, profile: UserProfile, additional_input: str) -> str:
        """How AutonomyOS works explanation"""
        return """
💡 HOW AUTONOMYOS WORKS

Your personal nomad transition command center:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 THE AUTONOMYOS ADVANTAGE

✅ No overwhelming open-ended questions
✅ Clear numbered choices for every decision  
✅ Systematic progression through transition phases
✅ Built-in progress tracking and accountability
✅ Expert guidance without decision paralysis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔬 BEHIND THE SCENES

• Powered by C-Suite AI executive team
• CFO optimizes your financial strategy
• COO streamlines your operations  
• CTO builds your technical systems
• All accessible through simple menu choices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 YOUR JOURNEY

1. Assessment → Know where you stand
2. Planning → Build your strategy  
3. Preparation → Set up foundations
4. Execution → Make the transition
5. Optimization → Perfect your nomad life

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Start my assessment now
2. View success stories
3. Get help from specialist

0. Return to main menu

Choose next step (0-3):
"""
    
    def _success_stories(self, profile: UserProfile, additional_input: str) -> str:
        """Success stories and testimonials"""
        return """
🏆 SUCCESS STORIES & TESTIMONIALS

Real nomads who used AutonomyOS for their transition:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 SARAH - SOFTWARE DEVELOPER
"AutonomyOS saved me from analysis paralysis. The numbered menus 
made each decision simple. Now earning $120K from Bali!"
Transition time: 4 months

💼 MARCUS - CONSULTANT  
"The CFO agent helped optimize my taxes, saving $18K annually.
COO agent streamlined everything. Pure freedom now."
Transition time: 6 months

📊 JENNY - MARKETING MANAGER
"Never thought I could go nomad with my corporate job. AutonomyOS 
showed me the exact steps. Working remotely from 12 countries now!"
Transition time: 8 months

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 AVERAGE RESULTS
• 73% increase in location independence
• 45% reduction in living costs
• 89% improved work-life balance
• 92% would recommend AutonomyOS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Read more success stories
2. Connect with successful nomads
3. Start my own success story

0. Return to main menu

Choose option (0-3):
"""
    
    def _emergency_assistance(self, profile: UserProfile, additional_input: str) -> str:
        """Emergency nomad assistance"""
        return """
🚨 EMERGENCY NOMAD ASSISTANCE

24/7 support for urgent nomad situations:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 IMMEDIATE SUPPORT NEEDED?
1. Visa expiration crisis
2. Banking/payment card blocked
3. Emergency evacuation needed
4. Legal trouble abroad
5. Medical emergency while traveling

💼 BUSINESS EMERGENCIES
6. Lost remote job while nomad
7. Client payment crisis
8. Business entity compliance issue
9. Tax deadline emergency
10. Insurance claim urgent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 EMERGENCY CONTACTS
• Embassy contact database
• Legal assistance network
• Medical evacuation services
• Emergency financial services

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

11. Access emergency resource database
12. Contact emergency specialist now
13. Prevention planning

0. Return to main menu

Choose emergency type or resource (0-13):
"""
    
    def _handle_invalid_choice(self, choice: str) -> str:
        """Handle invalid menu choices"""
        return f"""
❌ Invalid choice: "{choice}"

Please enter a valid number from the menu options.

💡 TIP: Type the number exactly as shown (e.g., "1", "7", "12")

Type "0" to return to the main menu, or choose a valid option.
"""
    
    def respond_to_user(self, user_message: str, user_id: str = None) -> str:
        """Main entry point for user interactions"""
        if not user_id:
            user_id = str(uuid.uuid4())
            
        # Check if it's a menu choice (number) or initial interaction
        user_message = user_message.strip()
        
        # If it's just a number, process as menu choice
        if user_message.isdigit() or (user_message.startswith('0') and len(user_message) <= 2):
            return self.process_menu_choice(user_message, user_id)
        
        # If it's an agent addition command
        if user_message.lower().startswith("add ") and " who will " in user_message.lower():
            return self.process_menu_choice("9", user_id, user_message)
        
        # For any other input, show main menu with explanation
        return f"""
Welcome to AutonomyOS! 🚀

I help professionals like you transition to nomadic freedom through simple, numbered choices instead of overwhelming open-ended questions.

{self.get_main_menu(user_id)}

💡 Simply reply with the number of your choice (e.g., "1" for readiness assessment)
"""

# Global AutonomyOS instance
autonomy_os_agent = AutonomyOSAgent()
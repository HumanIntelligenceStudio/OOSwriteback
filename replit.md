# Multi-Agent AI Conversation System

## Overview

This is a Flask-based web application that implements a multi-agent AI conversation system. The application allows users to interact with different AI agents, each with specialized roles and capabilities. The system uses OpenAI's GPT-3.5-turbo model to power the AI agents and maintains conversation history in memory.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple Flask web application architecture with the following key characteristics:

### Frontend Architecture
- **Framework**: Vanilla HTML/CSS/JavaScript with Bootstrap for styling
- **UI Components**: Single-page application with dynamic content updates
- **Styling**: Bootstrap Agent Dark Theme with custom CSS animations
- **Icons**: Font Awesome for visual elements
- **Navigation**: Tabbed interface for new conversations vs. conversation history
- **Interactive Features**: Keyboard shortcuts, search with highlighting, visual feedback

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **API Structure**: RESTful endpoints for agent interactions
- **Session Management**: Flask sessions for user state management
- **Logging**: Python logging module for debugging and monitoring

### Data Storage
- **Primary Storage**: PostgreSQL database for persistent conversation history
- **Database Models**: Conversation and ConversationEntry models using SQLAlchemy
- **Session Storage**: Flask session cookies for user identification
- **Persistent Data**: All conversations and agent responses are stored permanently

## Key Components

### Agent System
- **Base Agent Class**: Extensible class structure for different AI agent types
- **Agent Specialization**: Each agent has a unique name, role, and system prompt
- **OpenAI Integration**: Uses OpenAI's chat completions API for response generation
- **Conversation Context**: Maintains conversation history for context-aware responses

### Core Functionality
- **Multi-Agent Support**: Framework supports multiple specialized AI agents
- **Conversation Management**: Tracks and maintains conversation history in PostgreSQL database
- **Real-time Interaction**: AJAX-based communication for seamless user experience
- **Error Handling**: Comprehensive error handling for API failures and edge cases
- **Conversation History**: Browse and load previous conversations with persistent storage
- **Search Functionality**: Full-text search through conversation history with highlighted results
- **Export Capability**: Download conversations as formatted text files
- **Database Persistence**: All conversations survive server restarts and are permanently stored

## Data Flow

1. **User Input**: User submits input through the web interface
2. **Session Management**: Flask creates or retrieves existing session
3. **Agent Selection**: System determines which agent(s) should respond
4. **Context Preparation**: Conversation history is prepared for the AI model
5. **OpenAI API Call**: Request sent to OpenAI with system prompt and context
6. **Response Processing**: AI response is processed and formatted
7. **Storage Update**: Conversation history is updated in memory
8. **UI Update**: Frontend is updated with the new response

## External Dependencies

### Core Dependencies
- **Flask**: Web framework for Python
- **Flask-SQLAlchemy**: Database ORM for PostgreSQL integration
- **Flask-Limiter**: Rate limiting for API endpoints
- **Flask-WTF**: CSRF protection and form handling
- **OpenAI Python Client**: Official OpenAI API client library
- **PostgreSQL**: Database for persistent conversation storage
- **Bootstrap**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **Validators**: Input validation utilities

### API Dependencies
- **OpenAI API**: GPT-3.5-turbo model for AI agent responses
- **Model Configuration**: 500 max tokens, 0.7 temperature for balanced creativity

## Deployment Strategy

### Environment Configuration
- **Environment Variables**: 
  - `OPENAI_API_KEY`: Required for OpenAI API access
  - `SESSION_SECRET`: Flask session encryption key (defaults to dev key)

### Runtime Requirements
- **Python Environment**: Requires Python with Flask and OpenAI packages
- **Memory Usage**: Conversation data stored in memory (not persistent)
- **API Limits**: Subject to OpenAI API rate limits and usage quotas

### Scalability Considerations
- **Database Storage**: PostgreSQL provides persistent, scalable conversation storage
- **Session Dependency**: Uses Flask sessions for user identification
- **Database Design**: Normalized schema with Conversation and ConversationEntry tables

### Security Considerations
- **API Key Management**: OpenAI API key stored as environment variable
- **Session Security**: Flask session cookies with HTTPOnly, Secure, SameSite attributes
- **Input Validation**: Comprehensive input sanitization and validation
- **Rate Limiting**: IP-based rate limiting on all API endpoints
- **Security Headers**: XSS protection, content type options, frame options, HSTS
- **Error Handling**: Generic error messages to prevent information disclosure
- **CSRF Protection**: Flask-WTF CSRF protection for forms
- **Request Size Limits**: Maximum request size enforcement

## Development Notes

- The application is designed for development/demo purposes with in-memory storage
- Production deployment would require persistent storage for conversation history
- The agent system is designed to be extensible for adding new specialized agents
- Error handling includes logging for debugging and monitoring
- The UI uses animations and loading indicators for better user experience
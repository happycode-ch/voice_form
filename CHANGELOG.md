# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2023-12-05

### Added

- Initial project scaffolding
- Backend API structure with FastAPI
  - Transcription endpoint
  - Summarization endpoint
  - Health check endpoint
- Database models for questionnaires and responses
- OpenAI Whisper integration for voice transcription
- OpenAI GPT integration for response summarization
- Frontend React application
  - Audio recording component
  - Question and response interface
  - Multilingual support (EN/DE)
- Docker and docker-compose configuration
- Project documentation
  - README
  - CHANGELOG

### Todo

- Add tests for backend APIs
- Implement authentication and authorization
- Add PDF export functionality
- Create admin dashboard for questionnaire management 
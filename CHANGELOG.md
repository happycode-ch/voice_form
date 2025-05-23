# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- CHANGELOG_STANDARD_VERSION: 1 -->

## [Unreleased]

### Added
- Add Postgres-backed transcription storage with Alembic migrations #minor
- Add TranscriptionRepository for database operations #minor
- Add end-to-end testing guide for transcription integration #patch
- Add centralized configuration system with environment validation #minor
- Add comprehensive health check system for container monitoring #minor
  - Basic health endpoint (/api/health/)
  - Detailed system status endpoint (/api/health/detailed)
  - OpenAI API verification endpoint (/api/health/openai)
- Add container-aware database connection retry logic #minor
- Add container-specific documentation and setup guide #patch

### Changed
- Replace mock transcription with configurable OpenAI Whisper integration #minor
- Update Pydantic schema to use from_attributes instead of deprecated orm_mode #patch
- Enhance application startup with container dependency checking #minor
- Modernize service clients to use centralized configuration #minor
- Update database session management for containerized environment #minor

### Fixed
- Fix trailing-slash redirect loop in questionnaire navigation #patch
- Fix content-type validation for audio file uploads #patch
- Fix SQLAlchemy syntax for modern versions in health checks #patch

## [0.1.2] - 2024-05-22

### Added
- Basic React application structure in frontend
  - index.html template
  - index.tsx entry point
  - App component integration

### Changed
- Removed obsolete version field from docker-compose.yml (Compose v2 compatibility)
- Changed PostgreSQL external port to 5433 to avoid conflicts with local instances
- Modified frontend Dockerfile to use npm install instead of npm ci
- Enabled mock services for local development (transcription and summarization)

### Fixed
- Frontend build issues by adding missing React entry points
- Port conflict with local PostgreSQL instance
- Package installation issues in frontend container

## [0.1.1] - 2024-05-16

### Added
- Python virtual environment setup
- Project-specific Python version (3.11.8) via pyenv
- Activation script (activate.sh) for easier environment management

### Changed
- Updated Python version from 3.13.3 to 3.11.8 for better package compatibility
- Fixed dependency installation issues with pydantic-core

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
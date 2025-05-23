# Environment Setup Guide (Containerized Deployment)

## Quick Start

### 1. Create Environment File

Copy and paste the following into `backend/.env`:

```bash
# =============================================================================
# VoiceForm Application Configuration (Docker Container)
# =============================================================================

# Database Configuration (Container Networking)
DATABASE_URL=postgresql://postgres:postgres@db:5432/voiceform

# Container Database Startup Settings
DATABASE_CONNECTION_RETRIES=5
DATABASE_RETRY_DELAY_SECONDS=2
CONTAINER_STARTUP_TIMEOUT_SECONDS=60

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Mock Mode Configuration (for development/testing)
USE_MOCK_TRANSCRIPTION=true
USE_MOCK_SUMMARIZATION=true

# Logging Configuration
LOG_LEVEL=INFO

# Application Settings
ENVIRONMENT=development
DEBUG=true

# Security & Performance
MAX_AUDIO_FILE_SIZE_MB=25
MAX_AUDIO_DURATION_SECONDS=300
REQUEST_TIMEOUT_SECONDS=30

# API Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### 2. Container-Specific Setup

**This is a fully containerized application using Docker Compose:**

- **Backend**: FastAPI container (`backend/`)
- **Frontend**: React container (`frontend/`) 
- **Database**: PostgreSQL container (`db`)
- **Networking**: All services connected via `voiceform-network`

**Start the containers:**
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend

# Check container status
docker compose ps
```

### 3. Development vs Production Configuration

**For Development (Mock Mode - Default):**
- Keep `USE_MOCK_TRANSCRIPTION=true` and `USE_MOCK_SUMMARIZATION=true`
- No OpenAI API key required
- All features work with mock responses
- Database retries handle container startup timing

**For Production with Real OpenAI:**
1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY=sk-your-actual-key-here`
3. Set `USE_MOCK_TRANSCRIPTION=false` and `USE_MOCK_SUMMARIZATION=false`
4. Set `ENVIRONMENT=production` and `DEBUG=false`
5. Adjust container resource limits in docker-compose.yml

### 4. Verify Container Setup

After creating the .env file and starting containers:

```bash
# Check all container health
curl http://localhost:8000/api/health/detailed

# Test OpenAI API key (if configured)
curl http://localhost:8000/api/health/openai

# View container logs
docker compose logs backend
docker compose logs db
```

## Environment Variables Reference

### Core Configuration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | postgresql://...@db:5432/... | PostgreSQL connection (uses container networking) |
| `OPENAI_API_KEY` | Conditional | - | Required if mock mode disabled |
| `OPENAI_MODEL` | No | gpt-3.5-turbo | OpenAI model for summarization |

### Container-Specific Settings
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_CONNECTION_RETRIES` | No | 5 | Retries for DB container startup |
| `DATABASE_RETRY_DELAY_SECONDS` | No | 2 | Delay between DB connection retries |
| `CONTAINER_STARTUP_TIMEOUT_SECONDS` | No | 60 | Max wait time for container dependencies |

### Mock Mode & Application
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `USE_MOCK_TRANSCRIPTION` | No | false | Enable mock transcription |
| `USE_MOCK_SUMMARIZATION` | No | false | Enable mock summarization |
| `ENVIRONMENT` | No | development | Application environment |
| `DEBUG` | No | false | Enable debug mode |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Security & Performance
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MAX_AUDIO_FILE_SIZE_MB` | No | 25 | Maximum audio file size |
| `MAX_AUDIO_DURATION_SECONDS` | No | 300 | Maximum audio duration (5 minutes) |
| `REQUEST_TIMEOUT_SECONDS` | No | 30 | API request timeout |
| `RATE_LIMIT_PER_MINUTE` | No | 60 | API rate limit per minute |

## Container Architecture

### Service Communication
- **Frontend** → **Backend**: HTTP requests via container networking
- **Backend** → **Database**: PostgreSQL connection via `db:5432`
- **Backend** → **OpenAI**: External API calls (when not in mock mode)

### Port Mapping
- **Frontend**: `localhost:3000` → `container:80`
- **Backend**: `localhost:8000` → `container:8000`
- **Database**: `localhost:5433` → `container:5432` (external access)

### Volume Mounting
- `./backend:/app` - Backend code mounted for development
- `postgres-data:/var/lib/postgresql/data` - Database persistence

## Configuration Validation

The containerized application validates configuration on startup and will:

- ✅ Auto-enable mock mode if OpenAI key is missing in development
- 🔄 Retry database connections during container startup
- ❌ Refuse to start if critical configuration is missing in production
- ⚠️ Log warnings for configuration issues and continue with degraded functionality
- 📊 Display configuration summary including container-specific settings

## Troubleshooting

### Container Startup Issues

**"Database connection failed"**
- Check if database container is running: `docker compose ps`
- View database logs: `docker compose logs db`
- Increase retry settings: `DATABASE_CONNECTION_RETRIES=10`

**"Configuration validation failed"**
- Verify `.env` file exists in `backend/.env`
- Check docker-compose.yml includes `env_file: - ./backend/.env`
- Restart containers: `docker compose down && docker compose up -d`

**Container networking issues**
- Ensure all services are on the same network: `docker network ls`
- Check container connectivity: `docker compose exec backend ping db`

### "OpenAI API key verification failed"
- Verify your API key is correct and active
- Check your OpenAI account has sufficient credits
- Test from container: `docker compose exec backend curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models`

### Mock mode not working
- Ensure `USE_MOCK_TRANSCRIPTION=true` and `USE_MOCK_SUMMARIZATION=true`
- Check container logs: `docker compose logs backend`
- Restart backend container: `docker compose restart backend`

### Performance Issues
- Monitor container resources: `docker stats`
- Adjust memory limits in docker-compose.yml
- Check database connection pool settings in logs

## Container Management

### Development Workflow
```bash
# Start development environment
docker compose up -d

# View real-time logs
docker compose logs -f backend

# Rebuild after code changes
docker compose build backend
docker compose up -d backend

# Reset everything
docker compose down -v
docker compose up -d
```

### Production Deployment
```bash
# Set production environment
echo "ENVIRONMENT=production" >> backend/.env
echo "DEBUG=false" >> backend/.env

# Start with production settings
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Next Steps

After completing containerized setup:

1. **Test the API**: Visit http://localhost:8000/docs for interactive documentation
2. **Health Checks**: Use http://localhost:8000/api/health/detailed for system status
3. **Frontend**: Access the UI at http://localhost:3000
4. **Container Monitoring**: Set up logging and monitoring for production
5. **Transition to Live**: Update configuration when ready for real OpenAI integration 
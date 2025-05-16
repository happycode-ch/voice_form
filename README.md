# VoiceForm AI

A voice-first, multilingual intake tool for structured questionnaires

## 🎯 Overview

VoiceForm AI is a portfolio-grade proof-of-concept for a voice-first, multilingual intake tool. It demonstrates the capabilities of modern AI in transcribing, analyzing, and summarizing voice responses in a structured questionnaire format.

This project showcases:

- Voice recording and processing in the browser
- Real-time transcription using OpenAI's Whisper API
- Contextual response summarization using GPT
- Multilingual support (English/German)
- Structured data output for clinical or business analysis
- Privacy-conscious data handling

## 🔧 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (TypeScript)
- **Transcription**: OpenAI Whisper 
- **Summarization**: OpenAI GPT
- **Database**: PostgreSQL (via SQLAlchemy)
- **Infrastructure**: Docker + docker-compose

## 🚀 Getting Started

### Prerequisites

- Docker and docker-compose
- OpenAI API Key (for production use)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/username/voiceform-ai.git
   cd voiceform-ai
   ```

2. Create environment file:
   ```
   cp backend/.env.example backend/.env
   ```

3. Add your OpenAI API key to `backend/.env` if you want to use real transcription and summarization:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Build and start the containers:
   ```
   docker-compose up --build
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development Mode

For a development environment with hot-reloading:

```
# Start the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# In another terminal, start the frontend
cd frontend
npm install
npm start
```

## 🔍 Project Structure

```
voiceform_ai/
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── main.py        # Application entry point
│   │   ├── api/           # API endpoints
│   │   ├── db/            # Database models and session
│   │   ├── services/      # External services (Whisper, OpenAI)
│   │   └── utils/         # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/              # React application
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   └── App.tsx        # Main application component
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml     # Service orchestration
└── README.md
```

## 📋 Features

- **Voice Recording**: In-browser voice capture with visual feedback
- **Multilingual Support**: Toggle between English and German interfaces
- **Real-time Transcription**: Convert speech to text
- **AI-powered Analysis**: Summarize and extract key information from responses
- **Structured Output**: Classification based on question type (yes/no, Likert, open-ended)
- **Privacy Controls**: Mock secure transmission and data vaporization

## 🔒 Privacy & Compliance

This project simulates privacy-conscious data handling for healthcare and other sensitive domains. In a production environment, you would need to implement:

- Proper encryption for data at rest and in transit
- Compliance with regional regulations (GDPR, HIPAA, etc.)
- Secure authentication and authorization
- Audit logging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for their Whisper and GPT APIs
- FastAPI and React communities for their excellent documentation 
# VoiceForm AI – Cursor Agent System Prompt

## 🎯 Project Purpose

This project, **VoiceForm AI**, is a portfolio-grade proof-of-concept for a voice-first, multilingual intake tool. It is designed to showcase the developer’s ability to:

* Build a modular, full-stack AI application using modern frameworks
* Simulate privacy-conscious intake logic for sensitive domains (like Swiss healthcare)
* Demonstrate language handling, transcription, and summarization pipelines
* Deliver a complete, working demo project suitable for recruiters or clients

The project does **not** aim to be a production-level healthcare solution. Compliance logic is simulated and simplified to reduce build complexity.

The entire system is designed to:

* Interpret developer requests (e.g. "create a 10-question intake")
* Generate and classify questions (yes/no, Likert, open-ended)
* Send tokenized session links to users
* Record and transcribe user voice input
* Analyze responses against question intent
* Output a structured and optionally translated PDF summary
* Simulate secure transmission + vaporization of session data

## 📋 Scenario & Intended Flow

VoiceForm AI is not a generic voice form. It is a structured, **AI-powered questionnaire** tool, where each step presents a defined question, and the respondent **answers naturally via voice**.

* The system transcribes the audio input (Whisper)
* Then summarizes or interprets it using an LLM (OpenAI GPT)
* Then structures the response into a consistent, predefined schema (e.g., JSON field)

The intake is sequential and voice-first:

* Each question appears on screen
* The user answers verbally
* The AI processes, interprets, and moves to the next question

This is meant to simulate a **sleep clinic intake** workflow but should be abstract enough to extend to other industries. The entire project showcases:

* Conversational AI logic
* UX design for voice questionnaires
* Structured data output for clinicians or case managers

## 🔧 Tech Stack

* **Backend**: FastAPI (async-ready, modular routing)
* **Frontend**: React (using MediaRecorder API for in-browser voice capture)
* **Transcription**: Whisper (OpenAI API or local model stub)
* **Summarization**: GPT (OpenAI structured prompt interface)
* **Database**: PostgreSQL (via SQLAlchemy)
* **Environment**: pip + venv + `python-dotenv`
* **Infrastructure**: Docker + docker-compose
* **Testing**: `pytest` (scaffolded)
* **Docs**: `README.md`, `CHANGELOG.md`

## 📂 Suggested File Structure

```
voiceform_ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── transcribe.py
│   │   │   ├── summarize.py
│   │   │   └── routes.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── services/
│   │   │   ├── whisper_client.py
│   │   │   └── openai_client.py
│   │   └── utils/
│   │       └── logger.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── AudioRecorder.tsx
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
├── CHANGELOG.md
└── tests/
    ├── backend/
    └── frontend/
```

## 🔒 Compliance & Privacy Simulation

* Simulate GDPR/Swiss data handling
* Do not store audio or outputs unless explicitly configured
* Stub secure transmission logic for future implementation
* Mark any real-world compliance needs with `# TODO: PRODUCTION COMPLIANCE`
* Support vaporization logic: auto-delete after delivery or PDF export
* Simulate encrypted delivery (e.g., expiring download link or trusted mail provider)

## 🌍 Language Support

* Scaffold language toggle for EN/DE
* Modular translation logic (e.g. `translator.py` or i18n stub)
* All input/output fields should support localization

## 🧠 Cursor Agent Behavior

* Scaffold full folder structure with clear modularity
* Write concise, commented code blocks
* Use AI to generate testable modules (`/transcribe`, `/summarize`, etc.)
* After each session, update or append to `CHANGELOG.md`
* Suggest next actions at the end of each dev round
* Never hallucinate external services — use stubs or placeholders
* Avoid overbuilding — this is a **focused, resume-grade** project
* **Reduce complexity whenever possible**

  * Prefer working scaffolds over overengineered abstractions
  * Prioritize features that demonstrate value and flow

---

> 📌 This system prompt may be reused across agents or included in `project_notes.md` as a high-level dev briefing.

---

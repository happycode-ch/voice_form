Below is a practical, “recipe-style” roadmap you can follow when coaching ChatGPT (or another LLM-powered agent) to build **VoiceForm AI** from scratch all the way to demo-ready delivery.
For each stage I’ve added:

* **Outcome** – what you should have before moving on.
* **Ask the AI** – a concise, copy-pastable prompt (tweak as needed).
* **Developer notes** – caveats, compliance reminders, or manual tasks.

All guidance is drawn directly from the system brief in `voice_form.md`.&#x20;

---

### 1  · Project Kick-off & Repo Bootstrap

**Outcome**: Initialized Git repo with the folder skeleton listed in the brief.

| Ask the AI                                                                                                                            | Developer notes                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| “Scaffold the full `voiceform_ai/` file tree exactly as described, including placeholder files with docstrings and `# TODO` markers.” | Run `git init` first. Commit the scaffold immediately so diffs stay clean. |

---

### 2  · Environment & Toolchain

**Outcome**: Working Python + Node toolchains, Dockerfiles, and `docker-compose.yml`.

| Ask the AI                                                                                                                                                 | Developer notes                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| “Generate `backend/Dockerfile`, `frontend/Dockerfile`, and `docker-compose.yml` that wire FastAPI, React, Postgres and a reverse proxy. Keep images slim.” | Fill in real ports, image tags, and network names before build. Add `.env.example` for secret placeholders. |

---

### 3  · Backend Entry Point (`main.py`)

**Outcome**: FastAPI app that boots, serves `/health`, and mounts versioned API router stubs.

| Ask the AI                                                                                                     | Developer notes                              |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| “Create `backend/app/main.py` that instantiates FastAPI with CORS, logging middleware, and a `/health` route.” | Verify with `uvicorn app.main:app --reload`. |

---

### 4  · Database Models & Session Logic

**Outcome**: SQLAlchemy model for `Session`, `Question`, `Answer`.

| Ask the AI                                                                                                                                                  | Developer notes                   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| “Write `backend/app/db/models.py` with an abstract `Base`, plus `Session`, `Question`, `Answer` (UUID PKs). Add `created_at`, `vaporize_after` timestamps.” | Use Alembic later for migrations. |

---

### 5  · Service Stubs (Whisper & GPT)

**Outcome**: Thin wrappers around external APIs, easily mocked in tests.

| Ask the AI                                                                                                                                                                                                                                         | Developer notes                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| “Generate `services/whisper_client.py` and `services/openai_client.py` with async methods `transcribe()` and `summarize()` that accept `audio_bytes` / `text` and return JSON. Include a flag to return fake data when `settings.MODE == "DEV"`. ” | Add `# TODO: PRODUCTION COMPLIANCE` above real calls. |

---

### 6  · Core API Routes

**Outcome**: Functional endpoints:

* `POST /transcribe` → text
* `POST /summarize` → JSON summary
* `POST /answer` → saves structured answer and advances questionnaire

| Ask the AI                                                                                          | Developer notes             |
| --------------------------------------------------------------------------------------------------- | --------------------------- |
| “Implement `transcribe.py`, `summarize.py`, and `routes.py` with Pydantic request/response models.” | Unit-test with dummy audio. |

---

### 7  · Frontend Voice Recorder

**Outcome**: React component that records, POSTs audio, displays transcription.

| Ask the AI                                                                                                                                  | Developer notes                    |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| “Write `AudioRecorder.tsx` using the MediaRecorder API, with states: idle → recording → uploading → done. Return WAV/FLAC blob to backend.” | Keep UI minimal; styling can wait. |

---

### 8  · Questionnaire Flow (UX)

**Outcome**: Sequential question screen with language toggle (EN/DE).

| Ask the AI                                                                                                                     | Developer notes                                                  |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| “Create `QuestionFlow` React component that fetches the next question, renders it, records the answer, then fetches the next.” | Store current session ID in `localStorage`; purge when finished. |

---

### 9  · Privacy & Vaporization Logic

**Outcome**: Automatic deletion scheduler or `cron` job to purge data after PDF delivery.

| Ask the AI                                                                                                              | Developer notes                             |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| “Add a background task in FastAPI (`StartupEvent`) that checks `session.vaporize_after < now()` and hard-deletes rows.” | Mark in code: `# TODO: real secure delete`. |

---

### 10  · PDF Summary Export

**Outcome**: Endpoint `GET /session/{id}/report.pdf` returning structured summary.

| Ask the AI                                                                                                                                                 | Developer notes                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| “Generate a `report_service.py` that converts session data into a simple PDF (use `reportlab` or `weasyprint`). Expose route. Include localized headings.” | Consider streaming the PDF to avoid large memory usage. |

---

### 11  · Internationalization

**Outcome**: Simple i18n hook front & back; fallback English.

| Ask the AI                                                                                       | Developer notes                         |
| ------------------------------------------------------------------------------------------------ | --------------------------------------- |
| “Add a `translator.py` stub with `translate(text, target_lang)` returning the same text in DEV.” | Wire a language selector in the navbar. |

---

### 12  · Testing & CI

**Outcome**: `pytest` suite, GitHub Actions workflow.

| Ask the AI                                                                                | Developer notes                                |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------- |
| “Scaffold unit tests for each service using dependency injection to fake external calls.” | Minimum: health route, DB CRUD, service stubs. |

---

### 13  · Docker Compose Up & Demo Data

**Outcome**: One-command spin-up and clickable demo.

| Ask the AI                                                                                                             | Developer notes                      |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| “Write a Makefile task `demo` that runs `docker compose up --build`, seeds 3 sample questions, and opens the browser.” | Verify cross-platform path handling. |

---

### 14  · Changelog Discipline

**Outcome**: An updated `CHANGELOG.md` per feature.

| Ask the AI                                                                            | Developer notes                        |
| ------------------------------------------------------------------------------------- | -------------------------------------- |
| “Append an Unreleased section in `CHANGELOG.md` after you finish each major feature.” | Conventional Commits style works well. |

---

### 15  · Pitch & Documentation Polish

**Outcome**: README badges, architecture diagram, short Loom video link.

| Ask the AI                                                                                      | Developer notes                                   |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| “Draft the final `README.md` sections: Quick Start, Architecture, Privacy Simulation, Roadmap.” | Include a GIF or screenshot of the questionnaire. |

---

## How to Work With This List

1. **Tackle one row at a time.** Paste the “Ask the AI” text (edited with specifics) into ChatGPT.
2. **Review the output quickly**, fix naming or path errors, then commit.
3. **Run tests or docker compose early** to catch integration bugs before piling on features.
4. After every stage, **update `CHANGELOG.md`** and commit with a clear message.
5. **Iterate** – if the AI produces over-engineered code, remind it of the “Reduce complexity” rule from the brief.&#x20;

With this playbook you can steer the AI through a repeatable development cadence while ensuring every requirement in the original prompt is fulfilled. Happy building!

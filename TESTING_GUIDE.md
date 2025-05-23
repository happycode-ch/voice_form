"""
File: TESTING_GUIDE.md
Description: End-to-end testing guide for VoiceForm Postgres transcription integration.
AI-hints:
- Covers both mock and live transcription testing
- Provides database verification steps
- Includes troubleshooting common issues
"""

# VoiceForm Transcription Integration Testing Guide

## 🏁 Quick Status Check

✅ **Prerequisites Verified:**
- Database: `transcriptions` table exists with correct schema
- Backend: Running on http://localhost:8000 with OpenAI dependency
- Frontend: Running on http://localhost:3000
- Migration: Alembic revision `01` applied successfully

## 🧪 Testing Approaches

### 1. Browser End-to-End Testing (Recommended)

**Access the application:**
```bash
# Open in browser
http://localhost:3000
```

**Testing steps:**
1. Navigate through the questionnaire flow
2. When prompted for audio input, use your microphone or upload an audio file
3. Submit the audio for transcription
4. Verify the transcription appears in the UI
5. Check that the response includes a database ID

### 2. Database Persistence Verification

**Check stored transcriptions:**
```bash
docker compose exec db psql -U postgres -d voiceform -c "SELECT * FROM transcriptions ORDER BY id DESC LIMIT 5;"
```

**Expected output:**
```
 id | question_id |                    text                    |         created_at
----+-------------+--------------------------------------------+----------------------------
  1 |           1 | [Transcribed text content here]           | 2025-05-23 06:30:15.123+00
```

### 3. API Direct Testing

**Mock mode testing:**
```bash
# Ensure mock mode is enabled
docker compose exec backend bash -c "grep USE_MOCK_TRANSCRIPTION /app/.env"

# Test with curl (if needed)
curl -X POST "http://localhost:8000/api/transcribe/?qid=1" \
  -F "file=@test.wav;type=audio/wav"
```

## 🔧 Environment Configuration

### For Testing Without OpenAI API Key (Mock Mode)
```bash
# Enable mock transcription
docker compose exec backend bash -c "echo 'USE_MOCK_TRANSCRIPTION=true' >> /app/.env"
docker compose restart backend
```

### For Live OpenAI Testing
```bash
# Set your OpenAI API key
docker compose exec backend bash -c "echo 'OPENAI_API_KEY=your_key_here' >> /app/.env"
docker compose exec backend bash -c "echo 'USE_MOCK_TRANSCRIPTION=false' >> /app/.env"
docker compose restart backend
```

## 📊 Verification Checklist

- [ ] Frontend loads at http://localhost:3000
- [ ] Audio recording/upload interface works
- [ ] Transcription request completes without errors
- [ ] Response includes database ID (`id` field)
- [ ] Transcription text appears in UI
- [ ] Database entry created (verify with SQL query)
- [ ] `created_at` timestamp is recent
- [ ] `question_id` matches the current question

## 🚨 Troubleshooting

**Backend 500 errors:**
- Check `docker compose logs backend` for Python exceptions
- Verify database connection
- Confirm OpenAI API key if using live mode

**Content-Type errors:**
- Frontend should set proper MIME types automatically
- For manual testing, use `audio/wav`, `audio/mp3`, etc.

**Database connection issues:**
- Verify migration applied: `docker compose exec backend alembic current`
- Check database connectivity: `docker compose exec db psql -U postgres -d voiceform -c "\dt"`

## 🎯 Success Criteria

✅ **Integration is working when:**
1. Audio transcription completes successfully
2. Database entry created with auto-incremented ID
3. API response includes `TranscriptionSchema` fields:
   - `id` (database primary key)
   - `question_id` (matches request)
   - `text` (transcription result)
   - `created_at` (automatic timestamp)

---

**Next Steps:** After successful testing, commit final changes and update `CHANGELOG.md` 
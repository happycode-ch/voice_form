import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test that the root endpoint returns the expected message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to VoiceForm AI. Access the API at /api"}

def test_health_endpoint():
    """Test that the health endpoint returns a healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_mock_transcription():
    """Test that the transcription endpoint works with mock data."""
    # This requires setting USE_MOCK_TRANSCRIPTION=True in .env
    import os
    os.environ["USE_MOCK_TRANSCRIPTION"] = "True"
    
    # Create a small dummy audio file
    from io import BytesIO
    dummy_audio = BytesIO(b"dummy audio content")
    dummy_audio.name = "test.wav"
    
    response = client.post(
        "/api/transcribe",
        files={"file": ("test.wav", dummy_audio, "audio/wav")},
        data={"session_id": "test-session"}
    )
    
    assert response.status_code == 200
    assert "transcription" in response.json()
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_mock_summarization():
    """Test that the summarization endpoint works with mock data."""
    # This requires setting USE_MOCK_SUMMARIZATION=True in .env
    import os
    os.environ["USE_MOCK_SUMMARIZATION"] = "True"
    
    test_data = {
        "text": "I've been sleeping quite poorly lately. It takes me about an hour to fall asleep and I wake up frequently during the night.",
        "question": "How would you describe your sleep quality over the past week?",
        "question_type": "open",
        "session_id": "test-session",
        "language": "en"
    }
    
    response = client.post(
        "/api/summarize",
        json=test_data
    )
    
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "analysis" in response.json() 
import React, { useState, useEffect } from 'react';
import './App.css';
import AudioRecorder from './components/AudioRecorder';

interface Question {
  id: string;
  text: string;
  text_de?: string;
  type: 'open' | 'yes_no' | 'likert';
  order: number;
}

interface Response {
  question_id: string;
  transcription?: string;
  summary?: string;
  analysis?: any;
}

const App: React.FC = () => {
  const [language, setLanguage] = useState<'en' | 'de'>('en');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [responses, setResponses] = useState<Response[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  const [questions, setQuestions] = useState<Question[]>([
    // Sample questions (in production, these would be loaded from the API)
    { 
      id: '1', 
      text: 'How would you describe your sleep quality over the past week?', 
      text_de: 'Wie würden Sie Ihre Schlafqualität in der letzten Woche beschreiben?',
      type: 'open', 
      order: 1 
    },
    { 
      id: '2', 
      text: 'Do you have trouble falling asleep?', 
      text_de: 'Haben Sie Schwierigkeiten einzuschlafen?',
      type: 'yes_no', 
      order: 2 
    },
    { 
      id: '3', 
      text: 'On a scale from 1 to 5, how rested do you feel when you wake up?', 
      text_de: 'Auf einer Skala von 1 bis 5, wie ausgeruht fühlen Sie sich beim Aufwachen?',
      type: 'likert', 
      order: 3 
    },
  ]);

  // Initialize session on component mount
  useEffect(() => {
    const initSession = async () => {
      try {
        // In production, this would create a session via API
        setSessionId('sample-session-' + Math.random().toString(36).substring(2, 9));
      } catch (error) {
        console.error('Error initializing session:', error);
      }
    };

    initSession();
  }, []);

  const handleRecordingStart = () => {
    // Additional logic if needed when recording starts
  };

  const handleRecordingStop = () => {
    // Additional logic if needed when recording stops
  };

  const handleRecordingComplete = async (audioBlob: Blob) => {
    setIsProcessing(true);
    
    try {
      // Prepare form data with audio file
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      formData.append('session_id', sessionId);
      formData.append('language', language);
      
      // Make request to transcription API with redirect handling
      const transcriptionResponse = await fetch('/api/transcribe/', {  // Note the trailing slash
        method: 'POST',
        body: formData,
        redirect: 'follow',  // Explicitly follow redirects
      });
      
      if (!transcriptionResponse.ok) {
        const errorData = await transcriptionResponse.json().catch(() => ({ 
          detail: `Request failed with status ${transcriptionResponse.status}` 
        }));
        console.error('Transcription failed:', errorData);
        throw new Error(`Transcription failed: ${errorData.detail || transcriptionResponse.statusText}`);
      }
      
      const transcriptionData = await transcriptionResponse.json().catch(() => {
        throw new Error('Failed to parse transcription response');
      });
      
      if (!transcriptionData.transcription) {
        throw new Error('No transcription received from server');
      }
      
      const { transcription } = transcriptionData;
      
      // Get current question
      const currentQuestion = questions[currentQuestionIndex];
      
      // Prepare summarization request
      const summarizePayload = {
        text: transcription,
        question: language === 'en' ? currentQuestion.text : currentQuestion.text_de || currentQuestion.text,
        question_type: currentQuestion.type,
        session_id: sessionId,
        language,
      };
      
      // Make request to summarization API
      const summaryResponse = await fetch('/api/summarize/', {  // Note the trailing slash
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(summarizePayload),
        redirect: 'follow',  // Explicitly follow redirects
      });
      
      if (!summaryResponse.ok) {
        const errorData = await summaryResponse.json().catch(() => ({ 
          detail: `Request failed with status ${summaryResponse.status}` 
        }));
        console.error('Summarization failed:', errorData);
        throw new Error(`Summarization failed: ${errorData.detail || summaryResponse.statusText}`);
      }
      
      const summaryData = await summaryResponse.json().catch(() => {
        throw new Error('Failed to parse summary response');
      });
      
      // Store response
      const newResponse: Response = {
        question_id: currentQuestion.id,
        transcription,
        summary: summaryData.summary,
        analysis: summaryData.analysis,
      };
      
      setResponses([...responses, newResponse]);
      
      // Move to next question
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        // Questionnaire complete
        await handleCompleteSurvey();
      }
      
    } catch (err: unknown) {
      const error = err as Error;
      console.error('Error processing recording:', error);
      alert(language === 'en' 
        ? `Error: ${error.message}. Please try again.` 
        : `Fehler: ${error.message}. Bitte versuchen Sie es erneut.`);
    } finally {
      setIsProcessing(false);
      setIsRecording(false);  // Ensure recording state is reset
    }
  };

  const handleLanguageToggle = () => {
    setLanguage(language === 'en' ? 'de' : 'en');
  };

  const handleCompleteSurvey = async () => {
    // In production, this would send all responses to the backend for final processing
    alert(language === 'en' 
      ? 'Survey complete! Thank you for your time.' 
      : 'Umfrage abgeschlossen! Vielen Dank für Ihre Zeit.');
  };

  const getCurrentQuestion = () => {
    if (currentQuestionIndex < questions.length) {
      const question = questions[currentQuestionIndex];
      return language === 'en' ? question.text : (question.text_de || question.text);
    }
    return '';
  };

  const handleRecordButton = () => {
    setIsRecording(!isRecording);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>VoiceForm AI</h1>
        <button className="language-toggle" onClick={handleLanguageToggle}>
          {language === 'en' ? 'Deutsch' : 'English'}
        </button>
      </header>

      <main className="app-content">
        {sessionId ? (
          <>
            <div className="question-container">
              <div className="question-counter">
                {language === 'en' 
                  ? `Question ${currentQuestionIndex + 1} of ${questions.length}` 
                  : `Frage ${currentQuestionIndex + 1} von ${questions.length}`}
              </div>
              <h2 className="question-text">{getCurrentQuestion()}</h2>
            </div>

            <div className="recorder-container">
              <AudioRecorder
                isRecording={isRecording}
                onRecordingComplete={handleRecordingComplete}
                onRecordingStart={handleRecordingStart}
                onRecordingStop={handleRecordingStop}
                language={language}
              />
              
              <div className="controls">
                <button
                  className={`record-button ${isRecording ? 'recording' : ''}`}
                  onClick={handleRecordButton}
                  disabled={isProcessing}
                >
                  {isRecording 
                    ? (language === 'en' ? 'Stop Recording' : 'Aufnahme beenden') 
                    : (language === 'en' ? 'Start Recording' : 'Aufnahme starten')}
                </button>
              </div>
              
              {isProcessing && (
                <div className="processing-indicator">
                  {language === 'en' ? 'Processing...' : 'Verarbeitung...'}
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="loading">
            {language === 'en' ? 'Loading...' : 'Wird geladen...'}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          {language === 'en' 
            ? '© 2023 VoiceForm AI - Voice-first intake solutions' 
            : '© 2023 VoiceForm AI - Sprachbasierte Erfassungslösungen'}
        </p>
      </footer>
    </div>
  );
};

export default App; 
import React, { useState, useRef, useEffect } from 'react';
import './AudioRecorder.css';

interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void;
  isRecording: boolean;
  onRecordingStart: () => void;
  onRecordingStop: () => void;
  language?: string;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onRecordingComplete,
  isRecording,
  onRecordingStart,
  onRecordingStop,
  language = 'en'
}) => {
  const [recordingTime, setRecordingTime] = useState<number>(0);
  const [audioLevel, setAudioLevel] = useState<number>(0);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const microphoneStreamRef = useRef<MediaStream | null>(null);
  
  // Request microphone access and set up analyzer for audio levels
  const setupAudio = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      microphoneStreamRef.current = stream;
      
      // Create audio context and analyzer
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      audioContextRef.current = audioContext;
      
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      analyserRef.current = analyser;
      
      const microphone = audioContext.createMediaStreamSource(stream);
      microphone.connect(analyser);
      
      // Set up audio level monitoring
      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      
      const updateAudioLevel = () => {
        if (analyserRef.current && isRecording) {
          analyserRef.current.getByteFrequencyData(dataArray);
          
          // Calculate average level
          let sum = 0;
          for (let i = 0; i < dataArray.length; i++) {
            sum += dataArray[i];
          }
          const avg = sum / dataArray.length;
          
          // Normalize to 0-100
          setAudioLevel(Math.min(100, Math.max(0, avg * 1.5)));
          
          requestAnimationFrame(updateAudioLevel);
        }
      };
      
      if (isRecording) {
        updateAudioLevel();
      }
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };
  
  // Start recording
  const startRecording = async () => {
    audioChunksRef.current = [];
    setRecordingTime(0);
    
    await setupAudio();
    
    if (microphoneStreamRef.current) {
      const options = { mimeType: 'audio/webm' };
      const mediaRecorder = new MediaRecorder(microphoneStreamRef.current, options);
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        onRecordingComplete(audioBlob);
      };
      
      // Start the recorder
      mediaRecorder.start();
      mediaRecorderRef.current = mediaRecorder;
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
      
      onRecordingStart();
    }
  };
  
  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      
      // Stop timer
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      
      // Release microphone
      if (microphoneStreamRef.current) {
        microphoneStreamRef.current.getTracks().forEach(track => track.stop());
        microphoneStreamRef.current = null;
      }
      
      onRecordingStop();
    }
  };
  
  // Format recording time as MM:SS
  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };
  
  // Control recording based on isRecording prop
  useEffect(() => {
    if (isRecording) {
      startRecording();
    } else if (mediaRecorderRef.current) {
      stopRecording();
    }
    
    // Clean up on unmount
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (microphoneStreamRef.current) {
        microphoneStreamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [isRecording]);
  
  return (
    <div className="audio-recorder">
      <div className="audio-visualizer">
        <div 
          className="audio-level" 
          style={{ height: `${audioLevel}%` }}
        />
      </div>
      
      <div className="recording-info">
        <div className="recording-time">{formatTime(recordingTime)}</div>
        <div className="recording-status">
          {isRecording ? (
            <span className="recording-indicator">●</span>
          ) : null}
          {isRecording 
            ? language === 'de' ? 'Aufnahme läuft...' : 'Recording...' 
            : language === 'de' ? 'Bereit' : 'Ready'}
        </div>
      </div>
    </div>
  );
};

export default AudioRecorder; 
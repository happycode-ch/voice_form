import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../../frontend/src/App';

jest.mock('../../frontend/src/components/AudioRecorder', () => {
  return function MockAudioRecorder() {
    return <div data-testid="audio-recorder">Audio Recorder Component</div>;
  };
});

describe('App component', () => {
  test('renders the header with VoiceForm AI title', () => {
    render(<App />);
    const headerElement = screen.getByText(/VoiceForm AI/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('renders language toggle button', () => {
    render(<App />);
    const toggleButton = screen.getByText(/English|Deutsch/i);
    expect(toggleButton).toBeInTheDocument();
  });

  test('displays loading state initially', () => {
    render(<App />);
    const loadingElement = screen.getByText(/Loading|Wird geladen/i);
    expect(loadingElement).toBeInTheDocument();
  });
}); 
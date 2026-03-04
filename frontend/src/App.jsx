import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import CBTProcessor from './pages/CBTProcessor';
import AIGrading from './pages/AIGrading';
import AIChat from './components/AIChat';
import WAECBrowser from './pages/WAECBrowser';
import './index.css';

function App() {
  const [view, setView] = useState('dashboard');
  const [selectedExamId, setSelectedExamId] = useState(null);

  const startExam = (examId) => {
    setSelectedExamId(examId);
    setView('practice');
  };

  const startGrading = () => setView('grading');
  const startInterview = () => setView('interview');
  const startWAEC = () => setView('waec');
  const goBack = () => setView('dashboard');

  return (
    <div className="min-h-screen bg-background text-white selection:bg-primary/30 antialiased overflow-hidden">
      {view === 'dashboard' && (
        <Dashboard
          onStartExam={startExam}
          onStartGrading={startGrading}
          onStartInterview={startInterview}
          onStartWAEC={startWAEC}
        />
      )}

      {view === 'practice' && (
        <div className="p-8 h-screen">
          <button
            onClick={goBack}
            className="mb-6 btn-secondary px-4 py-2 text-sm"
          >
            ← Back to Dashboard
          </button>
          <CBTProcessor examId={selectedExamId} onExit={goBack} />
        </div>
      )}

      {view === 'grading' && (
        <div className="p-8 h-screen overflow-y-auto">
          <button
            onClick={goBack}
            className="mb-6 btn-secondary px-4 py-2 text-sm"
          >
            ← Back to Dashboard
          </button>
          <AIGrading onBack={goBack} />
        </div>
      )}

      {view === 'interview' && (
        <div className="p-8 h-screen">
          <button
            onClick={goBack}
            className="mb-6 btn-secondary px-4 py-2 text-sm"
          >
            ← Back to Dashboard
          </button>
          <AIInterview onBack={goBack} />
        </div>
      )}

      {view === 'waec' && (
        <WAECBrowser onExit={goBack} />
      )}

      <AIChat />
    </div>
  );
}

export default App;

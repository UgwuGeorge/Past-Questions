import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import CBTProcessor from './pages/CBTProcessor';
import AIGrading from './pages/AIGrading';
import AIInterview from './pages/AIInterview';

function App() {
  const [view, setView] = useState('dashboard');
  const [activeExam, setActiveExam] = useState(null);

  const startExam = (examId) => {
    setActiveExam(examId);
    setView('cbt');
  };

  return (
    <div className="min-h-screen bg-background text-white font-sans antialiased">
      {view === 'dashboard' && (
        <Dashboard
          onStartExam={startExam}
          onStartGrading={() => setView('essay')}
          onStartInterview={() => setView('interview')}
        />
      )}
      {view === 'cbt' && <CBTProcessor onExit={() => setView('dashboard')} />}
      {view === 'essay' && <AIGrading onBack={() => setView('dashboard')} />}
      {view === 'interview' && <AIInterview onBack={() => setView('dashboard')} />}
    </div>
  );
}

export default App;

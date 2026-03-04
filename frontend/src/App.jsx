import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import CBTProcessor from './pages/CBTProcessor';
import './index.css';

function App() {
  const [view, setView] = useState('dashboard');
  const [selectedExamId, setSelectedExamId] = useState(null);

  const startExam = (examId) => {
    setSelectedExamId(examId);
    setView('practice');
  };

  const goBack = () => setView('dashboard');

  return (
    <div className="min-h-screen bg-background text-white selection:bg-primary/30 antialiased overflow-hidden">
      {view === 'dashboard' && (
        <Dashboard
          onStartExam={startExam}
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
    </div>
  );
}

export default App;

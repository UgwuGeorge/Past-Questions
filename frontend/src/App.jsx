import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import CBTProcessor from './pages/CBTProcessor';
import AIGrading from './pages/AIGrading';
import AIInterview from './pages/AIInterview';
import AIChat from './components/AIChat';
import WAECBrowser from './pages/WAECBrowser';
import ExamRepo from './pages/ExamRepo';
import { ChevronLeft } from 'lucide-react';
import './index.css';

function App() {
  const [view, setView] = useState('dashboard');
  const [selectedExamId, setSelectedExamId] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedExamType, setSelectedExamType] = useState(null); // 'WAEC', 'NECO', etc.

  const startExam = (examId) => {
    setSelectedExamId(examId);
    setView('practice');
  };

  const startGrading = () => setView('grading');
  const startInterview = () => setView('interview');

  const startPractice = (type, examId = null) => {
    setSelectedExamType(type);
    setSelectedExamId(examId);
    if (type === 'WAEC') {
      setView('waec_practice');
    } else {
      setView('practice');
    }
  };

  const startPDFRepo = (type) => {
    setSelectedExamType(type);
    setView('pdf_repo');
  };

  const goBack = () => setView('dashboard');

  return (
    <div className="min-h-screen bg-background text-white selection:bg-primary/30 antialiased overflow-hidden">
      {view === 'dashboard' && (
        <Dashboard
          onStartPractice={startPractice}
          onStartPDFRepo={startPDFRepo}
          onStartGrading={startGrading}
          onStartInterview={startInterview}
        />
      )}

      {view === 'practice' && (
        <div className="h-screen overflow-hidden">
          <CBTProcessor examId={selectedExamId} onExit={goBack} />
        </div>
      )}

      {view === 'waec_practice' && (
        <WAECBrowser onExit={goBack} examId={selectedExamId} />
      )}

      {view === 'pdf_repo' && (
        <ExamRepo examType={selectedExamType} onExit={goBack} />
      )}

      {view === 'grading' && (
        <div className="p-8 h-screen overflow-y-auto">
          <button
            onClick={goBack}
            className="mb-6 flex items-center gap-2 px-4 py-2 text-sm bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all"
          >
            <ChevronLeft size={16} /> Back to Dashboard
          </button>
          <AIGrading onBack={goBack} />
        </div>
      )}

      {view === 'interview' && (
        <div className="p-8 h-screen">
          <button
            onClick={goBack}
            className="mb-6 flex items-center gap-2 px-4 py-2 text-sm bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all"
          >
            <ChevronLeft size={16} /> Back to Dashboard
          </button>
          <AIInterview onBack={goBack} />
        </div>
      )}

      <AIChat />
    </div>
  );
}

export default App;

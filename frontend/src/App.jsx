import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import CBTProcessor from './pages/CBTProcessor';
import AIGrading from './pages/AIGrading';
import AIInterview from './pages/AIInterview';
import AIChat from './components/AIChat';
import WAECBrowser from './pages/WAECBrowser';
import ExamRepo from './pages/ExamRepo';
import SubjectHub from './pages/SubjectHub';
import {
  ChevronLeft, LayoutDashboard, PenTool, Mic, FileText,
  Settings, LogOut, Home, ArrowLeft
} from 'lucide-react';
import { clsx } from 'clsx';
import './index.css';

function NavItem({ icon, label, active = false, onClick }) {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all group",
        active
          ? "bg-primary/10 text-primary border border-primary/20"
          : "text-white/50 hover:bg-white/5 hover:text-white"
      )}
    >
      <span className={clsx(active ? "text-primary" : "text-white/50 group-hover:text-primary transition-colors")}>{icon}</span>
      <span className="font-black text-xs uppercase tracking-widest">{label}</span>
      {active && <div className="ml-auto w-1.5 h-1.5 bg-primary rounded-full" />}
    </button>
  );
}

function App() {
  const [view, setView] = useState('dashboard');
  const [navHistory, setNavHistory] = useState([]); // True history stack
  const [selectedExamId, setSelectedExamId] = useState(null);
  const [selectedExamName, setSelectedExamName] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedExamType, setSelectedExamType] = useState(null);
  const [activeSubject, setActiveSubject] = useState(null);
  const [examAutoStart, setExamAutoStart] = useState(false);
  const [preferredDifficulty, setPreferredDifficulty] = useState('medium');

  // Helper to change view and push current view to history
  const navigateTo = (newView) => {
    setNavHistory(prev => [...prev, view]);
    setView(newView);
  };

  // Helper to go back to previous view in history
  const goBack = () => {
    setNavHistory(prev => {
      if (prev.length === 0) {
        setView('dashboard');
        return [];
      }
      const newHistory = [...prev];
      const previousView = newHistory.pop();
      setView(previousView);
      return newHistory;
    });
  };

  // Helper to forcefully reset to dashboard (clearing history)
  const goHome = () => {
    setNavHistory([]);
    setView('dashboard');
  };

  const startGrading = () => navigateTo('grading');
  const startInterview = () => navigateTo('interview');

  // All exam types now use the unified subject-select + config flow (WAECBrowser)
  const startPractice = (type, examId = null, examName = null) => {
    setSelectedExamType(type);
    setSelectedExamId(examId);
    setSelectedExamName(examName || type);
    if (examId) {
      // Has a real DB exam - use the full subject → config → exam flow
      navigateTo('waec_practice');
    } else {
      // Fallback for exams not in DB yet
      navigateTo('practice');
    }
  };

  const openSubjectHub = (subject, examName) => {
    setActiveSubject({ ...subject, examName });
    navigateTo('subject_hub');
  };

  const startPDFRepo = (type) => {
    setSelectedExamType(type);
    navigateTo('pdf_repo');
  };

  const handleAIAction = (action) => {
    console.log("AI Action Received:", action);
    if (action.type === 'navigate') {
      const page = action.page;
      if (page === 'dashboard' || page === 'home') goHome();
      else if (page === 'grading') startGrading();
      else if (page === 'interview') startInterview();
      else if (page === 'results') goHome(); // Could map to a real results page later
      else if (page === 'explorer') navigateTo('waec_practice'); // Map explorer to the browser
      else if (page === 'pdf' || page === 'repo') navigateTo('pdf_repo');
      else navigateTo(page);
    } else if (action.type === 'start_exam') {
      setSelectedExamId(action.exam_id);
      setSelectedSubject(action.subject_id);
      setPreferredDifficulty(action.difficulty || 'medium');
      setExamAutoStart(true);
      navigateTo('practice');
    }
  };

  return (
    <div className="flex h-screen bg-[#0b0f1a] text-white selection:bg-primary/30 antialiased overflow-hidden">
      {/* GLOBAL SIDEBAR */}
      <aside className="w-64 glass border-r border-white/5 p-6 flex flex-col z-50 shrink-0">
        <div className="flex items-center gap-4 mb-10 px-2 group cursor-pointer" onClick={goHome}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg group-hover:scale-110 transition-all">
            <span className="font-black text-white italic">R</span>
          </div>
          <span className="text-2xl font-black tracking-tighter">Reharz</span>
        </div>

        <nav className="flex-1 space-y-2">
          <NavItem
            icon={<LayoutDashboard size={20} />}
            label="Dashboard"
            active={view === 'dashboard'}
            onClick={goHome}
          />
          <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Lab</div>
          <NavItem
            icon={<PenTool size={20} />}
            label="Grading"
            active={view === 'grading'}
            onClick={startGrading}
          />
          <NavItem
            icon={<Mic size={20} />}
            label="Interview Prep"
            active={view === 'interview'}
            onClick={startInterview}
          />

          <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Practice</div>
          <NavItem
            icon={<FileText size={20} />}
            label="My Results"
            active={false}
          />

          <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">User</div>
          <NavItem icon={<Settings size={20} />} label="Settings" />
        </nav>

        <div className="mt-auto pt-6 border-t border-white/5">
          <button className="flex items-center gap-3 px-4 py-3 w-full text-white/50 hover:text-white hover:bg-white/5 rounded-xl transition-all group">
            <LogOut size={20} className="group-hover:text-rose-500 transition-colors" />
            <span className="font-bold text-sm">Sign Out</span>
          </button>
        </div>
      </aside>

      {/* VIEWPORT CONTENT */}
      <div className="flex-1 overflow-hidden relative">
        {view === 'dashboard' && (
          <Dashboard
            onStartPractice={startPractice}
            onStartPDFRepo={startPDFRepo}
            onStartGrading={startGrading}
            onStartInterview={startInterview}
            onOpenSubjectHub={openSubjectHub}
          />
        )}

        {view === 'subject_hub' && (
          <SubjectHub
            subject={activeSubject}
            examName={activeSubject.examName}
            onBack={goBack}
            onStartSimulation={(mode) => {
              setSelectedExamId(activeSubject.exam_id);
              setSelectedSubject(activeSubject.id);
              navigateTo('practice');
            }}
          />
        )}

        {view === 'practice' && (
          <div className="h-full overflow-hidden">
            <CBTProcessor
              examId={selectedExamId}
              subjectId={selectedSubject}
              difficulty={preferredDifficulty}
              autoStart={examAutoStart}
              onExit={() => { setExamAutoStart(false); goBack(); }}
            />
          </div>
        )}

        {view === 'waec_practice' && (
          <WAECBrowser
            onExit={goBack}
            examId={selectedExamId}
            examName={selectedExamName || selectedExamType}
          />
        )}

        {view === 'pdf_repo' && (
          <ExamRepo examType={selectedExamType} onExit={goBack} />
        )}

        {view === 'grading' && (
          <div className="p-8 h-full overflow-y-auto">
            <button
              onClick={goBack}
              className="mb-6 flex items-center gap-2 px-4 py-2 text-sm bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all"
            >
              <ChevronLeft size={16} /> Back
            </button>
            <AIGrading onBack={goBack} />
          </div>
        )}

        {view === 'interview' && (
          <div className="p-8 h-full">
            <button
              onClick={goBack}
              className="mb-6 flex items-center gap-2 px-4 py-2 text-sm bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all"
            >
              <ChevronLeft size={16} /> Back
            </button>
            <AIInterview onBack={goBack} />
          </div>
        )}

        <div className="fixed bottom-8 right-8 z-[100]">
          <AIChat subject={activeSubject} onAction={handleAIAction} />
        </div>
      </div>
    </div>
  );
}

export default App;

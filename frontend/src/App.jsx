import { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import { motion, AnimatePresence } from 'framer-motion';
import CBTProcessor from './pages/CBTProcessor';
import AIGrading from './pages/AIGrading';
import AIInterview from './pages/AIInterview';
import AIChat from './components/AIChat';
import WAECBrowser from './pages/WAECBrowser';
import ExamRepo from './pages/ExamRepo';
import SubjectHub from './pages/SubjectHub';
import Auth from './pages/Auth';
import MyResults from './pages/MyResults';
import AdminPanel from './pages/AdminPanel';
import SubscriptionHub from './pages/SubscriptionHub';
import {
    ChevronLeft, LayoutDashboard, PenTool, Mic, FileText,
    Settings, LogOut, Home, ArrowLeft, User as UserIcon,
    ShieldAlert, Menu, X, Crown
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
  const [user, setUser] = useState(null);
  const [view, setView] = useState('dashboard');
  const [navHistory, setNavHistory] = useState([]); // True history stack
  const [selectedExamId, setSelectedExamId] = useState(null);
  const [selectedExamName, setSelectedExamName] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedExamType, setSelectedExamType] = useState(null);
  const [activeSubject, setActiveSubject] = useState(null);
  const [examAutoStart, setExamAutoStart] = useState(false);
  const [preferredDifficulty, setPreferredDifficulty] = useState('medium');
  const [initialResultId, setInitialResultId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Persistence
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
    goHome();
  };

  // Helper to change view and push current view to history
  const navigateTo = (newView) => {
    setNavHistory(prev => [...prev, view]);
    setView(newView);
    setSidebarOpen(false); // Close sidebar on mobile after navigation
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
  const startResults = (sessionId = null) => {
    setInitialResultId(sessionId);
    navigateTo('results');
  };

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
      else if (page === 'results' || page === 'my_results') startResults(); 
      else if (page === 'explorer') navigateTo('waec_practice'); 
      else if (page === 'pdf' || page === 'repo') navigateTo('pdf_repo');
      else navigateTo(page);
    } else if (action.type === 'start_exam') {
      setSelectedExamId(action.exam_id);
      setSelectedSubject(action.subject_id);
      setPreferredDifficulty(action.difficulty || 'medium');
      setExamAutoStart(true);
      navigateTo('practice');
    } else if (action.type === 'view_session' || action.type === 'view_result') {
      startResults(action.session_id);
    }
  };

  if (!user) {
    return <Auth onLoginSuccess={(u) => setUser(u)} />;
  }

  return (
    <div className="flex h-screen bg-[#0b0f1a] text-white selection:bg-primary/30 antialiased overflow-hidden relative">
      {/* MOBILE TOP BAR */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 glass-hover bg-[#0b0f1a]/80 backdrop-blur-xl border-b border-white/5 z-40 flex items-center justify-between px-6">
        <div className="flex items-center gap-3 cursor-pointer" onClick={goHome}>
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <span className="font-black text-white italic text-xs">R</span>
          </div>
          <span className="text-xl font-black tracking-tighter">Reharz</span>
        </div>
        <button 
          onClick={() => setSidebarOpen(true)}
          className="p-2 rounded-xl bg-white/5 border border-white/10"
        >
          <Menu size={20} />
        </button>
      </div>

      {/* OVERLAY FOR MOBILE SIDEBAR */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 bg-black/60 backdrop-blur-md z-[60] lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* GLOBAL SIDEBAR */}
      <aside className={clsx(
        "fixed lg:relative inset-y-0 left-0 w-64 glass border-r border-white/5 p-6 flex flex-col z-[100] transition-transform duration-300 ease-in-out lg:translate-x-0 shrink-0",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="absolute top-4 right-4 lg:hidden">
            <button 
                onClick={() => setSidebarOpen(false)}
                className="p-2 rounded-lg bg-white/5 hover:bg-white/10"
            >
                <X size={20} className="text-white/40" />
            </button>
        </div>
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
            active={view === 'results'}
            onClick={startResults}
          />

          {user.is_admin && (
            <>
              <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Oversight</div>
              <NavItem
                icon={<ShieldAlert size={20} />}
                label="Admin Panel"
                active={view === 'admin'}
                onClick={() => navigateTo('admin')}
              />
            </>
          )}

          <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">User Profile</div>
          <div className="px-4 py-3 flex items-center gap-3 bg-white/5 rounded-2xl border border-white/10 group cursor-default">
             <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                <UserIcon size={16} />
             </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black truncate max-w-[100px]">{user.username}</span>
                  {user.is_admin && (
                    <span className="px-1.5 py-0.5 bg-amber-500/20 text-amber-500 text-[8px] font-black rounded uppercase border border-amber-500/20">Admin</span>
                  )}
                </div>
                <span className="text-[10px] text-white/30 font-bold">{user.is_admin ? 'System Architect' : 'Lvl 1 Agent'}</span>
              </div>
          </div>
          <NavItem icon={<Settings size={20} />} label="Settings" />
          
          <div className="mt-4">
            <button
              onClick={() => navigateTo('subscription')}
              className="w-full relative flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-gradient-to-r from-amber-500/20 to-orange-500/20 hover:from-amber-500/30 hover:to-orange-500/30 border border-amber-500/30 text-amber-500 font-black tracking-widest text-xs uppercase hover:scale-[1.02] transition-all"
            >
                <Crown size={16} /> Unlock Pro
            </button>
          </div>
        </nav>

        <div className="mt-auto pt-6 border-t border-white/5">
          <button 
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full text-white/50 hover:text-white hover:bg-white/5 rounded-xl transition-all group"
          >
            <LogOut size={20} className="group-hover:text-rose-500 transition-colors" />
            <span className="font-bold text-sm">Sign Out</span>
          </button>
        </div>
      </aside>

      {/* VIEWPORT CONTENT */}
      <div className="flex-1 overflow-hidden relative flex flex-col">
        {/* MOBILE SPACER */}
        <div className="h-16 lg:hidden shrink-0" />
        
        <div className="flex-1 overflow-hidden relative">
        {view === 'dashboard' && (
          <Dashboard
            userId={user.id}
            onStartPractice={startPractice}
            onStartPDFRepo={startPDFRepo}
            onStartGrading={startGrading}
            onStartInterview={startInterview}
            onOpenSubjectHub={openSubjectHub}
            onViewResult={startResults}
            onUnlockPro={() => navigateTo('subscription')}
          />
        )}

        {view === 'subject_hub' && (
          <SubjectHub
            userId={user.id}
            subject={activeSubject}
            examName={activeSubject.examName}
            onBack={goBack}
            onStartSimulation={(mode) => {
              setSelectedExamId(activeSubject.exam_id);
              setSelectedSubject(activeSubject.id);
              navigateTo('practice');
            }}
            onUnlockPro={() => navigateTo('subscription')}
          />
        )}

        {view === 'practice' && (
          <div className="h-full overflow-hidden">
            <CBTProcessor
              userId={user.id}
              examId={selectedExamId}
              subjectId={selectedSubject}
              difficulty={preferredDifficulty}
              autoStart={examAutoStart}
              onExit={() => { setExamAutoStart(false); goBack(); }}
              onUnlockPro={() => navigateTo('subscription')}
            />
          </div>
        )}

        {view === 'waec_practice' && (
          <WAECBrowser
            userId={user.id}
            onExit={goBack}
            examId={selectedExamId}
            examName={selectedExamName || selectedExamType}
            onUnlockPro={() => navigateTo('subscription')}
          />
        )}

        {view === 'pdf_repo' && (
          <ExamRepo examType={selectedExamType} onExit={goBack} />
        )}

        {view === 'results' && (
          <MyResults userId={user.id} initialSessionId={initialResultId} />
        )}

        {view === 'admin' && (
          <AdminPanel userId={user.id} />
        )}

        {view === 'grading' && (
          <div className="p-8 h-full overflow-y-auto">
            <button
              onClick={goBack}
              className="mb-6 flex items-center gap-2 px-4 py-2 text-sm bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all"
            >
              <ChevronLeft size={16} /> Back
            </button>
            <AIGrading userId={user.id} onBack={goBack} onUnlockPro={() => navigateTo('subscription')} />
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
            <AIInterview userId={user.id} onBack={goBack} onUnlockPro={() => navigateTo('subscription')} />
          </div>
        )}

        {view === 'subscription' && (
          <SubscriptionHub user={user} />
        )}

        <div className="fixed bottom-8 right-8 z-[100]">
          <AIChat userId={user.id} subject={activeSubject} onAction={handleAIAction} />
        </div>
       </div>
      </div>
    </div>
  );
}

export default App;

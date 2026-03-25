import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import {
    ChevronLeft, ChevronRight, CheckCircle2, Flag, Timer,
    BookOpen, Layers, XCircle, Zap, Settings2, ShieldCheck,
    Target, Clock
} from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = `http://${window.location.hostname}:8000/api`;

export default function WAECBrowser({ userId, onExit, examId: propExamId, examName: propExamName }) {
    const [view, setView] = useState('subjects'); // subjects | config | loading | exam | results
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState(null);
    const [config, setConfig] = useState({
        topicMode: 'all', // 'all' | 'specific'
        specificTopics: '',
        questionCount: 50,
        duration: 60,
        section: 'objective' // 'objective' | 'theory' | 'practical' | 'full exam'
    });

    const [questions, setQuestions] = useState([]);
    const [sessionData, setSessionData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Exam state
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState({});
    const [flags, setFlags] = useState({});
    const [timeLeft, setTimeLeft] = useState(0);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const examId = propExamId;
    const examName = propExamName || 'WAEC';

    useEffect(() => {
        if (!examId) {
            setError('No exam selected. Please go back and select an exam.');
            setLoading(false);
            return;
        }
        const fetchSubjects = async () => {
            setLoading(true);
            try {
                const res = await fetch(`${API_BASE}/exams/${examId}/subjects`);
                if (!res.ok) throw new Error("Could not load subjects");
                const data = await res.json();
                setSubjects(Array.isArray(data) ? data : []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchSubjects();
    }, [examId]);

    // ICAN-specific defaults
    useEffect(() => {
        if (examName?.includes('ICAN')) {
            const isFoundation = examName.includes('Foundation');
            const isHigher = examName.includes('Skills') || examName.includes('Professional');

            if (config.section === 'full exam') {
                if (isFoundation) {
                    setConfig(prev => ({ ...prev, questionCount: 25, duration: 180 }));
                } else if (isHigher) {
                    setConfig(prev => ({ ...prev, questionCount: 6, duration: 180 }));
                } else {
                    setConfig(prev => ({ ...prev, questionCount: 40, duration: 180 }));
                }
            } else if (config.section === 'objective') {
                setConfig(prev => ({ ...prev, questionCount: 20, duration: 45 }));
            }
        } else if (examName?.includes('WAEC') || examName?.includes('JAMB')) {
            if (config.section === 'full exam') {
                setConfig(prev => ({ ...prev, questionCount: 50, duration: 120 }));
            }
        }
    }, [examName, config.section]);

    // Timer countdown
    useEffect(() => {
        if (view !== 'exam' || isSubmitted || !timeLeft) return;
        const timer = setInterval(() => {
            setTimeLeft(t => {
                if (t <= 1) {
                    clearInterval(timer);
                    handleSubmit();
                    return 0;
                }
                return t - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [view, isSubmitted, timeLeft]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const handleSelectSubject = (subjectItem) => {
        setSelectedSubject(subjectItem);
        setView('config');
    };

    const startSimulation = async () => {
        setView('loading');
        setLoading(true);
        try {
            const topics = config.topicMode === 'specific'
                ? config.specificTopics.split(',').map(t => t.trim()).filter(t => t)
                : null;

            const res = await fetch(`${API_BASE}/simulation/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    exam_id: examId,
                    subject_id: selectedSubject.id,
                    question_count: config.questionCount,
                    duration_minutes: config.duration,
                    topics: topics,
                    section: config.section
                })
            });
            const data = await res.json();
            if (data.detail) throw new Error(data.detail);

            // Normalize choices for display if they aren't already
            const normalized = data.questions.map(q => ({
                ...q,
                choices: Array.isArray(q.choices) ? q.choices : [],
                // Find correct answer if provided by backend (optional check)
                correctLabel: (q.choices.find(c => c.is_correct) || {}).label
            }));

            setQuestions(normalized);
            setSessionData(data);
            setTimeLeft(data.duration_seconds);
            setCurrentIdx(0);
            setAnswers({});
            setFlags({});
            setIsSubmitted(false);
            setView('exam');
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
            setView('config');
        }
    };

    const handleSelectAnswer = (label) => {
        setAnswers(prev => ({ ...prev, [questions[currentIdx].id]: label }));
    };

    const toggleFlag = () => {
        setFlags(prev => ({ ...prev, [questions[currentIdx].id]: !prev[currentIdx] }));
    };

    const handleSubmit = async () => {
        if (isSubmitted) return;
        setIsSubmitted(true);
        setView('loading');
        try {
            const res = await fetch(`${API_BASE}/simulation/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionData.session_id,
                    answers: answers
                })
            });
            const data = await res.json();
            setSessionData({ ...sessionData, results: data });
            setView('results');
        } catch (err) {
            console.error("Submission failed:", err);
            setView('results'); // Show what we have or error
        }
        setLoading(false);
    };

    if (loading && view === 'loading') {
        return (
            <div className="h-screen flex flex-col items-center justify-center bg-background">
                <div className="relative">
                    <div className="w-24 h-24 border-4 border-primary/20 rounded-full animate-ping" />
                    <div className="absolute inset-0 flex items-center justify-center">
                        <Zap size={32} className="text-primary animate-pulse" />
                    </div>
                </div>
                <h2 className="text-xl font-black mt-8 tracking-widest uppercase">Initializing Simulation</h2>
                <p className="text-text-dim italic">Synthesizing {selectedSubject?.name} dataset...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="h-screen flex items-center justify-center bg-background">
                <GlowCard className="max-w-lg w-full text-center">
                    <XCircle className="w-16 h-16 text-rose-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Oops!</h2>
                    <p className="text-text-dim mb-6">{error}</p>
                    <button onClick={() => { setError(null); setView('subjects'); }} className="btn-primary w-full justify-center">Try Again</button>
                    <button onClick={onExit} className="mt-4 text-xs text-text-dim hover:text-white transition-colors">Back to Dashboard</button>
                </GlowCard>
            </div>
        );
    }

    if (view === 'subjects') {
        return (
            <div className="h-screen flex flex-col bg-background overflow-y-auto">
                <header className="glass px-8 py-5 flex items-center gap-4 border-b border-white/5 sticky top-0 z-10">
                    <button onClick={onExit} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold flex items-center gap-2 uppercase tracking-tighter">
                            <Layers size={20} className="text-primary" />
                            {examName} — Subjects
                        </h1>
                        <p className="text-xs text-text-dim">Select a proctored curriculum track</p>
                    </div>
                </header>
                <div className="p-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto w-full">
                    {subjects.map((sub, i) => (
                        <motion.button
                            key={sub.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            onClick={() => handleSelectSubject(sub)}
                            className="glass rounded-[32px] p-8 text-left border border-white/5 hover:border-primary/40 hover:bg-white/[0.04] transition-all group relative overflow-hidden h-64 flex flex-col"
                        >
                            <div className="absolute -right-4 -top-4 w-32 h-32 bg-primary/5 rounded-full blur-2xl group-hover:bg-primary/10 transition-colors" />
                            <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <BookOpen className="text-primary" size={24} />
                            </div>
                            <h3 className="text-2xl font-black tracking-tight mb-2 group-hover:text-primary transition-colors">{sub.name}</h3>
                            <p className="text-xs text-text-dim font-bold uppercase tracking-widest mt-auto italic">Verified Track AVAILABLE</p>
                        </motion.button>
                    ))}
                </div>
            </div>
        );
    }

    if (view === 'config') {
        return (
            <div className="h-screen flex flex-col bg-background overflow-y-auto">
                <header className="glass px-8 py-5 flex items-center gap-4 border-b border-white/5 sticky top-0 z-10">
                    <button onClick={() => setView('subjects')} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold flex items-center gap-2 uppercase tracking-tighter">
                            <Settings2 size={20} className="text-primary" />
                            {selectedSubject.name} Configuration
                        </h1>
                        <p className="text-xs text-text-dim">Calibrate your practice parameters</p>
                    </div>
                </header>

                <main className="flex-1 p-10 max-w-4xl mx-auto w-full">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
                        {/* Left: Mode \u0026 Topics */}
                        <div className="space-y-6">
                            <GlowCard className="p-8">
                                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-6 flex items-center gap-2">
                                    <ShieldCheck size={14} className="text-primary" /> Examination Mode
                                </h3>
                                <div className="grid grid-cols-1 gap-3">
                                    {['objective', 'theory', 'practical', 'full exam'].map(m => (
                                        <button
                                            key={m}
                                            onClick={() => setConfig({ ...config, section: m })}
                                            className={clsx(
                                                "p-4 rounded-xl border text-left transition-all uppercase text-[10px] font-black tracking-widest",
                                                config.section === m ? "bg-primary text-white border-primary shadow-lg shadow-primary/20" : "glass border-white/10 text-white/40 hover:bg-white/5"
                                            )}
                                        >
                                            {m === 'full exam' ? 'Full Exam' : `${m} Section`}
                                        </button>
                                    ))}
                                </div>
                            </GlowCard>

                            <GlowCard className={clsx("p-8 transition-all", config.section === 'full exam' && "opacity-50 pointer-events-none")}>
                                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-6 flex items-center gap-2">
                                    <Target size={14} className="text-secondary" /> Topic Focus
                                </h3>
                                <div className="space-y-4">
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => setConfig({ ...config, topicMode: 'all' })}
                                            className={clsx(
                                                "flex-1 py-3 rounded-lg text-[10px] font-black uppercase border transition-all",
                                                config.topicMode === 'all' ? "bg-white/10 border-white/20 text-white" : "border-transparent text-white/30 hover:bg-white/5"
                                            )}
                                        >
                                            Every Topic
                                        </button>
                                        <button
                                            onClick={() => setConfig({ ...config, topicMode: 'specific' })}
                                            className={clsx(
                                                "flex-1 py-3 rounded-lg text-[10px] font-black uppercase border transition-all",
                                                config.topicMode === 'specific' ? "bg-white/10 border-white/20 text-white" : "border-transparent text-white/30 hover:bg-white/5"
                                            )}
                                        >
                                            Specific Topics
                                        </button>
                                    </div>
                                    {config.topicMode === 'specific' && (
                                        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}>
                                            <label className="text-[10px] font-bold text-white/30 block mb-2">Input topics (comma separated)</label>
                                            <input
                                                type="text"
                                                placeholder="e.g. Algebra, Trigonometry, Calculus"
                                                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm outline-none focus:border-primary/50 transition-all"
                                                value={config.specificTopics}
                                                onChange={e => setConfig({ ...config, specificTopics: e.target.value })}
                                            />
                                        </motion.div>
                                    )}
                                </div>
                            </GlowCard>
                        </div>

                        {/* Right: Quantities */}
                        <GlowCard className="p-8">
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-8 flex items-center gap-2">
                                <Clock size={14} className="text-accent" /> Control Parameters
                            </h3>
                            {(config.section === 'full exam' && (examName.includes('WAEC') || examName.includes('JAMB'))) ? (
                                <div className="space-y-4 h-full flex flex-col justify-center pb-4">
                                    <GlowCard className="bg-primary/5 border-primary/20 p-6">
                                        <div className="flex items-center gap-3 mb-4">
                                            <ShieldCheck size={24} className="text-primary" />
                                            <div className="text-sm font-black uppercase tracking-[0.2em] text-primary">Full Exam Protocol Active</div>
                                        </div>
                                        <p className="text-xs text-white/60 leading-relaxed italic border-l-2 border-primary/40 pl-4 py-1">
                                            Custom parameters are securely locked. <br /><br />
                                            This simulated session will strictly enforce the exact official structure, duration constraints, and objective/theory divisions derived from the verified reference dataset.
                                        </p>
                                    </GlowCard>
                                </div>
                            ) : (
                                <div className="space-y-8">
                                    <div>
                                        <div className="flex justify-between mb-4">
                                            <label className="text-[10px] font-black uppercase tracking-widest text-white/40">Question Count</label>
                                            <span className="text-primary font-black">{config.questionCount}</span>
                                        </div>
                                        <input
                                            type="range"
                                            min="5"
                                            max="60"
                                            step="5"
                                            value={config.questionCount}
                                            onChange={e => setConfig({ ...config, questionCount: parseInt(e.target.value) })}
                                            className="w-full accent-primary h-1.5 bg-white/5 rounded-full appearance-none cursor-pointer"
                                        />
                                        <div className="flex justify-between mt-2 text-[8px] font-bold text-white/20">
                                            <span>5 Qs</span>
                                            <span>60 Qs</span>
                                        </div>
                                    </div>

                                    <div>
                                        <div className="flex justify-between mb-4">
                                            <label className="text-[10px] font-black uppercase tracking-widest text-white/40">Time Duration</label>
                                            <span className="text-secondary font-black">{config.duration} MIN</span>
                                        </div>
                                        <input
                                            type="range"
                                            min="10"
                                            max="120"
                                            step="10"
                                            value={config.duration}
                                            onChange={e => setConfig({ ...config, duration: parseInt(e.target.value) })}
                                            className="w-full accent-secondary h-1.5 bg-white/5 rounded-full appearance-none cursor-pointer"
                                        />
                                        <div className="flex justify-between mt-2 text-[8px] font-bold text-white/20">
                                            <span>10 MIN</span>
                                            <span>120 MIN</span>
                                        </div>
                                    </div>

                                    <GlowCard className="bg-rose-500/[0.02] border-rose-500/10 p-5">
                                        <div className="text-[10px] font-black uppercase tracking-[0.2em] text-rose-500 mb-2">Simulated Constraint</div>
                                        <p className="text-[10px] text-white/40 leading-relaxed italic">The session will fetch EXACTLY {config.questionCount} questions matching these parameters.</p>
                                    </GlowCard>
                                </div>
                            )}
                        </GlowCard>
                    </div>

                    <button
                        onClick={startSimulation}
                        className="btn-primary w-full py-5 text-lg font-black uppercase tracking-[0.2em] shadow-2xl shadow-primary/20 hover:scale-[1.01] transition-all"
                    >
                        Initialize Practice Session
                    </button>
                </main>
            </div>
        );
    }

    if (view === 'results') {
        const results = sessionData?.results || { correct: 0, total: questions.length, topics: {} };
        const score = results.correct;
        const total = results.total;
        const pct = Math.round((score / total) * 100) || 0;

        return (
            <div className="min-h-screen flex items-center justify-center p-6 bg-background">
                <GlowCard className="max-w-3xl w-full text-center p-12">
                    <CheckCircle2 className="w-20 h-20 text-emerald-500 mx-auto mb-6" />
                    <h1 className="text-5xl font-black italic tracking-tighter mb-2 uppercase">Session Analyzed.</h1>
                    <p className="text-text-dim mb-10 font-medium">{selectedSubject.name} — {config.section.toUpperCase()} TRACK</p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                        <div className="glass p-8 rounded-3xl border border-white/5">
                            <div className="text-4xl font-black text-primary mb-1">{score} / {total}</div>
                            <div className="text-[10px] text-text-dim font-black uppercase tracking-widest">Accuracy</div>
                        </div>
                        <div className="glass p-8 rounded-3xl border border-white/5">
                            <div className={clsx("text-4xl font-black mb-1", pct >= 60 ? "text-emerald-400" : "text-rose-400")}>{pct}%</div>
                            <div className="text-[10px] text-text-dim font-black uppercase tracking-widest">Score</div>
                        </div>
                        <div className="glass p-8 rounded-3xl border border-white/5">
                            <div className="text-4xl font-black text-accent mb-1">{Object.keys(flags).length}</div>
                            <div className="text-[10px] text-text-dim font-black uppercase tracking-widest">Flagged</div>
                        </div>
                    </div>

                    <button
                        onClick={() => setView('subjects')}
                        className="btn-primary w-full py-4 text-xs font-black uppercase tracking-widest"
                    >
                        Return to Subject Selection
                    </button>
                </GlowCard>
            </div>
        );
    }

    if (view === 'exam') {
        if (!questions.length) {
            return (
                <div className="h-screen flex items-center justify-center">
                    <div className="text-center">
                        <XCircle size={48} className="text-rose-500 mx-auto mb-4" />
                        <h2 className="text-2xl font-bold mb-2">No Matching Questions Found</h2>
                        <p className="text-white/40 mb-6 max-w-sm">We couldn't find enough questions matching your specific topic/mode criteria.</p>
                        <button onClick={() => setView('config')} className="btn-primary">Adjust Configuration</button>
                    </div>
                </div>
            )
        }

        const currentQ = questions[currentIdx];
        const isAnswered = !!answers[currentQ.id];

        return (
            <div className="h-screen flex flex-col overflow-hidden bg-background">
                <header className="glass px-10 py-5 flex justify-between items-center border-b border-white/5 shrink-0">
                    <div className="flex items-center gap-6">
                        <div className="bg-rose-500/10 border border-rose-500/20 px-3 py-1 rounded-full flex items-center gap-2">
                            <div className="w-2 h-2 bg-rose-500 rounded-full animate-pulse" />
                            <span className="text-[10px] font-black text-rose-500 uppercase tracking-widest">Simulation Active</span>
                        </div>
                        <div>
                            <span className="font-black text-sm uppercase tracking-tight">{selectedSubject.name} — {config.section}</span>
                            <div className="flex gap-4 text-[10px] text-text-dim font-black">
                                <span>{questions.length} QUESTIONS REQUISITIONED</span>
                            </div>
                        </div>
                    </div>

                    <div className={clsx(
                        "flex items-center gap-4 px-8 py-2 rounded-2xl glass border-2 transition-all duration-500",
                        timeLeft < 300 ? "border-rose-500/40 text-rose-500 animate-pulse" : "border-white/10"
                    )}>
                        <Timer size={22} className={timeLeft < 300 ? "text-rose-500" : "text-primary"} />
                        <span className="font-mono text-3xl font-black tracking-tighter">{formatTime(timeLeft)}</span>
                    </div>

                    <button
                        onClick={handleSubmit}
                        className="btn-primary py-3 px-8 rounded-xl text-[10px] font-black uppercase tracking-widest"
                    >
                        Terminate Session
                    </button>
                </header>

                <div className="flex-1 flex overflow-hidden">
                    <main className="flex-1 p-12 overflow-y-auto custom-scrollbar bg-white/[0.01]">
                        <div className="max-w-4xl mx-auto">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={currentIdx}
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                >
                                    <div className="flex items-center justify-between mb-8">
                                        <div className="flex items-center gap-4">
                                            <div className="w-14 h-14 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-black text-2xl">
                                                {currentIdx + 1}
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-text-dim font-black uppercase tracking-widest mb-1">Current Question Trace</div>
                                                <div className="flex gap-2">
                                                    <span className="px-3 py-1 bg-primary/10 border border-primary/20 rounded-lg text-[10px] font-black text-primary uppercase">{currentQ.section || 'SECTION A'}</span>
                                                    <span className="px-3 py-1 bg-white/5 border border-white/10 rounded-lg text-[10px] font-black text-white/40 uppercase">{currentQ.topic || 'General Topic'}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <button
                                            onClick={toggleFlag}
                                            className={clsx(
                                                "p-4 rounded-2xl border transition-all",
                                                flags[currentQ.id] ? "bg-amber-500/20 border-amber-500/40 text-amber-500" : "glass border-transparent hover:bg-white/5 text-white/20"
                                            )}
                                        >
                                            <Flag size={24} fill={flags[currentQ.id] ? "currentColor" : "none"} />
                                        </button>
                                    </div>

                                    <div className="glass p-12 rounded-[40px] border border-white/5 mb-8 shadow-2xl">
                                        <h2 className="text-3xl font-medium leading-relaxed text-white/90">{currentQ.text}</h2>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {currentQ.choices.length > 0 ? (
                                            currentQ.choices.map((c) => (
                                                <button
                                                    key={c.id}
                                                    onClick={() => handleSelectAnswer(c.label)}
                                                    className={clsx(
                                                        "p-7 rounded-[28px] text-left border transition-all flex items-center gap-6 group relative overflow-hidden",
                                                        answers[currentQ.id] === c.label
                                                            ? "bg-primary/20 border-primary shadow-lg shadow-primary/20"
                                                            : "glass border-white/5 hover:border-white/20 hover:bg-white/[0.04]"
                                                    )}
                                                >
                                                    <div className={clsx(
                                                        "w-12 h-12 rounded-2xl flex items-center justify-center font-black text-sm shrink-0 border transition-all",
                                                        answers[currentQ.id] === c.label
                                                            ? "bg-primary border-primary text-white"
                                                            : "bg-white/5 border-white/10 text-white/40 group-hover:bg-white/10 group-hover:text-white"
                                                    )}>
                                                        {c.label}
                                                    </div>
                                                    <span className="text-xl font-medium tracking-tight text-white/80">{c.text}</span>
                                                </button>
                                            ))
                                        ) : (
                                            <div className="col-span-1 md:col-span-2">
                                                <label className="text-[10px] font-black uppercase text-white/40 mb-3 block">Theory Answer Submission</label>
                                                <textarea
                                                    className="w-full h-64 bg-white/5 border border-white/10 rounded-3xl p-8 text-lg outline-none focus:border-primary/50 transition-all font-medium leading-relaxed"
                                                    placeholder="Input your detailed solution or response here..."
                                                    value={answers[currentQ.id] || ''}
                                                    onChange={e => setAnswers({ ...answers, [currentQ.id]: e.target.value })}
                                                />
                                            </div>
                                        )}
                                    </div>
                                </motion.div>
                            </AnimatePresence>
                        </div>
                    </main>

                    {/* Question Navigator */}
                    <aside className="w-[400px] glass border-l border-white/5 p-10 flex flex-col shrink-0 overflow-hidden">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="font-black text-[10px] uppercase tracking-[0.2em] text-white/30">Session Progress</h3>
                            <div className="text-[10px] font-black text-primary px-3 py-1.5 bg-primary/10 rounded-xl">
                                {Object.keys(answers).length} / {questions.length} RESOLVED
                            </div>
                        </div>

                        <div className="grid grid-cols-5 gap-3 mb-10 overflow-y-auto custom-scrollbar pr-3">
                            {questions.map((q, i) => (
                                <button
                                    key={q.id}
                                    onClick={() => setCurrentIdx(i)}
                                    className={clsx(
                                        "aspect-square rounded-2xl border flex items-center justify-center font-black text-xs transition-all",
                                        currentIdx === i ? "bg-primary/20 border-primary text-primary shadow-lg shadow-primary/10 scale-105" :
                                            flags[q.id] ? "bg-amber-500/20 border-amber-500/40 text-amber-500" :
                                                answers[q.id] ? "bg-white/10 border-white/20 text-white" : "glass border-white/5 text-white/20 hover:border-white/20"
                                    )}
                                >
                                    {i + 1}
                                </button>
                            ))}
                        </div>

                        <div className="mt-auto space-y-4 pt-10 border-t border-white/5">
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    disabled={currentIdx === 0}
                                    onClick={() => setCurrentIdx(p => p - 1)}
                                    className="h-16 rounded-3xl glass border border-white/5 flex items-center justify-center hover:bg-white/10 transition-all disabled:opacity-20 group"
                                >
                                    <ChevronLeft className="group-hover:-translate-x-1 transition-transform" /> <span className="font-black text-[10px] uppercase ml-2 tracking-widest">Previous</span>
                                </button>
                                <button
                                    disabled={currentIdx === questions.length - 1}
                                    onClick={() => setCurrentIdx(p => p + 1)}
                                    className="h-16 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 transition-all disabled:opacity-20 group"
                                >
                                    <span className="font-black text-[10px] uppercase mr-2 tracking-widest">Advance</span> <ChevronRight className="group-hover:translate-x-1 transition-transform" />
                                </button>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
        );
    }

    return null;
}

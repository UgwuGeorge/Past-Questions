import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import {
    Timer, ChevronLeft, ChevronRight, Flag, HelpCircle, CheckCircle2,
    XCircle, BookOpen, Layers, ShieldCheck, Zap, BarChart3, Clock, AlertTriangle
} from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000/api`;

export default function CBTProcessor({ userId, examId, subjectId, onExit, difficulty = 'medium', autoStart = false }) {
    const [step, setStep] = useState('config'); // 'config' | 'loading' | 'exam' | 'result'
    const [config, setConfig] = useState({
        questionCount: 40,
        duration: 45, // minutes
        mode: difficulty === 'hard' ? 'hardcore' : 'standard',
        subjectId: subjectId || null,
        section: 'Section A: Multiple Choice'
    });

    // Update config when props change
    useEffect(() => {
        if (subjectId) {
            setConfig(prev => ({
                ...prev,
                subjectId: subjectId,
                mode: difficulty === 'hard' ? 'hardcore' : 'standard'
            }));
        }
    }, [subjectId, difficulty]);

    const [subjects, setSubjects] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [sessionData, setSessionData] = useState(null);
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState({});
    const [flags, setFlags] = useState({});
    const [timeLeft, setTimeLeft] = useState(0);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [results, setResults] = useState(null);
    const [analysis, setAnalysis] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    // Fetch subjects for config
    useEffect(() => {
        if (!examId) return;
        fetch(`${API_BASE}/exams/${examId}/subjects`)
            .then(r => r.json())
            .then(data => {
                const fetchedSubjects = Array.isArray(data) ? data : [];
                setSubjects(fetchedSubjects);

                if (autoStart) {
                    // Small delay to ensure state and props are settled
                    setTimeout(() => startSimulation(), 600);
                }
            })
            .catch(err => console.error("Failed to fetch subjects:", err));
    }, [examId, autoStart, subjectId]);

    // Timer logic
    useEffect(() => {
        if (step !== 'exam' || !timeLeft || timeLeft <= 0) {
            if (step === 'exam' && timeLeft <= 0) handleAutoSubmit();
            return;
        }
        const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
        return () => clearInterval(timer);
    }, [step, timeLeft]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const startSimulation = async () => {
        // Use the prop subjectId if available, else first subject, else config
        const finalSubjectId = subjectId || (subjects.length > 0 ? subjects[0].id : config.subjectId);

        if (!finalSubjectId) {
            setError("No subject selected. Please choose a subject to continue.");
            return;
        }

        setStep('loading');
        try {
            const res = await fetch(`${API_BASE}/simulation/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    exam_id: examId,
                    subject_id: finalSubjectId,
                    question_count: config.questionCount,
                    duration_minutes: config.duration,
                    section: config.section
                })
            });
            const data = await res.json();
            if (data.detail) throw new Error(data.detail);

            setQuestions(data.questions);
            setSessionData(data);
            setTimeLeft(data.duration_seconds);
            setStep('exam');
        } catch (err) {
            setError(err.message);
            setStep('config');
        }
    };

    const handleAutoSubmit = () => {
        if (isSubmitting) return;
        submitExam();
    };

    const submitExam = async () => {
        setIsSubmitting(true);
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
            setResults(data);
            setStep('result');
        } catch (err) {
            console.error("Submission failed:", err);
            alert("Connection lost. Retrying submission...");
        } finally {
            setIsSubmitting(false);
        }
    };

    const requestAnalysis = async () => {
        if (!sessionData?.session_id || isAnalyzing) return;
        setIsAnalyzing(true);
        try {
            const res = await fetch(`${API_BASE}/simulation/${sessionData.session_id}/analyze`);
            const data = await res.json();
            setAnalysis(data);
        } catch (err) {
            console.error("Analysis failed:", err);
        } finally {
            setIsAnalyzing(false);
        }
    };

    // UI Renderers
    if (step === 'config') {
        return (
            <div className="h-full flex flex-col items-center justify-center max-w-4xl mx-auto py-10">
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full">
                    <div className="flex items-center gap-4 mb-10">
                        <button onClick={onExit} className="p-2 mr-2 hover:bg-white/5 rounded-lg transition-colors border border-white/5 glass">
                            <ChevronLeft size={20} />
                        </button>
                        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
                            <ShieldCheck size={32} className="text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-black italic tracking-tighter uppercase">Exam Simulation Engine</h1>
                            <p className="text-text-dim text-sm">Configure your proctored practice session</p>
                        </div>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex gap-3 text-rose-500 text-sm font-bold items-start">
                            <AlertTriangle size={18} className="shrink-0 mt-0.5" />
                            <p>{error}</p>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                        <GlowCard className="p-8">
                            <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                                <Layers size={18} className="text-primary" /> Parameters
                            </h3>
                            <div className="space-y-6">
                                <div>
                                    <label className="text-[10px] font-black uppercase text-white/40 block mb-2 tracking-widest">Subject Focus</label>
                                    <select
                                        className="w-full bg-white/5 border border-white/10 rounded-xl p-3 outline-none focus:border-primary/50"
                                        value={config.subjectId || ''}
                                        onChange={e => setConfig({ ...config, subjectId: e.target.value ? parseInt(e.target.value) : null })}
                                    >
                                        <option value="">All Subjects (Diagnostic Mix)</option>
                                        {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                                    </select>
                                </div>
                                    <div>
                                        <label className="text-[10px] font-black uppercase text-white/40 block mb-2 tracking-widest">Exam Section</label>
                                        <select
                                            className="w-full bg-white/5 border border-white/10 rounded-xl p-3 outline-none focus:border-primary/50"
                                            value={config.section}
                                            onChange={e => {
                                                const newSection = e.target.value;
                                                const isIcan = subjects[0]?.exam_name?.includes('ICAN');
                                                let updates = { section: newSection };
                                                
                                                if (isIcan && newSection === 'Section A: Multiple Choice') {
                                                    updates.questionCount = 20;
                                                    updates.duration = 45; // 45 mins for Section A
                                                } else {
                                                    updates.questionCount = 40;
                                                    updates.duration = 60;
                                                }
                                                setConfig({ ...config, ...updates });
                                            }}
                                        >
                                            <option value="Section A: Multiple Choice">Section A (MCQs)</option>
                                            <option value="Full Exam">Mixed Practice</option>
                                        </select>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="text-[10px] font-black uppercase text-white/40 block mb-2 tracking-widest">Questions</label>
                                            <input
                                                type="number"
                                                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 outline-none"
                                                value={config.questionCount}
                                                onChange={e => setConfig({ ...config, questionCount: parseInt(e.target.value) })}
                                            />
                                        </div>
                                        <div>
                                            <label className="text-[10px] font-black uppercase text-white/40 block mb-2 tracking-widest">Time (Mins)</label>
                                            <input
                                                type="number"
                                                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 outline-none"
                                                value={config.duration}
                                                onChange={e => setConfig({ ...config, duration: parseInt(e.target.value) })}
                                            />
                                        </div>
                                    </div>
                            </div>
                        </GlowCard>

                        <GlowCard className="p-8">
                            <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                                <Zap size={18} className="text-secondary" /> Practice Mode
                            </h3>
                            <div className="space-y-4">
                                {[
                                    { id: 'practice', name: 'Open Practice', desc: 'No timer pressure, hints allowed.', color: 'emerald' },
                                    { id: 'standard', name: 'Standard Exam', desc: 'Real-time simulation, full proctoring.', color: 'primary' },
                                    { id: 'hardcore', name: 'Hardcore', desc: '50% less time, penalty for skips.', color: 'rose' },
                                ].map(mode => (
                                    <button
                                        key={mode.id}
                                        onClick={() => setConfig({ ...config, mode: mode.id })}
                                        className={clsx(
                                            "w-full p-4 rounded-xl border text-left transition-all",
                                            config.mode === mode.id ? "bg-white/10 border-white/20" : "border-transparent hover:bg-white/5"
                                        )}
                                    >
                                        <div className="flex items-center gap-2 mb-1">
                                            <div className={`w-2 h-2 rounded-full bg-${mode.color}-400`} />
                                            <span className="font-bold text-sm">{mode.name}</span>
                                        </div>
                                        <p className="text-[10px] text-text-dim">{mode.desc}</p>
                                    </button>
                                ))}
                            </div>
                        </GlowCard>
                    </div>

                    <button
                        onClick={startSimulation}
                        className="btn-primary w-full py-5 text-lg font-black uppercase tracking-widest shadow-2xl shadow-primary/20 hover:scale-[1.01] transition-all"
                    >
                        Initialize Simulation Session
                    </button>
                </motion.div>
            </div>
        );
    }

    if (step === 'loading') {
        return (
            <div className="h-full flex flex-col items-center justify-center bg-background">
                <div className="relative">
                    <div className="w-32 h-32 border-4 border-primary/20 rounded-full animate-pulse" />
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                    </div>
                </div>
                <h2 className="text-xl font-black mt-8 tracking-widest uppercase">Fetching Dynamic Data</h2>
                <p className="text-text-dim italic">Synthesizing exam parameters from Reharz Core...</p>
            </div>
        );
    }

    if (step === 'exam') {
        const currentQ = questions[currentIdx];
        const isAnswered = !!answers[currentQ.id];

        return (
            <div className="h-screen fixed inset-0 z-[100] bg-background flex flex-col overflow-hidden">
                {/* Proctored Header */}
                <header className="glass h-20 px-8 flex justify-between items-center border-b border-white/5 shrink-0">
                    <div className="flex items-center gap-6">
                        <div className="bg-rose-500/10 border border-rose-500/20 px-3 py-1 rounded-full flex items-center gap-2">
                            <div className="w-2 h-2 bg-rose-500 rounded-full animate-pulse" />
                            <span className="text-[10px] font-black text-rose-500 uppercase tracking-widest">Live Proctoring</span>
                        </div>
                        <div>
                            <h2 className="font-black text-sm uppercase tracking-wider">{subjects.find(s => s.id === config.subjectId)?.name || 'Full Exam Simulation'}</h2>
                            <div className="flex gap-4 text-[10px] text-text-dim font-black">
                                <span>{questions.length} QUESTIONS TOTAL</span>
                                <span>STATION: REHARZ-ZETA</span>
                            </div>
                        </div>
                    </div>

                    <div className={clsx(
                        "flex items-center gap-4 px-8 py-2 rounded-2xl glass border-2 transition-all duration-500",
                        timeLeft < 300 ? "border-rose-500/40 text-rose-500 animate-pulse bg-rose-500/5 shadow-lg shadow-rose-500/20" : "border-white/10"
                    )}>
                        <Timer size={20} className={timeLeft < 300 ? "text-rose-500" : "text-primary"} />
                        <span className="font-mono text-3xl font-black tracking-tighter">{formatTime(timeLeft)}</span>
                    </div>

                    <button
                        onClick={submitExam}
                        disabled={isSubmitting}
                        className="btn-primary px-8 h-12 rounded-xl text-xs font-black uppercase tracking-widest shadow-xl shadow-primary/20"
                    >
                        {isSubmitting ? 'Processing Submission...' : 'Terminate Session'}
                    </button>
                </header>

                <div className="flex-1 flex overflow-hidden">
                    {/* Main Workspace */}
                    <main className="flex-1 overflow-y-auto custom-scrollbar p-12 bg-white/[0.01]">
                        <div className="max-w-4xl mx-auto">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={currentIdx}
                                    initial={{ opacity: 0, x: 10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -10 }}
                                >
                                    <div className="flex items-center justify-between mb-8">
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-black text-xl">
                                                {currentIdx + 1}
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-text-dim font-black uppercase tracking-widest mb-1">Current Question Context</div>
                                                <div className="flex gap-2">
                                                    <span className="px-2 py-0.5 bg-primary/10 border border-primary/20 rounded text-[10px] font-black text-primary uppercase">{currentQ.section || 'General Section'}</span>
                                                    <span className="px-2 py-0.5 bg-white/5 border border-white/10 rounded text-[10px] font-bold text-white/40">{currentQ.topic || 'General'}</span>
                                                    <span className="px-2 py-0.5 bg-white/5 border border-white/10 rounded text-[10px] font-bold text-white/40 uppercase">{currentQ.difficulty}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => setFlags({ ...flags, [currentQ.id]: !flags[currentQ.id] })}
                                            className={clsx(
                                                "p-3 rounded-xl border transition-all",
                                                flags[currentQ.id] ? "bg-amber-500/20 border-amber-500/40 text-amber-500" : "glass border-transparent hover:bg-white/5"
                                            )}
                                        >
                                            <Flag size={20} fill={flags[currentQ.id] ? "currentColor" : "none"} />
                                        </button>
                                    </div>

                                    <div className="glass p-10 rounded-[32px] border border-white/5 mb-10 shadow-2xl">
                                        <h3 className="text-2xl font-medium leading-relaxed text-white/90">
                                            {currentQ.text}
                                        </h3>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {currentQ.choices.map((choice) => (
                                            <button
                                                key={choice.id}
                                                onClick={() => setAnswers({ ...answers, [currentQ.id]: choice.label })}
                                                className={clsx(
                                                    "p-6 rounded-2xl text-left border transition-all flex items-center gap-5 group relative overflow-hidden",
                                                    answers[currentQ.id] === choice.label
                                                        ? "bg-primary/20 border-primary shadow-lg shadow-primary/20"
                                                        : "glass border-white/5 hover:border-white/20 hover:bg-white/[0.04]"
                                                )}
                                            >
                                                {answers[currentQ.id] === choice.label && (
                                                    <div className="absolute right-4 top-4">
                                                        <CheckCircle2 size={18} className="text-primary" />
                                                    </div>
                                                )}
                                                <div className={clsx(
                                                    "w-10 h-10 rounded-xl flex items-center justify-center font-black text-sm shrink-0 border transition-colors",
                                                    answers[currentQ.id] === choice.label
                                                        ? "bg-primary border-primary text-white"
                                                        : "bg-white/5 border-white/10 text-white/40 group-hover:text-white"
                                                )}>
                                                    {choice.label}
                                                </div>
                                                <span className="text-lg font-medium tracking-tight text-white/80">{choice.text}</span>
                                            </button>
                                        ))}
                                    </div>
                                </motion.div>
                            </AnimatePresence>
                        </div>
                    </main>

                    {/* Navigation Sidebar */}
                    <aside className="w-[380px] glass border-l border-white/5 p-8 flex flex-col overflow-hidden shrink-0">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="font-black text-xs uppercase tracking-[0.2em] text-white/30">Examination Map</h3>
                            <div className="text-[10px] font-black text-primary px-2 py-1 bg-primary/10 rounded-lg">
                                {Object.keys(answers).length} / {questions.length} DONE
                            </div>
                        </div>

                        <div className="grid grid-cols-5 gap-3 mb-10 overflow-y-auto custom-scrollbar pr-2">
                            {questions.map((q, i) => (
                                <button
                                    key={q.id}
                                    onClick={() => setCurrentIdx(i)}
                                    className={clsx(
                                        "aspect-square rounded-xl border flex items-center justify-center font-black text-sm transition-all",
                                        currentIdx === i ? "bg-primary/20 border-primary text-primary shadow-lg shadow-primary/10 scale-105" :
                                            flags[q.id] ? "bg-amber-500/20 border-amber-500/40 text-amber-500" :
                                                answers[q.id] ? "bg-white/10 border-white/20 text-white" : "glass border-white/5 text-white/30 hover:border-white/20"
                                    )}
                                >
                                    {i + 1}
                                </button>
                            ))}
                        </div>

                        <div className="mt-auto pt-8 border-t border-white/5 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    disabled={currentIdx === 0}
                                    onClick={() => setCurrentIdx(p => p - 1)}
                                    className="h-14 rounded-2xl glass border border-white/5 flex items-center justify-center hover:bg-white/10 transition-all disabled:opacity-20"
                                >
                                    <ChevronLeft /> <span className="font-black text-xs uppercase ml-2">Prev</span>
                                </button>
                                <button
                                    disabled={currentIdx === questions.length - 1}
                                    onClick={() => setCurrentIdx(p => p + 1)}
                                    className="h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 transition-all disabled:opacity-20"
                                >
                                    <span className="font-black text-xs uppercase mr-2">Next</span> <ChevronRight />
                                </button>
                            </div>

                            <GlowCard className="p-5 flex items-start gap-4 bg-amber-500/5 border-amber-500/10">
                                <AlertTriangle className="text-amber-500 shrink-0" size={18} />
                                <div>
                                    <div className="text-[10px] font-black text-amber-500 uppercase tracking-widest mb-1">Proctor's Note</div>
                                    <p className="text-[10px] text-white/40 leading-relaxed italic">Avoid refreshing. The system logs all session movements for integrity analysis.</p>
                                </div>
                            </GlowCard>
                        </div>
                    </aside>
                </div>
            </div>
        );
    }

    if (step === 'result') {
        return (
            <div className="h-full flex flex-col items-center justify-center p-10 max-w-5xl mx-auto">
                <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="w-full">
                    <div className="text-center mb-16">
                        <div className="w-24 h-24 bg-primary/10 rounded-[32px] flex items-center justify-center mx-auto mb-6 border border-primary/20">
                            <CheckCircle2 size={48} className="text-primary" />
                        </div>
                        <h1 className="text-5xl font-black italic tracking-tighter uppercase mb-4">Simulation Certified.</h1>
                        <p className="text-text-dim max-w-md mx-auto">The Reharz engine has evaluated your performance on {exams.find(e => e.id === examId)?.name} {config.section}.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                        <div className="glass p-8 rounded-[32px] border border-white/5 text-center">
                            <div className="text-4xl font-black mb-2 text-primary">{Math.round(results.correct / results.total * 100)}%</div>
                            <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Aggregate Score</div>
                        </div>
                        <div className="glass p-8 rounded-[32px] border border-white/5 text-center">
                            <div className="text-4xl font-black mb-2">{results.correct} / {results.total}</div>
                            <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Accuracy</div>
                        </div>
                        <div className="glass p-8 rounded-[32px] border border-white/5 text-center">
                            <div className="text-4xl font-black mb-2 text-secondary">{Math.floor(results.duration_seconds / 60)}m</div>
                            <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Time Used</div>
                        </div>
                        <div className="glass p-8 rounded-[32px] border border-white/5 text-center">
                            <div className="text-4xl font-black mb-2 text-accent">Lvl 4</div>
                            <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Performance</div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
                        <GlowCard className="p-10">
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-8 flex items-center gap-2">
                                <BarChart3 size={14} className="text-primary" /> Topic Mastery Breakdown
                            </h3>
                            <div className="space-y-6">
                                {Object.entries(results.topics).map(([topic, stats]) => {
                                    const p = stats.total > 0 ? (stats.correct / stats.total) * 100 : 0;
                                    return (
                                        <div key={topic}>
                                            <div className="flex justify-between text-[11px] font-black mb-2 uppercase tracking-tight">
                                                <span>{topic}</span>
                                                <span className={clsx(p >= 60 ? "text-emerald-400" : "text-rose-400")}>{Math.round(p)}%</span>
                                            </div>
                                            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                                                <motion.div
                                                    initial={{ width: 0 }}
                                                    animate={{ width: `${p}%` }}
                                                    className={clsx("h-full rounded-full transition-all", p >= 60 ? "bg-emerald-500" : "bg-rose-500")}
                                                />
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </GlowCard>

                        <GlowCard className="p-10 bg-primary/[0.02] flex flex-col h-full">
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-8 flex items-center gap-2">
                                <Clock size={14} className="text-primary" /> Session Insights
                            </h3>

                            {!analysis ? (
                                <>
                                    <div className="space-y-4 flex-1">
                                        <div className="flex items-center gap-4 p-4 glass rounded-2xl border border-white/5">
                                            <Zap size={20} className="text-primary" />
                                            <div>
                                                <div className="text-xs font-bold">Fastest Response</div>
                                                <div className="text-[10px] text-text-dim">Topic: {Object.keys(results.topics)[0] || 'N/A'}</div>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4 p-4 glass rounded-2xl border border-white/5">
                                            <AlertTriangle size={20} className="text-rose-400" />
                                            <div>
                                                <div className="text-xs font-bold">Weak Topic Detected</div>
                                                <div className="text-[10px] text-text-dim">Recommendation: Focus on {Object.entries(results.topics).sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))[0]?.[0] || 'N/A'}</div>
                                            </div>
                                        </div>
                                    </div>
                                    <button
                                        onClick={requestAnalysis}
                                        disabled={isAnalyzing}
                                        className="w-full mt-10 py-4 bg-primary/20 border border-primary/40 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] hover:bg-primary/30 transition-all text-primary flex items-center justify-center gap-2"
                                    >
                                        {isAnalyzing ? (
                                            <>
                                                <div className="w-4 h-4 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
                                                Synthesizing Strategy...
                                            </>
                                        ) : (
                                            <>
                                                <Sparkles size={14} /> Request AI Strategy Breakdown
                                            </>
                                        )}
                                    </button>
                                </>
                            ) : (
                                <div className="space-y-6 flex-1 overflow-y-auto custom-scrollbar pr-2">
                                    <div>
                                        <div className="text-[10px] font-black text-primary uppercase tracking-widest mb-2">Proctor Summary</div>
                                        <p className="text-sm italic leading-relaxed text-white/70">"{analysis.overall_assessment}"</p>
                                    </div>

                                    <div>
                                        <div className="text-[10px] font-black text-emerald-400 uppercase tracking-widest mb-2">Strong Assets</div>
                                        <div className="flex flex-wrap gap-2">
                                            {analysis.strong_topics.map((t, idx) => (
                                                <span key={idx} className="px-2 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded text-[10px] font-bold text-emerald-400 uppercase">{t}</span>
                                            ))}
                                        </div>
                                    </div>

                                    <div>
                                        <div className="text-[10px] font-black text-rose-400 uppercase tracking-widest mb-2">Strategic Gaps</div>
                                        <div className="flex flex-wrap gap-2">
                                            {analysis.critical_gaps.map((t, idx) => (
                                                <span key={idx} className="px-2 py-1 bg-rose-500/10 border border-rose-500/20 rounded text-[10px] font-bold text-rose-400 uppercase">{t}</span>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="pt-4 border-t border-white/5">
                                        <div className="text-[10px] font-black text-white/40 uppercase tracking-widest mb-3">Action Plan</div>
                                        <ul className="space-y-2">
                                            {analysis.action_plan.map((step, idx) => (
                                                <li key={idx} className="text-xs text-white/60 flex items-start gap-2">
                                                    <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                                                    {step}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    <p className="text-[10px] font-bold italic text-white/20 pt-4 border-t border-white/5">{analysis.encouragement}</p>
                                </div>
                            )}
                        </GlowCard>
                    </div>

                    <button
                        onClick={onExit}
                        className="btn-primary w-full py-5 text-sm font-black uppercase tracking-widest shadow-2xl shadow-primary/20"
                    >
                        Archive and Return to Command Center
                    </button>
                </motion.div>
            </div>
        );
    }

    return null;
}

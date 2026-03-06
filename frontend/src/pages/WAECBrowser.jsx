import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { ChevronLeft, ChevronRight, CheckCircle2, Flag, Timer, BookOpen, Layers, XCircle } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";

export default function WAECBrowser({ onExit, examId: propExamId }) {
    const [view, setView] = useState('subjects'); // subjects | years | exam | results
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState(null);
    const [selectedYear, setSelectedYear] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Exam state
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState({});
    const [flags, setFlags] = useState({});
    const [timeLeft, setTimeLeft] = useState(3600);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const examId = propExamId || 10; // Use prop or default to 10 (which is WAEC now)

    useEffect(() => {
        const fetchSubjects = async () => {
            setLoading(true);
            try {
                const res = await fetch(`${API_BASE}/exams/${examId}/subjects`);
                if (!res.ok) throw new Error("Could not load WAEC subjects");
                const data = await res.json();
                setSubjects(Array.isArray(data) ? data : []);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchSubjects();
    }, []);

    // Timer countdown
    useEffect(() => {
        if (view !== 'exam' || isSubmitted) return;
        const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
        return () => clearInterval(timer);
    }, [view, isSubmitted]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const handleSelectSubject = (subjectItem) => {
        setSelectedSubject(subjectItem);
        setView('years');
    };

    const handleSelectYear = async (yearStr) => {
        setSelectedYear(yearStr);
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE}/subjects/${selectedSubject.id}/questions?limit=50`);
            const data = await res.json();

            const filtered = Array.isArray(data) ? data.filter(q => !yearStr || q.year == parseInt(yearStr) || !q.year) : [];

            // Normalize choices
            const normalized = filtered.map(q => ({
                ...q,
                choices: Array.isArray(q.choices)
                    ? q.choices.reduce((acc, c) => ({ ...acc, [c.label]: c.text }), {})
                    : q.choices,
                answer: (q.choices.find(c => c.is_correct) || {}).label || 'A'
            }));

            setQuestions(normalized);
            setCurrentIdx(0);
            setAnswers({});
            setFlags({});
            setIsSubmitted(false);
            setTimeLeft(3600);
            setView('exam');
            setLoading(false);
        } catch (err) {
            setError("Failed to load questions");
            setLoading(false);
        }
    };

    const handleSelectAnswer = (label) => {
        setAnswers(prev => ({ ...prev, [currentIdx]: label }));
    };

    const toggleFlag = () => {
        setFlags(prev => ({ ...prev, [currentIdx]: !prev[currentIdx] }));
    };

    const handleSubmit = () => {
        setIsSubmitted(true);
        setView('results');
    };

    const calculateScore = () => {
        let score = 0;
        questions.forEach((q, i) => {
            if (answers[i] === q.answer) score++;
        });
        return score;
    };

    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-6" />
                    <p className="text-text-dim font-medium">Loading Complete WAEC Archive...</p>
                </div>
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
                    <button onClick={onExit} className="btn-primary w-full justify-center">Back to Dashboard</button>
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
                        <h1 className="text-xl font-bold flex items-center gap-2">
                            <Layers size={20} className="text-primary" />
                            WAEC Subject Archive
                        </h1>
                        <p className="text-xs text-text-dim">Select a subject to practice past questions</p>
                    </div>
                </header>
                <div className="p-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 max-w-5xl mx-auto w-full">
                    {subjects.map((sub, i) => (
                        <motion.button
                            key={sub.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            onClick={() => handleSelectSubject(sub)}
                            className="glass rounded-3xl p-7 text-left border border-white/5 hover:border-primary/40 hover:bg-white/[0.04] transition-all group"
                        >
                            <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-colors">
                                <BookOpen className="text-primary" size={22} />
                            </div>
                            <h3 className="text-xl font-bold mb-2">{sub.name}</h3>
                            <p className="text-xs text-text-dim">Multi-Year Practice Dataset</p>
                        </motion.button>
                    ))}
                </div>
            </div>
        );
    }

    if (view === 'years') {
        return (
            <div className="h-screen flex flex-col bg-background overflow-y-auto">
                <header className="glass px-8 py-5 flex items-center gap-4 border-b border-white/5 sticky top-0 z-10">
                    <button onClick={() => setView('subjects')} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold flex items-center gap-2">
                            WAEC {selectedSubject.name}
                        </h1>
                        <p className="text-xs text-text-dim">Select a Year</p>
                    </div>
                </header>
                <div className="p-10 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 max-w-5xl mx-auto w-full">
                    {['2023', '2022', '2021', '2020', '2019', '2018'].map((year, i) => (
                        <motion.button
                            key={year}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: i * 0.02 }}
                            onClick={() => handleSelectYear(year)}
                            className="glass rounded-2xl p-5 text-center transition-all border border-white/5 hover:border-primary/40 hover:opacity-100 hover:-translate-y-1"
                        >
                            <div className="text-2xl font-black text-white/90">{year}</div>
                            <div className="text-[10px] text-text-dim mt-1 uppercase tracking-wider">Document Set</div>
                        </motion.button>
                    ))}
                    <motion.button
                        onClick={() => handleSelectYear(null)}
                        className="glass rounded-2xl p-5 text-center transition-all border border-white/5 hover:border-primary/40 hover:opacity-100 hover:-translate-y-1 col-span-2"
                    >
                        <div className="text-xl font-black text-white/90">Complete Archive</div>
                        <div className="text-[10px] text-text-dim mt-1 uppercase tracking-wider">All years</div>
                    </motion.button>
                </div>
            </div>
        );
    }

    if (view === 'results') {
        const score = calculateScore();
        const pct = Math.round((score / questions.length) * 100) || 0;
        return (
            <div className="min-h-screen flex items-center justify-center p-6 bg-background">
                <GlowCard className="max-w-2xl w-full text-center">
                    <CheckCircle2 className="w-20 h-20 text-emerald-500 mx-auto mb-6" />
                    <h1 className="text-4xl font-bold mb-2">WAEC Completed!</h1>
                    <p className="text-text-dim mb-10">{selectedSubject.name} - {selectedYear || 'Archive'}</p>
                    <div className="grid grid-cols-3 gap-5 mb-10">
                        <div className="glass p-6 rounded-2xl">
                            <div className="text-4xl font-bold text-primary">{score}/{questions.length}</div>
                            <div className="text-xs text-text-dim mt-2 uppercase tracking-wider">Score</div>
                        </div>
                        <div className="glass p-6 rounded-2xl">
                            <div className={clsx("text-4xl font-bold", pct >= 60 ? "text-emerald-400" : "text-rose-400")}>{pct}%</div>
                            <div className="text-xs text-text-dim mt-2 uppercase tracking-wider">Accuracy</div>
                        </div>
                        <div className="glass p-6 rounded-2xl">
                            <div className="text-4xl font-bold text-accent">{Object.keys(flags).length}</div>
                            <div className="text-xs text-text-dim mt-2 uppercase tracking-wider">Flagged</div>
                        </div>
                    </div>
                    {/* Review answers */}
                    <div className="text-left space-y-4 mb-10 max-h-60 overflow-y-auto pr-2">
                        {questions.map((q, i) => {
                            const userAnswer = answers[i];
                            const isOk = q.answer === userAnswer;
                            return (
                                <div key={i} className={clsx("p-4 rounded-xl border text-sm", isOk ? "border-emerald-500/20 bg-emerald-500/5" : "border-rose-500/20 bg-rose-500/5")}>
                                    <div className="font-medium mb-1 line-clamp-2">{i + 1}. {q.text}</div>
                                    <div className="text-xs text-text-dim mb-1">
                                        Your answer: <span className={clsx("font-bold", isOk ? "text-emerald-400" : "text-rose-400")}>{userAnswer || 'Skipped'}</span>
                                        {!isOk && <> · Correct: <span className="font-bold text-emerald-400">{q.answer}</span></>}
                                    </div>
                                    {q.explanation && (
                                        <div className="text-xs text-white/60 italic border-l-2 border-white/20 pl-2 mt-2">{q.explanation}</div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                    <button onClick={() => setView('years')} className="btn-primary w-full justify-center text-sm">Return to Years</button>
                </GlowCard>
            </div>
        );
    }

    if (view === 'exam') {
        if (!questions.length) {
            return (
                <div className="h-screen flex items-center justify-center">
                    <div className="text-center">
                        <p className="text-white mb-4">No questions explicitly documented for this year.</p>
                        <button onClick={() => setView('years')} className="btn-secondary">Go Back</button>
                    </div>
                </div>
            )
        }

        const currentQ = questions[currentIdx];
        return (
            <div className="h-screen flex flex-col overflow-hidden bg-background">
                <header className="glass px-8 py-4 flex justify-between items-center border-b border-white/5 shrink-0">
                    <div className="flex items-center gap-4">
                        <button onClick={() => setView('years')} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                            <ChevronLeft />
                        </button>
                        <div>
                            <span className="font-bold text-base">WAEC {selectedSubject.name} ({selectedYear || 'Archive'})</span>
                            <p className="text-xs text-text-dim">{questions.length} Questions</p>
                        </div>
                    </div>
                    <div className={clsx(
                        "flex items-center gap-3 px-6 py-2 rounded-full glass border",
                        timeLeft < 300 ? "border-red-500/50 text-red-500 animate-pulse" : "border-primary/20 text-primary"
                    )}>
                        <Timer size={18} />
                        <span className="font-mono text-xl font-bold">{formatTime(timeLeft)}</span>
                    </div>
                    <button
                        onClick={handleSubmit}
                        className="btn-primary py-2 px-6"
                    >
                        Submit Exam
                    </button>
                </header>

                <div className="flex-1 flex overflow-hidden">
                    {/* Question Area */}
                    <div className="flex-1 p-10 overflow-y-auto">
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={currentIdx}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="max-w-3xl mx-auto"
                            >
                                <div className="flex items-center gap-4 mb-6">
                                    <span className="text-primary font-bold text-2xl">Question {currentIdx + 1}</span>
                                    {flags[currentIdx] && <Flag className="text-amber-500 fill-amber-500" size={18} />}
                                </div>

                                <h2 className="text-xl leading-relaxed mb-10 text-white/90">{currentQ.text}</h2>

                                <div className="space-y-4">
                                    {Object.entries(currentQ.choices).map(([label, text]) => (
                                        <button
                                            key={label}
                                            onClick={() => handleSelectAnswer(label)}
                                            className={clsx(
                                                "w-full p-5 rounded-2xl text-left border transition-all flex items-center gap-4 group",
                                                answers[currentIdx] === label
                                                    ? "bg-primary/20 border-primary shadow-lg shadow-primary/10"
                                                    : "glass border-transparent hover:border-white/20"
                                            )}
                                        >
                                            <div className={clsx(
                                                "w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm shrink-0",
                                                answers[currentIdx] === label
                                                    ? "bg-primary text-white"
                                                    : "bg-white/5 text-text-dim group-hover:bg-white/10"
                                            )}>
                                                {label}
                                            </div>
                                            <span className="leading-relaxed">{text}</span>
                                        </button>
                                    ))}
                                </div>
                            </motion.div>
                        </AnimatePresence>
                    </div>

                    {/* Navigator Sidebar */}
                    <aside className="w-72 glass border-l border-white/5 p-7 flex flex-col shrink-0">
                        <h3 className="font-bold mb-5 flex items-center gap-2 text-sm uppercase tracking-wider text-text-dim">
                            Question Navigator
                        </h3>
                        <div className="grid grid-cols-5 gap-2 flex-1 overflow-y-auto content-start">
                            {questions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => setCurrentIdx(i)}
                                    className={clsx(
                                        "aspect-square rounded-xl flex items-center justify-center font-bold text-sm transition-all border",
                                        currentIdx === i ? "border-primary bg-primary/20 text-primary" :
                                            answers[i] ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400" :
                                                flags[i] ? "bg-amber-500/10 border-amber-500/50 text-amber-400" :
                                                    "glass border-white/5 text-text-dim hover:border-white/20"
                                    )}
                                >
                                    {i + 1}
                                </button>
                            ))}
                        </div>

                        <div className="mt-6 space-y-3">
                            <button onClick={toggleFlag} className="btn-secondary w-full justify-center text-sm">
                                <Flag size={16} className={flags[currentIdx] ? "fill-amber-500 text-amber-500" : ""} />
                                {flags[currentIdx] ? "Unflag" : "Flag for Review"}
                            </button>
                            <div className="flex gap-3">
                                <button
                                    disabled={currentIdx === 0}
                                    onClick={() => setCurrentIdx(i => i - 1)}
                                    className="btn-secondary flex-1 justify-center disabled:opacity-30"
                                >
                                    <ChevronLeft size={18} /> Prev
                                </button>
                                <button
                                    disabled={currentIdx === questions.length - 1}
                                    onClick={() => setCurrentIdx(i => i + 1)}
                                    className="btn-primary flex-1 justify-center disabled:opacity-30"
                                >
                                    Next <ChevronRight size={18} />
                                </button>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
        );
    }
}

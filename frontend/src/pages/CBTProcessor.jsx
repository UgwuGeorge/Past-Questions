import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { Timer, ChevronLeft, ChevronRight, Flag, HelpCircle, CheckCircle2, XCircle, BookOpen, Layers } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";
const USER_ID = 1;

export default function CBTProcessor({ examId, onExit }) {
    const [step, setStep] = useState('select-subject'); // 'select-subject' | 'exam' | 'result'
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState({});
    const [flags, setFlags] = useState({});
    const [timeLeft, setTimeLeft] = useState(3600);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    // Fetch subjects for the selected exam
    useEffect(() => {
        if (!examId) return;
        setLoading(true);
        fetch(`${API_BASE}/exams/${examId}/subjects`)
            .then(r => r.json())
            .then(data => {
                if (data.detail) throw new Error(data.detail);
                setSubjects(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, [examId]);

    // Fetch questions when subject selected
    const handleSubjectSelect = (subject) => {
        setSelectedSubject(subject);
        setLoading(true);
        fetch(`${API_BASE}/subjects/${subject.id}/questions?limit=20`)
            .then(r => r.json())
            .then(data => {
                if (data.detail) throw new Error(data.detail);
                setQuestions(data);
                setStep('exam');
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    };

    // Timer countdown
    useEffect(() => {
        if (step !== 'exam' || isSubmitted) return;
        const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
        return () => clearInterval(timer);
    }, [step, isSubmitted]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const handleSelect = (label) => {
        setAnswers(prev => ({ ...prev, [questions[currentIdx].id]: label }));
    };

    const toggleFlag = () => {
        const qId = questions[currentIdx].id;
        setFlags(prev => ({ ...prev, [qId]: !prev[qId] }));
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        // Log answers to backend
        for (const q of questions) {
            const selectedLabel = answers[q.id];
            if (!selectedLabel) continue;
            const correctChoice = q.choices.find(c => c.is_correct);
            const isCorrect = correctChoice?.label === selectedLabel;
            try {
                await fetch(`${API_BASE}/submit`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: USER_ID,
                        question_id: q.id,
                        selected_label: selectedLabel,
                        is_correct: isCorrect,
                        topic: q.topic || selectedSubject?.name || 'General',
                        difficulty: 'medium'
                    })
                });
            } catch (e) {
                console.error('Failed to submit answer:', e);
            }
        }
        setSubmitting(false);
        setIsSubmitted(true);
    };

    const calculateScore = () => {
        let score = 0;
        questions.forEach(q => {
            const correctChoice = q.choices.find(c => c.is_correct);
            if (correctChoice && answers[q.id] === correctChoice.label) score++;
        });
        return score;
    };

    // ─── Loading / Error State ───────────────────────────────────────────────
    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-6" />
                    <p className="text-text-dim font-medium">Loading from Reharz DB...</p>
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

    // ─── Subject Selection Screen ────────────────────────────────────────────
    if (step === 'select-subject') {
        return (
            <div className="h-screen flex flex-col bg-background overflow-y-auto">
                <header className="glass px-8 py-5 flex items-center gap-4 border-b border-white/5 sticky top-0 z-10">
                    <button onClick={onExit} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold flex items-center gap-2">
                            <Layers size={20} className="text-primary" />
                            Select a Subject
                        </h1>
                        <p className="text-xs text-text-dim">Choose a subject to start your practice session</p>
                    </div>
                </header>
                <div className="p-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 max-w-5xl mx-auto w-full">
                    {subjects.map((subject, i) => (
                        <motion.button
                            key={subject.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.06 }}
                            onClick={() => handleSubjectSelect(subject)}
                            className="glass rounded-3xl p-7 text-left border border-white/5 hover:border-primary/40 hover:bg-white/[0.04] transition-all group"
                        >
                            <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-colors">
                                <BookOpen className="text-primary" size={22} />
                            </div>
                            <h3 className="text-lg font-bold mb-1">{subject.name}</h3>
                            <p className="text-xs text-text-dim">Tap to start practice</p>
                        </motion.button>
                    ))}
                </div>
            </div>
        );
    }

    // ─── Results Screen ──────────────────────────────────────────────────────
    if (isSubmitted) {
        const score = calculateScore();
        const pct = Math.round((score / questions.length) * 100);
        return (
            <div className="min-h-screen flex items-center justify-center p-6 bg-background">
                <GlowCard className="max-w-2xl w-full text-center">
                    <CheckCircle2 className="w-20 h-20 text-emerald-500 mx-auto mb-6" />
                    <h1 className="text-4xl font-bold mb-2">Exam Completed!</h1>
                    <p className="text-text-dim mb-10">Your results have been saved to the Reharz engine.</p>
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
                            const correct = q.choices.find(c => c.is_correct);
                            const userAnswer = answers[q.id];
                            const isOk = correct?.label === userAnswer;
                            return (
                                <div key={q.id} className={clsx("p-4 rounded-xl border text-sm", isOk ? "border-emerald-500/20 bg-emerald-500/5" : "border-rose-500/20 bg-rose-500/5")}>
                                    <div className="font-medium mb-1 line-clamp-2">{i + 1}. {q.text}</div>
                                    <div className="text-xs text-text-dim">
                                        Your answer: <span className={clsx("font-bold", isOk ? "text-emerald-400" : "text-rose-400")}>{userAnswer || 'Skipped'}</span>
                                        {!isOk && <> · Correct: <span className="font-bold text-emerald-400">{correct?.label}</span></>}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    <button onClick={onExit} className="btn-primary w-full justify-center">Return to Dashboard</button>
                </GlowCard>
            </div>
        );
    }

    // ─── Exam Screen ─────────────────────────────────────────────────────────
    const currentQ = questions[currentIdx];
    return (
        <div className="h-screen flex flex-col overflow-hidden bg-background">
            {/* Header */}
            <header className="glass px-8 py-4 flex justify-between items-center border-b border-white/5 shrink-0">
                <div className="flex items-center gap-4">
                    <button onClick={onExit} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <span className="font-bold text-base">{selectedSubject?.name}</span>
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
                    disabled={submitting}
                    className="btn-primary py-2 px-6 disabled:opacity-50"
                >
                    {submitting ? 'Submitting...' : 'Submit Exam'}
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
                                {currentQ.year && <span className="text-xs text-text-dim glass px-3 py-1 rounded-full border border-white/10">{currentQ.year}</span>}
                                {currentQ.topic && <span className="text-xs text-text-dim glass px-3 py-1 rounded-full border border-white/10">{currentQ.topic}</span>}
                                {flags[currentQ.id] && <Flag className="text-amber-500 fill-amber-500" size={18} />}
                            </div>

                            <h2 className="text-xl leading-relaxed mb-10 text-white/90">{currentQ.text}</h2>

                            <div className="space-y-4">
                                {currentQ.choices.map((choice) => (
                                    <button
                                        key={choice.id}
                                        onClick={() => handleSelect(choice.label)}
                                        className={clsx(
                                            "w-full p-5 rounded-2xl text-left border transition-all flex items-center gap-4 group",
                                            answers[currentQ.id] === choice.label
                                                ? "bg-primary/20 border-primary shadow-lg shadow-primary/10"
                                                : "glass border-transparent hover:border-white/20"
                                        )}
                                    >
                                        <div className={clsx(
                                            "w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm shrink-0",
                                            answers[currentQ.id] === choice.label
                                                ? "bg-primary text-white"
                                                : "bg-white/5 text-text-dim group-hover:bg-white/10"
                                        )}>
                                            {choice.label}
                                        </div>
                                        <span className="leading-relaxed">{choice.text}</span>
                                    </button>
                                ))}
                            </div>
                        </motion.div>
                    </AnimatePresence>
                </div>

                {/* Navigator Sidebar */}
                <aside className="w-72 glass border-l border-white/5 p-7 flex flex-col shrink-0">
                    <h3 className="font-bold mb-5 flex items-center gap-2 text-sm uppercase tracking-wider text-text-dim">
                        <HelpCircle size={16} className="text-primary" />
                        Question Navigator
                    </h3>
                    <div className="grid grid-cols-5 gap-2 flex-1 overflow-y-auto content-start">
                        {questions.map((q, i) => (
                            <button
                                key={q.id}
                                onClick={() => setCurrentIdx(i)}
                                className={clsx(
                                    "aspect-square rounded-xl flex items-center justify-center font-bold text-sm transition-all border",
                                    currentIdx === i ? "border-primary bg-primary/20 text-primary" :
                                        answers[q.id] ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400" :
                                            flags[q.id] ? "bg-amber-500/10 border-amber-500/50 text-amber-400" :
                                                "glass border-white/5 text-text-dim hover:border-white/20"
                                )}
                            >
                                {i + 1}
                            </button>
                        ))}
                    </div>

                    <div className="mt-6 space-y-3">
                        {/* Legend */}
                        <div className="flex flex-wrap gap-3 text-[10px] text-text-dim mb-2">
                            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-primary"></span>Current</span>
                            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500"></span>Answered</span>
                            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-500"></span>Flagged</span>
                        </div>
                        <button onClick={toggleFlag} className="btn-secondary w-full justify-center text-sm">
                            <Flag size={16} className={flags[currentQ.id] ? "fill-amber-500 text-amber-500" : ""} />
                            {flags[currentQ.id] ? "Unflag" : "Flag for Review"}
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

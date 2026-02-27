import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Timer, ChevronLeft, ChevronRight, Flag, HelpCircle, CheckCircle2, XCircle } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const DUMMY_QUESTIONS = [
    {
        id: 1,
        text: "According to the passage, why did the author consider the industrial revolution a 'double-edged sword'?",
        choices: [
            { id: 'a', text: "It brought both wealth and widespread poverty." },
            { id: 'b', text: "It increased production but destroyed the environment." },
            { id: 'c', text: "It improved education while limiting personal freedom." },
            { id: 'd', text: "It accelerated technology but slowed down population growth." }
        ],
        correct: 'b'
    },
    {
        id: 2,
        text: "Which of the following best describes the tone of the second paragraph?",
        choices: [
            { id: 'a', text: "Optimistic" },
            { id: 'b', text: "Cynical" },
            { id: 'c', text: "Objective" },
            { id: 'd', text: "Melancholic" }
        ],
        correct: 'c'
    },
    {
        id: 3,
        text: "The word 'ephemeral' as used in line 45 most nearly means:",
        choices: [
            { id: 'a', text: "Eternal" },
            { id: 'b', text: "Fleeting" },
            { id: 'c', text: "Beautiful" },
            { id: 'd', text: "Mysterious" }
        ],
        correct: 'b'
    }
];

export default function CBTProcessor({ onExit }) {
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState({});
    const [flags, setFlags] = useState({});
    const [timeLeft, setTimeLeft] = useState(3600); // 1 hour
    const [isSubmitted, setIsSubmitted] = useState(false);

    useEffect(() => {
        if (timeLeft <= 0 || isSubmitted) return;
        const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
        return () => clearInterval(timer);
    }, [timeLeft, isSubmitted]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const handleSelect = (choiceId) => {
        setAnswers(prev => ({ ...prev, [DUMMY_QUESTIONS[currentIdx].id]: choiceId }));
    };

    const toggleFlag = () => {
        setFlags(prev => ({ ...prev, [DUMMY_QUESTIONS[currentIdx].id]: !prev[DUMMY_QUESTIONS[currentIdx].id] }));
    };

    const calculateScore = () => {
        let score = 0;
        DUMMY_QUESTIONS.forEach(q => {
            if (answers[q.id] === q.correct) score++;
        });
        return score;
    };

    if (isSubmitted) {
        const score = calculateScore();
        return (
            <div className="min-h-screen flex items-center justify-center p-6">
                <GlowCard className="max-w-2xl w-full text-center">
                    <CheckCircle2 className="w-20 h-20 text-emerald-500 mx-auto mb-6" />
                    <h1 className="text-4xl font-bold mb-2">Exam Completed!</h1>
                    <p className="text-text-dim mb-10">Your results have been processed by the Antigravity engine.</p>

                    <div className="grid grid-cols-2 gap-6 mb-10">
                        <div className="glass p-6 rounded-2xl">
                            <div className="text-4xl font-bold text-primary">{score}/{DUMMY_QUESTIONS.length}</div>
                            <div className="text-sm text-text-dim mt-2">Score Accuracy</div>
                        </div>
                        <div className="glass p-6 rounded-2xl">
                            <div className="text-4xl font-bold text-accent">{Math.round((score / DUMMY_QUESTIONS.length) * 100)}%</div>
                            <div className="text-sm text-text-dim mt-2">Percentile Rank</div>
                        </div>
                    </div>

                    <button onClick={onExit} className="btn-primary w-full justify-center">
                        Return to Dashboard
                    </button>
                </GlowCard>
            </div>
        );
    }

    return (
        <div className="h-screen flex flex-col overflow-hidden bg-background">
            {/* Header */}
            <header className="glass px-8 py-4 flex justify-between items-center border-b border-white/5">
                <div className="flex items-center gap-4">
                    <button onClick={onExit} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <span className="font-bold text-lg">JAMB 2023 - Use of English</span>
                </div>

                <div className={clsx(
                    "flex items-center gap-3 px-6 py-2 rounded-full glass border",
                    timeLeft < 300 ? "border-red-500/50 text-red-500 animate-pulse" : "border-primary/20 text-primary"
                )}>
                    <Timer size={20} />
                    <span className="font-mono text-xl font-bold">{formatTime(timeLeft)}</span>
                </div>

                <button onClick={() => setIsSubmitted(true)} className="btn-primary py-2 px-6">
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
                            <div className="flex items-center gap-4 mb-8">
                                <span className="text-primary font-bold text-2xl">Question {currentIdx + 1}</span>
                                {flags[DUMMY_QUESTIONS[currentIdx].id] && <Flag className="text-amber-500 fill-amber-500" size={20} />}
                            </div>

                            <h2 className="text-2xl leading-relaxed mb-12">
                                {DUMMY_QUESTIONS[currentIdx].text}
                            </h2>

                            <div className="space-y-4">
                                {DUMMY_QUESTIONS[currentIdx].choices.map((choice) => (
                                    <button
                                        key={choice.id}
                                        onClick={() => handleSelect(choice.id)}
                                        className={clsx(
                                            "w-full p-6 rounded-2xl text-left border transition-all flex items-center gap-4",
                                            answers[DUMMY_QUESTIONS[currentIdx].id] === choice.id
                                                ? "bg-primary/20 border-primary shadow-lg shadow-primary/10"
                                                : "glass border-transparent hover:border-white/20"
                                        )}
                                    >
                                        <div className={clsx(
                                            "w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm",
                                            answers[DUMMY_QUESTIONS[currentIdx].id] === choice.id
                                                ? "bg-primary text-white"
                                                : "bg-white/5 text-text-dim"
                                        )}>
                                            {choice.id.toUpperCase()}
                                        </div>
                                        <span>{choice.text}</span>
                                    </button>
                                ))}
                            </div>
                        </motion.div>
                    </AnimatePresence>
                </div>

                {/* Question Palette Sidebar */}
                <aside className="w-80 glass border-l border-white/5 p-8 flex flex-col">
                    <h3 className="font-bold mb-6 flex items-center gap-2">
                        <LayoutDashboard size={18} className="text-primary" />
                        Navigation Palette
                    </h3>

                    <div className="grid grid-cols-4 gap-3 flex-1 overflow-y-auto content-start">
                        {DUMMY_QUESTIONS.map((q, i) => (
                            <button
                                key={q.id}
                                onClick={() => setCurrentIdx(i)}
                                className={clsx(
                                    "aspect-square rounded-xl flex items-center justify-center font-bold transition-all border",
                                    currentIdx === i ? "border-primary bg-primary/20 text-primary" :
                                        answers[q.id] ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-500" :
                                            "glass border-white/5 text-text-dim hover:border-white/20"
                                )}
                            >
                                {i + 1}
                            </button>
                        ))}
                    </div>

                    <div className="mt-8 space-y-4">
                        <button onClick={toggleFlag} className="btn-secondary w-full justify-center">
                            <Flag size={18} className={flags[DUMMY_QUESTIONS[currentIdx].id] ? "fill-amber-500 text-amber-500" : ""} />
                            {flags[DUMMY_QUESTIONS[currentIdx].id] ? "Unflag Question" : "Flag for Review"}
                        </button>
                        <div className="flex gap-4">
                            <button
                                disabled={currentIdx === 0}
                                onClick={() => setCurrentIdx(i => i - 1)}
                                className="btn-secondary flex-1 justify-center disabled:opacity-30"
                            >
                                <ChevronLeft size={18} />
                                Back
                            </button>
                            <button
                                disabled={currentIdx === DUMMY_QUESTIONS.length - 1}
                                onClick={() => setCurrentIdx(i => i + 1)}
                                className="btn-primary flex-1 justify-center disabled:opacity-30"
                            >
                                Next
                                <ChevronRight size={18} />
                            </button>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
}

// Re-using LayoutDashboard icon locally since I didn't import it in this block
const LayoutDashboard = ({ size, className }) => <HelpCircle size={size} className={className} />;

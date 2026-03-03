import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, Upload, Sparkles, CheckCircle, ChevronLeft, AlertCircle, XCircle, TrendingUp, TrendingDown } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";

const ESSAY_TYPES = [
    { id: "IELTS", label: "IELTS Writing Task 2", color: "border-rose-500/40 bg-rose-500/5", activeColor: "border-rose-500 bg-rose-500/20 text-rose-300" },
    { id: "SOP", label: "Scholarship / SOP", color: "border-amber-500/40 bg-amber-500/5", activeColor: "border-amber-500 bg-amber-500/20 text-amber-300" },
    { id: "WAEC", label: "Academic Essay", color: "border-blue-500/40 bg-blue-500/5", activeColor: "border-blue-500 bg-blue-500/20 text-blue-300" },
];

export default function AIGrading({ onBack }) {
    const [text, setText] = useState('');
    const [criteria, setCriteria] = useState('IELTS');
    const [isGrading, setIsGrading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleGrade = async () => {
        if (!text.trim()) return;
        setIsGrading(true);
        setResult(null);
        setError(null);

        try {
            const res = await fetch(`${API_BASE}/grade-essay`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: text, criteria })
            });
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsGrading(false);
        }
    };

    return (
        <div className="min-h-screen p-10 bg-background text-white">
            <header className="max-w-6xl mx-auto flex items-center gap-6 mb-10">
                <button onClick={onBack} className="p-2 glass rounded-xl hover:bg-white/5 transition-colors border border-white/10">
                    <ChevronLeft />
                </button>
                <div>
                    <h1 className="text-4xl font-bold flex items-center gap-3">
                        <Sparkles className="text-primary animate-glow" />
                        AI Essay Grader
                    </h1>
                    <p className="text-text-dim mt-1">Professional evaluation for IELTS, SOPs, and Academic Writing.</p>
                </div>
            </header>

            <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-5 gap-8">
                {/* Input Panel */}
                <div className="lg:col-span-2 space-y-5">
                    {/* Essay Type Selector */}
                    <GlowCard className="space-y-3">
                        <h3 className="text-sm font-bold uppercase tracking-wider text-text-dim">Essay Type</h3>
                        {ESSAY_TYPES.map(type => (
                            <button
                                key={type.id}
                                onClick={() => setCriteria(type.id)}
                                className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-all ${criteria === type.id ? type.activeColor : type.color + ' text-text-dim hover:bg-white/5'
                                    }`}
                            >
                                {type.label}
                            </button>
                        ))}
                    </GlowCard>

                    {/* Write/Paste Area */}
                    <GlowCard className="flex flex-col gap-4">
                        <h3 className="text-sm font-bold uppercase tracking-wider text-text-dim">Your Submission</h3>
                        <textarea
                            value={text}
                            onChange={e => setText(e.target.value)}
                            placeholder="Paste or type your essay here... Minimum 50 words recommended for accurate grading."
                            className="w-full bg-white/5 rounded-xl p-4 text-sm leading-relaxed outline-none focus:ring-2 ring-primary/50 transition-all resize-none border border-white/10 min-h-[220px]"
                        />
                        <div className="flex items-center justify-between">
                            <span className="text-xs text-text-dim">{text.trim().split(/\s+/).filter(Boolean).length} words</span>
                            <button
                                disabled={!text.trim() || isGrading}
                                onClick={handleGrade}
                                className="btn-primary px-8 py-2.5 disabled:opacity-50"
                            >
                                {isGrading ? (
                                    <><span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> Grading...</>
                                ) : (
                                    <><Sparkles size={16} /> Grade Essay</>
                                )}
                            </button>
                        </div>
                    </GlowCard>

                    <GlowCard className="bg-amber-500/5 border-amber-500/10">
                        <div className="flex gap-3">
                            <AlertCircle className="text-amber-500 shrink-0 mt-0.5" size={18} />
                            <p className="text-xs text-amber-500/80 leading-relaxed">
                                AI grading is based on examiner rubrics. Use this as a study guide and improvement tool, not as an official score.
                            </p>
                        </div>
                    </GlowCard>
                </div>

                {/* Results Panel */}
                <div className="lg:col-span-3">
                    <AnimatePresence mode="wait">
                        {isGrading && (
                            <motion.div
                                key="loading"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="h-full flex flex-col items-center justify-center glass rounded-3xl p-16 text-center border border-white/5"
                            >
                                <div className="w-20 h-20 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6" />
                                <h2 className="text-2xl font-bold mb-3">Analyzing Your Writing...</h2>
                                <p className="text-text-dim text-sm max-w-xs">Gemini AI is checking for coherence, lexical range, task achievement, and grammatical accuracy.</p>
                            </motion.div>
                        )}

                        {error && !isGrading && (
                            <motion.div
                                key="error"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="glass rounded-3xl p-10 text-center border border-rose-500/20"
                            >
                                <XCircle className="text-rose-500 w-12 h-12 mx-auto mb-4" />
                                <h3 className="text-xl font-bold mb-2">Grading Failed</h3>
                                <p className="text-text-dim text-sm">{error}</p>
                                <button onClick={() => setError(null)} className="mt-6 btn-secondary">Try Again</button>
                            </motion.div>
                        )}

                        {result && !isGrading && (
                            <motion.div
                                key="result"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="space-y-5"
                            >
                                {/* Score Header */}
                                <GlowCard>
                                    <div className="flex justify-between items-start mb-8">
                                        <div>
                                            <div className="text-xs text-primary font-bold uppercase tracking-widest mb-1">Overall Score</div>
                                            <div className="text-7xl font-black">{result.overall_score ?? result.score ?? '—'}</div>
                                            <div className="text-text-dim mt-2 text-sm">{criteria} Evaluation</div>
                                        </div>
                                        <CheckCircle className="text-emerald-400 w-14 h-14 mt-1" />
                                    </div>

                                    {/* Breakdown */}
                                    {result.breakdown && (
                                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
                                            {Object.entries(result.breakdown).map(([name, score]) => (
                                                <div key={name} className="glass p-4 rounded-2xl text-center border border-white/5">
                                                    <div className="text-2xl font-bold text-primary">{score}</div>
                                                    <div className="text-[10px] uppercase text-text-dim mt-1 leading-tight">{name}</div>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    {/* Improvement Plan */}
                                    {result.improvement_plan && (
                                        <div className="border-t border-white/5 pt-6">
                                            <h4 className="font-bold mb-3 flex items-center gap-2 text-sm">
                                                <Sparkles size={14} className="text-primary" /> AI Improvement Plan
                                            </h4>
                                            <p className="text-text-dim text-sm leading-relaxed">{result.improvement_plan}</p>
                                        </div>
                                    )}
                                </GlowCard>

                                {/* Strengths & Weaknesses */}
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    {result.strengths?.length > 0 && (
                                        <GlowCard className="bg-emerald-500/5 border-emerald-500/10">
                                            <h4 className="font-bold mb-3 flex items-center gap-2 text-emerald-400 text-sm">
                                                <TrendingUp size={16} /> Strengths
                                            </h4>
                                            <ul className="space-y-2">
                                                {result.strengths.map((s, i) => (
                                                    <li key={i} className="text-xs text-text-dim flex gap-2">
                                                        <span className="text-emerald-400 shrink-0">✓</span>{s}
                                                    </li>
                                                ))}
                                            </ul>
                                        </GlowCard>
                                    )}
                                    {result.weaknesses?.length > 0 && (
                                        <GlowCard className="bg-rose-500/5 border-rose-500/10">
                                            <h4 className="font-bold mb-3 flex items-center gap-2 text-rose-400 text-sm">
                                                <TrendingDown size={16} /> Areas to Improve
                                            </h4>
                                            <ul className="space-y-2">
                                                {result.weaknesses.map((w, i) => (
                                                    <li key={i} className="text-xs text-text-dim flex gap-2">
                                                        <span className="text-rose-400 shrink-0">✗</span>{w}
                                                    </li>
                                                ))}
                                            </ul>
                                        </GlowCard>
                                    )}
                                </div>

                                {/* Corrections */}
                                {result.corrections?.length > 0 && (
                                    <GlowCard>
                                        <h4 className="font-bold mb-4 text-sm flex items-center gap-2">
                                            <FileText size={14} className="text-primary" /> Suggested Corrections
                                        </h4>
                                        <div className="space-y-4 max-h-60 overflow-y-auto pr-2">
                                            {result.corrections.map((c, i) => (
                                                <div key={i} className="text-xs border border-white/5 rounded-xl p-4 glass">
                                                    <div className="text-rose-400 line-through mb-1">{c.original}</div>
                                                    <div className="text-emerald-400 mb-2">→ {c.suggestion}</div>
                                                    <div className="text-text-dim italic">{c.reason}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </GlowCard>
                                )}
                            </motion.div>
                        )}

                        {!result && !isGrading && !error && (
                            <motion.div
                                key="empty"
                                className="h-full flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-3xl p-16 text-center hover:border-primary/20 transition-colors"
                            >
                                <FileText className="text-white/5 mb-6" size={80} />
                                <h3 className="text-xl font-bold text-text-dim">Your result will appear here.</h3>
                                <p className="text-sm text-text-dim/60 mt-2">Type or paste your essay on the left, then click <strong>Grade Essay</strong>.</p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
}

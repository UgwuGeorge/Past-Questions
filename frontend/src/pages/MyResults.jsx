import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    FileText, TrendingUp, Calendar, ChevronRight, 
    BarChart3, Brain, FileCheck, Search, Clock, Award,
    Sparkles, RefreshCw, ChevronDown, CheckCircle2, XCircle,
    Zap, Target, BookOpen
} from 'lucide-react';
import GlowCard from '../components/GlowCard';
import { clsx } from 'clsx';
import apiClient from '../api/client';
import ScrollToTop from '../components/ScrollToTop';
import { useRef } from 'react';

const ProgressRing = ({ percentage, color = "stroke-primary", size = 80 }) => {
    const radius = size * 0.4;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
        <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
            <svg className="transform -rotate-90 w-full h-full">
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="transparent"
                    className="text-white/5"
                />
                <motion.circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="currentColor"
                    strokeWidth="6"
                    strokeDasharray={circumference}
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    fill="transparent"
                    strokeLinecap="round"
                    className={color}
                />
            </svg>
            <span className="absolute text-[10px] font-black">{Math.round(percentage)}%</span>
        </div>
    );
};

export default function MyResults({ userId, initialSessionId = null }) {
    const [activeTab, setActiveTab] = useState('exams'); // 'exams' | 'ai'
    const [exams, setExams] = useState([]);
    const [aiFeedback, setAiFeedback] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedItem, setSelectedItem] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [aiAnalysisResult, setAiAnalysisResult] = useState(null);
    const scrollRef = useRef(null);

    useEffect(() => {
        if (initialSessionId && exams.length > 0) {
            const found = exams.find(e => e.id === initialSessionId || e.session_id === initialSessionId);
            if (found) {
                setSelectedItem(found);
                setActiveTab('exams');
                // Automatically trigger analysis if it's the selected item? Maybe not, let user click.
            }
        }
    }, [initialSessionId, exams]);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [examsData, aiData] = await Promise.all([
                    apiClient.get(`/simulation/sessions/${userId}`),
                    apiClient.get(`/user/ai-feedback/${userId}`)
                ]);
                
                setExams(examsData);
                setAiFeedback(aiData);
            } catch (err) {
                console.error("Failed to fetch results:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [userId]);

    const handleAnalyze = async (sessionId) => {
        setAnalyzing(true);
        setAiAnalysisResult(null);
        try {
            const data = await apiClient.get(`/simulation/${sessionId}/analyze`);
            setAiAnalysisResult(data);
        } catch (err) {
            console.error("Analysis failed:", err);
        } finally {
            setAnalyzing(false);
        }
    };

    const formatJSON = (json) => {
        if (!json) return null;
        return (
            <div className="space-y-4">
                {Object.entries(json).map(([key, value]) => {
                    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                        return (
                            <div key={key} className="pl-4 border-l border-white/10">
                                <div className="text-[10px] font-black uppercase text-white/30 mb-2">{key.replace(/_/g, ' ')}</div>
                                {formatJSON(value)}
                            </div>
                        );
                    }
                    if (Array.isArray(value)) {
                        return (
                            <div key={key}>
                                <div className="text-[10px] font-black uppercase text-white/30 mb-1">{key.replace(/_/g, ' ')}</div>
                                <div className="flex flex-wrap gap-2">
                                    {value.map((v, i) => (
                                        <span key={i} className="px-2 py-0.5 bg-white/5 border border-white/10 rounded text-[10px] text-text-dim">
                                            {typeof v === 'string' ? v : JSON.stringify(v)}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        );
                    }
                    return (
                        <div key={key}>
                            <span className="text-[10px] font-black uppercase text-white/30 mr-2">{key.replace(/_/g, ' ')}:</span>
                            <span className="text-xs font-medium text-white/70">{value?.toString() || 'N/A'}</span>
                        </div>
                    );
                })}
            </div>
        );
    };

    if (loading) {
        return (
            <div className="h-full flex items-center justify-center">
                <motion.div 
                    animate={{ rotate: 360 }} 
                    transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                    className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full" 
                />
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col p-10 max-w-7xl mx-auto overflow-hidden">
            <header className="mb-10 shrink-0 flex items-end justify-between">
                <div>
                   <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-primary/10 rounded-xl">
                            <TrendingUp size={20} className="text-primary" />
                        </div>
                        <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white/30">Analytics Dashboard</span>
                   </div>
                    <h1 className="text-5xl font-black italic tracking-tighter uppercase leading-none">Intelligence Vault</h1>
                    <p className="text-text-dim text-sm italic mt-2">Personalized performance audit & AI-driven strategic feedback.</p>
                </div>
                
                <div className="flex gap-2 p-1 bg-white/5 rounded-2xl border border-white/10 glass">
                    <button 
                        onClick={() => { setActiveTab('exams'); setSelectedItem(null); setAiAnalysisResult(null); }}
                        className={clsx(
                            "px-6 py-2.5 rounded-xl font-black uppercase tracking-widest text-[10px] transition-all flex items-center gap-2",
                            activeTab === 'exams' ? "bg-primary text-white shadow-lg shadow-primary/20" : "text-white/40 hover:text-white"
                        )}
                    >
                        <BarChart3 size={14} /> Simulations
                    </button>
                    <button 
                        onClick={() => { setActiveTab('ai'); setSelectedItem(null); setAiAnalysisResult(null); }}
                        className={clsx(
                            "px-6 py-2.5 rounded-xl font-black uppercase tracking-widest text-[10px] transition-all flex items-center gap-2",
                            activeTab === 'ai' ? "bg-secondary text-white shadow-lg shadow-secondary/20" : "text-white/40 hover:text-white"
                        )}
                    >
                        <Brain size={14} /> AI Artifacts
                    </button>
                </div>
            </header>

            <div className="flex-1 flex gap-8 overflow-hidden">
                {/* Scrollable list of items */}
                <div className="w-[380px] flex flex-col gap-4 overflow-y-auto custom-scrollbar pr-4 pb-10">
                    <AnimatePresence mode="wait">
                        {activeTab === 'exams' ? (
                            exams.length > 0 ? exams.map((exam, idx) => (
                                <motion.div 
                                    key={exam.id}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    onClick={() => { setSelectedItem(exam); setAiAnalysisResult(null); }}
                                    className={clsx(
                                        "p-6 rounded-[2rem] border transition-all cursor-pointer group relative overflow-hidden",
                                        selectedItem?.id === exam.id ? "bg-white/10 border-primary" : "glass border-white/5 hover:border-white/20"
                                    )}
                                >
                                    {selectedItem?.id === exam.id && (
                                        <motion.div 
                                            layoutId="activeGlow"
                                            className="absolute -right-10 -top-10 w-32 h-32 bg-primary/20 blur-3xl rounded-full"
                                        />
                                    )}
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="px-2.5 py-1 bg-primary/10 rounded-lg text-[9px] font-black text-primary uppercase tracking-widest border border-primary/10">Simulation</div>
                                        <div className="text-[10px] text-text-dim font-bold flex items-center gap-1 opacity-60">
                                            <Calendar size={10} /> {exam.date.split(' ')[0]}
                                        </div>
                                    </div>
                                    <h3 className="font-black text-lg uppercase leading-tight mb-4 group-hover:text-primary transition-colors">{exam.exam_name}</h3>
                                    
                                    <div className="flex items-end justify-between">
                                        <div>
                                            <div className="text-[10px] font-black uppercase text-white/20 mb-1">Score Matrix</div>
                                            <div className={clsx("text-2xl font-black italic tracking-tighter", exam.score >= 50 ? "text-emerald-400" : "text-rose-400")}>
                                                {Math.round(exam.score)}%
                                            </div>
                                        </div>
                                        <div className="h-10 w-10 flex items-center justify-center rounded-xl bg-white/5 border border-white/5 group-hover:border-primary/30 transition-all">
                                            <ChevronRight size={16} className="text-white/20 group-hover:text-primary transition-all" />
                                        </div>
                                    </div>
                                    
                                    <div className="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden">
                                        <motion.div 
                                            initial={{ width: 0 }}
                                            animate={{ width: `${exam.score}%` }}
                                            transition={{ duration: 1, delay: 0.2 }}
                                            className={clsx("h-full", exam.score >= 50 ? "bg-emerald-500" : "bg-rose-500")}
                                        />
                                    </div>
                                </motion.div>
                            )) : (
                                <div className="text-center py-20 bg-white/5 rounded-[40px] border border-dashed border-white/10">
                                    <FileText className="mx-auto mb-4 opacity-10" size={48} />
                                    <p className="text-text-dim text-xs font-bold uppercase tracking-widest">No Records Found</p>
                                </div>
                            )
                        ) : (
                            aiFeedback.length > 0 ? aiFeedback.map((fb, idx) => (
                                <motion.div 
                                    key={fb.id}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    onClick={() => setSelectedItem(fb)}
                                    className={clsx(
                                        "p-6 rounded-[2rem] border transition-all cursor-pointer group relative overflow-hidden",
                                        selectedItem?.id === fb.id ? "bg-white/10 border-secondary" : "glass border-white/5 hover:border-white/20"
                                    )}
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="px-2.5 py-1 bg-secondary/10 rounded-lg text-[9px] font-black text-secondary uppercase tracking-widest border border-secondary/10">
                                            {fb.type.split('_')[0]}
                                        </div>
                                        <div className="text-[10px] text-text-dim font-bold flex items-center gap-1 opacity-60">
                                            <Calendar size={10} /> {fb.date.split(' ')[0]}
                                        </div>
                                    </div>
                                    <h3 className="font-bold text-sm leading-relaxed mb-4 text-white/70 italic group-hover:text-secondary transition-colors truncate">"{fb.input}"</h3>
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-2">
                                            <div className="w-6 h-6 rounded-lg bg-secondary/10 flex items-center justify-center">
                                                <Sparkles size={12} className="text-secondary" />
                                            </div>
                                            <span className="text-[9px] font-black uppercase text-white/40 tracking-widest">AI Synthesis</span>
                                        </div>
                                        <ChevronRight size={14} className="text-white/10" />
                                    </div>
                                </motion.div>
                            )) : (
                                <div className="text-center py-20 bg-white/5 rounded-[40px] border border-dashed border-white/10">
                                    <Brain className="mx-auto mb-4 opacity-10" size={48} />
                                    <p className="text-text-dim text-xs font-bold uppercase tracking-widest">No AI Artifacts</p>
                                </div>
                            )
                        )}
                    </AnimatePresence>
                </div>

                {/* Detail Viewport */}
                <div ref={scrollRef} className="flex-1 glass rounded-[3rem] border border-white/5 p-12 overflow-y-auto custom-scrollbar relative bg-white/[0.01]">
                    <ScrollToTop scrollContainerRef={scrollRef} />
                    <AnimatePresence mode='wait'>
                        {selectedItem ? (
                            <motion.div 
                                key={activeTab + selectedItem.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                className="h-full flex flex-col"
                            >
                                <div className="flex items-start justify-between mb-12">
                                    <div className="flex items-center gap-6">
                                        <div className={clsx(
                                            "w-24 h-24 rounded-[2.5rem] flex items-center justify-center relative group",
                                            activeTab === 'exams' ? "bg-primary/10 border border-primary/20 shadow-2xl shadow-primary/10" : "bg-secondary/10 border border-secondary/20 shadow-2xl shadow-secondary/10"
                                        )}>
                                            {activeTab === 'exams' ? (
                                                <Award className="text-primary group-hover:scale-110 transition-transform" size={48} />
                                            ) : (
                                                <Sparkles className="text-secondary group-hover:scale-110 transition-transform" size={48} />
                                            )}
                                        </div>
                                        <div>
                                            <div className="text-[10px] font-black uppercase tracking-[0.3em] text-white/30 mb-2">Detailed Report</div>
                                            <h2 className="text-4xl font-black italic tracking-tighter uppercase leading-none mb-3">
                                                {activeTab === 'exams' ? selectedItem.exam_name : `AI EVALUATION #${selectedItem.id}`}
                                            </h2>
                                            <div className="flex items-center gap-4 text-[10px] font-bold text-text-dim uppercase tracking-wider">
                                                <span className="flex items-center gap-1.5"><Zap size={10} className="text-primary" /> Session {selectedItem.id}</span>
                                                <span className="w-1 h-1 bg-white/10 rounded-full" />
                                                <span className="flex items-center gap-1.5"><Clock size={10} /> {selectedItem.date}</span>
                                            </div>
                                        </div>
                                    </div>

                                    {activeTab === 'exams' && (
                                        <button 
                                            onClick={() => handleAnalyze(selectedItem.id)}
                                            disabled={analyzing}
                                            className="px-6 py-3 rounded-2xl bg-gradient-to-r from-primary to-accent text-white font-black text-[10px] uppercase tracking-widest shadow-xl shadow-primary/20 flex items-center gap-2 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 transition-all"
                                        >
                                            {analyzing ? <RefreshCw className="animate-spin" size={14} /> : <Sparkles size={14} />}
                                            {analyzing ? "Synthesizing..." : "Request AI Coaching"}
                                        </button>
                                    )}
                                </div>

                                <div className="space-y-12 pb-12">
                                    {activeTab === 'exams' ? (
                                        <>
                                            {/* Top Metrics */}
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                                <GlowCard className="p-8 bg-primary/5">
                                                    <div className="text-[10px] font-black uppercase text-white/30 mb-4 tracking-widest">Aggregate Score</div>
                                                    <div className="flex items-end gap-2">
                                                        <div className="text-5xl font-black text-primary italic leading-none">{Math.round(selectedItem.score)}</div>
                                                        <div className="text-xl font-black text-primary/40 leading-none mb-1">%</div>
                                                    </div>
                                                </GlowCard>
                                                <GlowCard className="p-8">
                                                    <div className="text-[10px] font-black uppercase text-white/30 mb-4 tracking-widest">Accuracy</div>
                                                    <div className="flex items-center gap-4">
                                                        <ProgressRing percentage={selectedItem.data?.total ? (selectedItem.data.correct / selectedItem.data.total) * 100 : 0} size={60} color="stroke-emerald-400" />
                                                        <div>
                                                            <div className="text-xl font-black text-white">{selectedItem.data?.correct || 0}</div>
                                                            <div className="text-[10px] font-bold text-text-dim">CORRECT ANSWERS</div>
                                                        </div>
                                                    </div>
                                                </GlowCard>
                                                <GlowCard className="p-8">
                                                    <div className="text-[10px] font-black uppercase text-white/30 mb-4 tracking-widest">Speed Monitor</div>
                                                    <div className="flex items-center gap-4">
                                                        <div className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10">
                                                            <Clock size={20} className="text-accent" />
                                                        </div>
                                                        <div>
                                                            <div className="text-xl font-black text-white">{Math.round((selectedItem.data?.duration_seconds || 0) / 60)}</div>
                                                            <div className="text-[10px] font-bold text-text-dim">MINUTES SPENT</div>
                                                        </div>
                                                    </div>
                                                </GlowCard>
                                            </div>

                                            {/* AI Analysis Result Section (Animated) */}
                                            <AnimatePresence>
                                                {aiAnalysisResult && (
                                                    <motion.div 
                                                        initial={{ opacity: 0, height: 0 }}
                                                        animate={{ opacity: 1, height: 'auto' }}
                                                        className="space-y-6"
                                                    >
                                                        <h4 className="text-sm font-black uppercase tracking-[0.3em] text-primary flex items-center gap-2">
                                                            <Brain size={16} /> AI Strategic Coaching
                                                        </h4>
                                                        <div className="p-8 rounded-[2.5rem] bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20 shadow-2xl relative overflow-hidden group">
                                                            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                                                                <Brain size={120} />
                                                            </div>
                                                            <div className="relative z-10 space-y-8">
                                                                <div>
                                                                    <div className="text-[10px] font-black uppercase text-primary mb-2 opacity-60">Global Assessment</div>
                                                                    <p className="text-lg font-bold italic text-white/90 leading-relaxed max-w-2xl">
                                                                        "{aiAnalysisResult.overall_assessment}"
                                                                    </p>
                                                                </div>
                                                                
                                                                <div className="grid grid-cols-2 gap-8">
                                                                    <div>
                                                                        <div className="text-[10px] font-black uppercase text-emerald-400 mb-3 flex items-center gap-2">
                                                                            <CheckCircle2 size={12} /> Domain Mastery
                                                                        </div>
                                                                        <div className="space-y-2">
                                                                            {aiAnalysisResult.strong_topics?.map((topic, i) => (
                                                                                <div key={i} className="flex items-center gap-2 text-xs font-bold text-white/70">
                                                                                    <div className="w-1 h-1 rounded-full bg-emerald-500" /> {topic}
                                                                                </div>
                                                                            ))}
                                                                        </div>
                                                                    </div>
                                                                    <div>
                                                                        <div className="text-[10px] font-black uppercase text-rose-400 mb-3 flex items-center gap-2">
                                                                            <XCircle size={12} /> Vulnerable Sectors
                                                                        </div>
                                                                        <div className="space-y-2">
                                                                            {aiAnalysisResult.critical_gaps?.map((topic, i) => (
                                                                                <div key={i} className="flex items-center gap-2 text-xs font-bold text-white/70">
                                                                                    <div className="w-1 h-1 rounded-full bg-rose-500" /> {topic}
                                                                                </div>
                                                                            ))}
                                                                        </div>
                                                                    </div>
                                                                </div>

                                                                <div className="pt-6 border-t border-white/5">
                                                                    <div className="text-[10px] font-black uppercase text-primary mb-4 flex items-center gap-2">
                                                                        <Target size={12} /> Tactical Improvement Plan
                                                                    </div>
                                                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                                                        {aiAnalysisResult.action_plan?.map((step, i) => (
                                                                            <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 text-[11px] font-medium text-white/60 flex items-start gap-3">
                                                                                <div className="w-5 h-5 rounded flex items-center justify-center bg-primary text-white font-black text-[9px] shrink-0">{i+1}</div>
                                                                                {step}
                                                                            </div>
                                                                        ))}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </motion.div>
                                                )}
                                            </AnimatePresence>
                                            
                                            {/* Topic Breakdown */}
                                            <div className="pt-8">
                                                <h4 className="text-sm font-black uppercase tracking-[0.3em] text-white/30 mb-8 flex items-center gap-2">
                                                    <BookOpen size={16} /> Curricular Performance
                                                </h4>
                                                <div className="grid grid-cols-1 gap-6">
                                                    {selectedItem.data?.topics && Object.entries(selectedItem.data.topics).map(([topic, stats]) => {
                                                        const p = (stats.correct / stats.total) * 100;
                                                        return (
                                                            <div key={topic} className="group p-6 rounded-3xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all">
                                                                <div className="flex justify-between items-center mb-4">
                                                                    <div className="flex items-center gap-3">
                                                                        <div className={clsx(
                                                                            "w-10 h-10 rounded-xl flex items-center justify-center font-black text-sm",
                                                                            p >= 60 ? "bg-emerald-500/10 text-emerald-400" : "bg-rose-500/10 text-rose-400"
                                                                        )}>
                                                                            {topic[0]}
                                                                        </div>
                                                                        <div>
                                                                            <div className="text-sm font-black uppercase tracking-tight text-white/80 group-hover:text-white transition-colors">{topic}</div>
                                                                            <div className="text-[10px] font-bold text-text-dim">{stats.correct}/{stats.total} QUESTIONS CORRECT</div>
                                                                        </div>
                                                                    </div>
                                                                    <div className={clsx("text-lg font-black italic tracking-tighter", p >= 60 ? "text-emerald-400" : "text-rose-400")}>
                                                                        {Math.round(p)}%
                                                                    </div>
                                                                </div>
                                                                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                                                                    <motion.div 
                                                                        initial={{ width: 0 }}
                                                                        animate={{ width: `${p}%` }}
                                                                        transition={{ duration: 1, delay: 0.5 }}
                                                                        className={clsx("h-full", p >= 60 ? "bg-emerald-500 shadow-lg shadow-emerald-500/20" : "bg-rose-500 shadow-lg shadow-rose-500/20")}
                                                                    />
                                                                </div>
                                                            </div>
                                                        );
                                                    })}
                                                </div>
                                            </div>
                                        </>
                                    ) : (
                                        <>
                                            <div className="space-y-8">
                                                <div>
                                                    <h4 className="text-[10px] font-black uppercase tracking-widest text-secondary/60 mb-4 flex items-center gap-2">
                                                        <FileText size={12} /> Submission Context
                                                    </h4>
                                                    <div className="p-8 glass rounded-[2rem] border border-white/10 text-lg font-medium italic leading-relaxed text-white/80 bg-secondary/5">
                                                        "{selectedItem.input}"
                                                    </div>
                                                </div>
                                                
                                                <div className="pt-8 border-t border-white/5">
                                                    <h4 className="text-[10px] font-black uppercase tracking-widest text-secondary/60 mb-6 flex items-center gap-2">
                                                        <Brain size={12} /> Expert Feedback Synthesis
                                                    </h4>
                                                    <div className="p-8 glass rounded-[2.5rem] border border-white/5 bg-white/[0.01]">
                                                        {formatJSON(selectedItem.data)}
                                                    </div>
                                                </div>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </motion.div>
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-center">
                                <motion.div 
                                    animate={{ 
                                        y: [0, -10, 0],
                                        opacity: [0.3, 0.6, 0.3]
                                    }}
                                    transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                                    className="mb-8"
                                >
                                    <Search size={120} className="text-white/5" />
                                </motion.div>
                                <h3 className="text-2xl font-black text-white/20 uppercase tracking-[0.4em] italic leading-none">Intelligence Hub</h3>
                                <p className="text-text-dim text-sm max-w-sm mt-6 font-medium leading-relaxed">
                                    Select a simulation record or AI artifact from the sidebar to visualize granular performance metrics and expert coaching.
                                </p>
                                
                                <div className="mt-12 grid grid-cols-2 gap-4 w-full max-w-md">
                                    <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5">
                                        <div className="text-[10px] font-black uppercase text-white/20 mb-1">Total Sims</div>
                                        <div className="text-2xl font-black text-white/40">{exams.length}</div>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5">
                                        <div className="text-[10px] font-black uppercase text-white/20 mb-1">AI Logs</div>
                                        <div className="text-2xl font-black text-white/40">{aiFeedback.length}</div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}


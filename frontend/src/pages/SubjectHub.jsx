import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ChevronLeft, Sparkles, Target, Zap,
    BookOpen, BarChart3, Brain, ArrowRight,
    ShieldAlert, Clock, Play, Layers
} from 'lucide-react';
import GlowCard from '../components/GlowCard';
import { clsx } from 'clsx';

import apiClient from '../api/client';

export default function SubjectHub({ userId, subject, examName, onBack, onStartSimulation }) {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await apiClient.get(`/subjects/${subject.id}/profile?user_id=${userId}`);
                setProfile(data);
                setLoading(false);
            } catch (err) {
                console.error("Failed to load subject profile:", err);
                setLoading(false);
            }
        };
        fetchProfile();
    }, [subject.id]);

    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-background">
                <div className="relative">
                    <div className="w-24 h-24 border-2 border-primary/20 rounded-full animate-ping" />
                    <div className="absolute inset-0 flex items-center justify-center">
                        <Brain size={32} className="text-primary animate-pulse" />
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0b0f1a] text-white p-8 overflow-y-auto custom-scrollbar">
            <header className="max-w-7xl mx-auto flex items-center justify-between mb-12">
                <button
                    onClick={onBack}
                    className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-sm font-bold uppercase tracking-widest"
                >
                    <ChevronLeft size={16} /> Back
                </button>
                <div className="flex items-center gap-3">
                    <div className="px-4 py-1.5 bg-primary/10 border border-primary/20 rounded-full flex items-center gap-2">
                        <Sparkles size={14} className="text-primary animate-pulse" />
                        <span className="text-[10px] font-black uppercase tracking-widest text-primary">Simulator Active</span>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10">
                {/* Left Column: Hero & Performance */}
                <div className="lg:col-span-8 space-y-10">
                    <section>
                        <motion.h1
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="text-7xl font-black tracking-tighter mb-4 italic"
                        >
                            {subject.name}<span className="text-primary">.</span>
                        </motion.h1>
                        <p className="text-xl text-white/50 font-medium max-w-2xl leading-relaxed">
                            {examName} Professional Track. The engine has analyzed {profile?.scheme_of_work?.length || 0} core modules from the latest curriculum.
                        </p>
                    </section>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <GlowCard className="bg-primary/[0.02]">
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-8 flex items-center gap-2">
                                <Target size={14} className="text-primary" /> Topic Mastery Radar
                            </h3>
                            <div className="space-y-6">
                                {Object.entries(profile?.performance || {}).map(([topic, acc], i) => (
                                    <div key={topic}>
                                        <div className="flex justify-between text-[10px] font-black mb-1.5 uppercase tracking-widest">
                                            <span>{topic}</span>
                                            <span className={acc >= 70 ? "text-emerald-400" : "text-rose-400"}>{acc}%</span>
                                        </div>
                                        <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${acc}%` }}
                                                transition={{ delay: i * 0.1, duration: 1 }}
                                                className={clsx("h-full rounded-full bg-gradient-to-r", acc >= 70 ? "from-emerald-500 to-teal-500" : "from-rose-500 to-orange-500")}
                                            />
                                        </div>
                                    </div>
                                ))}
                                {Object.keys(profile?.performance || {}).length === 0 && (
                                    <p className="text-[10px] italic text-white/20">No data available. Start your first session to calibrate.</p>
                                )}
                            </div>
                        </GlowCard>

                        <GlowCard className="bg-secondary/[0.02]">
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-8 flex items-center gap-2">
                                <Brain size={14} className="text-secondary" /> Learning DNA
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {profile?.learning_path?.map((step, i) => (
                                    <div key={i} className="px-3 py-1.5 bg-white/5 border border-white/5 rounded-lg text-[10px] font-bold text-white/60">
                                        {i + 1}. {step}
                                    </div>
                                ))}
                            </div>
                            <div className="mt-8 pt-6 border-t border-white/5">
                                <div className="text-[10px] font-black uppercase text-secondary mb-2 tracking-widest">Mastery Tip</div>
                                <p className="text-xs text-white/40 italic leading-relaxed">
                                    {profile?.mastery_tips?.[0] || "Analyze past patterns to find recurring concepts."}
                                </p>
                            </div>
                        </GlowCard>
                    </div>

                    <section className="glass rounded-[40px] p-10 border border-white/5 relative overflow-hidden bg-white/[0.01]">
                        <div className="absolute top-0 right-0 p-10 opacity-10 pointer-events-none">
                            <BookOpen size={160} className="text-white" />
                        </div>
                        <h2 className="text-2xl font-black uppercase tracking-widest mb-8 flex items-center gap-3">
                            <Layers className="text-primary" /> Scheme of Work Analysis
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {profile?.scheme_of_work?.map((topic, i) => (
                                <div key={i} className="flex items-start gap-4">
                                    <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center shrink-0 text-[10px] font-black text-white/30">
                                        0{i + 1}
                                    </div>
                                    <div>
                                        <div className="font-bold text-sm mb-1">{topic}</div>
                                        <div className="text-[10px] text-white/20 uppercase tracking-widest">Active Module</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="mt-12 pt-10 border-t border-white/5">
                            <div className="text-[10px] font-black uppercase text-primary mb-4 tracking-widest">Structure Insight</div>
                            <p className="text-lg text-white/70 leading-relaxed font-medium">
                                {profile?.structure_analysis || "Standard multi-choice format with weighted topics."}
                            </p>
                        </div>
                    </section>
                </div>

                {/* Right Column: AI Proctor & Simulation Launcher */}
                <div className="lg:col-span-4 space-y-8">
                    <GlowCard className="p-10 bg-gradient-to-br from-primary/5 to-transparent border-primary/20">
                        <div className="w-20 h-20 rounded-3xl bg-primary flex items-center justify-center mb-8 shadow-2xl shadow-primary/40">
                            <Play size={32} fill="white" className="text-white ml-1" />
                        </div>
                        <h2 className="text-3xl font-black italic tracking-tighter mb-4">Start Simulation.</h2>
                        <p className="text-sm text-white/40 mb-10 leading-relaxed">
                            Initialize a proctored environment calibrated specifically for {subject.name} question structures.
                        </p>
                        <div className="space-y-4">
                            <button
                                onClick={() => onStartSimulation('standard')}
                                className="w-full py-5 bg-primary text-white font-black uppercase text-xs tracking-[0.2em] rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all shadow-xl shadow-primary/20"
                            >
                                Proctored Exam (50Q)
                            </button>
                            <button
                                onClick={() => onStartSimulation('practice')}
                                className="w-full py-5 bg-white/5 border border-white/10 text-white font-black uppercase text-xs tracking-[0.2em] rounded-2xl hover:bg-white/10 transition-all"
                            >
                                Adaptive Practice
                            </button>
                        </div>
                    </GlowCard>

                    <GlowCard className="p-8 border-rose-500/20 bg-rose-500/[0.02]">
                        <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-rose-500 mb-6 flex items-center gap-2">
                            <ShieldAlert size={14} /> Proctor Profile
                        </h3>
                        <div className="flex items-center gap-5 mb-6">
                            <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                                <Brain className="text-primary" size={24} />
                            </div>
                            <div>
                                <div className="font-bold text-sm">Professor Reharz</div>
                                <div className="text-[10px] text-white/40 font-bold italic">{profile?.ai_proctor_persona || "Rigorous Academic Mentor"}</div>
                            </div>
                        </div>
                        <p className="text-xs text-white/30 leading-relaxed mb-6">
                            "I have calibrated the simulation complexity based on your {profile?.performance?.length || 'recent'} topic gaps. Integrity filters are active."
                        </p>
                        <div className="flex items-center gap-6 text-[10px] font-black text-rose-500/50 uppercase tracking-widest">
                            <span className="flex items-center gap-1.5"><Clock size={12} /> 60 MIN</span>
                            <span className="flex items-center gap-1.5"><Zap size={12} /> HIGH TIED</span>
                        </div>
                    </GlowCard>
                </div>
            </main>
        </div>
    );
}

function ProgressCircle({ value, color = "primary" }) {
    return (
        <div className="relative w-32 h-32 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90">
                <circle cx="64" cy="64" r="58" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-white/5" />
                <motion.circle
                    cx="64" cy="64" r="58" stroke="currentColor" strokeWidth="8" fill="transparent"
                    strokeDasharray={364}
                    initial={{ strokeDashoffset: 364 }}
                    animate={{ strokeDashoffset: 364 - (value / 100) * 364 }}
                    className={`text-${color}-500`}
                />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-black">{value}%</span>
                <span className="text-[8px] font-black uppercase text-white/30">Mastery</span>
            </div>
        </div>
    );
}

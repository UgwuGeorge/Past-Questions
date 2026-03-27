import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import {
    GraduationCap,
    Briefcase,
    Globe,
    FileText,
    Search,
    ChevronRight,
    Play,
    LayoutDashboard,
    PenTool,
    Mic,
    Settings,
    LogOut,
    Bell,
    BarChart3,
    XCircle,
    ArrowRight,
    Brain,
    Layers,
    Clock,
    Target,
    Crown,
    Lock,
    ChevronUp
} from 'lucide-react';
import apiClient from '../api/client';
import ScrollToTop from '../components/ScrollToTop';
import { useRef } from 'react';

const CATEGORY_MAP = {
    'Academics': ['WAEC', 'NECO', 'JAMB', 'NABTEB', 'NDA', 'POLAC'],
    'Professional': ['ICAN Foundation', 'ICAN Skills', 'ICAN Professional', 'Med/Nursing license', 'The bar exam', 'TRCN', 'CIBN', 'COREN'],
    'Scholarships': ['IELTS Academic', 'IELTS General Training', 'PTDF', 'BEA', 'NNPC/Total energies', 'chevening', 'commonwealth', 'DAAD', 'erasmus mundus']
};

const TIER_PRIORITY = {
    'FREE': 0,
    'PREMIUM': 1,
    'ELITE': 2
};

export default function Dashboard({ userId, onStartPractice, onStartPDFRepo, onStartGrading, onStartInterview, onOpenSubjectHub, onViewResult, onUnlockPro }) {
    const [exams, setExams] = useState([]);
    const [recentSessions, setRecentSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({ exams_completed: 0, avg_score: 0, study_hours: 0, mastery_level: 0 });
    const [subStatus, setSubStatus] = useState(null);
    const [selectedExamForSubjects, setSelectedExamForSubjects] = useState(null); // { id, name, subjects }
    const [searchQuery, setSearchQuery] = useState("");
    const scrollRef = useRef(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const examsData = await apiClient.get('/exams');

                // Fetch subjects for each exam to have them ready
                const fullExams = await Promise.all(examsData.map(async (e) => {
                    const subjects = await apiClient.get(`/exams/${e.id}/subjects`);
                    return { ...e, subjects: Array.isArray(subjects) ? subjects : [] };
                }));

                setExams(fullExams);

                const sessionsData = await apiClient.get(`/simulation/sessions/${userId}`);
                setRecentSessions(sessionsData.slice(0, 3));

                try {
                    const statsData = await apiClient.get(`/user/${userId}/stats`);
                    setStats(statsData);
                    const subData = await apiClient.get('/subscription/status');
                    setSubStatus(subData);
                } catch (e) {
                    console.warn("Stats or Sub fetch failed");
                }

                setLoading(false);
            } catch (err) {
                console.error("Failed to fetch backend data:", err);
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const findExamInDb = (displayName) => {
        return exams.find(e => {
            const name = e.name.toUpperCase();
            const display = displayName.toUpperCase();
            if (name === display) return true;
            if (display.startsWith('ICAN') && name.startsWith(display)) return true;
            if (display === 'JAMB' && (name === 'UTME' || name.includes('JAMB'))) return true;
            if (display === 'THE BAR EXAM' && name.includes('BAR')) return true;
            if (display === 'MED/NURSING LICENSE' && (name.includes('MED') || name.includes('NURSING'))) return true;
            if (display === 'NNPC/TOTAL ENERGIES' && (name.includes('NNPC') || name.includes('TOTAL'))) return true;
            if (name.startsWith(display.split(' ')[0]) && !display.startsWith('ICAN')) return true;
            return false;
        });
    };

    return (
        <div className="flex-1 flex flex-col relative overflow-hidden h-full">
            <div className="flex-1 flex flex-col relative overflow-hidden">
                {/* Background Glows */}
                <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 blur-[120px] rounded-full -z-10" />
                <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full -z-10" />

                {/* Header */}
                <header className="h-20 border-b border-white/5 flex items-center justify-between px-6 lg:px-10 glass shrink-0">
                    <div className="relative w-full max-w-sm hidden md:block group">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 group-focus-within:text-primary transition-colors" size={18} />
                        <input
                            type="text"
                            placeholder="Find track..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 pl-12 pr-4 outline-none focus:border-primary/50 focus:bg-white/10 transition-all text-sm"
                        />
                    </div>

                    <div className="md:hidden flex items-center gap-2">
                         <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
                             <LayoutDashboard size={16} />
                         </div>
                         <span className="text-xs font-black uppercase tracking-widest text-white/60">Overview</span>
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="relative w-10 h-10 flex items-center justify-center text-white/50 hover:text-white transition-colors">
                            <Bell size={20} />
                            <div className="absolute top-2.5 right-2.5 w-2 h-2 bg-secondary rounded-full border-2 border-[#0b0f1a]" />
                        </button>
                        <div className="h-8 w-px bg-white/10" />
                        <div className="flex items-center gap-3 group cursor-pointer">
                            <div className="text-right">
                                <div className="text-sm font-bold opacity-0">User</div> {/* Hidden to keep layout, use actual username if available */}
                                <div className={clsx(
                                    "text-[10px] font-bold uppercase tracking-widest text-right mt-3",
                                    subStatus?.tier === 'ELITE' ? "text-amber-500" : subStatus?.tier === 'PREMIUM' ? "text-emerald-400" : "text-white/40"
                                )}>
                                    {subStatus?.tier || '...'}
                                </div>
                            </div>
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary/40 to-secondary/40 border border-white/10" />
                        </div>
                    </div>
                </header>

                <main ref={scrollRef} className="flex-1 overflow-y-auto p-6 md:p-10 custom-scrollbar">
                    <ScrollToTop scrollContainerRef={scrollRef} />
                    {/* PROMO BANNER */}
                    {subStatus && subStatus.tier !== 'ELITE' && (
                        <div className="mb-10 p-6 rounded-[32px] bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/20 flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-[30%] h-full bg-amber-500/10 blur-[50px] rounded-full" />
                            <div className="flex items-center gap-5 z-10">
                                <div className="w-16 h-16 rounded-2xl bg-amber-500/20 flex items-center justify-center text-amber-500 border border-amber-500/30">
                                    <Crown size={32} />
                                </div>
                                <div>
                                    <h3 className="text-2xl font-black text-amber-500 italic tracking-tighter">REHARZ PRO</h3>
                                    <p className="text-white/60 text-sm font-medium">Unlock ICAN Pathfinders, Theory Grading, and AI Master Models.</p>
                                </div>
                            </div>
                            <button 
                                onClick={onUnlockPro} 
                                className="z-10 w-full md:w-auto px-8 py-4 bg-gradient-to-r from-amber-500 to-orange-500 text-black font-black uppercase tracking-widest text-xs rounded-xl shadow-[0_0_40px_-10px_rgba(245,158,11,0.5)] hover:scale-105 hover:opacity-90 transition-all flex items-center justify-center gap-2"
                            >
                                <Crown size={16} /> Upgrade Now
                            </button>
                        </div>
                    )}

                    {/* Hero */}
                    <div className="flex flex-col md:flex-row gap-10 mb-12 md:mb-20 items-start md:items-end">
                        <div className="flex-1">
                            <motion.h1
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-4xl md:text-6xl font-black mb-4 tracking-tighter"
                            >
                                <span className="text-primary italic">Reharz.</span>
                            </motion.h1>
                            <p className="text-white/50 text-base md:text-xl max-w-2xl font-medium leading-relaxed">
                                Systematic access to the world's most critical examinations. Start a proctored simulation to evaluate your readiness.
                            </p>
                        </div>

                        {/* Recent Results Mini-Feed */}
                        <div className="w-full md:w-96 glass p-8 rounded-[32px] border border-white/10 shrink-0">
                            <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-white/40 mb-6 flex items-center justify-between">
                                <span>Recent Simulations</span>
                                <BarChart3 size={14} className="text-primary" />
                            </h4>
                            <div className="space-y-4">
                                {recentSessions.length > 0 ? recentSessions.map(s => (
                                    <div 
                                        key={s.id} 
                                        onClick={() => onViewResult?.(s.id)}
                                        className="flex items-center justify-between p-3 rounded-2xl bg-white/5 border border-white/5 group hover:border-primary/20 hover:bg-white/10 transition-all cursor-pointer"
                                    >
                                        <div>
                                            <div className="text-xs font-bold group-hover:text-primary transition-colors">{s.exam_name}</div>
                                            <div className="text-[10px] text-text-dim">{s.date}</div>
                                        </div>
                                        <div className={clsx("text-lg font-black", s.score >= 60 ? "text-emerald-400" : "text-rose-400")}>{Math.round(s.score)}%</div>
                                    </div>
                                )) : (
                                    <div className="text-[10px] italic text-text-dim text-center py-4">No simulations recorded yet.</div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
                        {[
                            { label: "Accuracy", value: `${stats.avg_score}%`, sub: "Avg per session", icon: Brain, color: "text-primary" },
                            { label: "Completion", value: stats.exams_completed, sub: "Total simulations", icon: FileText, color: "text-secondary" },
                            { label: "Study Time", value: `${stats.study_hours}h`, sub: "Eval. duration", icon: Clock, color: "text-accent" },
                            { label: "Mastery", value: `${stats.mastery_level}%`, sub: "Curriculum level", icon: Target, color: "text-emerald-400" },
                        ].map((s, i) => (
                            <motion.div
                                key={s.label}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="glass p-6 rounded-3xl border border-white/5 bg-white/[0.01]"
                            >
                                <div className="flex items-center gap-3 mb-4">
                                    <div className={clsx("w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center border border-white/5", s.color)}>
                                        <s.icon size={16} />
                                    </div>
                                    <span className="text-[10px] font-black uppercase tracking-widest text-white/30">{s.label}</span>
                                </div>
                                <div className="text-3xl font-black mb-1">{s.value}</div>
                                <div className="text-[10px] text-white/20 font-bold uppercase">{s.sub}</div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Content */}
                    <div className="space-y-24">
                        {Object.entries(CATEGORY_MAP).map(([catName, list], catIdx) => {
                            const filteredList = list.filter(item => 
                                item.toLowerCase().includes(searchQuery.toLowerCase())
                            );
                            
                            if (searchQuery && filteredList.length === 0) return null;

                            return (
                                <section key={catName}>
                                    <div className="flex items-center gap-4 mb-8">
                                        <div className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10">
                                            {catName === 'Academics' && <Globe size={24} className="text-primary" />}
                                            {catName === 'Professional' && <Briefcase size={24} className="text-secondary" />}
                                            {catName === 'Scholarships' && <GraduationCap size={24} className="text-accent" />}
                                        </div>
                                        <div>
                                            <h2 className="text-3xl font-black tracking-tight uppercase">{catName}</h2>
                                            <p className="text-white/50 text-xs font-bold tracking-widest uppercase">Verified Curriculum Track</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                        {filteredList.map((item, i) => {
                                            const examRecord = findExamInDb(item);
                                            const isAvailable = (item === 'WAEC' || examRecord);
                                            const userTierPower = TIER_PRIORITY[subStatus?.tier] || 0;
                                            const requiredTierPower = TIER_PRIORITY[examRecord?.required_tier] || 0;
                                            const isLocked = isAvailable && examRecord && userTierPower < requiredTierPower;
                                            return (
                                                <motion.div
                                                    key={item}
                                                    initial={{ opacity: 0, y: 10 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ delay: i * 0.05 + catIdx * 0.1 }}
                                                    className="group"
                                                >
                                                    <div
                                                        className={clsx(
                                                            "relative glass border border-white/5 rounded-3xl p-6 hover:border-primary/40 transition-all flex flex-col h-full bg-white/[0.01]",
                                                            isAvailable ? "cursor-pointer" : "opacity-70"
                                                        )}
                                                    >
                                                        <div className="flex items-center justify-between mb-6">
                                                            <div className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center font-black text-xl text-primary border border-white/5 group-hover:bg-primary/10 transition-colors">
                                                                {item[0]}
                                                            </div>
                                                            {isAvailable ? (
                                                                <div className={clsx(
                                                                    "px-3 py-1 border rounded-full flex items-center gap-1.5",
                                                                    isLocked ? "bg-amber-500/10 border-amber-500/20" : "bg-emerald-500/10 border-emerald-500/20"
                                                                )}>
                                                                    {isLocked && <Lock size={10} className="text-amber-500" />}
                                                                    <span className={clsx(
                                                                        "text-[10px] font-black tracking-tighter uppercase",
                                                                        isLocked ? "text-amber-500" : "text-emerald-400"
                                                                    )}>
                                                                        {isLocked ? "Locked" : "Available"}
                                                                    </span>
                                                                </div>
                                                            ) : (
                                                                <div className="px-3 py-1 bg-white/5 border border-white/10 rounded-full">
                                                                    <span className="text-[10px] font-black text-white/30 tracking-tighter uppercase">Syllabus</span>
                                                                </div>
                                                            )}
                                                        </div>

                                                        <h3 className="text-xl font-bold mb-1 tracking-tight group-hover:text-primary transition-colors">{item}</h3>
                                                        <p className="text-[10px] text-white/30 font-black uppercase tracking-[0.2em] mb-4">{catName}</p>

                                                        {isAvailable && examRecord?.subjects?.length > 0 && (
                                                            <div className="mt-4 space-y-1">
                                                                <p className="text-[8px] font-black uppercase text-white/20 mb-2">Popular Subjects</p>
                                                                <div className="flex flex-wrap gap-1">
                                                                    {examRecord.subjects.slice(0, 3).map(s => (
                                                                        <span key={s.id} className="px-2 py-0.5 bg-white/5 rounded text-[8px] font-bold text-white/40">
                                                                            {s.name}
                                                                        </span>
                                                                    ))}
                                                                </div>
                                                            </div>
                                                        )}

                                                        <div className="mt-auto pt-6 border-t border-white/5">
                                                            <button
                                                                disabled={!isAvailable}
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    if (isLocked) {
                                                                        onUnlockPro();
                                                                        return;
                                                                    }
                                                                    if (examRecord) {
                                                                        onStartPractice?.(item, examRecord.id, examRecord.name);
                                                                    }
                                                                }}
                                                                className={clsx(
                                                                    "w-full flex items-center justify-center gap-2 py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all",
                                                                    isAvailable
                                                                        ? isLocked 
                                                                            ? "bg-amber-500/20 text-amber-500 border border-amber-500/40 hover:bg-amber-500/30"
                                                                            : "bg-primary text-white shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98]"
                                                                        : "bg-white/5 text-white/20 cursor-not-allowed"
                                                                )}
                                                            >
                                                                {isAvailable ? (isLocked ? <><Crown size={14} /> Upgrade</> : <><Layers size={14} /> Explorer</>) : "Coming Soon"}
                                                            </button>
                                                        </div>
                                                    </div>
                                                </motion.div>
                                            );
                                        })}
                                    </div>
                                </section>
                            );
                        })}
                    </div>
                </main>
            </div>
        </div>
    );
}

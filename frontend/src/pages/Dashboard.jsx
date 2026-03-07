import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
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
    BarChart3
} from 'lucide-react';

const API_BASE = "http://localhost:8000/api";
const USER_ID = 1;

const CATEGORY_MAP = {
    'Academics': ['WAEC', 'NECO', 'JAMB', 'NABTEB', 'NDA', 'POLAC'],
    'Professional': ['ICAN', 'Med/Nursing license', 'The bar exam', 'TRCN', 'CIBN', 'COREN'],
    'Scholarships': ['IELTS', 'PTDF', 'BEA', 'NNPC/Total energies', 'chevening', 'commonwealth', 'DAAD', 'erasmus mundus']
};

export default function Dashboard({ onStartPractice, onStartPDFRepo, onStartGrading, onStartInterview }) {
    const [exams, setExams] = useState([]);
    const [recentSessions, setRecentSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const examsRes = await fetch(`${API_BASE}/exams`);
                const examsData = await examsRes.json();
                setExams(examsData);

                const sessionsRes = await fetch(`${API_BASE}/simulation/sessions/${USER_ID}`);
                const sessionsData = await sessionsRes.json();
                setRecentSessions(sessionsData.slice(0, 3));

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
            if (display === 'JAMB' && (name === 'UTME' || name.includes('JAMB'))) return true;
            if (display === 'THE BAR EXAM' && name.includes('BAR')) return true;
            if (display === 'MED/NURSING LICENSE' && (name.includes('MED') || name.includes('NURSING'))) return true;
            if (display === 'NNPC/TOTAL ENERGIES' && (name.includes('NNPC') || name.includes('TOTAL'))) return true;
            if (name.startsWith(display.split(' ')[0])) return true;
            return false;
        });
    };

    return (
        <div className="flex h-screen bg-[#0b0f1a] text-white font-sans overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 glass border-r border-white/5 p-6 flex flex-col z-20">
                <div className="flex items-center gap-4 mb-10 px-2 group cursor-pointer" onClick={() => window.location.reload()}>
                    <img src="/assets/reharz_logo.png" alt="Reharz" className="w-10 h-10 rounded-xl object-cover shadow-lg border border-white/10 group-hover:scale-110 transition-all" />
                    <span className="text-2xl font-black tracking-tighter">Reharz</span>
                </div>

                <nav className="flex-1 space-y-2">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">AI Lab</div>
                    <NavItem
                        icon={<PenTool size={20} />}
                        label="AI Grading"
                        onClick={onStartGrading}
                    />
                    <NavItem
                        icon={<Mic size={20} />}
                        label="Interview Prep"
                        onClick={onStartInterview}
                    />

                    <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Practice</div>
                    <NavItem icon={<FileText size={20} />} label="My Results" />

                    <div className="pt-6 pb-2 px-4 text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">User</div>
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <div className="mt-auto pt-6 border-t border-white/5">
                    <button className="flex items-center gap-3 px-4 py-3 w-full text-white/50 hover:text-white hover:bg-white/5 rounded-xl transition-all group">
                        <LogOut size={20} className="group-hover:text-rose-500 transition-colors" />
                        <span className="font-bold text-sm">Sign Out</span>
                    </button>
                </div>
            </aside>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col relative overflow-hidden">
                {/* Background Glows */}
                <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 blur-[120px] rounded-full -z-10" />
                <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full -z-10" />

                {/* Header */}
                <header className="h-20 border-b border-white/5 flex items-center justify-between px-10 glass shrink-0">
                    <div className="relative w-96 group">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 group-focus-within:text-primary transition-colors" size={18} />
                        <input
                            type="text"
                            placeholder="Search examination tracks..."
                            className="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 pl-12 pr-4 outline-none focus:border-primary/50 focus:bg-white/10 transition-all text-sm"
                        />
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="relative w-10 h-10 flex items-center justify-center text-white/50 hover:text-white transition-colors">
                            <Bell size={20} />
                            <div className="absolute top-2.5 right-2.5 w-2 h-2 bg-secondary rounded-full border-2 border-[#0b0f1a]" />
                        </button>
                        <div className="h-8 w-px bg-white/10" />
                        <div className="flex items-center gap-3 group cursor-pointer">
                            <div className="text-right">
                                <div className="text-sm font-bold">Daniel</div>
                                <div className="text-[10px] text-emerald-400 font-bold uppercase tracking-widest">Premium</div>
                            </div>
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary/40 to-secondary/40 border border-white/10" />
                        </div>
                    </div>
                </header>

                <main className="flex-1 overflow-y-auto p-10 custom-scrollbar">
                    {/* Hero */}
                    <div className="flex flex-col md:flex-row gap-10 mb-20 items-end">
                        <div className="flex-1">
                            <motion.h1
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-6xl font-black mb-4 tracking-tighter"
                            >
                                <span className="text-primary italic">Reharz</span> Simulator.
                            </motion.h1>
                            <p className="text-white/50 text-xl max-w-2xl font-medium leading-relaxed">
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
                                    <div key={s.id} className="flex items-center justify-between p-3 rounded-2xl bg-white/5 border border-white/5 group hover:border-primary/20 transition-all">
                                        <div>
                                            <div className="text-xs font-bold">{s.exam_name}</div>
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

                    {/* Content */}
                    <div className="space-y-24">
                        {Object.entries(CATEGORY_MAP).map(([catName, list], catIdx) => (
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
                                    {list.map((item, i) => {
                                        const examRecord = findExamInDb(item);
                                        const isAvailable = (item === 'WAEC' || examRecord);
                                        return (
                                            <motion.div
                                                key={item}
                                                initial={{ opacity: 0, y: 10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: i * 0.05 + catIdx * 0.1 }}
                                                className="group"
                                            >
                                                <div
                                                    onClick={() => isAvailable && onStartPDFRepo?.(item)}
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
                                                            <div className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
                                                                <span className="text-[10px] font-black text-emerald-400 tracking-tighter uppercase">Available</span>
                                                            </div>
                                                        ) : (
                                                            <div className="px-3 py-1 bg-white/5 border border-white/10 rounded-full">
                                                                <span className="text-[10px] font-black text-white/30 tracking-tighter uppercase">Syllabus</span>
                                                            </div>
                                                        )}
                                                    </div>

                                                    <h3 className="text-xl font-bold mb-1 tracking-tight group-hover:text-primary transition-colors">{item}</h3>
                                                    <p className="text-[10px] text-white/30 font-black uppercase tracking-[0.2em] mb-4">{catName}</p>
                                                    <p className="text-[10px] text-text-dim/60 mb-8 italic">Click card to view PDF Repo</p>

                                                    <div className="mt-auto pt-6 border-t border-white/5">
                                                        <button
                                                            disabled={!isAvailable}
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                onStartPractice?.(item, examRecord?.id);
                                                            }}
                                                            className={clsx(
                                                                "w-full flex items-center justify-center gap-2 py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all",
                                                                isAvailable
                                                                    ? "bg-primary text-white shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98]"
                                                                    : "bg-white/5 text-white/20 cursor-not-allowed"
                                                            )}
                                                        >
                                                            {isAvailable ? <><Play size={14} fill="currentColor" /> Practice</> : "Coming Soon"}
                                                        </button>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        );
                                    })}
                                </div>
                            </section>
                        ))}
                    </div>
                </main>
            </div>
        </div>
    );
}

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

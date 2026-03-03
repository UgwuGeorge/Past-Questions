import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import {
    GraduationCap,
    Briefcase,
    Globe,
    Star,
    FileText,
    Mic,
    LayoutDashboard,
    Settings,
    LogOut,
    Search,
    Bell,
    ChevronRight,
    Play,
    MessageSquare
} from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";

export default function Dashboard({ onStartExam, onStartGrading, onStartInterview }) {
    const [exams, setExams] = useState([]);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const examsRes = await fetch(`${API_BASE}/exams`);
                const examsData = await examsRes.json();

                const mappedExams = examsData.map(e => ({
                    id: e.id,
                    name: e.name,
                    category: e.category,
                    logo: getLogoForExam(e.name),
                    color: getColorForExam(e.name)
                }));
                setExams(mappedExams);

                const historyRes = await fetch(`${API_BASE}/history/1`);
                const historyData = await historyRes.json();
                setHistory(historyData);

                setLoading(false);
            } catch (err) {
                console.error("Failed to fetch backend data:", err);
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const getLogoForExam = (name) => {
        if (name.includes("JAMB")) return "/assets/jamb_logo.png";
        if (name.includes("WAEC")) return "/assets/waec_logo.png";
        if (name.includes("IELTS")) return "/assets/ielts_logo.png";
        if (name.includes("Scholarship") || name.includes("PTDF")) return "/assets/cws_logo.png";
        return "/assets/jamb_logo.png";
    };

    const getColorForExam = (name) => {
        if (name.includes("JAMB")) return "from-emerald-500/20";
        if (name.includes("WAEC")) return "from-blue-500/20";
        if (name.includes("IELTS")) return "from-rose-500/20";
        return "from-amber-500/20";
    };
    return (
        <div className="flex h-screen overflow-hidden bg-background text-white font-sans">
            {/* Sidebar */}
            <aside className="w-64 glass border-r border-white/5 p-6 flex flex-col z-20">
                <div className="flex items-center gap-3 mb-10 px-2 group cursor-pointer">
                    <div className="w-10 h-10 bg-primary/20 border border-primary/40 rounded-xl flex items-center justify-center shadow-lg shadow-primary/10 group-hover:shadow-primary/30 transition-all">
                        <Star className="text-primary w-6 h-6 animate-glow" />
                    </div>
                    <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">Antigravity</span>
                </div>

                <nav className="flex-1 space-y-1">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<FileText size={20} />} label="My Practice" />
                    <NavItem icon={<Mic size={20} />} label="AI Interviews" />
                    <NavItem icon={<GraduationCap size={20} />} label="Scholarships" />
                    <div className="pt-6 pb-2 px-4 text-[10px] font-bold text-text-dim uppercase tracking-widest">Preferences</div>
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <div className="mt-auto pt-6 border-t border-white/5">
                    <button className="flex items-center gap-3 px-4 py-3 w-full text-text-dim hover:text-white hover:bg-white/5 rounded-xl transition-all">
                        <LogOut size={20} />
                        <span className="font-medium">Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col h-full bg-[#0b0f1a] relative overflow-hidden">
                {/* Background Glows */}
                <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/20 blur-[120px] rounded-full -z-10" />
                <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/15 blur-[120px] rounded-full -z-10" />

                {/* Header */}
                <header className="h-20 border-b border-white/5 flex items-center justify-between px-10 glass sticky top-0 z-10">
                    <div className="relative w-96 group">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-dim group-focus-within:text-primary transition-colors" size={18} />
                        <input
                            type="text"
                            placeholder="Search exams, subjects, or ai tools..."
                            className="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 pl-12 pr-4 outline-none focus:border-primary/50 focus:bg-white/10 transition-all text-sm"
                        />
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="relative w-10 h-10 flex items-center justify-center text-text-dim hover:text-white transition-colors">
                            <Bell size={20} />
                            <div className="absolute top-2 right-2 w-2 h-2 bg-secondary rounded-full border-2 border-[#0b0f1a]" />
                        </button>
                        <div className="h-8 w-px bg-white/10" />
                        <div className="flex items-center gap-3 pl-2 group cursor-pointer">
                            <div className="text-right">
                                <div className="text-sm font-bold">Daniel Olaitan</div>
                                <div className="text-[10px] text-text-dim font-medium uppercase tracking-wider">Premium Plan</div>
                            </div>
                            <img
                                src="/assets/user_avatar.png"
                                alt="User"
                                className="w-10 h-10 rounded-xl border border-white/10 group-hover:border-primary/50 transition-all object-cover"
                            />
                        </div>
                    </div>
                </header>

                <main className="flex-1 overflow-y-auto p-10 custom-scrollbar">
                    {/* Hero Section */}
                    <div className="mb-12">
                        <motion.h1
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="text-5xl font-extrabold mb-3 tracking-tight"
                        >
                            Hello, <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Daniel</span>.
                        </motion.h1>
                        <p className="text-text-dim text-lg max-w-2xl font-medium leading-relaxed">
                            What challenges will we conquer today? Your AI-powered preparation ecosystem is ready.
                        </p>
                    </div>

                    {/* Quick Features Row */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                        <FeatureCard
                            title="Practice Center"
                            desc="Real-time mock exams & feedback."
                            icon={<FileText className="text-emerald-400" />}
                            color="from-emerald-500"
                            onClick={() => onStartExam?.()}
                        />
                        <FeatureCard
                            title="AI Essay Evaluation"
                            desc="Professional grade & rubrics."
                            icon={<MessageSquare className="text-blue-400" />}
                            color="from-blue-500"
                            onClick={() => onStartGrading?.()}
                        />
                        <FeatureCard
                            title="Mock Interviews"
                            desc="Voice-interactive AI prep."
                            icon={<Mic className="text-rose-400" />}
                            color="from-rose-500"
                            onClick={() => onStartInterview?.()}
                        />
                    </div>

                    <div className="grid grid-cols-1 xl:grid-cols-12 gap-10">
                        {/* Exams Grid (Arranged Grid) */}
                        <div className="xl:col-span-8">
                            <h2 className="text-xl font-bold mb-6 flex items-center justify-between">
                                <span className="flex items-center gap-2">
                                    <Star size={20} className="text-secondary" />
                                    Active Preparation Tracks
                                </span>
                                <button className="text-xs text-primary hover:underline font-bold uppercase tracking-wider">View All</button>
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                {loading ? (
                                    <div className="col-span-2 text-center py-20 text-text-dim font-bold animate-pulse">Syncing with AI Architect...</div>
                                ) : exams.map((exam, i) => (
                                    <GlowCard key={exam.id} delay={i * 0.1} className="py-5 px-6 items-start">
                                        <div className="flex items-center gap-4 mb-5">
                                            <div className="w-14 h-14 bg-white/[0.03] border border-white/5 rounded-2xl flex items-center justify-center">
                                                <img src={exam.logo} alt={exam.name} className="w-10 h-10 object-contain" />
                                            </div>
                                            <div>
                                                <h3 className="text-lg font-bold">{exam.name}</h3>
                                                <p className="text-xs text-text-dim font-medium">{exam.category}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-3">
                                            <button
                                                onClick={() => onStartExam?.(exam.id)}
                                                className="flex-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl py-2.5 text-xs font-bold transition-all flex items-center justify-center gap-2"
                                            >
                                                <Play size={14} /> Practice
                                            </button>
                                            <button className="w-10 h-10 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl flex items-center justify-center transition-all">
                                                <ChevronRight size={18} />
                                            </button>
                                        </div>
                                    </GlowCard>
                                ))}
                            </div>
                        </div>

                        {/* Recent History (The 'Arranged' Data Section) */}
                        <div className="xl:col-span-4">
                            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                                <FileText size={20} className="text-primary" />
                                Recent Activity
                            </h2>
                            <div className="glass rounded-3xl border border-white/5 flex flex-col overflow-hidden">
                                {history.length === 0 ? (
                                    <div className="p-10 text-center text-xs text-text-dim font-medium italic">
                                        No recent practice sessions found. Time to start learning!
                                    </div>
                                ) : history.map((item, i) => (
                                    <div key={item.id} className={clsx(
                                        "p-5 flex items-center gap-4 hover:bg-white/[0.02] transition-colors border-b border-white/5",
                                        i === history.length - 1 && "border-0"
                                    )}>
                                        <div className={clsx(
                                            "w-10 h-10 rounded-xl flex items-center justify-center font-bold text-xs",
                                            item.is_correct ? "bg-emerald-500/10 text-emerald-400" : "bg-rose-500/10 text-rose-400"
                                        )}>
                                            {item.is_correct ? "✓" : "✗"}
                                        </div>
                                        <div className="flex-1">
                                            <div className="text-sm font-bold truncate">{item.topic}</div>
                                            <div className="text-[10px] text-text-dim mt-0.5">{item.date} • {item.difficulty}</div>
                                        </div>
                                    </div>
                                ))}
                                <button className="p-4 text-xs font-bold text-center text-text-dim hover:text-white transition-colors">
                                    View Full History
                                </button>
                            </div>

                            {/* "Ask AI" Smart Widget */}
                            <div className="mt-8 relative group">
                                <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-secondary rounded-3xl blur opacity-25 group-hover:opacity-40 transition-opacity" />
                                <div className="relative glass rounded-3xl p-6 border border-white/10">
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className="w-8 h-8 skeleton-glow bg-primary rounded-lg flex items-center justify-center">
                                            <MessageSquare size={16} className="text-white" />
                                        </div>
                                        <span className="font-bold">Ask AI Tutor</span>
                                    </div>
                                    <div className="bg-white/5 rounded-xl p-3 mb-4 text-[11px] text-white/80 leading-relaxed italic border-l-2 border-primary">
                                        "I'm syncing your performance history to suggest your next move."
                                    </div>
                                    <button className="w-full bg-primary py-2.5 rounded-xl text-xs font-bold hover:bg-primary-hover transition-all shadow-lg shadow-primary/20">
                                        Open Chat
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

function NavItem({ icon, label, active = false }) {
    return (
        <button className={clsx(
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all group",
            active ? "bg-primary/10 text-primary border border-primary/20" : "text-text-dim hover:bg-white/5 hover:text-white"
        )}>
            <span className={clsx(active ? "text-primary" : "text-text-dim group-hover:text-white")}>{icon}</span>
            <span className="font-bold text-sm">{label}</span>
            {active && <div className="ml-auto w-1 h-5 bg-primary rounded-full" />}
        </button>
    );
}

function FeatureCard({ title, desc, icon, color, onClick }) {
    return (
        <button
            onClick={onClick}
            className="glass p-6 rounded-3xl border border-white/5 text-left group hover:border-white/20 transition-all hover:bg-white/[0.02]"
        >
            <div className={`w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center mb-6 border border-white/10 group-hover:scale-110 transition-transform`}>
                {icon}
            </div>
            <h3 className="text-xl font-bold mb-2">{title}</h3>
            <p className="text-xs text-text-dim leading-relaxed font-medium">{desc}</p>
        </button>
    );
}


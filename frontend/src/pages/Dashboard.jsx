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
    Play
} from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";

export default function Dashboard({ onStartExam }) {
    const [exams, setExams] = useState([]);
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

    const categories = ['Academics', 'Professional', 'Scholarships'];

    return (
        <div className="flex h-screen overflow-hidden bg-background text-white font-sans">
            {/* Sidebar */}
            <aside className="w-64 glass border-r border-white/5 p-6 flex flex-col z-20">
                <div className="flex items-center gap-4 mb-10 px-2 group cursor-pointer">
                    <img src="/assets/reharz_logo.png" alt="Reharz" className="w-12 h-12 rounded-2xl object-cover shadow-xl shadow-primary/30 group-hover:scale-110 transition-all border border-white/10" />
                    <span className="text-3xl font-black tracking-tighter bg-gradient-to-r from-white via-white to-white/70 bg-clip-text text-transparent">Reharz</span>
                </div>

                <nav className="flex-1 space-y-1">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<FileText size={20} />} label="My Practice" />
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
                            placeholder="Search exams..."
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
                            Organized past questions and preparation resources for your future.
                        </p>
                    </div>

                    {/* Organized sections */}
                    <div className="space-y-16">
                        {loading ? (
                            <div className="text-center py-20 text-text-dim font-bold animate-pulse">Syncing with AI Architect...</div>
                        ) : (
                            categories.map(cat => (
                                <section key={cat} id={cat.toLowerCase()}>
                                    <div className="flex items-center gap-4 mb-8">
                                        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20">
                                            {cat === 'Academics' && <Globe size={20} className="text-primary" />}
                                            {cat === 'Professional' && <Briefcase size={20} className="text-primary" />}
                                            {cat === 'Scholarships' && <GraduationCap size={20} className="text-primary" />}
                                        </div>
                                        <div>
                                            <h2 className="text-3xl font-black tracking-tight">{cat}</h2>
                                            <p className="text-text-dim text-sm font-medium">Preparation tracks for {cat.toLowerCase()} exams.</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                        {exams.filter(e => e.category === cat).map((exam, i) => (
                                            <GlowCard key={exam.id} delay={i * 0.1} className="py-6 px-6 items-start">
                                                <div className="flex flex-col gap-4 w-full">
                                                    <div className="w-14 h-14 bg-white/[0.03] border border-white/5 rounded-2xl flex items-center justify-center">
                                                        <img src={exam.logo} alt={exam.name} className="w-10 h-10 object-contain" />
                                                    </div>
                                                    <div className="flex-1 min-w-0">
                                                        <h3 className="text-lg font-bold truncate">{exam.name}</h3>
                                                        <p className="text-[10px] text-text-dim font-bold uppercase tracking-widest">{exam.category}</p>
                                                    </div>
                                                    <div className="flex items-center gap-3 w-full mt-2">
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
                                                </div>
                                            </GlowCard>
                                        ))}
                                        {exams.filter(e => e.category === cat).length === 0 && (
                                            <div className="col-span-full py-10 glass rounded-3xl border border-white/5 text-center text-text-dim italic font-medium">
                                                No exams currently available in this category.
                                            </div>
                                        )}
                                    </div>
                                </section>
                            ))
                        )}
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

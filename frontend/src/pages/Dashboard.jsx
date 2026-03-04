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
    Play
} from 'lucide-react';

const API_BASE = "http://localhost:8000/api";

const CATEGORY_MAP = {
    'Academics': ['WAEC', 'NECO', 'JAMB', 'NABTEB', 'NDA', 'POLAC'],
    'Professional': ['ICAN', 'Med/Nursing license', 'The bar exam', 'TRCN', 'CIBN', 'COREN'],
    'Scholarships': ['IELTS', 'PTDF', 'BEA', 'NNPC/Total energies', 'chevening', 'commonwealth', 'DAAD', 'erasmus mundus']
};

export default function Dashboard({ onStartExam }) {
    const [exams, setExams] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const examsRes = await fetch(`${API_BASE}/exams`);
                const examsData = await examsRes.json();
                setExams(examsData);
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
            if (display === 'THE BAR EXAM' && name.includes('BAR')) return true;
            if (display === 'MED/NURSING LICENSE' && (name.includes('MED') || name.includes('NURSING'))) return true;
            if (display === 'NNPC/TOTAL ENERGIES' && (name.includes('NNPC') || name.includes('TOTAL'))) return true;
            if (name.startsWith(display.split(' ')[0])) return true;
            return false;
        });
    };

    return (
        <div className="min-h-screen bg-background text-white font-sans selection:bg-primary/30 antialiased">
            {/* Background Glows */}
            <div className="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
                <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 blur-[120px] rounded-full" />
                <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full" />
            </div>

            {/* Header */}
            <header className="h-20 border-b border-white/5 flex items-center justify-between px-10 glass sticky top-0 z-50">
                <div className="flex items-center gap-4 group cursor-pointer">
                    <img src="/assets/reharz_logo.png" alt="Reharz" className="w-10 h-10 rounded-xl object-cover shadow-lg border border-white/10" />
                    <span className="text-2xl font-black tracking-tighter">Reharz</span>
                </div>

                <div className="relative w-96 hidden md:block group">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-dim group-focus-within:text-primary transition-colors" size={18} />
                    <input
                        type="text"
                        placeholder="Search tracks..."
                        className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-12 pr-4 outline-none focus:border-primary/50 focus:bg-white/10 transition-all text-sm"
                    />
                </div>

                <div className="flex items-center gap-4">
                    <div className="text-right hidden sm:block">
                        <div className="text-sm font-bold">Admin Panel</div>
                        <div className="text-[10px] text-text-dim font-medium uppercase tracking-wider italic">Curated View</div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto p-10">
                {/* Hero Section */}
                <div className="mb-16 text-center">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-6xl font-black mb-4 tracking-tighter"
                    >
                        Prepare for <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Greatness</span>.
                    </motion.h1>
                    <p className="text-text-dim text-xl max-w-2xl mx-auto font-medium">
                        Systematic access to the world's most critical examinations and scholarships.
                    </p>
                </div>

                {/* Sections */}
                <div className="space-y-24">
                    {Object.entries(CATEGORY_MAP).map(([catName, list], catIdx) => (
                        <section key={catName} className="relative">
                            <div className="flex items-center gap-4 mb-10">
                                <div className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10">
                                    {catName === 'Academics' && <Globe size={24} className="text-primary" />}
                                    {catName === 'Professional' && <Briefcase size={24} className="text-secondary" />}
                                    {catName === 'Scholarships' && <GraduationCap size={24} className="text-accent" />}
                                </div>
                                <div>
                                    <h2 className="text-4xl font-black tracking-tight uppercase">{catName}</h2>
                                    <p className="text-text-dim font-medium">Official preparation syllabus and past questions.</p>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                {list.map((item, i) => {
                                    const examRecord = findExamInDb(item);
                                    return (
                                        <motion.div
                                            key={item}
                                            initial={{ opacity: 0, scale: 0.95 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            transition={{ delay: i * 0.05 + catIdx * 0.1 }}
                                            className="group relative"
                                        >
                                            <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-3xl blur opacity-0 group-hover:opacity-100 transition duration-500" />
                                            <div className="relative glass rounded-3xl border border-white/5 p-6 hover:border-white/20 transition-all flex flex-col h-full">
                                                <div className="flex items-start justify-between mb-6">
                                                    <div className="w-14 h-14 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center font-black text-xl text-primary">
                                                        {item[0]}
                                                    </div>
                                                    {examRecord ? (
                                                        <span className="text-[10px] bg-emerald-500/10 text-emerald-400 font-bold px-2 py-1 rounded-full border border-emerald-500/20">READY</span>
                                                    ) : (
                                                        <span className="text-[10px] bg-white/5 text-text-dim font-bold px-2 py-1 rounded-full border border-white/10">PENDING</span>
                                                    )}
                                                </div>

                                                <h3 className="text-xl font-bold mb-1 tracking-tight group-hover:text-primary transition-colors">{item}</h3>
                                                <p className="text-xs text-text-dim font-bold uppercase tracking-widest mb-6">{catName}</p>

                                                <div className="mt-auto pt-6 border-t border-white/5 flex items-center justify-between">
                                                    <button
                                                        onClick={() => examRecord && onStartExam?.(examRecord.id)}
                                                        className={clsx(
                                                            "flex items-center gap-2 font-bold text-sm transition-all",
                                                            examRecord ? "text-white hover:text-primary" : "text-text-dim cursor-not-allowed"
                                                        )}
                                                    >
                                                        {examRecord ? <><Play size={16} fill="currentColor" /> Start Practice</> : "Coming Soon"}
                                                    </button>
                                                    <ChevronRight size={18} className="text-text-dim group-hover:translate-x-1 transition-transform" />
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

            <footer className="mt-20 py-10 border-t border-white/5 text-center text-text-dim text-sm font-medium">
                © 2026 Reharz AI Architecture. All repository endpoints pruned to requested categories.
            </footer>
        </div>
    );
}

function NavItem({ icon, label, active = false }) {
    return (
        <button className={clsx(
            "flex items-center gap-3 px-4 py-3 rounded-xl transition-all group",
            active ? "bg-primary/10 text-primary border border-primary/20" : "text-text-dim hover:bg-white/5 hover:text-white"
        )}>
            <span className={clsx(active ? "text-primary" : "text-text-dim group-hover:text-white")}>{icon}</span>
            <span className="font-bold text-sm">{label}</span>
        </button>
    );
}

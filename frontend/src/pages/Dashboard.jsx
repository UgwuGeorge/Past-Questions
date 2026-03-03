import React from 'react';
import { clsx } from 'clsx';
import { GraduationCap, Briefcase, Globe, Star, FileText, Mic, LayoutDashboard, Settings, LogOut } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const EXAMS = [
    { id: 1, name: "JAMB", category: "Admission", icon: <GraduationCap />, color: "from-blue-500" },
    { id: 2, name: "ICAN", category: "Professional", icon: <Briefcase />, color: "from-purple-500" },
    { id: 3, name: "IELTS", category: "Language", icon: <Globe />, color: "from-emerald-500" },
    { id: 4, name: "Scholarships", category: "Global", icon: <Star />, color: "from-amber-500" },
];

export default function Dashboard({ onStartExam, onStartGrading, onStartInterview }) {
    return (
        <div className="flex h-screen overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 glass border-r border-white/5 p-6 flex flex-col">
                <div className="flex items-center gap-3 mb-10 px-2">
                    <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/30">
                        <Star className="text-white w-6 h-6" />
                    </div>
                    <span className="text-xl font-bold tracking-tight">Antigravity</span>
                </div>

                <nav className="flex-1 space-y-2">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<FileText size={20} />} label="Exams" />
                    <NavItem icon={<Mic size={20} />} label="AI Interviews" />
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <button className="flex items-center gap-3 px-4 py-3 text-text-dim hover:text-white transition-colors mt-auto">
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-10">
                <header className="flex justify-between items-center mb-12">
                    <div>
                        <motion.h1
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="text-4xl font-bold mb-2"
                        >
                            Welcome back, Exam Prep!
                        </motion.h1>
                        <p className="text-text-dim">Your AI-powered bridge to success starts here.</p>
                    </div>
                    <div className="w-12 h-12 rounded-full glass flex items-center justify-center border-primary/20">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-secondary animate-pulse" />
                    </div>
                </header>

                {/* Exam Grid */}
                <section className="mb-12">
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                        <LayoutDashboard size={20} className="text-primary" />
                        Active Exam Tracks
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {EXAMS.map((exam, i) => (
                            <GlowCard key={exam.id} delay={i * 0.1}>
                                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${exam.color} to-transparent opacity-20 absolute top-4 right-4`} />
                                <div className="mb-4 text-primary">{exam.icon}</div>
                                <h3 className="text-lg font-bold mb-1">{exam.name}</h3>
                                <p className="text-sm text-text-dim mb-6">{exam.category}</p>
                                <button
                                    onClick={() => onStartExam?.(exam.id)}
                                    className="btn-secondary w-full justify-center text-sm py-2"
                                >
                                    Practice Now
                                </button>
                            </GlowCard>
                        ))}
                    </div>
                </section>

                {/* AI Features */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <GlowCard className="bg-gradient-to-br from-indigo-500/10 to-transparent">
                        <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                            <FileText className="text-primary" />
                            AI Essay Grader
                        </h3>
                        <p className="text-text-dim mb-6">
                            Upload your IELTS essay or Scholarship SOP for a professional AI evaluation based on global standards.
                        </p>
                        <button onClick={onStartGrading} className="btn-primary">
                            Launch Grader
                        </button>
                    </GlowCard>

                    <GlowCard className="bg-gradient-to-br from-purple-500/10 to-transparent">
                        <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                            <Mic className="text-accent" />
                            AI Interview Coach
                        </h3>
                        <p className="text-text-dim mb-6">
                            Practice for your big day with interactive, voice-ready mock interviews tailored to your target exam.
                        </p>
                        <button onClick={onStartInterview} className="btn-primary bg-accent shadow-accent/20 hover:shadow-accent/40">
                            Start Coaching
                        </button>
                    </GlowCard>
                </div>
            </main>
        </div>
    );
}

function NavItem({ icon, label, active = false }) {
    return (
        <button className={clsx(
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all",
            active ? "bg-primary/10 text-primary border border-primary/20" : "text-text-dim hover:bg-white/5 hover:text-white"
        )}>
            {icon}
            <span className="font-medium">{label}</span>
        </button>
    );
}

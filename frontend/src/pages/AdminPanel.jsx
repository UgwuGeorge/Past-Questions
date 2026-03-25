import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    ShieldAlert, Users, Layers, LayoutGrid, CheckCircle2, 
    XCircle, UserPlus, Trash2, Search, ArrowRight, 
    TrendingUp, Database, FileText
} from 'lucide-react';
import { clsx } from "clsx";
import GlowCard from "../components/GlowCard";

const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000/api`;

export default function AdminPanel({ userId }) {
    const [users, setUsers] = useState([]);
    const [stats, setStats] = useState({ users: 0, sessions: 0, exams: 0, subjects: 0, questions: 0 });
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAdminData();
    }, []);

    const fetchAdminData = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const [usersRes, statsRes] = await Promise.all([
                fetch(`${API_BASE}/admin/users`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                }),
                fetch(`${API_BASE}/admin/system_stats`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
            ]);

            if (!usersRes.ok || !statsRes.ok) throw new Error("Failed to fetch admin data (Permissions?)");

            const usersData = await usersRes.json();
            const statsData = await statsRes.json();

            setUsers(usersData);
            setStats(statsData);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const toggleAdmin = async (targetId) => {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API_BASE}/admin/user/${targetId}/toggle_admin`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const updated = await res.json();
                setUsers(prev => prev.map(u => u.id === targetId ? { ...u, is_admin: updated.is_admin } : u));
            }
        } catch (err) {
            console.error("Toggle failed:", err);
        }
    };

    const filteredUsers = users.filter(u => 
        u.username.toLowerCase().includes(searchQuery.toLowerCase()) || 
        u.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return (
            <div className="h-full flex flex-col items-center justify-center p-20">
                <ShieldAlert className="w-12 h-12 text-primary animate-pulse mb-6" />
                <h2 className="text-xl font-black uppercase tracking-widest text-white/40">Securing Admin Channel...</h2>
            </div>
        );
    }

    if (error) {
        return (
            <div className="h-full flex flex-col items-center justify-center p-20 text-center">
                <XCircle className="w-16 h-16 text-rose-500 mb-6" />
                <h2 className="text-2xl font-black text-white mb-2 italic">Access Denied.</h2>
                <p className="text-white/40 max-w-sm mb-8">This portal requires system architecture privileges. Ensure your clearance level is sufficient.</p>
                <button onClick={fetchAdminData} className="btn-primary px-8">Re-authenticate</button>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col overflow-y-auto custom-scrollbar bg-background">
            {/* Header */}
            <header className="p-10 border-b border-white/5 flex items-center justify-between shrink-0">
                <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center shadow-2xl shadow-primary/20">
                        <ShieldAlert size={28} className="text-primary" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-black tracking-tighter uppercase italic">Control Panel.</h1>
                        <p className="text-[10px] text-white/30 font-black uppercase tracking-[0.2em] mt-1 italic">Authorized Personal Only — System Oversight Protocol</p>
                    </div>
                </div>

                <div className="flex items-center gap-6">
                    <div className="text-right">
                        <div className="text-[10px] font-black uppercase text-white/40 tracking-widest">System Health</div>
                        <div className="text-xs font-black text-emerald-400 flex items-center gap-2">
                             <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" /> OPERATIONAL
                        </div>
                    </div>
                </div>
            </header>

            <main className="flex-1 p-10 space-y-12">
                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                    {[
                        { label: "Total Users", val: stats.users, icon: Users, col: "text-primary" },
                        { label: "Simulations", val: stats.sessions, icon: TrendingUp, col: "text-secondary" },
                        { label: "Exams", val: stats.exams, icon: LayoutGrid, col: "text-accent" },
                        { label: "Subjects", val: stats.subjects, icon: Layers, col: "text-emerald-400" },
                        { label: "Questions", val: stats.questions, icon: Database, col: "text-amber-500" },
                    ].map((s, i) => (
                        <GlowCard key={s.label} className="p-6 overflow-hidden group">
                           <div className="flex items-center justify-between mb-4">
                                <div className={clsx("w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:scale-110 transition-transform", s.col)}>
                                    <s.icon size={18} />
                                </div>
                                <ArrowRight size={14} className="text-white/10 group-hover:text-white/40 transition-colors" />
                           </div>
                           <div className="text-3xl font-black tracking-tighter mb-1">{s.val}</div>
                           <div className="text-[10px] font-black uppercase tracking-widest text-white/30">{s.label}</div>
                        </GlowCard>
                    ))}
                </div>

                {/* User Mgmt */}
                <GlowCard className="p-0 border border-white/10">
                    <div className="p-8 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
                        <div className="flex items-center gap-3">
                            <Users size={20} className="text-primary" />
                            <h3 className="text-lg font-black tracking-tight uppercase">User Directory</h3>
                        </div>
                        <div className="relative w-72">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/20" size={16} />
                            <input 
                                type="text"
                                placeholder="Filter users..."
                                value={searchQuery}
                                onChange={e => setSearchQuery(e.target.value)}
                                className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-12 pr-4 text-xs outline-none focus:border-primary/50 transition-all font-medium"
                            />
                        </div>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-white/[0.02] border-b border-white/5">
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-white/30">User Identity</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-white/30">Email Channel</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-white/30">Enlistment Date</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-white/30 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5 font-medium">
                                {filteredUsers.map(u => (
                                    <tr key={u.id} className="hover:bg-white/[0.01] transition-colors group">
                                        <td className="px-8 py-6">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center font-black text-primary border border-white/5 group-hover:scale-105 transition-transform">
                                                    {u.username[0].toUpperCase()}
                                                </div>
                                                <span className="text-sm font-bold tracking-tight">{u.username}</span>
                                            </div>
                                        </td>
                                        <td className="px-8 py-6 text-sm text-white/40">{u.email}</td>
                                        <td className="px-8 py-6 text-[10px] font-black text-white/30 uppercase tracking-widest">{u.created_at}</td>
                                        <td className="px-8 py-6 text-right">
                                            <div className="flex items-center justify-end gap-2 text-right">
                                                {u.is_admin ? (
                                                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-amber-500/10 border border-amber-500/20 rounded-lg">
                                                        <div className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-pulse" />
                                                        <span className="text-[10px] font-black text-amber-500 uppercase tracking-tighter">System Architect</span>
                                                    </div>
                                                ) : (
                                                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-lg text-white/30">
                                                        <span className="text-[10px] font-black uppercase tracking-tighter">Lvl 1 Agent</span>
                                                    </div>
                                                )}
                                                <button 
                                                    onClick={() => toggleAdmin(u.id)}
                                                    className={clsx(
                                                        "p-3 rounded-xl border transition-all hover:scale-105 active:scale-95 ml-4",
                                                        u.is_admin ? "bg-rose-500/10 border-rose-500/20 text-rose-500 hover:bg-rose-500/20" : "bg-emerald-500/10 border-emerald-500/20 text-emerald-500 hover:bg-emerald-500/20"
                                                    )}
                                                    title={u.is_admin ? "Revoke Admin" : "Grant Admin"}
                                                >
                                                    {u.is_admin ? <XCircle size={16} /> : <CheckCircle2 size={16} />}
                                                </button>
                                                <button className="p-3 rounded-xl bg-white/5 border border-white/10 text-white/20 hover:text-rose-500 hover:border-rose-500/20 transition-all">
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </GlowCard>

                {/* DB Mgmt */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                     <GlowCard className="p-10 border border-white/5 flex flex-col items-center text-center">
                        <FileText size={48} className="text-secondary mb-6" />
                        <h4 className="text-2xl font-black tracking-tighter mb-2 italic">PDF Dataset Ingestion.</h4>
                        <p className="text-white/40 text-sm max-w-sm mb-8 leading-relaxed italic">Upload official examination pathfinders to the neural vault for CBT synthesis.</p>
                        <button className="btn-primary w-full py-4 text-[10px] font-black uppercase tracking-widest bg-secondary/80 hover:bg-secondary">Launch Uploader</button>
                     </GlowCard>

                     <GlowCard className="p-10 border border-white/5 flex flex-col items-center text-center">
                        <Database size={48} className="text-accent mb-6" />
                        <h4 className="text-2xl font-black tracking-tighter mb-2 italic">Question Vault Audit.</h4>
                        <p className="text-white/40 text-sm max-w-sm mb-8 leading-relaxed italic">Perform structural integrity checks on {stats.questions} proctored items across 3 layers.</p>
                        <button className="btn-primary w-full py-4 text-[10px] font-black uppercase tracking-widest bg-emerald-500/80 hover:bg-emerald-500">Run Diagnostics</button>
                     </GlowCard>
                </div>
            </main>
        </div>
    );
}

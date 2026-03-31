import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import {
    User, Crown, Shield, Star, Zap, Clock,
    Target, Brain, FileText, TrendingUp,
    Calendar, Award, ChevronRight, Settings,
    LogOut, Edit3, CheckCircle, BarChart3, Layers
} from 'lucide-react';
import apiClient from '../api/client';
import ScrollToTop from '../components/ScrollToTop';

const TIER_CONFIG = {
    FREE: {
        label: 'Free',
        color: 'text-white/50',
        bg: 'bg-white/5',
        border: 'border-white/10',
        icon: Star,
        glow: 'transparent',
    },
    PREMIUM: {
        label: 'Premium',
        color: 'text-emerald-400',
        bg: 'bg-emerald-500/10',
        border: 'border-emerald-500/30',
        icon: Zap,
        glow: 'rgba(52,211,153,0.15)',
    },
    ELITE: {
        label: 'Elite',
        color: 'text-amber-400',
        bg: 'bg-amber-500/10',
        border: 'border-amber-500/30',
        icon: Crown,
        glow: 'rgba(245,158,11,0.15)',
    },
};

function StatCard({ label, value, sub, icon: Icon, color, delay = 0 }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            className="glass p-6 rounded-3xl border border-white/5 bg-white/[0.02] flex flex-col gap-4"
        >
            <div className="flex items-center gap-3">
                <div className={clsx('w-9 h-9 rounded-2xl bg-white/5 border border-white/5 flex items-center justify-center', color)}>
                    <Icon size={18} />
                </div>
                <span className="text-[10px] font-black uppercase tracking-[0.2em] text-white/30">{label}</span>
            </div>
            <div>
                <div className="text-4xl font-black tracking-tighter mb-1">{value}</div>
                <div className="text-[10px] font-bold uppercase text-white/20">{sub}</div>
            </div>
        </motion.div>
    );
}

export default function Profile({ user, onLogout, onUnlockPro }) {
    const [stats, setStats] = useState({ exams_completed: 0, avg_score: 0, study_hours: 0, mastery_level: 0 });
    const [subStatus, setSubStatus] = useState(null);
    const [recentSessions, setRecentSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const scrollRef = useRef(null);

    const initials = user?.username
        ? user.username.split(/[-_ ]/).map(w => w[0]).join('').toUpperCase().slice(0, 2)
        : 'U';

    const memberSince = user?.created_at
        ? new Date(user.created_at).toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
        : 'Reharz Member';

    useEffect(() => {
        const load = async () => {
            try {
                const [statsData, subData, sessionsData] = await Promise.all([
                    apiClient.get(`/user/${user.id}/stats`),
                    apiClient.get('/subscription/status'),
                    apiClient.get(`/simulation/sessions/${user.id}`),
                ]);
                setStats(statsData);
                setSubStatus(subData);
                setRecentSessions(sessionsData.slice(0, 5));
            } catch (e) {
                console.warn('Profile data fetch failed:', e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [user.id]);

    const tier = subStatus?.tier || 'FREE';
    const tierCfg = TIER_CONFIG[tier] || TIER_CONFIG.FREE;
    const TierIcon = tierCfg.icon;

    return (
        <div className="flex-1 flex flex-col relative overflow-hidden h-full">
            {/* Background glows */}
            <div className="absolute top-[-10%] right-[-5%] w-[50%] h-[50%] bg-primary/8 blur-[150px] rounded-full -z-10" />
            <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/8 blur-[150px] rounded-full -z-10" />

            <main ref={scrollRef} className="flex-1 overflow-y-auto p-6 md:p-10 custom-scrollbar">
                <ScrollToTop scrollContainerRef={scrollRef} />

                {/* Hero Card */}
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="relative mb-10 rounded-[32px] overflow-hidden glass border border-white/5"
                >
                    {/* Background gradient band */}
                    <div
                        className="absolute inset-0 opacity-60"
                        style={{
                            background: `radial-gradient(ellipse at 80% 50%, ${tierCfg.glow} 0%, transparent 70%)`
                        }}
                    />
                    <div className="relative p-8 md:p-12 flex flex-col md:flex-row items-start md:items-center gap-8">
                        {/* Avatar */}
                        <div className="relative shrink-0">
                            <div className="w-24 h-24 md:w-32 md:h-32 rounded-3xl bg-gradient-to-br from-primary/60 to-secondary/60 border-2 border-white/10 flex items-center justify-center text-4xl md:text-5xl font-black text-white shadow-2xl">
                                {initials}
                            </div>
                            {/* Online dot */}
                            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-emerald-400 rounded-full border-4 border-[#0b0f1a]" />
                        </div>

                        {/* Info */}
                        <div className="flex-1">
                            <div className="flex flex-wrap items-center gap-3 mb-2">
                                <h1 className="text-3xl md:text-4xl font-black tracking-tight">{user.username}</h1>
                                {user.is_admin && (
                                    <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/30 rounded-full text-amber-400 text-[10px] font-black uppercase tracking-widest">
                                        <Shield size={10} /> System Admin
                                    </span>
                                )}
                            </div>
                            <p className="text-white/40 text-sm font-medium mb-5">{user.email || 'Reharz Scholar'}</p>

                            <div className="flex flex-wrap items-center gap-3">
                                {/* Tier badge */}
                                <div className={clsx(
                                    'inline-flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-black',
                                    tierCfg.bg, tierCfg.border, tierCfg.color
                                )}>
                                    <TierIcon size={14} />
                                    {tierCfg.label} Plan
                                </div>
                                {/* Member since */}
                                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 text-white/40 text-xs font-bold">
                                    <Calendar size={12} />
                                    Member since {memberSince}
                                </div>
                                {/* Days left */}
                                {subStatus?.days_left > 0 && (
                                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 text-white/40 text-xs font-bold">
                                        <Clock size={12} />
                                        {subStatus.days_left} days left
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Upgrade CTA (if not Elite) */}
                        {tier !== 'ELITE' && (
                            <button
                                onClick={onUnlockPro}
                                className="shrink-0 flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-black font-black uppercase tracking-widest text-xs rounded-2xl shadow-[0_0_30px_-5px_rgba(245,158,11,0.5)] hover:scale-105 hover:opacity-90 transition-all"
                            >
                                <Crown size={14} />
                                {tier === 'FREE' ? 'Go Premium' : 'Go Elite'}
                            </button>
                        )}
                    </div>
                </motion.div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
                    <StatCard label="Accuracy" value={`${stats.avg_score}%`} sub="Avg per session" icon={Brain} color="text-primary" delay={0.05} />
                    <StatCard label="Simulations" value={stats.exams_completed} sub="Total completed" icon={FileText} color="text-secondary" delay={0.1} />
                    <StatCard label="Study Time" value={`${stats.study_hours}h`} sub="Total duration" icon={Clock} color="text-accent" delay={0.15} />
                    <StatCard label="Mastery" value={`${stats.mastery_level}%`} sub="Curriculum level" icon={Target} color="text-emerald-400" delay={0.2} />
                </div>

                {/* Two-column layout: Recent Activity + Account Info */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Recent Simulations */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.25 }}
                        className="glass border border-white/5 rounded-[28px] p-8"
                    >
                        <div className="flex items-center justify-between mb-6">
                            <div className="flex items-center gap-3">
                                <div className="w-9 h-9 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                                    <BarChart3 size={16} />
                                </div>
                                <h2 className="text-sm font-black uppercase tracking-widest">Recent Activity</h2>
                            </div>
                            <span className="text-[10px] font-bold uppercase text-white/20 tracking-widest">Last 5</span>
                        </div>
                        <div className="space-y-3">
                            {loading ? (
                                [...Array(3)].map((_, i) => (
                                    <div key={i} className="h-14 rounded-2xl bg-white/5 animate-pulse" />
                                ))
                            ) : recentSessions.length > 0 ? recentSessions.map((s, i) => (
                                <motion.div
                                    key={s.id}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.3 + i * 0.05 }}
                                    className="flex items-center justify-between p-4 bg-white/3 hover:bg-white/[0.05] border border-white/5 hover:border-primary/20 rounded-2xl transition-all cursor-default group"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className={clsx(
                                            'w-8 h-8 rounded-xl flex items-center justify-center text-xs font-black',
                                            s.score >= 70 ? 'bg-emerald-500/10 text-emerald-400' :
                                            s.score >= 50 ? 'bg-amber-500/10 text-amber-400' :
                                            'bg-rose-500/10 text-rose-400'
                                        )}>
                                            {s.score >= 70 ? <CheckCircle size={14} /> : <Target size={14} />}
                                        </div>
                                        <div>
                                            <div className="text-xs font-bold text-white group-hover:text-primary transition-colors">{s.exam_name}</div>
                                            <div className="text-[10px] text-white/30">{s.date}</div>
                                        </div>
                                    </div>
                                    <div className={clsx(
                                        'text-xl font-black',
                                        s.score >= 70 ? 'text-emerald-400' :
                                        s.score >= 50 ? 'text-amber-400' :
                                        'text-rose-400'
                                    )}>
                                        {Math.round(s.score)}%
                                    </div>
                                </motion.div>
                            )) : (
                                <div className="py-12 text-center">
                                    <Layers size={32} className="text-white/10 mx-auto mb-3" />
                                    <p className="text-sm text-white/30 font-medium">No simulations yet.</p>
                                    <p className="text-xs text-white/20 mt-1">Start one from the Dashboard!</p>
                                </div>
                            )}
                        </div>
                    </motion.div>

                    {/* Account Info */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="glass border border-white/5 rounded-[28px] p-8 flex flex-col"
                    >
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-9 h-9 rounded-2xl bg-secondary/10 border border-secondary/20 flex items-center justify-center text-secondary">
                                <User size={16} />
                            </div>
                            <h2 className="text-sm font-black uppercase tracking-widest">Account Details</h2>
                        </div>

                        <div className="space-y-4 flex-1">
                            {[
                                { label: 'Username', value: user.username },
                                { label: 'Email', value: user.email || '—' },
                                { label: 'Role', value: user.is_admin ? 'System Administrator' : 'Scholar' },
                                { label: 'Subscription', value: tierCfg.label + ' Plan' },
                                { label: 'Expiry', value: subStatus?.expiry_date || 'N/A (Free)' },
                            ].map(({ label, value }) => (
                                <div key={label} className="flex items-center justify-between py-3 border-b border-white/5 last:border-0">
                                    <span className="text-xs font-bold uppercase tracking-widest text-white/30">{label}</span>
                                    <span className="text-xs font-bold text-white/80">{value}</span>
                                </div>
                            ))}
                        </div>

                        {/* Danger zone */}
                        <div className="mt-8 pt-6 border-t border-white/5 space-y-3">
                            <button
                                onClick={onLogout}
                                className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-black uppercase tracking-widest hover:bg-rose-500/20 transition-all"
                            >
                                <LogOut size={14} />
                                Sign Out
                            </button>
                        </div>
                    </motion.div>
                </div>

                {/* Performance Trend Banner */}
                {!loading && stats.exams_completed > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                        className="mt-8 p-6 md:p-8 rounded-[28px] glass border border-white/5 bg-gradient-to-r from-primary/5 to-secondary/5 flex flex-col md:flex-row items-center justify-between gap-6"
                    >
                        <div className="flex items-center gap-5">
                            <div className="w-14 h-14 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                                <TrendingUp size={28} />
                            </div>
                            <div>
                                <h3 className="text-lg font-black tracking-tight mb-1">
                                    {stats.avg_score >= 70 ? '🏆 Outstanding Performance' :
                                     stats.avg_score >= 50 ? '📈 On the Right Track' :
                                     '💪 Room to Grow'}
                                </h3>
                                <p className="text-white/50 text-sm">
                                    {stats.avg_score >= 70
                                        ? `You're averaging ${stats.avg_score}% — keep pushing for mastery.`
                                        : stats.avg_score >= 50
                                        ? `Averaging ${stats.avg_score}%. Keep practicing to hit 70%+.`
                                        : `${stats.exams_completed} exam${stats.exams_completed > 1 ? 's' : ''} done. Consistency is key — you'll improve!`}
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3 shrink-0">
                            <Award size={20} className="text-primary" />
                            <span className="text-2xl font-black text-primary">{stats.avg_score}%</span>
                            <span className="text-xs text-white/30 font-bold">AVG SCORE</span>
                        </div>
                    </motion.div>
                )}
            </main>
        </div>
    );
}

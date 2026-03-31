import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Crown, CheckCircle2, Shield, ArrowRight, Clock, Zap } from 'lucide-react';
import GlowCard from '../components/GlowCard';
import apiClient from '../api/client';
import { clsx } from 'clsx';

export default function SubscriptionHub({ user }) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);
    const [successMsg, setSuccessMsg] = useState('');

    useEffect(() => {
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        setLoading(true);
        try {
            const data = await apiClient.get('/subscription/status');
            setStatus(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpgrade = (tierPlan) => {
        if (!window.PaystackPop) {
            alert("Payment service is loading. Please try again in a few seconds.");
            return;
        }

        const handler = window.PaystackPop.setup({
            key: import.meta.env.VITE_PAYSTACK_PUBLIC_KEY || 'pk_test_your_public_key_here',
            email: user?.email || 'customer@reharz.ai',
            amount: tierPlan.name === 'ELITE' ? 1500000 : 500000, // Naira to Kobo
            currency: 'NGN',
            callback: async (response) => {
                setProcessing(true);
                try {
                    const res = await apiClient.post('/subscription/purchase', {
                        tier: tierPlan.name,
                        reference: response.reference,
                        duration: 30
                    });
                    setSuccessMsg(res.message);
                    await fetchStatus();
                } catch (err) {
                    alert(err.message);
                } finally {
                    setProcessing(false);
                }
            },
            onClose: () => {
                console.log('Payment window closed.');
            }
        });
        handler.openIframe();
    };

    const plans = [
        {
            name: "PREMIUM",
            price: "₦5,000",
            period: "/month",
            desc: "For JAMB, WAEC, and Post-UTME Candidates.",
            features: [
                "Full Standardized Past Questions",
                "Advanced Automated Assessment",
                "Performance Analytics",
                "Email Support"
            ],
            color: "emerald-400"
        },
        {
            name: "ELITE",
            price: "₦15,000",
            period: "/month",
            desc: "The ultimate tool for Professional Exams (ICAN).",
            features: [
                "Everything in Premium",
                "ICAN Pathfinders & Theory",
                "Master's Answer Model Grading",
                "Priority Expert Coaching",
                "Simulated Proctored Environment"
            ],
            color: "amber-500",
            popular: true
        }
    ];

    if (loading) return (
        <div className="h-full flex items-center justify-center">
            <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
    );

    return (
        <div className="h-full overflow-y-auto relative p-8">
            <div className="absolute top-0 right-0 w-[50%] h-[30%] bg-amber-500/5 blur-[120px] rounded-full -z-10" />
            
            <div className="max-w-5xl mx-auto">
                <div className="flex items-center justify-between mb-12">
                     <div>
                        <h1 className="text-4xl font-black italic tracking-tighter flex items-center gap-3">
                             <Crown className="text-amber-500" size={36} /> REHARZ PRO
                        </h1>
                        <p className="text-white/40 mt-2 text-sm max-w-xl">
                            Unlock unrestricted access to advanced automated grading and professional-level exam simulations.
                        </p>
                     </div>
                     <div className="bg-white/5 border border-white/10 p-4 rounded-2xl text-right">
                         <div className="text-[10px] uppercase font-black tracking-widest text-white/40 mb-1">Current Tier</div>
                         <div className={clsx(
                             "text-xl font-black italic",
                             status?.tier === 'ELITE' ? "text-amber-500" : status?.tier === 'PREMIUM' ? "text-emerald-400" : "text-white/80"
                         )}>
                             {status?.tier || 'FREE'}
                         </div>
                         {status?.is_premium && (
                             <div className="text-xs text-secondary font-bold mt-1 flex items-center justify-end gap-1">
                                 <Clock size={12} /> {status.days_left} Days Remaining
                             </div>
                         )}
                     </div>
                </div>

                <AnimatePresence>
                    {successMsg && (
                        <motion.div 
                            initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                            className="bg-emerald-500/20 text-emerald-400 p-4 rounded-xl border border-emerald-500/30 font-bold flex items-center justify-center gap-2 mb-8"
                        >
                            <Shield size={20} /> {successMsg}
                        </motion.div>
                    )}
                </AnimatePresence>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {plans.map((plan, idx) => {
                        const isCurrent = status?.tier === plan.name;
                        return (
                        <GlowCard key={idx} className={clsx("p-8 relative", plan.popular && "border-amber-500/30")}>
                            {plan.popular && (
                                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-amber-500 to-orange-500 text-black text-xs font-black px-4 py-1 rounded-full uppercase tracking-widest shadow-lg shadow-amber-500/20">
                                    Professionals Choice
                                </div>
                            )}

                            <div className={clsx("font-black tracking-widest uppercase text-sm mb-2", `text-${plan.color}`)}>
                                {plan.name}
                            </div>
                            <div className="flex items-end gap-1 mb-4">
                                <span className="text-5xl font-black tracking-tighter">{plan.price}</span>
                                <span className="text-white/40 font-bold mb-2">{plan.period}</span>
                            </div>
                            <p className="text-white/60 text-sm mb-8 h-10">{plan.desc}</p>

                            <button
                                disabled={processing || isCurrent}
                                onClick={() => handleUpgrade(plan.name)}
                                className={clsx(
                                    "w-full py-4 rounded-xl font-bold flex w-full items-center justify-center transition-all",
                                    isCurrent 
                                        ? "bg-white/5 text-white/40 cursor-not-allowed border-transparent"
                                        : plan.popular
                                            ? "bg-gradient-to-r from-amber-500 to-orange-500 text-black hover:opacity-90 shadow-lg shadow-amber-500/20"
                                            : "bg-white/10 hover:bg-white/20 text-white"
                                )}
                            >
                                {processing ? <div className="w-5 h-5 border-2 border-black/20 border-t-black rounded-full animate-spin" /> :
                                    isCurrent ? "Active Plan" : "Upgrade Now"}
                            </button>

                            <div className="mt-8 space-y-4">
                                {plan.features.map((feature, i) => (
                                    <div key={i} className="flex items-start gap-3">
                                        <CheckCircle2 size={18} className={clsx("shrink-0 mt-0.5", `text-${plan.color}`)} />
                                        <span className="text-white/80 text-sm font-medium">{feature}</span>
                                    </div>
                                ))}
                            </div>
                        </GlowCard>
                    )})}
                </div>
            </div>
        </div>
    );
}

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LogIn, UserPlus, Mail, Lock, User, ArrowRight, Loader2, Sparkles, Eye, EyeOff } from 'lucide-react';

const API_BASE = '/api';

export default function Auth({ onLoginSuccess }) {
    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const endpoint = isLogin ? `${API_BASE}/auth/login` : `${API_BASE}/auth/register`;
        const payload = isLogin 
            ? { username: formData.username, password: formData.password }
            : { username: formData.username, email: formData.email, password: formData.password };

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Authentication failed');

            // Store user and token
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('token', data.access_token);
            
            onLoginSuccess(data.user);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#0b0f1a] flex items-center justify-center p-6 relative overflow-hidden">
            {/* Background Polish */}
            <div className="absolute top-0 left-0 w-full h-full">
                <div className="absolute top-[-10%] right-[-10%] w-[50%] h-[50%] bg-primary/20 blur-[120px] rounded-full animate-pulse" />
                <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-secondary/10 blur-[120px] rounded-full animate-pulse" style={{ animationDelay: '2s' }} />
            </div>

            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-md z-10"
            >
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-secondary mb-4 shadow-2xl shadow-primary/20">
                        <span className="text-3xl font-black italic text-white italic">R</span>
                    </div>
                    <h1 className="text-3xl font-black tracking-tighter mb-2">Reharz AI</h1>
                    <p className="text-white/50 text-sm font-medium">Your personalized exam success agent</p>
                </div>

                <div className="glass border border-white/10 rounded-[32px] p-8 shadow-2xl backdrop-blur-xl">
                    <div className="flex bg-white/5 p-1 rounded-2xl mb-8">
                        <button 
                            onClick={() => setIsLogin(true)}
                            className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold transition-all ${isLogin ? 'bg-primary text-white shadow-lg' : 'text-white/50 hover:text-white'}`}
                        >
                            <LogIn size={16} /> Login
                        </button>
                        <button 
                            onClick={() => setIsLogin(false)}
                            className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold transition-all ${!isLogin ? 'bg-primary text-white shadow-lg' : 'text-white/50 hover:text-white'}`}
                        >
                            <UserPlus size={16} /> Register
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <AnimatePresence mode='wait'>
                            <motion.div
                                key={isLogin ? 'login' : 'register'}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.2 }}
                                className="space-y-4"
                            >
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-2">Username</label>
                                    <div className="relative group">
                                        <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-white/30 group-focus-within:text-primary transition-colors">
                                            <User size={18} />
                                        </div>
                                        <input 
                                            type="text"
                                            required
                                            value={formData.username}
                                            onChange={(e) => setFormData({...formData, username: e.target.value})}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 transition-all"
                                            placeholder="johndoe"
                                        />
                                    </div>
                                </div>

                                {!isLogin && (
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-2">Email Address</label>
                                        <div className="relative group">
                                            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-white/30 group-focus-within:text-primary transition-colors">
                                                <Mail size={18} />
                                            </div>
                                            <input 
                                                type="email"
                                                required
                                                value={formData.email}
                                                onChange={(e) => setFormData({...formData, email: e.target.value})}
                                                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 transition-all"
                                                placeholder="john@example.com"
                                            />
                                        </div>
                                    </div>
                                )}

                                <div className="space-y-2">
                                     <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-2">Password</label>
                                     <div className="relative group">
                                         <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-white/30 group-focus-within:text-primary transition-colors">
                                             <Lock size={18} />
                                         </div>
                                         <input 
                                             type={showPassword ? 'text' : 'password'}
                                             required
                                             value={formData.password}
                                             onChange={(e) => setFormData({...formData, password: e.target.value})}
                                             className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-12 text-sm focus:outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 transition-all"
                                             placeholder="••••••••"
                                         />
                                         <button
                                             type="button"
                                             onClick={() => setShowPassword(p => !p)}
                                             className="absolute inset-y-0 right-4 flex items-center text-white/30 hover:text-primary transition-colors"
                                             aria-label={showPassword ? 'Hide password' : 'Show password'}
                                         >
                                             {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                         </button>
                                     </div>
                                 </div>

                                 {isLogin && (
                                     <div className="flex items-center justify-between px-2 pt-2">
                                         <label className="flex items-center gap-2 cursor-pointer group">
                                             <div className="w-4 h-4 rounded border border-white/10 bg-white/5 flex items-center justify-center group-hover:border-primary/50 transition-all">
                                                 <input type="checkbox" className="sr-only" />
                                                 <div className="w-2 h-2 rounded-sm bg-primary opacity-0 group-has-[:checked]:opacity-100 transition-opacity" />
                                             </div>
                                             <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest group-hover:text-white/60 transition-colors">Remember me</span>
                                         </label>
                                         <button type="button" className="text-[10px] font-bold text-primary/60 uppercase tracking-widest hover:text-primary transition-colors">Forgot Password?</button>
                                     </div>
                                 )}
                            </motion.div>
                        </AnimatePresence>

                        {error && (
                            <motion.div 
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="bg-rose-500/10 border border-rose-500/20 text-rose-500 px-4 py-3 rounded-2xl text-xs font-bold text-center"
                            >
                                {error}
                            </motion.div>
                        )}

                        <button 
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-primary to-secondary text-white rounded-2xl py-4 font-black flex items-center justify-center gap-2 hover:opacity-90 hover:scale-[0.98] active:scale-[0.95] disabled:opacity-50 disabled:scale-100 transition-all shadow-xl shadow-primary/20 mt-6"
                        >
                            {loading ? (
                                <Loader2 size={20} className="animate-spin" />
                            ) : (
                                <>
                                    {isLogin ? 'Login Now' : 'Create Account'}
                                    <ArrowRight size={20} />
                                </>
                            )}
                        </button>
                    </form>
                </div>

                <p className="mt-8 text-center text-white/30 text-xs font-medium">
                    By continuing, you agree to our <span className="text-white/50 hover:text-primary transition-colors cursor-pointer">Terms of Service</span> and <span className="text-white/50 hover:text-primary transition-colors cursor-pointer">Privacy Policy</span>
                </p>
            </motion.div>
        </div>
    );
}

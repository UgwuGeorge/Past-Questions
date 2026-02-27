import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Sparkles, ChevronLeft, Send, User, Bot, Brain } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const INTERVIEW_SEGMENTS = [
    { id: 1, label: "Introduction", duration: "2 mins" },
    { id: 2, label: "Core Competency", duration: "5 mins" },
    { id: 3, label: "Behavioral", duration: "3 mins" },
    { id: 4, label: "Closing", duration: "2 mins" }
];

export default function AIInterview({ onBack }) {
    const [messages, setMessages] = useState([
        { role: 'bot', text: "Hello! I'm your AI Interview Coach. Today we'll be practicing for your scholarship interview. Are you ready to begin with the introduction?" }
    ]);
    const [input, setInput] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [currentSegment, setCurrentSegment] = useState(1);
    const [showFeedback, setShowFeedback] = useState(false);

    const handleSend = () => {
        if (!input.trim()) return;

        const newMessages = [...messages, { role: 'user', text: input }];
        setMessages(newMessages);
        setInput('');

        // Simulate Bot response
        setTimeout(() => {
            setMessages(prev => [...prev, {
                role: 'bot',
                text: "That's a strong opening. Can you tell me more about your specific contributions to that project?"
            }]);
            if (currentSegment < 4) setCurrentSegment(prev => prev + 1);
            else setShowFeedback(true);
        }, 1000);
    };

    if (showFeedback) {
        return (
            <div className="min-h-screen p-10 flex items-center justify-center">
                <GlowCard className="max-w-3xl w-full">
                    <div className="flex items-center gap-4 mb-8">
                        <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                            <Brain className="text-accent" />
                        </div>
                        <h1 className="text-3xl font-bold">Interview Insight</h1>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                        <div className="glass p-6 rounded-2xl border-primary/20">
                            <div className="text-3xl font-bold text-primary">85%</div>
                            <div className="text-xs text-text-dim uppercase mt-1">Confidence</div>
                        </div>
                        <div className="glass p-6 rounded-2xl border-secondary/20">
                            <div className="text-3xl font-bold text-secondary">A-</div>
                            <div className="text-xs text-text-dim uppercase mt-1">Articulation</div>
                        </div>
                        <div className="glass p-6 rounded-2xl border-accent/20">
                            <div className="text-3xl font-bold text-accent">High</div>
                            <div className="text-xs text-text-dim uppercase mt-1">Relevance</div>
                        </div>
                    </div>

                    <div className="space-y-6 mb-10">
                        <div>
                            <h4 className="font-bold mb-2 flex items-center gap-2">
                                <Sparkles size={16} className="text-primary" />
                                Key Strength
                            </h4>
                            <p className="text-text-dim text-sm italic">"Your answer regarding community impact was exceptionally well-structured and demonstrated leadership."</p>
                        </div>
                        <div>
                            <h4 className="font-bold mb-2 flex items-center gap-2 text-secondary">
                                <Brain size={16} />
                                Area for Improvement
                            </h4>
                            <p className="text-text-dim text-sm italic">"Try to be more concise in the introductory segment. Reducing filler words will improve your overall impact."</p>
                        </div>
                    </div>

                    <button onClick={onBack} className="btn-primary w-full justify-center">
                        Return to Dashboard
                    </button>
                </GlowCard>
            </div>
        );
    }

    return (
        <div className="h-screen flex flex-col bg-background">
            <header className="glass px-10 py-6 flex justify-between items-center border-b border-white/5">
                <div className="flex items-center gap-6">
                    <button onClick={onBack} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h2 className="text-xl font-bold">Interactive Mock Interview</h2>
                        <p className="text-xs text-text-dim">Scholarship Preparation Track</p>
                    </div>
                </div>

                <div className="flex gap-2">
                    {INTERVIEW_SEGMENTS.map(seg => (
                        <div
                            key={seg.id}
                            className={clsx(
                                "px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider transition-all",
                                currentSegment === seg.id ? "bg-primary text-white scale-110 shadow-lg shadow-primary/30" :
                                    currentSegment > seg.id ? "bg-emerald-500/20 text-emerald-500" : "glass text-text-dim opacity-50"
                            )}
                        >
                            {seg.label}
                        </div>
                    ))}
                </div>
            </header>

            <div className="flex-1 overflow-y-auto px-10 py-10 space-y-8 scroll-smooth">
                <AnimatePresence initial={false}>
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            className={clsx(
                                "flex items-start gap-4 max-w-2xl px-2",
                                msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                            )}
                        >
                            <div className={clsx(
                                "w-10 h-10 rounded-xl flex items-center justify-center shrink-0",
                                msg.role === 'bot' ? "bg-primary/20 text-primary" : "bg-accent/20 text-accent"
                            )}>
                                {msg.role === 'bot' ? <Bot size={20} /> : <User size={20} />}
                            </div>
                            <div className={clsx(
                                "p-4 rounded-2xl leading-relaxed text-sm",
                                msg.role === 'bot' ? "glass rounded-tl-none" : "bg-primary/10 border border-primary/20 rounded-tr-none"
                            )}>
                                {msg.text}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            <footer className="p-8 glass-border-t">
                <div className="max-w-4xl mx-auto flex items-center gap-4 bg-white/5 rounded-2xl p-2 pl-6 focus-within:ring-2 ring-primary/50 transition-all">
                    <input
                        type="text"
                        placeholder="Type your response or use voice..."
                        className="flex-1 bg-transparent outline-none py-3"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button
                        onClick={() => setIsRecording(!isRecording)}
                        className={clsx(
                            "w-12 h-12 rounded-xl flex items-center justify-center transition-all",
                            isRecording ? "bg-red-500 text-white animate-pulse" : "glass text-text-dim hover:text-white"
                        )}
                    >
                        {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
                    </button>
                    <button
                        onClick={handleSend}
                        disabled={!input.trim()}
                        className="w-12 h-12 rounded-xl bg-primary text-white flex items-center justify-center shadow-lg shadow-primary/20 hover:shadow-primary/40 disabled:opacity-50 transition-all"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </footer>
        </div>
    );
}

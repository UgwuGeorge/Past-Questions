import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useDragControls } from 'framer-motion';
import {
    MessageSquare,
    Send,
    X,
    Bot,
    User,
    Sparkles,
    Zap,
    ShieldCheck,
    HelpCircle,
    Minimize2,
    Move
} from 'lucide-react';
import { clsx } from 'clsx';

const API_BASE = "http://localhost:8000/api";

export default function AIChat() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { role: 'assistant', text: "Welcome to Reharz I'm your Exam Architect. How can I help you master your curriculum today?" }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const scrollRef = useRef(null);
    const chatRef = useRef(null);
    const dragControls = useDragControls();
    // Holds pending exam request details until difficulty is provided
    const [pendingExam, setPendingExam] = useState(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isTyping]);

    // Click outside to dock
    useEffect(() => {
        function handleClickOutside(event) {
            if (chatRef.current && !chatRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        }
        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isOpen]);

    // Helper to detect exam related requests
    const isExamRequest = (msg) => {
        const lowered = msg.toLowerCase();
        const keywords = ['post utme', 'jamb', 'mock exam', 'mock exams', 'exam', 'take a', 'i want to take'];
        return keywords.some(k => lowered.includes(k));
    };

    const handleSend = async () => {
        if (!input.trim() || isTyping) return;

        const currentInput = input;
        const userMsg = { role: 'user', text: currentInput };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        // If the message is an exam request, short‑circuit the backend and ask for difficulty
        if (isExamRequest(currentInput)) {
            // Store pending exam request (default to WAEC category for now)
            setPendingExam({ category: 'WAEC' });
            setMessages(prev => [...prev, { role: 'assistant', text: 'What difficulty level would you like? (easy, medium, hard)' }]);
            setIsTyping(false);
            return;
        }
        // If we are waiting for difficulty after an exam request
        if (pendingExam && ['easy', 'medium', 'hard'].includes(currentInput.toLowerCase())) {
            // Fetch an exam list for the stored category
            (async () => {
                try {
                    const examRes = await fetch(`${API_BASE}/exams?category=${pendingExam.category}`);
                    const exams = await examRes.json();
                    const examId = exams?.[0]?.id;
                    if (!examId) throw new Error('No exam found');
                    // Get subjects for the exam
                    const subjectsRes = await fetch(`${API_BASE}/exams/${examId}/subjects`);
                    const subjects = await subjectsRes.json();
                    const subjectId = subjects?.[0]?.id;
                    if (!subjectId) throw new Error('No subject found');
                    // Get first few questions for the subject
                    const questionsRes = await fetch(`${API_BASE}/subjects/${subjectId}/questions?limit=1`);
                    const questions = await questionsRes.json();
                    const question = questions?.[0];
                    if (!question) throw new Error('No question found');
                    // Send the question back to the user
                    setMessages(prev => [...prev, { role: 'assistant', text: `Here is a ${pendingExam.category} question (difficulty: ${currentInput}):\n\n${question.text}` }]);
                } catch (e) {
                    console.error(e);
                    setMessages(prev => [...prev, { role: 'assistant', text: 'Sorry, I could not fetch a question right now.' }]);
                } finally {
                    setPendingExam(null);
                    setIsTyping(false);
                }
            })();
            return;
        }
        setIsTyping(true);

        try {
            // Rectified endpoint to match agent_core/main.py
            const res = await fetch(`${API_BASE}/chat/1`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: currentInput,
                    history: messages.map(m => ({
                        role: m.role === 'assistant' ? 'model' : 'user',
                        text: m.text
                    })),
                    subject_context: subject?.name
                }),
            });

            if (!res.ok) throw new Error("Server error");

            const data = await res.json();
            setMessages(prev => [...prev, { role: 'assistant', text: data.response }]);
        } catch (err) {
            console.error("Chat Error:", err);
            setMessages(prev => [...prev, {
                role: 'assistant',
                text: "I encountered a synchronization error with the brain center. Please ensure the backend server is running on port 8000."
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="fixed bottom-8 right-8 z-[100]">
            <AnimatePresence>
                {isOpen ? (
                    <motion.div
                        ref={chatRef}
                        drag
                        dragListener={false}
                        dragControls={dragControls}
                        dragConstraints={{ left: -1000, right: 0, top: -800, bottom: 0 }}
                        dragElastic={0.1}
                        dragMomentum={false}
                        initial={{ opacity: 0, scale: 0.5, x: 0, y: 50, filter: 'blur(10px)' }}
                        animate={{ opacity: 1, scale: 1, x: 0, y: 0, filter: 'blur(0px)' }}
                        exit={{ opacity: 0, scale: 0.5, x: 0, y: 50, filter: 'blur(10px)' }}
                        className="w-[460px] max-h-[90vh] min-h-[500px] h-auto glass rounded-[2.5rem] border border-white/10 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.5)] flex flex-col overflow-hidden mb-6 relative"
                    >
                        {/* Interactive Background Glow */}
                        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-primary/20 to-transparent -z-10" />

                        {/* Header */}
                        <div
                            onPointerDown={(e) => dragControls.start(e)}
                            className="p-6 border-b border-white/5 bg-white/5 backdrop-blur-xl flex items-center justify-between cursor-move touch-none"
                            title="Drag to undock"
                        >
                            <div className="flex items-center gap-4">
                                <div className="relative">
                                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20 pointer-events-none">
                                        <Bot className="text-white" size={24} />
                                    </div>
                                    <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-[#0b0f1a] shadow-sm pointer-events-none" />
                                </div>
                                <div className="pointer-events-none">
                                    <h3 className="font-black text-base tracking-tight text-white flex items-center gap-2">
                                        Exam Architect <Move size={14} className="text-white/30" />
                                    </h3>
                                    <div className="flex items-center gap-1.5">
                                        <Sparkles size={10} className="text-primary animate-pulse" />
                                        <span className="text-[10px] text-primary font-black uppercase tracking-widest">Engine Active</span>
                                    </div>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button onClick={() => setIsOpen(false)} title="Dock Chat" className="w-9 h-9 rounded-xl hover:bg-white/10 flex items-center justify-center transition-all text-white/50 hover:text-white">
                                    <Minimize2 size={18} />
                                </button>
                                <button onClick={() => { setIsOpen(false); setMessages([{ role: 'assistant', text: "Welcome to Reharz! I'm your Exam Architect. How can I help you master your curriculum today?" }]); }} title="Clear & Close" className="w-9 h-9 rounded-xl hover:bg-red-500/20 flex items-center justify-center transition-all text-white/50 hover:text-red-400">
                                    <X size={18} />
                                </button>
                            </div>
                        </div>

                        {/* Message Stream */}
                        <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-black/20">
                            {messages.map((m, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={clsx("flex gap-3", m.role === 'user' ? "flex-row-reverse" : "flex-row")}
                                >
                                    <div className={clsx(
                                        "w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-1",
                                        m.role === 'user' ? "bg-secondary/20 text-secondary" : "bg-primary/20 text-primary"
                                    )}>
                                        {m.role === 'user' ? <User size={14} /> : <Zap size={14} />}
                                    </div>
                                    <div className={clsx(
                                        "max-w-[75%] p-4 rounded-2xl text-sm leading-relaxed shadow-sm",
                                        m.role === 'user'
                                            ? "bg-gradient-to-br from-primary/80 to-primary text-white rounded-tr-none font-medium"
                                            : "glass border border-white/5 text-white/90 rounded-tl-none"
                                    )}>
                                        {m.text}
                                    </div>
                                </motion.div>
                            ))}
                            {isTyping && (
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-primary/20 text-primary flex items-center justify-center shrink-0 mt-1">
                                        <Bot size={14} />
                                    </div>
                                    <div className="glass border border-white/5 p-4 rounded-2xl rounded-tl-none">
                                        <div className="flex gap-1.5">
                                            <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                            <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                            <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Input Deck */}
                        <div className="p-6 bg-[#0b0f1a]/80 backdrop-blur-2xl border-t border-white/5">
                            <div className="relative group">
                                <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-2xl blur opacity-0 group-focus-within:opacity-100 transition duration-500" />
                                <div className="relative flex items-center bg-white/5 border border-white/10 rounded-2xl p-2 pr-3 focus-within:border-primary/50 transition-all">
                                    <input
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                                        placeholder="Ask about JAMB, IELTS, or Career..."
                                        className="flex-1 bg-transparent px-4 py-3 outline-none text-sm placeholder:text-white/20"
                                    />
                                    <button
                                        onClick={handleSend}
                                        disabled={!input.trim() || isTyping}
                                        className="w-10 h-10 bg-primary text-white rounded-xl flex items-center justify-center shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all disabled:opacity-50"
                                    >
                                        <Send size={18} />
                                    </button>
                                </div>
                            </div>
                            <div className="mt-4 flex items-center justify-center gap-6 text-[10px] font-black uppercase tracking-widest text-white/20">
                                <div className="flex items-center gap-1.5"><ShieldCheck size={12} /> Secure</div>
                                <div className="flex items-center gap-1.5"><HelpCircle size={12} /> Adaptive</div>
                            </div>
                        </div>
                    </motion.div>
                ) : null}
            </AnimatePresence>

            {/* Pulsing Toggle Button */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsOpen(true)}
                className={clsx(
                    "w-20 h-20 rounded-[2rem] bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white shadow-[0_20px_50px_rgba(8,_112,_184,_0.7)] relative group overflow-hidden",
                    isOpen && "hidden"
                )}
            >
                <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute inset-0 animate-ping bg-primary/20 rounded-[2rem]" />
                <MessageSquare size={32} className="relative z-10" />

                {/* Floating Notification Badge */}
                <div className="absolute top-4 right-4 w-3 h-3 bg-white rounded-full shadow-lg border-2 border-primary" />
            </motion.button>
        </div>
    );
}

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
    Move,
    Mic
} from 'lucide-react';
import { clsx } from 'clsx';

const API_BASE = "http://localhost:8000/api";

export default function AIChat({ subject, onAction }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { role: 'assistant', text: "Welcome to Reharz! I'm your Exam Architect. How can I help you master your curriculum today?" }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const scrollRef = useRef(null);
    const chatRef = useRef(null);
    const dragControls = useDragControls();

    // Voice Recognition Setup
    const recognitionRef = useRef(null);

    useEffect(() => {
        if (typeof window !== 'undefined' && (window.SpeechRecognition || window.webkitSpeechRecognition)) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = true;
            recognitionRef.current.lang = 'en-US';

            recognitionRef.current.onresult = (event) => {
                let finalTranscript = '';
                let interimTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }

                if (finalTranscript) {
                    setInput(finalTranscript);
                    // auto-send if final transcript is substantial
                    if (finalTranscript.trim().length > 1) {
                        setTimeout(() => handleSend(finalTranscript), 500);
                        setIsListening(false);
                        recognitionRef.current.stop();
                    }
                } else if (interimTranscript) {
                    setInput(interimTranscript);
                }
            };

            recognitionRef.current.onerror = (event) => {
                console.error("Speech Recognition Error:", event.error);
                setIsListening(false);
            };
            recognitionRef.current.onend = () => {
                setIsListening(false);
            };
        }
    }, []);

    const toggleVoice = () => {
        if (isListening) {
            recognitionRef.current?.stop();
            setIsListening(false);
        } else {
            setInput('');
            recognitionRef.current?.start();
            setIsListening(true);
        }
    };

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

    const handleChoiceSelect = (choice, question) => {
        const isCorrect = choice.is_correct;
        const feedback = isCorrect
            ? `Correct! ${choice.label} is the right answer. ${question.explanation || ''}`
            : `That's incorrect. The correct answer was ${question.choices.find(c => c.is_correct)?.label}. ${question.explanation || ''}`;

        setMessages(prev => [...prev,
        { role: 'user', text: `I choose ${choice.label}: ${choice.text}` },
        { role: 'assistant', text: feedback }
        ]);
    };

    const handleSend = async (overrideInput = null) => {
        const textToSend = overrideInput || input;
        if (!textToSend.trim() || isTyping) return;

        const currentInput = textToSend;
        const userMsg = { role: 'user', text: currentInput };
        setMessages(prev => [...prev, userMsg]);
        setInput('');

        // Check if the user is answering a question by typing the label (A, B, C, D)
        const lastMsg = messages[messages.length - 1];
        if (lastMsg?.questionData) {
            const inputLabel = currentInput.toUpperCase().trim();
            const matchingChoice = lastMsg.questionData.choices.find(c => c.label.toUpperCase() === inputLabel);
            if (matchingChoice) {
                handleChoiceSelect(matchingChoice, lastMsg.questionData);
                return;
            }
        }

        setIsTyping(true);

        try {
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
            let responseText = data.response;

            // Parse structured actions if they exist
            const actionMatch = responseText.match(/\[ACTIONS: ([\s\S]*?)\]/);
            if (actionMatch) {
                try {
                    const actions = JSON.parse(actionMatch[1]);
                    actions.forEach(action => {
                        try {
                            if (onAction) onAction(action);
                        } catch (e) {
                            console.error("Action execution failed:", e);
                        }
                    });
                    // Clean text for display
                    responseText = responseText.replace(/\[ACTIONS: .*?\]/, "").trim();
                    responseText = responseText.replace(/\[ACTION_TRIGGERED\]/, "").trim();
                } catch (e) {
                    console.error("Failed to parse actions:", e);
                }
            }

            setMessages(prev => [...prev, { role: 'assistant', text: responseText }]);
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
                                        "max-w-[85%] p-4 rounded-2xl text-sm leading-relaxed shadow-sm flex flex-col gap-3",
                                        m.role === 'user'
                                            ? "bg-gradient-to-br from-primary/80 to-primary text-white rounded-tr-none font-medium"
                                            : "glass border border-white/5 text-white/90 rounded-tl-none"
                                    )}>
                                        <div className="whitespace-pre-wrap font-medium">{m.text}</div>

                                        {m.questionData && (
                                            <div className="mt-4 grid grid-cols-1 gap-2">
                                                {m.questionData.choices.map((choice) => (
                                                    <button
                                                        key={choice.id}
                                                        onClick={() => handleChoiceSelect(choice, m.questionData)}
                                                        className="text-left p-3 rounded-xl bg-white/5 border border-white/10 hover:bg-primary/20 hover:border-primary/50 transition-all text-xs"
                                                    >
                                                        <span className="font-bold mr-2 text-primary">{choice.label}.</span>
                                                        {choice.text}
                                                    </button>
                                                ))}
                                            </div>
                                        )}
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
                                    <button
                                        onClick={toggleVoice}
                                        className={clsx(
                                            "w-10 h-10 rounded-xl flex items-center justify-center transition-all",
                                            isListening ? "bg-red-500 text-white animate-pulse" : "text-white/30 hover:text-white hover:bg-white/5"
                                        )}
                                        title={isListening ? "Stop Listening" : "Voice Input"}
                                    >
                                        <Mic size={18} />
                                    </button>
                                    <input
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                                        placeholder={isListening ? "Listening..." : "Ask about exams or navigate..."}
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
                                <div className="flex items-center gap-1.5"><Zap size={12} /> Real-time</div>
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

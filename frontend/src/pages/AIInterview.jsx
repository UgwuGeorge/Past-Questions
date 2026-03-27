import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { Mic, MicOff, Sparkles, ChevronLeft, Send, User, Bot, Brain, Star, ChevronRight } from 'lucide-react';
import GlowCard from '../components/GlowCard';

import apiClient from '../api/client';

const SEGMENT_QUESTIONS = [
    "Tell me about yourself and why you are applying for this scholarship.",
    "Describe a significant challenge you've overcome and what you learned from it.",
    "Where do you see yourself in 5 years, and how does this opportunity fit into that vision?",
    "What unique contribution will you bring to your field of study?",
];

export default function AIInterview({ userId, onBack, onUnlockPro }) {
    const [messages, setMessages] = useState([
        { role: 'bot', text: "Hello! I'm your Interview Coach. I'll be guiding you through a mock scholarship interview. Ready to begin? I'll start with the first question.", feedback: null, isError: false }
    ]);
    const [input, setInput] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [currentSegment, setCurrentSegment] = useState(0);
    const [isEvaluating, setIsEvaluating] = useState(false);
    const [showFeedback, setShowFeedback] = useState(false);
    const [allFeedback, setAllFeedback] = useState([]);
    const [hasSentFirst, setHasSentFirst] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isEvaluating) return;

        const userText = input;
        setInput('');

        // Add user message
        const currentQuestion = SEGMENT_QUESTIONS[currentSegment];
        const newMessages = [...messages, { role: 'user', text: userText, feedback: null }];

        // If first message, just ask first question
        if (!hasSentFirst) {
            setHasSentFirst(true);
            setMessages([
                ...newMessages,
                { role: 'bot', text: `Great! Let's begin.\n\n**Q${currentSegment + 1}: ${currentQuestion}**`, feedback: null }
            ]);
            return;
        }

        // Evaluate the response against the current question
        setIsEvaluating(true);
        setMessages([...newMessages, { role: 'bot', text: '...', feedback: null, typing: true }]);

        try {
            const evalResult = await apiClient.post('/interview-evaluate', { userId, question: currentQuestion, answer: userText });

            const nextSegment = currentSegment + 1;
            const isLast = nextSegment >= SEGMENT_QUESTIONS.length;

            // Build bot response
            let botText = `**Feedback on your answer:**\n\n`;
            botText += `🎯 Confidence: **${evalResult.confidence_rating}/10** | Relevance: **${evalResult.content_rating}/10**\n\n`;
            botText += evalResult.overall_feedback || '';

            if (!isLast) {
                botText += `\n\n---\n\n**Q${nextSegment + 1}: ${SEGMENT_QUESTIONS[nextSegment]}**`;
            }

            setAllFeedback(prev => [...prev, { question: currentQuestion, answer: userText, eval: evalResult }]);
            setMessages(prev => [
                ...prev.filter(m => !m.typing),
                { role: 'bot', text: botText, feedback: evalResult }
            ]);

            if (isLast) {
                setTimeout(() => setShowFeedback(true), 1200);
            } else {
                setCurrentSegment(nextSegment);
            }
        } catch (e) {
            const errorText = e.message;
            setMessages(prev => [
                ...prev.filter(m => !m.typing),
                { 
                    role: 'bot', 
                    text: errorText, 
                    feedback: null, 
                    isError: true,
                    isSubscriptionError: errorText.includes('Subscription')
                }
            ]);
        } finally {
            setIsEvaluating(false);
        }
    };

    // ─── Final Feedback Summary ──────────────────────────────────────────────
    if (showFeedback) {
        const avgConfidence = Math.round(allFeedback.reduce((s, f) => s + (f.eval?.confidence_rating || 0), 0) / allFeedback.length);
        const avgContent = Math.round(allFeedback.reduce((s, f) => s + (f.eval?.content_rating || 0), 0) / allFeedback.length);

        return (
            <div className="min-h-screen p-10 flex items-center justify-center bg-background">
                <GlowCard className="max-w-3xl w-full">
                    <div className="flex items-center gap-4 mb-8">
                        <div className="w-12 h-12 rounded-2xl bg-primary/20 flex items-center justify-center">
                            <Brain className="text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">Interview Complete!</h1>
                            <p className="text-text-dim text-sm">Here's your performance analysis.</p>
                        </div>
                    </div>

                    {/* Scores */}
                    <div className="grid grid-cols-3 gap-5 mb-10">
                        <div className="glass p-6 rounded-2xl text-center">
                            <div className="text-4xl font-bold text-primary">{avgConfidence}/10</div>
                            <div className="text-xs text-text-dim uppercase mt-2 tracking-wider">Avg Confidence</div>
                        </div>
                        <div className="glass p-6 rounded-2xl text-center">
                            <div className="text-4xl font-bold text-secondary">{avgContent}/10</div>
                            <div className="text-xs text-text-dim uppercase mt-2 tracking-wider">Avg Relevance</div>
                        </div>
                        <div className="glass p-6 rounded-2xl text-center">
                            <div className="text-4xl font-bold text-accent">{allFeedback.length}</div>
                            <div className="text-xs text-text-dim uppercase mt-2 tracking-wider">Questions Done</div>
                        </div>
                    </div>

                    {/* Per-question breakdown */}
                    <div className="space-y-4 mb-10 max-h-72 overflow-y-auto pr-2">
                        {allFeedback.map((item, i) => (
                            <div key={i} className="glass rounded-2xl p-5 border border-white/5">
                                <div className="text-xs text-text-dim font-bold uppercase tracking-wider mb-2">Q{i + 1}</div>
                                <p className="text-sm font-medium mb-3">{item.question}</p>
                                {item.eval?.positive_aspects?.length > 0 && (
                                    <div className="text-xs text-emerald-400 mb-2">
                                        ✓ {item.eval.positive_aspects[0]}
                                    </div>
                                )}
                                {item.eval?.areas_for_improvement?.length > 0 && (
                                    <div className="text-xs text-amber-400">
                                        △ {item.eval.areas_for_improvement[0]}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    <button onClick={onBack} className="btn-primary w-full justify-center">
                        Return to Dashboard
                    </button>
                </GlowCard>
            </div>
        );
    }

    // ─── Chat Interface ──────────────────────────────────────────────────────
    return (
        <div className="h-screen flex flex-col bg-background">
            {/* Header */}
            <header className="glass px-10 py-5 flex justify-between items-center border-b border-white/5 shrink-0">
                <div className="flex items-center gap-5">
                    <button onClick={onBack} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft />
                    </button>
                    <div>
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            <Brain size={20} className="text-primary" /> Mock Interview
                        </h2>
                        <p className="text-xs text-text-dim">Scholarship Preparation Track</p>
                    </div>
                </div>

                {/* Progress segments */}
                <div className="flex gap-2 items-center">
                    {SEGMENT_QUESTIONS.map((_, i) => (
                        <div
                            key={i}
                            className={clsx(
                                "h-2 rounded-full transition-all",
                                i < currentSegment ? "w-8 bg-emerald-500" :
                                    i === currentSegment ? "w-8 bg-primary animate-pulse" :
                                        "w-4 bg-white/10"
                            )}
                        />
                    ))}
                    <span className="text-xs text-text-dim ml-2 font-medium">
                        {Math.min(currentSegment + 1, SEGMENT_QUESTIONS.length)}/{SEGMENT_QUESTIONS.length}
                    </span>
                </div>
            </header>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-10 py-8 space-y-6">
                <AnimatePresence initial={false}>
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 12 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={clsx(
                                "flex items-start gap-4 max-w-3xl",
                                msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                            )}
                        >
                            <div className={clsx(
                                "w-10 h-10 rounded-xl flex items-center justify-center shrink-0",
                                msg.role === 'bot' ? "bg-primary/20 text-primary" : "bg-secondary/20 text-secondary"
                            )}>
                                {msg.role === 'bot' ? <Bot size={20} /> : <User size={20} />}
                            </div>
                            <div className={clsx(
                                "p-5 rounded-2xl leading-relaxed text-sm max-w-lg",
                                msg.isError ? "bg-rose-500/10 border border-rose-500/20" :
                                msg.role === 'bot' ? "glass rounded-tl-none border border-white/5" :
                                    "bg-secondary/10 border border-secondary/20 rounded-tr-none"
                            )}>
                                {msg.typing ? (
                                    <div className="flex gap-1.5 items-center py-1">
                                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                ) : (
                                    <>
                                        <div className="whitespace-pre-line">{msg.text}</div>
                                        {msg.isSubscriptionError && (
                                            <button
                                                onClick={onUnlockPro}
                                                className="mt-4 px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-black rounded-lg font-black uppercase text-[10px] tracking-widest flex items-center gap-2 hover:opacity-90 transition-opacity"
                                            >
                                                <Crown size={12} /> Upgrade to Pro
                                            </button>
                                        )}
                                    </>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <footer className="p-6 border-t border-white/5 glass shrink-0">
                <div className="max-w-4xl mx-auto flex items-end gap-3 bg-white/5 rounded-2xl p-3 pl-5 focus-within:ring-2 ring-primary/40 transition-all">
                    <textarea
                        rows={2}
                        placeholder={hasSentFirst ? "Type your response..." : "Type 'Ready' to begin the interview..."}
                        className="flex-1 bg-transparent outline-none py-2 resize-none text-sm leading-relaxed"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                    />
                    <div className="flex gap-2 shrink-0">
                        <button
                            onClick={() => setIsRecording(!isRecording)}
                            className={clsx(
                                "w-10 h-10 rounded-xl flex items-center justify-center transition-all",
                                isRecording ? "bg-red-500 text-white animate-pulse" : "glass text-text-dim hover:text-white border border-white/10"
                            )}
                        >
                            {isRecording ? <MicOff size={18} /> : <Mic size={18} />}
                        </button>
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isEvaluating}
                            className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center shadow-lg shadow-primary/20 hover:shadow-primary/40 disabled:opacity-40 transition-all"
                        >
                            {isEvaluating ? <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Send size={18} />}
                        </button>
                    </div>
                </div>
                <p className="text-center text-xs text-text-dim mt-3">Press Enter to send • Shift+Enter for new line</p>
            </footer>
        </div>
    );
}

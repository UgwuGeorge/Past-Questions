import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Upload, Sparkles, CheckCircle, ChevronLeft, AlertCircle } from 'lucide-react';
import GlowCard from '../components/GlowCard';

export default function AIGrading({ onBack }) {
    const [file, setFile] = useState(null);
    const [isGrading, setIsGrading] = useState(false);
    const [result, setResult] = useState(null);

    const handleUpload = () => {
        setIsGrading(true);
        // Simulate AI API call
        setTimeout(() => {
            setResult({
                score: "7.5",
                band: "Expert User",
                criteria: {
                    "Task Response": 8,
                    "Coherence": 7,
                    "Lexical Resource": 8,
                    "Grammar": 7
                },
                feedback: "Your essay presents a clear position throughout. To improve further, focus on using more complex sentence structures in your second paragraph."
            });
            setIsGrading(false);
        }, 2000);
    };

    return (
        <div className="min-h-screen p-10 bg-background text-white">
            <header className="max-w-5xl mx-auto flex items-center gap-6 mb-12">
                <button onClick={onBack} className="p-2 glass rounded-lg hover:bg-white/5 transition-colors">
                    <ChevronLeft />
                </button>
                <div>
                    <h1 className="text-4xl font-bold flex items-center gap-3">
                        <Sparkles className="text-primary animate-glow" />
                        AI Essay Grader
                    </h1>
                    <p className="text-text-dim mt-1">Professional evaluation for IELTS, SOPs, and Assignments.</p>
                </div>
            </header>

            <main className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Upload Section */}
                <div className="lg:col-span-1 space-y-6">
                    <GlowCard className="text-center py-10">
                        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
                            <Upload className="text-primary" size={32} />
                        </div>
                        <h3 className="text-xl font-bold mb-2">Upload Submission</h3>
                        <p className="text-sm text-text-dim mb-8">PDF, Word, or Text files accepted.</p>

                        <input type="file" id="essay-upload" className="hidden" onChange={(e) => setFile(e.target.files[0])} />
                        <label htmlFor="essay-upload" className="btn-secondary w-full justify-center mb-4 cursor-pointer">
                            {file ? file.name : 'Select File'}
                        </label>

                        <button
                            disabled={!file || isGrading}
                            onClick={handleUpload}
                            className="btn-primary w-full justify-center disabled:opacity-50"
                        >
                            {isGrading ? 'Grading...' : 'Start Evaluation'}
                        </button>
                    </GlowCard>

                    <GlowCard className="bg-amber-500/5 border-amber-500/10">
                        <div className="flex gap-3">
                            <AlertCircle className="text-amber-500 shrink-0" />
                            <div className="text-sm text-amber-500/80">
                                AI grading is based on typical examiner rubrics. Use this as a guide for improvement.
                            </div>
                        </div>
                    </GlowCard>
                </div>

                {/* Results Section */}
                <div className="lg:col-span-2">
                    {isGrading ? (
                        <div className="h-full flex flex-col items-center justify-center glass rounded-2xl p-12 text-center">
                            <div className="w-20 h-20 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6" />
                            <h2 className="text-2xl font-bold mb-2">Analyzing your writing...</h2>
                            <p className="text-text-dim">Our AI is checking for coherence, lexical range, and grammatical accuracy.</p>
                        </div>
                    ) : result ? (
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                            <GlowCard>
                                <div className="flex justify-between items-start mb-10">
                                    <div>
                                        <div className="text-sm text-primary font-bold uppercase tracking-wider mb-1">Overall Band Score</div>
                                        <div className="text-6xl font-bold">{result.score}</div>
                                        <div className="text-text-dim mt-2">{result.band}</div>
                                    </div>
                                    <CheckCircle className="text-emerald-500 w-12 h-12" />
                                </div>

                                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
                                    {Object.entries(result.criteria).map(([name, score]) => (
                                        <div key={name} className="glass p-4 rounded-xl text-center">
                                            <div className="text-2xl font-bold text-primary">{score}</div>
                                            <div className="text-[10px] uppercase text-text-dim mt-1">{name}</div>
                                        </div>
                                    ))}
                                </div>

                                <div className="border-t border-white/5 pt-8">
                                    <h4 className="font-bold mb-4 flex items-center gap-2">
                                        <Sparkles size={16} className="text-primary" />
                                        AI Insights & Corrections
                                    </h4>
                                    <p className="text-text-dim leading-relaxed h-48 overflow-y-auto pr-4">
                                        {result.feedback}
                                    </p>
                                </div>
                            </GlowCard>
                        </motion.div>
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-2xl p-12 text-center group hover:border-primary/20 transition-colors">
                            <FileText className="text-white/5 group-hover:text-primary/20 transition-colors mb-6" size={80} />
                            <h3 className="text-xl font-bold text-text-dim">Your result will appear here.</h3>
                            <p className="text-sm text-text-dim/60">Upload your work on the left to begin the AI analysis.</p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

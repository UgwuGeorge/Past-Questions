import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { ChevronLeft, FileText, Download, Eye, Search, BookOpen, Layers, Clock } from 'lucide-react';
import GlowCard from '../components/GlowCard';

const API_BASE = "http://localhost:8000/api";

export default function ExamRepo({ examType, onExit }) {
    const [id, setId] = useState(null);
    const [subjects, setSubjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [view, setView] = useState('subjects'); // subjects | years | document
    const [selectedSubject, setSelectedSubject] = useState(null); // This will be the subject object {id, name}
    const [selectedYear, setSelectedYear] = useState(null);
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
        const fetchInitial = async () => {
            setLoading(true);
            try {
                // First find the exam record by name to get its ID
                const examsRes = await fetch(`${API_BASE}/exams`);
                const examsData = await examsRes.json();
                const examRecord = examsData.find(e =>
                    e.name.toUpperCase() === examType.toUpperCase() ||
                    (examType === 'THE BAR EXAM' && e.name.includes('BAR')) ||
                    e.name.startsWith(examType.split(' ')[0])
                ) || (examType === 'WAEC' ? { id: 2, name: 'WAEC' } : null);

                if (!examRecord) throw new Error(`${examType} not found in database.`);
                setId(examRecord.id);

                // Fetch subjects for this exam
                const subRes = await fetch(`${API_BASE}/exams/${examRecord.id}/subjects`);
                const subData = await subRes.json();
                setSubjects(Array.isArray(subData) ? subData : []);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchInitial();
    }, [examType]);

    const handleSelectSubject = (subjectItem) => {
        setSelectedSubject(subjectItem);
        setView('years');
    };

    const handleSelectYear = async (year) => {
        setSelectedYear(year);
        setLoading(true);
        try {
            // Fetch questions for the selected subject
            const qRes = await fetch(`${API_BASE}/subjects/${selectedSubject.id}/questions?limit=50`);
            const qData = await qRes.json();

            // If we have year data, filter by it. Otherwise show all.
            const filtered = Array.isArray(qData)
                ? qData.filter(q => !year || q.year === parseInt(year) || !q.year)
                : [];

            // Normalize choices for display if they are list of objects
            const normalized = filtered.map(q => ({
                ...q,
                choices: Array.isArray(q.choices)
                    ? q.choices.reduce((acc, c) => ({ ...acc, [c.label]: c.text }), {})
                    : q.choices
            }));

            setQuestions(normalized);
            setView('document');
        } catch (err) {
            console.error("Failed to fetch questions:", err);
            setQuestions([]);
            setView('document');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return (
        <div className="h-screen flex items-center justify-center bg-background">
            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
    );

    return (
        <div className="h-screen flex flex-col bg-background overflow-hidden relative">
            <div className="absolute top-0 right-0 w-[50%] h-[30%] bg-primary/5 blur-[120px] rounded-full -z-10" />

            <header className="glass px-8 py-5 flex items-center justify-between border-b border-white/5 shrink-0 z-10">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => {
                            if (view === 'subjects') onExit();
                            else if (view === 'years') setView('subjects');
                            else setView('years');
                        }}
                        className="p-2 hover:bg-white/5 rounded-xl transition-all border border-white/5 group"
                    >
                        <ChevronLeft className="group-hover:-translate-x-0.5 transition-transform" />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold flex items-center gap-2">
                            <Layers size={20} className="text-primary" />
                            {examType} PDF REPO
                        </h1>
                        <p className="text-[10px] text-text-dim uppercase tracking-widest font-black">
                            {view === 'subjects' && "Electronic Archive"}
                            {view === 'years' && `${selectedSubject.name} Archive`}
                            {view === 'document' && `${selectedSubject.name} • ${selectedYear} Document`}
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <div className="hidden md:flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-[10px] font-black uppercase tracking-tighter text-white/40">
                        <Clock size={12} /> Last updated: Today
                    </div>
                </div>
            </header>

            <main className="flex-1 overflow-y-auto custom-scrollbar p-10">
                <AnimatePresence mode="wait">
                    {view === 'subjects' && (
                        <motion.div
                            key="subjects"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto w-full"
                        >
                            {subjects.map((sub, i) => (
                                <div
                                    key={sub.id}
                                    onClick={() => handleSelectSubject(sub)}
                                    className="group relative glass rounded-3xl p-8 border border-white/5 hover:border-primary/40 hover:bg-white/[0.03] transition-all cursor-pointer overflow-hidden"
                                >
                                    <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity">
                                        <FileText size={120} />
                                    </div>
                                    <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 border border-primary/20 group-hover:scale-110 transition-transform">
                                        <BookOpen className="text-primary" size={26} />
                                    </div>
                                    <h3 className="text-2xl font-bold mb-2 group-hover:text-primary transition-colors">{sub.name}</h3>
                                    <div className="flex gap-4 items-center">
                                        <div className="text-[10px] text-text-dim font-black uppercase tracking-wider">Multi-Year Archive</div>
                                        <div className="w-1 h-1 bg-white/10 rounded-full" />
                                        <div className="text-[10px] text-emerald-400 font-black uppercase tracking-wider">Indexed</div>
                                    </div>
                                </div>
                            ))}
                        </motion.div>
                    )}

                    {view === 'years' && (
                        <motion.div
                            key="years"
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 1.02 }}
                            className="max-w-4xl mx-auto w-full"
                        >
                            <div className="flex items-center gap-3 mb-10 pb-6 border-b border-white/5">
                                <div className="text-3xl font-black">{selectedSubject.name}</div>
                                <div className="px-3 py-1 bg-primary/10 border border-primary/20 rounded-full text-[10px] text-primary font-black uppercase tracking-widest">Select Edition</div>
                            </div>
                            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                                {['2023', '2022', '2021', '2020', '2019', '2018'].map((year, i) => (
                                    <button
                                        key={year}
                                        onClick={() => handleSelectYear(year)}
                                        className="glass rounded-2xl p-6 text-center border border-white/5 hover:border-primary/40 hover:-translate-y-1 transition-all group"
                                    >
                                        <div className="text-2xl font-black mb-1 group-hover:text-primary transition-colors">{year}</div>
                                        <div className="text-[10px] text-text-dim uppercase font-black tracking-widest">Document Set</div>
                                    </button>
                                ))}
                                <button
                                    onClick={() => handleSelectYear(null)}
                                    className="glass rounded-2xl p-6 text-center border border-white/5 hover:border-primary/40 hover:-translate-y-1 transition-all group col-span-2"
                                >
                                    <div className="text-xl font-black mb-1 group-hover:text-primary transition-colors">Complete Archive</div>
                                    <div className="text-[10px] text-text-dim uppercase font-black tracking-widest">All Questions</div>
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {view === 'document' && (
                        <motion.div
                            key="document"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="max-w-4xl mx-auto w-full pb-20"
                        >
                            <div className="flex justify-between items-center mb-10">
                                <div>
                                    <h2 className="text-4xl font-black mb-2">{selectedSubject.name} <span className="text-primary">{selectedYear || 'Archive'}</span></h2>
                                    <div className="flex gap-4 items-center text-text-dim text-xs">
                                        <span className="flex items-center gap-1.5"><FileText size={14} /> PDF SOURCE: DB_INTERNAL</span>
                                        <span className="w-1 h-1 bg-white/20 rounded-full" />
                                        <span className="flex items-center gap-1.5"><Eye size={14} /> READ ONLY MODE</span>
                                    </div>
                                </div>
                                <button className="btn-primary gap-2 py-3 px-6 shadow-xl shadow-primary/20">
                                    <Download size={18} /> Download PDF
                                </button>
                            </div>

                            <div className="glass shadow-2xl rounded-[40px] border border-white/5 bg-white/[0.01] p-12 md:p-20 overflow-hidden relative">
                                {/* Watermark */}
                                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 -rotate-12 pointer-events-none opacity-[0.02] text-9xl font-black select-none">
                                    REHARZ REPO
                                </div>

                                {questions.length > 0 ? (
                                    <div className="space-y-16 relative">
                                        {questions.map((q, i) => (
                                            <div key={i} className="relative">
                                                <div className="absolute -left-12 top-0 text-primary font-black opacity-20 text-3xl">{i + 1}</div>
                                                <h4 className="text-xl font-medium leading-relaxed mb-8 text-white/90">{q.text}</h4>
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                                                    {Object.entries(q.choices).map(([label, text]) => (
                                                        <div key={label} className="flex gap-4 items-start py-2 border-l border-white/5 pl-4 hover:border-primary/20 transition-colors">
                                                            <span className="text-primary font-black w-6">{label}</span>
                                                            <span className="text-text-dim leading-relaxed">{text}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="text-center py-20">
                                        <div className="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6">
                                            <Search className="text-white/20" size={32} />
                                        </div>
                                        <h3 className="text-xl font-bold mb-2">No Digitized Data Found</h3>
                                        <p className="text-text-dim italic">The raw PDF is currently undergoing OCR processing. Check back soon.</p>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}

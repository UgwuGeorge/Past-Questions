import React, { useState, useEffect } from 'react';
import { ChevronUp } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

export default function ScrollToTop({ scrollContainerRef }) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const container = scrollContainerRef?.current;
        if (!container) return;

        const checkScroll = () => {
            if (container.scrollTop > 300) {
                setIsVisible(true);
            } else {
                setIsVisible(false);
            }
        };

        container.addEventListener('scroll', checkScroll);
        return () => container.removeEventListener('scroll', checkScroll);
    }, [scrollContainerRef]);

    const scrollToTop = () => {
        scrollContainerRef?.current?.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    return (
        <AnimatePresence>
            {isVisible && (
                <motion.button
                    initial={{ opacity: 0, y: 20, scale: 0.8 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 20, scale: 0.8 }}
                    onClick={scrollToTop}
                    className="scroll-to-top"
                    title="Scroll to Top"
                >
                    <ChevronUp size={24} />
                </motion.button>
            )}
        </AnimatePresence>
    );
}

import { motion } from "framer-motion";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export default function GlowCard({ children, className, delay = 0 }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay }}
            whileHover={{ y: -5, scale: 1.02 }}
            className={twMerge(
                "glass glass-hover p-6 rounded-2xl group relative overflow-hidden",
                className
            )}
        >
            {/* Glow Effect */}
            <div className="absolute -inset-px bg-gradient-to-r from-primary/50 to-secondary/50 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity blur-xl -z-10" />

            {children}
        </motion.div>
    );
}

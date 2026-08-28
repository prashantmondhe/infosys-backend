"use client";

import { motion } from "framer-motion";
import { fadeIn } from "@/lib/animations";

interface AnimatedContainerProps {
  children: React.ReactNode;
}

export default function AnimatedContainer({
  children,
}: AnimatedContainerProps) {
  return (
    <motion.div
      variants={fadeIn}
      initial="hidden"
      animate="visible"
    >
      {children}
    </motion.div>
  );
}
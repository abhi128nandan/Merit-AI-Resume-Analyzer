"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, Loader2, FileSearch, Zap, LineChart } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const STEPS = [
  { id: 1, label: "Extracting text from document...", icon: FileSearch },
  { id: 2, label: "Analyzing semantic structure...", icon: Zap },
  { id: 3, label: "Comparing against job description...", icon: LineChart },
  { id: 4, label: "Generating ATS score...", icon: CheckCircle2 },
];

export default function LoadingState() {
  const [currentStep, setCurrentStep] = useState(1);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const totalDuration = 5000; // 5 seconds
    const interval = 50;
    const steps = totalDuration / interval;
    let current = 0;

    const timer = setInterval(() => {
      current++;
      const newProgress = Math.min((current / steps) * 100, 100);
      setProgress(newProgress);

      if (newProgress > 75) setCurrentStep(4);
      else if (newProgress > 50) setCurrentStep(3);
      else if (newProgress > 25) setCurrentStep(2);

      if (current >= steps) {
        clearInterval(timer);
      }
    }, interval);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-background items-center justify-center p-6">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold tracking-tight">Analyzing Resume</h2>
          <p className="text-muted-foreground text-sm">Please wait while our engine processes your document.</p>
        </div>

        <Card className="p-6 bg-card border shadow-lg">
          <div className="space-y-6">
            {STEPS.map((step) => {
              const isActive = currentStep === step.id;
              const isPast = currentStep > step.id;
              const Icon = step.icon;

              return (
                <div key={step.id} className="flex items-center gap-4">
                  <div className="relative">
                    <AnimatePresence mode="popLayout">
                      {isPast ? (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="w-8 h-8 bg-emerald-500/15 rounded-full flex items-center justify-center text-emerald-600 dark:text-emerald-400"
                        >
                          <CheckCircle2 className="w-4 h-4" />
                        </motion.div>
                      ) : isActive ? (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="w-8 h-8 bg-primary/15 rounded-full flex items-center justify-center text-primary"
                        >
                          <Loader2 className="w-4 h-4 animate-spin" />
                        </motion.div>
                      ) : (
                        <div className="w-8 h-8 rounded-full border-2 border-muted flex items-center justify-center">
                          <Icon className="w-4 h-4 text-muted-foreground" />
                        </div>
                      )}
                    </AnimatePresence>
                  </div>
                  <span
                    className={`text-sm font-medium transition-colors ${
                      isActive ? "text-foreground" : isPast ? "text-muted-foreground" : "text-muted-foreground/50"
                    }`}
                  >
                    {step.label}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="mt-8 space-y-2">
            <Progress value={progress} className="h-2" />
            <div className="flex justify-between text-xs text-muted-foreground font-mono">
              <span>{Math.round(progress)}%</span>
              <span>Processing</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

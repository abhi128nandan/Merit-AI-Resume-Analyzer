"use client";

import { useState, useRef } from "react";
import { Upload, FileText, CheckCircle2, AlertCircle, Terminal, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { motion, AnimatePresence } from "framer-motion";
import { analyzeMatch, AnalysisResponse, ApiError } from "@/lib/api";
import { AnalysisResults } from "@/components/AnalysisResults";

export default function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  
  const jdInputRef = useRef<HTMLTextAreaElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file || !jd.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await analyzeMatch(file, jd);
      setResults(response);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  if (results) {
    return (
      <div className="min-h-screen bg-background pt-12 pb-24 px-4">
        <AnalysisResults data={results} onReset={() => { setResults(null); setFile(null); setJd(""); }} />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <header className="px-6 h-16 flex items-center border-b border-border/40 backdrop-blur-md sticky top-0 z-50">
        <div className="font-bold text-xl tracking-tighter flex items-center gap-2 cursor-pointer" onClick={() => window.location.href="/"}>
          <div className="w-5 h-5 bg-foreground rounded-sm flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-background rounded-full" />
          </div>
          Merit
        </div>
        <div className="ml-auto text-xs font-mono text-muted-foreground flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          API Connected
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 flex flex-col items-center justify-center py-12 max-w-4xl relative">
        <AnimatePresence mode="wait">
          {!isLoading ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
              className="w-full"
            >
              <div className="text-center mb-12">
                <h1 className="text-4xl font-bold tracking-tight mb-3">Initiate Analysis</h1>
                <p className="text-muted-foreground text-lg max-w-lg mx-auto">
                  Provide your resume and the target job description. Our engine will map semantic connections and generate an ATS score.
                </p>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-lg flex items-center gap-2 max-w-2xl mx-auto">
                  <AlertCircle className="w-5 h-5" />
                  <span className="font-medium text-sm">{error}</span>
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                {/* File Dropzone */}
                <div
                  className={`relative overflow-hidden rounded-2xl border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center p-8 text-center min-h-[320px] cursor-pointer
                    ${isDragging ? "border-emerald-500 bg-emerald-500/5 scale-[1.02]" : "border-border/60 hover:border-foreground/30 hover:bg-secondary/20"}
                    ${file ? "border-solid border-foreground/20 bg-secondary/10" : ""}
                  `}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById("resume-upload")?.click()}
                >
                  <input
                    id="resume-upload"
                    type="file"
                    className="hidden"
                    accept=".pdf,.doc,.docx"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        setFile(e.target.files[0]);
                        setTimeout(() => jdInputRef.current?.focus(), 100);
                      }
                    }}
                  />
                  
                  {!file ? (
                    <>
                      <div className="w-14 h-14 bg-secondary rounded-full flex items-center justify-center mb-6">
                        <Upload className="w-6 h-6 text-foreground" />
                      </div>
                      <h3 className="text-lg font-semibold mb-2">Upload Resume</h3>
                      <p className="text-sm text-muted-foreground max-w-[200px] mb-4">
                        Drag and drop your PDF or DOCX file here.
                      </p>
                      <Button variant="secondary" size="sm" className="pointer-events-none">Select File</Button>
                    </>
                  ) : (
                    <div className="flex flex-col items-center text-foreground">
                      <FileText className="w-12 h-12 mb-4 text-emerald-500" />
                      <p className="font-medium text-lg mb-1">{file.name}</p>
                      <p className="text-sm text-muted-foreground mb-6">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                      <div className="flex gap-3">
                        <Button 
                          variant="outline" 
                          size="sm" 
                          onClick={(e) => {
                            e.stopPropagation();
                            setFile(null);
                          }}
                        >
                          Remove
                        </Button>
                        <Button 
                          variant="secondary" 
                          size="sm"
                          className="pointer-events-none"
                        >
                          <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-500" />
                          Ready
                        </Button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Job Description */}
                <div className="flex flex-col relative rounded-2xl border border-border/60 overflow-hidden shadow-sm bg-card transition-colors focus-within:border-foreground/30 focus-within:ring-1 focus-within:ring-foreground/30">
                  <div className="px-6 py-4 border-b border-border/40 bg-secondary/30 flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-muted-foreground" />
                    <span className="font-medium text-sm">Target Job Description</span>
                  </div>
                  <Textarea
                    ref={jdInputRef}
                    placeholder="Paste the full job description here. Include responsibilities, requirements, and qualifications..."
                    className="flex-1 resize-none border-0 focus-visible:ring-0 p-6 bg-transparent text-sm leading-relaxed rounded-none min-h-[250px]"
                    value={jd}
                    onChange={(e) => setJd(e.target.value)}
                  />
                </div>
              </div>

              {/* Action Bar */}
              <div className="mt-12 flex flex-col items-center">
                <Button 
                  size="lg" 
                  disabled={!file || jd.trim().length < 50}
                  onClick={handleAnalyze}
                  className="h-14 px-12 text-lg rounded-full shadow-xl shadow-foreground/10 group"
                >
                  Start Processing
                  <ArrowRight className="ml-3 h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Button>
                {(!file || jd.trim().length < 50) && (
                  <p className="text-sm text-muted-foreground mt-4">
                    Please provide both a resume and a job description to continue.
                  </p>
                )}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="w-full max-w-2xl border border-border/40 bg-card rounded-2xl shadow-2xl overflow-hidden"
            >
              <div className="border-b border-border/40 bg-secondary/30 px-4 py-3 flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-border" />
                  <div className="w-3 h-3 rounded-full bg-border" />
                  <div className="w-3 h-3 rounded-full bg-border" />
                </div>
                <div className="ml-4 text-xs font-mono text-muted-foreground">merit-analysis-engine</div>
              </div>
              <div className="p-8 md:p-12 flex flex-col items-center justify-center text-center">
                <div className="relative w-24 h-24 mb-8">
                  {/* Premium Pulsing loader */}
                  <div className="absolute inset-0 border-4 border-foreground/10 rounded-full" />
                  <motion.div 
                    className="absolute inset-0 border-4 border-emerald-500 rounded-full border-t-transparent"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-10 h-10 bg-foreground rounded-sm flex items-center justify-center">
                      <div className="w-3 h-3 bg-background rounded-full" />
                    </div>
                  </div>
                </div>
                <h3 className="text-2xl font-bold mb-2">Analyzing Profile</h3>
                <p className="text-muted-foreground max-w-sm">
                  Performing deep semantic extraction and cross-referencing against ATS criteria. This usually takes 5-10 seconds.
                </p>
                <div className="mt-8 flex gap-2">
                   <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                   <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping [animation-delay:200ms]" />
                   <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping [animation-delay:400ms]" />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

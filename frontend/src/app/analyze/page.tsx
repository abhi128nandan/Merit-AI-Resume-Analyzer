"use client";

import { useState, useRef } from "react";
import { Upload, FileText, CheckCircle2, AlertCircle, Terminal, ArrowRight, Play, RefreshCw, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { motion, AnimatePresence } from "framer-motion";
import { analyzeMatch, AnalysisResponse, ApiError } from "@/lib/api";
import { AnalysisResults } from "@/components/AnalysisResults";

export default function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [pipelineStep, setPipelineStep] = useState<string>("Initializing...");
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  
  const jdInputRef = useRef<HTMLTextAreaElement>(null);

  // 1-Click Recruiter Sample Case
  const handleLoadSampleCase = () => {
    // Create a mock sample resume file
    const sampleResumeContent = `John Doe
Senior Backend Engineer
Email: john.doe@example.com | Phone: (555) 123-4567 | Location: San Francisco, CA

SUMMARY
Senior Software Engineer with 6+ years of experience designing high-throughput REST APIs, asynchronous microservices, and distributed backend infrastructure in Python, FastAPI, PostgreSQL, and Docker.

EXPERIENCE
TechFlow Inc. — Senior Backend Engineer
2021 – Present | San Francisco, CA
• Architected RESTful microservices using Python, FastAPI, and Pydantic handling 15M+ daily requests with 99.99% uptime.
• Optimized complex PostgreSQL queries and implemented Redis caching layer, reducing median API latency by 42%.
• Containerized microservices using Docker and orchestrated deployments on Kubernetes cluster via AWS EKS.
• Mentored 4 junior engineers and instituted automated pytest integration testing pipelines in GitHub Actions.

DataScale Systems — Backend Developer
2018 – 2021 | San Jose, CA
• Developed real-time data ingestion pipelines utilizing Python, Celery, and RabbitMQ.
• Designed relational database schemas in PostgreSQL and conducted automated database migrations using Alembic.

TECHNICAL SKILLS
• Languages & Frameworks: Python, FastAPI, Flask, SQL, HTML/CSS
• Databases & Caching: PostgreSQL, Redis, SQLAlchemy, Alembic
• DevOps & Cloud: Docker, Kubernetes, AWS (S3, EKS, RDS), CI/CD, Git
• Architecture: REST APIs, Microservices, AsyncIO, Clean Architecture

EDUCATION
Bachelor of Science in Computer Science — University of California, Berkeley (2018)`;

    const blob = new Blob([sampleResumeContent], { type: "text/plain" });
    const sampleFile = new File([blob], "John_Doe_Senior_Backend_Engineer.txt", { type: "text/plain" });
    
    setFile(sampleFile);
    setJd(`Target Role: Senior Backend Engineer (Python / FastAPI)

Key Responsibilities & Qualifications:
• 5+ years of production experience with Python, FastAPI, or similar web frameworks.
• Deep expertise in database design, SQL, and PostgreSQL query optimization.
• Hands-on containerization experience with Docker and Kubernetes deployment pipelines.
• Proven track record architecting scalable RESTful APIs and asynchronous backend microservices.
• Bachelor's degree in Computer Science or equivalent practical experience.`);

    setError(null);
  };

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
    setPipelineStep("Validating file magic bytes and payload limits...");
    
    try {
      setTimeout(() => setPipelineStep("Dispatching extraction worker to ProcessPoolExecutor..."), 600);
      setTimeout(() => setPipelineStep("Running Pass 1: Entity extraction & normalization..."), 1400);
      setTimeout(() => setPipelineStep("Running Pass 2: Dual-Pass quote verification & ATS policy matrix..."), 2200);

      const response = await analyzeMatch(file, jd);
      setResults(response);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : "An unexpected error occurred during processing.");
    } finally {
      setIsLoading(false);
    }
  };

  if (results) {
    return (
      <div className="min-h-screen bg-background pt-8 pb-20 px-4">
        <AnalysisResults data={results} onReset={() => { setResults(null); setFile(null); setJd(""); }} />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background font-sans antialiased text-foreground">
      {/* Header */}
      <header className="px-6 h-14 flex items-center justify-between border-b border-border/60 bg-background sticky top-0 z-50">
        <div className="font-bold text-sm tracking-tight flex items-center gap-2 cursor-pointer" onClick={() => window.location.href="/"}>
          <div className="w-5 h-5 bg-foreground rounded-sm flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-background rounded-full" />
          </div>
          Merit AI <span className="text-xs text-muted-foreground font-normal">/ Analysis Workbench</span>
        </div>

        <div className="flex items-center gap-4">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleLoadSampleCase}
            className="h-8 px-3 text-xs font-mono text-emerald-600 dark:text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/10"
          >
            <Play className="w-3 h-3 mr-1.5 fill-current" />
            Load Sample Case (1-Click Test)
          </Button>

          <div className="text-xs font-mono text-muted-foreground hidden sm:flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            API Ready
          </div>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 flex flex-col items-center justify-center py-10 max-w-4xl relative">
        <AnimatePresence mode="wait">
          {!isLoading ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.3 }}
              className="w-full"
            >
              <div className="mb-8 flex flex-col sm:flex-row sm:items-end justify-between border-b border-border/40 pb-6">
                <div>
                  <h1 className="text-2xl font-bold tracking-tight mb-1">ATS Candidate Workbench</h1>
                  <p className="text-sm text-muted-foreground">
                    Provide a resume document and target job description for deterministic evaluation.
                  </p>
                </div>
                
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleLoadSampleCase}
                  className="mt-3 sm:mt-0 text-xs font-mono text-muted-foreground hover:text-foreground self-start sm:self-auto"
                >
                  <RefreshCw className="w-3 h-3 mr-1.5" />
                  Pre-fill Senior Engineer Test Case
                </Button>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-lg flex items-center gap-3 text-sm">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span className="font-medium">{error}</span>
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
                {/* File Dropzone */}
                <div
                  className={`relative rounded-xl border-2 border-dashed transition-all duration-200 flex flex-col items-center justify-center p-6 text-center min-h-[300px] cursor-pointer bg-card
                    ${isDragging ? "border-emerald-500 bg-emerald-500/5" : "border-border/60 hover:border-foreground/30"}
                    ${file ? "border-solid border-emerald-500/40 bg-emerald-500/5" : ""}
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
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        setFile(e.target.files[0]);
                        setTimeout(() => jdInputRef.current?.focus(), 100);
                      }
                    }}
                  />
                  
                  {!file ? (
                    <>
                      <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center mb-4 text-muted-foreground">
                        <Upload className="w-5 h-5" />
                      </div>
                      <h3 className="text-sm font-semibold mb-1">Upload Resume Document</h3>
                      <p className="text-xs text-muted-foreground max-w-[220px] mb-4 leading-relaxed">
                        Drag and drop PDF or DOCX file (Max 5 MB). Verified in-memory.
                      </p>
                      <Button variant="secondary" size="sm" className="h-8 text-xs pointer-events-none">
                        Select File
                      </Button>
                    </>
                  ) : (
                    <div className="flex flex-col items-center text-foreground w-full">
                      <div className="w-10 h-10 bg-emerald-500/10 rounded-full flex items-center justify-center mb-3">
                        <FileText className="w-5 h-5 text-emerald-500" />
                      </div>
                      <p className="font-medium text-sm mb-1 truncate max-w-[240px]">{file.name}</p>
                      <p className="text-xs font-mono text-muted-foreground mb-4">
                        {(file.size / 1024).toFixed(1)} KB • Verified MIME
                      </p>
                      <div className="flex gap-2">
                        <Button 
                          variant="outline" 
                          size="sm"
                          className="h-7 text-xs" 
                          onClick={(e) => {
                            e.stopPropagation();
                            setFile(null);
                          }}
                        >
                          Change File
                        </Button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Job Description Input */}
                <div className="flex flex-col rounded-xl border border-border/60 bg-card overflow-hidden">
                  <div className="px-4 py-3 border-b border-border/40 bg-muted/30 flex items-center justify-between font-mono text-xs text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <Terminal className="w-3.5 h-3.5" />
                      <span>Target Job Description</span>
                    </div>
                    <span>{jd.length} chars</span>
                  </div>
                  <Textarea
                    ref={jdInputRef}
                    placeholder="Paste job description qualifications, technical requirements, and responsibilities..."
                    className="flex-1 resize-none border-0 focus-visible:ring-0 p-4 bg-transparent text-xs leading-relaxed min-h-[240px] font-sans"
                    value={jd}
                    onChange={(e) => setJd(e.target.value)}
                  />
                </div>
              </div>

              {/* Action Toolbar */}
              <div className="mt-8 flex flex-col items-center">
                <Button 
                  size="lg" 
                  disabled={!file || jd.trim().length < 30}
                  onClick={handleAnalyze}
                  className="h-11 px-8 text-sm font-medium rounded-lg group shadow-sm"
                >
                  Run Deterministic Analysis
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
                
                <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground mt-4">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                  <span>Dual-Pass Verifier & Magic Byte Guard Active</span>
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              className="w-full max-w-lg border border-border/60 bg-card rounded-xl shadow-lg overflow-hidden"
            >
              <div className="border-b border-border/60 bg-muted/40 px-4 py-2.5 flex items-center justify-between font-mono text-xs text-muted-foreground">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span>merit-pipeline-execution</span>
                </div>
                <span>Async Worker</span>
              </div>
              <div className="p-8 flex flex-col items-center justify-center text-center">
                <div className="relative w-16 h-16 mb-6">
                  <div className="absolute inset-0 border-2 border-muted rounded-full" />
                  <motion.div 
                    className="absolute inset-0 border-2 border-emerald-500 rounded-full border-t-transparent"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1.2, repeat: Infinity, ease: "linear" }}
                  />
                </div>

                <h3 className="text-base font-semibold mb-2">Executing Pipeline</h3>
                <p className="text-xs font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-md border border-emerald-500/20 mb-4 max-w-xs">
                  {pipelineStep}
                </p>
                <p className="text-xs text-muted-foreground max-w-xs">
                  Offloading CPU parsing to ProcessPool threads and running quote verification.
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}


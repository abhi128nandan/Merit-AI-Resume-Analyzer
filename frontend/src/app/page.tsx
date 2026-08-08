"use client";

import { useState } from "react";
import { 
  ArrowRight, 
  CheckCircle2, 
  Layers, 
  Cpu, 
  Lock, 
  Terminal, 
  FileText, 
  Search, 
  ShieldCheck, 
  Sparkles,
  ChevronRight
} from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function ProductOverviewPage() {
  const [activeStep, setActiveStep] = useState<number>(3);
  const [selectedDemoTab, setSelectedDemoTab] = useState<"matched" | "evidence" | "policy">("matched");

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground font-sans antialiased">
      {/* Navigation Header */}
      <header className="px-6 h-14 flex items-center justify-between border-b border-border/60 bg-background/95 backdrop-blur-md sticky top-0 z-40">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 bg-foreground rounded-sm flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-background rounded-full" />
          </div>
          <span className="font-bold text-sm tracking-tight">Merit AI</span>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-muted text-muted-foreground border border-border/40">v1.0.0</span>
        </div>

        <nav className="flex items-center gap-6 text-xs font-mono text-muted-foreground" aria-label="Main Navigation">
          <a href="#pipeline-demo" className="hover:text-foreground transition-colors hidden sm:block">Demonstration</a>
          <a href="#system-architecture" className="hover:text-foreground transition-colors hidden sm:block">Architecture</a>
          <a href="#matching-policy" className="hover:text-foreground transition-colors hidden sm:block">Policy Matrix</a>
          <div className="w-px h-3 bg-border hidden sm:block" />
          <Link href="/analyze">
            <Button size="sm" className="h-8 px-4 text-xs font-medium font-sans focus-ring">
              Launch Workbench
              <ArrowRight className="ml-1.5 w-3.5 h-3.5" />
            </Button>
          </Link>
        </nav>
      </header>

      <main id="main-content" className="flex-1">
        {/* Product Demonstration Hero */}
        <section className="container mx-auto px-6 pt-16 pb-14 max-w-5xl">
          <div className="max-w-3xl mb-12">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span>Verbatim Ground-Truth Engine • 100% Explainable</span>
            </div>

            <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight mb-5">
              Resume intelligence engineered for deterministic ATS evaluation.
            </h1>

            <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-8 max-w-2xl">
              Traditional ATS software relies on naive keyword search. LLMs hallucinate skills. 
              Merit combines strict text extraction, fixed policy weights, and verbatim quote verification to prove candidate-job compatibility.
            </p>

            <div className="flex flex-wrap items-center gap-4">
              <Link href="/analyze">
                <Button size="lg" className="h-11 px-6 text-sm font-semibold group shadow-sm focus-ring">
                  Launch Interactive Workbench
                  <ArrowRight className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <a href="#pipeline-demo">
                <Button variant="outline" size="lg" className="h-11 px-6 text-sm font-medium focus-ring">
                  View Product Pipeline Flow ↓
                </Button>
              </a>
            </div>
          </div>

          {/* 5-Step Visual Dataflow Pipeline */}
          <div id="pipeline-demo" className="rounded-xl border border-border/60 bg-card p-6 md:p-8 shadow-sm space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-border/40 pb-4 gap-2">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Product Workflow Pipeline</span>
                <h2 className="text-lg font-bold tracking-tight">How Merit Evaluates Candidates</h2>
              </div>
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20 self-start sm:self-auto">
                No Black-Box Scoring
              </span>
            </div>

            {/* Step Navigation Bar */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs font-mono">
              {[
                { num: "01", label: "Upload Resume", detail: "PDF / DOCX / TXT" },
                { num: "02", label: "Target Job Description", detail: "Role Requirements" },
                { num: "03", label: "Dual-Pass Verifier", detail: "Quote Extraction" },
                { num: "04", label: "ATS Policy Engine", detail: "40/30/20/10 Weight" },
                { num: "05", label: "Evidence Report", detail: "Match Score & Gap" },
              ].map((step, idx) => {
                const stepNum = idx + 1;
                const isActive = activeStep === stepNum;
                return (
                  <button
                    key={idx}
                    onClick={() => setActiveStep(stepNum)}
                    className={`p-3 rounded-lg border text-left transition-all cursor-pointer focus-ring ${
                      isActive 
                        ? "border-emerald-500/50 bg-emerald-500/10 text-foreground font-semibold" 
                        : "border-border/40 bg-muted/20 text-muted-foreground hover:bg-muted/40 hover:text-foreground"
                    }`}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className={isActive ? "text-emerald-400 font-bold" : "text-muted-foreground"}>{step.num}.</span>
                      {isActive && <ChevronRight className="w-3.5 h-3.5 text-emerald-400" />}
                    </div>
                    <div className="font-sans font-medium text-xs leading-tight truncate">{step.label}</div>
                    <div className="text-[10px] text-muted-foreground truncate">{step.detail}</div>
                  </button>
                );
              })}
            </div>

            {/* Interactive Stage Inspector Card */}
            <div className="p-5 rounded-lg bg-muted/30 border border-border/40 font-mono text-xs space-y-4">
              {activeStep === 1 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                    <FileText className="w-4 h-4" /> Stage 01: Multi-Format Extraction & Magic Byte Security
                  </div>
                  <p className="text-muted-foreground text-xs leading-relaxed font-sans">
                    Uploaded resumes are validated in-memory using magic header bytes (PDF header <code className="bg-muted px-1 rounded">%PDF-</code>, DOCX zip headers). Text is extracted cleanly using isolated workers without storing files to disk.
                  </p>
                  <div className="p-3 bg-background rounded border border-border/40 text-[11px] text-foreground">
                    ✓ Validated file MIME: application/pdf (1.2 MB)<br/>
                    ✓ Cleaned raw text stream: 1,505 characters
                  </div>
                </div>
              )}

              {activeStep === 2 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-indigo-400 font-semibold">
                    <Search className="w-4 h-4" /> Stage 02: Job Description Requirement Identification
                  </div>
                  <p className="text-muted-foreground text-xs leading-relaxed font-sans">
                    The job description detector extracts explicit technical skill requirements, years of experience, and required credentials using structural regex and lightweight LLM classification.
                  </p>
                  <div className="p-3 bg-background rounded border border-border/40 text-[11px] text-foreground">
                    ✓ Identified Role: Senior Backend Engineer (Python / FastAPI)<br/>
                    ✓ Extracted 5 Core Requirements: [Python, FastAPI, PostgreSQL, Docker, 5+ Yrs Exp]
                  </div>
                </div>
              )}

              {activeStep === 3 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                    <ShieldCheck className="w-4 h-4" /> Stage 03: Dual-Pass Verbatim Quote Verification
                  </div>
                  <p className="text-muted-foreground text-xs leading-relaxed font-sans">
                    Every skill or experience claim extracted by the model MUST be cross-referenced against verbatim document text. If a claim cannot be verified with a direct source quote, it is dropped to prevent hallucinations.
                  </p>
                  <div className="p-3 bg-background rounded border border-border/40 text-[11px] space-y-1.5">
                    <div className="text-emerald-400 flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Verified Match: &quot;Architected RESTful microservices using Python, FastAPI...&quot;</span>
                    </div>
                    <div className="text-muted-foreground flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-400" />
                      <span>Verified Match: &quot;Containerized microservices using Docker and Kubernetes...&quot;</span>
                    </div>
                  </div>
                </div>
              )}

              {activeStep === 4 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-amber-400 font-semibold">
                    <Layers className="w-4 h-4" /> Stage 04: Fixed Policy Matrix Scoring
                  </div>
                  <p className="text-muted-foreground text-xs leading-relaxed font-sans">
                    Instead of unconstrained model numbers, match scores are calculated deterministically:
                  </p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-[11px] text-center">
                    <div className="p-2 bg-background rounded border border-border/40">Hard Skills: 40%</div>
                    <div className="p-2 bg-background rounded border border-border/40">Experience: 30%</div>
                    <div className="p-2 bg-background rounded border border-border/40">Tooling: 20%</div>
                    <div className="p-2 bg-background rounded border border-border/40">Education: 10%</div>
                  </div>
                </div>
              )}

              {activeStep === 5 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                    <Sparkles className="w-4 h-4" /> Stage 05: Evidence-Backed Match Report & Revisions
                  </div>
                  <p className="text-muted-foreground text-xs leading-relaxed font-sans">
                    Presents an unambiguous hiring decision, breakdown of matched vs missing skills, exact quote references, and tailored keyword revisions.
                  </p>
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded text-[11px] text-emerald-400 font-bold">
                    RECOMMENDED • Overall ATS Match Score: 89 / 100
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Live Product Sample Demonstration Matrix */}
        <section id="demo-matrix" className="border-t border-b border-border/60 bg-muted/20 py-16">
          <div className="container mx-auto px-6 max-w-5xl">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-8">
              <div>
                <div className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-2">Live Demonstration Preview</div>
                <h2 className="text-2xl font-bold tracking-tight">Interactive Candidate Audit Matrix</h2>
              </div>
              
              <div className="flex gap-1 mt-4 md:mt-0 bg-card p-1 rounded-lg border border-border/60 text-xs font-mono">
                <button
                  onClick={() => setSelectedDemoTab("matched")}
                  className={`px-3 py-1.5 rounded transition-all cursor-pointer ${selectedDemoTab === "matched" ? "bg-muted text-emerald-400 font-semibold" : "text-muted-foreground hover:text-foreground"}`}
                >
                  Verified Skills
                </button>
                <button
                  onClick={() => setSelectedDemoTab("evidence")}
                  className={`px-3 py-1.5 rounded transition-all cursor-pointer ${selectedDemoTab === "evidence" ? "bg-muted text-indigo-400 font-semibold" : "text-muted-foreground hover:text-foreground"}`}
                >
                  Source Quotes
                </button>
                <button
                  onClick={() => setSelectedDemoTab("policy")}
                  className={`px-3 py-1.5 rounded transition-all cursor-pointer ${selectedDemoTab === "policy" ? "bg-muted text-amber-400 font-semibold" : "text-muted-foreground hover:text-foreground"}`}
                >
                  Policy Weights
                </button>
              </div>
            </div>

            {/* Demo Matrix Card */}
            <div className="rounded-xl border border-border/60 bg-card p-6 shadow-sm">
              {selectedDemoTab === "matched" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-muted-foreground flex justify-between">
                    <span>Target Qualification</span>
                    <span>Status</span>
                  </div>
                  <div className="space-y-2 text-xs font-mono">
                    <div className="p-3 bg-muted/30 rounded border border-border/40 flex justify-between items-center">
                      <span className="text-foreground">Python / FastAPI microservices (5+ Yrs)</span>
                      <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[10px] font-bold">VERIFIED MATCH</span>
                    </div>
                    <div className="p-3 bg-muted/30 rounded border border-border/40 flex justify-between items-center">
                      <span className="text-foreground">PostgreSQL query optimization & Redis</span>
                      <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[10px] font-bold">VERIFIED MATCH</span>
                    </div>
                    <div className="p-3 bg-muted/30 rounded border border-border/40 flex justify-between items-center">
                      <span className="text-foreground">Docker & Kubernetes orchestration</span>
                      <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[10px] font-bold">VERIFIED MATCH</span>
                    </div>
                  </div>
                </div>
              )}

              {selectedDemoTab === "evidence" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-muted-foreground">Verbatim Source Quote Verification (Pass 2)</div>
                  <div className="p-4 bg-muted/40 rounded border border-border/40 text-xs font-mono leading-relaxed space-y-3">
                    <div className="border-l-2 border-emerald-500 pl-3">
                      <span className="text-muted-foreground text-[10px] block">REQUIREMENT: Python / FastAPI</span>
                      <span className="text-foreground">&quot;Architected RESTful microservices using Python, FastAPI, and Pydantic handling 15M+ daily requests.&quot;</span>
                    </div>
                    <div className="border-l-2 border-emerald-500 pl-3">
                      <span className="text-muted-foreground text-[10px] block">REQUIREMENT: Database Optimization</span>
                      <span className="text-foreground">&quot;Optimized complex PostgreSQL queries and implemented Redis caching layer...&quot;</span>
                    </div>
                  </div>
                </div>
              )}

              {selectedDemoTab === "policy" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-muted-foreground">Deterministic Policy Scoring Breakdown</div>
                  <div className="space-y-3 text-xs font-mono">
                    <div>
                      <div className="flex justify-between text-muted-foreground mb-1">
                        <span>Hard Skills Match (40% Weight)</span>
                        <span className="text-emerald-400 font-bold">95 / 100</span>
                      </div>
                      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500 w-[95%]" />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-muted-foreground mb-1">
                        <span>Work Experience Relevancy (30% Weight)</span>
                        <span className="text-emerald-400 font-bold">88 / 100</span>
                      </div>
                      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500 w-[88%]" />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-muted-foreground mb-1">
                        <span>Education & Credentials (10% Weight)</span>
                        <span className="text-emerald-400 font-bold">100 / 100</span>
                      </div>
                      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500 w-[100%]" />
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Engineering Principles */}
        <section id="matching-policy" className="py-16 container mx-auto px-6 max-w-5xl">
          <div className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-2">Architectural Guarantees</div>
          <h2 className="text-2xl font-bold tracking-tight mb-10">Engineered on four verifiable constraints</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl border border-border/60 bg-card">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-4">
                <CheckCircle2 className="w-4.5 h-4.5" />
              </div>
              <h3 className="text-base font-semibold mb-2">1. Dual-Pass Quote Verification</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Extracted skills and credentials are matched against raw document strings. Unsubstantiated claims are dropped to prevent model hallucinations.
              </p>
            </div>

            <div className="p-6 rounded-xl border border-border/60 bg-card">
              <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4">
                <Layers className="w-4.5 h-4.5" />
              </div>
              <h3 className="text-base font-semibold mb-2">2. Mathematical Policy Scoring</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                ATS compatibility scores follow fixed matrix weights (Skills: 40%, Experience: 30%, Tooling: 20%, Education: 10%) rather than arbitrary LLM output.
              </p>
            </div>

            <div className="p-6 rounded-xl border border-border/60 bg-card">
              <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center mb-4">
                <Cpu className="w-4.5 h-4.5" />
              </div>
              <h3 className="text-base font-semibold mb-2">3. Non-Blocking ProcessPool Workers</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                CPU-intensive PDF and DOCX parsing routines are offloaded to Python worker processes, ensuring non-blocking async execution.
              </p>
            </div>

            <div className="p-6 rounded-xl border border-border/60 bg-card">
              <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center mb-4">
                <Lock className="w-4.5 h-4.5" />
              </div>
              <h3 className="text-base font-semibold mb-2">4. Zero-Persistence Security Guard</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Document payloads are validated via magic header bytes, processed transiently in-memory, and immediately purged post-analysis.
              </p>
            </div>
          </div>
        </section>

        {/* System Dataflow Console */}
        <section id="system-architecture" className="py-16 border-t border-border/60 bg-muted/10">
          <div className="container mx-auto px-6 max-w-5xl">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-8">
              <div>
                <div className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-2">Pipeline Telemetry</div>
                <h2 className="text-2xl font-bold tracking-tight">System Dataflow Architecture</h2>
              </div>
              <a 
                href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer/blob/main/docs/Architecture.md" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs font-mono text-muted-foreground hover:text-foreground mt-2 md:mt-0 flex items-center gap-1 focus-ring"
              >
                View Full Technical Spec on GitHub →
              </a>
            </div>

            {/* Architecture Console */}
            <div className="rounded-xl border border-border/60 bg-card overflow-hidden shadow-sm">
              <div className="px-4 py-3 border-b border-border/60 bg-muted/40 flex items-center justify-between font-mono text-xs text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Terminal className="w-3.5 h-3.5" />
                  <span>merit-execution-pipeline.json</span>
                </div>
                <span className="text-emerald-400">Endpoint Ready</span>
              </div>

              <div className="p-6 font-mono text-xs leading-relaxed space-y-4 overflow-x-auto">
                <div className="grid md:grid-cols-4 gap-4">
                  <div className="p-4 rounded-lg bg-muted/30 border border-border/40">
                    <div className="text-muted-foreground text-[10px] mb-1">01. TRANSPORT</div>
                    <div className="font-semibold text-foreground">FastAPI Router</div>
                    <div className="text-[11px] text-muted-foreground mt-2">Multipart payload check (&lt;5MB)</div>
                  </div>

                  <div className="p-4 rounded-lg bg-muted/30 border border-border/40">
                    <div className="text-muted-foreground text-[10px] mb-1">02. PARSING</div>
                    <div className="font-semibold text-foreground">ProcessPool Worker</div>
                    <div className="text-[11px] text-muted-foreground mt-2">pdfplumber / docx parsing</div>
                  </div>

                  <div className="p-4 rounded-lg bg-muted/30 border border-border/40">
                    <div className="text-muted-foreground text-[10px] mb-1">03. MATCHING</div>
                    <div className="font-semibold text-foreground">ATS Policy Matrix</div>
                    <div className="text-[11px] text-muted-foreground mt-2">TF-IDF & vector cosine scoring</div>
                  </div>

                  <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                    <div className="text-emerald-400 text-[10px] mb-1">04. VERIFIER</div>
                    <div className="font-semibold text-foreground">Dual-Pass Guard</div>
                    <div className="text-[11px] text-emerald-400 mt-2">Source quote verification</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Action Entry CTA */}
        <section className="py-16 container mx-auto px-6 max-w-5xl text-center">
          <h2 className="text-2xl font-bold tracking-tight mb-3">Ready to evaluate candidate alignment?</h2>
          <p className="text-xs md:text-sm text-muted-foreground max-w-lg mx-auto mb-8">
            Upload your candidate resume or launch our pre-filled senior engineering test case.
          </p>
          <Link href="/analyze">
            <Button size="lg" className="h-11 px-8 text-sm font-semibold focus-ring">
              Launch Analysis Workbench
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </Link>
        </section>
      </main>

      <footer className="border-t border-border/60 py-8 text-xs font-mono text-muted-foreground">
        <div className="container mx-auto px-6 max-w-5xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>Merit AI • Deterministic ATS Candidate Evaluation Engine</div>
          <div className="flex items-center gap-6">
            <a href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer" target="_blank" rel="noopener noreferrer" className="hover:text-foreground focus-ring">GitHub</a>
            <Link href="/analyze" className="hover:text-foreground focus-ring">Workbench</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

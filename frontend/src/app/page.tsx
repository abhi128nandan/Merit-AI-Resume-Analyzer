"use client";

import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck, Cpu, GitCommit, Lock, CheckCircle2, AlertCircle, FileText, Layers, Terminal } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function ProductOverviewPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground font-sans antialiased">
      {/* System Navigation */}
      <header className="px-6 h-14 flex items-center justify-between border-b border-border/60 bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 bg-foreground rounded-sm flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-background rounded-full" />
          </div>
          <span className="font-bold text-sm tracking-tight">Merit AI</span>
          <span className="text-xs font-mono px-2 py-0.5 rounded bg-muted text-muted-foreground border border-border/40">v1.0.0</span>
        </div>

        <nav className="flex items-center gap-6 text-xs font-mono text-muted-foreground">
          <a href="#system-architecture" className="hover:text-foreground transition-colors">Architecture</a>
          <a href="#matching-policy" className="hover:text-foreground transition-colors">Scoring Engine</a>
          <a href="#security" className="hover:text-foreground transition-colors">Security</a>
          <div className="w-px h-3 bg-border" />
          <Link href="/analyze">
            <Button size="sm" className="h-8 px-4 text-xs font-medium font-sans">
              Launch Workbench
              <ArrowRight className="ml-1.5 w-3.5 h-3.5" />
            </Button>
          </Link>
        </nav>
      </header>

      <main className="flex-1">
        {/* Core Product Proposition */}
        <section className="container mx-auto px-6 pt-20 pb-16 max-w-5xl">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-mono mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Deterministic Semantic ATS Engine • Zero-Hallucination Pipeline
            </div>

            <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-tight mb-6">
              Resume intelligence engineered for objective ATS evaluation.
            </h1>

            <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-8 max-w-2xl">
              Traditional ATS software relies on naive keyword matching. LLMs hallucinate skills. 
              Merit combines strict text extraction, deterministic policy weights, and verbatim quote verification to deliver explainable candidate-job alignment.
            </p>

            <div className="flex flex-wrap items-center gap-4">
              <Link href="/analyze">
                <Button size="lg" className="h-11 px-6 text-sm font-semibold group shadow-sm">
                  Launch Interactive Workspace
                  <ArrowRight className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <a href="#system-architecture">
                <Button variant="outline" size="lg" className="h-11 px-6 text-sm font-medium">
                  View Architecture & Schemas
                </Button>
              </a>
            </div>
          </div>
        </section>

        {/* Product Mechanics: Know, Feel, Do */}
        <section className="border-t border-b border-border/60 bg-muted/20 py-16">
          <div className="container mx-auto px-6 max-w-5xl">
            <div className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-3">System Operating Principles</div>
            <h2 className="text-2xl font-bold tracking-tight mb-12">Built on four verifiable engineering constraints</h2>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="p-6 rounded-xl border border-border/60 bg-card">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center mb-4">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <h3 className="text-base font-semibold mb-2">1. Dual-Pass Ground-Truth Verification</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Every extracted skill or degree must be cross-referenced against verbatim document strings. If a claim cannot be proven with a direct quote, it is dropped to prevent LLM hallucinations.
                </p>
              </div>

              <div className="p-6 rounded-xl border border-border/60 bg-card">
                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-500 flex items-center justify-center mb-4">
                  <Layers className="w-4 h-4" />
                </div>
                <h3 className="text-base font-semibold mb-2">2. Deterministic Scoring Policies</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  ATS Match scores are calculated using fixed mathematical policy weights (Hard Skills: 40%, Experience Relevancy: 30%, Tooling: 20%, Education: 10%) rather than unconstrained model predictions.
                </p>
              </div>

              <div className="p-6 rounded-xl border border-border/60 bg-card">
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-500 flex items-center justify-center mb-4">
                  <Cpu className="w-4 h-4" />
                </div>
                <h3 className="text-base font-semibold mb-2">3. Non-Blocking Concurrent Pipeline</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  CPU-bound PDF and DOCX extractions are offloaded to Python <code className="font-mono text-xs bg-muted px-1 py-0.5 rounded">ProcessPoolExecutor</code> threads via <code className="font-mono text-xs bg-muted px-1 py-0.5 rounded">asyncio.gather</code>, keeping the API event loop responsive.
                </p>
              </div>

              <div className="p-6 rounded-xl border border-border/60 bg-card">
                <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-500 flex items-center justify-center mb-4">
                  <Lock className="w-4 h-4" />
                </div>
                <h3 className="text-base font-semibold mb-2">4. Zero-Persistence Privacy Guard</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Uploaded files are validated using magic byte headers, processed in-memory or ephemeral isolated containers, and immediately purged post-analysis.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* System Architecture Overview */}
        <section id="system-architecture" className="py-20 container mx-auto px-6 max-w-5xl">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
            <div>
              <div className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-2">Clean Architecture</div>
              <h2 className="text-2xl font-bold tracking-tight">System Dataflow Architecture</h2>
            </div>
            <a 
              href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer/blob/main/docs/Architecture.md" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-xs font-mono text-muted-foreground hover:text-foreground mt-4 md:mt-0 flex items-center gap-1"
            >
              View complete specification on GitHub →
            </a>
          </div>

          {/* Clean Interactive Architecture Console */}
          <div className="rounded-xl border border-border/60 bg-card overflow-hidden shadow-sm">
            <div className="px-4 py-3 border-b border-border/60 bg-muted/40 flex items-center justify-between font-mono text-xs text-muted-foreground">
              <div className="flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5" />
                <span>merit-execution-pipeline.json</span>
              </div>
              <span className="text-emerald-500">Pipeline Active</span>
            </div>

            <div className="p-6 md:p-8 font-mono text-xs leading-relaxed space-y-6 overflow-x-auto">
              <div className="grid md:grid-cols-4 gap-4">
                <div className="p-4 rounded-lg bg-muted/40 border border-border/40">
                  <div className="text-muted-foreground mb-1">01. TRANSPORT</div>
                  <div className="font-semibold text-foreground">FastAPI Endpoint</div>
                  <div className="text-[11px] text-muted-foreground mt-2">Multipart upload + size check (&lt;5MB)</div>
                </div>

                <div className="p-4 rounded-lg bg-muted/40 border border-border/40">
                  <div className="text-muted-foreground mb-1">02. PARSING</div>
                  <div className="font-semibold text-foreground">ProcessPool Worker</div>
                  <div className="text-[11px] text-muted-foreground mt-2">pdfplumber / python-docx extraction</div>
                </div>

                <div className="p-4 rounded-lg bg-muted/40 border border-border/40">
                  <div className="text-muted-foreground mb-1">03. MATCHING</div>
                  <div className="font-semibold text-foreground">ATS Policy Engine</div>
                  <div className="text-[11px] text-muted-foreground mt-2">TF-IDF & vector cosine scoring</div>
                </div>

                <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                  <div className="text-emerald-500 mb-1">04. VERIFIER</div>
                  <div className="font-semibold text-foreground">Dual-Pass Guard</div>
                  <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-2">Quote verification against raw source</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Call to Action Workspace Entry */}
        <section className="border-t border-border/60 bg-muted/10 py-16">
          <div className="container mx-auto px-6 max-w-5xl text-center">
            <h2 className="text-2xl font-bold tracking-tight mb-3">Ready to inspect candidate alignment?</h2>
            <p className="text-sm text-muted-foreground max-w-lg mx-auto mb-8">
              Test the full matching pipeline using your own document or launch our pre-populated senior engineering test case.
            </p>
            <Link href="/analyze">
              <Button size="lg" className="h-11 px-8 text-sm font-semibold">
                Open Analysis Workspace
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-border/60 py-8 text-xs font-mono text-muted-foreground">
        <div className="container mx-auto px-6 max-w-5xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>Merit AI • Clean Architecture & ATS Verification Engine</div>
          <div className="flex items-center gap-6">
            <a href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer" target="_blank" rel="noopener noreferrer" className="hover:text-foreground">GitHub Repo</a>
            <a href="/analyze" className="hover:text-foreground">Workbench</a>
          </div>
        </div>
      </footer>
    </div>
  );
}


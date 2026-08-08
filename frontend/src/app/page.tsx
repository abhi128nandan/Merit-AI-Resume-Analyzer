"use client";

import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck, Zap, Server, Code2, Network, CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Premium Navbar */}
      <header className="px-6 h-16 flex items-center border-b border-border/40 backdrop-blur-md sticky top-0 z-50">
        <div className="font-bold text-xl tracking-tighter flex items-center gap-2">
          <div className="w-5 h-5 bg-foreground rounded-sm flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-background rounded-full" />
          </div>
          Merit
        </div>
        <nav className="ml-auto hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
          <a href="#how-it-works" className="hover:text-foreground transition-colors">How it works</a>
          <a href="#engineering" className="hover:text-foreground transition-colors">Engineering</a>
          <div className="w-px h-4 bg-border" />
          <Link href="/analyze">
            <Button size="sm" variant="secondary" className="font-semibold">
              Analyze Resume
            </Button>
          </Link>
        </nav>
      </header>

      <main className="flex-1 overflow-hidden">
        {/* Vercel-style Hero Section */}
        <section className="relative container mx-auto px-6 pt-32 pb-24 max-w-6xl">
          {/* Subtle Background Glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] bg-emerald-500/5 blur-[120px] -z-10 rounded-full" />
          
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            >
              <h1 className="text-5xl md:text-6xl font-bold tracking-tighter mb-6 text-balance leading-tight">
                Know if you match <br />
                <span className="text-muted-foreground">before you apply.</span>
              </h1>
              <p className="text-lg text-muted-foreground mb-8 max-w-md text-balance leading-relaxed">
                Stop guessing what ATS systems think. Merit analyzes your resume against any job description to reveal exactly what you're missing, increasing your interview rate.
              </p>
              
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                <Link href="/analyze">
                  <Button size="lg" className="h-12 px-8 text-base group shadow-lg shadow-foreground/5">
                    See ATS Report
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
                <p className="text-sm text-muted-foreground flex items-center gap-2 mt-2 sm:mt-0">
                  <ShieldCheck className="h-4 w-4" /> Secure & Private
                </p>
              </div>
            </motion.div>

            {/* Interactive Product Demonstration (Node Graph Simulation) */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="relative h-[400px] w-full rounded-2xl border border-border/50 bg-secondary/20 shadow-2xl overflow-hidden flex items-center justify-center p-8 backdrop-blur-sm"
            >
              {/* Simulated Semantic Mapping UI */}
              <div className="w-full max-w-md space-y-6">
                <div className="flex justify-between items-center text-xs font-mono text-muted-foreground mb-8">
                  <span>Resume.pdf</span>
                  <ArrowRight className="w-4 h-4 opacity-50" />
                  <span>Job_Description.txt</span>
                </div>

                <div className="space-y-4 relative">
                  {/* Connection Lines (SVGs) */}
                  <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: -1 }}>
                    <motion.path d="M 120 20 Q 200 20 280 60" fill="transparent" stroke="currentColor" className="text-emerald-500/30" strokeWidth="2" strokeDasharray="4 4" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }} />
                    <motion.path d="M 120 70 Q 200 70 280 110" fill="transparent" stroke="currentColor" className="text-emerald-500/30" strokeWidth="2" strokeDasharray="4 4" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, delay: 0.5, repeat: Infinity, ease: "linear" }} />
                    <motion.path d="M 120 120 Q 200 120 280 20" fill="transparent" stroke="currentColor" className="text-amber-500/30" strokeWidth="2" strokeDasharray="4 4" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, delay: 1, repeat: Infinity, ease: "linear" }} />
                  </svg>

                  {/* Nodes */}
                  <div className="flex justify-between items-center">
                    <div className="px-3 py-1.5 rounded-md bg-secondary border text-sm font-medium">React Developer</div>
                    <div className="px-3 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-sm font-medium flex items-center gap-2">
                      <CheckCircle2 className="w-3 h-3" /> Frontend Engineer
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="px-3 py-1.5 rounded-md bg-secondary border text-sm font-medium">Built REST APIs</div>
                    <div className="px-3 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-sm font-medium flex items-center gap-2">
                      <CheckCircle2 className="w-3 h-3" /> API Design Experience
                    </div>
                  </div>

                  <div className="flex justify-between items-center">
                    <div className="px-3 py-1.5 rounded-md bg-secondary border text-sm font-medium text-muted-foreground line-through">Java</div>
                    <div className="px-3 py-1.5 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 text-sm font-medium flex items-center gap-2">
                      <Zap className="w-3 h-3" /> Missing: Go/Golang
                    </div>
                  </div>
                </div>

                <div className="pt-8 border-t border-border/50 flex justify-between items-end">
                  <div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">ATS Match Score</div>
                    <div className="text-4xl font-bold tracking-tighter text-foreground">84<span className="text-xl text-muted-foreground">/100</span></div>
                  </div>
                  <div className="text-xs font-mono text-emerald-500 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                    Semantic Match Active
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Engineering Highlights (Replacing generic features) */}
        <section id="engineering" className="container mx-auto px-6 py-24 max-w-6xl border-t border-border/40">
          <div className="mb-16">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Engineering Transparency.</h2>
            <p className="text-muted-foreground max-w-2xl">
              We expose the raw data so you know exactly why you received your score. No black boxes.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="bg-background border-border/50 hover:border-border transition-colors">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-secondary flex items-center justify-center mb-4">
                  <Network className="h-5 w-5 text-foreground" />
                </div>
                <CardTitle className="text-lg">Semantic Matching</CardTitle>
                <CardDescription className="mt-2">
                  Traditional ATS systems look for exact keyword matches. Merit understands context. It knows that "Led a team" satisfies a "Management experience" requirement.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-background border-border/50 hover:border-border transition-colors">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-secondary flex items-center justify-center mb-4">
                  <Code2 className="h-5 w-5 text-foreground" />
                </div>
                <CardTitle className="text-lg">Evidence Extraction</CardTitle>
                <CardDescription className="mt-2">
                  Every match score is backed by direct quotes from your resume. If a skill is marked as matched, we show you exactly which bullet point proved it.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-background border-border/50 hover:border-border transition-colors">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-secondary flex items-center justify-center mb-4">
                  <Server className="h-5 w-5 text-foreground" />
                </div>
                <CardTitle className="text-lg">Hallucination Prevention</CardTitle>
                <CardDescription className="mt-2">
                  Our dual-pass validation architecture strictly prevents the system from inventing skills you don't possess, ensuring your score is objectively truthful.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>
      </main>

      <footer className="border-t border-border/40 py-12">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2 font-medium text-foreground">
            <div className="w-4 h-4 bg-foreground rounded-sm flex items-center justify-center">
              <div className="w-1.5 h-1.5 bg-background rounded-full" />
            </div>
            Merit
          </div>
          <p>© 2026 Merit AI Infrastructure. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

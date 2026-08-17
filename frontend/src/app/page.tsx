"use client";

import Link from "next/link";
import { 
  ArrowRight, 
  Upload, 
  Search, 
  Layers, 
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  History,
  Activity
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

import { useAuth } from "@/lib/auth-context";

export default function LandingPage() {
  const { user } = useAuth();
  const isAuthenticated = !!user;

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground font-sans antialiased selection:bg-emerald-500/20 selection:text-emerald-500">
      <main id="main-content" className="flex-1">
        
        {/* 2. Hero Section */}
        <section className="relative pt-20 pb-24 lg:pt-32 lg:pb-32 overflow-hidden">
          {/* Subtle background glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-emerald-500/5 rounded-full blur-[100px] pointer-events-none" />
          
          <div className="container mx-auto px-6 max-w-6xl relative z-10 grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
            
            <div className="max-w-2xl">
              <Badge variant="outline" className="mb-6 py-1 px-3 border-emerald-500/30 bg-emerald-500/10 text-emerald-400">
                <Sparkles className="w-3.5 h-3.5 mr-2" /> ATS Match Predictor
              </Badge>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1] mb-6">
                Know exactly why your resume didn&apos;t match the job.
              </h1>
              <p className="text-lg text-muted-foreground leading-relaxed mb-8 max-w-xl">
                Before a recruiter ever sees your application, an Applicant Tracking System scores it. Merit AI analyzes your resume against any job description, proving exactly what you&apos;re missing using verbatim quotes.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/analyze">
                  <Button size="lg" className="h-12 px-8 text-base font-semibold group shadow-sm bg-emerald-600 hover:bg-emerald-500 text-white w-full sm:w-auto">
                    Analyze my resume
                    <ArrowRight className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
                <a href="#how-it-works">
                  <Button variant="outline" size="lg" className="h-12 px-8 text-base font-medium w-full sm:w-auto">
                    See how it works
                  </Button>
                </a>
              </div>
            </div>

            {/* Visual Mockup */}
            <div className="relative mx-auto w-full max-w-md lg:max-w-full">
              <Card className="bg-card/80 backdrop-blur-sm border-border/60 shadow-xl overflow-hidden rounded-xl relative z-20 transform lg:rotate-[-2deg] transition-transform hover:rotate-0 duration-500">
                <div className="px-5 py-4 border-b border-border/40 bg-muted/30 flex justify-between items-center">
                  <div>
                    <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">Sample Analysis</div>
                    <div className="font-semibold text-sm">Senior Frontend Developer</div>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-black font-mono tracking-tight text-emerald-400">88<span className="text-sm text-muted-foreground">/100</span></div>
                  </div>
                </div>
                <div className="p-5 space-y-4">
                  <div className="p-3 bg-muted/40 rounded border border-border/40 text-sm">
                    <div className="flex items-start gap-3 mb-2">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-foreground">React &amp; TypeScript (5+ years)</p>
                        <Badge variant="success" className="mt-2 text-[10px] uppercase">Verified Quote</Badge>
                      </div>
                    </div>
                    <div className="pl-8 border-l-2 border-emerald-500/50 ml-2 mt-2">
                      <p className="text-xs font-mono text-muted-foreground italic">
                        &quot;Engineered scalable web applications using React and TypeScript for 6 years...&quot;
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
              {/* Decorative elements behind the card */}
              <div className="absolute -z-10 top-10 -right-4 w-full h-full border border-emerald-500/20 rounded-xl bg-emerald-500/5 lg:rotate-[4deg]" />
            </div>

          </div>
        </section>

        {/* 3. How It Works */}
        <section id="how-it-works" className="py-20 bg-muted/20 border-y border-border/60">
          <div className="container mx-auto px-6 max-w-5xl">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight mb-4">How Merit Works</h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">A transparent, 4-step process to bulletproof your resume.</p>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 relative">
              <div className="hidden lg:block absolute top-6 left-1/4 right-1/4 h-[1px] bg-gradient-to-r from-transparent via-border to-transparent" />
              
              <div className="flex flex-col items-center text-center relative z-10">
                <div className="w-12 h-12 rounded-full bg-card border border-border/60 flex items-center justify-center mb-4 shadow-sm text-foreground">
                  <Upload className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-lg mb-2">1. Upload Documents</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">Provide your resume (PDF/DOCX) and the exact Job Description you are targeting.</p>
              </div>

              <div className="flex flex-col items-center text-center relative z-10">
                <div className="w-12 h-12 rounded-full bg-card border border-border/60 flex items-center justify-center mb-4 shadow-sm text-indigo-400">
                  <Search className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-lg mb-2">2. Parse &amp; Extract</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">Our engine identifies every required skill, tool, and qualification from the job description.</p>
              </div>

              <div className="flex flex-col items-center text-center relative z-10">
                <div className="w-12 h-12 rounded-full bg-card border border-border/60 flex items-center justify-center mb-4 shadow-sm text-amber-400">
                  <Layers className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-lg mb-2">3. Match &amp; Score</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">We calculate an ATS compatibility score based on strict weighting (Skills, Experience, Education).</p>
              </div>

              <div className="flex flex-col items-center text-center relative z-10">
                <div className="w-12 h-12 rounded-full bg-card border border-border/60 flex items-center justify-center mb-4 shadow-sm text-emerald-400">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-lg mb-2">4. Get Evidence</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">See exactly where your resume proves a match, and where critical keywords are missing.</p>
              </div>
            </div>
          </div>
        </section>

        {/* 4. Why it's different / Trust */}
        <section id="why-merit" className="py-24 container mx-auto px-6 max-w-5xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Built for Truth, Not Hallucinations</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">Standard AI tools invent skills you don&apos;t have to make your resume look better. We don&apos;t.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <Card className="p-8 bg-card border-border/60 rounded-2xl flex flex-col items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">Only Verbatim Evidence</h3>
                <p className="text-muted-foreground leading-relaxed">
                  If the system claims you have a skill, it must prove it by highlighting the exact quote from your resume. No more guessing if the ATS actually recognized your bullet points.
                </p>
              </div>
            </Card>
            
            <Card className="p-8 bg-card border-border/60 rounded-2xl flex flex-col items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                <Activity className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">No Fabricated Skills</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Our Dual-Pass Verification drops any claims that can&apos;t be sourced directly from your document. You get a harsh, but accurate, reality check.
                </p>
              </div>
            </Card>
          </div>
        </section>

        {/* 5. History Teaser */}
        <section className="py-20 bg-emerald-950/20 border-y border-emerald-900/30">
          <div className="container mx-auto px-6 max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 mb-6">
              <History className="w-6 h-6" />
            </div>
            <h2 className="text-3xl font-bold tracking-tight mb-4 text-emerald-50">Track Your Progress</h2>
            <p className="text-emerald-200/70 max-w-xl mx-auto mb-8 text-lg leading-relaxed">
              Sign up to save your past analyses. Compare scores across different job applications and watch your ATS compatibility improve as you refine your resume over time.
            </p>
            <Link href={isAuthenticated ? "/history" : "/analyze"}>
              <Button size="lg" variant="outline" className="h-12 px-8 text-base border-emerald-500/30 hover:bg-emerald-500/10 hover:text-emerald-400">
                {isAuthenticated ? "View my history" : "Create an account"}
              </Button>
            </Link>
          </div>
        </section>

        {/* 6. Social Proof / Stats (Placeholder) */}
        <section className="py-16 container mx-auto px-6 max-w-5xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 divide-x divide-border/40 text-center">
            <div className="px-4">
              <div className="text-3xl md:text-4xl font-black font-mono text-foreground mb-2">10,000+</div>
              <div className="text-sm text-muted-foreground">Resumes Analyzed<br/>(Placeholder)</div>
            </div>
            <div className="px-4">
              <div className="text-3xl md:text-4xl font-black font-mono text-emerald-400 mb-2">24%</div>
              <div className="text-sm text-muted-foreground">Avg. Score Increase<br/>(Placeholder)</div>
            </div>
            <div className="px-4">
              <div className="text-3xl md:text-4xl font-black font-mono text-foreground mb-2">99.9%</div>
              <div className="text-sm text-muted-foreground">Verification Accuracy<br/>(Placeholder)</div>
            </div>
            <div className="px-4">
              <div className="text-3xl md:text-4xl font-black font-mono text-foreground mb-2">&lt; 5s</div>
              <div className="text-sm text-muted-foreground">Analysis Latency<br/>(Placeholder)</div>
            </div>
          </div>
        </section>

        {/* 7. Final CTA */}
        <section className="py-24 text-center container mx-auto px-6">
          <h2 className="text-3xl font-bold tracking-tight mb-6">Stop guessing what the ATS wants.</h2>
          <Link href="/analyze">
            <Button size="lg" className="h-14 px-10 text-lg font-semibold bg-emerald-600 hover:bg-emerald-500 text-white focus-ring">
              Analyze my resume for free
            </Button>
          </Link>
        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-border/60 bg-muted/10 py-12 text-sm text-muted-foreground">
        <div className="container mx-auto px-6 max-w-6xl grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4 text-foreground">
              <div className="w-5 h-5 bg-emerald-500 rounded-sm flex items-center justify-center">
                <div className="w-1.5 h-1.5 bg-background rounded-full" />
              </div>
              <span className="font-bold tracking-tight">Merit AI</span>
            </div>
            <p className="mb-4">Deterministic ATS Candidate Matching Engine.</p>
            <p className="text-xs">&copy; {new Date().getFullYear()} Merit AI. All rights reserved.</p>
          </div>
          
          <div>
            <h4 className="font-semibold text-foreground mb-4">Product</h4>
            <ul className="space-y-2">
              <li><Link href="/analyze" className="hover:text-foreground transition-colors">Workbench</Link></li>
              <li><Link href="#how-it-works" className="hover:text-foreground transition-colors">How it works</Link></li>
              <li><Link href="/history" className="hover:text-foreground transition-colors">History</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-4">Developers</h4>
            <ul className="space-y-2">
              <li><a href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">GitHub Repository</a></li>
              <li><a href="https://github.com/abhi128nandan/Merit-AI-Resume-Analyzer/blob/main/docs/Architecture.md" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">Architecture Docs</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-4">Connect</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-foreground transition-colors">Contact Support</a></li>
              <li><a href="#" className="hover:text-foreground transition-colors">Twitter / X</a></li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
}

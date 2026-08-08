"use client";

import { motion } from "framer-motion";
import { CheckCircle2, AlertTriangle, Info, ChevronRight, Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function ResultsPage() {
  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Pane 1: Navigation & Summary (25%) */}
      <aside className="w-1/4 border-r bg-muted/20 flex flex-col h-full">
        <div className="p-4 border-b flex items-center justify-between sticky top-0 bg-background/95 backdrop-blur z-10">
          <div className="font-bold text-lg flex items-center gap-2">
            <div className="w-5 h-5 bg-primary rounded-sm flex items-center justify-center">
              <div className="w-1.5 h-1.5 bg-white rounded-full" />
            </div>
            Merit
          </div>
          <Button variant="ghost" size="sm">Export Report</Button>
        </div>
        
        <div className="p-4 flex-1 overflow-y-auto">
          {/* Main Score */}
          <div className="text-center py-6 mb-6">
            <div className="relative inline-flex items-center justify-center">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-muted" />
                <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" strokeDasharray="377" strokeDashoffset={377 - (377 * 82) / 100} className="text-emerald-500" />
              </svg>
              <div className="absolute flex flex-col items-center justify-center">
                <span className="text-4xl font-bold">82</span>
                <span className="text-xs text-muted-foreground uppercase tracking-wider">Score</span>
              </div>
            </div>
            <h2 className="text-lg font-semibold mt-4">Strong Match</h2>
            <p className="text-sm text-muted-foreground">Top 15% of candidates</p>
          </div>

          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-2">Key Insights</h3>
            <div className="flex items-center justify-between p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-sm text-emerald-700 dark:text-emerald-400">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Format ATS parsing</span>
              </div>
              <span className="font-mono font-medium">100%</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-sm text-amber-700 dark:text-amber-400">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                <span>Missing exact keywords</span>
              </div>
              <span className="font-mono font-medium">3</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Pane 2: Source Document (35%) */}
      <section className="w-[35%] border-r bg-muted/10 flex flex-col h-full relative">
        <div className="p-4 border-b flex items-center justify-between sticky top-0 bg-background/95 backdrop-blur z-10">
          <h2 className="text-sm font-semibold flex items-center gap-2">
            Source Resume
          </h2>
          <Badge variant="outline" className="font-mono text-xs">PDF</Badge>
        </div>
        <div className="flex-1 p-6 overflow-y-auto">
          {/* Mock Document Render */}
          <Card className="shadow-lg min-h-[800px] border-none rounded-sm bg-white text-zinc-900 p-8 space-y-6">
            <div className="border-b-2 border-zinc-200 pb-4">
              <h1 className="text-3xl font-bold tracking-tight">John Doe</h1>
              <p className="text-zinc-600">john.doe@example.com • (555) 123-4567 • San Francisco, CA</p>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-zinc-800 uppercase tracking-wide border-b border-zinc-200 mb-2">Experience</h2>
              <div className="mb-4">
                <div className="flex justify-between items-baseline mb-1">
                  <h3 className="font-bold text-zinc-900">Senior Backend Engineer</h3>
                  <span className="text-sm text-zinc-500">2021 - Present</span>
                </div>
                <p className="text-sm text-zinc-600 mb-2">TechFlow Inc.</p>
                <ul className="list-disc list-outside ml-4 text-sm space-y-1">
                  <li className="bg-amber-100 rounded px-1 transition-colors">Designed and implemented scalable microservices using <span className="font-semibold text-amber-700">Python, FastAPI, and PostgreSQL</span>.</li>
                  <li>Improved API response times by 40% through aggressive query optimization and Redis caching.</li>
                  <li className="bg-emerald-100 rounded px-1 transition-colors">Led a team of 4 engineers in migrating legacy monolithic architecture to AWS EKS.</li>
                </ul>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Pane 3: Analysis Engine (40%) */}
      <main className="flex-1 flex flex-col h-full bg-background relative">
        <div className="p-4 border-b flex items-center gap-4 sticky top-0 bg-background/95 backdrop-blur z-10">
          <h2 className="text-sm font-semibold flex items-center gap-2">
            Analysis Engine Output
          </h2>
          <div className="flex gap-2">
            <Badge variant="success">Experience Match</Badge>
            <Badge variant="warning">Skills Gap</Badge>
          </div>
        </div>
        
        <div className="flex-1 p-6 overflow-y-auto space-y-8">
          
          <section>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Hard Skills Match</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="font-medium">Python / FastAPI</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-mono">Present</span>
                </div>
                <Progress value={100} className="h-2" />
                <p className="text-xs text-muted-foreground mt-1.5 flex items-center gap-1">
                  <Check className="w-3 h-3 text-emerald-500" /> Found in Experience section (TechFlow Inc.)
                </p>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="font-medium">AWS / Kubernetes</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-mono">Present</span>
                </div>
                <Progress value={100} className="h-2" />
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="font-medium">GraphQL</span>
                  <span className="text-destructive font-mono">Missing</span>
                </div>
                <Progress value={0} className="h-2 [&>div]:bg-destructive" />
                <p className="text-xs text-muted-foreground mt-1.5 flex items-center gap-1 text-destructive">
                  <AlertTriangle className="w-3 h-3" /> Critical requirement not found in resume
                </p>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">ATS Parsing Diagnostics</h3>
            <Card className="bg-muted/30 border-none shadow-none">
              <CardContent className="p-0 text-sm">
                <div className="divide-y divide-border/50">
                  <div className="flex items-center justify-between py-3 px-4">
                    <span className="text-muted-foreground">Format</span>
                    <Badge variant="success" className="font-mono">PASS</Badge>
                  </div>
                  <div className="flex items-center justify-between py-3 px-4">
                    <span className="text-muted-foreground">Section Headers</span>
                    <Badge variant="success" className="font-mono">PASS</Badge>
                  </div>
                  <div className="flex items-center justify-between py-3 px-4">
                    <span className="text-muted-foreground">Keyword Density</span>
                    <Badge variant="warning" className="font-mono">MODERATE</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>
          
        </div>
      </main>
    </div>
  );
}

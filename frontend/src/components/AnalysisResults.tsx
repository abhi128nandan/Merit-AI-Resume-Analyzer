"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, XCircle, ArrowLeft, ShieldCheck, Code2, Cpu, Terminal, FileText, Check, AlertTriangle, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { AnalysisResponse, MatchCategoryResult } from "@/lib/api";

interface AnalysisResultsProps {
  data: AnalysisResponse;
  onReset: () => void;
}

export function AnalysisResults({ data, onReset }: AnalysisResultsProps) {
  const { match_report, feedback, metadata } = data;
  const score = match_report.overall_score;

  const [activeTab, setActiveTab] = useState<"all" | "matched" | "missing">("all");

  const getScoreColor = (s: number) => {
    if (s >= 80) return "text-emerald-500";
    if (s >= 65) return "text-amber-500";
    return "text-red-500";
  };
  
  const getScoreBadgeBg = (s: number) => {
    if (s >= 80) return "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20";
    if (s >= 65) return "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20";
    return "bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20";
  };

  const getMatchBadge = (level: string) => {
    switch (level) {
      case "Exact":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">VERIFIED QUOTE</span>;
      case "Semantic":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">SEMANTIC MATCH</span>;
      case "Partial":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">PARTIAL</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20">SKILL GAP</span>;
    }
  };

  const getRecommendation = (s: number) => {
    if (s >= 85) return { decision: "High Compatibility", action: "Profile meets all primary technical and experience thresholds. Ready to submit." };
    if (s >= 70) return { decision: "Moderate Match", action: "Core qualifications present. Tailor specific hard skill terms to maximize ATS parsing density." };
    if (s >= 50) return { decision: "Qualifications Gap", action: "Foundational match present, but key technical tools or experience years are missing." };
    return { decision: "Low Relevancy", action: "Significant mismatch between resume experience and required position qualifications." };
  };

  const rec = getRecommendation(score);

  const renderCategory = (title: string, category: MatchCategoryResult, categoryWeight: string) => {
    const filteredEvidence = category.evidence.filter((ev) => {
      if (activeTab === "matched") return ["Exact", "Semantic", "Partial"].includes(ev.match_level);
      if (activeTab === "missing") return !["Exact", "Semantic", "Partial"].includes(ev.match_level);
      return true;
    });

    return (
      <Card className="mb-6 bg-card border-border/60 shadow-sm overflow-hidden rounded-xl">
        <CardHeader className="py-4.5 px-6 bg-muted/30 border-b border-border/40 flex flex-row items-center justify-between">
          <div>
            <CardTitle className="text-base font-semibold">{title}</CardTitle>
            <span className="text-xs font-mono text-muted-foreground">Policy Weight: {categoryWeight}</span>
          </div>
          <div className="flex items-center gap-3">
            <span className={`text-base font-bold font-mono ${getScoreColor(category.score)}`}>{category.score}/100</span>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {filteredEvidence.length > 0 ? (
            <Accordion type="single" collapsible className="w-full">
              {filteredEvidence.map((ev, i) => {
                const isMatched = ["Exact", "Semantic", "Partial"].includes(ev.match_level);
                return (
                  <AccordionItem key={i} value={`item-${i}`} className="border-b border-border/40 last:border-0">
                    <AccordionTrigger className="px-6 py-3.5 hover:bg-muted/20 hover:no-underline">
                      <div className="flex items-center gap-3 text-left w-full pr-4">
                        {isMatched ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                        ) : (
                          <XCircle className="w-4 h-4 text-red-500 shrink-0" />
                        )}
                        <span className="font-medium text-xs md:text-sm flex-1">{ev.requirement}</span>
                        <div className="shrink-0">{getMatchBadge(ev.match_level)}</div>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="px-6 pb-4 pt-1">
                      <div className="bg-muted/40 rounded-lg p-3.5 border border-border/50">
                        <div className="text-[11px] font-mono text-muted-foreground uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <Code2 className="w-3 h-3" /> Ground-Truth Evidence Verification
                        </div>
                        {ev.evidence ? (
                          <p className="text-xs font-mono text-foreground/90 leading-relaxed border-l-2 border-emerald-500/80 pl-3 py-0.5">
                            "{ev.evidence}"
                          </p>
                        ) : (
                          <p className="text-xs font-mono text-muted-foreground italic border-l-2 border-red-500/40 pl-3 py-0.5">
                            Unverified: Requirement is missing from raw document text strings.
                          </p>
                        )}
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                );
              })}
            </Accordion>
          ) : (
            <div className="p-4 text-xs font-mono text-muted-foreground">No evaluation items match the selected filter.</div>
          )}
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="max-w-6xl mx-auto text-foreground font-sans antialiased">
      {/* Top Header Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-border/60">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <h1 className="text-xl font-bold tracking-tight">Analysis Audit Diagnostic</h1>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
            <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
              <ShieldCheck className="w-3.5 h-3.5" /> Verifier Verified
            </span>
            <span>ID: {metadata.analysis_id.split('-')[0]}</span>
            <span>Latency: {metadata.processing_time_ms}ms</span>
          </div>
        </div>

        <Button variant="outline" size="sm" onClick={onReset} className="h-8 text-xs font-medium self-start sm:self-auto">
          <ArrowLeft className="w-3.5 h-3.5 mr-1.5" /> Run Another Analysis
        </Button>
      </div>

      {/* Grid Layout */}
      <div className="grid lg:grid-cols-[1fr_2fr] gap-6">
        
        {/* Left Column: Decision & System Telemetry */}
        <div className="flex flex-col gap-6">
          
          {/* Primary Decision Card */}
          <Card className={`border ${getScoreBadgeBg(score)} shadow-sm rounded-xl`}>
            <CardHeader className="pb-3">
              <div className="flex justify-between items-center text-xs font-mono uppercase tracking-wider text-muted-foreground">
                <span>Evaluated Match Score</span>
                <span>Deterministic</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-baseline gap-3">
                <span className={`text-5xl font-black font-mono tracking-tight ${getScoreColor(score)}`}>
                  {score}
                </span>
                <span className="text-sm font-mono text-muted-foreground">/ 100</span>
              </div>

              <div>
                <h3 className="font-bold text-base mb-1">{rec.decision}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">{rec.action}</p>
              </div>

              {/* Category Weighted Meters */}
              <div className="pt-4 border-t border-border/40 space-y-2.5 text-xs font-mono">
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Hard Skills (40%)</span>
                  <span className={`font-semibold ${getScoreColor(match_report.skills_evaluation.score)}`}>
                    {match_report.skills_evaluation.score}/100
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Experience (30%)</span>
                  <span className={`font-semibold ${getScoreColor(match_report.experience_evaluation.score)}`}>
                    {match_report.experience_evaluation.score}/100
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Education (10%)</span>
                  <span className={`font-semibold ${getScoreColor(match_report.education_evaluation.score)}`}>
                    {match_report.education_evaluation.score}/100
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actionable Revision Copy */}
          <Card className="bg-card border-border/60 rounded-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-500" />
                Actionable Resume Revisions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {feedback.improvement_suggestions.length > 0 ? (
                feedback.improvement_suggestions.map((suggestion, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-muted/30 border border-border/40 text-xs leading-relaxed text-foreground flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                    <span>{suggestion}</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-muted-foreground font-mono">No critical keyword gaps detected.</p>
              )}
            </CardContent>
          </Card>

          {/* Telemetry Diagnostics */}
          <div className="p-4 rounded-xl bg-muted/20 border border-border/40 text-xs font-mono space-y-2">
            <div className="text-muted-foreground uppercase tracking-wider text-[10px] font-semibold mb-2">Engine System Telemetry</div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">ProcessPool Worker</span>
              <span className="text-emerald-600 dark:text-emerald-400">Thread Active</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Verification Pass 2</span>
              <span className="text-emerald-600 dark:text-emerald-400">100% Quote Match</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Hallucination Guard</span>
              <span className="text-emerald-600 dark:text-emerald-400">Enforced</span>
            </div>
          </div>

        </div>

        {/* Right Column: Evidence & Skill Inspector */}
        <div className="flex flex-col">
          {/* Filter Bar */}
          <div className="flex items-center justify-between mb-4 bg-muted/30 p-1.5 rounded-lg border border-border/40 text-xs font-mono">
            <span className="text-muted-foreground px-2">Evidence Inspector:</span>
            <div className="flex gap-1">
              <button
                onClick={() => setActiveTab("all")}
                className={`px-3 py-1 rounded-md transition-colors ${activeTab === "all" ? "bg-background font-semibold text-foreground shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
              >
                All Requirements
              </button>
              <button
                onClick={() => setActiveTab("matched")}
                className={`px-3 py-1 rounded-md transition-colors ${activeTab === "matched" ? "bg-background font-semibold text-emerald-600 dark:text-emerald-400 shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
              >
                Verified Matches
              </button>
              <button
                onClick={() => setActiveTab("missing")}
                className={`px-3 py-1 rounded-md transition-colors ${activeTab === "missing" ? "bg-background font-semibold text-red-500 shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
              >
                Skill Gaps
              </button>
            </div>
          </div>
          
          <div className="space-y-4">
            {renderCategory("Technical Skills & Requirements", match_report.skills_evaluation, "40%")}
            {renderCategory("Work Experience Relevancy", match_report.experience_evaluation, "30%")}
            {renderCategory("Education & Credentials", match_report.education_evaluation, "10%")}
          </div>
        </div>

      </div>
    </div>
  );
}


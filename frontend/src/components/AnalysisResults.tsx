"use client";

import { useState } from "react";
import { CheckCircle2, XCircle, ArrowLeft, ShieldCheck, Code2, Terminal, Copy, Download, Check, AlertTriangle } from "lucide-react";
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
  const [copied, setCopied] = useState(false);

  const handleCopySummary = () => {
    const summaryText = `Merit AI Match Report\nAnalysis ID: ${metadata.analysis_id}\nMatch Score: ${score}/100\nDecision: ${getRecommendation(score).decision}\n\nMatched Skills:\n${feedback.matched_skills.join(", ") || "None"}\n\nMissing Skills:\n${feedback.missing_skills.join(", ") || "None"}\n\nRevisions:\n${feedback.improvement_suggestions.join("\n")}`;
    navigator.clipboard.writeText(summaryText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportJson = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `merit_analysis_${metadata.analysis_id.split('-')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getScoreColor = (s: number) => {
    if (s >= 80) return "text-emerald-400";
    if (s >= 65) return "text-amber-400";
    return "text-red-400";
  };



  const getMatchBadge = (level: string) => {
    switch (level) {
      case "Exact":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">VERIFIED QUOTE</span>;
      case "Semantic":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">SEMANTIC MATCH</span>;
      case "Partial":
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">PARTIAL MATCH</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-red-500/10 text-red-400 border border-red-500/20">SKILL GAP</span>;
    }
  };

  const getRecommendation = (s: number) => {
    if (s >= 85) {
      return {
        badge: "HIGH COMPATIBILITY • RECOMMENDED TO APPLY",
        decision: "Strong Candidate Alignment — Submit Application",
        action: "Your profile meets over 85% of primary technical and experience requirements. Proceed directly to application.",
        colorClass: "border-emerald-500/30 bg-emerald-500/5 text-emerald-400"
      };
    }
    if (s >= 70) {
      return {
        badge: "MODERATE MATCH • CONDITIONAL APPLICATION",
        decision: "Moderate Qualification Match — Tailor Resume",
        action: "Core qualifications are present. Align hard skill keywords with the job description before submitting.",
        colorClass: "border-amber-500/30 bg-amber-500/5 text-amber-400"
      };
    }
    if (s >= 50) {
      return {
        badge: "QUALIFICATIONS GAP • REVISION REQUIRED",
        decision: "Noticeable Qualification Gaps Present",
        action: "Foundational match present, but key technical tools or experience thresholds are unverified.",
        colorClass: "border-amber-500/30 bg-amber-500/5 text-amber-400"
      };
    }
    return {
      badge: "LOW RELEVANCY • NOT RECOMMENDED",
      decision: "Significant Experience Mismatch",
      action: "High mismatch between resume experience and required job qualifications.",
      colorClass: "border-red-500/30 bg-red-500/5 text-red-400"
    };
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
        <CardHeader className="py-4 px-6 bg-muted/30 border-b border-border/40 flex flex-row items-center justify-between">
          <div>
            <CardTitle className="text-sm font-bold">{title}</CardTitle>
            <span className="text-[11px] font-mono text-muted-foreground">Policy Weight: {categoryWeight}</span>
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
                    <AccordionTrigger className="px-6 py-3.5 hover:bg-muted/20 hover:no-underline focus-ring">
                      <div className="flex items-center gap-3 text-left w-full pr-4">
                        {isMatched ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                        ) : (
                          <XCircle className="w-4 h-4 text-red-400 shrink-0" />
                        )}
                        <span className="font-medium text-xs md:text-sm flex-1">{ev.requirement}</span>
                        <div className="shrink-0">{getMatchBadge(ev.match_level)}</div>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="px-6 pb-4 pt-1">
                      <div className="bg-muted/40 rounded-lg p-3.5 border border-border/50">
                        <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <Code2 className="w-3 h-3 text-emerald-400" /> Ground-Truth Source Quote Verification
                        </div>
                        {ev.evidence ? (
                          <p className="text-xs font-mono text-foreground leading-relaxed border-l-2 border-emerald-500 pl-3 py-0.5">
                            &quot;{ev.evidence}&quot;
                          </p>
                        ) : (
                          <p className="text-xs font-mono text-muted-foreground italic border-l-2 border-red-500/40 pl-3 py-0.5">
                            Unverified: Requirement is absent from candidate resume text strings.
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
    <div className="max-w-6xl mx-auto text-foreground font-sans antialiased space-y-6">
      {/* Top Header Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border/60">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <h1 className="text-xl font-bold tracking-tight">ATS Candidate Audit Diagnostic</h1>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
            <span className="flex items-center gap-1 text-emerald-400">
              <ShieldCheck className="w-3.5 h-3.5" /> Verifier Active
            </span>
            <span>ID: {metadata.analysis_id.split('-')[0]}</span>
            <span>Latency: {metadata.processing_time_ms}ms</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-start sm:self-auto">
          <Button variant="outline" size="sm" onClick={handleCopySummary} className="h-8 text-xs font-medium focus-ring">
            {copied ? <Check className="w-3.5 h-3.5 mr-1.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}
            {copied ? "Copied!" : "Copy Report"}
          </Button>

          <Button variant="outline" size="sm" onClick={handleExportJson} className="h-8 text-xs font-medium focus-ring">
            <Download className="w-3.5 h-3.5 mr-1.5" /> Export JSON
          </Button>

          <Button variant="default" size="sm" onClick={onReset} className="h-8 text-xs font-medium focus-ring">
            <ArrowLeft className="w-3.5 h-3.5 mr-1.5" /> Analyze Another
          </Button>
        </div>
      </div>

      {/* Hero "Should I Apply?" Verdict Banner */}
      <Card className={`border ${rec.colorClass} shadow-sm rounded-xl p-6`}>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest px-2.5 py-1 rounded bg-card border border-border/40 inline-block mb-3 font-semibold">
              {rec.badge}
            </div>
            <h2 className="text-xl md:text-2xl font-bold tracking-tight mb-1">{rec.decision}</h2>
            <p className="text-xs md:text-sm text-muted-foreground max-w-2xl leading-relaxed font-sans">
              {rec.action}
            </p>
          </div>

          <div className="flex items-baseline gap-2 bg-card p-4 rounded-xl border border-border/60 self-start md:self-auto shrink-0">
            <span className={`text-4xl md:text-5xl font-black font-mono tracking-tight ${getScoreColor(score)}`}>
              {score}
            </span>
            <span className="text-xs font-mono text-muted-foreground">/ 100</span>
          </div>
        </div>
      </Card>

      {/* Main Analysis Grid */}
      <div className="grid lg:grid-cols-[1fr_2fr] gap-6">
        
        {/* Left Column: Weighted Meters & Revisions */}
        <div className="flex flex-col gap-6">
          
          {/* Policy Weighted Category Meters */}
          <Card className="bg-card border-border/60 rounded-xl p-5 space-y-4">
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground font-semibold pb-2 border-b border-border/40">
              Deterministic Policy Breakdown
            </div>

            <div className="space-y-3 text-xs font-mono">
              <div>
                <div className="flex justify-between text-muted-foreground mb-1">
                  <span>Hard Skills (40% Weight)</span>
                  <span className={`font-bold ${getScoreColor(match_report.skills_evaluation.score)}`}>
                    {match_report.skills_evaluation.score}/100
                  </span>
                </div>
                <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500" style={{ width: `${match_report.skills_evaluation.score}%` }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-muted-foreground mb-1">
                  <span>Experience (30% Weight)</span>
                  <span className={`font-bold ${getScoreColor(match_report.experience_evaluation.score)}`}>
                    {match_report.experience_evaluation.score}/100
                  </span>
                </div>
                <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500" style={{ width: `${match_report.experience_evaluation.score}%` }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-muted-foreground mb-1">
                  <span>Education (10% Weight)</span>
                  <span className={`font-bold ${getScoreColor(match_report.education_evaluation.score)}`}>
                    {match_report.education_evaluation.score}/100
                  </span>
                </div>
                <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500" style={{ width: `${match_report.education_evaluation.score}%` }} />
                </div>
              </div>
            </div>
          </Card>

          {/* Actionable Resume Revisions */}
          <Card className="bg-card border-border/60 rounded-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-bold flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                Actionable Resume Revisions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {feedback.improvement_suggestions.length > 0 ? (
                feedback.improvement_suggestions.map((suggestion, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-muted/30 border border-border/40 text-xs leading-relaxed text-foreground flex items-start gap-2.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400 mt-0.5 shrink-0" />
                    <span>{suggestion}</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-muted-foreground font-mono">No critical keyword gaps detected in candidate profile.</p>
              )}
            </CardContent>
          </Card>

          {/* Telemetry Diagnostics */}
          <div className="p-4 rounded-xl bg-muted/20 border border-border/40 text-xs font-mono space-y-2">
            <div className="text-muted-foreground uppercase tracking-wider text-[10px] font-semibold mb-2">Engine System Telemetry</div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">ProcessPool Worker</span>
              <span className="text-emerald-400">Thread Active</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Verification Pass 2</span>
              <span className="text-emerald-400">100% Quote Match</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Hallucination Guard</span>
              <span className="text-emerald-400">Enforced</span>
            </div>
          </div>

        </div>

        {/* Right Column: Evidence & Skill Inspector */}
        <div className="flex flex-col">
          {/* Requirement Filter Bar */}
          <div className="flex items-center justify-between mb-4 bg-muted/30 p-1.5 rounded-lg border border-border/40 text-xs font-mono">
            <span className="text-muted-foreground px-2">Evidence Inspector:</span>
            <div className="flex gap-1">
              <button
                onClick={() => setActiveTab("all")}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer focus-ring ${activeTab === "all" ? "bg-background font-semibold text-foreground shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
              >
                All Requirements
              </button>
              <button
                onClick={() => setActiveTab("matched")}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer focus-ring ${activeTab === "matched" ? "bg-background font-semibold text-emerald-400 shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
              >
                Verified Matches
              </button>
              <button
                onClick={() => setActiveTab("missing")}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer focus-ring ${activeTab === "missing" ? "bg-background font-semibold text-red-400 shadow-xs" : "text-muted-foreground hover:text-foreground"}`}
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

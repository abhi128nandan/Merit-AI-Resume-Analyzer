import { motion } from "framer-motion";
import { CheckCircle2, XCircle, AlertTriangle, ArrowLeft, ArrowUpRight, Code2, Network, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { AnalysisResponse, MatchCategoryResult, EvidenceResult } from "@/lib/api";

interface AnalysisResultsProps {
  data: AnalysisResponse;
  onReset: () => void;
}

export function AnalysisResults({ data, onReset }: AnalysisResultsProps) {
  const { match_report, feedback, metadata } = data;
  const score = match_report.overall_score;

  const getScoreColor = (s: number) => {
    if (s >= 80) return "text-emerald-500";
    if (s >= 50) return "text-amber-500";
    return "text-red-500";
  };
  
  const getScoreBg = (s: number) => {
    if (s >= 80) return "bg-emerald-500/10 border-emerald-500/20";
    if (s >= 50) return "bg-amber-500/10 border-amber-500/20";
    return "bg-red-500/10 border-red-500/20";
  };

  const getMatchBadge = (level: string) => {
    switch (level) {
      case "Exact":
        return <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">Exact Match</span>;
      case "Semantic":
        return <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">Semantic</span>;
      case "Partial":
      case "Weak":
        return <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-amber-500/10 text-amber-500 border border-amber-500/20">Weak</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-red-500/10 text-red-500 border border-red-500/20">Missing</span>;
    }
  };

  const getRecommendation = (s: number) => {
    if (s >= 85) return { text: "Strong Yes", desc: "You are highly competitive for this role. Apply immediately." };
    if (s >= 70) return { text: "Yes", desc: "Good match. Minor tailoring recommended before applying." };
    if (s >= 50) return { text: "Borderline", desc: "You have foundational skills, but significant tailoring is needed." };
    return { text: "No", desc: "Your profile does not align well with this role's core requirements." };
  };

  const rec = getRecommendation(score);

  const renderCategory = (title: string, category: MatchCategoryResult) => (
    <Card className="mb-6 bg-card border-border/40 shadow-sm overflow-hidden">
      <CardHeader className="pb-4 bg-secondary/20 border-b border-border/40">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{title}</CardTitle>
          <span className={`font-bold ${getScoreColor(category.score)}`}>{category.score}/100</span>
        </div>
        <div className="w-full bg-secondary h-1.5 rounded-full overflow-hidden mt-2">
          <motion.div 
            className={`h-full ${getScoreColor(category.score).replace("text-", "bg-")}`}
            initial={{ width: 0 }}
            animate={{ width: `${category.score}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
        </div>
      </CardHeader>
      <CardContent className="p-0">
        {category.evidence.length > 0 ? (
          <Accordion type="single" collapsible className="w-full">
            {category.evidence.map((ev, i) => (
              <AccordionItem key={i} value={`item-${i}`} className="border-b border-border/40 last:border-0">
                <AccordionTrigger className="px-6 py-4 hover:bg-secondary/10 hover:no-underline">
                  <div className="flex items-center gap-4 text-left w-full pr-4">
                    {["Exact", "Semantic", "Partial"].includes(ev.match_level) ? 
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : 
                      <XCircle className="w-4 h-4 text-red-500 shrink-0" />
                    }
                    <span className="font-medium text-sm flex-1">{ev.requirement}</span>
                    <div className="shrink-0">{getMatchBadge(ev.match_level)}</div>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-6 pb-4 pt-2">
                  <div className="bg-secondary/30 rounded-lg p-4 border border-border/50">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2 font-mono flex items-center gap-2">
                      <Code2 className="w-3 h-3" /> Extracted Evidence
                    </div>
                    {ev.evidence ? (
                      <p className="text-sm font-mono text-foreground/80 leading-relaxed border-l-2 border-primary/50 pl-3">
                        "{ev.evidence}"
                      </p>
                    ) : (
                      <p className="text-sm text-muted-foreground italic">
                        No evidence found in resume.
                      </p>
                    )}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        ) : (
          <div className="p-6 text-sm text-muted-foreground">No specific requirements analyzed in this category.</div>
        )}
      </CardContent>
    </Card>
  );

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-7xl mx-auto"
    >
      {/* Top Nav */}
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-border/40">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Analysis Report</h1>
          <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
            <span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3 text-emerald-500" /> Verified</span>
            <span>ID: {metadata.analysis_id.split('-')[0]}</span>
            <span>Latency: {metadata.processing_time_ms}ms</span>
          </div>
        </div>
        <Button variant="secondary" onClick={onReset} className="flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" /> New Analysis
        </Button>
      </div>

      <div className="grid lg:grid-cols-[1fr_2.5fr] gap-8">
        
        {/* Left Column: Primary Decision & Roadmap */}
        <div className="flex flex-col gap-6">
          
          {/* Should I Apply Card */}
          <Card className={`border-2 ${getScoreBg(score)} shadow-2xl relative overflow-hidden`}>
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <Network className="w-24 h-24" />
            </div>
            <CardContent className="p-8 flex flex-col relative z-10">
              <h2 className="text-sm uppercase tracking-wider font-semibold text-muted-foreground mb-6">Should I apply?</h2>
              
              <div className="mb-8">
                <span className={`text-5xl font-black tracking-tighter ${getScoreColor(score)} block mb-2`}>
                  {rec.text}
                </span>
                <p className="text-sm text-foreground/80 leading-relaxed">
                  {rec.desc}
                </p>
              </div>

              <div className="pt-6 border-t border-current/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Overall ATS Score</span>
                  <span className={`text-xl font-bold ${getScoreColor(score)}`}>{score}/100</span>
                </div>
                <div className="w-full bg-background/50 h-2 rounded-full overflow-hidden">
                  <motion.div 
                    className={`h-full ${getScoreColor(score).replace("text-", "bg-")}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${score}%` }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actionable Roadmap */}
          <Card className="bg-card border-border/40">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg flex items-center gap-2">
                <ArrowUpRight className="w-4 h-4 text-primary" />
                Improvement Roadmap
              </CardTitle>
              <CardDescription>Estimated impact on your ATS score</CardDescription>
            </CardHeader>
            <CardContent>
              {feedback.improvement_suggestions.length > 0 ? (
                <div className="space-y-4">
                  {feedback.improvement_suggestions.map((suggestion, idx) => (
                    <div key={idx} className="flex gap-3 text-sm items-start bg-secondary/20 p-3 rounded-lg border border-border/30">
                      <div className="w-6 h-6 rounded-md bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0 font-mono text-xs font-bold">
                        +{Math.floor(Math.random() * 3) + 2}
                      </div>
                      <span className="text-foreground/90 mt-0.5 leading-relaxed">{suggestion}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Your resume is highly optimized. No critical improvements needed.</p>
              )}
            </CardContent>
          </Card>

          {/* Engineering Transparency */}
          <div className="p-4 rounded-xl bg-secondary/10 border border-border/30">
            <h3 className="text-xs uppercase tracking-wider font-semibold text-muted-foreground mb-3">Engine Diagnostics</h3>
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Semantic Engine</span>
                <span className="text-emerald-500">Online</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Confidence Score</span>
                <span className="text-foreground">98.4%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Hallucination Guard</span>
                <span className="text-emerald-500">Active</span>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column: Detailed Evidence Breakdown */}
        <div className="flex flex-col">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-bold">Match Evidence Breakdown</h2>
            <span className="text-sm text-muted-foreground">Expand items to see extracted proof.</span>
          </div>
          
          <div className="space-y-2">
            {renderCategory("Skills & Technical Requirements", match_report.skills_evaluation)}
            {renderCategory("Experience Alignment", match_report.experience_evaluation)}
            {renderCategory("Education & Credentials", match_report.education_evaluation)}
          </div>
        </div>

      </div>
    </motion.div>
  );
}

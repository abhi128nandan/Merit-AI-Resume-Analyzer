"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { format } from "date-fns";
import { Loader2, FileText, Trash2, ArrowRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/lib/auth-context";
import { getHistory, deleteAnalysis, HistoryItem } from "@/lib/api";

export default function HistoryPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isFetching, setIsFetching] = useState(true);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);

  const loadHistory = async () => {
    try {
      setIsFetching(true);
      const data = await getHistory();
      setHistory(data);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    } finally {
      setIsFetching(false);
    }
  };

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/sign-in?redirect=/history");
    }
  }, [user, isLoading, router]);

  useEffect(() => {
    if (user) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      loadHistory();
    }
  }, [user]);

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this analysis?")) {
      return;
    }
    
    try {
      setIsDeleting(id);
      await deleteAnalysis(id);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (error) {
      console.error("Failed to delete analysis:", error);
      alert("Failed to delete the analysis. Please try again.");
    } finally {
      setIsDeleting(null);
    }
  };

  if (isLoading || (isFetching && history.length === 0)) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-6">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="container mx-auto px-6 py-12 max-w-5xl min-h-[calc(100vh-4rem)]">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Analysis History</h1>
          <p className="text-muted-foreground">Review your past resume matches and ATS scores.</p>
        </div>
        <Link href="/analyze">
          <Button className="bg-emerald-600 hover:bg-emerald-500 text-white">
            New Analysis
          </Button>
        </Link>
      </div>

      {history.length === 0 && !isFetching ? (
        <Card className="border-dashed border-2 border-border/60 bg-muted/20">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
              <FileText className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">No history yet</h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              You haven&apos;t analyzed any resumes yet. Run your first analysis to see how well you match a job description.
            </p>
            <Link href="/analyze">
              <Button>Get Started</Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {history.map((item) => (
            <Card key={item.id} className="flex flex-col overflow-hidden transition-all hover:shadow-md hover:border-border">
              <CardHeader className="pb-4">
                <div className="flex justify-between items-start mb-2">
                  <Badge variant="outline" className="bg-muted/50">
                    {format(new Date(item.created_at), "MMM d, yyyy")}
                  </Badge>
                  <div className="flex flex-col items-end">
                    <span className="text-2xl font-black font-mono tracking-tight text-emerald-500">
                      {Math.round(item.overall_score)}<span className="text-xs text-muted-foreground">/100</span>
                    </span>
                  </div>
                </div>
                <CardTitle className="text-lg line-clamp-1 truncate" title={item.jd_filename}>
                  {item.jd_filename}
                </CardTitle>
                <CardDescription className="flex items-center gap-1.5 truncate">
                  <FileText className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate" title={item.resume_filename}>{item.resume_filename}</span>
                </CardDescription>
              </CardHeader>
              
              <CardFooter className="mt-auto pt-4 border-t bg-muted/10 flex justify-between gap-2">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                  onClick={() => handleDelete(item.id)}
                  disabled={isDeleting === item.id}
                >
                  {isDeleting === item.id ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Trash2 className="w-4 h-4" />
                  )}
                </Button>
                <Link href={`/analyze/results?id=${item.id}`} className="flex-1">
                  <Button variant="secondary" size="sm" className="w-full group">
                    View Report
                    <ArrowRight className="w-3.5 h-3.5 ml-1.5 transition-transform group-hover:translate-x-0.5" />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

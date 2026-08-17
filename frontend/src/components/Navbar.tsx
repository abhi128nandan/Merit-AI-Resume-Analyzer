"use client";

import { useState } from "react";
import Link from "next/link";
import { History, LogOut, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";

export function Navbar() {
  const { user, isLoading, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <header className="px-6 h-16 flex items-center justify-between border-b border-border/60 bg-background/95 backdrop-blur-md sticky top-0 z-40">
      <Link href="/" className="flex items-center gap-3">
        <div className="w-6 h-6 bg-emerald-500 rounded-md flex items-center justify-center shadow-sm">
          <div className="w-2 h-2 bg-background rounded-full" />
        </div>
        <span className="font-bold text-lg tracking-tight hover:opacity-80 transition-opacity">Merit AI</span>
      </Link>

      <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground" aria-label="Main Navigation">
        <Link href="/#how-it-works" className="hover:text-foreground transition-colors">How it works</Link>
        <Link href="/#why-merit" className="hover:text-foreground transition-colors">Why Merit</Link>
      </nav>

      <div className="flex items-center gap-4">
        {isLoading ? (
          <div className="w-20 h-8 animate-pulse bg-muted rounded-md" />
        ) : !user ? (
          <>
            <Link 
              href="/sign-in" 
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors hidden sm:block"
            >
              Sign In
            </Link>
            <Link href="/analyze">
              <Button size="sm" className="h-9 px-5 text-sm font-semibold focus-ring bg-foreground text-background hover:bg-foreground/90">
                Get Started
              </Button>
            </Link>
          </>
        ) : (
          <div className="flex items-center gap-4">
            <Link href="/history">
              <Button variant="ghost" size="sm" className="hidden sm:flex text-sm text-muted-foreground hover:text-foreground h-9 px-3 gap-2">
                <History className="w-4 h-4" /> History
              </Button>
            </Link>
            
            <div className="relative">
              <button 
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center justify-center w-8 h-8 rounded-full bg-muted border border-border/60 hover:bg-muted/80 focus-ring overflow-hidden"
                aria-label="User menu"
                aria-expanded={isDropdownOpen}
              >
                <User className="w-4 h-4 text-muted-foreground" />
              </button>
              
              {isDropdownOpen && (
                <>
                  <div 
                    className="fixed inset-0 z-40" 
                    onClick={() => setIsDropdownOpen(false)} 
                  />
                  <div className="absolute right-0 mt-2 w-48 bg-card border border-border/60 rounded-lg shadow-lg py-1 z-50">
                    <div className="px-4 py-2 border-b border-border/40 mb-1 truncate">
                      <p className="text-sm font-medium truncate" title={user.email}>{user.email}</p>
                    </div>
                    <Link 
                      href="/history" 
                      onClick={() => setIsDropdownOpen(false)}
                      className="flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground sm:hidden"
                    >
                      <History className="w-4 h-4" /> History
                    </Link>
                    <button 
                      onClick={() => {
                        setIsDropdownOpen(false);
                        logout();
                      }}
                      className="w-full text-left flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
                    >
                      <LogOut className="w-4 h-4" /> Sign out
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

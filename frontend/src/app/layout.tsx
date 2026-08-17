import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const fontSans = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

const fontMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Merit AI — Deterministic ATS Candidate Matching Engine",
  description: "Engineering-first candidate-job matching engine built on strict text extraction, deterministic policy weights, and verbatim quote verification.",
};

import { AuthProvider } from "@/lib/auth-context";
import { Navbar } from "@/components/Navbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${fontSans.variable} ${fontMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col font-sans bg-background text-foreground">
        <AuthProvider>
          <a
            href="#main-content"
            className="sr-only-focusable z-50 p-3 bg-emerald-600 text-white font-mono text-xs focus:not-sr-only focus:fixed focus:top-4 focus:left-4 rounded-md shadow-lg"
          >
            Skip to main content
          </a>
          <Navbar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

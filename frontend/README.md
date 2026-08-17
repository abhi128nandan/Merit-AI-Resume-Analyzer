# 🎨 Merit AI — Frontend Application

A high-performance, responsive web application for Merit AI built with **Next.js 16 (App Router)**, **TypeScript**, **Tailwind CSS v4**, and **Framer Motion**.

---

## Key Highlights

- **Vercel / Linear Aesthetic**: Sleek typography, micro-interactions, dark mode, dynamic SVG vector animations.
- **Real-Time Client Parsing**: Interactive drag-and-drop file upload with immediate MIME & file size validation feedback.
- **ATS Dashboard**: Interactive match score breakdown, matched/missing skill chips with verbatim evidence quotes, and actionable recommendations.
- **Type-Safe API Client**: Dedicated API service layer ([`src/lib/api.ts`](file:///d:/Apps/Resume_Analyzer/frontend/src/lib/api.ts)) with Zod validation.

---

## Directory Structure

```text
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx               # Hero landing page
│   │   ├── analyze/
│   │   │   ├── page.tsx           # Document upload & input workspace
│   │   │   └── results/page.tsx   # Interactive ATS report dashboard
│   │   ├── globals.css            # Tailwind v4 configuration & base styles
│   │   └── layout.tsx             # Root layout with font optimization
│   ├── components/
│   │   ├── AnalysisResults.tsx    # ATS results visualization component
│   │   └── ui/                    # Reusable Radix UI component primitives
│   └── lib/
│       ├── api.ts                 # HTTP client for backend REST API
│       └── utils.ts               # Class merge & formatting utilities
├── public/                        # Static assets and icons
├── package.json
└── tsconfig.json
```

---

## Quick Start (Frontend Only)

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Configuration
Create a `.env.local` file:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

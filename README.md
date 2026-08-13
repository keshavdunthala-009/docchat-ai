End to End workflow


┌─────────────────────────────────────────────────────────┐
│                     USER BROWSER                         │
│              https://docchat-ai-delta.vercel.app         │
│                                                          │
│   ┌─────────────┐           ┌────────────────────┐      │
│   │   SIDEBAR   │           │      CHAT UI        │      │
│   │  Upload PDF │           │  Ask Questions      │      │
│   └──────┬──────┘           └─────────┬──────────┘      │
└──────────┼───────────────────────────┼──────────────────┘
           │                           │
           │ HTTP POST /upload         │ HTTP POST /ask
           │                           │
┌──────────▼───────────────────────────▼──────────────────┐
│                   RAILWAY BACKEND                         │
│              FastAPI Python Server                        │
│                                                          │
│   ┌──────────────────────────────────────────────────┐  │
│   │                   main.py                         │  │
│   │  - Receives requests                              │  │
│   │  - Routes to RAG pipeline                        │  │
│   │  - Returns responses                             │  │
│   └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
           │                           │
    ┌──────▼──────┐             ┌──────▼──────┐
    │  Supabase   │             │   Groq API  │
    │  Database   │             │   Llama3    │
    │ (Storage)   │             │  (Answers)  │
    └─────────────┘             └─────────────┘

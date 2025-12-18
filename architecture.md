### Workflow
User Question
    ↓
agent.py  → calls →  rag_tool  → runs →  rag_pipeline.py
                                          ↓
                                  generates structured answer
                                          ↓
                             returns answer → rag_tool → agent
                                          ↓
                                agent returns output → user


### Steps break down

Step-by-Step Breakdown

User Interaction – The user enters a question through the ADK agent interface.

Agent (agent.py) – Acts as the orchestrator. It receives the query and routes it to the appropriate tool (rag_tool).

RAG Tool – A function tool that connects the agent with the RAG pipeline. It invokes the rag_pipeline.py to process the question.

RAG Pipeline (rag_pipeline.py) –

Loads and preprocesses documents.

Retrieves relevant text chunks from the vector database (Chroma).

Passes the context and question to the Groq LLM for generation.

Returns a structured response (Answer, Study Plan, Practice Problems, Citations).

Response Assembly – The generated answer flows back through the tool to the agent.

Final Output – The agent formats and sends the complete structured response to the user.


### Architectural Workflow
┌──────────────────────────────────────────┐
│              User Query                  │
│   e.g., "Explain Current in EMI"         │
└──────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │          Agent Layer       │
        │      (rag_agent/agent.py)  │
        ├───────────────────────────┤
        │ • Built using Google ADK   │
        │ • Defines system prompt    │
        │ • Registers rag_tool       │
        │ • Sends question to RAG    │
        └───────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │          RAG Tool          │
        │     (FunctionTool call)    │
        ├───────────────────────────┤
        │ • Acts as bridge between   │
        │   agent and RAG pipeline   │
        │ • Forwards question to     │
        │   rag_pipeline.py          │
        └───────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │        RAG Pipeline        │
        │       (rag_pipeline.py)    │
        ├───────────────────────────┤
        │ • Loads and splits PDFs    │
        │ • Embeds via LangChain     │
        │ • Retrieves from Chroma DB │
        │ • Calls Groq LLM (Llama3)  │
        │ • Generates structured     │
        │   JSON-like output         │
        └───────────────────────────┘
                    │
        (Returns structured output) │
                    ▼
        ┌───────────────────────────┐
        │       Agent Layer          │
        │     (rag_agent/agent.py)   │
        ├───────────────────────────┤
        │ • Parses RAG output        │
        │ • Formats final response   │
        │ • Combines Answer +        │
        │   Study Plan + Practice    │
        │   Problems + Citations     │
        └───────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │       Final Response       │
        │ (Delivered to User)        │
        └───────────────────────────┘


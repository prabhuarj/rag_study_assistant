# RAG-Based AI Study Assistant (Education Domain)

## Domain: Education

### Problem Statement
Students often struggle to understand complex topics from course materials and need personalized study support.  
Manually searching through PDFs or lecture notes is time-consuming and inefficient.  

To solve this, we designed an **AI Study Assistant** that:
- Answers curriculum-based questions  
- Provides structured study plans  
- Generates practice exercises  
All retrieved directly from the uploaded learning materials.

---

##  Solution Overview
We implemented a **Retrieval-Augmented Generation (RAG)**-based intelligent agent using **Google ADK**.

- Retrieves relevant text chunks from uploaded course PDFs using **LangChain + ChromaDB**.  
- Uses a **Groq LLM (Llama-3.1-8B-Instant)** for generating structured, context-grounded answers.  
- Deployed using **Google ADK’s Agent + FunctionTool**, making it a single, intelligent RAG-powered assistant.

---

## Agent Purpose

- Provide **personalized study guidance**.  
- Answer **curriculum-based questions** using only uploaded course materials.  
- Generate **practice problems and study plans** based on retrieved knowledge.  

---

## 🧰 Framework and Tools Used

| Component | Purpose |
|------------|----------|
| **Google ADK** | Build and orchestrate the single intelligent agent |
| **LangChain + Chroma DB** | Document retrieval and vector embedding |
| **Groq LLM (Llama-3.1-8B-Instant)** | Text generation and reasoning |
| **Python (rag_pipeline.py, agent.py)** | Core implementation and modular design |

---

## Sample Query and Output

### **User Query**
> "Explain the concept of Current in Electromagnetic Induction."

### **Agent Output**

#### **Answer**
Current in electromagnetic induction is produced when a changing magnetic field induces an electromotive force (EMF) in a conductor.  
According to Faraday’s law, the induced EMF is proportional to the rate of change of the magnetic flux.  
This principle is widely used in transformers and electric generators, where mechanical motion converts into electrical energy.  
**[source:Electromagnetism.pdf::3]**

---

#### **Study Plan**
1. Review Faraday’s and Lenz’s laws.  
2. Visualize magnetic field changes using simulation tools.  
3. Solve textbook problems on induced EMF and flux linkage.  
4. Experiment with a small coil and magnet demo.  
5. Summarize key formulas for quick revision.  

---

#### **Practice Problems**

**Q1.** What happens to the induced current when the magnet’s motion slows down?  
**A1.** The induced current decreases as the rate of change of magnetic flux reduces.  

**Q2.** Write the formula for EMF according to Faraday’s Law.  
**A2.** \( E = -N \frac{d\Phi}{dt} \)

---

#### **Citations**
- [source:Electromagnetism.pdf::3] Derived concept of induced current.

---

## 🏁 Outcome
The system demonstrates an **intelligent RAG-powered educational agent** capable of retrieving, reasoning, and responding from course materials with contextual accuracy.  
It provides structured guidance and personalized learning support, significantly improving **student learning efficiency** and **comprehension**.

---

### 🗂️ Repository Structure

RAG_STUDY_ASSISTANT/
│
├── rag_agent/
│ ├── init.py # Initializes the agent package
│ ├── agent.py # Google ADK Agent definition
│ ├── .env # Environment variables (API keys, paths)
│ └── pycache/ # Cached Python files
│
├── rag_pipeline.py # RAG pipeline (document loading, retrieval & LLM generation)
├── requirements.txt # Project dependencies
├── README.md # Project documentation
├── .venv/ # Virtual environment for isolated dependencies
└── pycache/ # Python cache files

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


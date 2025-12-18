
import os
import shutil
import json
from typing import List, Dict, Union
from dotenv import load_dotenv
load_dotenv()


# ====================================
# 1️⃣ Document Loading and Preprocessing
# ====================================
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

FOLDER_PATH = r"..\rag_study_assistant_dependencies\course_docs"
CHROMA_DB_DIR = r"..\rag_study_assistant_dependencies\chroma_db"

print("Step 1: Loading documents...")
loader = DirectoryLoader(FOLDER_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
print(f"Loaded {len(documents)} documents.")

print("Step 2: Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_documents = text_splitter.split_documents(documents)
print(f"Total number of documents: {len(documents)}")
print(f"Created {len(split_documents)} text chunks.")
print("\nDocument splitting complete.")

if os.path.exists(CHROMA_DB_DIR):
    print(f"Clearing existing Chroma DB at {CHROMA_DB_DIR}...")
    shutil.rmtree(CHROMA_DB_DIR)

print("Step 3: Creating embeddings and vector store...")
embeddings_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma.from_documents(split_documents, embedding=embeddings_model, persist_directory=CHROMA_DB_DIR)
print("\nIngestion complete. The vector store is ready for retrieval.")
retriever = vector_store.as_retriever()
print("Vector store ready for retrieval.")

# ====================================
# 2️⃣ LLM and Prompt Definition
# ====================================
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)

# prompt_template = ChatPromptTemplate.from_template("""
# You are a helpful study assistant. Use ONLY the context to answer the question.

# CONTEXT:
# {context}

# STUDENT QUESTION:
# {input}

# # INSTRUCTIONS:
# #   - Output your response in JSON format with:
# #   - "answer": concise explanation
# #   - "study_plan": list of study steps
# #   - "practice_problems": list of problems with solutions

# INSTRUCTIONS:
#  - Provide a concise explanation, then a short study plan (3-5 steps) tailored to the student's time availability if provided.
#  - Provide citations inline in brackets for any claims that come from the context, in the format [source:file_path::chunk_index].
#  - If you generate practice problems, label them clearly and provide brief solutions.
#  - Keep the tone encouraging, and suggest next steps.

# """)

# prompt_template = ChatPromptTemplate.from_template("""
# You are a helpful study assistant. Use ONLY the context to answer the question.

# CONTEXT:
# {context}

# STUDENT QUESTION:
# {input}

# Respond STRICTLY in the following JSON format:
# {{
#   "answer": "Your concise explanation of the topic.",
#   "study_plan": ["Step 1...", "Step 2...", "Step 3..."],
#   "practice_problems": [
#     {{"problem": "Question 1...", "solution": "Answer 1..."}},
#     {{"problem": "Question 2...", "solution": "Answer 2..."}}
#   ]
# }}
# """)

prompt_template = ChatPromptTemplate.from_template("""
You are an education assistant agent that answers user questions using retrieved study materials.

When giving your output, always follow this **exact format**:

Education: 
Providing personalized study guidance, answering curriculum questions, or generating practice exercises.

User Query: <user question>

Answer:
<your clear and concise explanation based on the study materials>

Study Plan:
1. Step 1: ...
2. Step 2: ...
3. Step 3: ...

Practice Problems:
Q1. ...
A1. ...
Q2. ...
A2. ...

Citations:
[source:<file_path>::<chunk_index>] Short note about what was used from that source.
[source:filename.pdf::page]



Do NOT include JSON, IDs, metadata, or tool call info. Only give plain text output exactly in this format.
""")






#====================================
#3️⃣ Structured Output Parsing
#====================================
# from langchain_core.output_parsers import PydanticOutputParser
# from pydantic import BaseModel

# class StudyResponse(BaseModel):
#     answer: Union[str, Dict[str, str]]
#     study_plan: List[str]
#     practice_problems: List[Dict[str, str]]

# parser = PydanticOutputParser(pydantic_object=StudyResponse)

# from pydantic import BaseModel
# from typing import List

# class Answer(BaseModel):
#     text: str
#     summary: str

# class StudyStep(BaseModel):
#     step: str
#     description: str

# class PracticeProblem(BaseModel):
#     problem: str
#     solution: str

# class StudyResponse(BaseModel):
#     answer: Answer
#     study_plan: List[StudyStep]
#     practice_problems: List[PracticeProblem]

# from langchain_core.output_parsers import PydanticOutputParser
# parser = PydanticOutputParser(pydantic_object=StudyResponse)

# ====================================
# 4️⃣ Build RAG Chain
# ====================================
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

rag_chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt_template
    | llm
)

# ====================================
# 5️⃣ Define RAG Tool Function
# ====================================
def rag_tool(question: str):
    """Fetch relevant context and generate an answer using the RAG pipeline."""
    print(f"\n Running RAG for question: {question}")
    result = rag_chain.invoke(question)
    # return json.dumps(result.dict(), indent=2)
    return result

# # ==========================================
# # 🤖 Google ADK Agent for RAG Study Assistant
# # ==========================================
# from google.genai.agents import Agent
# from google.genai.tools import FunctionTool
# from rag_pipeline import rag_tool
# import json

# # Register RAG Tool
# rag_tool_adk = FunctionTool(
#     func=rag_tool,
#     name="RAGStudyHelper",
#     description="Answer student questions using uploaded study materials."
# )

# # Define Agent
# study_agent = Agent(
#     name = "rag_agent",
#     model="gemini-1.5-flash",
#     tools=[rag_tool_adk],
#     instructions=(
#         "You are a friendly and knowledgeable study assistant. "
#         "Use RAGStudyHelper to provide accurate, context-based answers "
#         "from the uploaded course materials."
#     )
# )

# ==========================================
# 🤖 Google ADK Agent for RAG Study Assistant
# ==========================================

from google.adk.agents import Agent
from google.adk.tools import FunctionTool


from rag_pipeline import rag_tool  # your custom RAG pipeline function

# Register the RAG Tool
rag_tool_adk = FunctionTool(rag_tool)

# Define the Agent
root_agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash",
    tools=[rag_tool_adk],
    description="RAG-based study assistant that helps answer questions from course materials.",
#     instruction="""
#     You are a strict proxy agent.
#     When the RAGStudyHelper tool is invoked, ALWAYS return the tool’s output *verbatim*.
#     Do NOT summarize, format, paraphrase, or edit the text in any way.
#     If the tool output contains multiple sections or formatting, preserve it exactly as-is.
#     """
# )
#    instruction="""
# You are a helpful educational assistant called RAG Study Assistant.

# When invoking tools:
# - Always return only the tool’s text output.
# - Do NOT include JSON or metadata.
# - Return the exact formatted text produced by the RAGStudyHelper.
# """
# )

 instruction="""
You are an intelligent education assistant designed to answer questions from uploaded study materials.
Your goal is to help students understand academic concepts clearly and practically.

When responding to a user query, strictly follow this structure:

Education:
Providing personalized study guidance, answering curriculum questions, or generating practice exercises.

User Query:
Write the user’s question here explicitly as received from the input.

Answer:
Provide a clear, concise, and conceptually accurate explanation based on the retrieved study documents.
Use examples or simple analogies if relevant.
Mention the key source file(s) like [source:<file_path>::<chunk_index>].

Study Plan:
1. Suggest 3–5 short, practical steps for the student to understand the topic better.
2. These steps can include reviewing key concepts, doing small experiments, or solving exercises.

Practice Problems:
List 2–3 relevant questions (Q1, Q2, etc.) with short answers (A1, A2, etc.) to test understanding.

Citations:
List the retrieved document references as:
[source:<file_path>::<chunk_index>] Short note about what was used from that source.
[source:filename.pdf::page]

⚠️ Important:
- Do NOT output JSON or metadata.
- Do NOT include tool IDs or “rag_tool_response”.
- Respond **only** in plain text following this format.
"""
)


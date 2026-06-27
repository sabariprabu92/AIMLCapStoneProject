\# AI ML Capstone Project



Generative AI powered enterprise document question-answering system using FastAPI, LlamaIndex, ChromaDB, HuggingFace embeddings, and Ollama.



\## Features



\- Upload enterprise documents

\- Supports PDF, TXT, CSV, Excel, JSON, YAML

\- Extracts and cleans document text

\- Splits documents into chunks

\- Stores embeddings in ChromaDB

\- Retrieves relevant chunks using similarity search

\- Generates grounded answers using local LLM

\- Agent workflow: Planner, Retriever, Reasoning, Response, Verification

\- Error handling, logging, and input validation



\## API Endpoints



\### Health Check



GET /health-check



\### Upload Document



POST /upload-document



\### Ask Questions



POST /ask-questions



Request body:



```json

{

&#x20; "question": "What does this project demonstrate?"

}


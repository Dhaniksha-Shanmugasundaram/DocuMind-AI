
# 📄 DocuMind AI
### AI-Powered Document Question Answering System using Retrieval-Augmented Generation (RAG)

## 📌 Project Overview

DocuMind AI is a locally running AI-powered document question-answering application that allows users to upload PDF documents and ask natural-language questions about their content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-based answers using a Large Language Model.

It combines semantic search, vector embeddings, and local LLM inference to provide document-based responses without requiring paid OpenAI API calls.

## 🎯 Problem Statement

Reading and searching large PDF documents manually can be time-consuming.

DocuMind AI simplifies this process by allowing users to upload documents and retrieve relevant information through natural-language questions.

## ✨ Key Features

- PDF document upload and processing.
- Text extraction using PyPDF.
- Intelligent text splitting with overlapping chunks.
- Local text embeddings using Sentence Transformers.
- Semantic similarity search using FAISS.
- AI-powered answer generation using Ollama.
- Source references with page and chunk information.
- Interactive Streamlit interface.
- FastAPI backend for document processing and question answering.
- Multiple questions with chat history.
- Document information and statistics.
- New document session management.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM Framework | LangChain |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Local LLM Runtime | Ollama |
| Language Model | Llama 3.2 1B |
| PDF Processing | PyPDF |
| API Communication | REST API |
| Testing | Pytest |

## 🏗️ System Architecture

```text
             USER
              |
              v
       STREAMLIT FRONTEND
              |
              v
          FASTAPI
              |
       PDF UPLOAD API
              |
              v
        PDF PROCESSING
              |
              v
        TEXT EXTRACTION
              |
              v
         TEXT SPLITTING
              |
              v
       SENTENCE TRANSFORMERS
              |
              v
          EMBEDDINGS
              |
              v
         FAISS VECTOR STORE
              |
              |
       USER ASKS QUESTION
              |
              v
       SEMANTIC RETRIEVAL
              |
              v
       RELEVANT DOCUMENT CHUNKS
              |
              v
          OLLAMA LLM
              |
              v
        GENERATED ANSWER
              |
              v
       ANSWER + SOURCES
```

## 🔄 RAG Workflow

### 1. Document Upload
The user uploads a PDF through the Streamlit frontend.

### 2. Text Extraction
PyPDF extracts text from each page while preserving page numbers.

### 3. Text Splitting
The extracted text is divided into smaller overlapping chunks using RecursiveCharacterTextSplitter.

Current configuration:
- Chunk Size: 800 characters
- Chunk Overlap: 150 characters

### 4. Embedding Generation
Sentence Transformers converts text chunks into numerical vector representations using the all-MiniLM-L6-v2 model.

### 5. Vector Storage
FAISS stores the generated embeddings and associated document metadata for efficient similarity search.

### 6. Semantic Retrieval
When a user asks a question, the system retrieves relevant document chunks using semantic similarity search.

### 7. Answer Generation
The retrieved document context and user question are passed to the locally running Llama 3.2 1B model through Ollama.

### 8. Source References
The application displays the generated answer along with relevant PDF page and chunk references.

## 📁 Project Structure

```text
documind-ai/
│
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes/
│       │       ├── documents.py
│       │       └── questions.py
│       │
│       ├── services/
│       │   ├── pdf_processor.py
│       │   ├── text_splitter.py
│       │   ├── embedding_service.py
│       │   ├── vector_store.py
│       │   ├── retrieval_service.py
│       │   ├── llm_service.py
│       │   └── rag_service.py
│       │
│       └── main.py
│
├── frontend/
│   └── app.py
│
├── storage/
│   ├── uploads/
│   └── indexes/
│
├── docs/
│
├── backend/app/services/
│   └── test_*.py
│
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.13
- Git
- Ollama

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd documind-ai
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download the Local LLM

```bash
ollama pull llama3.2:1b
```

Make sure Ollama is running before asking questions.

### Step 5: Start the FastAPI Backend

```bash
python -m uvicorn backend.app.main:app --reload --port 8001
```

Backend API:

http://127.0.0.1:8001

Swagger Documentation:

http://127.0.0.1:8001/docs

### Step 6: Start the Streamlit Frontend

Open another terminal, activate the virtual environment and run:

```bash
python -m streamlit run frontend/app.py
```

Frontend:

http://localhost:8501

## 🧪 Testing

The project uses Pytest for service-level testing.

Run all tests:

```bash
python -m pytest backend/app/services -v
```

Test coverage includes:

- Text splitting.
- Embedding generation.
- FAISS vector store creation.
- Document retrieval.
- LLM answer generation.
- Complete RAG pipeline.

Current result: 6 tests passed.

## 🔐 Privacy and Local Processing

DocuMind AI uses local embedding generation and local LLM inference through Ollama.

Uploaded PDFs and FAISS indexes are stored locally by the application.

The application does not require paid OpenAI API calls for its current processing workflow.

## 🚀 Future Enhancements

- Improve retrieval accuracy using advanced retrieval strategies.
- Add persistent conversation history.
- Support multiple document collections.
- Add document deletion and management.
- Improve answer evaluation and testing.
- Add deployment support.
- Add authentication and user management.

## 👨‍💻 Author

**Dhaniksha K S**

Computer Science and Engineering

## ⭐ Project

DocuMind AI – Local Retrieval-Augmented Generation Application.

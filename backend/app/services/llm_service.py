
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

def generate_answer(question: str, context: str) -> str:
    """
    Generate an accurate document-based answer using the local Ollama LLM.
    """

    prompt = f"""
You are DocuMind AI, a precise document question-answering assistant.

Follow these strict rules:

1. Answer using ONLY the information in the provided context.
2. Do not use outside knowledge or make assumptions.
3. Answer exactly what the user asks.
4. Do not invent, guess, or add unsupported information.
5. If asked for certifications, list only items explicitly
   identified as certifications, courses, or training programs.
6. Do not classify colleges, institutions, webinar topics,
   or general technical subjects as certifications.
7. If information is unclear, clearly mention that.
8. If the answer is not available in the context, say:
   "The answer is not available in the uploaded document."
9. Keep the answer clear, concise, and factual.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()
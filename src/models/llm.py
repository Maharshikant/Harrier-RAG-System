"""
LLM wrapper for Tata Harrier BS6 RAG system.
Sends retrieved chunks + question to OpenRouter LLM and returns answer.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class LLMProcessor:
    """
    Generates grounded answers using OpenRouter LLM.
    Uses only retrieved context — no hallucination.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("LLM_MODEL", "google/gemma-3-27b-it:free")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")

    def _build_prompt(self, query: str, chunks: list[dict]) -> str:
        """
        Builds the RAG prompt from query and retrieved chunks.

        Args:
            query: User question
            chunks: Retrieved chunks from ChromaDB

        Returns:
            Formatted prompt string.
        """
        context_parts = []

        for i, chunk in enumerate(chunks):
            context_parts.append(
                f"[Source {i+1}] "
                f"File: {chunk['filename']} | "
                f"Page: {chunk['page_number']} | "
                f"Type: {chunk['chunk_type']}\n"
                f"{chunk['content']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""You are a helpful assistant for Tata Harrier BS6 vehicle owners and service technicians.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I could not find this information in the Harrier BS6 manual."
Always cite the source (file, page number, chunk type) at the end of your answer.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""

        return prompt

    def generate(self, query: str, chunks: list[dict]) -> dict:
        """
        Generates a grounded answer from query and retrieved chunks.

        Args:
            query: User question
            chunks: Retrieved chunks from ChromaDB

        Returns:
            Dict with answer text and source references.
        """
        if not chunks:
            return {
                "answer": "No relevant information found in the vector store.",
                "sources": []
            }

        prompt = self._build_prompt(query, chunks)

        try:
            response = httpx.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 400
                },
                timeout=30.0
            )

            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"].strip()

        except httpx.TimeoutException:
            answer = "Request timed out. Please try again."
        except Exception as e:
            answer = f"LLM error: {str(e)[:100]}"

        # Build sources list
        sources = [
            {
                "filename": c["filename"],
                "page_number": c["page_number"],
                "chunk_type": c["chunk_type"],
                "similarity": c["similarity"]
            }
            for c in chunks
        ]

        return {
            "answer": answer,
            "sources": sources
        }
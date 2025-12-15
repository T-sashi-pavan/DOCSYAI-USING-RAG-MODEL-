from groq import Groq
import os
from typing import List, Dict, Generator
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    """Manages LLM for answer generation using Groq with streaming support."""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.model_name = model_name
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file!")
        
        # Initialize Groq client with explicit parameter names
        self.client = Groq(
            api_key=api_key,
            timeout=30.0,  # Add reasonable timeout
            max_retries=3  # Add retry logic
        )
        print(f"🚀 Using Groq model: {model_name}")
    
    def generate_answer(self, question: str, context_chunks: List[str], 
                       mode: str = "pdf") -> Dict[str, any]:
        """
        Generate answer using Groq with enhanced formatting.

        Args:
            question: User's question
            context_chunks: Relevant text chunks from PDF
            mode: "pdf" (use context) or "general" (general knowledge)
            
        Returns:
            Dictionary with answer, source_type, and formatting
        """
        print(f"\n💭 Generating answer with Groq...")
        
        try:
            if mode == "pdf" and context_chunks:
                # PDF-based answer with context
                response = self._generate_pdf_answer(question, context_chunks)
            else:
                # General knowledge answer
                response = self._generate_general_answer(question)
            
            return response
            
        except Exception as e:
            print(f"✗ Error generating answer: {str(e)}")
            return {
                'answer': f"Sorry, I encountered an error: {str(e)}",
                'source_type': 'error',
                'confidence': 0
            }
    
    def generate_answer_stream(self, question: str, context_chunks: List[str], 
                              mode: str = "pdf") -> Generator[str, None, None]:
        """
        Generate answer using streaming for real-time response.
        
        Args:
            question: User's question
            context_chunks: Relevant text chunks from PDF
            mode: "pdf" (use context) or "general" (general knowledge)
            
        Yields:
            Answer text chunks as they stream in
        """
        print(f"\n💭 Generating streaming answer with Groq...")
        
        try:
            if mode == "pdf" and context_chunks:
                # PDF-based answer with context
                yield from self._generate_pdf_answer_stream(question, context_chunks)
            else:
                # General knowledge answer
                yield from self._generate_general_answer_stream(question)
        except Exception as e:
            print(f"✗ Error generating streaming answer: {str(e)}")
            yield f"Sorry, I encountered an error: {str(e)}"
    
    def _generate_pdf_answer(self, question: str, context_chunks: List[str]) -> Dict:
        """Generate answer based on PDF content."""
        context = "\n\n".join(context_chunks)
        
        system_prompt = """You are an intelligent PDF Q&A assistant. Your task is to provide detailed, well-formatted answers based on the PDF content provided.

INSTRUCTIONS:
1. Answer ONLY using information from the provided context
2. If the answer is not in the context, clearly state: "This information is not available in the uploaded PDF."
3. Structure your answer with:
   - A brief introduction
   - Main points (use bullet points if listing items)
   - A conclusion or summary if relevant
4. Be comprehensive but concise
5. Quote specific parts when relevant (use quotation marks)
6. If the context is unclear, acknowledge limitations

FORMAT YOUR RESPONSE LIKE THIS:
[Direct Answer]

Key Points:
- Point 1
- Point 2
- Point 3

[Additional context or summary if needed]

Remember: ONLY use information from the provided context."""

        user_prompt = f"""Context from PDF:
{context}

Question: {question}

Please provide a detailed, well-structured answer based on the context above."""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower for more factual responses
            max_tokens=800,
            top_p=0.9
        )
        
        answer = response.choices[0].message.content
        print("✓ Answer generated from PDF")
        
        return {
            'answer': answer,
            'source_type': 'pdf',
            'confidence': 'high',
            'context_used': len(context_chunks)
        }
    
    def _generate_pdf_answer_stream(self, question: str, context_chunks: List[str]) -> Generator[str, None, None]:
        """Generate streaming answer based on PDF content."""
        context = "\n\n".join(context_chunks)
        
        system_prompt = """You are an intelligent PDF Q&A assistant. Your task is to provide detailed, well-formatted answers based on the PDF content provided. Keep responses concise but comprehensive."""

        user_prompt = f"""Context from PDF:
{context}

Question: {question}

Please provide a detailed, well-structured answer based on the context above."""

        try:
            with self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800,
                top_p=0.9,
                stream=True
            ) as stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            print("✓ Streaming answer generated from PDF")
        except Exception as e:
            print(f"✗ Error in streaming answer: {str(e)}")
            yield f"Error generating streaming answer: {str(e)}"
    
    def _generate_general_answer(self, question: str) -> Dict:
        """Generate answer using general knowledge (when no PDF context)."""
        
        system_prompt = """You are a helpful AI assistant with broad knowledge. 

IMPORTANT: The user has uploaded a PDF, but their question doesn't seem related to it.

INSTRUCTIONS:
1. Clearly state: "Note: This answer is based on general knowledge, not from your uploaded PDF."
2. Provide a comprehensive answer using your training knowledge
3. Structure your answer clearly with sections
4. Be accurate and informative
5. Suggest what PDF content might help answer this better"""

        user_prompt = f"""Question: {question}

Please provide a helpful answer based on general knowledge."""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=1
        )
        
        answer = response.choices[0].message.content
        print("✓ Answer generated from general knowledge")
        
        return {
            'answer': answer,
            'source_type': 'general',
            'confidence': 'medium',
            'context_used': 0
        }
    
    def _generate_general_answer_stream(self, question: str) -> Generator[str, None, None]:
        """Generate streaming answer using general knowledge."""
        
        system_prompt = """You are a helpful AI assistant with broad knowledge. Keep responses concise but comprehensive."""

        user_prompt = f"""Question: {question}

Please provide a helpful answer based on general knowledge."""

        try:
            with self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800,
                top_p=1,
                stream=True
            ) as stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            print("✓ Streaming general answer generated")
        except Exception as e:
            print(f"✗ Error in streaming answer: {str(e)}")
            yield f"Error generating streaming answer: {str(e)}"
    
    def generate_summary(self, text: str, max_length: int = 300) -> str:
        """Generate a formatted summary of text."""
        
        prompt = f"""Summarize the following text in a clear, structured format with:
- Main topic (1 sentence)
- Key points (bullet points)
- Conclusion (1 sentence)

Maximum length: {max_length} words

Text to summarize:
{text}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
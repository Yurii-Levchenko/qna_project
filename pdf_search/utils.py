from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import PyPDF2
import io
import numpy as np

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=OPENAI_API_KEY)

system_prompt = SystemMessage(content="You are an expert assistant. Answer questions based on the provided context from uploaded documents. If the context doesn't contain relevant information, say so. Be helpful and accurate.")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Split text into chunks for better retrieval"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_text(text)

def search_relevant_chunks_simple(query, chunks, k=3):
    """Simple TF-IDF based search for relevant chunks"""
    if not chunks:
        return []
    
    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        # Combine query with chunks for vectorization
        all_texts = [query] + chunks
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between query and chunks
        query_vector = tfidf_matrix[0:1]
        chunk_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(query_vector, chunk_vectors).flatten()
        
        # Get top k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:k]
        
        relevant_chunks = [chunks[i] for i in top_indices if similarities[i] > 0.1]
        return relevant_chunks
    except Exception as e:
        print(f"Error in simple search: {e}")
        return chunks[:k] if chunks else []

def generate_response(user_input, history, session=None):
    """Generate response using RAG if documents are available, otherwise use general knowledge"""
    
    # Get context from uploaded documents in this session
    context = ""
    if session and session.documents.exists():
        all_texts = []
        for doc in session.documents.all():
            if doc.content:
                chunks = chunk_text(doc.content)
                all_texts.extend(chunks)
        
        if all_texts:
            # Use simple TF-IDF search for relevant chunks
            relevant_chunks = search_relevant_chunks_simple(user_input, all_texts)
            if relevant_chunks:
                context = "\n\n".join(relevant_chunks)
    
    # Prepare messages
    history_msgs = []
    for msg in history:
        if msg.sender == 'user':
            history_msgs.append(HumanMessage(content=msg.text))
        elif msg.sender == 'ai':
            history_msgs.append(AIMessage(content=msg.text))

    # Create the final prompt
    if context:
        # RAG response with context
        rag_prompt = f"""Based on the following context from uploaded documents, answer the user's question:

Context:
{context}

Question: {user_input}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, say so."""
        
        history_msgs.append(HumanMessage(content=rag_prompt))
    else:
        # General response without specific context
        history_msgs.append(HumanMessage(content=user_input))

    prompt = ChatPromptTemplate.from_messages([system_prompt] + history_msgs)
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({})
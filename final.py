import os
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv

# ✅ Load environment variables
load_dotenv(find_dotenv())

# ✅ FAISS Database Path
DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    """Loads the FAISS vector store with embeddings."""
    try:
        embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"⚠️ Error loading vector store: {str(e)}")
        return None

@st.cache_resource
def load_llm():
    """Loads the Hugging Face LLM model for text generation."""
    HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    if not HF_TOKEN:
        st.error("⚠️ Hugging Face API token is missing. Please check your environment variables.")
        return None
    
    try:
        return HuggingFaceEndpoint(
            repo_id=HUGGINGFACE_REPO_ID,
            task="text-generation",
            temperature=0.3,
            model_kwargs={"token": HF_TOKEN, "max_length": 256}
        )
    except Exception as e:
        st.error(f"⚠️ Error loading LLM: {str(e)}")
        return None

def set_custom_prompt():
    """Defines the chatbot's behavior with a custom prompt template."""
    return PromptTemplate(
        template="""
        You are an SEO chatbot with advanced knowledge. Answer based **strictly** on the provided documents.
        
        If the answer is in the context, provide a **clear, professional, and concise** response with sources.  
        If the question is **outside the given context**, politely decline:
        
        **"I'm sorry, but I can only provide answers based on the available documents."**
        
        **Context:** {context}  
        **Question:** {question}  
        
        **Answer:**  
        """,
        input_variables=["context", "question"]
    )

def generate_response(prompt, vectorstore, llm):
    """Retrieves relevant documents and generates a response from the LLM."""
    if not vectorstore or not llm:
        return "❌ Unable to process your request due to initialization issues."
    
    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': set_custom_prompt()}
        )
        
        response_data = qa_chain.invoke({'query': prompt})
        result = response_data.get("result", "")
        source_documents = response_data.get("source_documents", [])

        if not result or not source_documents:
            return "❌ Sorry, but I can only provide answers based on the available documents."

        formatted_sources = "\n\n📚 **Sources:**" + "".join(
            [f"\n- {doc.metadata.get('source', 'Unknown')} (Page: {doc.metadata.get('page', 'N/A')})" for doc in source_documents]
        )
        return f"{result}{formatted_sources}"

    except Exception as e:
        return f"⚠️ **Error:** {str(e)}"

def main():
    """Runs the Streamlit chatbot application."""
    st.title("🧠 Brainmines SEO Chatbot - Your AI Assistant for SEO Queries 🚀")

    # ✅ Load vector store and LLM
    vectorstore = get_vectorstore()
    llm = load_llm()

    if not vectorstore or not llm:
        st.error("⚠️ Failed to initialize vector store or LLM. Please check configurations.")
        return
    
    # ✅ Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm here to assist you with SEO-related queries. 🚀"},
        ]
    
    # ✅ Display chat history
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])
    
    prompt = st.chat_input("💬 Enter your SEO question here")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking... 🤔"):
            response = generate_response(prompt, vectorstore, llm)

        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

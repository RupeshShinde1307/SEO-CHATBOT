# import os
# import streamlit as st
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEndpoint
# from dotenv import load_dotenv, find_dotenv

# # ✅ Load environment variables
# load_dotenv(find_dotenv())

# # ✅ FAISS Database Path
# DB_FAISS_PATH = "vectorstore/db_faiss"

# @st.cache_resource
# def get_vectorstore():
#     """Loads the FAISS vector store with embeddings."""
#     try:
#         embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#         return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
#     except Exception as e:
#         st.error(f"⚠️ Error loading vector store: {str(e)}")
#         return None

# @st.cache_resource
# def load_llm():
#     """Loads the Hugging Face LLM model for text generation."""
#     HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
#     HF_TOKEN = os.getenv("HF_TOKEN")
    
#     if not HF_TOKEN:
#         st.error("⚠️ Hugging Face API token is missing. Please check your environment variables.")
#         return None
    
#     try:
#         return HuggingFaceEndpoint(
#             repo_id=HUGGINGFACE_REPO_ID,
#             task="text-generation",
#             temperature=0.3,
#             model_kwargs={"token": HF_TOKEN, "max_length": 256}
#         )
#     except Exception as e:
#         st.error(f"⚠️ Error loading LLM: {str(e)}")
#         return None

# def set_custom_prompt():
#     """Defines the chatbot's behavior with a custom prompt template."""
#     return PromptTemplate(
#         template="""
#         You are an SEO chatbot with advanced knowledge. Answer based **strictly** on the provided documents.
        
#         If the answer is in the context, provide a **clear, professional, and concise** response with sources.  
#         If the question is **outside the given context**, politely decline:
        
#         **"I'm sorry, but I can only provide answers based on the available documents."**
        
#         **Context:** {context}  
#         **Question:** {question}  
        
#         **Answer:**  
#         """,
#         input_variables=["context", "question"]
#     )

# def generate_response(prompt, vectorstore, llm):
#     """Retrieves relevant documents and generates a response from the LLM."""
#     if not vectorstore or not llm:
#         return "❌ Unable to process your request due to initialization issues."
    
#     try:
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
#             return_source_documents=True,
#             chain_type_kwargs={'prompt': set_custom_prompt()}
#         )
        
#         response_data = qa_chain.invoke({'query': prompt})
#         result = response_data.get("result", "")
#         source_documents = response_data.get("source_documents", [])

#         if not result or not source_documents:
#             return "❌ Sorry, but I can only provide answers based on the available documents."

#         formatted_sources = "\n\n📚 **Sources:**" + "".join(
#             [f"\n- {doc.metadata.get('source', 'Unknown')} (Page: {doc.metadata.get('page', 'N/A')})" for doc in source_documents]
#         )
#         return f"{result}{formatted_sources}"

#     except Exception as e:
#         return f"⚠️ **Error:** {str(e)}"

# def main():
#     """Runs the Streamlit chatbot application."""
#     st.title("🧠 Brainmines SEO Chatbot - Your AI Assistant for SEO Queries 🚀")

#     # ✅ Load vector store and LLM
#     vectorstore = get_vectorstore()
#     llm = load_llm()

#     if not vectorstore or not llm:
#         st.error("⚠️ Failed to initialize vector store or LLM. Please check configurations.")
#         return
    
#     # ✅ Initialize session state
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "Hello! 👋 I'm here to assist you with SEO-related queries. 🚀"},
#         ]
    
#     # ✅ Display chat history
#     for message in st.session_state.messages:
#         st.chat_message(message["role"]).markdown(message["content"])
    
#     prompt = st.chat_input("💬 Enter your SEO question here")

#     if prompt:
#         st.chat_message("user").markdown(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         with st.spinner("Thinking... 🤔"):
#             response = generate_response(prompt, vectorstore, llm)

#         st.chat_message("assistant").markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

# if __name__ == "__main__":
#     main()



####################################### Version 2 ##########################################################3

# import os
# import streamlit as st
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEndpoint
# from dotenv import load_dotenv, find_dotenv

# # ✅ Load environment variables
# load_dotenv(find_dotenv())

# # ✅ FAISS Database Path
# DB_FAISS_PATH = "vectorstore/db_faiss"

# @st.cache_resource
# def get_vectorstore():
#     """Loads the FAISS vector store with embeddings."""
#     try:
#         embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#         return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
#     except Exception as e:
#         st.error(f"⚠️ Error loading vector store: {str(e)}")
#         return None

# @st.cache_resource
# def load_llm():
#     """Loads the Hugging Face LLM model for text generation."""
#     HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
#     HF_TOKEN = os.getenv("HF_TOKEN")
    
#     if not HF_TOKEN:
#         st.error("⚠️ Hugging Face API token is missing. Please check your environment variables.")
#         return None
    
#     try:
#         return HuggingFaceEndpoint(
#             repo_id=HUGGINGFACE_REPO_ID,
#             task="text-generation",
#             temperature=0.3,
#             model_kwargs={"token": HF_TOKEN, "max_length": 512}  # Increased max_length for detailed responses
#         )
#     except Exception as e:
#         st.error(f"⚠️ Error loading LLM: {str(e)}")
#         return None

# def set_custom_prompt():
#     """Defines the chatbot's behavior with a custom prompt template."""
#     return PromptTemplate(
#         template="""
#         You are an advanced SEO chatbot with expertise in search engine optimization. Answer strictly based on the provided documents.
        
#         If the answer is in the context, provide a clear, professional, and concise response. Include actionable insights and examples where applicable.
#         If the question is outside the given context, politely decline with the following message:
        
#         "I'm sorry, but I can only provide answers based on the available documents."
        
#         If the question is ambiguous or incomplete, ask clarifying questions to better understand the user's intent.
        
#         **Context:** {context}  
#         **Question:** {question}  
        
#         **Answer:**  
#         """,
#         input_variables=["context", "question"]
#     )

# def generate_response(prompt, vectorstore, llm):
#     """Retrieves relevant documents and generates a response from the LLM."""
#     if not vectorstore or not llm:
#         return "❌ Unable to process your request due to initialization issues."
    
#     try:
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=vectorstore.as_retriever(search_kwargs={'k': 5}),  # Increased k for richer context
#             return_source_documents=True,
#             chain_type_kwargs={'prompt': set_custom_prompt()}
#         )
        
#         response_data = qa_chain.invoke({'query': prompt})
#         result = response_data.get("result", "")
#         source_documents = response_data.get("source_documents", [])
        
#         # Check if the result is meaningful
#         if not result.strip() or "I'm sorry, but I can only provide answers based on the available documents." in result:
#             return "❌ Sorry, I couldn't find relevant information in the provided documents."
        
#         # Format unique sources
#         unique_sources = set()
#         formatted_sources = "\n\n📚 **Sources:**\n"
#         for doc in source_documents:
#             source = f"- {doc.metadata.get('source', 'Unknown')} (Page: {doc.metadata.get('page', 'N/A')})"
#             if source not in unique_sources:
#                 unique_sources.add(source)
#                 formatted_sources += f"{source}\n"
        
#         return f"{result}\n{formatted_sources}"
#     except Exception as e:
#         return f"⚠️ **Error:** {str(e)}"

# def main():
#     """Runs the Streamlit chatbot application."""
#     # Use columns to align the logo and title
#     col1, col2 = st.columns([3, 7])  # Adjust column widths as needed
    
#     with col1:
#         # Add a small logo at the top-left corner
#         st.image("logo2.jpg", caption=None, use_container_width=True)  # Updated to use_container_width
    
#     with col2:
#         # Add the app title next to the logo
#         st.title("🧠 Brainmines SEO Chatbot  Your AI Assistant for SEO Queries 🚀")
    
#     # ✅ Load vector store and LLM
#     vectorstore = get_vectorstore()
#     llm = load_llm()
#     if not vectorstore or not llm:
#         st.error("⚠️ Failed to initialize vector store or LLM. Please check configurations.")
#         return
    
#     # ✅ Initialize session state
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "Hello! 👋 I'm here to assist you with SEO-related queries. 🚀"},
#         ]
    
#     # ✅ Display chat history
#     for message in st.session_state.messages:
#         st.chat_message(message["role"]).markdown(message["content"])
    
#     prompt = st.chat_input("💬 Enter your SEO question here")
#     if prompt:
#         st.chat_message("user").markdown(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         with st.spinner("Thinking... 🤔"):
#             response = generate_response(prompt, vectorstore, llm)
        
#         st.chat_message("assistant").markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

# if __name__ == "__main__":
#     main()



############################################## new #######################################################



import os
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# FAISS Database Path
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
            max_new_tokens=2048,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            top_p=0.9
        )
    except Exception as e:
        st.error(f"⚠️ Error loading LLM: {str(e)}")
        return None

def set_custom_prompt():
    """Defines the chatbot's behavior with strict context usage and formatting instructions."""
    return PromptTemplate(
        template="""
        You are an advanced SEO chatbot. Provide answers based **exclusively** on the provided context.
        Format the answer according to the context structure:
        - If the context is a list, use numbered points (1., 2., etc.).
        - If the context is a table, use markdown table format.
        - If the context is a paragraph, present it as plain text.
        
        **Do not include any information outside the provided context.**
        
        **Context:** {context}  
        **Question:** {question}  
        
        **Answer:**  
        """,
        input_variables=["context", "question"]
    )

def generate_response(prompt, vectorstore, llm):
    """Generates responses with proper formatting and conditional source display."""
    if not vectorstore or not llm:
        return "❌ Unable to process your request due to initialization issues."
    
    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={'k': 5}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': set_custom_prompt()}
        )
        
        response_data = qa_chain.invoke({'query': prompt})
        result = response_data.get("result", "").strip()
        source_documents = response_data.get("source_documents", [])
        
        # Check for decline messages (no relevant context found)
        if "I'm sorry" in result or "I can only provide answers based on the available documents" in result:
            return result
        
        # Format sources with unique tracking
        sources = []
        seen_sources = set()
        for doc in source_documents:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', None)
            slide = doc.metadata.get('slide', None)
            location = f"Slide: {slide}" if slide else f"Page: {page}" if page else "N/A"
            source_str = f"{source} ({location})" if location != "N/A" else source
            
            if source_str not in seen_sources:
                seen_sources.add(source_str)
                sources.append(f"- {source_str}")
        
        formatted_sources = f"\n\n---\n📚 **Sources:**\n" + "\n".join(sources) if sources else ""
        
        return f"{result}{formatted_sources}"
    
    except Exception as e:
        return f"⚠️ **Error:** {str(e)}"

def main():
    """Runs the Streamlit chatbot application with enhanced UI."""
    # Use columns to align the logo and title
    col1, col2 = st.columns([3, 7])
    
    with col1:
        st.image("logo2.jpg", caption=None, use_container_width=True)
    
    with col2:
        st.markdown("<h1 style='font-size: 3rem; padding-left: 1rem;'>"
                    "🧠 Brainmines SEO Chatbot - Your AI Assistant for SEO Queries 🚀</h1>",
                    unsafe_allow_html=True)
    
    # Load vector store and LLM
    vectorstore = get_vectorstore()
    llm = load_llm()
    if not vectorstore or not llm:
        st.error("⚠️ Failed to initialize vector store or LLM. Please check configurations.")
        return
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm here to assist you with SEO-related queries. 🚀"},
        ]
    
    # Display chat history
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


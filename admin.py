
# import streamlit as st
# import os
# from PIL import Image
# import cv2
# import pytesseract
# from docx import Document
# from pptx import Presentation
# from io import BytesIO
# import pandas as pd
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.schema import Document as LangchainDocument
# from dotenv import load_dotenv, find_dotenv
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Load environment variables
# load_dotenv(find_dotenv())

# # Paths
# UPLOAD_FOLDER = 'data/'
# DB_FAISS_PATH = "vectorstore/db_faiss"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set Tesseract OCR Path
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Rupesh Shinde\\Tesseract\\tesseract.exe"

# # Function to extract text from images
# def extract_text_from_image(image_path):
#     try:
#         img = cv2.imread(str(image_path))
#         if img is None:
#             logging.error(f"Failed to read image: {image_path}")
#             return ""
#         return pytesseract.image_to_string(img).strip()
#     except Exception as e:
#         logging.error(f"Error during OCR for {image_path}: {e}")
#         return ""

# # Function to load and vectorize documents
# def vectorize_documents():
#     logging.info("Starting document vectorization...")
#     documents = []

#     # Load PDFs
#     pdf_loader = DirectoryLoader(UPLOAD_FOLDER, glob="*.pdf", loader_cls=PyPDFLoader)
#     documents.extend(pdf_loader.load())

#     # Load DOCX files
#     for file in Path(UPLOAD_FOLDER).glob("*.docx"):
#         doc = Document(file)
#         text = "\n".join([para.text for para in doc.paragraphs])
#         documents.append(LangchainDocument(page_content=text, metadata={"source": file.name}))

#     # Load PPTX files
#     for file in Path(UPLOAD_FOLDER).glob("*.pptx"):
#         prs = Presentation(file)
#         for i, slide in enumerate(prs.slides):
#             text = "\n".join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
#             if text.strip():
#                 documents.append(LangchainDocument(page_content=text, metadata={"source": file.name, "slide": i + 1}))

#     # Load images (JPG and PNG)
#     for image_file in Path(UPLOAD_FOLDER).rglob("*.jpg"):
#         text = extract_text_from_image(image_file)
#         if text:
#             documents.append(LangchainDocument(page_content=text, metadata={"source": image_file.name}))

#     for image_file in Path(UPLOAD_FOLDER).rglob("*.png"):
#         text = extract_text_from_image(image_file)
#         if text:
#             documents.append(LangchainDocument(page_content=text, metadata={"source": image_file.name}))

#     if documents:
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#         text_chunks = text_splitter.split_documents(documents)
#         embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         db = FAISS.from_documents(text_chunks, embedding_model)
#         db.save_local(DB_FAISS_PATH)
#         logging.info("Vector store updated successfully!")
#         return True  # Return success status
#     else:
#         logging.info("No new documents to vectorize.")
#         return False  # Return failure status

# # Function to handle file uploads
# def upload_files():
#     st.subheader("Upload Files")
#     uploaded_files = st.file_uploader(
#         "Choose files", type=["pdf", "docx", "pptx", "jpg", "png", "txt"], accept_multiple_files=True
#     )
#     if uploaded_files:
#         progress_bar = st.progress(0)
#         total_files = len(uploaded_files)
#         for i, uploaded_file in enumerate(uploaded_files):
#             file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             progress_bar.progress((i + 1) / total_files)
#             st.success(f"✅ {uploaded_file.name} uploaded successfully! ({i + 1}/{total_files})")

#         # Start vectorization
#         st.info("Vectorization started. Please wait...")
#         with st.spinner("Processing documents..."):
#             success = vectorize_documents()  # Run vectorization in the main thread
#         if success:
#             st.success("✅ Vector store updated successfully!")
#         else:
#             st.info("No new documents to vectorize.")

# # Function to display and manage uploaded files
# def manage_files():
#     st.subheader("Manage Files")
#     files = os.listdir(UPLOAD_FOLDER)
#     if files:
#         file_data = [
#             {
#                 "File Name": file,
#                 "Type": file.split(".")[-1].upper(),
#                 "Size (KB)": round(os.path.getsize(os.path.join(UPLOAD_FOLDER, file)) / 1024, 2),
#             }
#             for file in files
#         ]
#         df = pd.DataFrame(file_data)
#         st.dataframe(df, use_container_width=True)
#         selected_file = st.selectbox("Select a file to manage", files)
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Delete Selected File"):
#                 os.remove(os.path.join(UPLOAD_FOLDER, selected_file))
#                 st.error(f"❌ {selected_file} deleted successfully!")
#                 st.rerun()
#         with col2:
#             with open(os.path.join(UPLOAD_FOLDER, selected_file), "rb") as f:
#                 st.download_button(
#                     label="Download Selected File",
#                     data=f,
#                     file_name=selected_file,
#                     mime="application/octet-stream",
#                 )
#     else:
#         st.info("No files uploaded yet.")

# # Function to handle login
# def login():
#     st.sidebar.subheader("Login")
#     username = st.sidebar.text_input("Username")
#     password = st.sidebar.text_input("Password", type="password")
#     if st.sidebar.button("Login"):
#         with st.spinner("Logging in..."):  # Show a spinner during login
#             if username == "admin" and password == "secret":
#                 st.session_state.logged_in = True
#                 st.sidebar.success("You are logged in!")
#                 st.rerun()
#             else:
#                 st.sidebar.error("Invalid credentials.")

# # Function to handle logout
# def logout():
#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.sidebar.success("You have been logged out!")
#         st.rerun()

# # Main function to run the app
# def main():
#     st.title("Admin Panel")
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         login()
#         st.stop()

#     logout()
#     upload_files()
#     manage_files()

# if __name__ == "__main__":
#     main()




import streamlit as st
import os
from PIL import Image
import cv2
import pytesseract
from docx import Document
from pptx import Presentation
from io import BytesIO
import pandas as pd
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document as LangchainDocument
from dotenv import load_dotenv, find_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(find_dotenv())

# Paths
UPLOAD_FOLDER = 'data/'
DB_FAISS_PATH = "vectorstore/db_faiss"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set Tesseract OCR Path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Rupesh Shinde\\Tesseract\\tesseract.exe"

# Function to extract text from images
def extract_text_from_image(image_path):
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            logging.error(f"Failed to read image: {image_path}")
            return ""
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        logging.error(f"Error during OCR for {image_path}: {e}")
        return ""

# Function to load and vectorize documents
def vectorize_documents():
    logging.info("Starting document vectorization...")
    documents = []

    # Load PDFs
    pdf_loader = DirectoryLoader(UPLOAD_FOLDER, glob="*.pdf", loader_cls=PyPDFLoader)
    documents.extend(pdf_loader.load())

    # Load DOCX files
    for file in Path(UPLOAD_FOLDER).glob("*.docx"):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        documents.append(LangchainDocument(page_content=text, metadata={"source": file.name}))

    # Load PPTX files
    for file in Path(UPLOAD_FOLDER).glob("*.pptx"):
        prs = Presentation(file)
        for i, slide in enumerate(prs.slides):
            text = "\n".join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
            if text.strip():
                documents.append(LangchainDocument(page_content=text, metadata={"source": file.name, "slide": i + 1}))

    # Load images (JPG and PNG)
    for image_file in Path(UPLOAD_FOLDER).rglob("*.jpg"):
        text = extract_text_from_image(image_file)
        if text:
            documents.append(LangchainDocument(page_content=text, metadata={"source": image_file.name}))

    for image_file in Path(UPLOAD_FOLDER).rglob("*.png"):
        text = extract_text_from_image(image_file)
        if text:
            documents.append(LangchainDocument(page_content=text, metadata={"source": image_file.name}))

    if documents:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_documents(documents)
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(text_chunks, embedding_model)
        db.save_local(DB_FAISS_PATH)
        logging.info("Vector store updated successfully!")
        return True  # Return success status
    else:
        logging.info("No new documents to vectorize.")
        return False  # Return failure status

# Function to handle file uploads
def upload_files():
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files", type=["pdf", "docx", "pptx", "jpg", "png", "txt"], accept_multiple_files=True
    )
    if uploaded_files:
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)
        successful_uploads = 0

        for i, uploaded_file in enumerate(uploaded_files):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            # Check if the file already exists
            if os.path.exists(file_path):
                st.warning(f"⚠️ File '{uploaded_file.name}' already exists. Skipping upload.")
                continue

            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            successful_uploads += 1
            progress_bar.progress((i + 1) / total_files)
            st.success(f"✅ {uploaded_file.name} uploaded successfully! ({successful_uploads}/{total_files})")

        if successful_uploads > 0:
            # Start vectorization
            st.info("Vectorization started. Please wait...")
            with st.spinner("Processing documents..."):
                success = vectorize_documents()  # Run vectorization in the main thread
            if success:
                st.success("✅ Vector store updated successfully!")
            else:
                st.info("No new documents to vectorize.")
        else:
            st.info("No new files were uploaded.")

# Function to display and manage uploaded files
def manage_files():
    st.subheader("Manage Files")
    files = os.listdir(UPLOAD_FOLDER)
    if files:
        file_data = [
            {
                "File Name": file,
                "Type": file.split(".")[-1].upper(),
                "Size (KB)": round(os.path.getsize(os.path.join(UPLOAD_FOLDER, file)) / 1024, 2),
            }
            for file in files
        ]
        df = pd.DataFrame(file_data)
        st.dataframe(df, use_container_width=True)
        selected_file = st.selectbox("Select a file to manage", files)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete Selected File"):
                os.remove(os.path.join(UPLOAD_FOLDER, selected_file))
                st.error(f"❌ {selected_file} deleted successfully!")
                st.rerun()
        with col2:
            with open(os.path.join(UPLOAD_FOLDER, selected_file), "rb") as f:
                st.download_button(
                    label="Download Selected File",
                    data=f,
                    file_name=selected_file,
                    mime="application/octet-stream",
                )
    else:
        st.info("No files uploaded yet.")

# Function to handle login
def login():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        with st.spinner("Logging in..."):  # Show a spinner during login
            if username == "admin" and password == "secret":
                st.session_state.logged_in = True
                st.sidebar.success("You are logged in!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials.")

# Function to handle logout
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.sidebar.success("You have been logged out!")
        st.rerun()

# Main function to run the app
def main():
    st.title("Admin Panel")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login()
        st.stop()
    logout()
    upload_files()
    manage_files()

if __name__ == "__main__":
    main()

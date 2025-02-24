# import streamlit as st
# import os
# from PIL import Image
# import cv2
# import pytesseract
# from docx import Document
# from pptx import Presentation
# from io import BytesIO
# import base64
# from zipfile import ZipFile
# import pandas as pd

# # Set the path where uploaded files will be stored
# UPLOAD_FOLDER = 'data/'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Function to handle login
# def login():
#     st.subheader("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if username == "admin" and password == "secret":
#         st.success("You are logged in!")
#         return True
#     else:
#         st.error("Invalid credentials.")
#         return False

# # Function to handle file uploads
# def upload_files():
#     st.subheader("Upload Files")
#     uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "pptx", "jpg", "png", "txt"], accept_multiple_files=True)
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success(f"{uploaded_file.name} uploaded successfully!")

# # Main function to run the app
# def main():
#     st.title("Admin Panel")
    
#     # Check if user is logged in
#     if not login():
#         st.stop()
    
#     # Display uploaded files (optional)
#     files = os.listdir(UPLOAD_FOLDER)
#     st.write("Uploaded Files:")
#     for file in files:
#         st.write(file)
    
#     # Upload files
#     upload_files()

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
import base64
from zipfile import ZipFile
import pandas as pd


# Set the path where uploaded files will be stored
UPLOAD_FOLDER = 'data/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to handle login
def login():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "secret":
            st.session_state.logged_in = True  # Set login state to True
            st.sidebar.success("You are logged in!")
            st.rerun()  # Rerun the app to refresh the page
        else:
            st.sidebar.error("Invalid credentials.")

# Function to handle logout
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False  # Reset login state
        st.sidebar.success("You have been logged out!")
        st.rerun()  # Rerun the app to refresh the page

# Function to handle file uploads
def upload_files():
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "pptx", "jpg", "png", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")  # Green success alert
        st.rerun()  # Rerun the app to refresh the file list

# Function to display and manage uploaded files
def manage_files():
    st.subheader("Manage Files")
    files = os.listdir(UPLOAD_FOLDER)
    
    if files:
        # Create a DataFrame for all files
        file_data = []
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            file_type = file.split(".")[-1].upper()  # Extract file extension
            file_data.append({"File Name": file, "Type": file_type, "Size (KB)": round(file_size, 2)})
        
        df = pd.DataFrame(file_data)
        
        # Display the table
        st.dataframe(df, use_container_width=True)
        
        # Add options to delete or download files
        selected_file = st.selectbox("Select a file to manage", files)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete Selected File"):
                os.remove(os.path.join(UPLOAD_FOLDER, selected_file))
                st.error(f"❌ {selected_file} deleted successfully!")  # Red error alert
                st.rerun()  # Rerun the app to refresh the file list
        with col2:
            with open(os.path.join(UPLOAD_FOLDER, selected_file), "rb") as f:
                st.download_button(
                    label="Download Selected File",
                    data=f,
                    file_name=selected_file,
                    mime="application/octet-stream"
                )
    else:
        st.info("No files uploaded yet.")

# Main function to run the app
def main():
    st.title("Admin Panel")
    
    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login()
        st.stop()  # Stop the app if not logged in
    
    # Logout button
    logout()
    
    # Upload files
    upload_files()
    
    # Manage files (table for all files)
    manage_files()

if __name__ == "__main__":
    main()

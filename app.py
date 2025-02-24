import streamlit as st

PAGES = {
    "Chat": "final.py",
    "Admin": "admin.py"
}

def main():
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    if page == PAGES["Chat"]:
        import final
        final.main()
    elif page == PAGES["Admin"]:
        import admin
        admin.main()

if __name__ == "__main__":
    main()
import streamlit as st


# Basic html to change background
class Background:
    def place():
        st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://images.unsplash.com/photo-1557682250-33bd709cbe85?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8cHVycGxlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHw%3D&w=1000&q=80");
                    background-attachment: fixed;
                    background-size: cover;
                    background-opacity: 0.5;
                }}
                </style>
                """,
                unsafe_allow_html = True
        )

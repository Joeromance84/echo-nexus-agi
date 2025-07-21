import streamlit as st

st.title("Test App")
st.write("Hello World")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    st.write(f"File: {uploaded_file.name}")
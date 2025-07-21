import streamlit as st

st.title("Debug Test - No Redirects")
st.write("This is a minimal debug test.")
st.write("If you see this, the app is working correctly.")
st.write("Current URL should be localhost:8502")

if st.button("Test Button"):
    st.success("Button clicked - no redirects!")

st.text_input("Test input:")
st.selectbox("Test dropdown:", ["Option 1", "Option 2"])
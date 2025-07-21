import streamlit as st

# Minimal clean app - no redirects possible
st.title("🧪 Minimal Clean Test - Port 8504")
st.write("This is a completely minimal test with no redirects.")
st.write("URL should be localhost:8504")

st.success("✅ If you see this, the app is working correctly!")

st.write("---")
st.write("Browser debug info:")
st.write(f"Current page: {st.query_params}")

if st.button("Test Button"):
    st.balloons()
    st.success("Button works - no redirects!")
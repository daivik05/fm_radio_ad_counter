import streamlit as st
import requests

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")

st.title("Audio File Processing")
uploaded_file = st.file_uploader("Upload an Audio File", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.markdown("### Uploaded File Details:")
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**File Type:** {uploaded_file.type}")
    st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
    st.markdown("### Audio Preview:")
    st.audio(uploaded_file, format=uploaded_file.type)

    # Send the file to the Flask API
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://127.0.0.1:5000/upload", files=files)

    if response.status_code == 200:
        result = response.json()
        st.write(f"**Status:** {result['status']}")
    else:
        st.error("Failed to process the file. Please try again.")
else:
    st.warning("Please upload an audio file to proceed.")

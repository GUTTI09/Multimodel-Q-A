import os

import streamlit as st
from dotenv import load_dotenv

from models.Direct_vison_model import ask_image_question, encode_uploaded_file

load_dotenv(override=True)

st.set_page_config(page_title="Vision Chat Assistant", layout="wide")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("API key not found in your .env file. Please add GEMINI_API_KEY or OPENAI_API_KEY.")
    st.stop()

is_gemini = API_KEY.startswith("AQ.") or API_KEY.startswith("AIza")
provider_name = "Google Gemini (gemini-3.8-flash)" if is_gemini else "OpenAI (gpt-4o-mini)"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "image_b64" not in st.session_state:
    st.session_state.image_b64 = None
if "mime_type" not in st.session_state:
    st.session_state.mime_type = "image/png"
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

st.markdown(f"""
# 🖼️ Visual Q&A Assistant
Upload an image and ask questions about what is visible in it.  
*Powered by {provider_name}*
""")

left_col, right_col = st.columns([1.15, 1], gap="large")

with left_col:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"], key="uploader")

    if uploaded_file is not None:
        st.session_state.image_b64 = encode_uploaded_file(uploaded_file)
        st.session_state.mime_type = uploaded_file.type or "image/png"
        st.session_state.uploaded_filename = uploaded_file.name

    if st.session_state.uploaded_filename:
        st.success(f"Uploaded: {st.session_state.uploaded_filename}")

    st.markdown("---")
    st.subheader("🖼️ Image Preview")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    elif st.session_state.image_b64:
        st.info("Image uploaded. Ask a question in the conversation panel.")
    else:
        st.info("Upload an image to preview it here.")

with right_col:
    st.subheader("💬 Conversation")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.chat_history:
            st.info("Your questions and answers will appear here.")
        else:
            for item in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.write(item["question"])
                with st.chat_message("assistant"):
                    st.write(item["answer"])

    question = st.chat_input("Ask a question about the uploaded image...")

    if question:
        if not st.session_state.image_b64:
            st.error("Please upload an image first.")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    answer = ask_image_question(
                        question=question,
                        image_b64=st.session_state.image_b64,
                        mime_type=st.session_state.mime_type,
                        api_key=API_KEY,
                    )

                    st.session_state.chat_history.append({"question": question, "answer": answer})
                    st.rerun()
                except Exception as exc:
                    st.error(f"Error: {exc}")

import os

import streamlit as st
from dotenv import load_dotenv

from models.caption_model import generate_caption
from models.vqa_model import get_vqa_answer, normalize_vqa_answer
from utils.image_utils import prepare_image

load_dotenv(override=True)

st.set_page_config(page_title="Multi-Modal Q&A Assistant", layout="centered")

HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in your .env file.")
    st.stop()

if not HF_TOKEN:
    st.warning("HF_TOKEN not found in .env file. The app will still run with the OpenAI-powered fallback image chat.")

st.title("🖼️ Multi-Modal Q&A Assistant")
st.write("Upload an image, then ask a question about it.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = prepare_image(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")

    if "last_uploaded_name" not in st.session_state or st.session_state.last_uploaded_name != uploaded_file.name:
        st.session_state.last_uploaded_name = uploaded_file.name
        st.session_state.image = image
        st.session_state.caption = generate_caption(image)
        st.session_state.chat_history = []

    st.subheader("Image Description")
    st.success(st.session_state.caption)

    user_question = st.text_input("Ask a question about the image:")

    if st.button("Get Answer"):
        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing image and generating answer..."):
                raw_vqa_answer = get_vqa_answer(st.session_state.image, user_question)
                normalized_vqa_answer = normalize_vqa_answer(raw_vqa_answer)
                final_answer = (
                    f"Caption: {st.session_state.caption}\n"
                    f"Question: {user_question}\n"
                    f"Visual answer: {normalized_vqa_answer or 'No specific answer generated.'}"
                )
                st.session_state.chat_history.append({"question": user_question, "answer": final_answer})

    if st.session_state.chat_history:
        st.subheader("Conversation")
        for idx, item in enumerate(st.session_state.chat_history, start=1):
            st.markdown(f"**Q{idx}:** {item['question']}")
            st.markdown(f"**A{idx}:** {item['answer']}")
            st.markdown("---")

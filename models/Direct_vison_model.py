import base64
import io
import warnings

from PIL import Image

warnings.filterwarnings("ignore", category=FutureWarning)


def encode_uploaded_file(uploaded_file) -> str:
    """Turn a Streamlit upload object into a data URL for Vision input."""
    file_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or "image/png"
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def ask_image_question(question: str, image_b64: str, mime_type: str = "image/png", api_key: str = None) -> str:
    """Ask a question about the uploaded image using Google Gemini or OpenAI Vision API."""
    if not api_key:
        raise ValueError("API key is missing. Add GEMINI_API_KEY or OPENAI_API_KEY to your .env file.")

    # Check if key is for Google Gemini (starts with AQ. or AIza)
    if api_key.startswith("AQ.") or api_key.startswith("AIza"):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Decode base64 to PIL Image
        if image_b64.startswith("data:"):
            _, b64_data = image_b64.split(",", 1)
        else:
            b64_data = image_b64
        image_bytes = base64.b64decode(b64_data)
        pil_image = Image.open(io.BytesIO(image_bytes))

        response = model.generate_content([pil_image, question])
        return response.text.strip()

    # Otherwise use OpenAI
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_b64 if image_b64.startswith("data:") else f"data:{mime_type};base64,{image_b64}"
                        },
                    },
                ],
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

# 🖼️ Multi-Modal Visual Q&A Assistant

An AI-powered web application that lets users upload images and ask questions about them in natural language. Built with **Python**, **Streamlit**, and **Google Gemini 3.8 Flash**.

## ✨ Features

- 📤 Upload images (PNG, JPG, JPEG, WebP)
- 💬 Chat-style conversation — ask multiple questions about the same image
- 🔄 Dual AI provider support (Google Gemini & OpenAI)
- 🧠 Multi-modal AI — understands both images and text simultaneously
- 🗑️ Clear conversation history with one click
- ⚡ Fast responses powered by Gemini Flash

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web UI framework |
| Google Gemini API (gemini-3.8-flash) | Multi-modal vision + language model |
| OpenAI API (gpt-4o-mini) | Alternative vision model |
| Pillow (PIL) | Image processing & format conversion |
| Base64 | Image encoding for API transmission |
| python-dotenv | Secure API key management |

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API key ([Get free key here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GUTTI09/Multimodel-Q-A.git
   cd Multimodel-Q-A
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   > You can also use OpenAI instead:
   > ```env
   > OPENAI_API_KEY=your_openai_api_key_here
   > ```

4. **Run the application**
   ```bash
   streamlit run app2.py
   ```

5. Open your browser at `http://localhost:8501`

## 📁 Project Structure

```
Multimodel-Q-A/
├── app.py                     # App v1 — Caption + VQA pipeline
├── app2.py                    # App v2 — Direct vision model (main app)
├── .env                       # API keys (not tracked in git)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── models/
│   ├── __init__.py
│   ├── Direct_vison_model.py  # Core vision API logic (Gemini / OpenAI)
│   ├── caption_model.py       # Image captioning module
│   ├── vqa_model.py           # Visual Question Answering module
│   └── llm_answer.py          # LLM answer formatting
└── utils/
    └── image_utils.py         # Image preprocessing utilities
```

## 💡 How It Works

```
User uploads image  →  Base64 encoding  →  User asks a question
                                                    ↓
                                           Image + Question sent
                                            to Gemini / OpenAI
                                                    ↓
                                            AI analyzes image
                                           and generates answer
                                                    ↓
                                          Answer displayed in chat
```

1. User uploads an image through the Streamlit web interface
2. The image is converted to Base64 format for API transmission
3. User types a natural language question about the image
4. The encoded image and question are sent to Google Gemini (or OpenAI)
5. The multi-modal AI model analyzes the image content and generates an answer
6. The answer is displayed in a chat-style conversation interface

## 🔧 Configuration

The app automatically detects which AI provider to use based on the API key format:

| Key Prefix | Provider | Model |
|---|---|---|
| `AQ.` or `AIza` | Google Gemini | gemini-3.8-flash |
| `sk-` | OpenAI | gpt-4o-mini |

## 📌 Use Cases

- **Accessibility** — Helping visually impaired users understand images
- **Education** — Students asking questions about diagrams and charts
- **E-commerce** — Customers inquiring about product details from photos
- **Content Analysis** — Analyzing and extracting information from images

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

# Hurix Chat LLM App

A Streamlit-based chat application with ChatGPT-like UI, Google OAuth (hurix.com only), document upload, chat history, and support for multiple LLMs (ChatGPT, Claude, etc.).

## Features
- Google login (hurix.com domain only)
- ChatGPT-style UI with chat history, new chat, and delete chat
- Upload documents (PDF, DOCX, TXT) to use as context
- Switch between LLMs (ChatGPT, Claude, versions)
- All chats/messages stored in MongoDB

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set up a `.env` file (see `.env.example`)
4. Run: `streamlit run app.py`

## Environment Variables
- `MONGODB_URI`: MongoDB connection string
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Google OAuth credentials
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`: LLM API keys

## Usage
- Log in with your hurix.com Google account
- Start new chats, upload documents, and interact with LLMs
- All chat history is saved and can be managed from the sidebar 
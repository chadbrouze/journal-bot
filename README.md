# Alv - Your Journal AI

A simple local journal interface that lets you talk to your journal entries by month.

## Setup

1. Install Ollama from https://ollama.ai/
2. Pull the Llama model: `ollama pull llama3.1:8b`
3. Install requirements: `pip install -r requirements.txt`
4. Add your journal files (format: YYYY-MM.md) to the `data/journals` directory
5. Run the app: `streamlit run app.py`

## Usage

1. Select the month you want to talk to
2. Type your message in the chat input
3. The AI will respond based on your journal entries for that month
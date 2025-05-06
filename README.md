# Alv - Your Journal AI

Talk to your journal entries using Tinfoil's private AI.

## Setup

1. Install: `pip install -r requirements.txt`
2. Add journal files (YYYY-MM.md) to `data/journals/`
3. Set up your Tinfoil API key (two options):
   - Create `.env` file with `TINFOIL_API_KEY=your_key`
   - Enter API key in the app interface
4. Run: `streamlit run app.py`

## Features

- **Multiple AI Models**: Choose between DeepSeek, Mistral, or Llama models
- **Customizable Settings**: Adjust token count, temperature, and system prompts
- **Private & Secure**: All processing happens through Tinfoil's secure enclave
- **Rich Context**: High token limits for analyzing large journal entries
- **Modern UI**: Clean interface with separate settings and chat panels

## Usage

1. Select your preferred model
2. Choose which months to analyze
3. Adjust settings if needed
4. Chat with your journal
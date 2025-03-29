import streamlit as st
import requests
import json
from utils import get_available_months, load_journal

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"  # Change to your preferred model

def get_response_from_ollama(prompt, context, system_prompt):
    """Get response from Ollama API"""
    # Use the system prompt as is, without adding multiple months context
    full_prompt = f"{system_prompt}\n\nHere are the journal entries:\n{context}\n\nUser: {prompt}\n\nAlv:"
    
    # Make request to Ollama API with increased context
    response = requests.post(
        OLLAMA_API,
        json={
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False,
            "context_length": 128000
        }
    )
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Alv - Your Journal")
    
    # Add system prompt configuration in sidebar
    with st.sidebar:
        default_prompt = "You are Alv, a personal AI journal companion. Respond as if you are the journal itself. Limit your answer to a few sentences."
        system_prompt = st.text_area(
            "Customize System Prompt",
            value=default_prompt,
            help="Customize how Alv behaves"
        )
    
    # Month selector - changed from multiselect to single select
    months = get_available_months()
    if not months:
        st.error("No journal files found. Please add .md files to the data/journals directory.")
        return
    
    selected_month = st.selectbox(
        "Select month to talk to (YYYY-MM format)", 
        months
    )
    
    # Load journal content for selected month
    journal_content = ""
    if selected_month:
        journal_content += f"\n\n=== {selected_month} ===\n\n"
        journal_content += load_journal(selected_month)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(
            message["role"],
            avatar="assets/alv.jpeg" if message["role"] == "assistant" else "assets/chad.jpeg"
        ):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Talk to your journal...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="assets/chad.jpeg"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant", avatar="assets/alv.jpeg"):
            with st.spinner("woofing..."):
                response = get_response_from_ollama(user_input, journal_content, system_prompt)
                st.write(response)
        
        # Add AI response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
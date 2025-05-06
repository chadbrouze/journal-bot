import streamlit as st
import os
from utils import get_available_months, load_journal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TINFOIL_API_KEY = os.getenv("TINFOIL_API_KEY")

try:
    from tinfoil import TinfoilAI
    client = TinfoilAI(
        enclave="llama3-3-70b-p.model.tinfoil.sh",
        repo="tinfoilsh/confidential-llama3-3-70b-prod",
        api_key=TINFOIL_API_KEY
    )
    TINFOIL_AVAILABLE = True
except ImportError:
    TINFOIL_AVAILABLE = False

def main():
    st.set_page_config(page_title="Alv - Journal", page_icon="📖")
    st.title("Alv - Your Journal")
    
    # Sidebar
    with st.sidebar:
        # API key input if not in environment
        if not TINFOIL_API_KEY:
            api_key = st.text_input("Tinfoil API Key", type="password")
            if api_key:
                try:
                    # Recreate client with provided API key
                    global client
                    client = TinfoilAI(
                        enclave="llama3-3-70b-p.model.tinfoil.sh",
                        repo="tinfoilsh/confidential-llama3-3-70b-prod",
                        api_key=api_key
                    )
                    st.success("API key set")
                except Exception as e:
                    st.error(f"Error setting API key: {str(e)}")
        
        # Month selector
        months = get_available_months()
        if not months:
            st.error("No journal files found.")
            return
        
        selected_months = st.multiselect("Select months", months)
    
    # Load journal content
    journal_content = ""
    for month in selected_months:
        journal_content += f"\n\n=== {month} ===\n\n"
        journal_content += load_journal(month)
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        avatar = "assets/alv.jpeg" if message["role"] == "assistant" else "assets/chad.jpeg"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Talk to your journal...")
    
    if user_input and selected_months:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="assets/chad.jpeg"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant", avatar="assets/alv.jpeg"):
            with st.spinner("Thinking..."):
                if TINFOIL_AVAILABLE:
                    try:
                        system_msg = "You are Alv, a personal AI journal companion. Respond based on the journal entries provided."
                        
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": system_msg},
                                {"role": "user", "content": f"Journal entries:\n{journal_content}\n\nUser query: {user_input}"}
                            ],
                            model="llama3-3-70b",
                            max_tokens=8000
                        )
                        response = chat_completion.choices[0].message.content
                    except Exception as e:
                        response = f"Error: {str(e)}"
                else:
                    response = "Tinfoil not installed. Run: pip install tinfoil"
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif user_input and not selected_months:
        st.warning("Please select at least one month.")

if __name__ == "__main__":
    main()
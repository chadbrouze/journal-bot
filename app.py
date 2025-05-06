import streamlit as st
import os
from utils import get_available_months, load_journal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TINFOIL_API_KEY = os.getenv("TINFOIL_API_KEY")

# Model configurations
MODELS = {
    "DeepSeek-R1-70B": {
        "enclave": "deepseek-r1-70b-p.model.tinfoil.sh",
        "repo": "tinfoilsh/confidential-deepseek-r1-70b-prod",
        "model_name": "deepseek-r1-70b",
        "description": "High-performance reasoning model (70.6B parameters, 64k context)"
    },
    "Mistral Small 3.1 24B": {
        "enclave": "mistral-s-3-1-24b-p.model.tinfoil.sh",
        "repo": "tinfoilsh/confidential-mistral-small-3-1",
        "model_name": "mistral-small-3-1-24b",
        "description": "Advanced multimodal model (24B parameters, 128k context)"
    },
    "Llama 3.3 70B": {
        "enclave": "llama3-3-70b-p.model.tinfoil.sh",
        "repo": "tinfoilsh/confidential-llama3-3-70b-prod",
        "model_name": "llama3-3-70b",
        "description": "High-performance multilingual model (70B parameters, 64k context)"
    }
}

try:
    from tinfoil import TinfoilAI
    # We'll initialize the client based on model selection
    TINFOIL_AVAILABLE = True
except ImportError:
    TINFOIL_AVAILABLE = False

def create_tinfoil_client(api_key, model_key):
    """Create a TinfoilAI client for the selected model"""
    if not model_key or not api_key:
        return None
    
    model_config = MODELS[model_key]
    return TinfoilAI(
        enclave=model_config["enclave"],
        repo=model_config["repo"],
        api_key=api_key
    )

def main():
    st.set_page_config(
        page_title="Alv - Journal", 
        page_icon="📖",
        layout="wide"
    )
    
    # Define columns for main layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Settings")
        
        # API key input if not in environment
        if not TINFOIL_API_KEY:
            api_key = st.text_input("Tinfoil API Key", type="password")
        else:
            api_key = TINFOIL_API_KEY
            st.success("✓ API key loaded from environment")
        
        # Model selector
        selected_model = st.selectbox(
            "Select Model",
            options=list(MODELS.keys()),
            format_func=lambda x: x
        )
        
        if selected_model:
            st.caption(MODELS[selected_model]["description"])
        
        # Month selector
        st.subheader("Journal Selection")
        months = get_available_months()
        if not months:
            st.error("No journal files found.")
            return
        
        selected_months = st.multiselect("Select months", months)
        
        # Advanced settings in expandable section
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.7, 
                step=0.1,
                help="Higher values produce more creative responses"
            )
            
            system_prompt = st.text_area(
                "System Prompt",
                value="You are Alv, a personal AI journal companion. Respond based on the journal entries provided.",
                height=100
            )
    
    # Main content area
    with col2:
        st.title("Alv - Your Journal")
        
        # Load journal content
        journal_content = ""
        for month in selected_months:
            journal_content += f"\n\n=== {month} ===\n\n"
            journal_content += load_journal(month)
        
        # Chat container with custom styling
        chat_container = st.container(height=550, border=False)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        with chat_container:
            for message in st.session_state.messages:
                avatar = "assets/alv.jpeg" if message["role"] == "assistant" else "assets/chad.jpeg"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
        
        # User input
        user_input = st.chat_input("Talk to your journal...")
        
        if user_input and selected_months and api_key:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with chat_container:
                with st.chat_message("user", avatar="assets/chad.jpeg"):
                    st.markdown(user_input)
            
            # Get AI response
            with chat_container:
                with st.chat_message("assistant", avatar="assets/alv.jpeg"):
                    with st.spinner(f"Woofing with {selected_model}..."):
                        if TINFOIL_AVAILABLE:
                            try:
                                # Create client for selected model
                                client = create_tinfoil_client(api_key, selected_model)
                                
                                if client:
                                    # Get model name for API call
                                    model_name = MODELS[selected_model]["model_name"]
                                    
                                    chat_completion = client.chat.completions.create(
                                        messages=[
                                            {"role": "system", "content": system_prompt},
                                            {"role": "user", "content": f"Journal entries:\n{journal_content}\n\nUser query: {user_input}"}
                                        ],
                                        model=model_name,
                                        max_tokens=16000,
                                        temperature=temperature
                                    )
                                    response = chat_completion.choices[0].message.content
                                else:
                                    response = "Error: Failed to initialize Tinfoil client. Check your API key and selected model."
                            except Exception as e:
                                response = f"Error: {str(e)}"
                        else:
                            response = "Tinfoil not installed. Run: pip install tinfoil"
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
        
        elif user_input and not selected_months:
            st.warning("Please select at least one month.")
        elif user_input and not api_key:
            st.warning("Please provide a Tinfoil API key.")

if __name__ == "__main__":
    main()
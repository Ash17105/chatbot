import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv

# Load API key from .env (optional for local dev)
load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="💬 Gemini Chatbot", page_icon="🤖")

# App title and instructions
st.title("🤖 Gemini Chatbot")
st.write(
    "This chatbot uses **Google Gemini Pro** via LangChain. "
    "You can get your API key from [Google AI Studio](https://makersuite.google.com/app)."
)

# Input field for Google API Key
GOOGLE_API_KEY = st.text_input("🔑 Enter your Gemini API Key", type="password")

if not GOOGLE_API_KEY:
    st.info("Please enter your Gemini API key to begin chatting.", icon="🗝️")
else:
    # Initialize Gemini LLM using LangChain
    llm = ChatGoogleGenerativeAI(
    model="models/chat-bison-001",  # <-- change model here
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

    

    # Setup conversation memory and chain
    memory = ConversationBufferMemory(return_messages=True)
    chat_chain = ConversationChain(llm=llm, memory=memory)

    # Initialize chat history in session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("What would you like to ask?"):
        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant reply using Gemini
        with st.chat_message("assistant"):
            response = chat_chain.run(prompt)
            st.markdown(response)

        # Store assistant reply
        st.session_state.messages.append({"role": "assistant", "content": response})

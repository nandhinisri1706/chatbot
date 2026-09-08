import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Get Hugging Face token
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    HF_TOKEN = os.getenv("HF_TOKEN")

# Page configuration
st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="centered"
)

# App title
st.title("Nova AI")
st.caption("Your intelligent AI assistant")

# Check token
if not HF_TOKEN:
    st.error("Hugging Face token not configured.")
    st.stop()

# Hugging Face client
client = InferenceClient(
    api_key=HF_TOKEN,
    provider="groq"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.header("Options")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("Model")
    st.write("GPT-OSS 120B")

    st.write("Status")
    st.write("Online")


# Welcome screen
if len(st.session_state.messages) == 0:

    st.info("Welcome to Nova AI!")

    st.write("You can ask me anything.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Explain AI"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Explain Artificial Intelligence simply."
            })

            st.rerun()

        if st.button("Python Help"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Help me learn Python."
            })

            st.rerun()

    with col2:

        if st.button("Study Help"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Help me create a study plan."
            })

            st.rerun()

        if st.button("Project Ideas"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Give me some AI project ideas."
            })

            st.rerun()


# Display previous messages
for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    else:

        with st.chat_message("assistant"):
            st.write(message["content"])


# Chat input
user_input = st.chat_input("Type your message...")


if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                response = client.chat.completions.create(

                    model="openai/gpt-oss-120b",

                    messages=[
                        {
                            "role": "system",
                            "content": """
You are Nova AI, a helpful and friendly AI assistant.

Answer questions clearly and accurately.

If the user speaks Tamil or Tanglish,
reply naturally in Tamil or Tanglish.

If the user speaks English,
reply in English.

For programming questions,
give simple step-by-step explanations.

For student questions,
give practical and easy-to-understand answers.

Be concise but helpful.
"""
                        }
                    ] + st.session_state.messages,

                    max_tokens=1024,

                    temperature=0.7
                )

                # Get AI response
                answer = response.choices[0].message.content

                # Display response
                st.write(answer)

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception as e:

            st.error("Something went wrong.")

            st.write(str(e))

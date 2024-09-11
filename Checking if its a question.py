import streamlit as st
import random
import time

# Streamed response emulator for general responses
def response_generator():
    response = random.choice(
        [
            "Ask a question.",
            "Thats not a question.",
            "Questions only please!"
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.25)

# Function to check if the input is a question
def is_question(text):
    question_words = ["what", "why", "how", "when", "where", "who", "which", "whom", "whose"]
    text_lower = text.lower().strip()
    # Check if the input ends with a question mark or starts with a question word
    return text_lower.endswith("?") or any(text_lower.startswith(qw) for qw in question_words)

st.title("Simple Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if the user input is a question
    if is_question(prompt):
        assistant_response = "That is an excellent question! Let me think about it."
    else:
        # Generate a general response
        assistant_response = ""
        for word in response_generator():
            assistant_response += word
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

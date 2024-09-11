import streamlit as st
import random
import time

# Streamed response emulator for general responses
def response_generator():
    response = random.choice(
        [
            "Ask a question.",
            "That's not a question.",
            "Questions only, please!"
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.25)

# Function to check if the input is a question
def is_question(text):
    question_words = ["what", "why", "how", "when", "where", "who", "which", "whom", "whose"]
    text_lower = text.lower().strip()
    return text_lower.endswith("?") or any(text_lower.startswith(qw) for qw in question_words)
# Function to detect if the question is "how are you"
def is_how_are_you(text):
    patterns = [
        "how you", "how is it", "how are you", "how are you doing", "how's it going", "how are you doing today",
        "what's up", "how's life", "how have you been", "how's everything", "how are you feeling",
        "how do you do", "how's your day", "how's your day going", "are you ok", "are you good"
    ]
    text_lower = text.lower().strip()
    return any(pattern in text_lower for pattern in patterns)

st.title("Simple Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
input_option = st.radio("Anything you want to share?", ("Text", "Image", "Document"))

if input_option == "Text":
    # Text input from user
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        if is_how_are_you(prompt):
            assistant_response = "I'm an algorithm, I do not have any feelings."
        elif is_question(prompt):
            assistant_response = "That is an excellent question! Let me think about it."
        else:
            assistant_response = ""
            for word in response_generator():
                assistant_response += word

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

elif input_option == "Image":
    # Image input from user
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.session_state.messages.append({"role": "user", "content": "User uploaded an image."})
        
        with st.chat_message("user"):
            st.image(uploaded_image)

        assistant_response = "That's a great image! Thanks for sharing."
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

elif input_option == "Document":
    # Document input from user
    uploaded_document = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    if uploaded_document:
        st.session_state.messages.append({"role": "user", "content": "User uploaded a document."})
        
        with st.chat_message("user"):
            st.markdown(f"Uploaded document: {uploaded_document.name}")

        assistant_response = "I've received your document!"
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
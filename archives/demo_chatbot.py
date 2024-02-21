import streamlit as st

st.title("Bot + Propre")

# Initialize chat history
if "messages" not in st.session_state:
    response = f"Bonjour, je suis votre assistant virtuel. Comment puis-je vous aider ?"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages = [
        {"role": "assistant", "content": response}
    ]

else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Dites quelque chose..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

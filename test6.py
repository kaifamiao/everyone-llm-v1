import streamlit as st

# Custom CSS to style the input area like the provided design
st.markdown("""
    <style>
    .input-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #f5f5f5;
        border-radius: 50px;
        padding: 10px;
        width: 100%;
        max-width: 800px;
        margin: auto;
        box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
    }
    .input-container textarea {
        flex: 1;
        border: none;
        outline: none;
        background-color: transparent;
        resize: none;
        font-size: 16px;
        margin-left: 10px;
    }
    .input-container textarea::placeholder {
        color: #888;
    }
    .attachment-icon {
        width: 24px;
        height: 24px;
        margin-right: 10px;
    }
    .send-button {
        background-color: #000;
        color: white;
        border: none;
        border-radius: 50%;
        height: 40px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .send-button svg {
        fill: white;
        width: 16px;
        height: 16px;
    }
    </style>
    """, unsafe_allow_html=True)


# HTML and custom button with an input field
def main():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    # Left attachment icon
    st.markdown('''
        <img class="attachment-icon" src="https://img.icons8.com/material-outlined/24/000000/attach.png" alt="attach">
    ''', unsafe_allow_html=True)

    # Text area for input
    user_input = st.text_area("", height=40, key="chat_input", label_visibility="collapsed",
                              placeholder="Type a message...")

    # Send button (as an SVG icon inside a button element)
    st.markdown('''
        <button class="send-button">
            <svg viewBox="0 0 24 24">
                <path d="M2 21l21-9L2 3v7l15 2-15 2v7z"></path>
            </svg>
        </button>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle button click
    if st.button("Send", key="send_button"):
        st.write(f"User input: {user_input}")


if __name__ == "__main__":
    main()

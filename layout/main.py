import streamlit as st

def history():
    st.write("### Chat History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def chat(user_input: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": user_input})


# 公用函数 showContent
def showContent(t1, t2, t3, t4):
    """根据传入的参数更新主窗口的内容"""
    st.session_state['output'] = f"t1: {t1}, t2: {t2}, t3: {t3}, t4: {t4}"
    # if len(st.session_state.messages)>1:
    #     chat(st.session_state['output'])




def main():
    # Main 主窗口布局
    st.write("## Main Layout")

    # 第一行，4列
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Main Row1 Col1"):
            showContent("Main Row1 Col1", "", "", "")
    with col2:
        if st.button("Main Row1 Col2"):
            showContent("Main Row1 Col2", "", "", "")
    with col3:
        if st.button("Main Row1 Col3"):
            showContent("Main Row1 Col3", "", "", "")
    with col4:
        if st.button("Main Row1 Col4"):
            showContent("Main Row1 Col4", "", "", "")

    # 第二行，3列
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Main Row2 Col1"):
            showContent("", "Main Row2 Col1", "", "")
    with col2:
        if st.button("Main Row2 Col2"):
            showContent("", "Main Row2 Col2", "", "")
    with col3:
        if st.button("Main Row2 Col3"):
            showContent("", "Main Row2 Col3", "", "")

    # 第三行，1列 (用于显示点击事件)
    if 'output' not in st.session_state:
        st.session_state['output'] = "No Button Clicked Yet"
    st.write("### Main Row 3 - Output: ")
    st.write(st.session_state['output'])
    showContent("", "", "Main Row4 Btn", "")
    history()
    # 第四行，1列
    if st.button("Main Row4 Btn"):
        showContent("", "", "Main Row4 Btn", "")

    # 第五行，4列
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Main Row5 Col1"):
            showContent("", "", "", "Main Row5 Col1")
    with col2:
        if st.button("Main Row5 Col2"):
            showContent("", "", "", "Main Row5 Col2")
    with col3:
        if st.button("Main Row5 Col3"):
            showContent("", "", "", "Main Row5 Col3")
    with col4:
        if st.button("Main Row5 Col4"):
            showContent("", "", "", "Main Row5 Col4")
            st.session_state.messages = []
            chat("Main Row5 Col4")
            st.rerun()

    # 第六行，8列
    cols = st.columns(8)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Main Row6 Col{i + 1}"):
                showContent("", "", "", f"Main Row6 Col{i + 1}")

    # 添加聊天输入框
    st.write("### Chat Input")
    if chat_input := st.chat_input("Type your message here:"):
        chat(chat_input)
        st.rerun()
        # showContent("", "", "", f"Chat Message: {chat_input}")
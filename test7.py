import streamlit as st
# 设置页面配置
st.set_page_config(
    page_title="everyOne LLM 开放测试——文档对话",
    page_icon="📄",
    layout="wide" # "centered" | "wide" | "wide",
    # initial_sidebar_state="expanded",
)

from chat_config.chat_config import showlogo


# Custom CSS for styling chat input
# Custom CSS to style the text area
# Custom CSS to style the text area and button
st.markdown("""
    <style>
    .custom-container {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .custom-textarea {
        height: 100px; /* Set the height */
        max-height: 100px; /* Set the max height */
        width: 100%; /* Set the width */
        font-size: 18px; /* Set the font size */
        padding: 10px; /* Set padding */
        box-sizing: border-box; /* Ensure padding is included in width/height */
    }
    .custom-button {
        margin-top: 10px; /* Add space between input and button */
        padding: 10px 20px; /* Button padding */
        font-size: 18px; /* Button font size */
        background-color: #007bff; /* Button background color */
        color: white; /* Button text color */
        border: none; /* Remove border */
        border-radius: 5px; /* Round corners */
        cursor: pointer; /* Pointer cursor on hover */
        align-self: flex-start; /* Align button to the start */
        width: 100%
    }
    .custom-button:hover {
        background-color: #0056b3; /* Darker background on hover */
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize state for messages and display content
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "你好有啥可以帮助你的吗？"})

if 'display' not in st.session_state:
    st.session_state.display = "main"

if 'Current_PageName' not in st.session_state:
    st.session_state.Current_PageName = "main"

Current_Message =st.empty()
st.write("# EveryOne LLM template")

def history():
    st.write("### Chat History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def showMessage(content):
    st.session_state.messages.append({"role": "assistant", "content": content})


def update_message(button_name):
    showMessage(f"Button '{button_name}' clicked!")
    st.toast(f"Button '{button_name}' clicked!")
    st.rerun()


def main():
    st.markdown("### Main")
    if st.button("Strat Chat..."):
        st.session_state.display="chat"
        st.rerun()
def chat():
    st.write("### M1")
    with st.expander("M1 Component"):
        cols = st.columns(10)
        radio_options = [f"Option {i + 1}" for i in range(10)]
        selected_option = st.radio("Select an option:", radio_options, key="radio")

    st.write("### M2")
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Button M2-{i + 1}"):
                update_message(f"Button M2-{i + 1}")

    st.write("### M3")
    col1, col2 = st.columns([8, 2])  # 70% and 30% width ratio
    with col1:
        history()
    with col2:
        if st.button("Button M3-1"):
            update_message("Button M3-1")
        with st.expander("Component 3", expanded=True):
            if st.button("Button 3-32"):
                update_message("Button 3-3")
    # Display messages in the wider column
    # Display messages
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # history()
    st.write("### M4")
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Button M4-{i + 1}"):
                update_message(f"Button M4-{i + 1}")

    st.write("### M5")
    cols = st.columns(8)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Button M5-{i + 1}"):
                update_message(f"Button M5-{i + 1}")

    st.write("### M6")
    col1,col2,col3 = st.columns([2, 6,2 ])
if mp:=st.chat_input("What is up?", key="chat"):
    update_message(mp)
def show1():
    st.write("### Show 1")
    st.write("Content for Show 1")


if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 'tab1'
    print("初始化")


# 修改 show2() 来记住用户选择的选项卡状态
def show2():
    st.write("### Show 2")
    st.write("Content for Show 2")
    # 如果没有选择过，初始化 session_state 的 tab 选项

    # 创建带状态的选项卡
    tab1, tab2, tab3 = st.tabs(["tab1", "tab2", "tab3"])

    # 选择用户的选项卡并更新 session_state
    if st.session_state.selected_tab == "tab1":
        with tab1:
            st.write("tab1 content")
            st.session_state.selected_tab = "tab1"
    elif st.session_state.selected_tab == "tab2":
        with tab2:
            st.write("tab2 content")
            st.session_state.selected_tab = "tab2"
    elif st.session_state.selected_tab == "tab3":
        with tab3:
            st.write("tab3 content")
            st.session_state.selected_tab = "tab3"

    # 用户点击不同选项卡后，更新 session_state
    with tab1:
        if st.button("Select Tab 1"):
            st.session_state.selected_tab = "tab1"
    with tab2:
        if st.button("Select Tab 2"):
            st.session_state.selected_tab = "tab2"
    with tab3:
        if st.button("Select Tab 3"):
            st.session_state.selected_tab = "tab3"


def show3():
    st.write("### Show 3")
    st.write("Content for Show 3")


def show4():
    st.write("### Show 4")
    st.write("Content for Show 4")


def show5():
    st.write("### Show 5")
    st.write("Content for Show 5")
p_logo = st.sidebar.empty()
showlogo(p_logo)
# Sidebar layout
with st.sidebar:

    st.write("### w1")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Button 1-1"):
            update_message("Button 1-1")
    with col2:
        if st.button("Button 1-2"):
            update_message("Button 1-2")

    st.write("### w2")
    if st.button("Button 2-1"):
        update_message("Button 2-1")

    st.write("### w3")
    with st.expander("Component 1"):
        if st.button("Button 3-1"):
            update_message("Button 3-1")
    with st.expander("Component 2"):
        if st.button("Button 3-2"):
            update_message("Button 3-2")
    with st.expander("Component 3"):
        if st.button("Button 3-3"):
            update_message("Button 3-3")

    st.write("### w4")
    for i in range(6):
        if st.button(f"Button W4-{i + 1}"):
            st.session_state.display = f"show{i + 1}" if i > 0 else "main"

    st.write("### w5")
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Button 5-{i + 1}"):
                update_message(f"Button 5-{i + 1}")



# Main window layout
if st.session_state.display == "main":
    main()
elif st.session_state.display == "chat":
    chat()
    # st.rerun()
elif st.session_state.display == "show1":
    show1()
elif st.session_state.display == "show2":
    show2()
elif st.session_state.display == "show3":
    show3()
elif st.session_state.display == "show4":
    show4()
elif st.session_state.display == "show5":
    show5()


from layout.css import cumstom_css
st.markdown(cumstom_css, unsafe_allow_html=True)

# st.title("Chat Input Styling Example")

# Simulated chat input with custom CSS class
# st.markdown('<div class="custom-container">', unsafe_allow_html=True)
# user_input = st.text_area("", height=100, key="chat_input",
#                           label_visibility="collapsed")  # Set initial height for text area
# st.markdown('</div>', unsafe_allow_html=True)
#
# st.markdown('''
#   <script>
#   function show(){
#     document.write("ok")
#   }
#   </script>
# ''', unsafe_allow_html=True)
# if 'user_input' not in st.session_state:
#     st.session_state.user_input = "ok"
# # # Display the button inside the container
# print(st.session_state.user_input)
# if st.markdown(f'<button class="custom-button" onclick="show()" >{st.session_state.user_input}</button>', unsafe_allow_html=True):
#     if st.session_state.user_input=="ok":
#         st.write(f"User input:{st.session_state.user_input}")
#         st.session_state.user_input= "no"
#         print(st.session_state.user_input)
#     else:
#         st.write(f"User input:{st.session_state.user_input}")
#         # st.session_state.user_input = "ok"
#

print(st.session_state.selected_tab)
st.toast(f"st.session_state.display : {st.session_state.display}")
st.toast(f"Current_PageName : {st.session_state.Current_PageName}")

Current_Message.success(f"st.session_state.display : {st.session_state.display}")
Current_Message.success(f"Current_PageName : {st.session_state.Current_PageName}")
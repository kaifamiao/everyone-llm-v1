import streamlit as st

from layout.set_page_config import set_page_config

set_page_config()
from layout.main import main
from layout.main import showContent
from layout.newUI import newUI
from layout.setting import Setting



# 初始化状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "你好有啥可以帮助你的吗？"})

if 'output' not in st.session_state:
    st.session_state['output'] = ""
if 'page' not in st.session_state:
    st.session_state.page = "main"  # 默认显示主页面



# 定义新页面的UI函数



# 侧边栏布局
with st.sidebar:
    # 第一行，两个按钮，按列
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sidebar Btn 1"):
            showContent("Sidebar Btn 1", "", "", "")
    with col2:
        if st.button("Sidebar Btn 2"):
            showContent("Sidebar Btn 2", "", "", "")

    # 第二行到第三行，分别有 expander 和按钮
    with st.expander("Expander 1"):
        if st.button("Expander 1 Btn"):
            showContent("", "Expander 1 Btn", "", "")

    with st.expander("Expander 2"):
        if st.button("Expander 2 Btn"):
            showContent("", "Expander 2 Btn", "", "")

    with st.expander("Expander 3"):
        if st.button("Expander 3 Btn"):
            showContent("", "Expander 3 Btn", "", "")

    # 第四行按钮
    if st.button("Sidebar Btn 3"):
        showContent("", "", "Sidebar Btn 3", "")

    # 第五行，4列
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Col 1 Btn"):
            showContent("", "", "", "Col 1 Btn")
    with col2:
        if st.button("Col 2 Btn"):
            showContent("", "", "", "Col 2 Btn")
    with col3:
        if st.button("Col 3 Btn"):
            showContent("", "", "", "Col 3 Btn")
    with col4:
        if st.button("Col 4 Btn"):
            showContent("", "", "", "Col 4 Btn")

    # 增加一个按钮叫 "第二页"，点击后切换页面
    if st.button("第1页"):
        st.session_state.page = "main"
    if st.button("第2页"):
        st.session_state.page = "newUI"  # 切换到新页面
    if st.button("第3页"):
        st.session_state.page = "Setting"  # 切换到新页面

# Main 主窗口布局
if st.session_state.page == "main":
    main()
    st.session_state.page = "main"


if st.session_state.page == "newUI":
    # 如果 "第二页" 按钮被点击，调用 newUI
    newUI()
    st.session_state.page = "newUI"

if st.session_state.page == "Setting":
    # 如果 "第三页" 按钮被点击，调用 Setting
    Setting()
    st.session_state.page = "Setting"

if st.session_state.page=="main":
    pass
from layout.css import cumstom_css
st.markdown(cumstom_css, unsafe_allow_html=True)
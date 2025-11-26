from kfm_config import extract_second_link

import kfm_globals
from kfm_core.kfm_sys.log_config import setup_logger
from kfm_core.utils import read_markdown

kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"kfm_globals initialization")
json_data = kfm_globals.json_data

# 读取并显示 logo.md 文件中的内容
print(read_markdown("logo.md"))
kfm_logger.debug(f"Get configuration parameters {kfm_globals.title} ,version {kfm_globals.version}")

import streamlit as st

from chat_config.chat_config import showlogo
from layout.css import cumstom_css
from kfm_config import read_markdown

# 设置页面配置
st.set_page_config(
    page_title="everyOne LLM 开放测试——文档对话",
    page_icon="📄",
    layout="wide" # "centered" | "wide" | "wide",
    # initial_sidebar_state="expanded",
)
st.markdown(cumstom_css, unsafe_allow_html=True)
# 使用 CSS 自定义样式
st.markdown(
    """
    <style>
    .top-aligned-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 隐藏 Streamlit 的导航条 */
    header {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 确保整个页面内容紧贴顶部 */
    .main > div {
        padding-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 调整侧边栏宽度 */
    .css-1d391kg {
        width: 500px;
    }
    .css-1d391kg .css-1v3fvcr {
        width: 500px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 自定义 CSS 样式
st.markdown(
    """
    <style>
    /* 调整 st.expander 的样式，文字居左对齐 */
    .streamlit-expanderContent p * {
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# 创建一个自定义样式的容器
st.markdown('<div class="top-aligned-container">', unsafe_allow_html=True)
p_logo = st.sidebar.empty()
sidebar_s=st.sidebar.empty()


showlogo(p_logo)

# 读取并显示 logo.md 文件中的内容
print(read_markdown("logo.md"))
def sidebar():
    sidebar_s.subheader('''  AI than everyone can use''')



sidebar()


if "session_id" not in st.session_state:
    st.session_state.session_id = ""

from chat_config.set_query_doc_chat import get_session_history, get_sqlite_data_list

store={}
######################################################################################################################
def show_history_message(store,st):
    st.session_state.messages = []
    for o in store.messages:
        # print(f"o: {o.type}")
        if o.type == "human":
            st.session_state.messages.append({"role": "user", "content": o.content})
        else:
            st.session_state.messages.append({"role": "assistant", "content": o.content})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



## //////////////////////////////////////////// 获取历史记录  //////////////////////////////////////////////////
def show_sidebar_history(store,st1,st):
    kfm_logger.debug("st.sidebar show_sidebar_history HISTORY_LIST initialization start 🚀 ")
    filename_list = []
    i=0
    # kfm_logger.debug(f"show_sidebar_history store is  start len : {len(store.messages)} ")
    for bt in get_sqlite_data_list():
        print(f"Create st1[{i}].button({bt[0]})")
        if st1[i].button(bt[0]):
            kfm_logger.debug(f"show_sidebar_history -> Cilck st.session_state.session_id : {st.session_state.session_id}")
            st.session_state.PAGE_STATE = "HISTORY_LIST"
            st.session_state.DOC_DIALOG_FILENAME = []
            store = {}
            st.session_state.messages = []
            st.session_state.session_id = bt[0]
            store = get_session_history(st.session_state.session_id)
            # print("store\n")


            st.session_state.messages = store
            # show_history_message(store,st)
            kfm_logger.debug(f"Select historical st.session_state.session_id is {st.session_state.session_id}")
            result = extract_second_link(st.session_state.session_id)
            kfm_logger.fatal(f"get_sqlite_data_list document name is : {result}")
            filename_list.append(result)
            if result != None:
                kfm_logger.debug(f"Select historical dialogue。。。{filename_list}")
                st.session_state.DOC_DIALOG_FILENAME = filename_list
                collection_name = st.session_state.DOC_DIALOG_FILENAME
                kfm_logger.error(f"st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME}")
        i=i+1
    ## //////////////////////////////////////////// 获取历史记录  //////////////////////////////////////////////////

    # kfm_logger.debug(f"show_sidebar_history store is  end len : {len(st.session_state.messages)} ")
    kfm_logger.debug("st.sidebar HISTORY_LIST initialization completed ✅ ")




# 主区域
st.header("everyOne LLM")
st.subheader("第0行 - 列 1")
st.write("这是第一列的内容")
# 主区域的第一行，包含三列
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("第一行 - 列 1")
    st.write("这是第一列的内容")

with col2:
    st.subheader("第一行 - 列 2")
    st.write("这是第二列的内容")

with col3:
    st.subheader("第一行 - 列 3")
    st.write("这是第三列的内容")

# 主区域的第二行，包含一列
st.subheader("第二行")
st.write("这是第二行的内容")

# 主区域的第四行，包含一列
st.subheader("第三行")
st.write("这是第三行的内容")



# placeholder_history_message=st.container()
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "你好有啥可以帮助你的吗？"})


def chat(user_input: str):
    st.session_state.messages.append({"role": "user", "content":user_input})
    st.session_state.messages.append({"role": "assistant", "content": "assistant : ok"})
if prompt :=st.chat_input("hello"):
    chat(prompt)

kfm_logger.debug(f"check show_history_message : st.session_state.messages {st.session_state.messages} ")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("第四行")
st.write("这是第四行的内容")

st.subheader("第五行")
st.write("这是第五行的内容")
# 主区域的第六行，包含六列
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.write("第六列 - 列 1")
    if st.button("row6-1"):
        chat("row6-1")

with col2:
    st.write("第六列 - 列 2")
    if st.button("row6-2"):
        chat("row6-2")

with col3:
    st.write("第六列 - 列 3")
    if st.button("row6-3"):
        chat("row6-5")

with col4:
    st.write("第六列 - 列 4")
    if st.button("row6-4"):
        chat("row6-4")

with col5:
    st.write("第六列 - 列 5")
    if st.button("row6-5"):
        chat("row6-5")

with col6:
    st.write("第六列 - 列 6")
    if st.button("row6-6"):
        chat("row6-6")

col21, col22, col23, col24, col25, col26 = st.columns(6)
with col21:
    if st.button("🆑"):
        st.markdown("")
with col22:
    if st.button("⭐️"):
        st.markdown("")
with col23:
    if st.button("👍"):
        st.markdown("")
with col24:
    if st.button("👎"):
        st.markdown("")
with col25:
    if st.button("📃"):
        st.markdown("")
with col26:
    if st.button(""):
        st.markdown("")



# 侧边栏区域
with st.sidebar:
    st.header("侧边栏")

    # 侧边栏第一行，包含两列
    col1, col2 = st.columns(2)

    with col1:
        st.write("侧边栏第一行 - 列 1")
        if st.button("OK"):
            pass

    with col2:
        st.write("侧边栏第一行 - 列 2")
        if st.button("+New Chat"):
            pass
    st.sidebar.success(
        "This application identifies the crop health in the picture.")
    # 侧边栏中间部分
    st.write("侧边栏中间的内容")

    # 侧边栏
    with st.sidebar:
        st.header("侧边栏")

        with st.expander("历史记录"):
            # st.write("双击显示历史记录")

            # 创建占位符数组
            ppp = [st.empty() for _ in range(100)]
            show_sidebar_history(store, ppp, st)

        with st.expander("展开部分 2"):
            st.write("侧边栏内容行 2")

        with st.expander("展开部分 3"):
            st.write("侧边栏内容行 3")
    # 侧边栏最后一行，包含四列
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("侧边栏最后一行 - 列 1")
        if st.button("foot01"):
            chat("foot01")

    with col2:
        st.write("侧边栏最后一行 - 列 2")
        if st.button("foot02"):
            chat("foot02")

    with col3:
        st.write("侧边栏最后一行 - 列 3")
        if st.button("foot03"):
            chat("foot03")

    with col4:
        st.write("侧边栏最后一行 - 列 4")
        if st.button("foot04"):
            chat("foot04")








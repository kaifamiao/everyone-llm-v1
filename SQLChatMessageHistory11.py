# -*- coding: utf-8 -*-

import streamlit as st

from chat_config.set_query_doc_similarity_search import kfm_query_doc_with_similarity_search
from kfm_config import read_markdown
from kfm_core.kfm_sys.log_config import setup_logger
from chat_config.chat_config import showlogo, set_chat_name
from kfm_config import rrrr, extract_link, extract_second_link
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
# 设置页面配置
st.set_page_config(
    page_title="everyOne LLM 开放测试——文档对话",
    page_icon="📄",
    layout="wide" # "centered" | "wide" | "wide",
    # initial_sidebar_state="expanded",
)
from chat_config.style import cumstom_css
st.markdown(cumstom_css, unsafe_allow_html=True)
# 自定义按钮样式，使文字左对齐
st.markdown(
    """
    <style>
    .stButton>button {
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 读取并显示 logo.md 文件中的内容
print(read_markdown("logo.md"))

# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("gpt2")

kfm_logger = setup_logger(__name__)

kfm_logger.debug("Style initialization completed ✅ ")


if "session_id" not in st.session_state:
    st.session_state.session_id = ""


from langchain_core.messages import HumanMessage, trim_messages

from chat_config.set_query_doc_chat import get_session_history, get_sqlite_data_list, \
     kfm_query_doc_chat, index_upload_config


st.title("📄💬文档对话")
st.subheader("everyOne LLM 开放测试")
if "PAGE_STATE" not in st.session_state:
    st.session_state.PAGE_STATE = "LOADING"

collection_name=[]


kfm_logger.debug(f"📄💬对话。。。Document dialogue begins st.session_state.pageName :  {st.session_state.PAGE_STATE} ")


p_logo = st.sidebar.empty()
showlogo(p_logo)
# kfm_logger.error(f"st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME}")



# 显示首页 upload 调用配置
if st.session_state.session_id == "":
    kfm_logger.debug("index_upload_config is initialization completed ✅ ")
    index_upload_config(st)

store = {}

# print(f"history store: \n{store}")

# st.markdown(f"use collection_name {collection_name}")

st.sidebar.subheader('''  AI than everyone can use''')
st.sidebar.markdown('''🏠<a href="/" target="_self" >主页</a>''', unsafe_allow_html=True)
if st.sidebar.button("💬New Chat"):
    st.session_state.page = "new"
    st.sidebar.write("New Chat history.")
    st.session_state.messages = []
    store = []
    # exec(SQLChatMessageHistory5.py)
    st.session_state.session_id = ""
    st.session_state.PAGE_STATE="NEWCHAT"
    st.session_state.DOC_DIALOG_FILENAME=[]
    st.rerun()

placeholder = st.sidebar.empty()
select_info = st.empty()

def show_history_message(store):
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

filename_list = []
## //////////////////////////////////////////// 获取历史记录  //////////////////////////////////////////////////
for bt in get_sqlite_data_list():

    if st.sidebar.button(bt[0]):

        st.session_state.PAGE_STATE = "HISTORY_LIST"
        st.session_state.DOC_DIALOG_FILENAME = []
        store = {}
        st.session_state.messages = []
        st.session_state.session_id = bt[0]
        store = get_session_history(st.session_state.session_id)
        show_history_message(store)
        kfm_logger.debug(f"Select historical st.session_state.session_id is {st.session_state.session_id}")
        result = extract_second_link(st.session_state.session_id)
        kfm_logger.fatal(f"get_sqlite_data_list document name is : {result}")
        filename_list.append(result)
        if result != None:
            kfm_logger.debug(f"Select historical dialogue。。。{filename_list}")
            st.session_state.DOC_DIALOG_FILENAME=filename_list
            collection_name=st.session_state.DOC_DIALOG_FILENAME
            kfm_logger.error(f"st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME}")

## //////////////////////////////////////////// 获取历史记录  //////////////////////////////////////////////////

kfm_logger.debug("st.sidebar HISTORY_LIST initialization completed ✅ ")

if "page" not in st.session_state:
    st.session_state.page = "new"

if "DOC_DIALOG_FILENAME" not in st.session_state:
    st.session_state.DOC_DIALOG_FILENAME = []
    collection_name=[]

if "session_id" not in st.session_state:
    st.session_state.session_id = ""

if "messages" not in st.session_state:

    # st.markdown(f"messages not in session_state {st.session_state.page}")
    # st.info(f"st.session_state.page :,{st.session_state.page}")
    st.session_state.messages = []
    # st.session_state.messages = load_chat_history()

if st.session_state.session_id != "":
    select_info.success(f"💬历史对话 {st.session_state.session_id} collection_name :  {collection_name} ")
else:
    select_info.success(f"💬📖开始文档对话 {st.session_state.session_id} collection_name : {collection_name} st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME}")

kfm_logger.debug("st.session_state is initialization completed ✅ ")
kfm_logger.debug(f"st.session_state is \n {st.session_state}")

store = get_session_history(st.session_state.session_id)
# kfm_logger.debug(f"{rrrr("store")}")
# print(f"{rrrr("store")}: \n{store}")
# st.info(f"session_id: {st.session_state.session_id} page: {st.session_state.page}")



def start_chat(prompt:str):
    kfm_logger.debug(f"{st.session_state.DOC_DIALOG_FILENAME}")
    # kfm_logger.debug(f"\n{rrrr("======================== prompt := st.chat_input('What is up?') =======================")} ")
    kfm_logger.debug("")
    kfm_logger.debug(f"*\tprompt: {prompt}")
    kfm_logger.debug("")
    if len(st.session_state.DOC_DIALOG_FILENAME) <0:
        st.warning("还没有上传文档")

    st.session_state.PAGE_STATE = "CHAT_INPUT"
    st.session_state.messages.append({"role": "user", "content": prompt})
    if st.session_state.page == "new" and st.session_state.session_id == "":
        session_id = set_chat_name(prompt)
        kfm_logger.debug(f"st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME}")
        if len(st.session_state.DOC_DIALOG_FILENAME)<1:
            st.warning("还没有上传文档，AI会胡说八道...")
            session_id = "[文档]" + session_id
        else:
            session_id="[文档]["+st.session_state.DOC_DIALOG_FILENAME[0]+"]"+session_id
            config = {"configurable": {"session_id": session_id}}
            print(config)
            print(
                "===================================================第一次聊天 Start===================================================")
            print(f"st.session_state.page  {st.session_state.page}")
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner(f"Document {st.session_state.DOC_DIALOG_FILENAME} search in progress..."):
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in kfm_query_doc_with_similarity_search(prompt,config):
                        full_response += (chunk.content or "")
                        print(chunk.content, end="", flush=True)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            get_session_history(session_id).messages.append(HumanMessage(content=prompt))
            st.session_state.session_id = session_id
            placeholder.markdown(f"session_id: {st.session_state.session_id}")

            print(f"第一次聊天 End st.session_state.session_id: {st.session_state.session_id}")
            st.session_state.page = "history"

        print(
            "================================================第一次聊天 END===============================================")
    else:
        show_history_message(store)
        print(
            "===============================================第二次聊天 Start==============================================")
        print(f"st.session_state.page  {st.session_state.page}")
        print(f"session_id: {st.session_state.session_id}")
        placeholder.markdown(f"session_id: {st.session_state.session_id}")
        config = {"configurable": {"session_id": st.session_state.session_id}}

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            if len(st.session_state.DOC_DIALOG_FILENAME)<1:
                msg=f"🤖AI直接回答，没有文档 session_id,{st.session_state.session_id} , DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME}"
            else:
                msg=f"🔍Search '{st.session_state.DOC_DIALOG_FILENAME}' document  in progress..."
            with st.spinner(msg):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in kfm_query_doc_with_similarity_search(prompt, config):
                    full_response += (chunk.content or "")
                    print(chunk.content, end="", flush=True)
                    # if len(st.session_state.DOC_DIALOG_FILENAME)>0:
                    #     full_response += (chunk.content or "")
                    #     print(chunk.content, end="", flush=True)
                    # else:
                    #     full_response += (chunk.content or "")
                    #     print(chunk.content, end="", flush=True)
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        print(
            "\n===================================================第二次聊天 END===================================================")


kfm_logger.debug("Get ready to start the conversation ✅ ")
kfm_logger.error(f"st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME}")
if prompt := st.chat_input("What is up?"):
    start_chat(prompt)


# st.markdown(f"{doc_sources}")
# print(f"last store: \n{store}")






        # st.rerun()



# 自定义侧边栏背景颜色
st.markdown(
    """
    <style>
       [class="st-emotion-cache-1gv3huu eczjsme18"] {
        background-color: #ffffff;
        padding: 1rem;

        }
    </style>
    """,
    unsafe_allow_html=True
)

# 你的 Streamlit 应用代码
st.sidebar.title("侧边栏")
st.sidebar.markdown("这是侧边栏的内容。")




if st.session_state.session_id !="":
    st.warning(f"历史记录： {st.session_state.session_id} ")
col1, col2, col3, col4 =st.columns(4)
# 创建一个按钮
if st.session_state.session_id !="":
    with col1:
        if st.button(f"🆑清除历史记录:{st.session_state.session_id}"):
            st.markdown(f"历史记录已清除{st.session_state.session_id}")
    with col2:
        if st.button("⭐️收藏"):
            st.markdown("收藏成功")
    with col3:
        if st.button("🫗导出"):
            st.markdown("导出还在做。。。")
    with col4:
        if st.button("😊评分"):
            st.markdown("评分还在做。。。")


if len(st.session_state.DOC_DIALOG_FILENAME)<0:
    st.toast("请上传文档，开始对话", icon="🔔")
else:
    if st.session_state.session_id == "" and len(st.session_state.DOC_DIALOG_FILENAME) > 0:
        st.toast(f"还没有开始对话", icon="🔔")
    else:
        st.toast(f"历史对话: {st.session_state.session_id}", icon="🔔")


# css_file_url = "./chat_config/style.css"
# st.markdown(f'<link rel="stylesheet" href="{css_file_url}">', unsafe_allow_html=True)




if st.button(f"分析文档{st.session_state.DOC_DIALOG_FILENAME}"):
    start_chat(f"总结分析当前这个文档")


# con = st.container()
# cc1 ,cc2,cc3,cc4 =con.columns(4)
# with cc1:
#     cc1.markdown("cc1")
#     if cc1.button("分析文档"):
#         start_chat(f"总结当前这个文档")
# with cc2:
#     cc2.markdown("cc2")
# with cc3:
#     cc3.markdown("cc3")
# with cc4:
#     cc4.markdown("cc4")
# cola =st.columns(21)
# cola.append(con)

kfm_logger.debug(f"footer 📄💬对话。。。Document dialogue end...  st.session_state.PAGE_STATE \n : {rrrr(st.session_state.PAGE_STATE)}\n st.session_state.DOC_DIALOG_FILENAME  : {st.session_state.DOC_DIALOG_FILENAME.__str__()} \n st.session_state.session_id: {st.session_state.session_id}")

print("*********************************************************************************************************")
print("*                                                                                                       *")
print("*                                                                                                       *")
print("*                            运行顺利   ，大吉大利                                                      *")
print("*                                                                                                       *")
print("*                                                                                                       *")
print("*********************************************************************************************************")
# 示例字符串
# text = "历史记录： [文档][自制变频机故障代码(2)(1).pdf]给我说下，自制变频机"
# print(text)
# # 调用函数并打印结果
# result = extract_second_link(text)
# print(result)  # 输出: 关于——开发喵AI.pdf
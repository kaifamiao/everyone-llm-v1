from operator import itemgetter
import streamlit as st
import chromadb
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat_config.set_upload import kfm_upload_file, UPLOAD_FOLDER_FINAL
from kfm_config import get_project_root, qqqq, rrrr, yyyy, extract_second_link
from kfm_core.kfm_chatllama.KfmChatLlama import kfm_llm,kfm_embeddings

from langchain_community.document_loaders import DirectoryLoader

from kfm_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)

kfm_logger.warning("set_query_chat.py is running...")
kfm_logger.warning("=================================== Set DOC Query Start ===================================")
def kfm_query_doc_chat():
    kfm_logger.debug(f"{rrrr("📄💬对话。。。")} kfm_query_doc_chat()")

    kfm_logger.debug(f"get_project_root { get_project_root() }")

    if len(st.session_state.DOC_DIALOG_FILENAME)>=1:

        kfm_logger.debug(f"st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME} ✅ ")
    else:
        kfm_logger.error(f"st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME} ❌ ")
    # if st.session_state.session_id!="":
    #     st.session_state.DOC_DIALOG_FILENAME=extract_second_link(st.session_state.session_id)
    # kfm_logger.debug(f"st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME}")
    kfm_logger.debug(f"st.session_state.session_id : {st.session_state.session_id}")
    file_path =UPLOAD_FOLDER_FINAL
    kfm_logger.debug(f"📄💬 文件获取目录 file_path \n\t { yyyy(file_path) }")
    kfm_logger.debug(f"📄💬 文件获取目录 file_path \n\t { file_path} +{st.session_state.DOC_DIALOG_FILENAME}")

    if st.session_state.DOC_DIALOG_FILENAME is not None and len(st.session_state.DOC_DIALOG_FILENAME) >0:

        kfm_logger.warning(f"Enter judgment Check is st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME} ✅ ")
        loader = DirectoryLoader(file_path, glob=st.session_state.DOC_DIALOG_FILENAME, show_progress=True, use_multithreading=True)
        docs = loader.load()
        #

        kfm_logger.debug(f"read file len is  {len(docs)} {rrrr("Starting slicing...")}")
        for d in docs:
            print("=====================================================================================")
            print(yyyy(d.page_content[:100]))
        kfm_logger.debug(f"read file len is  【{len(docs)}】 {rrrr("Ending slicing...")}")


        doc_sources = [doc.metadata["source"] for doc in docs]
        kfm_logger.debug(f"doc_sources ： {doc_sources}")
        #
        #
        kfm_logger.debug("Create text_splitter by RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        kfm_logger.debug("Create splits by text_splitter.split_documents(docs)")
        splits = text_splitter.split_documents(docs)

        kfm_logger.debug("Create vectorstore by Chroma.from_documents ")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=kfm_embeddings)

        print("=================================== DOC ===================================")
        # doc = vectorstore.similarity_search("介绍下林睿")
        # print(doc[0].page_content[:100])

        kfm_logger.debug("Create retriever by  vectorstore.as_retriever()")
        retriever = vectorstore.as_retriever()


        ### Contextualize question ###
        contextualize_q_system_prompt = (""
            # "Given a chat history and the latest user question "
            # "which might reference context in the chat history, "
            # "formulate a standalone question which can be understood "
            # "without the chat history. Do NOT answer the question, "
            # "just reformulate it if needed and otherwise return it as is."
        )
        kfm_logger.debug(f"Create contextualize_q_system_prompt ")
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        kfm_logger.debug(f"Create contextualize_q_prompt by ")


        history_aware_retriever = create_history_aware_retriever(
            kfm_llm, retriever, contextualize_q_prompt
        )
        kfm_logger.debug(f"Create history_aware_retriever by ")


        ### Answer question ###
        system_prompt = (
            "请按照文档查询内容回答问题，如果没有就回答不知道，不可以编造回答"
            "\n\n"
            "{context}"
        )

        kfm_logger.debug(f"Create system_prompt by ")

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        kfm_logger.debug(f"Create qa_prompt by ")


        question_answer_chain = create_stuff_documents_chain(kfm_llm, qa_prompt)

        kfm_logger.debug(f"Create question_answer_chain by ")

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        kfm_logger.debug(f"Create rag_chain by ")

        print("######################################### RunnableWithMessageHistory ################################################################")
        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        kfm_logger.debug(f"Create with_message_history by {st.session_state.DOC_DIALOG_FILENAME} ,{st.session_state.session_id}\n\n")
        return with_message_history

    else:
        # st.session_state.DOC_DIALOG_FILENAME = "*.*"
        kfm_logger.warning(f"Start a regular AI conversation....🤖 ")
        kfm_logger.warning(f"Check is st.session_state.DOC_DIALOG_FILENAME : {st.session_state.DOC_DIALOG_FILENAME}")
        kfm_logger.warning(f"Check is st.session_state.session_id : {st.session_state.session_id}")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你的名字叫AI喵，无论谁问你叫什么，或者你的名字，你都叫AI喵，喵！喵！喵！You are a helpful assistant.",
                ),
                MessagesPlaceholder(variable_name="input"),
            ]
        )
        trimmer = trim_messages(
            max_tokens=9000,
            strategy="last",
            token_counter=kfm_llm,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
        chain = (
                RunnablePassthrough.assign(messages=itemgetter("input") | trimmer)
                | prompt
                | kfm_llm
        )

        ai_with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input"
        )
        kfm_logger.debug(
            f"🤖 Create with_message_history by st.session_state.DOC_DIALOG_FILENAME ： {st.session_state.DOC_DIALOG_FILENAME} ,t.session_state.session_id ： {st.session_state.session_id}\n\n")
        return ai_with_message_history


#########################################################################################################

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # print(f"set_query_doc_chat : get_session_history session_id: {session_id}")
    if session_id=="":
        kfm_logger.debug(f"session_id 还未获取到。。。")
    else:
        kfm_logger.debug(f"set_query_doc_chat : get_session_history session_id: {session_id}")
    return SQLChatMessageHistory(session_id, connection="sqlite:///ai_chat_message.db")
    # if session_id not in store:
    #     store[session_id] = SQLChatMessageHistory(session_id,
    #                                               connection="sqlite:///ai_chat_message.db")
    # return store[session_id]



# for chunk in kfm_query_chat().stream(
#     {"input": "林睿是做什么的"},
#     config={
#         "configurable": {"session_id": "abc123"}
#     },  # constructs a key "abc123" in `store`.
# ):
#     print(chunk.get('answer'), end="", flush=True)


#print("################################# AI 普通对话 ###########################################################")
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "你的名字叫AI喵，无论谁问你叫什么，或者你的名字，你都叫AI喵，喵！喵！喵！You are a helpful assistant.",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
# trimmer = trim_messages(
#     max_tokens=9000,
#     strategy="last",
#     token_counter=kfm_llm,
#     include_system=True,
#     allow_partial=False,
#     start_on="human",
# )
# chain = (
#         RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
#         | prompt
#         | kfm_llm
# )

# with_message_history = RunnableWithMessageHistory(
#     rag_chain,
#     get_session_history,
#     input_messages_key="messages"
# )

kfm_logger.warning("=================================== Set DOC Query End ===================================")

def get_sqlite_data_list():
    kfm_logger.debug("get_sqlite_data_list list is running...")
    # 获取ai_chat_message.db中所有数据message_store表的数据
    # 1. 连接数据库
    import sqlite3
    conn = sqlite3.connect('ai_chat_message.db')
    cursor = conn.cursor()
    # 2. 查询数据
    # show session_id
    cursor.execute('select session_id from message_store group by session_id order by id desc')
    session_id = cursor.fetchall()
    # print(f"session_id: {session_id}")
    # 3. 关闭连接
    cursor.close()
    conn.close()

    return session_id


# 上传组件
def index_upload_config(st):
    with st.expander("什么是文档对话(点击展开上传文件)", expanded=False):
        st.markdown("""
文档对话是一种先进的人工智能技术，它结合了信息检索和自然语言处理，使AI系统能够基于大量文档进行智能交互。

""")
        kfm_logger.debug(f"index_config")
        print("---------------------------------------DOC_DIALOG_FILENAME---------------------------------------------------------")
        kfm_upload_file(st)
        # print(f"222. st.session_state.DOC_DIALOG_FILENAME {st.session_state.DOC_DIALOG_FILENAME}")

#
# 以下是文档对话的主要特点和工作原理：
# 1. 信息检索：
# 系统会在大规模文档库中快速检索与用户问题相关的信息。这个文档库可以包含各种类型的文本，如网页、文章、报告等。
# 2. 上下文理解：
# 系统分析检索到的信息，理解其中的关键概念和关系，以更好地回答用户问题。
# 3. 动态知识整合：
# 将检索到的信息与AI模型的预训练知识相结合，生成更全面、准确的回答。
# 4. 生成式回答：
# 使用先进的语言模型，基于检索到的信息构建连贯、相关的回答。
# 5. 实时更新能力：
# 可以提供基于最新信息的回答，不局限于模型训练时的知识。
# 6. 提高可解释性：
# 通过引用特定文档，增加回答的可信度和可追溯性。
# 7. 领域适应性：
# 通过更新文档库，系统可以轻松适应不同领域或主题。
# 8. 减少AI幻觉：
# 基于实际文档信息，降低生成虚假或不准确信息的风险。
# 9. 支持多轮对话：
# 能够记住对话历史，在后续问答中利用上下文信息。
# 10. 个性化体验：
# 可以整合用户特定的文档，提供个性化的对话体验。
# 文档对话技术广泛应用于客户服务、教育辅助、研究助手等领域，能够提供更精确、可靠的AI交互体验。尽管面临一些技术挑战，但它代表了AI系统向更智能、实用方向发展的重要趋势。

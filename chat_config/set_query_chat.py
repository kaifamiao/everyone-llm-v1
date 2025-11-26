from operator import itemgetter

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

from kfm_config import get_project_root, qqqq
from kfm_rag_core.kfm_chatllama.KfmChatLlama import kfm_llm,kfm_embeddings

from langchain_community.document_loaders import DirectoryLoader

from kfm_rag_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)

kfm_logger.warning("set_query_chat.py is running...")
collection_name = "my_collection"
kfm_logger.debug(f"collection_name :\n\t\t {collection_name}")
def kfm_query_chat():

    kfm_logger.debug(f"get_project_root { get_project_root() }")
    file_path =get_project_root() + "/uploadfile/"
    kfm_logger.debug(f"文件获取目录：\n { qqqq(file_path) }")
    loader = DirectoryLoader(file_path, glob="*.pdf", show_progress=True, use_multithreading=True)
    docs = loader.load()
    #
    kfm_logger.debug(f"read file len is  {len(docs)}")
    # print(docs[0].page_content[:200])

    doc_sources = [doc.metadata["source"] for doc in docs]
    # print(doc_sources)
    kfm_logger.debug(f"doc_sources is {doc_sources}")
    #
    #
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)


    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=kfm_embeddings,
        persist_directory="./kfm_data/kfm_knowledge_data/",
        collection_name=collection_name)
    client = chromadb.PersistentClient(path="./kfm_data/kfm_knowledge_data/")
    print("判断集合。。。。。")
    kfm_logger.debug(f"use collection_name {collection_name}")
    kfm_logger.debug("判断集合。。。。。")
    try:
        collection = client.get_collection(name=collection_name)
        print(f"集合 '{collection_name}' 已经存在。")
    except:
        print("集合不存在")
    vector_query= Chroma(
        persist_directory="./kfm_data/kfm_knowledge_data/",
        embedding_function=kfm_embeddings,
        collection_name=collection_name
    )
    print("=================================== doc ===================================")
    # doc = vector_query.similarity_search("hi")
    # print(doc)
    retriever = vector_query.as_retriever()

    ### Contextualize question ###
    contextualize_q_system_prompt = (""
        # "Given a chat history and the latest user question "
        # "which might reference context in the chat history, "
        # "formulate a standalone question which can be understood "
        # "without the chat history. Do NOT answer the question, "
        # "just reformulate it if needed and otherwise return it as is."
    )
    print(contextualize_q_system_prompt)
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        kfm_llm, retriever, contextualize_q_prompt
    )


    ### Answer question ###
    system_prompt = (
        "请按照文档查询内容回答问题，如果没有就回答不知道，不可以编造回答"
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(kfm_llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)



    print("#########################################################################################################")
    with_message_history = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return with_message_history
#########################################################################################################

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    print(f"get_session_history session_id: {session_id}")
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


print("################################# AI 普通对话 ###########################################################")
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

kfm_logger.warning("=================================== Set Query End ===================================")

def get_sqlite_data():
    # 获取ai_chat_message.db中所有数据message_store表的数据
    # 1. 连接数据库
    import sqlite3
    conn = sqlite3.connect('ai_chat_message.db')
    cursor = conn.cursor()
    # 2. 查询数据
    # show session_id
    cursor.execute('select session_id from message_store group by session_id order by id desc')
    session_id = cursor.fetchall()
    print(f"session_id: {session_id}")
    # 3. 关闭连接
    cursor.close()
    conn.close()

    return session_id
from operator import itemgetter

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory

from kfm_core.kfm_chatllama.KfmChatLlama import kfm_llm


#########################################################################################################

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    print(f"get_session_history session_id: {session_id}")
    return SQLChatMessageHistory(session_id, connection="sqlite:///ai_chat_message.db")
    # if session_id not in store:
    #     store[session_id] = SQLChatMessageHistory(session_id,
    #                                               connection="sqlite:///ai_chat_message.db")
    # return store[session_id]



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你的名字叫AI喵，无论谁问你叫什么，或者你的名字，你都叫AI喵，喵！喵！喵！You are a helpful assistant.",
        ),
        MessagesPlaceholder(variable_name="messages"),
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
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
        | prompt
        | kfm_llm
)

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages"
)


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
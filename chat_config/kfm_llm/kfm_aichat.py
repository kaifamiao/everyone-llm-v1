from operator import itemgetter

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

from kfm_rag_core.kfm_chatllama.KfmChatLlama import kfm_llm
from kfm_rag_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)





class kfm_aichat():
    def __init__(self):
        kfm_logger.debug(f"init kfm_langchain_llm()")
        self.prompt = None
        self.session_id = None
        self.kfm_llm = kfm_llm
    def __int__(self, user_kfm_llm):
        kfm_logger.debug(f"init kfm_langchain_llm()")
        self.kfm_llm = user_kfm_llm

    @staticmethod
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        kfm_logger.debug(f"kfm_langchain_llm create get_session_history session_id : {session_id}")
        print(f"get_session_history session_id: {session_id}")
        return SQLChatMessageHistory(session_id, connection="sqlite:///ai_chat_message.db")
    def ai_qa(self):
        kfm_logger.debug(f"Start a regular AI conversation....🤖 My qa()  ")
        kfm_logger.debug(f"kfm_langchain_llm create prompt")
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你的名字叫AI喵，无论谁问你叫什么，或者你的名字，你都叫AI喵，喵！喵！喵！You are a helpful assistant.",
                ),
                MessagesPlaceholder(variable_name="input"),
            ]
        )
        kfm_logger.debug(f"kfm_langchain_llm create trimmer")
        trimmer = trim_messages(
            max_tokens=9000,
            token_counter=self.kfm_llm,
            strategy="last",
            include_system=True,
            allow_partial=False,
            start_on="human",
        )

        chain = (
                RunnablePassthrough.assign(messages=itemgetter("input") | trimmer)
                | prompt
                | self.kfm_llm
        )

        ai_with_message_history = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="input"
        )

        return ai_with_message_history
    def ai_qa_history(self, prompt, session_id):
        kfm_logger.debug(f"Start a AI conversation with history....🤖self.session_id {self.session_id}")
        self.prompt=prompt
        self.session_id=session_id
        config = {"configurable": {"session_id": session_id}}
        response_stream = self.ai_qa().stream({
                                "input": prompt,
                            },
                            config=config,
            )
        return response_stream


if __name__ == '__main__':
    kfm = kfm_aichat()
    rep = kfm.ai_qa_history("我叫什么名字", "abc")
    for chunk in rep:
        print(chunk.content, end="", flush=True)

    print(len(kfm.get_session_history("abc").messages))

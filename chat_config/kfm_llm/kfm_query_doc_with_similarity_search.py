from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_core.callbacks import BaseCallbackHandler, StreamingStdOutCallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat_config.set_upload import UPLOAD_FOLDER_FINAL
from kfm_config import get_project_root
from kfm_rag_core.kfm_chatllama.KfmChatLlama import kfm_llm, kfm_embeddings
from kfm_rag_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)
# 定义一个流式处理的回调类
class StreamHandler(BaseCallbackHandler):
    def __init__(self):
        print("StreamHandler init")
        # self.container = container
        # self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # token={"answer", token}
        print(token, end="", flush=True)


class CustomStreamingStdOutCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        print("CustomStreamingStdOutCallbackHandler init")
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end="", flush=True)

class kfm_similarity_search:

    def __init__(self,user_kfm_llm, user_kfm_embeddings):
        kfm_logger.debug(f"kfm_query_doc_with_similarity_search init Search version...")
        self.prompt = None
        self.session_id = None
        self.kfm_llm = user_kfm_llm
        self.kfm_embeddings = user_kfm_embeddings
        self.vectorstore = self.create_vectorstore()

    @staticmethod
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        kfm_logger.debug(f"kfm_langchain_llm create get_session_history session_id : {session_id}")
        print(f"get_session_history session_id: {session_id}")
        return SQLChatMessageHistory(session_id, connection="sqlite:///ai_chat_message.db")

    def create_vectorstore(self):
        kfm_logger.debug(f" create_vectorstore()")
        kfm_logger.debug(f"get_project_root {get_project_root()}")

        file_path = UPLOAD_FOLDER_FINAL
        kfm_logger.debug(f"📄💬 文件获取目录 file_path \n\t {file_path} ")

        loader = DirectoryLoader(file_path, glob="*.md", show_progress=True, use_multithreading=True)
        docs = loader.load()
        kfm_logger.debug(f"read file len is  {len(docs)} Starting slicing...")

        for d in docs:
            print("=====================================================================================")
            print(d.page_content[:100])

        doc_sources = [doc.metadata["source"] for doc in docs]

        kfm_logger.debug("Create text_splitter by RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.kfm_embeddings)

        doc_sources = [doc.metadata["source"] for doc in docs]
        print(f"doc_sources ：{doc_sources}")
        return vectorstore
    def query_doc_chat(self):

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a helpful AI assistant. Use the following context from the document to answer the user's question: {context}"),
            ("human", "{question}")
        ])
        chain = prompt | self.kfm_llm
        with_message_history= RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )

        return with_message_history

    def ai_doc_query_similarity_search(self, prompt, session_id):

        self.prompt=prompt
        self.session_id=session_id
        config = {"configurable": {"session_id": session_id}}
        print(f"configurable : \n {config}")
        kfm_logger.debug(f"Start a AI ai_qa_history self.session_id {self.session_id}")
        kfm_logger.debug(f"Start a AI ai_qa_history self.prompt {self.prompt}")
        kfm_logger.debug(f"Start a AI ai_qa_history config {config}")

        # 使用 similarity_search 方法
        similar_docs = self.vectorstore.similarity_search(prompt, k=3)
        context = "\n".join([doc.page_content for doc in similar_docs])

        response_stream = self.query_doc_chat().stream(
            {"question": prompt, "context": context},
            config=config,
            )
        return response_stream

if __name__ == '__main__':
    kfm = kfm_similarity_search(kfm_llm, kfm_embeddings)
    rep = kfm.ai_doc_query_similarity_search("文档讲了什么？", "test3")
    for chunk in rep:
        print(chunk.content, end="", flush=True)

    # print(len(kfm.get_session_history("abc").messages))

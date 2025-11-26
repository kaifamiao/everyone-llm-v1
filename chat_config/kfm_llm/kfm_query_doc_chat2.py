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

class kfm_query_doc_chat():

    def __init__(self,user_kfm_llm, user_kfm_embeddings):
        kfm_logger.debug(f"init kfm_query_doc_chat 2 🥈()")
        self.prompt = None
        self.session_id = None
        self.kfm_llm = user_kfm_llm
        self.kfm_embeddings = user_kfm_embeddings

    @staticmethod
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        kfm_logger.debug(f"kfm_langchain_llm create get_session_history session_id : {session_id}")
        print(f"get_session_history session_id: {session_id}")
        return SQLChatMessageHistory(session_id, connection="sqlite:///ai_chat_message.db")

    def query_doc_chat(self):
        kfm_logger.debug(f" kfm_query_doc_chat()")
        kfm_logger.debug(f"get_project_root {get_project_root()}")

        file_path = UPLOAD_FOLDER_FINAL
        kfm_logger.debug(f"📄💬 文件获取目录 file_path \n\t {file_path} ")

        loader = DirectoryLoader(file_path, glob="*.md", show_progress=True,use_multithreading=True)
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

        # doc = vectorstore.similarity_search("介绍下林睿")
        # print(doc[0].page_content[:100])

        retriever = vectorstore.as_retriever()

        doc_sources = [doc.metadata["source"] for doc in docs]
        print(f"doc_sources ：{doc_sources}")
        ### Contextualize Q&A ####
        contextualize_q_system_prompt = "请问你要查询的内容是什么？"

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            self.kfm_llm, retriever, contextualize_q_prompt
        )

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
        question_answer_chain = create_stuff_documents_chain(self.kfm_llm, qa_prompt)


        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        #-------------------------------------------------------------------------------------------------#
        # PDF ingestion and Question/Answering system

        question_answer_chain = create_stuff_documents_chain(self.kfm_llm, qa_prompt)
        rag_chain=create_retrieval_chain(history_aware_retriever, question_answer_chain)
        #-------------------------------------------------------------------------------------------------#

        # -------------------------------------------------------------------------------------------------#
        # RetrievalQA
        custom_prompt_template="""
        Context:{context}
        Question:{question}
        """
        prompt=PromptTemplate(template=custom_prompt_template,
                              input_variable=['context','question'])

        # 创建StreamHandler实例
        stream_handler = StreamHandler()
        print("RetrievalQA.from_chain_type.........")
        rag_chain =ConversationalRetrievalChain.from_llm(
            llm=self.kfm_llm,
            retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
            )

        # 创建带有回调的链
        chain_with_callbacks = rag_chain.with_config(callbacks=[stream_handler])

        # # -------------------------------------------------------------------------------------------------#
        print("RunnableWithMessageHistory.........")
        config = {"configurable": {"session_id": "test3"}}
        with_message_history = RunnableWithMessageHistory(
            chain_with_callbacks,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )
        for r in with_message_history.stream({"question": "林睿是谁？"},config=config):
            print(r, end="", flush=True)
        return with_message_history

    def ai_qa_history(self, prompt, session_id):

        self.prompt=prompt
        self.session_id=session_id
        config = {"configurable": {"session_id": session_id}}
        print(f"configurable : \n {config}")
        kfm_logger.debug(f"Start a AI ai_qa_history self.session_id {self.session_id}")
        kfm_logger.debug(f"Start a AI ai_qa_history self.prompt {self.prompt}")
        kfm_logger.debug(f"Start a AI ai_qa_history config {config}")
        response_stream = self.query_doc_chat().stream({
                                "query": prompt,
                            },
                            config=config,
            )
        return response_stream

if __name__ == '__main__':
    kfm = kfm_query_doc_chat(kfm_llm, kfm_embeddings)
    rep = kfm.ai_qa_history("林睿是谁？", "test3")
    for chunk in rep:
        print(chunk, end="", flush=True)

    # print(len(kfm.get_session_history("abc").messages))

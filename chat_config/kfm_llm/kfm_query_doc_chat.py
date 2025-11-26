from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat_config.set_upload import UPLOAD_FOLDER_FINAL
from kfm_config import get_project_root
from kfm_rag_core.kfm_chatllama.KfmChatLlama import kfm_llm, kfm_embeddings
from kfm_rag_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)

class kfm_query_doc_chat():

    def __init__(self,user_kfm_llm, user_kfm_embeddings):
        kfm_logger.debug(f"init kfm_query_doc_chat()")
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

        loader = DirectoryLoader(file_path, glob="*.*", show_progress=True,use_multithreading=True)
        docs = loader.load()
        kfm_logger.debug(f"read file len is  {len(docs)} Starting slicing...")
        for d in docs:
            print("=====================================================================================")
            print(d.page_content[:100])
        kfm_logger.debug(f"read file len is  【{len(docs)}】 Ending slicing...")

        doc_sources = [doc.metadata["source"] for doc in docs]
        kfm_logger.debug(f"doc_sources ： {doc_sources}")

        kfm_logger.debug(
            "Create text_splitter by RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        kfm_logger.debug("Create splits by text_splitter.split_documents(docs)")
        splits = text_splitter.split_documents(docs)

        kfm_logger.debug("Create vectorstore by Chroma.from_documents ")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.kfm_embeddings)

        print("=================================== DOC ===================================")
        # doc = vectorstore.similarity_search("介绍下林睿")
        # print(doc[0].page_content[:100])

        kfm_logger.debug("Create retriever by  vectorstore.as_retriever()")
        retriever = vectorstore.as_retriever()

        ### Contextualize question ###
        contextualize_q_system_prompt = "请问你要查询的内容是什么？"
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

        print(
            "######################################### RunnableWithMessageHistory ################################################################")
        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        return with_message_history

    def ai_qa_history(self, prompt, session_id):
        kfm_logger.debug(f"Start a AI conversation with history....🤖self.session_id {self.session_id}")
        self.prompt=prompt
        self.session_id=session_id
        config = {"configurable": {"session_id": session_id}}
        response_stream = self.query_doc_chat().stream({
                                "input": prompt,
                            },
                            config=config,
            )
        return response_stream

if __name__ == '__main__':
    kfm = kfm_query_doc_chat(kfm_llm, kfm_embeddings)
    rep = kfm.ai_qa_history("文档有什么？", "test")
    for chunk in rep:
        print(chunk.get("answer"), end="", flush=True)

    # print(len(kfm.get_session_history("abc").messages))

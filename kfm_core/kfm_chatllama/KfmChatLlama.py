# init.py
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
import langchain, chromadb

import kfm_config

from kfm_core.kfm_sys.log_config import setup_logger
import langchain_core, langchain_community
# 创建一个loggerp
print("KfmChatLlama moudel 日志输出目录：" + kfm_config.get_project_root()+"/logs")
logger = setup_logger(__name__, log_dir=kfm_config.get_project_root()+"/logs")

logger.info(f"LangChain version: {langchain.__version__},langchain_core version:{langchain_core.__version__} Chromadb version: {chromadb.__version__}")
logger.info(f"langchain_community version: {langchain_community.__version__},\t Chromadb version: {chromadb.__version__}")
# 初始化LLM，确保启用流式输出
def get_kfm_stream_llm(CustomStreamingStdOutCallbackHandler):
    return  ChatOllama(
            model="qwen2",
            temperature=0.1,
            top_p=0.9,
            max_length=4098,
            streaming=True,  # 启用流式生成,
            callbacks=[CustomStreamingStdOutCallbackHandler()]
        )
kfm_llm = ChatOllama(model="qwen2",
            temperature=0.1,
            top_p=0.9,
            max_length=4098)


kfm_stream_llm = ChatOllama(model="qwen2",
            temperature=0.1,
            top_p=0.9,
            streaming=True,  # 启用流式生成,
            max_length=4098)

kfm_llms = ChatOllama(model="qwen2",
            temperature=0.1,
            top_p=0.9,
            streaming=True,  # 启用流式生成,
            max_length=4098)
# 初始化嵌入模型
kfm_embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

logger.info(f"llm is {kfm_llm} ,kfm_stream_llm is {kfm_stream_llm}  embedding :{kfm_embeddings}")

logger.debug("KfmChatLlama LLM is  initialization completed ✅  ")

# 接口实现
from langchain_community.chat_models import ChatOllama

from kfm_core.kfm_sys.log_config import setup_logger
from kfm_framework.public import *


from kfm_framework.interface.kfm_model.KfmModel import KfmModel
kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"KfmModel2 initialization")
class KfmModel2(KfmModel):
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.llm = ChatOllama(
            model="llama3.1:8b",
            temperature=0,
            top_p=0.9,
            max_length=4098,
            streaming=True,
        )
        kfm_logger.info(f"KfmModel2 B init params : {self.params}")
        kfm_logger.info(f"KfmModel2 B init llm : {self.llm}")

    def process(self, input: str) -> object:
        return self.llm
        # return f"Processed by KfmModel2 B: {input}"
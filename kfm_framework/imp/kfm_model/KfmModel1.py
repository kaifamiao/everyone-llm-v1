# 接口实现
from kfm_framework.public import *


from kfm_framework.interface.kfm_model.KfmModel import KfmModel

from kfm_core.kfm_chatllama.KfmChatLlama import kfm_llm
class KfmModel1(KfmModel):
    def __init__(self, params: Dict[str, Any]):
        self.params = params

    def process(self, input: str) -> object:
        return kfm_llm
        # return f"Processed by KfmModel1 A: {input}"

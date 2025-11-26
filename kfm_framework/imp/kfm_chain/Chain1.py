from typing import Dict

from langchain_community.chat_models import ChatOllama

from kfm_framework.interface.kfm_chain.KfmChain import KfmChain

from kfm_core.kfm_sys.log_config import setup_logger

kfm_logger = setup_logger(__name__)
class Chain1(KfmChain):
    def execute(self, input: Dict) -> str:
        print("==================== Chain1 execute Start ==================")
        print(type(input))
        print(f"input.get('model'){type(input.get('model'))}")
        print(input.get('kfm_embedding'))
        print(input.get('template'))
        print(input.get('vector'))
        print("==================== Chain1 execute Ebd ==================")

        kkm = input.get('model')
        res = kkm.invoke("你是哪个模型").content
        return res
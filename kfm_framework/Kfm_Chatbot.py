from kfm_framework.KfmComponentFactory import KfmComponentFactory
from kfm_framework.public import Dict, Any

from kfm_core.kfm_sys.log_config import setup_logger

kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"kfm_chatbot initialization")
# 主类
class Kfm_Chatbot:
    def __init__(self, config: Dict[str, Any]):
        kfm_logger.debug("LLM is initialization")
        kfm_logger.debug("====================== LLM is initialization ======================")
        self.model = KfmComponentFactory.create_model(config['kfm_model'], config['kfm_model_param'])
        self.template = KfmComponentFactory.create_template(config['kfm_template'])
        self.vector = KfmComponentFactory.create_vector(config['kfm_vector'], config['kfm_knowledge_lib_param'])
        self.embedding = KfmComponentFactory.create_embedding(config['kfm_embedding'])
        self.chain = KfmComponentFactory.create_chain(config['kfm_chain'])

        self.chain_dict={}

    def response(self, input: str, user_id: str, session_id: str) -> str:
        vectorized = self.vector.vectorize(input)
        embedded = self.embedding.embed(vectorized)
        processed = self.model.process(embedded)
        templated = self.template.apply(processed)
        self.chain_dict = {
            "vector": vectorized,
            "kfm_embedding": embedded,
            "model": processed,
            "template": templated
        }
        print("chain_dict")
        print(type(self.chain_dict))
        return self.chain.execute(self.chain_dict)


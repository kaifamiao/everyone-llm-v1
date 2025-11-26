
from kfm_framework.interface.kfm_model.KfmModel import KfmModel
from kfm_framework.imp.kfm_model.KfmModel1 import KfmModel1
from kfm_framework.imp.kfm_model.KfmModel2 import KfmModel2

from kfm_framework.interface.kfm_template.KfmTemplate import KfmTemplate
from kfm_framework.imp.kfm_template.KfmTemplate1 import KfmTemplate1
from kfm_framework.imp.kfm_template.KfmTemplate2 import KfmTemplate2

from kfm_framework.interface.kfm_vector.KfmVector import KfmVector
from kfm_framework.imp.kfm_vector.Vector2 import Vector2
from kfm_framework.imp.kfm_vector.Vector1 import Vector1


from kfm_framework.interface.kfm_chain.KfmChain import KfmChain
from kfm_framework.imp.kfm_chain.Chain2 import Chain2
from kfm_framework.imp.kfm_chain.Chain1 import Chain1
from kfm_framework.imp.kfm_chain.China_Agent1 import China_Agent1

from kfm_framework.interface.kfm_embed.KfmEmbedding import KfmEmbedding
from kfm_framework.imp.kfm_embed.Embedding2 import Embedding2
from kfm_framework.imp.kfm_embed.Embedding1 import Embedding1





from kfm_framework.public import Dict,Any

# 接口定义

# 工厂类
class KfmComponentFactory:
    @staticmethod
    def create_model(model_name: str, params: Dict[str, Any]) -> KfmModel:
        models = {
            "kfm_model1": KfmModel1,
            "kfm_model2": KfmModel2,
        }
        return models[model_name](params)

    @staticmethod
    def create_template(template_name: str) -> KfmTemplate:
        templates = {
            "kfm_template1": KfmTemplate1,
            "kfm_template2": KfmTemplate2,
        }
        return templates[template_name]()

    @staticmethod
    def create_vector(vector_name: str, params: Dict[str, Any]) -> KfmVector:
        vectors = {
            "vector1": Vector1,
            "vector2": Vector2,
        }
        return vectors[vector_name](params)

    @staticmethod
    def create_embedding(embedding_name: str) -> KfmEmbedding:
        embeddings = {
            "embedding1": Embedding1,
            "embedding2": Embedding2,
        }
        return embeddings[embedding_name]()

    @staticmethod
    def create_chain(chain_name: str) -> KfmChain:
        chains = {
            "chain1": Chain1,
            "chain2": Chain2,
            "chain3": China_Agent1
        }
        return chains[chain_name]()

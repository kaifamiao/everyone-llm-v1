from kfm_framework.interface.kfm_embed.KfmEmbedding import KfmEmbedding
from kfm_framework.public import *
class Embedding2(KfmEmbedding):
    def embed(self, text: str) -> Any:
        return f"Embedded by Embedding2: {text}"
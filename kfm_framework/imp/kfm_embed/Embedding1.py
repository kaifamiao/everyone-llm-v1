from kfm_framework.interface.kfm_embed.KfmEmbedding import KfmEmbedding
from kfm_framework.public import *
class Embedding1(KfmEmbedding):
    def embed(self, text: str) -> Any:
        return f"Embedded by Embedding1: {text}"
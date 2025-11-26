from kfm_framework.interface.kfm_vector.KfmVector import KfmVector

from kfm_framework.public import *
class Vector1(KfmVector):
    def __init__(self, params: Dict[str, Any]):
        self.params = params

    def vectorize(self, text: str) -> Any:
        return f"Vectorized by Vector1: {text}"
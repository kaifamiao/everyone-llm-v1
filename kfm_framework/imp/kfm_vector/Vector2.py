from kfm_framework.interface.kfm_vector.KfmVector import KfmVector

from kfm_framework.public import *
class Vector2(KfmVector):
    def __init__(self, params: Dict[str, Any]):
        self.params = params

    def vectorize(self, text: str) -> Any:
        print(f"vector 2 {self.params}")
        return f"Vectorized by Vector2: {text}"
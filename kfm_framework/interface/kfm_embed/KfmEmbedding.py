from kfm_framework.public import *

class KfmEmbedding(ABC):
    @abstractmethod
    def embed(self, text: str) -> Any:
        pass

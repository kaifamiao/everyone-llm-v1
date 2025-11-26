from kfm_framework.public import *
class KfmVector(ABC):
    @abstractmethod
    def vectorize(self, text: str) -> Any:
        pass
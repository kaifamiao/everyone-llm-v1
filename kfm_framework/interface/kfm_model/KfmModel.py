from kfm_framework.public import *
class KfmModel(ABC):
    @abstractmethod
    def process(self, input: str) -> str:
        pass
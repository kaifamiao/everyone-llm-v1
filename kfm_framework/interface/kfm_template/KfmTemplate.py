from kfm_framework.public import *

class KfmTemplate(ABC):
    @abstractmethod
    def apply(self, content: str) -> str:
        pass
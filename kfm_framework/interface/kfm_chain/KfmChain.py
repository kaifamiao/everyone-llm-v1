from kfm_framework.public import *

class KfmChain(ABC):
    @abstractmethod
    def execute(self, input: Dict) -> object:
        pass

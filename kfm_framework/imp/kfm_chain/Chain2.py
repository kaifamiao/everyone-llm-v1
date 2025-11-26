from kfm_framework.interface.kfm_chain.KfmChain import KfmChain


class Chain2(KfmChain):
    def execute(self, input: str) -> str:
        return f"Executed by Chain2: {input}"
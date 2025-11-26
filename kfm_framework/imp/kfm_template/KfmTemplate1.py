from kfm_framework.interface.kfm_template.KfmTemplate import KfmTemplate


class KfmTemplate1(KfmTemplate):
    def apply(self, content: str) -> str:
        return f"Template1 applied: {content}"
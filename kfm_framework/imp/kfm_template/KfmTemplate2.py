from kfm_framework.interface.kfm_template.KfmTemplate import KfmTemplate


class KfmTemplate2(KfmTemplate):
    def apply(self, content: str) -> str:
        return f"Template2 applied: {content}"
from langchain_core.messages import HumanMessage

from kfm_config import get_setting_value

import kfm_globals
from kfm_core.kfm_sys.log_config import setup_logger

kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"kfm_globals initialization")
json_data = kfm_globals.json_data
# print(json_data)

kfm_logger.debug(f"Get configuration parameters {kfm_globals.title} ,version {kfm_globals.version}")

from kfm_framework.Kfm_Chatbot import Kfm_Chatbot

# 使用示例
kfm_config = {
    "kfm_model": "kfm_model1",
    "kfm_template": "kfm_template2",
    "kfm_vector": "vector2",
    "kfm_embedding": "embedding2",
    "kfm_chain": "chain3",
    "kfm_knowledge_lib_param": [{"k": 1, "chunk": 200, "overlap": 50}],
    "kfm_model_param": [{"p1": 0, "p2": 0, "p3": 0}, {"top": 1, "max_token": 128}]
}

kfm = Kfm_Chatbot(kfm_config)
response = kfm.response("hello", user_id="", session_id="session_id")

for chunk in response.stream(
        {"input": [HumanMessage(content="数据表多少几条记录?")]},
        config={'configurable': {'session_id': 'xxxxx'}}
):
    print(chunk, end='', flush=True)
    print("\n")
print("\n")
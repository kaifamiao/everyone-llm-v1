from kfm_framework.Kfm_Chatbot import Kfm_Chatbot

# 使用示例
kfm_config = {
    "kfm_model": "kfm_model2",
    "kfm_template": "kfm_template2",
    "kfm_vector": "vector2",
    "kfm_embedding": "embedding2",
    "kfm_chain": "chain3",
    "kfm_knowledge_lib_param": [{"k": 1, "chunk": 200, "overlap": 50}],
    "kfm_model_param": [{"p1": 0, "p2": 0, "p3": 0}, {"top": 1, "max_token": 128}]
}

kfm = Kfm_Chatbot(kfm_config)
response = kfm.response("hello", user_id="", session_id="session_id")
print(response)

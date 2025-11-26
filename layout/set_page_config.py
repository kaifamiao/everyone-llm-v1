import streamlit as st



def set_page_config():
    # 设置页面配置
    st.set_page_config(
        page_title="everyOne LLM 开放测试——文档对话",
        page_icon="📄",
        layout="wide" # "centered" | "wide" | "wide",
        # initial_sidebar_state="expanded",
    )
    st.markdown("set_page_config")
from langchain_core.messages import HumanMessage

from kfm_config import get_setting_value

import kfm_globals
from kfm_core.kfm_sys.log_config import setup_logger
from kfm_core.utils import read_markdown

kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"kfm_globals initialization")
json_data = kfm_globals.json_data

# 读取并显示 logo.md 文件中的内容
print(read_markdown("logo.md"))
kfm_logger.debug(f"Get configuration parameters {kfm_globals.title} ,version {kfm_globals.version}")


import streamlit as st
# 设置页面配置
st.set_page_config(
    page_title="everyOne LLM 开放测试——文档对话",
    page_icon="📄",
    layout="wide" # "centered" | "wide" | "wide",
    # initial_sidebar_state="expanded",
)
sidebar_s=st.sidebar.empty()
main_s=st.container()

row1,row2 = st.columns([1, 3])
def sidebar():
    sidebar_s.info(
        "This application identifies the crop health in the picture.")
sidebar()
# def main():
#     main_s.title(f"💬💬{kfm_globals.title}聊天机器人")
#     main_s.markdown(f"> {kfm_globals.title}")
#
# if __name__ == '__main__':
#     print()
#     sidebar_s()
#     main()
import streamlit as st

# 主区域
st.header("主区域")

# 主区域的第一行，包含三列
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("第一行 - 列 1")
    st.write("这是第一列的内容")

with col2:
    st.subheader("第一行 - 列 2")
    st.write("这是第二列的内容")

with col3:
    st.subheader("第一行 - 列 3")
    st.write("这是第三列的内容")

# 主区域的第二行，包含一列
st.subheader("第二行")
st.write("这是第二行的内容")

# 主区域的第三行，包含六列
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.write("第六列 - 列 1")

with col2:
    st.write("第六列 - 列 2")

with col3:
    st.write("第六列 - 列 3")

with col4:
    st.write("第六列 - 列 4")

with col5:
    st.write("第六列 - 列 5")

with col6:
    st.write("第六列 - 列 6")

# 主区域的第四行，包含一列
st.subheader("第四行")
st.write("这是第四行的内容")

# 侧边栏区域
with st.sidebar:
    st.header("侧边栏")

    # 侧边栏第一行，包含两列
    col1, col2 = st.columns(2)

    with col1:
        st.write("侧边栏第一行 - 列 1")

    with col2:
        st.write("侧边栏第一行 - 列 2")

    # 侧边栏中间部分
    st.write("侧边栏中间的内容")

    # 侧边栏
    with st.sidebar:
        st.header("侧边栏")

        with st.expander("展开部分 1"):
            st.write("侧边栏内容行 1")

        with st.expander("展开部分 2"):
            st.write("侧边栏内容行 2")

        with st.expander("展开部分 3"):
            st.write("侧边栏内容行 3")
    # 侧边栏最后一行，包含四列
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("侧边栏最后一行 - 列 1")

    with col2:
        st.write("侧边栏最后一行 - 列 2")

    with col3:
        st.write("侧边栏最后一行 - 列 3")

    with col4:
        st.write("侧边栏最后一行 - 列 4")

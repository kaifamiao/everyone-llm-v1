import os

import streamlit
from PIL import Image
from io import BytesIO
import base64

from kfm_core.kfm_sys.log_config import setup_logger

logger = setup_logger(__name__)



def set_chat_name(prompt, length=10, placeholder="..."):
    # 提取前6个字符，如果字符串长度不足10个字符，则用placeholder补足
    chat_name = prompt[:length] + placeholder[:(length - len(prompt))] if len(prompt) < length else prompt[:length]
    return chat_name


def showlogo(st):
    logger.debug("initialization sidebar && Showlogo is running...")
    logger.debug("图片链接和目标URL")
    # 图片链接和目标URL
    # 加载图片
    print("\t"+os.path.dirname(os.path.abspath(__file__)) + "/images/logo9.png")
    print("\t"+os.path.dirname(os.path.abspath(__file__)))

    logos = Image.open("./images/logo12.png")
    logo = logos.resize((200, 50))  # 200是宽度，50是高度

    # 将图片转换为base64编码
    buffered = BytesIO()
    logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 创建带有链接的HTML
    html = f'''
        <a href="/" target="_self">
            <img src="data:image/png;base64,{img_str}" width="200" height="50">
        </a>
    '''

    # 在侧边栏中显示带有链接的图片
    st.markdown(html, unsafe_allow_html=True)


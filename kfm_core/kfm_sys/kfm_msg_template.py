# alert_module.py
import time

import streamlit as st
import streamlit_antd_components as sac

def toast_alert(message):
    st.toast(message)

@st.dialog("  ")
def dia1_alert(message, alert_type="warning"):
    icon, bg_color, text_color = get_alert_styles(alert_type)
    st.markdown(f'<p style="color:{text_color};">{message}</p>', unsafe_allow_html=True)

@st.dialog(" 提示 ")
def dia2_alert(message, alert_type="warning"):
    if alert_type == 'info':
        st.info(message)
    elif alert_type == 'success':
        st.success(message)
    elif alert_type == 'warning':
        st.warning(message)
    elif alert_type == 'error':
        st.error(message)
    else:
        st.write(message)  # 如果提供了未知的类型，则直接显示文本

def show_alert(message, alert_type='info'):
    """
    显示一个通用的提示框。
    :param message: 要显示的提示信息
    :param alert_type: 提示框的类型，可以是 'info', 'success', 'warning', 'error'
    """
    alert_data = None
    if alert_type == 'info':
        alert_data = st.info(message)
    elif alert_type == 'success':
        alert_data = st.success(message)
    elif alert_type == 'warning':
        alert_data = st.warning(message)
    elif alert_type == 'error':
        alert_data = st.error(message)
    else:
        alert_data = st.write(message)  # 如果提供了未知的类型，则直接显示文本
    # 等待3秒后清除提示框
    time.sleep(2)
    alert_data.empty()

def vote_alert(message, alert_type='info'):
    # 不同类型对应不同的图标
    icon, bg_color, text_color = get_alert_styles(alert_type)

    placeholder = st.empty()  # 创建一个占位符

    with placeholder.container():
        st.markdown(
            f"""
            <div style="
                position: fixed;
                top: 10%;
                right: 20px;
                z-index: 1000;
                padding: 10px 20px;
                border-radius: 8px;
                background-color: {bg_color};
                color: {text_color};
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-weight: bold;
            ">
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 10px;">{icon}</span>
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 提示框3秒后自动关闭
    time.sleep(3)
    placeholder.empty()


def sac_alert(label, message, alert_type):
    # color:
    # 默认为info，取值有：info、success、warning、error、dark、grey、各种颜色
    sac.alert(label=label, description=message, color=alert_type, banner=[False, True], icon=True, closable=True)


def get_alert_styles(alert_type):
    if alert_type == 'success':
        return "✔️", "#E6F4EA", "#2D6A4F"
    elif alert_type == 'warning':
        return "⚠️", "#FFF3CD", "#856404"
    elif alert_type == 'error':
        return "❌", "#F8D7DA", "#721C24"
    else:
        return "ℹ️", "#D1ECF1", "#0C5460"


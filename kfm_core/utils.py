# kfm_config.py
import logging
import os
import json

from kfm_config import get_project_root


# def get_project_root():
#     # 获取当前工作目录
#     current_directory = os.getcwd()
#
#     # 获取上级目录
#     parent_directory = os.path.dirname(current_directory)
#     return parent_directory
#     # return os.path.dirname(os.path.abspath(__file__))


def get_setting_value(para_name, json_data):
    try:
        data = json.loads(json_data)
        for item in data:
            if item['ParaName'] == para_name:
                return item['ParaValue']
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def read_markdown(filename):
    # 读取并显示 sidebar_content.md 文件中的内容
    filepath = os.path.join(get_project_root(), 'content/')
    markdown_file = filepath + filename
    logging.warn(f"Reading {markdown_file} file.")
    sidebar_content = "ERROR"
    if os.path.exists(markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as file:
            sidebar_content = file.read()
    else:
        sidebar_content = f"**content file `{filename}` not found.**"
    return sidebar_content


def read_html(filename):
    filepath = os.path.join(get_project_root(), 'content/')
    html_file = filepath + filename
    print(html_file)
    html_content = "ERROR"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
    else:
        html_content = "<p style='color:red'>ERROR!</p>"
    return html_content


def out_html(st: object, sts: int, filename: object) -> object:
    if sts == 0:
        st.sidebar.markdown(read_html(filename), unsafe_allow_html=True)
    else:
        st.markdown(read_html(filename), unsafe_allow_html=True)

import streamlit.components.v1 as components
def com_out_html(sts:int,filename):

    components.html(read_html(filename))
    # components.html(read_html(filename), height=600, scrolling=False)


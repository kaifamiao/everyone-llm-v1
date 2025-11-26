# kfm_config.py
import json
import os
def get_project_root():
    # 获取当前工作目录
    return os.path.dirname(os.path.abspath(__file__))

system_path =get_project_root()
def get_system_path():
    return system_path



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



from colorama import Fore, Style, init
init()
def qqqq(str):
    return Fore.LIGHTWHITE_EX + str + Style.RESET_ALL

def rrrr(str):
    return Fore.RED + str + Style.RESET_ALL

def mmmm(str):
    return Fore.MAGENTA + str + Style.RESET_ALL

def yyyy(str):
    return Fore.YELLOW + str + Style.RESET_ALL


import re
def extract_link(text):
    # 定义正则表达式模式，用于匹配方括号内的内容
    pattern = r'\[([^\]]+)\]'

    # 使用 re.search 查找匹配的内容
    match = re.search(pattern, text)

    # 如果找到匹配的内容，返回匹配的组（即方括号内的内容）
    if match:
        return match.group(1)
    else:
        return None


def extract_second_link(text):
    # 定义正则表达式模式，用于匹配第二个方括号内的内容
    pattern = r'\[[^\]]+\]\[\s*([^\]]+)\s*\]'

    # 使用 re.search 查找匹配的内容
    match = re.search(pattern, text)

    # 如果找到匹配的内容，返回匹配的组（即第二个方括号内的内容）
    if match:
        return match.group(1)
    else:
        return None




def read_markdown(filename):

    # 读取并显示 sidebar_content.md 文件中的内容
    filepath = os.path.join(get_project_root(), 'content/')
    markdown_file = filepath + filename
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


def ppppp(text, color="red"):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    if color not in colors:
        raise ValueError(f"Unsupported color: {color}")

    # 将 text 转换为字符串
    # text_str = str(text)

    colored_text = f"{colors[color]}{text}{colors['reset']}"
    print(colored_text)

def pppppp(text, color="red"):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    if color not in colors:
        raise ValueError(f"Unsupported color: {color}")

    # 将 text 转换为字符串
    # text_str = str(text)

    colored_text = f"{colors[color]}{text}{colors['reset']}"
    return colored_text
# 示例用法
# print_colored_text("Hello, World!", "red")
# print_colored_text(["Hello", "World"], "green")
# print_colored_text({"message": "Hello, World!"}, "blue")
# print_colored_text(42, "yellow")
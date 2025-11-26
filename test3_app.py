import streamlit as st

# 侧边栏布局
with st.sidebar:
    # 第一行，两个按钮，按列
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sidebar Btn 1"):
            st.session_state['output'] = "Sidebar Btn 1 Clicked"
    with col2:
        if st.button("Sidebar Btn 2"):
            st.session_state['output'] = "Sidebar Btn 2 Clicked"

    # 第二行到第三行，分别有 expander 和按钮
    with st.expander("Expander 1"):
        if st.button("Expander 1 Btn"):
            st.session_state['output'] = "Expander 1 Btn Clicked"

    with st.expander("Expander 2"):
        if st.button("Expander 2 Btn"):
            st.session_state['output'] = "Expander 2 Btn Clicked"

    # 第四行按钮
    if st.button("Sidebar Btn 3"):
        st.session_state['output'] = "Sidebar Btn 3 Clicked"

    # 第五行，4列
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Col 1 Btn"):
            st.session_state['output'] = "Sidebar Col 1 Btn Clicked"
    with col2:
        if st.button("Col 2 Btn"):
            st.session_state['output'] = "Sidebar Col 2 Btn Clicked"
    with col3:
        if st.button("Col 3 Btn"):
            st.session_state['output'] = "Sidebar Col 3 Btn Clicked"
    with col4:
        if st.button("Col 4 Btn"):
            st.session_state['output'] = "Sidebar Col 4 Btn Clicked"

# Main 主窗口布局
# 第一行，4列
st.write("## Main Layout")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Main Row1 Col1"):
        st.session_state['output'] = "Main Row1 Col1 Clicked"
with col2:
    if st.button("Main Row1 Col2"):
        st.session_state['output'] = "Main Row1 Col2 Clicked"
with col3:
    if st.button("Main Row1 Col3"):
        st.session_state['output'] = "Main Row1 Col3 Clicked"
with col4:
    if st.button("Main Row1 Col4"):
        st.session_state['output'] = "Main Row1 Col4 Clicked"

# 第二行，3列
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Main Row2 Col1"):
        st.session_state['output'] = "Main Row2 Col1 Clicked"
with col2:
    if st.button("Main Row2 Col2"):
        st.session_state['output'] = "Main Row2 Col2 Clicked"
with col3:
    if st.button("Main Row2 Col3"):
        st.session_state['output'] = "Main Row2 Col3 Clicked"

# 第三行，1列 (用于显示点击事件)
if 'output' not in st.session_state:
    st.session_state['output'] = "No Button Clicked Yet"
st.write("### Main Row 3 - Output: ")
st.write(st.session_state['output'])

# 第四行，1列
if st.button("Main Row4 Btn"):
    st.session_state['output'] = "Main Row4 Btn Clicked"

# 第五行，4列
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Main Row5 Col1"):
        st.session_state['output'] = "Main Row5 Col1 Clicked"
with col2:
    if st.button("Main Row5 Col2"):
        st.session_state['output'] = "Main Row5 Col2 Clicked"
with col3:
    if st.button("Main Row5 Col3"):
        st.session_state['output'] = "Main Row5 Col3 Clicked"
with col4:
    if st.button("Main Row5 Col4"):
        st.session_state['output'] = "Main Row5 Col4 Clicked"

# 第六行，8列
cols = st.columns(8)
for i, col in enumerate(cols):
    with col:
        if st.button(f"Main Row6 Col{i+1}"):
            st.session_state['output'] = f"Main Row6 Col{i+1} Clicked"

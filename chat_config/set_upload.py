import streamlit as st
import os
import shutil
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from kfm_config import get_project_root, rrrr, yyyy
from kfm_core.kfm_sys.log_config import setup_logger
kfm_logger = setup_logger(__name__)

# 创建必要的文件夹
UPLOAD_FOLDER_TEMP = get_project_root()+"/kfm_uploadfile_temp2"
UPLOAD_FOLDER_FINAL = get_project_root()+"/kfm_final_uploadfile"
kfm_logger.debug(f"upload file...\n\t UPLOAD_FOLDER : {UPLOAD_FOLDER_TEMP},\n\t UPLOAD_FOLDER_FINAL : {UPLOAD_FOLDER_FINAL}")

os.makedirs(UPLOAD_FOLDER_TEMP, exist_ok=True)

os.makedirs(UPLOAD_FOLDER_FINAL, exist_ok=True)

# 使用普通的字典来跟踪上传进度
upload_progress = {}
UPLOAD_FILE_SUM =2


kfm_logger.debug(f"Document dialogue directory is initialization complete ✅ ")
def upload_file(file):
    global upload_progress
    file_size = file.size
    chunk_size = 1024  # 1KB chunks
    uploaded_size = 0

    with open(os.path.join(UPLOAD_FOLDER_TEMP, file.name), "wb") as f:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            uploaded_size += len(chunk)
            upload_progress[file.name] = min(uploaded_size / file_size, 1.0)

    return file.name

def main(uploaded_files,st):
    global upload_progress
    upload_progress = {}


    if uploaded_files and uploaded_files != st.session_state.get('last_uploaded_files', None):
        if len(uploaded_files) > UPLOAD_FILE_SUM:
            st.error(f"只能上传{UPLOAD_FILE_SUM} 个文件.")
            return

        st.session_state['last_uploaded_files'] = uploaded_files
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 重置进度字典
        upload_progress = {file.name: 0 for file in uploaded_files}

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(upload_file, file) for file in uploaded_files]

            while futures:
                done, futures = concurrent.futures.wait(futures, timeout=0, return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    file_name = future.result()
                    status_text.text(f"Uploaded: {file_name}")

                kfm_logger.warning(f"uploaded_files is {upload_progress.values()}")
                #time.sleep(0.01)

                progress = sum(upload_progress.values()) / len(uploaded_files)

                progress_bar.progress(progress)

        # st.success(f"{file_name} files uploaded successfully!")
        st.toast(f"{file_name} 文件上传成功！", icon="🔔")
        if progress<1:
            progress_bar.progress(100)


    return True
if "session_id" not in st.session_state:
    st.session_state.session_id = ""
def kfm_upload_file(st):

    kfm_logger.debug(f"{yyyy("kfm_upload_file is running...")}")
    uploaded_files = st.file_uploader("开始上传文档", type=["txt", "md", "pdf", "doc", "docx"], accept_multiple_files=True)
    st.write(f"目前支持txt、md、pdf、doc、docx格式的文件上传，文件大小限制在50M以内，可以支持{UPLOAD_FILE_SUM}个文件")
    if main(uploaded_files, st) and st.session_state.session_id=="":
        list_filename=[]
        for list_file in uploaded_files:
            list_filename.append(list_file.name)
            kfm_logger.debug(f"list_file.name is {list_file.name}")
        st.session_state.DOC_DIALOG_FILENAME = list_filename
        kfm_logger.debug(f"91. st.session_state.DOC_DIALOG_FILENAME is {st.session_state.DOC_DIALOG_FILENAME}")
        # for list in uploaded_files:
        #     st.markdown(f"""
        #     - {list.name}
        #     """)
        if uploaded_files:
            if st.button("确认文件，开始对话", key='confirm'):
                print("Confirm ")
                for file in uploaded_files:
                    shutil.copy(os.path.join(UPLOAD_FOLDER_TEMP, file.name),
                                os.path.join(UPLOAD_FOLDER_FINAL, file.name))
                st.success("Files copied to final_uploadfile folder!")
                st.session_state.PAGE_STATE="Ready.."
                st.session_state.DOC_DIALOG_FILENAME = list_filename
                kfm_logger.debug(f"104.st.session_state.DOC_DIALOG_FILENAME is {st.session_state.DOC_DIALOG_FILENAME}")
                kfm_logger.debug(f"104.st.session_state.session_id  {st.session_state.session_id }")
                print("\n\n")
                kfm_logger.debug("st.rerun()\n\n")
                st.rerun()

    # return list_filename

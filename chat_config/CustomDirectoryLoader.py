import os
import chardet
import pdfplumber
from docx import Document
from langchain_community.document_loaders import DirectoryLoader as BaseDirectoryLoader
from concurrent.futures import ThreadPoolExecutor

class CustomDirectoryLoader(BaseDirectoryLoader):
    def __init__(self, directory, glob="*.*", show_progress=True, use_multithreading=True):
        super().__init__(directory, glob, show_progress, use_multithreading)

    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        # 如果chardet未能检测到编码，默认使用utf-8
        if encoding is None:
            encoding = 'utf-8'
        return encoding

    def read_txt(self, file_path):
        encoding = self.detect_encoding(file_path)
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                return f.read()
        except UnicodeDecodeError:
            # 如果仍然失败，尝试使用不同的编码
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except Exception as e:
                print(f"Failed to read {file_path} with encoding {encoding}: {e}")
                return None

    def read_pdf(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                content = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content.append(text)
                return '\n'.join(content)
        except Exception as e:
            print(f"Failed to read PDF {file_path}: {e}")
            return None

    def read_docx(self, file_path):
        try:
            doc = Document(file_path)
            content = []
            for para in doc.paragraphs:
                content.append(para.text)
            return '\n'.join(content)
        except Exception as e:
            print(f"Failed to read DOCX {file_path}: {e}")
            return None

    def process_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return self.read_txt(file_path)
        elif ext == '.pdf':
            return self.read_pdf(file_path)
        elif ext == '.docx':
            return self.read_docx(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return None

    def load_files(self):
        files = [os.path.join(root, file)
                 for root, _, filenames in os.walk(self.directory)
                 for file in filenames if file.endswith(self.glob)]

        results = []
        if self.use_multithreading:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(self.process_file, files))
        else:
            results = [self.process_file(file) for file in files]

        # 过滤掉None的结果
        results = [result for result in results if result is not None]
        return results

# 使用示例
# file_path = 'your_directory_path'
# loader = CustomDirectoryLoader(file_path, glob="*.*", show_progress=True, use_multithreading=True)
# documents = loader.load_files()
#
# for document in documents:
#     if document:
#         print(document)

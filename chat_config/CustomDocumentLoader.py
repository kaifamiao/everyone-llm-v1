from typing import AsyncIterator, Iterator
import chardet
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class CustomDocumentLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def _detect_encoding(self):
        with open(self.file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding']

    def lazy_load(self) -> Iterator[Document]:
        encodings_to_try = ['utf-8', 'latin-1', 'ascii', 'gbk', 'gb2312']

        for encoding in encodings_to_try:
            try:
                with open(self.file_path, encoding=encoding) as f:
                    line_number = 0
                    for line in f:
                        yield Document(
                            page_content=line,
                            metadata={"line_number": line_number, "source": self.file_path},
                        )
                        line_number += 1
                return  # If successful, exit the function
            except UnicodeDecodeError:
                continue  # Try the next encoding

        # If none of the encodings work, try to detect the encoding
        detected_encoding = self._detect_encoding()
        try:
            with open(self.file_path, encoding=detected_encoding) as f:
                line_number = 0
                for line in f:
                    yield Document(
                        page_content=line,
                        metadata={"line_number": line_number, "source": self.file_path},
                    )
                    line_number += 1
        except UnicodeDecodeError:
            raise ValueError(
                f"Unable to decode the file with any known encoding. Detected encoding was {detected_encoding}")

    async def alazy_load(self) -> AsyncIterator[Document]:
        import aiofiles
        encodings_to_try = ['utf-8', 'latin-1', 'ascii', 'gbk', 'gb2312']

        for encoding in encodings_to_try:
            try:
                async with aiofiles.open(self.file_path, encoding=encoding) as f:
                    line_number = 0
                    async for line in f:
                        yield Document(
                            page_content=line,
                            metadata={"line_number": line_number, "source": self.file_path},
                        )
                        line_number += 1
                return  # If successful, exit the function
            except UnicodeDecodeError:
                continue  # Try the next encoding

        # If none of the encodings work, try to detect the encoding
        detected_encoding = self._detect_encoding()
        try:
            async with aiofiles.open(self.file_path, encoding=detected_encoding) as f:
                line_number = 0
                async for line in f:
                    yield Document(
                        page_content=line,
                        metadata={"line_number": line_number, "source": self.file_path},
                    )
                    line_number += 1
        except UnicodeDecodeError:
            raise ValueError(
                f"Unable to decode the file with any known encoding. Detected encoding was {detected_encoding}")

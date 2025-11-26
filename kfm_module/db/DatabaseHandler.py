import os
import sqlite3
import json
import pandas as pd
import threading
from dotenv import load_dotenv
from dicttoxml import dicttoxml

from kfm_config import get_project_root
from kfm_core.kfm_sys.log_config import setup_logger

logger = setup_logger(__name__)

class DatabaseHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DatabaseHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        if not hasattr(self, 'initialized'):  # 确保 __init__ 只执行一次
            self.initialized = True
            logger.debug(f"CLASS DatabaseHandler initialization")
            load_dotenv()
            self.database = os.getenv('SYSDATABASE')

            logger.debug(f"os.getenv('SYSDATABASE') :  {self.database}")
            if not self.database:
                raise ValueError("SYSDATABASE environment variable not set.")
            # 获取项目根目录
            project_root = get_project_root()

            # 将相对路径转换为绝对路径
            self.database = os.path.join(project_root, self.database)
            # 确保目录存在
            os.makedirs(os.path.dirname(self.database), exist_ok=True)
            logger.info(f"sqlite3 database path: {self.database}")

            # 连接数据库
            try:
                self.conn = sqlite3.connect(self.database, check_same_thread=False)
                self.cursor = self.conn.cursor()
            except sqlite3.Error as e:
                print(f"An error occurred connecting to the database: {e}")
                raise

    def execute_dml(self, query, params=()):
        """Execute DML (insert, update, delete) statements."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def execute_select(self, query, params=(), return_format='rs'):
        """Execute select statements and return results in the specified format."""
        # print("""Execute select statements and return results in the specified format.""")
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            columns = [description[0] for description in self.cursor.description]
            if return_format == 'df':
                return pd.DataFrame(rows, columns=columns)
            elif return_format == 'json':
                result = [dict(zip(columns, row)) for row in rows]
                return json.dumps(result, indent=4)
            elif return_format == 'xml':
                result = [dict(zip(columns, row)) for row in rows]
                return dicttoxml(result, custom_root='results', attr_type=False).decode()
            elif return_format == 'rs':
                print(query)
                return rows
            else:
                return rows

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def __del__(self):
        logger.warn("CLASS DatabaseHandler connection release")
        if hasattr(self, 'conn'):
            self.conn.close()






import os

from kfm_config import get_setting_value
from kfm_core.kfm_sys.log_config import setup_logger
from kfm_module.db.DatabaseHandler import DatabaseHandler

kfm_logger = setup_logger(__name__)
kfm_logger.debug(f"kfm_globals initialization")
class GlobalVars:
    def __init__(self):
        kfm_logger.debug("GlobalVars initialization")
        self._setName = None
        self._setConfig = None
        self._setPath = None

    def set_name(self, value):
        self._setName = value

    def get_name(self):
        return self._setName

    def set_config(self, value):
        self._setConfig = value

    def get_config(self):
        return self._setConfig

    def get_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




Obj = GlobalVars()
db = DatabaseHandler()
kfm_logger.debug(f"Create a global instance of:\n GlobalVars {Obj} , DatabaseHandler {db}")
def get_setting_from_db():
    kfm_logger.info("get_setting_from_db")
    # 假设你使用sqlite3数据库
    select_query: str = "SELECT * FROM setting WHERE user_role = ?"
    kfm_logger.debug(f"{select_query}")
    return db.execute_select(select_query, ('system',), return_format='json')

json_data=get_setting_from_db()
title = get_setting_value("title", json_data)
version = get_setting_value("version", json_data)
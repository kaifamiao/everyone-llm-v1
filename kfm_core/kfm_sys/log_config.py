# log_config.py

import logging
import colorlog
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

from kfm_config import  get_project_root

log_path=get_project_root()
def setup_logger(name, log_dir=log_path+'/logs'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 检查 logger 是否已经有 handlers，如果有，就不再添加
    if not logger.handlers:
        # 控制台处理器（带颜色）
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s|%(name)s| %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'SUCCESS': 'green',
                'CRITICAL': 'red,bg_white',
            }
        ))
        logger.addHandler(console_handler)

        # 文件处理器（每日轮换）
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, f'log_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when='midnight',
            interval=1,
            backupCount=30,  # 保留30天的日志
            encoding='utf-8'
        )
        file_handler.suffix = "%Y%m%d"
        file_handler.extMatch = r"^\d{8}$"
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(file_handler)

    return logger

# 第一版日志
# # log_config.py
#
# import logging
# import colorlog
#
# def setup_logger(name):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.DEBUG)
#
#     # 检查 logger 是否已经有 handlers，如果有，就不再添加
#     if not logger.handlers:
#         handler = colorlog.StreamHandler()
#         handler.setFormatter(colorlog.ColoredFormatter(
#             '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S',
#             log_colors={
#                 'DEBUG': 'cyan',
#                 'INFO': 'green',
#                 'WARNING': 'yellow',
#                 'ERROR': 'red',
#                 'CRITICAL': 'red,bg_white',
#             }
#         ))
#         logger.addHandler(handler)
#
#     return logger

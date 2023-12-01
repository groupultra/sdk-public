# logging_config.py

import datetime
import logging
import os

def configure_logger(name, log_dir="logs"):
    # 确保log文件夹存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 为日志文件生成唯一的文件名（例如：logs/2023-09-09_12-30-00.log）
    log_file = os.path.join(log_dir, f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

logger = configure_logger(__name__)

def log_info(msg, print_to_console=False):
    if print_to_console:
        print(msg)
    logger.info(msg)

def log_error(msg, print_to_console=False):
    if print_to_console:
        print(msg)
    logger.error(msg)
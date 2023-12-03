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

color_dict = {
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan": "\033[1;36m",
    "white": "\033[1;37m"
}
def log(msg, error=False, print_to_console=False, color=None):
    """
    print_color: "31" for red, "32" for green, "33" for yellow, "34" for blue, "35" for magenta, "36" for cyan, "37" for white
    """
    
    if print_to_console:
        if color is not None and color in color_dict:
            print(f"{color_dict[color]}{msg}\033[0m")
        else:
            print(msg)
    if error:
        logger.error(msg)
    else:
        logger.info(msg)
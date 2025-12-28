import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_file_path='furtrack_downloader.log', level=logging.INFO):
    rootLogger = logging.getLogger()
    if rootLogger.handlers:
        return  # logger already configured

    logFormat = "%(asctime)s | %(levelname)s - %(message)s"
    formatter = logging.Formatter(logFormat)

    # this goes to the console
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(logging.WARN)
    rootLogger.addHandler(streamHandler)

    fileHandler = RotatingFileHandler(
        log_file_path, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8'
    )
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(level)
    rootLogger.addHandler(fileHandler)

    rootLogger.setLevel(level)


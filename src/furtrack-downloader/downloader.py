import os
import sys
import logging
from .csv_handler import open_csv_read
from .progress import load_progress, save_progress
from .config import DOWNLOAD_PROGRESS_FILE_PATH


def init_logger():
	return logging.getLogger(__name__)

logger = init_logger()

def download_image():
	print ('Uh oh, not implemented yet!!!')

def downloader():
	base_df = open_csv_read()
	if base_df is None:
		logger.error("CSV file not found. Please run the scraper first.")
		return
	download_progress_index = load_progress(DOWNLOAD_PROGRESS_FILE_PATH)
	print(base_df)
import os
import sys
import logging
import requests
import tkinter as tk
from tkinter import filedialog
from .csv_handler import open_csv_read
from .progress import load_progress, save_progress
from .config import DOWNLOAD_PROGRESS_FILE_PATH


def init_logger():
	return logging.getLogger(__name__)

logger = init_logger()


def save_sidecar_file(download_path, index, character_tags):
	sidecar_filename = os.path.join(download_path, f"{index}")
	try:
		with open(sidecar_filename + ".txt", 'w', encoding='utf-8') as f:
			f.write(character_tags)
		return True
	except OSError as e:
		logger.error(f"Error saving sidecar file for index {index}: {e}")
		return False


def download_image(index, image_url, character_tags, download_path):
	save_sidecar_file(download_path, index, character_tags)

def downloader():
	try:
		DOWNLOAD_ARCHIVE_PATH = filedialog.askdirectory(title="Select Download Directory")
		if not DOWNLOAD_ARCHIVE_PATH:
			logger.warning("No download directory selected, exiting downloader.")
			return
		
		base_df = open_csv_read()
		if base_df is None:
			logger.error("CSV file not found. Please run the scraper first.")
			return
		logger.info("Successfully loaded CSV file.")

		download_progress_index = load_progress(DOWNLOAD_PROGRESS_FILE_PATH)
		if download_progress_index == 10:
			logger.warning("Default download index detected, starting from first entry")
			download_progress_index = base_df.iloc[0,0]
		logger.info(f"Resuming downloads from index: {download_progress_index}")

		# filter dataframe to only entries >= download_progress_index
		main_df = base_df[base_df['index'] >= download_progress_index]
		
		for row in main_df.itertuples():
			index = row.index
			image_url = row.image_url
			characters = str(row.character_tags)

			logger.info(f"Downloading index {index} with characters: {characters}")
			download_image(index, image_url, characters, DOWNLOAD_ARCHIVE_PATH) # placeholder

			# after successful download, save progress
			if save_progress(index, DOWNLOAD_PROGRESS_FILE_PATH):
				logger.info(f"Saved download progress at index {index}")
			else:
				logger.error(f"Failed to save download progress at index {index}")
	except Exception as e:
		logger.error(f"An error occurred during parsing: {e}")
	return
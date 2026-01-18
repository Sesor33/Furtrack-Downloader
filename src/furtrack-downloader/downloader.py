import os
import sys
import time
import random
import logging
import requests
import tkinter as tk
from tkinter import filedialog
from urllib3.exceptions import MaxRetryError, ReadTimeoutError, NewConnectionError
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException
import undetected_chromedriver as uc
from .csv_handler import open_csv_read
from .progress import load_progress, save_progress
from .config import DOWNLOAD_PROGRESS_FILE_PATH, DEFAULT_MAX_DOWNLOAD_INDEX


def init_logger():
	return logging.getLogger(__name__)


logger = init_logger()


def create_driver():
	options = uc.ChromeOptions()
	return uc.Chrome(options=options)


def restart_driver(driver):
	driver.quit()
	return create_driver()


def save_sidecar_file(download_path, index, character_tags):
	sidecar_filename = os.path.join(download_path, f"{index}")
	try:
		with open(sidecar_filename + ".txt", 'w', encoding='utf-8') as f:
			f.write(character_tags)
		return True
	except OSError as e:
		logger.error(f"Error saving sidecar file for index {index}: {e}")
		raise
	except Exception as e:
		logger.error(f"Unexpected error saving sidecar file for index {index}: {e}")
		raise


def download_image(driver, index, image_url, character_tags, download_path):
	try:
		image_save_path = os.path.join(download_path, f"{index}{os.path.splitext(image_url)[1]}")
		
		driver.get(image_url)
		time.sleep(1)
		
		# super weird way to get image data from selenium
		image_data = driver.execute_script("""
			let canvas = document.createElement('canvas');
			let img = document.querySelector('img');
			if (!img) {
				let imgElement = new Image();
				imgElement.src = arguments[0];
				canvas.width = imgElement.width;
				canvas.height = imgElement.height;
				canvas.getContext('2d').drawImage(imgElement, 0, 0);
			} else {
				canvas.width = img.width;
				canvas.height = img.height;
				canvas.getContext('2d').drawImage(img, 0, 0);
			}
			return canvas.toDataURL('image/png').split(',')[1];
		""", image_url)
		
		if image_data:
			import base64
			with open(image_save_path, 'wb') as f:
				f.write(base64.b64decode(image_data))
			logger.info(f"Successfully downloaded image for index {index}")
			save_sidecar_file(download_path, index, character_tags)
		else:
			logger.error(f"Failed to retrieve image data for index {index}")
			return
	# closing my laptop causes this, ensure it ends program without exploding the logs
	except InvalidSessionIdException as e:
		logger.error(f"Invalid session for index {index}: {e}")
		sys.exit(1)
	except Exception as e:
		logger.error(f"Error downloading image for index {index}: {e}")
		return


def downloader(max_index=DEFAULT_MAX_DOWNLOAD_INDEX):
	try:
		DOWNLOAD_ARCHIVE_PATH = filedialog.askdirectory(title="Select Download Directory")
		if not DOWNLOAD_ARCHIVE_PATH:
			logger.warning("No download directory selected, exiting downloader.")
			return
		
		driver = create_driver()

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

		main_df = base_df[base_df['index'] >= download_progress_index]
		
		for row in main_df.itertuples():
			retries = 0
			while retries < 3:
				try:
					index = row.index
					if index > max_index:
						logger.info(f"Reached max download index {max_index}, stopping downloader.")
						print("Download complete.")
						return
					image_url = row.image_url
					characters = str(row.character_tags)

					logger.info(f"Downloading index {index} with characters: {characters}")
					download_image(driver, index, image_url, characters, DOWNLOAD_ARCHIVE_PATH)

					if save_progress(index, DOWNLOAD_PROGRESS_FILE_PATH):
						logger.info(f"Saved download progress at index {index}")
					else:
						logger.error(f"Failed to save download progress at index {index}")
				
					time.sleep(random.uniform(0.1, 1)) 
					break
				except (MaxRetryError, ReadTimeoutError, NoSuchWindowException) as e:
					retries += 1
					if retries < 3:
						logger.error(f"{type(e).__name__} while processing index {index}, Retry count: {retries}: {e}")
						driver = restart_driver(driver)
					else:
						logger.error(f"Max retries reached for index {index} due to {type(e).__name__}: {e}")
						sys.exit(1)
	except Exception as e:
		logger.error(f"An error occurred during parsing: {e}")
	finally:
		driver.quit()
		logger.info("Webdriver closed")
	return
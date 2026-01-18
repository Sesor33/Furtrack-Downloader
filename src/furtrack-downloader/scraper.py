import sys
import time
import random
import logging
import undetected_chromedriver as uc
from urllib3.exceptions import MaxRetryError, ReadTimeoutError
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException
from bs4 import BeautifulSoup
from .progress import load_progress, save_progress
from .csv_handler import open_csv_write
from .config import BASE_URL, DEFAULT_MAX_SCRAPING_INDEX


def init_logger():
	return logging.getLogger(__name__)

logger = init_logger()


def restart_driver(driver):
	driver.quit()
	return create_driver()

def create_driver():
	options = uc.ChromeOptions()
	options.add_experimental_option(
		"prefs", {"profile.managed_default_content_settings.images": 2}
	)
	return uc.Chrome(options=options)


def scrape_page(driver, index, retries=0):
	try:
		driver.get(BASE_URL.format(index))
		time.sleep(random.uniform(0.1, 0.2)) # so js loads

		soup = BeautifulSoup(driver.page_source, "html5lib")

		image_tag = soup.find("meta", {"property": "og:image"})
		characters = [div.text.strip() for div in soup.find_all("div", {"class": "plz-tag-primary character"})]

		if image_tag and characters:
			return image_tag["content"], characters

		return None, None
	# closing my laptop causes this, ensure it ends program without exploding the logs
	except InvalidSessionIdException as e:
		logger.error(f"Invalid session for index {index}: {e}")
		sys.exit(1)
	except MaxRetryError as e:
		raise
	# tries to handle a weird error where the Chrome window will hang
	except ReadTimeoutError as e:
		raise
	except NoSuchWindowException as e:
		raise
	except Exception as e:
		logger.error(f"Error scraping index {index}: {e}")
		return None, None


def build_csv(max_index=DEFAULT_MAX_SCRAPING_INDEX):
	start_index = load_progress()
	driver = create_driver()
	csv_file, writer = open_csv_write()

	try:
		for index in range(start_index, max_index+1):
			retries = 0
			while retries < 3:
				try:
					image_url, characters = scrape_page(driver, index)
					if image_url:
						writer.writerow([index, image_url, ",".join(characters)])
						logger.info(f"Characters found at index {index}: {', '.join(characters)}")
					logger.info(f"Processed index: {index}")

					save_progress(index)
					logger.debug(f"Progress saved at index: {index}")
					break
				except (MaxRetryError, ReadTimeoutError, NoSuchWindowException) as e:
					retries += 1
					if retries < 3:
						logger.error(f"{type(e).__name__} while processing index {index}, Retry count: {retries}: {e}")
						driver = restart_driver(driver)
					else:
						logger.error(f"Max retries reached for index {index} due to {type(e).__name__}: {e}")
						sys.exit(1)
	finally:
		driver.quit()
		logger.info("Webdriver closed")
		csv_file.close()
		logger.info("CSV file closed")
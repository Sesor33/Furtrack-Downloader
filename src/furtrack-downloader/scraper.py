import time
import random
import logging
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from .logging_config import setup_logging
from .progress import load_progress, save_progress
from .csv_handler import open_csv
from .config import BASE_URL, DEFAULT_MAX_INDEX

def init_logger():
    return logging.getLogger(__name__)

logger = init_logger()

def create_driver():
    options = uc.ChromeOptions()
    options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    return uc.Chrome(options=options)


def scrape_page(driver, index):
    driver.get(BASE_URL.format(index))
    
    soup = BeautifulSoup(driver.page_source, "html5lib")

    image_tag = soup.find("meta", {"property": "og:image"})
    characters = [div.text.strip() for div in soup.find_all("div", {"class": "plz-tag-primary character"})]

    if image_tag and characters:
        return image_tag["content"], characters

    return None, None

def build_csv(max_index=DEFAULT_MAX_INDEX):
    start_index = load_progress()
    driver = create_driver()
    csv_file, writer = open_csv()

    try:
        for index in range(start_index, max_index):
            image_url, characters = scrape_page(driver, index)
            if image_url:
                writer.writerow([index, image_url, ",".join(characters)])
                logger.info(f"Characters found at index {index}: {', '.join(characters)}")
            logger.info(f"Processed index: {index}")

            save_progress(index)
            logger.debug(f"Progress saved at index: {index}")
    finally:
        driver.quit()
        logger.info("Webdriver closed")
        csv_file.close()
        logger.info("CSV file closed")
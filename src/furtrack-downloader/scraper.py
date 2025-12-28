import time
import random
import logging
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from .progress import load_progress, save_progress
from .csv_handler import open_csv
from .config import BASE_URL, DEFAULT_MAX_INDEX

def init_logger():
    return

def create_driver():
    options = uc.ChromeOptions()
    options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    return uc.Chrome(options=options)


def scrape_page(driver, index):
    driver.get(BASE_URL.format(index))
    time.sleep(random.uniform(0.1, 0.2))

    soup = BeautifulSoup(driver.page_source, "html5lib")

    image_tag = soup.find("meta", {"property": "og:image"})
    characters = [
        div.text.strip()
        for div in soup.find_all("div", {"class": "plz-tag-primary character"})
    ]

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

            save_progress(index)
    finally:
        driver.quit()
        csv_file.close()
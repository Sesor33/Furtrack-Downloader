import time
import random
import csv
import os
from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Constants
CSV_HEADERS = ["index", "image_url", "character_tags"] 
CSV_FILE_PATH = "furtrack_image_lib.csv"
BASE_URL = "https://www.furtrack.com/p/{}"
CURRENT_INDEX = 126355
CURRENT_MAX_INDEX = 1000000


def check_csv_for_data(reader):
	try:
		next(reader) 
		return True
	except StopIteration:
		return False


def main():
	# Initialize browser options
	chrome_options = uc.ChromeOptions()
	
	# Initialize browser
	driver = uc.Chrome(options=chrome_options)

	file_is_new = not os.path.exists(CSV_FILE_PATH)
	with open(CSV_FILE_PATH, 'a+', encoding='utf-8', newline='') as csv_file:
		writer = csv.writer(csv_file)
		if file_is_new:
			writer.writerow(CSV_HEADERS)

		try:
			for index in range(CURRENT_INDEX, CURRENT_MAX_INDEX):
				# Navigate to URL
				driver.get(BASE_URL.format(index))
				time.sleep(random.uniform(1, 3))
				
				# Wait for JS to execute and parse the page source with BeautifulSoup
				soup = BeautifulSoup(driver.page_source, 'html5lib')
				
				# Extract og:image URL
				image_tag = soup.find('meta', {'property': 'og:image'})
				# Find all divs with class value of "plz-tag-primary character" and get values,
				# even if div is nested
				characters = [div.text.strip() for div in soup.find_all('div', {'class': 'plz-tag-primary character'})]

				if image_tag and characters:
					writer.writerow([str(index), image_tag['content'], ','.join(characters)])
				
				# Output progress to console
				print(f"Processed {index} of {CURRENT_MAX_INDEX}")

				time.sleep(random.uniform(2, 5))
		finally:
			# Clean up
			driver.quit()
			csv_file.close()


if __name__ == "__main__":
	main()
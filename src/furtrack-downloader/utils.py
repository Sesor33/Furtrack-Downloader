import time
import random
import csv
import sys
import os
from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def check_csv_for_data(reader):
	try:
		next(reader) 
		return True
	except StopIteration:
		return False


def cleanup(csv_file, index):
	csv_file.close()
	save_progress(index)
	return


def get_max_index():
	while True:
		try:
			user_input = input("Enter the maximum index to process (or press Enter for default): ")
			if not user_input:
				return DEFAULT_MAX_INDEX
			else:
				return int(user_input)
		except ValueError:
			print("Invalid input, please enter an integer")
		
		except KeyboardInterrupt:
			end_program()


def csv_generator():
	# attempt to load progress
	CURRENT_INDEX = load_progress()
	DEFAULT_MAX_INDEX = get_max_index()

	# initialize browser options
	chrome_options = uc.ChromeOptions()

	# disable image loading
	prefs = {"profile.managed_default_content_settings.images": 2}
	chrome_options.add_experimental_option("prefs", prefs)
	
	# initialize browser
	driver = uc.Chrome(options=chrome_options)

	csv_file_is_new = not os.path.exists(CSV_FILE_PATH)
	with open(CSV_FILE_PATH, 'a+', encoding='utf-8', newline='') as csv_file:
		writer = csv.writer(csv_file)
		if csv_file_is_new:
			writer.writerow(CSV_HEADERS)

		try:
			for index in range(CURRENT_INDEX, DEFAULT_MAX_INDEX):
				# Navigate to URL
				driver.get(BASE_URL.format(index))
				time.sleep(random.uniform(0.1, 0.2)) # so js loads
				
				# Wait for JS to execute and parse the page source with BeautifulSoup
				soup = BeautifulSoup(driver.page_source, 'html5lib')
				
				# Extract og:image URL
				image_tag = soup.find('meta', {'property': 'og:image'})
				# Find all divs with class value of "plz-tag-primary character" and get values,
				# even if div is nested
				characters = [div.text.strip() for div in soup.find_all('div', {'class': 'plz-tag-primary character'})]

				if image_tag and characters:
					writer.writerow([str(index), image_tag['content'], ','.join(characters)])
				
				print(f"Processed {index} of {DEFAULT_MAX_INDEX}")

		except KeyboardInterrupt:
			print("Downloader is shutting down...")
			cleanup(csv_file, index)
			end_program()
		
		except Exception as e:
			print(f"Error processing {index}: {str(e)}")
			cleanup(csv_file, index)
			end_program()
		
		finally:
			# clean up
			driver.quit()
			csv_file.close()


def downloader():
	print('Whoops. not implemented yet')
	end_program()


def main():
	while True:
		try:
			option_input = input("Enter '1' to build CSV, '2' to run downloader, and '3' or CTRL+C to exit> ")
			option_input = int(option_input)
			match option_input:
				case 1:
					csv_generator()
				case 2:
					downloader()
				case 3:
					end_program()
				case _:
					print("Invalid Input, please enter a valid input")

		except ValueError:
			print("Invalid Input, please enter a valid input")

		except KeyboardInterrupt:
			end_program()


if __name__ == "__main__":
	main()
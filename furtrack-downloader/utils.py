import time
import random
import csv
import sys
import os
from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Constants
CSV_HEADERS = ["index", "image_url", "character_tags"] 
CSV_FILE_PATH = "furtrack_image_lib.csv"
PROGRESS_FILE_PATH = "progress.arc"
BASE_URL = "https://www.furtrack.com/p/{}"
CURRENT_INDEX = 10
CURRENT_MAX_INDEX = 1000000


def check_csv_for_data(reader):
	try:
		next(reader) 
		return True
	except StopIteration:
		return False


def load_progress(filename=PROGRESS_FILE_PATH):
	try:
		with open(filename, 'r') as progress_file:
			progress_content = progress_file.read()
			if progress_content:
				progress_file.close()
				return int(progress_content.strip())
			else:
				return None
	except Exception as e:
		print(f"Error loading progress file: {e}")
		progress_file.close()
		return None


def save_progress(index, filename=PROGRESS_FILE_PATH):
	try:
		with open(filename, 'w') as progress_file:
			progress_file.write(str(index + 1))
			progress_file.close()
			return True
	except Exception as e:
		print(f"Error saving progress file: {e}")
		progress_file.close()
		return False


def cleanup(csv_file, index):
	csv_file.close()
	save_progress(index)
	print("Progress saved!")
	return


def end_program(exit_code=0):
	print("Goodbye!")
	sys.exit(exit_code)


def get_max_index():
	while True:
		try:
			user_input = input("Enter the maximum index to process (or press Enter for default): ")
			if not user_input:
				return CURRENT_MAX_INDEX
			else:
				return int(user_input)
		except ValueError:
			print("Invalid input, please enter an integer")
		
		except KeyboardInterrupt:
			end_program()


def csv_generator():
	# Attempt to load progress
	CURRENT_INDEX = load_progress()
	CURRENT_MAX_INDEX = get_max_index()

	# Initialize browser options
	chrome_options = uc.ChromeOptions()
	
	# Initialize browser
	driver = uc.Chrome(options=chrome_options)

	csv_file_is_new = not os.path.exists(CSV_FILE_PATH)
	with open(CSV_FILE_PATH, 'a+', encoding='utf-8', newline='') as csv_file:
		writer = csv.writer(csv_file)
		if csv_file_is_new:
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

				time.sleep(random.uniform(0.2, 0.5))

		except KeyboardInterrupt:
			print("Downloader is shutting down...")
			cleanup(csv_file, index)
			end_program()
		
		except Exception as e:
			print(f"Error processing {index}: {str(e)}")
			cleanup(csv_file, index)
			end_program()
		
		finally:
			# Clean up
			driver.quit()
			csv_file.close()


def downloader():
	print('Whoops. not implemented yet')
	end_program()


def main():
	while True:
		try:
			option_input = input("Enter '1' to start downloading, '2' to run downloader, and '3' or CTRL+C to exit> ")
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
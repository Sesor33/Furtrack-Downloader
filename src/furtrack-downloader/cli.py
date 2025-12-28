import sys
from .scraper import build_csv
from .downloader import download
from .config import DEFAULT_MAX_INDEX

def end_program(exit_code=0):
	print("Goodbye!")
	sys.exit(exit_code)

def main():
	while True:
		try:
			option_input = input("Enter '1' to build CSV, '2' to run downloader, and '3' or CTRL+C to exit> ")
			option_input = int(option_input)
			match option_input:
				case 1:
					max_index = input("Enter max index (or press Enter for default): ")
					if not max_index.strip():
						max_index = DEFAULT_MAX_INDEX
					build_csv(max_index)
				case 2:
					download()
				case 3:
					end_program()
				case _:
					print("Invalid Input, please enter a valid input")

		except ValueError:
			print("Invalid Input, please enter a valid input")

		except KeyboardInterrupt:
			end_program()


import csv
import os
from .config import CSV_HEADERS, CSV_FILE_PATH

def open_csv():
	is_new = not os.path.exists(CSV_FILE_PATH)
	csv_file = open(CSV_FILE_PATH, "a+", encoding="utf-8", newline="")
	writer = csv.writer(csv_file)

	if is_new:
		writer.writerow(CSV_HEADERS)

	return csv_file, writer

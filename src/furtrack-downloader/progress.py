from .config import PROGRESS_FILE_PATH, DEFAULT_START_INDEX

def load_progress(filename=PROGRESS_FILE_PATH):
	try:
		with open(filename, 'r') as progress_file:
			progress_content = progress_file.read()
			if progress_content:
				progress_file.close()
				progress_val = int(progress_content.strip())
				print(f'Progress file found! Starting from: {progress_val}')
				return progress_val
			else:
				print(f'No progress file found, starting from {DEFAULT_START_INDEX}')
				return DEFAULT_START_INDEX
	except Exception as e:
		print(f"Error loading progress file: {e}")

		return 1


def save_progress(index, filename=PROGRESS_FILE_PATH):
	try:
		with open(filename, 'w') as progress_file:
			progress_file.write(str(index + 1))
			return True
	except Exception as e:
		print(f"Error saving progress file: {e}")
		return False
import os
from .config import PROGRESS_FILE_PATH, DEFAULT_START_INDEX

def load_progress(filename=PROGRESS_FILE_PATH):
    # checking if file exists to be safe
    if not os.path.exists(filename):
        print(f"No progress file found. Starting from {DEFAULT_START_INDEX}")
        return DEFAULT_START_INDEX

    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not content:
                return DEFAULT_START_INDEX
            
            progress_val = int(content)
            print(f"Progress file found! Resuming from: {progress_val}")
            return progress_val
            
    except (ValueError, OSError) as e:
        print(f"Warning: Could not parse progress file ({e}). Starting from {DEFAULT_START_INDEX}")
        return DEFAULT_START_INDEX

def save_progress(index, filename=PROGRESS_FILE_PATH):
    try:
        # temp file hack to prevent corruption
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, 'w') as f:
            f.write(str(index))
        
        os.replace(temp_filename, filename)
        return True
    except OSError as e:
        print(f"Error saving progress: {e}")
        # temp file cleanup in case weirdness happens
        try:
            os.remove(temp_filename)
        except OSError:
            pass
        return False
# Furtrack Downloader

A Python-based web scraper and image downloader for FurTrack. This tool allows you to scrape character tags and image URLs from FurTrack pages and download the associated images.

## Features

- **Web Scraping**: Extracts character tags and image URLs from FurTrack pages using an undetected Chrome driver
- **Progress Tracking**: Automatically saves your progress, allowing you to resume from where you left off
- **CSV Export**: Stores scraped data in a structured CSV format
- **Logging**: Comprehensive logging to both console and file
- **Error Handling**: Robust error handling and recovery mechanisms

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/furtrack-downloader.git
cd furtrack-downloader
```

2. Install dependencies:
```bash
pip install -e .
```

Or if using `pyproject.toml`:
```bash
pip install .
```

## Usage

Run the application:
```bash
python -m furtrack_downloader
```

### Menu Options

1. **Scrape Tags** - Extract character tags and image URLs from FurTrack
   - Specify a maximum index (or press Enter for default: 1,000,000)
   - Progress is automatically saved and can be resumed

2. **Run Downloader** - Download images (feature in development)

3. **Exit** - Close the application

## Configuration

Edit [`src/furtrack-downloader/config.py`](src/furtrack-downloader/config.py) to customize:

- `BASE_URL` - FurTrack URL format
- `DEFAULT_START_INDEX` - Starting index for scraping (default: 10)
- `DEFAULT_MAX_INDEX` - Maximum index to scrape (default: 1,000,000)
- `CSV_FILE_PATH` - Output CSV file location
- `PROGRESS_FILE_PATH` - Progress tracking file location

## Output Files

- **furtrack_image_lib.csv** - CSV file containing:
  - Index
  - Image URL
  - Character tags (comma-separated)

- **progress.arc** - Tracks the last processed index for resume functionality

- **furtrack_downloader.log** - Application logs with rotating file handler (5MB max per file)

## Project Structure

```
src/furtrack-downloader/
├── __init__.py              # Package initialization
├── __main__.py              # Entry point
├── cli.py                   # Command-line interface
├── config.py                # Configuration constants
├── scraper.py               # Web scraping logic
├── downloader.py            # Download functionality (WIP)
├── csv_handler.py           # CSV file operations
├── progress.py              # Progress tracking
├── logging_config.py        # Logging configuration
└── __pycache__/             # Compiled Python files
```

## Dependencies

- **undetected-chromedriver** - Bypass detection in web scraping
- **beautifulsoup4** - HTML parsing
- **selenium** - Web automation
- **html5lib** - HTML parser for BeautifulSoup

See [`pyproject.toml`](pyproject.toml) for complete dependency list.

## Logging

Logs are written to `furtrack_downloader.log` with the following configuration:
- **Console**: Warning level and above
- **File**: Info level and above
- **Rotation**: 5MB per file with 2 backup files

## Notes

- The scraper uses an undetected Chrome driver to avoid detection
- Images are disabled during scraping to reduce load times
- Random delays between requests are implemented for politeness
- Progress is saved automatically after each successful scrape

## Status

- ✅ Web scraping
- ✅ Progress tracking
- ✅ CSV export
- ⏳ Image downloader (in development)

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
# CIVD Tender Scraper

## Description
CIVD Tender Scraper is a Python script that scrapes tender data from the SKK Migas website. It collects information about various tenders, including title, invitation type, owner, validity date, business classification, procurement type, business field, description, and attachment URLs. The scraped data is then saved into a CSV file for further analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/alazzhras/CIVD-Tender-Scraper.git
   cd CIVD-Tender-Scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the scraper script using Python:
```bash
python scraper.py
```
The script will scrape the tender data and save it to a CSV file named `CIVD Tender List_<timestamp>.csv`.

## Dependencies
- requests
- beautifulsoup4
- pandas

## Functionality Overview
- The script sends HTTP requests to the SKK Migas website to retrieve tender data.
- It processes multiple pages of data and extracts relevant information using BeautifulSoup.
- The scraped data is saved into a CSV file with a timestamp for easy identification.

## License
This project is licensed under the MIT License.

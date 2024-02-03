# Medium Scraper

This project contains scripts for scraping Medium articles from selected publications and analysing trends in their popularity. 
It features a Python scraper to collect data and a subsequent analysis script to identify patterns in claps (likes/upvotes) and the impact of publication timing.

## Installation and Setup

### Setting Up a Virtual Environment

Before installing the required packages, it's recommended to use a virtual environment. Then run:
`pip install -r requirements.txt`

## The Scraper Script

The scraper, `medium_scraper.py`, iterates over predefined Medium publication URLs to collect articles, extracting information such as publication name, date, title, and the number of claps. 
Utilising libraries like `requests` for fetching web content and `BeautifulSoup` for HTML parsing, it's designed to handle leap years and convert day numbers to dates. 
The collected data is then saved into a CSV file within a `data` directory for organized storage and easy access.

### Key Features:
- Scrapes multiple Medium publications.
- Handles date conversion and leap years.
- Extracts article titles, publication dates, and clap counts.

### Customizing the Script

- **Saving Data**: By default, the scraped data is saved to `medium_data.csv` within a `data` directory. If the directory does not exist in your project structure, the script will create it if not present.
  
- **Changing Publication URLs**: The `urls` dictionary within the script contains the Medium publication URLs to be scraped. You can customize this list by adding or removing entries based on the publications you're interested in. For example:

  ```
  urls = {
      "Towards Data Science": "https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}",
      "UX Collective": "https://uxdesign.cc/archive/{0}/{1:02d}/{2:02d}",
      # Add or remove publications as desired
  }
  
## The Analysis Script
Following data collection, the analysis script `medium_analysis.py` loads the scraped data to perform several analyses:
- Identifies the most popular articles based on claps.
- Analyses common keywords in article titles.
- Performs a seasonal analysis to examine trends in article popularity over different months.

### Key Features:
- Uses `Pandas` for data manipulation.
- Employs `Matplotlib` and `Seaborn` for visualising trends in data.
- Identifies key patterns in article popularity and publication timing.

## Getting Started
### To run the scraper:
`python medium_scraper.py`

### To analyze the collected data:
`python medium_analysis.py`

## Caveat

The functionality of `medium_scraper.py` relies heavily on the HTML structure of Medium publication pages, specifically the CSS classes used to identify article elements. It's important to note that these classes (`"cardChromeless u-marginTop20 u-paddingTop10 u-paddingBottom15 u-paddingLeft20 u-paddingRight20"`) are subject to change. If Medium updates their site's design or structure, the scraper may not function as intended until it is updated to match the new HTML structure.

### What to Do If the Scraper Breaks Due to Changes on Medium:

1. **Inspect the Medium Page**: Use your browser's developer tools to inspect the article elements on Medium and identify the new CSS classes or HTML structure.
2. **Update the CSS Selectors**: Modify the `soup.find_all()` calls in `medium_scraper.py` to use the updated CSS classes or element identifiers.
3. **Test the Scraper**: Run the scraper again to ensure it's functioning correctly with the updated selectors.

## Enjoy 🙃

# Wikipedia Scientist Scraper

- This repository contains code for collecting and processing data about scientists from the Wikipedia API
- Focus on separate genders

## Overview

The purpose of this project is to extract time-based revision data of Wikipedia articles for a sampled set of male and female scientists. The collected data can then be used for computational social science research or similar analytical purposes.

## Scripts

### `query_people.py`
Used to query the Wikipedia database for 1000 male and 1000 female scientists— and save their names for further processing.

### `main.py`
Main scraping script. Fetches revision history and article intros for each individual during specified time and time interval. Stores gender along with other metadata for each revision.

### `data_cleaner.py`
Cleans up raw intro text by removing links and such


## Output

- `scraped.json`: Raw collected data with timestamps, intros, gender, and interval metadata.
- `cleaned.json`: Cleaned version of the intros, stripped of Wikipedia syntax.


Install dependencies with:

```bash
pip install -r requirements.txt

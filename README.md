# Scraper-Mail-Sender

This script allows the automatic collection of information, and it will then send it via email to a specifiec recipient.
The collected text is encoded using *UTF8*, so there are no compatibility issues when the text contains characters such as *ä, ö, ü, €* etc.

## Requirements:
```
Bs4
Requests
```

## Sample Scraper - countryScraper.py
The file ```countryScraper.py``` is designed to scrape the current cases of Covid-19 per 100'000 citizens in european countries, and report if any of them have a rate of over 60 as prescribed by the Swiss Government.

It also lists the official Swiss "Red List", which dictates, from which country returning citizens have to go into self quarantine for 14 days (All in German).

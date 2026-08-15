import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR/"output"/"reports"

# ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- SCRAPING TARGET CONFIGURATIONS ---

# 1. Sri Lanka Source: Colombo Stock exchange (CSE) Announcements
CSE_CONFIG = {
    "url":"https://www.cse.lk/announcements/?category=CORPORATE%20DISCLOSURE",
    "region":"Sri Lanka",
    "source":"Colombo Stock Exchange",
    "limit": 10,
    # DOM Selection for CSE
    "selectors":{
        "table_row":"tbody tr",
        "title": "td:nth-child(2)",
        "date": "td:nth-child(1)",
        "link":"td:nth-child(2) a"
    }
}

# 2. Global Source: Yahoo Finance Stock Market News
YAHOO_CONFIG = {
    "url":"https://finance.yahoo.com/topic/stock-market-news/",
    "region":"Global",
    "source": "Yahoo Finance",
    "limit": 10,
    # DOM Selection for yahoo Finance
    "selectors":{
        "new_card":"section[data-testid='news-stream'] li, ul.stream-items > li",
        "title":"h3",
        "date":"div.publishing, span.date",
        "link":"a"
    }
}

# --- PLAYWRIGHT BROWSER SETTINGS ---
BROWSER_SETTINGS = {
    "headlines": True,
    "timeout":3000,
    "user_agent":(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64 "
        "AppleWebKet/537.36 (KHML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# --- Report Settings ---
TODAY_DATE = datetime.now().strftime("%d-%m-%Y")
EXCEL_FILE_NAME = "Top_20_Stock_Market_News.xlsx"
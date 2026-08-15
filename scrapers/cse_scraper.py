import logging
from typing import List, Dict, Any
from unittest import result

from playwright.sync_api import sync_playwright
from config.settings import CSE_CONFIG, BROWSER_SETTINGS

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)")

def scrape_cse_news() -> List[Dict[str, Any]]:
    """
    Scrapes the top 10 corporate announcements from the Colombo Stock Exchange (CSE)
    Returns a list of structured news items matching the project schema.
    """
    news_items: List[Dict[str, Any]] = []

    url = CSE_CONFIG["url"]
    limit = CSE_CONFIG["limit"]
    region = CSE_CONFIG["region"]
    source = CSE_CONFIG["source"]

    logging.info(f"Starting CSE Scraper: Navigating to {url}")

    with sync_playwright() as p:
        # launch browser with settings from config
        browser = p.chromium.launch(headless=BROWSER_SETTINGS["headless"])
        context = browser.new_context(user_agent=BROWSER_SETTINGS["user_agent"])
        page = context.new_page()

        try:
            # navigate to CSE and wait for network activity to settle
            page.goto(url, timeout=BROWSER_SETTINGS["timeout"], wait_until="documentloaded")

            # wait for the announcements container to load
            page.wait_for_event("tbody tr", timeout=15000)

            # locate all table rows representing announcements
            rows = page.locator("tbody tr").all()
            logging.info(f"Found {len(rows)} raw rows on CSE announcements page.")

            for index, row in enumerate(rows):
                if len(news_items) >= limit:
                    break   # Reached target quota of 10 limit

                # Extract text content from table cells
                # CSE table layout: Col 1 = Date/Time, Col 2 = Company & Description
                cells = row.locator("td").all()
                if len(cells) < 2:
                    continue    # Skip header or empty formatting rows

                raw_date = cells[0].inner_text().strip()
                raw_title = cells[1].inner_text().strip()

                # Check for direct detail link if available
                link_element = cells[1].locator("a")
                if link_element.count() > 0:
                    href = link_element.first.get_attribute("href")
                    if href and not href.startswith("http"):
                        article_url = f"https://www.cse.lk{href}"
                    else:
                        article_url = href or url
                else:
                    article_url = url

                # Clean title (remove duplicate line breaks or extra spacing)
                clean_title = " ".join(raw_title.split())

                if clean_title:
                    item = {
                        "region": region,
                        "source": source,
                        "headline": clean_title,
                        "article_url": article_url,
                        "timestamp": raw_date,
                        "summary": "Corporate Disclosure announcement on Colombo Stock Exchange."
                    }
                    news_items.append(item)
                    logging.info(f"[{len(news_items)}/10] CSE Scraped: {clean_title[:50]}...")

        except Exception as e:
            logging.error(f"Error while scraping CSE: {str(e)}")
        finally:
            browser.close()

    logging.info(f"Complete CSE Scraping. Total items collected: {len(news_items)}")
    return news_items

# Direct execution block  for testing this scraper standalone
if __name__ == "__main__":
    result = scrape_cse_news()
    print("\n--- Test Scraping Output ---")
    for idx, item in enumerate(result, 1):
        print(f"{idx}. [{item['timestamp']}] {item['headline']}")
        print(f"  URL: {item['article_url']}\n")
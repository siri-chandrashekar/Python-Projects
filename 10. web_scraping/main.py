import requests
from bs4 import BeautifulSoup
import csv


def scrape_bbc_us_canada():
    url = "https://www.bbc.com/news"
    base_url = "https://www.bbc.com"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; bbc-scraper/1.0)"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    seen = set()  # to avoid duplicates

    # find all cards
    cards = soup.find_all(
        lambda tag: tag.has_attr('data-testid') and tag['data-testid'].endswith('-card')
    )

    for card in cards:

        # headline
        h2 = card.find('h2', {'data-testid': 'card-headline'})
        if not h2:
            continue
        headline = h2.text.strip()

        # link
        a_tag = card.find('a', href=True)
        link = a_tag['href'] if a_tag else None

        if link and link.startswith('/'):
            link = base_url + link

        # category
        category_tag = card.find('span', {'data-testid': 'card-metadata-tag'})
        category = category_tag.text.strip() if category_tag else None

        # fallback (extra safety)
        if not category and link and "us_and_canada" in link:
            category = "US & Canada"

        # filter + deduplicate
        if category == "US & Canada" and link not in seen:
            seen.add(link)

            data.append({
                "headline": headline,
                "category": category,
                "url": link
            })

    return data


def save_to_csv(data, filename="bbc_us_canada_news.csv"):
    with open(filename, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["headline", "category", "url"])
        writer.writeheader()
        writer.writerows(data)


# run
if __name__ == "__main__":
    news_data = scrape_bbc_us_canada()
    if news_data:
        save_to_csv(news_data)
        print(f"Saved {len(news_data)} articles to CSV.")
    else:
        print("No articles were saved. Check your connection or BBC page structure.")




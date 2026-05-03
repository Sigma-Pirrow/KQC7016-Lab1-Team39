import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import collections

# -- Part 1: Setup
BASE_URL = "https://quotes.toscrape.com/page/{}/"
_HERE = os.path.dirname(os.path.abspath(__file__))

# -- Part 2: Scrape All 10 Pages
print("\n*** Scraping All Pages (1-10) ***")
all_records = []

for page_num in range(1, 11):
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        break

    for quote in quotes:
        text   = quote.find("span", class_="text")
        author = quote.find("small", class_="author")
        tags   = quote.find_all("a", class_="tag")

        quote_text  = text.text.strip()
        author_name = author.text.strip()
        tag_list    = [tag.text for tag in tags]
        tag_str     = ", ".join(tag_list)

        all_records.append({"quote": quote_text, "author": author_name, "tags": tag_str})

    print(f"  Page {page_num}: {len(quotes)} quotes scraped")
    time.sleep(0.3)

print(f"\nTotal quotes scraped: {len(all_records)}")

# -- Part 3: Filter Inspirational Quotes
print("\n*** Filtering 'Inspirational' Quotes ***")
inspirational = [r for r in all_records if "inspirational" in r["tags"]]
print(f"Found {len(inspirational)} inspirational quotes:\n")
for r in inspirational:
    print("Quote: ", r["quote"])
    print("Author:", r["author"])
    print()

# -- Part 4: Statistics
print("*** Statistics ***")
authors    = [r["author"] for r in all_records]
all_tags   = []
for r in all_records:
    all_tags.extend([t.strip() for t in r["tags"].split(",") if t.strip()])

top_authors = collections.Counter(authors).most_common(5)
top_tags    = collections.Counter(all_tags).most_common(5)

print("Top 5 Authors by Quote Count:")
for author, count in top_authors:
    print(f"  {author}: {count} quotes")

print("\nTop 5 Tags:")
for tag, count in top_tags:
    print(f"  {tag}: {count} quotes")

# -- Part 5: Save to CSV
output_all = os.path.join(_HERE, "scraped_quotes.csv")
with open(output_all, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_records)

output_filtered = os.path.join(_HERE, "inspirational_quotes.csv")
with open(output_filtered, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
    writer.writeheader()
    writer.writerows(inspirational)

print(f"\n[Saved] {len(all_records)} quotes -> scraped_quotes.csv")
print(f"[Saved] {len(inspirational)} inspirational quotes -> inspirational_quotes.csv")
print("\n*** END ***")
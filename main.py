from sources.web_scraper import WebScraper
from exporters.csv_exporter import CSVExporter
from exporters.xml_exporter import XMLExporter
from exporters.json_exporter import JSONExporter
import pandas as pd
import os
from datetime import datetime

def main():
    url = input("Enter a URL to scrape: ")
    scraper = WebScraper(url)
    df = scraper.fetch_data()

    if df.empty:
        print(" No data was scraped.")
        return

    print(f" Scraped {len(df)} links")
    print(df.head())

    print("Choose export format:")
    print("1 = CSV")
    print("2 = XML")
    print("3 = JSON")
    choice = input("Enter 1,2 or 3 : ").strip()

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        output_file = os.path.join("outputs", f"scrape_{timestamp}.csv")
        exporter = CSVExporter()
    elif choice == "2":
        output_file = os.path.join("outputs", f"scrape_{timestamp}.xml")
        exporter = XMLExporter()
    elif choice == "3":
        output_file = os.path.join("outputs", f"scrape_{timestamp}.json")
        exporter = JSONExporter()
    else:
        print(" Invalid choice. Defaulting to CSV.")
        output_file = os.path.join("outputs", f"scrape_{timestamp}.csv")
        exporter = CSVExporter()

    exporter.export(df, output_file)


if __name__ == "__main__":
    main()

import pandas as pd

from bs4 import BeautifulSoup
import requests

class FilterManager:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    
    def preview (self, df: pd.DataFrame, n = 5):
        print(f"\n Preview {n} rows: ")
        print(df.head(n))
        print(f"\nTotal rows: {len(df)}")


    def filter_links(self):
        if "link" in self.df.columns:
            return self.df[self.df["link"].notnull()]
        print("No links found")
        return self.df
    
    def filter_headings(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        data = []
        for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            data.append({"heading" : h.text.strip()})
        return pd.DataFrame(data)       
    
    def filter_paragraphs(self, url:str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        data = [{"paragraph" : p.text.strip()} for p in soup.find_all("p")]
        return pd.DataFrame(data)
    
    def filter_by_keyword(self, keyword: str):
        text_cols = [c for c in self.df.columns if "text" in c.lower()]
        if not text_cols:
            print("no text found")
            return self.df
        mask = pd.concat(
            [self.df[col].str.lower().str.contains(keyword.lower(), na = False) for col in text_cols],
            axis = 1
        ).any(axis=1)
        return self.df[mask]
    
    def select_filter(self, url:str):
        while True:
            print("\n How woulf you like to extract data?")
            print("1 = Links<a>")
            print("2 = Headings <h1> - <h6>")
            print("3 = Paragraphs <p>")
            print("4 = Search by keyword (from scraped data)")
            print("5 = All scraped text (no filter)")

            choice = input("Enter choice: ").strip()
            filtered_df = self.df

            if choice == "1":
                filtered_df = self.filter_links()
            elif choice == "2":
                filtered_df = self.filter_headings(url)

            elif choice == "3":
                filtered_df = self.filter_paragraphs(url)
            
            elif choice == "4":
                keyword = input("Enter keywords that should be scraped").strip()
                filtered_df = self.filter_by_keyword(keyword)
            
            elif choice == "5":
                filtered_df = self.df
            
            else:
                print("Invalid choice")
                continue

            self.preview(filtered_df)

            happy = input("\nAre you happy with this data? (y/n):").strip().lower()
            if happy == "y":
                print("Filter confirmed")
                return filtered_df
            else:
                print("Try another filter")

        

import requests
from bs4 import BeautifulSoup
import pandas as pd
from .base_source import BaseSource

class WebScraper(BaseSource):

    def __init__(self, url: str):
        super().__init__("Website")
        self.url = url


    def _get_soup(self):
        response = requests.get(self.url)
        response.raise_for_status()    
        return BeautifulSoup(response.text, "lxml")

    def fetch_data(self, mode: str = "links", keyword: str = None) -> pd.DataFrame:  
        soup = self._get_soup()
        data = []

        if mode == "links":
            for a in soup.find_all("a", href=True):
                text = a.get_text(strip=True)
                href = a["href"]
                data.append({"text": text, "href": href})

        elif mode == "headings":
            for h in soup.find_all(["h1","h2","h3","h4","h5","h6"]):
                data.append({"heading": h.get_text(strip=True)})


        elif mode == "paragraphs":
            for p in soup.find_all("p"):
                data.append({"paragraph": p.get_text(strip=True)})
        
        elif mode == "keyword" and keyword:
            keyword_lower = keyword.lower()
            for tag in soup.find_all(True):
                text = tag.get_text("", strip=True)
                if keyword_lower in text.lower():
                    data.append({"matching_text" : text})
        
        elif mode == "all":
            all_text = soup.get_text(separator="\n", strip=True)
            for line in all_text.splitlines():
                data.append({"text": line})
        
        else:
            print(f"Unknown mode {mode}")
            return pd.DataFrame()
        
        return pd.DataFrame(data)

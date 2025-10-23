import requests
from bs4 import BeautifulSoup
import pandas as pd
from .base_source import BaseSource

class WebScraper(BaseSource):

    def __init__(self, url: str):
        super().__init__("Website")
        self.url = url

    def fetch_data(self) -> pd.DataFrame:  
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")  # parses html/xml

            data = [] #to store the scraped links 
            #ovde treba da ja implementiram logikata za filters 
            # #probno samo za headers:

            for a in soup.find_all("a", href=True):
                text = a.text.strip() or "(empty)"
                href = a["href"]
                data.append({"text": text, "link": href})

            df = pd.DataFrame(data)
            return df
        
        except requests.exceptions.RequestException as e:
            print("some err")
            return pd.DataFrame()

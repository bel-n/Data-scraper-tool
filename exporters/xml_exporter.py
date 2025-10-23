from .base_exporter import BaseExporter
import pandas as pd
from bs4 import BeautifulSoup

class XMLExporter(BaseExporter):
    def export(self, df: pd.DataFrame, filename : str):
        soup = BeautifulSoup(features="xml")

        root = soup.new_tag("items")
        soup.append(root)

        for _,row in df.iterrows():
            item_tag = soup.new_tag("item")
            for col in df.columns:
                child_tag = soup.new_tag(col)
                child_tag.string = str(row[col])
                item_tag.append(child_tag)
        root.append(item_tag)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        
        print(f" Data exported to {filename} (XML)")
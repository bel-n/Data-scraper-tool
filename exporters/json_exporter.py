from .base_exporter import BaseExporter
import pandas as pd
import json

class JSONExporter(BaseExporter):
    def export(self, df: pd.DataFrame, filename: str):
               with open(filename, "w", encoding="utf-8") as f:
                json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
                print(f"Data exported to {filename} (JSON)")
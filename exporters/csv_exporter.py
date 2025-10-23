from exporters.base_exporter import BaseExporter
import pandas as pd

class CSVExporter(BaseExporter):
    def export(self, df, filename):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

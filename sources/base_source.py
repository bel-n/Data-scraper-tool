from abc import ABC, abstractmethod
import pandas as pd


class BaseSource(ABC):

    def __init__(self, source_name : str):
        self.source_name = source_name

        @abstractmethod
        def fetch_data(self) -> pd.DataFrame:
            pass
    

#this methods do nothing, other classes will implement them
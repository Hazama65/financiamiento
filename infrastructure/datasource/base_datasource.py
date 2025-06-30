
from abc import ABC, abstractmethod
import pandas as pd

class BaseDataSource(ABC):
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        pass
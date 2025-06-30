# infrastructure/datasource/excel_datasource.py

import pandas as pd
import unidecode
from .base_datasource import BaseDataSource

class ExcelMultiTableDataSource(BaseDataSource):
    def __init__(self, file_map: dict):
        self.file_map = file_map

    def clean_column(self, col):
        col = unidecode.unidecode(col).strip().lower()
        col = col.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace(":", "")
        return col

    def load_data(self) -> dict:
        tablas = {}
        for table_name, path in self.file_map.items():
            df = pd.read_excel(path)
            df.columns = [self.clean_column(c) for c in df.columns]
            df.dropna(how='all', inplace=True)
            df = df.reset_index(drop=True)

            print(f"{table_name} cargado con shape: {df.shape}")
            tablas[table_name] = df
        return tablas

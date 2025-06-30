import pandas as pd
import unidecode
from sqlalchemy import create_engine

class PostgresDataRepository:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def _clean_column(self, col):
        col = unidecode.unidecode(col).strip().lower()
        return col.replace(" ", "_").replace("\n", "_").replace("(", "").replace(")", "").replace("/", "_").replace(":", "")

    def save_dataframe(self, table_name: str, df: pd.DataFrame):
        df.dropna(how='all', inplace=True)
        df.columns = [self._clean_column(col) for col in df.columns]
        df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)



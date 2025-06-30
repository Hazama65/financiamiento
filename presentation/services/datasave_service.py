
class DataSaverService:
    def __init__(self, repository):
        self.repository = repository

    def save_all(self, tablas_dict: dict[str, 'pd.DataFrame']):
        for table_name, df in tablas_dict.items():
            self.repository.save_dataframe(table_name, df)
            
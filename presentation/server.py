from flask import Flask
from presentation.routes import Routes
from presentation.services.loging_service import LoggingService
from presentation.services.query_service import QueryService

import pandas as pd
from sqlalchemy import create_engine

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.logger = LoggingService().get_logger()
        self.data_total = self._cargar_datos()

        # print(self.data_total)

        self.query_service = QueryService(self.data_total, self.logger)

        self._configure_routes()

    def _configure_routes(self):
        Routes(self.app, self.query_service)

    def _cargar_datos(self):
        try:
            self.logger.info("Cargando datos desde PostgreSQL...")
            engine = create_engine("postgresql://postgres:123456@localhost:5432/Financiamiento")

            df1 = pd.read_sql_table("datos_operacion", con=engine)
            df2 = pd.read_sql_table("output", con=engine)
            df3 = pd.read_sql_table("cifras_control", con=engine)
            df4 = pd.read_sql_table("incidentes", con=engine)

            max_len = max(len(df1), len(df2), len(df3), len(df4))
            df1 = df1.reset_index(drop=True).reindex(range(max_len))
            df2 = df2.reset_index(drop=True).reindex(range(max_len))
            df3 = df3.reset_index(drop=True).reindex(range(max_len))
            df4 = df4.reset_index(drop=True).reindex(range(max_len))

            df_total = pd.concat([df1, df2, df3, df4], axis=1)
            self.logger.info("Datos cargados correctamente.")
            return df_total
        except Exception as e:
            self.logger.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()

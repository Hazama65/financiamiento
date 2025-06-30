from pandas_nql import PandasNQL, BedrockSqlGenerator
from unidecode import unidecode

class QueryService:
    def __init__(self, data, logger):
        self.data = data
        self.logger = logger

    def ejecutar_query(self, query_str):
        query_str = unidecode(query_str).upper()
        self.logger.debug("Input usuario: %s", query_str)

        pandas_nql = PandasNQL(self.data, generator=BedrockSqlGenerator())
        results = pandas_nql.query(query_str)
        results_df = results[0]

        if results_df.empty:
            results_str = "No encontré datos para tu consulta, por favor intenta refrasearla."
        elif results_df.shape[0] == 1:
            results_str = results_df.iloc[0].to_string().strip()
        else:
            results_df = results_df.head(50)
            results_str = results_df.to_string().strip()

        self.logger.debug("Resultados query: %s", results_str)
        answer = pandas_nql.answer(query_str, results_str)
        self.logger.debug("Respuesta: %s", answer)
        return answer

    def info_dataframe(self):
        return {
            "columnas": list(self.data.columns),
            "total_filas": len(self.data)
        }

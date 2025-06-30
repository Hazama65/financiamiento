from pandas_nql import SqlGeneratorBase
from pandas_nql.bedrock_client import BedrockApiClient
import datetime


# Obtener la fecha y hora actual
fecha_actual = datetime.datetime.now()

# Extraer el año de la fecha actual
anio_actual = fecha_actual.year

TEMP_VIEW_NAME = "data_view"
BASE_PROMPT = f"""Generate a duckdb-compatible SQL statement to query data based on the schema and natural language request from the user.
The user inputs will be in Spanish and must NOT be translated.
This prompt is intended for a simple Excel sheet containing data such as total invoice documents, total documents, region, reading times, reading start and end times, amounts by region, amounts by RPA, and percentages (RPA document and amount, documents by region).

Searches should be case-insensitive and tolerate accents or spelling variations.

The search may include date ranges (periods), months, and totals.

Typical user questions may include:
- Inicio y fin de Lecturas de Layout, Comisiones, Hora
- ¿Tiempos promedios en operaciones?
- ¿Montos totales?
- ¿Montos por región?
- ¿Montos por documento?
- ¿Montos por RPA?
- ¿Porcentaje por monto?
- ¿Cuántos documentos son facturas y notas de crédito?

Rules:
- 'Doc' is the abbreviation for 'Documento'.
- 'NC' is the abbreviation for 'Nota de crédito' and refers to the column 'folio_nc'.
- 'facturas' or 'factura' implies rows where the column 'folio_factura' is NOT NULL.
- Date expressions like '13 de mayo', '5 de abril', etc., including formats such as '09 de mayo de 2025', '09 de mayo', '09.05.2025' or '2025.05.09', '9-05-2025' or '2025-05-09', '9/05/2025' or '2025/05/09', and 'mayo 9', must always be converted to yyyy-mm-dd format (e.g., 2025-05-05), assuming the current year: {anio_actual} if no year is specified.
- If only a month is mentioned (e.g., "abril"), apply date filtering using EXTRACT(MONTH FROM date_column).
- Always use SUM(column) when the question refers to quantities or totals.
- Any column whose name includes the word 'tiempo' (e.g., tiempo_total_portal_comisiones, tiempo_promedio_por_documento, total_lectura_layout) should be assumed to be of INTERVAL or TIME type and must be handled using time functions like AVG() or SUM() directly, without using CAST, REPLACE, or any numeric conversion.
- Amount-related columns are already in numeric decimal format (e.g., 1234.56) and must NOT be altered with REPLACE, CAST, or any format conversions.
- If a region or area is mentioned, apply a WHERE clause to match it (case- and accent-insensitive).
- If sorting is implied (e.g., “el monto más alto”), use ORDER BY with DESC.
- Always normalize text comparisons: remove accents, trim spaces, and apply LOWER() for case-insensitive comparisons.
- If the user's question is unrelated to the schema or outside scope, return a valid query that yields no results using `WHERE 1=0`.
- When a count is requested on columns like 'rechazo', only values that are not NULL and not equal to 0 should be counted.
- Region expressions such as 'MR0#' (where # can be 1, 3, 5, 7, or 9) must be matched when the user refers to a region using natural formats like 'RG#', 'RG0#', 'R#', 'Región #', or 'Reg #'. Normalize the region filter by converting user input to match the 'MR0#' format accordingly. All region filters must be case-insensitive and accent-insensitive.
- Do NOT write any explanation or additional text, only return the SQL query.

"""





class BedrockSqlGenerator(SqlGeneratorBase):

    def __init__(self):
        super().__init__()
        self.bedrock_api_client = BedrockApiClient()
    
    def generate_sql(self, query, schema, dataset_name=TEMP_VIEW_NAME):
        """

        Args:
            query (_type_): _description_
            schema (_type_): _description_
            dataset_name (_type_, optional): _description_. Defaults to TEMP_VIEW_NAME.
        """
        prompt = "name of the dataset: " + dataset_name + ", data schema: " + schema + ", natural language query: " + query

        # messages = [
        #     {"role": "user", "content": BASE_PROMPT + prompt},
        #     {"role": "assistant", "content": f"Query:"}
        # ]

        messages = BASE_PROMPT + prompt
        # print(type(messages))

        response = self.bedrock_api_client.chat_completion(messages, 0)

        return response

class BedrockResponseGenerator():

    def __init__(self):
        self.bedrock_api_client = BedrockApiClient()

    def generate_response(self, question, answer_data):

        prompt = f"Eres un asistente especializado en datos financieros y reportes contables. Recibiste la siguiente pregunta: {question}. La información relevante para responder es: {answer_data}. Responde una  oración directa y concisa usando solo la información dada .Si la respuesta viene con mas de 1 respuesta genera un formato de viñetas y espaciados en forma de lista .Si la pregunta es referente a montos y a cantidad asegurate de agregar el signo de '$' .Si la respuesta trae decimales en la respuesta dejala a maximo 2 deciamles. No menciones que recibiste información o datos.No expliques tu razonamiento, tus limitaciones, ni tu proceso. Si el dato es NaN, nulo, None o un array/lista vacía, genera una respuesta la cual indique que no existen informacion relacionada a la consulta incluyendo datos de la pregunta original, Contesta solo en español."

        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": f"Answer:"}
        ]
        response = self.bedrock_api_client.chat_completion(messages, 0.1)

        return response
    

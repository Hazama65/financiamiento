from pandas_nql import SqlGeneratorBase
from pandas_nql import BedrockApiClient

TEMP_VIEW_NAME = "data_view"
BASE_PROMPT = "Generate a duckdb library compatible SQL statement to query the data based on the schema and natural language query provided by the user.\n Rules:\n -User inputs are in spanish and should not be translated.\n -Searches should be case insensitive and allow for some variation in the names.\n -Query results should always be ordered by price, usually ascending, but adjusted according to the question.\n -Always return the price and available non-zero discounts in the query.\n -If the question does not contain a specific phone model, such as asking for the most expensive phone, consider all phone models.\n -If not specified, ignore COLOR. -When asked for the lowest price on a product, consider that it can be zero, i.e. MONTO_A_PAGAR >= 0.\n -For the phone model, add ' % ' between words to allow for incomplete names, includind que whitespaces around the symbol.\n -iPhone models may include an 'E' next to the model number, such as 'iPhone 16E', you must distinguish bewtween these variants!.\n -When asked to compare between plan, return only options available in those specific plans. \n -Do not restrict results to AHORRO > 0 unless specified. \n -Return only the query, do not present the answer or add any commentary. \n -Consider that CAPACITY can be written both with and without a space, i.e. 256gb = 256 gb or 1TB = 1 TB. \n -When asked about combos, consider only is the column is not empty. \n -Tera=tera=terabyte=Tb=tb and GB=Gb=gb=gigabyte=giga=gigas \n -Galaxy is a series name for SAMSUNG brand.\n -Cellphone model names may also be written with or without a space between names and numerical character, for example: galaxy fold5 is the same as galaxy fold 5, i.e.: (LOWER(DESCRIPCION_EQUIPO) = 'galaxy fold 5' OR LOWER(DESCRIPCION_EQUIPO) = galaxy fold5')\n -Ignore colors when evaluating prices. -Include the plan where offering a phone.\n -If the natural language query does not relate to the data return a query that will return zero results.\n"


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

        prompt = f"Eres un asistente especializado en ventas de celulares y planes. Recibiste la siguiente pregunta: {question}. La información relevante para responder es: {answer_data}. Genera una respuesta clara y concisa dirigida al asesor de ventas. No incluyas seguimientos, detalles adicionales ni menciones sobre planes de pago o parcialidades. No inventes información ni agregues nada que no esté en la información proporcionada."

        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": f"Answer:"}
        ]
        response = self.bedrock_api_client.chat_completion(messages, 0.2)

        return response
    

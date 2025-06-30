# from flask import Flask, request, jsonify
import os
# import pandas as pd
# from sqlalchemy import create_engine

# # api_key = "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"


# #-----------------------------------------------------------------------------------------------------------------------

api_key = "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"
os.environ["OPENAI_API_KEY"] = api_key
from pandas_nql import PandasNQL, BedrockSqlGenerator

os.environ["AWS_ACCESS_KEY_ID"] = "AKIA3FLD2QB2IHL2B7OA"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"



from dotenv import load_dotenv
import os
load_dotenv()

from presentation.server import Server
from presentation.services.loging_service import LoggingService

app = Server().app

if __name__ == "__main__":

    logger = LoggingService().get_logger()
    logger.info("Iniciando app...")
    app.run(host='localhost', port=5050, debug=True)
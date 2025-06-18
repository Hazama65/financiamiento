from flask import Flask, request, jsonify
import os
import pandas as pd
from unidecode import unidecode
from sqlalchemy import create_engine
import logging
# api_key = "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"

logging.basicConfig(filename='cotizador_backend.log',
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    force=True)
#-----------------------------------------------------------------------------------------------------------------------

api_key = "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"
os.environ["OPENAI_API_KEY"] = api_key
from pandas_nql import PandasNQL, BedrockSqlGenerator
# os.environ["AWS_ACCESS_KEY_ID"] = "AKIARFL4OUUPKNSB4G5G"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

os.environ["AWS_ACCESS_KEY_ID"] = "AKIA3FLD2QB2C2TX326B"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"


# Load data once--------------------------
logging.info('Cargando información ...')
# Seccion de carga de datos por medio de postgres


def cargar_datos_desde_postgres():
    try:
        engine = create_engine("postgresql://postgres:1234..@localhost:5432/Financiamiento")

        df1 = pd.read_sql_table("datosoperacion", con=engine)
        df2 = pd.read_sql_table("comisiones", con=engine)
        df3 = pd.read_sql_table("cifrascontrol", con=engine)

        # Asegurar misma longitud (rellenar con NaNs si es necesario)
        max_len = max(len(df1), len(df2), len(df3))
        df1 = df1.reset_index(drop=True).reindex(range(max_len))
        df2 = df2.reset_index(drop=True).reindex(range(max_len))
        df3 = df3.reset_index(drop=True).reindex(range(max_len))

        # Combinar horizontalmente
        df_total = pd.concat([df1, df2, df3], axis=1)

        logging.info("Datos de las 3 tablas cargados y combinados correctamente.")
        return df_total

    except Exception as e:
        logging.error(f"Error al cargar y unir tablas desde PostgreSQL: {e}")
        return pd.DataFrame()




data_total = cargar_datos_desde_postgres()
print("Filas cargadas:", len(data_total))  # Esto debería mostrar cuántas filas hay

#-------------------------------------  

app = Flask(__name__)

logging.info('Cargando app...')


# Ruta 1
@app.route('/query', methods=['POST'])
def query_total():
    query_str = unidecode(request.json.get('query')).upper()
    return jsonify({"data": ejecutar_query(data_total, query_str)})


@app.route('/info_dataframe', methods=['GET'])
def info_dataframe():
    columnas = list(data_total.columns)
    num_filas = len(data_total)
    return jsonify({"columnas": columnas, "total_filas": num_filas})



# Función para consulta
def ejecutar_query(data, query_str):
    logging.debug("Input usuario: %s", query_str)
    pandas_nql = PandasNQL(data, generator=BedrockSqlGenerator())
    results = pandas_nql.query(query_str)
    results_df = results[0]

    if results_df.empty:
        results_str = "No encontré datos para tu consulta, por favor intenta refrasearla."
    elif results_df.shape[0] == 1:
        results_str = results_df.iloc[0].to_string().strip()
    else:
        results_df = results_df.head(50)
        results_str = results_df.to_string().strip()

    logging.debug("Resultados query: %s", results_str)
    answer = pandas_nql.answer(query_str, results_str)
    logging.debug("Respuesta: %s", answer)
    return answer



if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)
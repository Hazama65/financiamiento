from flask import jsonify
import os
from infrastructure.datasource.excel_datasource import ExcelMultiTableDataSource
from infrastructure.repository.postgres_repository import PostgresDataRepository
from presentation.services.datasave_service import DataSaverService

class DataController:
    def __init__(self):
        conn_str = "postgresql://postgres:123456@localhost:5432/Financiamiento"
        repository = PostgresDataRepository(conn_str)
        self.saver = DataSaverService(repository)

    def cargar_excel_a_postgres(self):
        base_path = os.path.join(os.path.dirname(__file__), '../../files')

        file_map = {
            "datos_operacion": os.path.join(base_path, "Datosoperacion.xlsx"),
            "output": os.path.join(base_path, "output.xlsx"),
            "cifras_control": os.path.join(base_path, "cifras control.xlsx"),
            "incidentes": os.path.join(base_path, "Incidentes.xlsx")
        }

        data_source = ExcelMultiTableDataSource(file_map)
        tablas = data_source.load_data()
        self.saver.save_all(tablas)

        return jsonify({"message": "✅ Datos guardados en PostgreSQL correctamente."}), 200

# presentation/controllers/user_controller.py
from flask import request, jsonify
from unidecode import unidecode
from presentation.services.loging_service import LoggingService

class QueryController:

    def __init__(self, query_service):
        self.query_service = query_service
        self.logger_service = LoggingService()
    
    def get_query(self):
        logger = self.logger_service.get_logger()  

        input_usuario = unidecode(request.json.get('query')).upper()
        logger.info(f"Input usuario: {input_usuario}")
        
        print(self.query_service)
        return jsonify({"message": self.query_service.ejecutar_query(input_usuario)}), 200
    


# presentation/routes_users.py
from presentation.seedData.data_controller import DataController

class RegisterDataRoutes:
    def __init__(self, app):
        controller = DataController()
        app.add_url_rule('/creardata', view_func=controller.cargar_excel_a_postgres, methods=['POST'])
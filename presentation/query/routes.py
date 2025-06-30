# presentation/routes_users.py
from presentation.query.controllers.query_controller import QueryController

class QueryRoutes:
    def __init__(self, app, query_service):
        query_controller = QueryController(query_service)
        app.add_url_rule('/query', view_func=query_controller.get_query, methods=['POST'])
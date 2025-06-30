# presentation/routes.py
from presentation.query.routes import QueryRoutes

from presentation.seedData.routes import RegisterDataRoutes
class Routes:
    def __init__(self, app, query_service):
        self.app = app
        self.query_service = query_service
        self._register_all_routes()

    def _register_all_routes(self):
        QueryRoutes(self.app, self.query_service)
        RegisterDataRoutes(self.app)

